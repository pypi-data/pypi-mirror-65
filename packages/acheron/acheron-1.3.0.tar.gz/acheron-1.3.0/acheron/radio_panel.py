import enum
import functools
import logging
import multiprocessing
import time

from PySide2 import QtCore, QtWidgets

import hyperborea.proxy

from . import bootloader
from . import radio_scan
from .bulk_update_firmware import BulkUpdateFirmwareDialog
from .ui_radio_panel import Ui_RadioPanel

logger = logging.getLogger(__name__)


def finish_scan(device):
    device.stop_radio()
    results = device.get_radio_scan_results()
    return results


def create_remote(device):
    remote = device.get_remote_device()
    remote.open()
    return remote


def bulk_claim(device):
    device_logger = hyperborea.proxy.get_device_logger(logger, device)
    remote = device.get_remote_device()
    remote.open()

    try:
        to_claim = set()

        device.start_radio_scan()
        finish = time.monotonic() + 1
        while finish > time.monotonic():
            for result in device.get_radio_extra_scan_results():
                if result.device_mode:
                    to_claim.add(result.serial_number)
        device.stop_radio()

        if not to_claim:
            device_logger.info("No Devices to Claim")
        else:
            for serial_number in to_claim:
                try:
                    device_logger.info("Claiming %s...", serial_number)
                    device.connect_radio(serial_number)
                    remote.wait_for_connect(5000)
                    remote.set_device_mode(0)
                    device_logger.info("Claimed %s", serial_number)
                except:
                    device_logger.error("Error Claiming %s", serial_number)
            device_logger.info("Finished Bulk Claim")
    finally:
        device.stop_radio()
        remote.close()


class PipeWithSerial:
    def __init__(self, pipe):
        self.pipe = pipe
        self.serial_number = 0

    def send(self, message):
        if isinstance(message, str):
            new_message = "{}: {}".format(self.serial_number, message)
            self.pipe.send(new_message)
        else:
            self.pipe.send(message)

    def close(self):
        # ignore close calls, the pipe will be reused
        pass


