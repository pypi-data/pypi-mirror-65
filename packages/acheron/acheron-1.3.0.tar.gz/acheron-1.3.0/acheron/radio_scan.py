import bisect
import collections
import datetime
import logging
import time
import threading

from PySide2 import QtCore, QtGui, QtWidgets

import asphodel
from hyperborea.preferences import read_bool_setting
import hyperborea.proxy

from .ui_radio_scan_dialog import Ui_RadioScanDialog

logger = logging.getLogger(__name__)


instances = {}


ScanResult = collections.namedtuple(
    "ScanResult", ["active_scan", "serial_number", "is_bootloader",
                   "device_mode", "scan_strength", "last_seen", "user_tag_1",
                   "user_tag_2", 'board_info', 'build_info', 'build_date',
                   'has_bootloader'])


def start_radio_scan_manager(device, *args, **kwargs):
    device_logger = hyperborea.proxy.get_device_logger(logger, device)
    device_logger.info("Starting radio scan manager")

    if device in instances:
        stop_radio_scan_manager(device)

    instance = RadioScanManager(device, device_logger, *args, **kwargs)
    instances[device] = instance
    instance.start()

    hyperborea.proxy.register_local_cleanup(stop_radio_scan_manager, device)


def stop_radio_scan_manager(device):
    if device not in instances:
        return

    instances[device].stop()

    device_logger = hyperborea.proxy.get_device_logger(logger, device)
    device_logger.info("Stopped radio scan manager")

    del instances[device]

    hyperborea.proxy.unregister_local_cleanup(stop_radio_scan_manager, device)


class RadioScanManager:
    def __init__(self, device, logger, status_pipe, control_pipe):
        self.device = device
        self.remote = device.get_remote_device()
        self.logger = logger
        self.status_pipe = status_pipe
        self.control_pipe = control_pipe

        self.supports_scan_power = True
        self.power_max_queries = min(
            self.device.get_max_outgoing_param_length() // 4,
            self.device.get_max_incoming_param_length())

        self.finished = threading.Event()
        self.scan_thread = threading.Thread(target=self.scan_thread_run)

    def start(self):
        self.scan_thread.start()
        self.remote.open()

    def stop(self):
        self.finished.set()

        # note: need to release the lock while waiting for the thread to finish
        hyperborea.proxy.device_lock.release()
        self.scan_thread.join()
        hyperborea.proxy.device_lock.acquire()

        self.remote.close()
        self.status_pipe.close()
        self.control_pipe.close()

    def do_active_scan(self, request):
        sn, is_boot = request
        try:
            if not is_boot:
                self.device.connect_radio(sn)
            else:
                self.device.connect_radio_boot(sn)

            self.remote.wait_for_connect(1000)

            tag_locations = self.remote.get_user_tag_locations()
            try:
                t1 = self.remote.read_user_tag_string(*tag_locations[0])
            except UnicodeDecodeError:
                t1 = None
            try:
                t2 = self.remote.read_user_tag_string(*tag_locations[1])
            except UnicodeDecodeError:
                t2 = None
            board_info = self.remote.get_board_info()
            build_info = self.remote.get_build_info()
            build_date = self.remote.get_build_date()
            has_bootloader = bool(self.remote.get_bootloader_info())

            last_seen = datetime.datetime.now(datetime.timezone.utc)
            s = ScanResult(True, sn, is_boot, None, None, last_seen, t1, t2,
                           board_info, build_info, build_date, has_bootloader)
            self.status_pipe.send(s)

        except:
            # couldn't do the active scan
            # no big deal
            pass
        finally:
            self.device.stop_radio()

    def collect_scan_results(self):
        last_seen = datetime.datetime.now(datetime.timezone.utc)

        # get the results
        results = self.device.get_radio_extra_scan_results()

        # get the scan powers
        scan_powers = {}  # key: sn, value: power dBm
        if self.supports_scan_power:
            try:
                for i in range(0, len(results), self.power_max_queries):
                    result_subset = results[i:i + self.power_max_queries]
                    serials = [r.serial_number for r in result_subset]
                    powers = self.device.get_radio_scan_power(serials)
                    for sn, power in zip(serials, powers):
                        if power != 0x7F:
                            scan_powers[sn] = power
            except asphodel.AsphodelError as e:
                if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
                    self.supports_scan_power = False
                else:
                    raise

        for r in results:
            power = scan_powers.get(r.serial_number, None)
            is_bootloader = bool(r.asphodel_type &
                                 asphodel.ASPHODEL_PROTOCOL_TYPE_BOOTLOADER)
            s = ScanResult(None, r.serial_number, is_bootloader, r.device_mode,
                           power, last_seen, None, None, None, None, None,
                           None)
            self.status_pipe.send(s)

    def scan_thread_run(self):
        try:
            active_scans = collections.deque()

            with hyperborea.proxy.device_lock:
                self.device.start_radio_scan()

            # next allowable time to stop the scan
            scan_stop = time.time() + 0.6

            restart_scan = False

            while not self.finished.is_set():
                if restart_scan:
                    with hyperborea.proxy.device_lock:
                        self.device.start_radio_scan()
                    restart_scan = False

                # poll control pipe
                while True:
                    if self.control_pipe.poll():
                        try:
                            request = self.control_pipe.recv()
                            active_scans.append(request)
                        except EOFError:
                            # pipe broken, treat it like a stop call
                            self.finished.set()
                            break
                    else:
                        break

                if self.finished.is_set():
                    with hyperborea.proxy.device_lock:
                        self.device.stop_radio()
                    break

                # collect all scan results from the device
                with hyperborea.proxy.device_lock:
                    self.collect_scan_results()

                if time.time() < scan_stop:
                    # not enough time scanning
                    continue

                # do all active scan connects
                while not self.finished.is_set():
                    try:
                        request = active_scans.popleft()
                    except IndexError:
                        # no (more) devices
                        break

                    with hyperborea.proxy.device_lock:
                        self.do_active_scan(request)
                    restart_scan = True

                if self.finished.is_set():
                    with hyperborea.proxy.device_lock:
                        self.device.stop_radio()
                    break

                # do a boot scan
                with hyperborea.proxy.device_lock:
                    self.device.start_radio_scan_boot()
                    end_time = time.time() + 0.1
                    while time.time() < end_time:
                        if self.finished.is_set():
                            break
                        self.collect_scan_results()
                restart_scan = True
                scan_stop = time.time() + 0.6

        except:
            self.logger.exception("Unhandled exception in scan_thread_run")
            self.status_pipe.send("error")


class RadioScanTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_level = 0

        self.scan_list = []

        self.header = ["Serial", "Strength", "Tag 1", "Tag 2",
                       "Board Info", "Build Info", "Build Date", "Bootloader",
                       "Device Mode", "Last Seen"]

        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.update_timer_cb)

        self.last_sort_col = 0
        self.last_sort_reverse = False

    def rowCount(self, parent):
        return len(self.scan_list)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None

        scan_result = self.scan_list[index.row()]
        col = index.column()

        if role == QtCore.Qt.BackgroundRole:
            if scan_result.is_bootloader:
                return QtGui.QColor(QtCore.Qt.yellow)
            elif col == 9:
                now = datetime.datetime.now(datetime.timezone.utc)
                delta = now - scan_result.last_seen
                seconds = int(delta.total_seconds())
                if seconds > 30:
                    return QtGui.QColor(QtCore.Qt.red)
                elif seconds > 10:
                    return QtGui.QColor(QtCore.Qt.yellow)
            return None
        if role == QtCore.Qt.FontRole:
            if col == 7:
                if scan_result.is_bootloader:
                    font = QtGui.QFont()
                    font.setBold(True)
                    return font
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None

        if col == 0:  # Serial Number
            return str(scan_result.serial_number)
        elif col == 1:  # Radio Strength
            if scan_result.scan_strength is not None:
                return "{} dBm".format(scan_result.scan_strength)
        elif col == 2:  # User Tag 1
            if scan_result.user_tag_1:
                return scan_result.user_tag_1
        elif col == 3:  # User Tag 2
            if scan_result.user_tag_2:
                return scan_result.user_tag_2
        elif col == 4:  # Board Info
            if scan_result.board_info:
                return "{} rev {}".format(*scan_result.board_info)
        elif col == 5:  # Build Info
            if scan_result.build_info:
                return scan_result.build_info
        elif col == 6:  # Build Info
            if scan_result.build_date:
                return scan_result.build_date
        elif col == 7:  # Bootloader
            if scan_result.is_bootloader:
                return "Running"
            elif scan_result.has_bootloader is True:
                return "Capable"
            elif scan_result.has_bootloader is False:
                return "Not Capable"
        elif col == 8:  # Device Mode
            return str(scan_result.device_mode)
        else:  # Last Seen
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - scan_result.last_seen
            seconds = int(delta.total_seconds())
            return str("{}s ago".format(seconds))
        return None

    def flags(self, index):
        if not index.isValid():
            return None

        scan_result = self.scan_list[index.row()]
        if scan_result.scan_strength is None:
            # radio doesn't support scan strength
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        elif scan_result.scan_strength < self.filter_level:
            # too low, don't enable
            return QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self.header[col]
        return None

    def get_sort_key(self, col):
        def get_key(attrs):
            def f(scan_result):
                values = (getattr(scan_result, attr) for attr in attrs)
                comparable_values = ((v is None, v) for v in values)

                if scan_result.scan_strength is None:
                    filtered = False
                else:
                    filtered = scan_result.scan_strength < self.filter_level

                return [filtered, tuple(comparable_values)]
            return f

        if col == 0:  # Serial Number
            return get_key(["serial_number"])
        elif col == 1:  # Radio Strength
            return get_key(["scan_strength"])
        elif col == 2:  # User Tag 1
            return get_key(['user_tag_1'])
        elif col == 3:  # User Tag 2
            return get_key(['user_tag_2'])
        elif col == 4:  # Board Info
            return get_key(['board_info'])
        elif col == 5:  # Build Info
            return get_key(['build_info'])
        elif col == 6:  # Build Date
            return get_key(['build_date'])
        elif col == 7:  # Bootloader
            return get_key(['is_bootloader', 'has_bootloader'])
        elif col == 8:  # Device Mode
            return get_key(['device_mode'])
        else:  # Last Seen
            return get_key(['last_seen'])

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()

        reverse = (order == QtCore.Qt.DescendingOrder)

        self.last_sort_col = col
        self.last_sort_reverse = reverse

        self.scan_list.sort(key=self.get_sort_key(col), reverse=reverse)

        self.layoutChanged.emit()

    def create_updated_result(self, original, new):
        d = original._asdict()
        for key, value in new._asdict().items():
            if value is not None:
                d[key] = value
        return ScanResult(**d)

    def insert_scan_result(self, scan_result):
        if not self.scan_list:
            # first entry
            self.update_timer.start(1000)

        original_index = None
        for i, s in enumerate(self.scan_list):
            if s.serial_number == scan_result.serial_number:
                # have a duplicate
                original_index = i
                scan_result = self.create_updated_result(s, scan_result)
                break

        key = self.get_sort_key(self.last_sort_col)
        keys = [key(s) for s in self.scan_list]

        if original_index is not None:
            del keys[original_index]

        new_index = bisect.bisect_right(keys, key(scan_result))

        parent = QtCore.QModelIndex()
        if original_index is not None:
            if original_index == new_index:
                # just an update
                top_left_index = self.index(original_index, 0)
                bottom_right_index = self.index(original_index,
                                                len(self.header) - 1)
                self.scan_list[original_index] = scan_result
                self.dataChanged.emit(top_left_index, bottom_right_index)
            else:
                if new_index < original_index:
                    move_index = new_index
                else:
                    move_index = new_index + 1
                self.beginMoveRows(parent, original_index, original_index,
                                   parent, move_index)
                del self.scan_list[original_index]
                self.scan_list.insert(new_index, scan_result)
                self.endMoveRows()
        else:
            self.beginInsertRows(parent, new_index, new_index)
            self.scan_list.insert(new_index, scan_result)
            self.endInsertRows()

    def mark_for_rescan(self, scan_result):
        index = None
        for i, s in enumerate(self.scan_list):
            if s.serial_number == scan_result.serial_number:
                index = i
                break

        d = s._asdict()
        d['active_scan'] = None

        top_left_index = self.index(index, 0)
        bottom_right_index = self.index(index, len(self.header) - 1)
        self.scan_list[index] = ScanResult(**d)
        self.dataChanged.emit(top_left_index, bottom_right_index)

    def has_active_scan(self, serial_number):
        for s in self.scan_list:
            if s.serial_number == serial_number:
                return (s.active_scan is True)

    def clear_scan_results(self):
        if self.scan_list:
            self.layoutAboutToBeChanged.emit()
            self.scan_list.clear()
            self.layoutChanged.emit()
        self.update_timer.stop()

    def update_timer_cb(self):
        start_index = self.index(0, 7)
        end_index = self.index(len(self.scan_list), 7)
        self.dataChanged.emit(start_index, end_index)

    def set_filter_level(self, new_filter_level):
        filtered_by_old = set()
        filtered_by_new = set()
        for scan_result in self.scan_list:
            if scan_result.scan_strength < self.filter_level:
                filtered_by_old.add(scan_result)
            if scan_result.scan_strength < new_filter_level:
                filtered_by_new.add(scan_result)

        if filtered_by_new != filtered_by_old:
            self.layoutAboutToBeChanged.emit()
            self.filter_level = new_filter_level
            self.scan_list.sort(key=self.get_sort_key(self.last_sort_col),
                                reverse=self.last_sort_reverse)
            self.layoutChanged.emit()
        else:
            self.filter_level = new_filter_level