def bulk_update(device, progress_pipe, cancel_pipe, firm_data, valid_range,
                device_mode, radio_strength):
    canceled = False
    pipe_with_serial = PipeWithSerial(progress_pipe)
    device_logger = hyperborea.proxy.get_device_logger(logger, device)
    remote = device.get_remote_device()
    remote.open()

    power_max_queries = min(device.get_max_outgoing_param_length() // 4,
                            device.get_max_incoming_param_length())

    scanned = 0
    to_program = 0
    ignored = 0
    finished = 0
    errors = 0

    try:
        # all of these contain elements of (sn, app_mode)
        unknown_serials = set()
        reprogram_serials = set()

        scan_powers = {}  # key: sn, value: power dBm

        progress_pipe.send("Scanning for bootloaders...")
        device.start_radio_scan_boot()
        finish = time.monotonic() + 1  # 1 second
        while finish > time.monotonic():
            unknown_powers = []
            for result in device.get_radio_extra_scan_results():
                if result.serial_number in valid_range:
                    unknown_serials.add((False, result.serial_number))
                    if result.serial_number not in scan_powers:
                        unknown_powers.append(result.serial_number)
            # get the powers
            if radio_strength is not None:
                for i in range(0, len(unknown_powers), power_max_queries):
                    serials = unknown_powers[i:i + power_max_queries]
                    powers = device.get_radio_scan_power(serials)
                    for sn, power in zip(serials, powers):
                        if power != 0x7F:
                            scan_powers[sn] = power
        device.stop_radio()

        progress_pipe.send("Scanning for devices...")
        device.start_radio_scan()
        finish = time.monotonic() + 2  # 2 seconds
        while finish > time.monotonic():
            unknown_powers = []
            for result in device.get_radio_extra_scan_results():
                if result.serial_number in valid_range:
                    unknown_serials.add((True, result.serial_number))
                    if result.serial_number not in scan_powers:
                        unknown_powers.append(result.serial_number)
            # get the powers
            if radio_strength is not None:
                for i in range(0, len(unknown_powers), power_max_queries):
                    serials = unknown_powers[i:i + power_max_queries]
                    powers = device.get_radio_scan_power(serials)
                    for sn, power in zip(serials, powers):
                        if power != 0x7F:
                            scan_powers[sn] = power
        device.stop_radio()

        # filter by radio strength
        if radio_strength is not None:
            for app_mode, serial_number in unknown_serials.copy():
                if serial_number in scan_powers:
                    if scan_powers[serial_number] < radio_strength:
                        unknown_serials.remove((app_mode, serial_number))

        if not unknown_serials:
            device_logger.info("No Devices Found")
            return

        scanned = len(unknown_serials)

        for app_mode, serial_number in sorted(unknown_serials):
            try:
                # connect
                progress_pipe.send("Querying {}...".format(serial_number))
                if app_mode:
                    device.connect_radio(serial_number)
                else:
                    device.connect_radio_boot(serial_number)
                remote.wait_for_connect(5000)

                if app_mode and remote.get_bootloader_info() != "Asphodel":
                    device_logger.info(
                        "{} doesn't have a bootloader".format(serial_number))
                    continue

                # see if the firmware is supported
                board_info = remote.get_board_info()
                for rev, board_name in firm_data['board']:
                    if (rev == board_info[1] and
                            board_name == board_info[0]):
                        break
                else:
                    device_logger.info("{} isn't a supported board".format(
                        serial_number))
                    continue

                if firm_data['chip'] != remote.get_chip_model():
                    device_logger.info("{} doesn't have correct chip".format(
                        serial_number))
                    continue

                in_bootloader = remote.supports_bootloader_commands()
                device_info = {'supports_bootloader': in_bootloader,
                               'build_info': remote.get_build_info(),
                               'build_date': remote.get_build_date()}
                if bootloader.already_programmed(firm_data, device_info):
                    device_logger.info("{} already programmed".format(
                        serial_number))
                    continue

                reprogram_serials.add((app_mode, serial_number))
            except:
                device_logger.info("Error Querying {}".format(serial_number))

        if not reprogram_serials:
            device_logger.info("No Valid Devices Found")
            return

        to_program = len(reprogram_serials)
        ignored = scanned - to_program

        device_logger.info(
            "Bulk Update: scanned=%s, ignored=%s, to_program=%s", scanned,
            ignored, to_program)

        for app_mode, serial_number in sorted(reprogram_serials):
            if cancel_pipe.poll():
                progress_pipe.send("Cancelling...")
                canceled = True
                break

            try:
                tries = 2
                while True:
                    try:
                        # connect
                        progress_pipe.send((0, 0))
                        progress_pipe.send("Connecting to {}...".format(
                            serial_number))
                        if app_mode:
                            device.connect_radio(serial_number)
                        else:
                            device.connect_radio_boot(serial_number)
                        remote.wait_for_connect(5000)

                        # bootloader
                        pipe_with_serial.serial_number = serial_number
                        bootloader.do_bootload(remote, firm_data,
                                               pipe_with_serial)

                        # device mode
                        if device_mode is not None:
                            remote.set_device_mode(device_mode)
                    except:
                        tries -= 1
                        if tries == 0:
                            raise
                        else:
                            continue
                    break
                finished += 1
                device_logger.info("Finished {}".format(serial_number))
            except:
                errors += 1
                device_logger.exception("Error Programming {}".format(
                    serial_number))
    finally:
        progress_pipe.close()
        device.stop_radio()
        remote.close()

    device_logger.info(
        "Bulk Update: scanned=%s, ignored=%s, finished=%s, errors=%s", scanned,
        ignored, finished, errors)

    if canceled:
        device_logger.info("Canceled Bulk Update")
    else:
        device_logger.info("Finished Bulk Update")


@enum.unique
class RadioState(enum.Enum):
        UNINITIALIZED = 0
        DISCONNECTED = 1
        CONNECTING = 2
        CONNECTED = 3
        SCANNING = 4