class RadioScanDialog(QtWidgets.QDialog, Ui_RadioScanDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.status_pipe = None
        self.control_pipe = None

        self.settings = QtCore.QSettings()

        self.setupUi(self)
        self.extra_ui_setup()

        self.status_timer = QtCore.QTimer(self)
        self.status_timer.timeout.connect(self.status_timer_cb)

        self.selection_changed()

    def extra_ui_setup(self):
        self.table_model = RadioScanTableModel(self)
        self.tableView.setModel(self.table_model)

        header = self.tableView.horizontalHeader()
        header.setResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.clearButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Reset)
        self.clearButton.setText(self.tr("Clear"))
        self.clearButton.clicked.connect(self.table_model.clear_scan_results)

        self.filterSlider.valueChanged.connect(self.set_filter_level)
        self.activeScan.toggled.connect(self.set_active_scan)

        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed)
        self.tableView.doubleClicked.connect(self.double_click_cb)

    def double_click_cb(self, index=None):
        self.accept()

    def get_selected_scan_result(self):
        selected_devices = []
        for index in self.tableView.selectionModel().selectedRows():
            selected_devices.append(self.table_model.scan_list[index.row()])
        return selected_devices[0]

    def selection_changed(self, selected=None, deselected=None):
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if self.tableView.selectionModel().hasSelection():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    def status_timer_cb(self):
        while self.status_pipe.poll():
            try:
                message = self.status_pipe.recv()
                if isinstance(message, ScanResult):
                    scan_result = message
                    self.table_model.insert_scan_result(scan_result)

                    if self.activeScan.isChecked():
                        has_active_scan = self.table_model.has_active_scan(
                            scan_result.serial_number)
                        if not has_active_scan:
                            self.control_pipe.send((scan_result.serial_number,
                                                    scan_result.is_bootloader))
                else:
                    # error
                    self.stop_scan()
                    return
            except EOFError:
                break

    def set_filter_level(self, value):
        self.table_model.set_filter_level(value)
        self.settings.setValue("ScanFilterLevel", value)

    def set_active_scan(self, junk=None):
        value = 1 if self.activeScan.isChecked() else 0
        self.settings.setValue("ActiveScan", value)

    def start_scan(self, status_pipe, control_pipe):
        # read check boxes and filter slider states from settings
        active_scan = read_bool_setting(self.settings, "ActiveScan", False)
        self.activeScan.setChecked(active_scan)
        filter_level = self.settings.value("ScanFilterLevel")
        if filter_level is not None:
            try:
                filter_level = int(filter_level)
            except:
                filter_level = self.filterSlider.minimum()  # default
        else:
            filter_level = self.filterSlider.minimum()  # default
        self.filterSlider.setValue(filter_level)

        self.status_pipe = status_pipe
        self.control_pipe = control_pipe
        self.status_timer.start(20)  # 20 milliseconds

    def stop_scan(self):
        self.status_timer.stop()
        self.status_pipe = None
        self.control_pipe = None

    def mark_for_rescan(self, scan_result):
        self.table_model.mark_for_rescan(scan_result)