class RadioPanel(QtWidgets.QGroupBox, Ui_RadioPanel):
    def __init__(self, start_usb_operation, parent=None):
        super().__init__(parent)

        self.device_tab = parent
        self.start_usb_operation = start_usb_operation

        self.radio_scan_dialog = None

        self.state = RadioState.UNINITIALIZED

        self.last_connect_op = None
        self.last_connect_sn = None

        self.no_streaming = False

        self.connect_available = False
        self.remote_tab = None

        self.setupUi(self)
        self.extra_ui_setup()

        self.setup_callbacks()
        self.setup_usb_operations()

    def extra_ui_setup(self):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction(self.actionConnectNoStreaming)
        self.menu.addSeparator()
        self.menu.addAction(self.actionBulkClaim)
        self.menu.addAction(self.actionBulkUpdateFirmware)
        self.menu.addSeparator()
        self.menu.addAction(self.actionConnectAnyBootloader)
        self.menu.addAction(self.actionConnectSpecificBootloader)
        self.menu.addAction(self.actionBootloaderScan)
        self.advancedMenuButton.setMenu(self.menu)

        self.bulk_update_progress = QtWidgets.QProgressDialog(
            self.tr(""), self.tr("Cancel"), 0, 100)
        self.bulk_update_progress.setWindowTitle(self.tr("Bulk Update"))
        self.bulk_update_progress.setWindowModality(QtCore.Qt.WindowModal)
        self.bulk_update_progress.setMinimumDuration(0)
        self.bulk_update_progress.setAutoReset(False)
        self.bulk_update_progress.canceled.connect(self.bulk_update_canceled)
        self.bulk_update_progress.reset()

    def setup_callbacks(self):
        self.devicesComboBox.currentIndexChanged.connect(self.combo_changed)
        self.detailScanButton.clicked.connect(self.detail_scan)
        self.scanButton.clicked.connect(self.start_scan)
        self.connectButton.clicked.connect(self.connect_button_cb)
        self.disconnectButton.clicked.connect(self.disconnect_button_cb)
        self.goToRemoteButton.clicked.connect(self.show_remote_tab)

        self.scan_timer = QtCore.QTimer(self)
        self.scan_timer.timeout.connect(self.scan_timer_cb)
        self.connect_check_timer = QtCore.QTimer(self)
        self.connect_check_timer.timeout.connect(self.connect_check_timer_cb)

        self.actionConnectNoStreaming.triggered.connect(
            self.connect_no_streaming_cb)
        self.actionConnectAnyBootloader.triggered.connect(
            self.connect_any_bootloader_cb)
        self.actionConnectSpecificBootloader.triggered.connect(
            self.connect_specific_bootloader_cb)
        self.actionBootloaderScan.triggered.connect(self.start_scan_boot)
        self.actionBulkClaim.triggered.connect(self.start_bulk_claim)
        self.actionBulkUpdateFirmware.triggered.connect(
            self.start_bulk_update_firmware)

        self.bulk_update_progress_timer = QtCore.QTimer(self)
        self.bulk_update_progress_timer.timeout.connect(
            self.bulk_update_progress_cb)

    def setup_usb_operations(self):
        self.start_scan_op = hyperborea.proxy.SimpleDeviceOperation(
            "start_radio_scan")
        self.start_scan_op.completed.connect(self.start_scan_cb)
        self.start_scan_boot_op = hyperborea.proxy.SimpleDeviceOperation(
            "start_radio_scan_boot")
        self.start_scan_boot_op.completed.connect(self.start_boot_scan_cb)
        self.stop_op = hyperborea.proxy.SimpleDeviceOperation("stop_radio")
        self.finish_scan_op = hyperborea.proxy.DeviceOperation(finish_scan)
        self.finish_scan_op.completed.connect(self.finish_scan_cb)

        self.connect_radio_op = hyperborea.proxy.SimpleDeviceOperation(
            "connect_radio")
        self.connect_radio_op.completed.connect(self.connect_radio_cb)
        self.connect_radio_boot_op = hyperborea.proxy.SimpleDeviceOperation(
            "connect_radio_boot")
        self.connect_radio_boot_op.completed.connect(self.connect_radio_cb)
        self.get_status_op = hyperborea.proxy.SimpleDeviceOperation(
            "get_radio_status")
        self.get_status_op.completed.connect(self.get_status_cb)

        self.start_detail_scan_op = hyperborea.proxy.DeviceOperation(
            radio_scan.start_radio_scan_manager)
        self.stop_detail_scan_op = hyperborea.proxy.DeviceOperation(
            radio_scan.stop_radio_scan_manager)
        self.stop_detail_scan_op.completed.connect(self.stop_detail_scan_cb)

        self.bulk_claim_op = hyperborea.proxy.DeviceOperation(bulk_claim)
        self.bulk_claim_op.completed.connect(self.bulk_claim_cb)
        self.bulk_update_op = hyperborea.proxy.DeviceOperation(bulk_update)
        self.bulk_update_op.completed.connect(self.bulk_update_cb)

    def add_ctrl_var_widget(self, widget):
        self.ctrlVarLayout.addWidget(widget)

    def do_start_operation(self, operation, sn):
        self.last_connect_op = operation
        self.last_connect_sn = sn
        self.start_usb_operation(operation, sn)

    def do_stop_operation(self, operation):
        self.last_connect_op = None
        self.last_connect_sn = None
        self.start_usb_operation(operation)

    def go_to_disconnected_state(self):
        # no device is connected; not scanning; may have scan results
        self.state = RadioState.DISCONNECTED

        self.connect_available = True

        self.devicesComboBox.setEnabled(True)
        self.detailScanButton.setEnabled(True)
        self.scanButton.setEnabled(True)
        self.actionBootloaderScan.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.goToRemoteButton.setEnabled(False)
        self.actionConnectAnyBootloader.setEnabled(True)
        self.actionConnectSpecificBootloader.setEnabled(True)
        self.actionBulkClaim.setEnabled(True)
        self.actionBulkUpdateFirmware.setEnabled(True)

        self.scanButton.setText(self.tr("Scan"))
        self.connectButton.setText(self.tr("Connect"))

        if self.devicesComboBox.currentText() == "":
            self.connectButton.setEnabled(False)
            self.actionConnectNoStreaming.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)
            self.actionConnectNoStreaming.setEnabled(True)

        self.device_tab.rgb_remote_disconnected()

    def go_to_connecting_state(self):
        # trying to connect to a device
        self.state = RadioState.CONNECTING

        self.connect_available = False

        self.devicesComboBox.setEnabled(True)
        self.detailScanButton.setEnabled(False)
        self.scanButton.setEnabled(False)
        self.actionBootloaderScan.setEnabled(False)
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(True)
        self.goToRemoteButton.setEnabled(False)
        self.actionConnectNoStreaming.setEnabled(False)
        self.actionConnectAnyBootloader.setEnabled(False)
        self.actionConnectSpecificBootloader.setEnabled(False)
        self.actionBulkClaim.setEnabled(False)
        self.actionBulkUpdateFirmware.setEnabled(False)

        self.scanButton.setText(self.tr("Scan"))
        self.connectButton.setText(self.tr("Connecting..."))

        self.device_tab.rgb_remote_disconnected()

    def go_to_connected_state(self):
        # device is connected
        self.state = RadioState.CONNECTED

        self.connect_available = False

        self.devicesComboBox.setEnabled(True)
        self.detailScanButton.setEnabled(False)
        self.scanButton.setEnabled(False)
        self.actionBootloaderScan.setEnabled(False)
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(True)
        self.goToRemoteButton.setEnabled(True)
        self.actionConnectNoStreaming.setEnabled(False)
        self.actionConnectAnyBootloader.setEnabled(False)
        self.actionConnectSpecificBootloader.setEnabled(False)
        self.actionBulkClaim.setEnabled(False)
        self.actionBulkUpdateFirmware.setEnabled(False)

        self.scanButton.setText(self.tr("Scan"))
        self.connectButton.setText(self.tr("Connected"))

        self.device_tab.rgb_remote_connected()

    def go_to_scanning_state(self):
        # scanning for devices; not connected or disconnected
        self.state = RadioState.SCANNING

        self.connect_available = False

        self.devicesComboBox.clear()
        self.devicesComboBox.setEnabled(True)
        self.detailScanButton.setEnabled(False)
        self.scanButton.setEnabled(False)
        self.actionBootloaderScan.setEnabled(False)
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.goToRemoteButton.setEnabled(False)
        self.actionConnectNoStreaming.setEnabled(False)
        self.actionConnectAnyBootloader.setEnabled(False)
        self.actionConnectSpecificBootloader.setEnabled(False)
        self.actionBulkClaim.setEnabled(False)
        self.actionBulkUpdateFirmware.setEnabled(False)

        self.scanButton.setText(self.tr("Scanning..."))
        self.connectButton.setText(self.tr("Connect"))

        self.device_tab.rgb_remote_disconnected()

    def connected(self, device_info):
        # the device has been reconnected
        self.devicesComboBox.clear()
        self.go_to_disconnected_state()
        self.has_scan_power = device_info['radio_scan_power']
        default_serial = device_info['radio_default_serial'] & 0xFFFFFFFF
        if default_serial == 0:
            self.start_scan()
        else:
            self.no_streaming = False
            self.devicesComboBox.addItem(str(default_serial))
            self.devicesComboBox.setCurrentIndex(0)
            self.do_start_operation(self.connect_radio_op, default_serial)
            self.go_to_connecting_state()

    def disconnected(self):
        # the device has been disconnected (e.g. unplugged)
        self.state = RadioState.UNINITIALIZED

        if self.radio_scan_dialog:
            self.radio_scan_dialog.reject()

        self.scan_timer.stop()
        self.connect_check_timer.stop()

        self.close_remote_tab()

        self.connect_available = False

        # disable all
        self.devicesComboBox.clear()
        self.devicesComboBox.setEnabled(False)
        self.detailScanButton.setEnabled(False)
        self.scanButton.setEnabled(False)
        self.actionBootloaderScan.setEnabled(False)
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.goToRemoteButton.setEnabled(False)
        self.actionConnectNoStreaming.setEnabled(False)
        self.actionConnectAnyBootloader.setEnabled(False)
        self.actionConnectSpecificBootloader.setEnabled(False)
        self.actionBulkClaim.setEnabled(False)
        self.actionBulkUpdateFirmware.setEnabled(False)

        self.scanButton.setText(self.tr("Scan"))
        self.connectButton.setText(self.tr("Connect"))

    def stop(self):
        if self.radio_scan_dialog:
            self.radio_scan_dialog.reject()
        self.close_remote_tab()
        self.do_stop_operation(self.stop_op)

    def start_scan(self):
        self.go_to_scanning_state()
        self.do_stop_operation(self.start_scan_op)

    def start_scan_boot(self):
        self.go_to_scanning_state()
        self.do_stop_operation(self.start_scan_boot_op)

    def start_scan_cb(self):
        self.scan_timer.start(600)  # 0.6 seconds

    def start_boot_scan_cb(self):
        self.scan_timer.start(2000)  # 2.0 seconds

    def scan_timer_cb(self):
        self.start_usb_operation(self.finish_scan_op)
        self.scan_timer.stop()

    def finish_scan_cb(self, results):
        self.devicesComboBox.clear()
        for result in sorted(results):
            result_str = str(result)
            self.devicesComboBox.addItem(result_str)

        if results:
            self.devicesComboBox.setCurrentIndex(0)

        if self.state == RadioState.SCANNING:
            self.go_to_disconnected_state()

    def combo_changed(self, junk=None):
        if self.connect_available:
            if self.devicesComboBox.currentText() == "":
                self.connectButton.setEnabled(False)
                self.actionConnectNoStreaming.setEnabled(False)
            else:
                self.connectButton.setEnabled(True)
                self.actionConnectNoStreaming.setEnabled(True)

    def connect_button_cb(self):
        sn_str = self.devicesComboBox.currentText()
        try:
            sn = int(sn_str) & 0xFFFFFFFF
        except ValueError:
            # TODO: error box
            return
        self.no_streaming = False
        self.do_start_operation(self.connect_radio_op, sn)
        self.go_to_connecting_state()

    def connect_radio_cb(self):
        # immediately check the connected status
        self.connect_check_timer_cb()

    def connect_check_timer_cb(self):
        self.connect_check_timer.stop()  # will be restarted if necessary
        if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
            self.start_usb_operation(self.get_status_op)

    def get_status_cb(self, status):
        connected = status[0]
        if connected:
            self.device_tab.rgb_remote_connected()
            old_sn_str = self.devicesComboBox.currentText()
            new_sn_str = str(status[1])
            if old_sn_str != new_sn_str:
                # update serial number
                index = self.devicesComboBox.currentIndex()
                if index >= 0:
                    self.devicesComboBox.setItemText(index, new_sn_str)
                else:
                    self.devicesComboBox.clear()
                    self.devicesComboBox.addItem(new_sn_str)
                    self.devicesComboBox.setCurrentIndex(0)

            subproxy = self.device_tab.proxy.create_subproxy(create_remote)
            cb = functools.partial(self.subproxy_connected_cb, subproxy)
            subproxy.connected.connect(cb)
            subproxy.disconnected.connect(self.reconnect)
            subproxy.open_connection()
        elif status[1] == 0:
            # disconnected immediately; go straight to reconnect
            if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
                self.reconnect()
        else:
            self.connect_check_timer.start(250)  # 0.25 seconds

    def subproxy_connected_cb(self, subproxy):
        if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
            get_sn_op = hyperborea.proxy.SimpleDeviceOperation(
                "get_serial_number")
            cb = functools.partial(self.get_sn_cb, subproxy)
            get_sn_op.completed.connect(cb)
            subproxy.send_job(get_sn_op)
        else:
            subproxy.disconnected.disconnect(self.reconnect)
            subproxy.close_connection()

    def get_sn_cb(self, subproxy, serial):
        subproxy.disconnected.disconnect(self.reconnect)

        if self.state not in (RadioState.CONNECTED, RadioState.CONNECTING):
            subproxy.close_connection()
            return

        if self.remote_tab:
            self.remote_tab.set_proxy(subproxy)
            self.go_to_connected_state()
        else:
            self.remote_tab = self.device_tab.plotmain.create_tab(
                subproxy, serial, [] if self.no_streaming else True)

            # make a reference to this tab so the remote panel can function
            self.remote_tab.radio_tab = self.device_tab

            # have the remote's close button act like a disconnect press
            self.remote_tab.close_pressed.connect(self.disconnect_button_cb)

            # reconnect when it disconnects
            self.remote_tab.disconnected_signal.connect(self.reconnect)

            def recreate(new_tab):
                self.remote_tab = new_tab
                self.remote_tab.radio_tab = self.device_tab
                self.remote_tab.close_pressed.connect(
                    self.disconnect_button_cb)
                self.remote_tab.recreate.connect(recreate)
                self.remote_tab.disconnected_signal.connect(self.reconnect)

            self.remote_tab.recreate.connect(recreate)

            self.go_to_connected_state()
            self.show_remote_tab()

    def disconnect_button_cb(self):
        self.scan_timer.stop()
        self.connect_check_timer.stop()
        self.close_remote_tab()
        self.do_stop_operation(self.stop_op)
        self.go_to_disconnected_state()

    def close_remote_tab(self):
        if self.remote_tab:
            self.device_tab.plotmain.close_tab(self.remote_tab)
            self.remote_tab = None

    def show_remote_tab(self):
        if self.remote_tab:
            self.device_tab.plotmain.show_tab(self.remote_tab)

    def connect_any_bootloader_cb(self):
        self.no_streaming = False
        self.devicesComboBox.clear()
        self.devicesComboBox.addItem("Bootloader")
        self.devicesComboBox.setCurrentIndex(0)
        self.do_start_operation(self.connect_radio_boot_op, -1 & 0xFFFFFFFF)
        self.go_to_connecting_state()

    def connect_specific_bootloader_cb(self):
        sn, ok = QtWidgets.QInputDialog.getInt(
            None, self.tr("Bootloader Serial"),
            self.tr("Input bootloader serial number"))
        if not ok:
            return
        sn = sn & 0xFFFFFFFF

        self.no_streaming = False
        self.devicesComboBox.clear()
        self.devicesComboBox.addItem(str(sn))
        self.devicesComboBox.setCurrentIndex(0)
        self.do_start_operation(self.connect_radio_boot_op, sn)
        self.go_to_connecting_state()

    def reconnect(self):
        if self.last_connect_op:
            if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
                self.do_start_operation(self.last_connect_op,
                                        self.last_connect_sn)
                self.go_to_connecting_state()
                if self.remote_tab:
                    self.remote_tab.set_disconnected("Reconnecting...")
                    self.goToRemoteButton.setEnabled(True)

    def connect_no_streaming_cb(self):
        sn_str = self.devicesComboBox.currentText()
        try:
            sn = int(sn_str) & 0xFFFFFFFF
        except ValueError:
            # TODO: error box
            return
        self.no_streaming = True
        self.do_start_operation(self.connect_radio_op, sn)
        self.go_to_connecting_state()

    def detail_scan(self):
        if self.radio_scan_dialog is None:
            self.radio_scan_dialog = radio_scan.RadioScanDialog(self)

        rx, tx = multiprocessing.Pipe(False)
        self.rx_status_pipe = rx
        self.tx_status_pipe = tx
        rx, tx = multiprocessing.Pipe(False)
        self.rx_control_pipe = rx
        self.tx_control_pipe = tx

        # start the background thread
        self.start_usb_operation(self.start_detail_scan_op,
                                 self.tx_status_pipe,
                                 self.rx_control_pipe)

        # start the foreground thread
        self.radio_scan_dialog.start_scan(self.rx_status_pipe,
                                          self.tx_control_pipe)

        # run the dialog
        ret = self.radio_scan_dialog.exec_()

        # stop the background thread
        self.start_usb_operation(self.stop_detail_scan_op)

        # stop the foreground thread
        self.radio_scan_dialog.stop_scan()

        if ret == 0:
            return  # user canceled

        result = self.radio_scan_dialog.get_selected_scan_result()
        self.radio_scan_dialog.mark_for_rescan(result)

        self.devicesComboBox.clear()
        self.no_streaming = False
        self.devicesComboBox.addItem(str(result.serial_number))
        self.devicesComboBox.setCurrentIndex(0)
        if result.is_bootloader:
            self.do_start_operation(self.connect_radio_boot_op,
                                    result.serial_number)
        else:
            self.do_start_operation(self.connect_radio_op,
                                    result.serial_number)
        self.go_to_connecting_state()

    def stop_detail_scan_cb(self):
        self.rx_status_pipe.close()
        self.tx_control_pipe.close()
        self.rx_status_pipe = None
        self.tx_status_pipe = None
        self.rx_control_pipe = None
        self.tx_control_pipe = None

    def start_bulk_claim(self):
        self.go_to_scanning_state()
        self.start_usb_operation(self.bulk_claim_op)

    def bulk_claim_cb(self):
        if self.state == RadioState.SCANNING:
            self.go_to_disconnected_state()

    def start_bulk_update_firmware(self):
        dialog = BulkUpdateFirmwareDialog(self.has_scan_power,
                                          parent=self)
        ret = dialog.exec_()
        if ret == 0:
            return  # user canceled

        results = dialog.get_results()
        firm_file = results['firmware_location']

        try:
            firm_data = bootloader.decode_firm_file(firm_file)
        except:
            self.logger.exception('Error loading firmware from "%s"',
                                  firm_file)
            m = self.tr('Error loading firmware from file!').format(firm_file)
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            return

        rx, tx = multiprocessing.Pipe(False)
        self.bulk_update_rx_pipe = rx
        self.bulk_update_tx_pipe = tx
        rx, tx = multiprocessing.Pipe(False)
        self.cancel_rx_pipe = rx
        self.cancel_tx_pipe = tx

        # setup the progress dialog
        self.bulk_update_progress.setMinimum(0)
        self.bulk_update_progress.setMaximum(0)
        self.bulk_update_progress.setValue(0)
        self.bulk_update_progress.setLabelText(self.tr("Initializing..."))
        self.bulk_update_progress.forceShow()

        self.bulk_update_progress_timer.start(20)  # 20 milliseconds

        valid_range = range(results['min_serial'], results['max_serial'] + 1)

        self.go_to_scanning_state()
        self.start_usb_operation(
            self.bulk_update_op, self.bulk_update_tx_pipe, self.cancel_rx_pipe,
            firm_data, valid_range, results['device_mode'],
            results['radio_strength'])

    def bulk_update_canceled(self):
        if self.cancel_tx_pipe is not None:
            self.cancel_tx_pipe.send(True)

    def bulk_update_progress_cb(self):
        last_value = None
        while self.bulk_update_rx_pipe.poll():
            try:
                data = self.bulk_update_rx_pipe.recv()
                if isinstance(data, str):
                    self.bulk_update_progress.setLabelText(data)
                if isinstance(data, tuple):
                    self.bulk_update_progress.setMinimum(data[0])
                    self.bulk_update_progress.setMaximum(data[1])
                if isinstance(data, int):
                    last_value = data
            except EOFError:
                break
        if last_value is not None:
            self.bulk_update_progress.setValue(last_value)

    def bulk_update_cb(self):
        self.bulk_update_progress_timer.stop()
        self.bulk_update_progress.reset()

        # close the pipes
        self.bulk_update_rx_pipe.close()
        self.bulk_update_tx_pipe.close()
        self.cancel_rx_pipe.close()
        self.cancel_tx_pipe.close()
        self.cancel_rx_pipe = None
        self.cancel_tx_pipe = None

        if self.state == RadioState.SCANNING:
            self.go_to_disconnected_state()
