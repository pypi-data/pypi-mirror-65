import collections
import datetime
import functools
import io
import json
import logging
import lzma
import math
import multiprocessing
import os
import struct
import threading
import time

import numpy
from PySide2 import QtCore, QtGui, QtWidgets
import pyqtgraph

import asphodel
import hyperborea.device_info
from hyperborea.preferences import read_bool_setting
import hyperborea.proxy
import hyperborea.ringbuffer
import hyperborea.stream
import hyperborea.unit_preferences

from .calibration import CalibrationPanel
from .change_stream_dialog import ChangeStreamDialog
from .ctrl_var_panel import CtrlVarPanel
from .ctrl_var_widget import CtrlVarWidget
from .info_dialog import InfoDialog
from .hardware_tests import HardwareTestDialog
from .led_control_widget import LEDControlWidget
from .radio_panel import RadioPanel
from .remote_panel import RemotePanel
from .rf_power_panel import RFPowerPanel
from .rgb_control_widget import RGBControlWidget
from .setting_dialog import SettingDialog
from . import bootloader
from .ui_device_tab import Ui_DeviceTab

logger = logging.getLogger(__name__)


def reset_and_reconnect(device):
    device.reset()
    device.reconnect()


def explode(device):
    raise Exception("Explosion")


def write_nvm(device, new_nvm):
    device.erase_nvm()
    device.write_nvm_section(0, new_nvm)


def reset_rf_power_timeout(device, timeout):
    try:
        device.reset_rf_power_timeout(timeout)
    except asphodel.AsphodelError as e:
        if e.args[1] != "ERROR_CODE_UNIMPLEMENTED_COMMAND":
            raise


def set_device_mode(device, new_mode):
    try:
        device.set_device_mode(new_mode)
        return True, new_mode
    except asphodel.AsphodelError as e:
        if e.args[1] == "ERROR_CODE_INVALID_DATA":
            return False, new_mode
        else:
            raise


class GUILogHandler(logging.Handler):
    """
    A handler class that exposes a Qt Signal to allow thread-safe logging.
    """

    class InternalQObject(QtCore.QObject):
        loggedMessage = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.internalQObject = self.InternalQObject()
        self.loggedMessage = self.internalQObject.loggedMessage

    def emit(self, record):
        message = self.format(record)
        self.loggedMessage.emit(message)


class SimpleExceptionFormatter(logging.Formatter):
    """
    a logging.Formatter to only show basic exception info (e.g. no stack)
    """
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            import traceback
            e = traceback.format_exception_only(record.exc_info[0],
                                                record.exc_info[1])
            s = s + " " + "".join(e)
            if s[-1:] == "\n":
                s = s[:-1]
        return s


class MeasurementLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
        self.setFixedWidth(100)

        self.copy_action = QtWidgets.QAction(self)
        self.copy_action.setText(self.tr("Copy All"))
        self.copy_action.setShortcut(QtGui.QKeySequence.Copy)
        self.copy_action.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.copy_action.triggered.connect(self.copy_cb)
        self.addAction(self.copy_action)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def copy_cb(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.text())


class DeviceTab(QtWidgets.QWidget, Ui_DeviceTab):
    name_update = QtCore.Signal(str)
    close_pressed = QtCore.Signal()
    recreate = QtCore.Signal(object)
    disconnected_signal = QtCore.Signal()
    status_received = QtCore.Signal(object)
    packet_received = QtCore.Signal(object)
    log_message = QtCore.Signal(int, str)
    bootloader_progress_set_max = QtCore.Signal(int)
    bootloader_progress_set_value = QtCore.Signal(int)

    def __init__(self, is_paused, serial_number, base_dir, parent=None,
                 stream_list=True, disable_streaming=False,
                 disable_archiving=False, upload_manager=None):
        super().__init__(parent)

        self.plotmain = parent
        self.stream_list = stream_list  # NOTE: True means activate all streams
        self.disable_streaming = disable_streaming
        self.disable_archiving = disable_archiving

        self.upload_manager = upload_manager

        self.settings = QtCore.QSettings()
        self.auto_rgb = read_bool_setting(self.settings, "AutoRGB", True)
        self.downsample = read_bool_setting(self.settings, "Downsample", True)

        self.proxy = None
        self.is_paused = is_paused
        self.device_info = None
        self.serial_number = serial_number
        self.base_dir = base_dir

        self.rgb_widgets = []
        self.led_widgets = []
        self.ctrl_var_widgets = []
        self.panels = []

        self.channel_indexes = {}  # mapping from channel id to channel index
        self.channel_names = []
        self.channel_streams = []  # holds a stream id for each channel
        self.subchannel_names = []  # holds a list for each channel
        self.channel_rate_infos = []

        self.streaming = False
        self.streaming_stopped = threading.Event()
        self.status_thread = None
        self.packet_thread = None

        self.channel_samples = []
        self.channel_rates = []
        self.channel_downsample = []
        self.plot_ringbuffers = []
        self.mean_ringbuffers = []
        self.fft_ringbuffers = []
        self.fft_size = []
        self.fft_freq_axes = []
        self.fft_shortened = []
        self.time_curves = []
        self.unit_info = []  # [(str, scale)], scale is None for non-SI
        self.unit_formatters = []
        self.subchannel_fields = []  # list of tuples of (mean, std dev)
        self.legend = None

        self.last_channel_index = None  # last plotted channel

        self.saved_plot_ranges = {}

        self.lost_packet_lock = threading.Lock()
        self.lost_packet_count = 0
        self.lost_packet_last_time = None
        self.recent_lost_packet_count = 0
        self.lost_packet_deque = collections.deque()
        self.recent_lost_packet_highlight = False
        self.last_displayed_packet_count = 0
        self.last_displayed_packet_time = None

        self.setupUi(self)
        self.extra_ui_setup()

        self.setup_logging()
        self.setup_callbacks()
        self.setup_usb_operations()
        self.setup_graphics()

    def extra_ui_setup(self):
        # make status label visible (this is easily forgotten in QtDesigner)
        self.stackedWidget.setCurrentIndex(0)
        self.status_connected = False
        self.status_message = self.statusLabel.text()

        # hide status progress bar
        self.statusProgressBar.setVisible(False)

        # clear out the labels
        self.serialNumber.setText(self.serial_number)
        self.userTag1.setText("")
        self.userTag2.setText("")
        self.boardInfo.setText("")
        self.buildInfo.setText("")
        self.buildDate.setText("")
        self.bootloaderIndicator.setVisible(False)

        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction(self.actionSetUserTag1)
        self.menu.addAction(self.actionSetUserTag2)
        self.menu.addSeparator()
        self.firmware_menu = self.menu.addMenu(
            self.tr("Update Firmware"))
        self.firmware_menu.setEnabled(False)
        self.firmware_menu.addAction(self.actionFirmwareLatestStable)
        self.firmware_menu.addAction(self.actionFirmwareFromBranch)
        self.firmware_menu.addAction(self.actionFirmwareFromCommit)
        self.firmware_menu.addAction(self.actionFirmwareFromFile)
        self.advanced_menu = self.menu.addMenu(
            self.tr("Advanced Actions"))
        self.advanced_menu.addAction(self.actionForceRunBootloader)
        self.advanced_menu.addAction(self.actionForceRunApplication)
        self.advanced_menu.addAction(self.actionForceReset)
        self.advanced_menu.addAction(self.actionRaiseException)
        self.advanced_menu.addAction(self.actionRecoverNVM)
        self.menu.addAction(self.actionCalibrate)
        self.menu.addAction(self.actionEditDeviceSettings)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSetDeviceMode)
        self.menu.addAction(self.actionChangeActiveStreams)
        self.menu.addAction(self.actionRunTests)
        self.menu.addSeparator()
        self.menu.addAction(self.actionShowPacketStats)
        self.menu.addAction(self.actionShowDeviceInfo)
        self.menuButton.setMenu(self.menu)

        self.bootloader_progress = QtWidgets.QProgressDialog("", "", 0, 100)
        self.bootloader_progress.setLabelText(self.tr(""))
        self.bootloader_progress.setWindowTitle(self.tr("Firmware Update"))
        self.bootloader_progress.setCancelButton(None)
        self.bootloader_progress.setWindowModality(QtCore.Qt.WindowModal)
        self.bootloader_progress.setMinimumDuration(0)
        self.bootloader_progress.setAutoReset(False)
        self.bootloader_progress.reset()

        self.actionCalibrate.setIcon(QtGui.QIcon.fromTheme("caliper"))
        self.actionChangeActiveStreams.setIcon(QtGui.QIcon.fromTheme(
            "preferences_edit"))
        self.actionEditDeviceSettings.setIcon(QtGui.QIcon.fromTheme("gear"))
        self.actionFirmwareFromBranch.setIcon(QtGui.QIcon.fromTheme(
            "branch_view"))
        self.actionFirmwareFromCommit.setIcon(QtGui.QIcon.fromTheme(
            "symbol_hash"))
        self.actionFirmwareFromFile.setIcon(QtGui.QIcon.fromTheme(
            "document_plain"))
        self.actionFirmwareLatestStable.setIcon(QtGui.QIcon.fromTheme(
            "branch"))
        self.actionForceReset.setIcon(QtGui.QIcon.fromTheme("redo"))
        self.actionForceRunApplication.setIcon(QtGui.QIcon.fromTheme(
            "application"))
        self.actionForceRunBootloader.setIcon(QtGui.QIcon.fromTheme(
            "flash_yellow"))
        self.actionRaiseException.setIcon(QtGui.QIcon.fromTheme("bomb"))
        self.actionRecoverNVM.setIcon(QtGui.QIcon.fromTheme("document_gear"))
        self.actionRunTests.setIcon(QtGui.QIcon.fromTheme("stethoscope"))
        self.actionSetDeviceMode.setIcon(QtGui.QIcon.fromTheme(
            "text_list_numbers"))
        self.actionSetUserTag1.setIcon(QtGui.QIcon.fromTheme("tag"))
        self.actionSetUserTag2.setIcon(QtGui.QIcon.fromTheme("tag"))
        self.actionShowDeviceInfo.setIcon(QtGui.QIcon.fromTheme("information"))
        self.actionShowPacketStats.setIcon(QtGui.QIcon.fromTheme(
            "chart_column"))
        self.firmware_menu.setIcon(QtGui.QIcon.fromTheme("cpu_flash"))
        self.advanced_menu.setIcon(QtGui.QIcon.fromTheme("wrench"))

    def setup_logging(self):
        level = logging.INFO

        # create a log handler for the GUI and connect it
        self.gui_log_handler = GUILogHandler()
        self.gui_log_handler.loggedMessage.connect(self.handle_log_message)
        self.gui_log_handler.setLevel(level)

        # create a formatter
        formatter = SimpleExceptionFormatter('[%(asctime)s] %(message)s',
                                             datefmt="%Y-%m-%dT%H:%M:%SZ")
        formatter.converter = time.gmtime
        self.gui_log_handler.setFormatter(formatter)

        # attach the handler to the root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.gui_log_handler)

        # create a filter for this tab's serial number
        def filter_func(record):
            try:
                device = record.device
            except AttributeError:
                return False
            return device == self.serial_number

        # add the filter function to the handler
        self.gui_log_handler.addFilter(filter_func)

        # create a logger that includes the serial number information
        self.logger = hyperborea.proxy.DeviceLoggerAdapter(
            logger, self.serial_number)

        # make sure the root is set to capture the desired level
        if logger.getEffectiveLevel() > level:
            logger.setLevel(level)

    def setup_callbacks(self):
        self.closeButton.clicked.connect(self.close_cb)
        self.status_received.connect(self.status_callback)
        self.packet_received.connect(self.packet_callback)
        self.log_message.connect(self.log_callback)

        self.display_timer = QtCore.QTimer(self)
        self.display_timer.timeout.connect(self.display_update_cb)

        self.graphChannelComboBox.currentIndexChanged.connect(
            self.graph_channel_changed)

        self.actionSetUserTag1.triggered.connect(self.set_user_tag_1)
        self.actionSetUserTag2.triggered.connect(self.set_user_tag_2)
        self.actionFirmwareLatestStable.triggered.connect(
            self.do_bootloader_latest_stable)
        self.actionFirmwareFromBranch.triggered.connect(
            self.do_bootloader_from_branch)
        self.actionFirmwareFromCommit.triggered.connect(
            self.do_bootloader_from_commit)
        self.actionFirmwareFromFile.triggered.connect(
            self.do_bootloader_from_file)
        self.actionForceRunBootloader.triggered.connect(
            self.force_run_bootloader)
        self.actionForceRunApplication.triggered.connect(
            self.force_run_application)
        self.actionForceReset.triggered.connect(self.force_reset)
        self.actionRaiseException.triggered.connect(self.do_explode)
        self.actionRecoverNVM.triggered.connect(self.recover_nvm)
        self.actionShowPacketStats.triggered.connect(self.show_packet_stats)
        self.actionChangeActiveStreams.triggered.connect(
            self.change_active_streams)
        self.actionShowDeviceInfo.triggered.connect(self.show_device_info)
        self.actionCalibrate.triggered.connect(self.calibrate)
        self.actionEditDeviceSettings.triggered.connect(self.edit_settings)
        self.actionRunTests.triggered.connect(self.run_tests)
        self.actionSetDeviceMode.triggered.connect(self.set_device_mode)

        self.bootloader_progress_timer = QtCore.QTimer(self)
        self.bootloader_progress_timer.timeout.connect(
            self.bootloader_progress_cb)

        self.bootloader_progress_set_max.connect(
            self.bootloader_progress.setMaximum)
        self.bootloader_progress_set_value.connect(
            self.bootloader_progress.setValue)

        self.device_info_progress_timer = QtCore.QTimer(self)
        self.device_info_progress_timer.timeout.connect(
            self.device_info_progress_cb)

        self.firmware_finder = hyperborea.download.FirmwareFinder()
        self.firmware_finder.completed.connect(self.firmware_finder_completed)
        self.firmware_finder.error.connect(self.firmware_finder_error)
        self.downloader = hyperborea.download.Downloader()
        self.downloader.completed.connect(self.download_completed)
        self.downloader.error.connect(self.download_error)

    def setup_usb_operations(self):
        self.get_initial_info_op = hyperborea.proxy.DeviceOperation(
            hyperborea.device_info.get_initial_info)
        self.get_initial_info_op.completed.connect(self.initial_info_cb)
        self.get_initial_info_op.error.connect(self.initial_info_error)
        self.get_reconnect_info_op = hyperborea.proxy.DeviceOperation(
            hyperborea.device_info.get_reconnect_info)
        self.get_reconnect_info_op.completed.connect(self.reconnect_info_cb)
        self.set_rgb_op = hyperborea.proxy.SimpleDeviceOperation(
            "set_rgb_values")
        self.set_led_op = hyperborea.proxy.SimpleDeviceOperation(
            "set_led_value")
        self.set_ctrl_var_op = hyperborea.proxy.SimpleDeviceOperation(
            "set_ctrl_var")
        self.set_rf_power_op = hyperborea.proxy.SimpleDeviceOperation(
            "enable_rf_power")
        self.reset_rf_power_timeout_op = hyperborea.proxy.DeviceOperation(
            reset_rf_power_timeout)
        self.start_streaming_op = hyperborea.proxy.DeviceOperation(
            hyperborea.stream.start_streaming)
        self.stop_streaming_op = hyperborea.proxy.DeviceOperation(
            hyperborea.stream.stop_streaming)
        self.stop_streaming_op.completed.connect(self.stop_streaming_cb)
        self.stop_streaming_op.error.connect(self.stop_streaming_cb)
        self.close_device_op = hyperborea.proxy.SimpleDeviceOperation("close")
        self.write_user_tag_op = hyperborea.proxy.SimpleDeviceOperation(
            "write_user_tag_string")
        self.write_user_tag_op.completed.connect(self.write_nvm_cb)
        self.write_user_tag_op.error.connect(self.write_nvm_error)
        self.write_nvm_op = hyperborea.proxy.DeviceOperation(write_nvm)
        self.write_nvm_op.completed.connect(self.write_nvm_cb)
        self.write_nvm_op.error.connect(self.write_nvm_error)
        self.bootloader_op = hyperborea.proxy.DeviceOperation(
            bootloader.do_bootload)
        self.bootloader_op.completed.connect(self.do_bootloader_cb)
        self.bootloader_op.error.connect(self.bootloader_error)
        self.force_bootloader_op = hyperborea.proxy.DeviceOperation(
            bootloader.force_bootloader)
        self.force_bootloader_op.completed.connect(self.force_reset_cb)
        self.force_bootloader_op.error.connect(self.force_reset_error)
        self.force_application_op = hyperborea.proxy.DeviceOperation(
            bootloader.force_application)
        self.force_application_op.completed.connect(self.force_reset_cb)
        self.force_application_op.error.connect(self.force_reset_error)
        self.force_reset_op = hyperborea.proxy.DeviceOperation(
            reset_and_reconnect)
        self.force_reset_op.completed.connect(self.force_reset_cb)
        self.force_reset_op.error.connect(self.force_reset_error)

        self.set_device_mode_op = hyperborea.proxy.DeviceOperation(
            set_device_mode)
        self.set_device_mode_op.completed.connect(self.set_device_mode_cb)

    def handle_log_message(self, message):
        # check if the scroll window is already at the bottom
        scrollBar = self.logList.verticalScrollBar()
        atBottom = scrollBar.value() == scrollBar.maximum()

        # log the message
        logItem = QtWidgets.QListWidgetItem(message)
        self.logList.addItem(logItem)

        # adjust the scroll position if necessary
        if atBottom:
            self.logList.scrollToBottom()

    def start_usb_operation(self, operation, *args, **kwargs):
        if not self.proxy:
            self.logger.error("called start_usb_operation with no proxy")
            return
        self.proxy.send_job(operation, *args, **kwargs)

    def setup_graphics(self):
        fft_pen = "c"

        self.timePlot = self.graphicsLayout.addPlot(row=0, col=0)
        self.fftPlot = self.graphicsLayout.addPlot(row=0, col=1)

        self.timePlot.showGrid(x=True, y=True)
        self.fftPlot.showGrid(x=True, y=True)

        self.timePlot.setLabel("bottom", "Time (s)")
        self.fftPlot.setLabel("bottom", "Frequency (Hz)")

        self.timePlot.setTitle("Time Domain")
        self.fftPlot.setTitle("Frequency Domain")
        self.buffering = False

        self.fft_curve = self.fftPlot.plot(pen=fft_pen)

        def override_labelString(axis):
            old_method = axis.labelString

            def new_func(self):
                # take off the leading <span>
                s = old_method()
                i = s.find(">")
                prefix = s[:i + 1]
                s = s[i + 1:]
                # take off the trailing </span>
                i = s.rfind("<")
                suffix = s[i:]
                s = s[:i]
                s = s.strip()
                if s.startswith("(") and s.endswith(")"):
                    s = s.strip("()")
                return "".join((prefix, s, suffix))
            new_method = new_func.__get__(axis)
            axis.labelString = new_method
        override_labelString(self.timePlot.getAxis("left"))
        override_labelString(self.fftPlot.getAxis("left"))

    def set_connected(self):
        self.logger.info("Connected")
        self.status_connected = True
        if not self.is_paused:
            self.stackedWidget.setCurrentIndex(1)
        for panel in self.panels:
            panel.connected(self.device_info)
        self.menuButton.setEnabled(True)
        self.statusProgressBar.setVisible(False)
        self.rgb_streaming()

    def set_disconnected(self, message):
        self.status_connected = False
        self.status_message = message
        if not self.is_paused:
            self.statusLabel.setText(message)
            self.stackedWidget.setCurrentIndex(0)
        for panel in self.panels:
            panel.disconnected()
        self.menuButton.setEnabled(False)

    def proxy_disconnect_cb(self):
        self.set_disconnected(self.tr("Disconnected"))
        self.statusProgressBar.setVisible(False)
        self.proxy = None

        self.streaming = False
        self.streaming_stopped.set()

        self.disconnected_signal.emit()

    def set_proxy(self, proxy):
        self.proxy = proxy
        self.proxy.disconnected.connect(self.proxy_disconnect_cb)

        if self.is_paused:
            self.connect_stopped = True
        else:
            self.connect_stopped = False
            self.get_device_info()

    def pause(self):
        if not self.is_paused:
            self.is_paused = True

            # pause all the plots
            for fft_ringbuffer in self.fft_ringbuffers:
                if fft_ringbuffer is not None:
                    fft_ringbuffer.pause()
            for plot_ringbuffer in self.plot_ringbuffers:
                if plot_ringbuffer is not None:
                    plot_ringbuffer.pause()
            for mean_ringbuffer in self.mean_ringbuffers:
                if mean_ringbuffer is not None:
                    mean_ringbuffer.pause()

    def resume(self):
        if self.is_paused:
            self.is_paused = False

            # resume all the plots
            for fft_ringbuffer in self.fft_ringbuffers:
                if fft_ringbuffer is not None:
                    fft_ringbuffer.resume()
            for plot_ringbuffer in self.plot_ringbuffers:
                if plot_ringbuffer is not None:
                    plot_ringbuffer.resume()
            for mean_ringbuffer in self.mean_ringbuffers:
                if mean_ringbuffer is not None:
                    mean_ringbuffer.resume()

            if self.proxy is not None and self.connect_stopped:
                self.connect_stopped = False
                self.get_device_info()

            # set the status label to the most recent value
            self.statusLabel.setText(self.status_message)
            new_index = 1 if self.status_connected else 0
            self.stackedWidget.setCurrentIndex(new_index)

    def get_device_info(self):
        if not self.device_info:
            self.set_disconnected(self.tr("Loading Device Information..."))
            rx, tx = multiprocessing.Pipe(False)
            self.device_info_rx_pipe = rx
            self.device_info_tx_pipe = tx
            self.start_usb_operation(self.get_initial_info_op,
                                     self.device_info_tx_pipe)

            # setup the progress bar
            self.statusProgressBar.setMinimum(0)
            self.statusProgressBar.setMaximum(0)
            self.statusProgressBar.setValue(0)
            self.statusProgressBar.setVisible(True)

            self.device_info_progress_timer.start(20)  # 20 milliseconds
        else:
            self.set_disconnected(self.tr("Reloading Device Information..."))
            self.statusProgressBar.setVisible(False)
            self.start_usb_operation(self.get_reconnect_info_op)

    def device_info_progress_cb(self):
        last_value = None
        while self.device_info_rx_pipe.poll():
            try:
                last_value = self.device_info_rx_pipe.recv()
            except EOFError:
                break
        if last_value is not None:
            self.statusProgressBar.setMaximum(last_value[1])
            self.statusProgressBar.setValue(last_value[0])

    def initial_info_error(self):
        self.device_info_progress_timer.stop()
        self.device_info_rx_pipe.close()
        self.device_info_tx_pipe.close()
        self.statusProgressBar.setVisible(False)

    def initial_info_cb(self, info):
        # stop progress timer and close pipes
        self.device_info_progress_timer.stop()
        self.device_info_rx_pipe.close()
        self.device_info_tx_pipe.close()

        if not info:
            # error while getting initial info
            self.statusProgressBar.setVisible(False)
            QtCore.QCoreApplication.processEvents()
            if self.proxy:
                self.proxy.close_connection()
            return

        # set bar to 100%
        self.statusProgressBar.setValue(self.statusProgressBar.maximum())
        QtCore.QCoreApplication.processEvents()

        self.device_info = info

        if info['user_tag_1']:
            self.userTag1.setText(info['user_tag_1'])
            self.display_name = info['user_tag_1']
        else:
            self.userTag1.setText(self.tr("<INVALID>"))
            # fall back to serial number
            self.display_name = self.serial_number
        self.name_update.emit(self.display_name)

        if info['user_tag_2']:
            self.userTag2.setText(info['user_tag_2'])
        else:
            self.userTag2.setText(self.tr("<INVALID>"))

        self.boardInfo.setText("{} rev {}".format(*info['board_info']))
        self.buildInfo.setText(info['build_info'])
        self.buildDate.setText(info['build_date'])

        if info['supports_bootloader']:
            self.bootloaderIndicator.setVisible(True)
        else:
            self.bootloaderIndicator.setVisible(False)

        for i, values in enumerate(info['rgb_settings']):
            self.create_rgb_widget(i, values)
        for i, value in enumerate(info['led_settings']):
            self.create_led_widget(i, value)

        for i, (name, ctrl_var_info, setting) in enumerate(info['ctrl_vars']):
            self.create_ctrl_var_widget(i, name, ctrl_var_info, setting)

        unassigned_ctrl_var_indexes = list(range(len(info['ctrl_vars'])))

        if len(info['settings']) == 0:
            # No settings on the device
            self.actionEditDeviceSettings.setEnabled(False)
            self.actionEditDeviceSettings.setText("No Device Settings")

        if info['supports_rf_power']:
            self.create_rf_power_panel(info['rf_power_status'])

            for ctrl_var_index in info['rf_power_ctrl_vars']:
                unassigned_ctrl_var_indexes.remove(ctrl_var_index)
                widget = self.ctrl_var_widgets[ctrl_var_index]
                self.rf_power_panel.add_ctrl_var_widget(widget)

        if info['supports_radio']:
            self.create_radio_panel()

            for ctrl_var_index in info['radio_ctrl_vars']:
                unassigned_ctrl_var_indexes.remove(ctrl_var_index)
                widget = self.ctrl_var_widgets[ctrl_var_index]
                self.radio_panel.add_ctrl_var_widget(widget)

        if info['supports_remote']:
            self.create_remote_panel()

        if (info['supports_bootloader'] or
                info["bootloader_info"] == "Asphodel"):
            self.firmware_menu.setEnabled(True)
            self.actionFirmwareLatestStable.setEnabled(True)
            self.actionFirmwareFromBranch.setEnabled(True)
            self.actionFirmwareFromCommit.setEnabled(True)
            self.actionFirmwareFromFile.setEnabled(True)
        if info["bootloader_info"] == "Asphodel":
            self.actionForceRunBootloader.setEnabled(True)
        if info['supports_bootloader']:
            self.actionForceRunApplication.setEnabled(True)

        if info['supports_device_mode']:
            self.actionSetDeviceMode.setEnabled(True)

        if unassigned_ctrl_var_indexes:
            self.create_ctrl_var_panel(unassigned_ctrl_var_indexes)

        self.rgb_connected()

        # self.set_connected() will be called when streaming has started
        self.set_disconnected(self.tr("Starting streaming..."))
        QtCore.QCoreApplication.processEvents()

        self.create_device_decoder(info['stream_filler_bits'],
                                   info['stream_id_bits'], info['streams'],
                                   info['channels'])

        # create the calibration panel after the device decoder is setup
        has_calibration = False
        channel_calibration = info['channel_calibration']
        for channel_id, calibration_info in enumerate(channel_calibration):
            if calibration_info is not None:
                if channel_id in self.channel_indexes:
                    has_calibration = True
        if has_calibration:
            self.create_calibration_panel()
            self.actionCalibrate.setEnabled(True)

    def reconnect_info_cb(self, info):
        if not info:
            # error while getting reconnect info
            if self.proxy:
                self.proxy.close_connection()
            return

        for i, values in enumerate(info['rgb_settings']):
            self.rgb_widgets[i].set_values(values)
        for i, value in enumerate(info['led_settings']):
            self.led_widgets[i].set_value(value)

        for i, value in enumerate(info['ctrl_var_settings']):
            self.ctrl_var_widgets[i].set_value(value)

        self.device_info.update(info)

        self.rgb_connected()

        # self.set_connected() will be called when streaming has started
        self.set_disconnected(self.tr("Starting streaming..."))
        QtCore.QCoreApplication.processEvents()

        # clear all the plots
        for fft_ringbuffer in self.fft_ringbuffers:
            if fft_ringbuffer is not None:
                fft_ringbuffer.clear()
        for plot_ringbuffer in self.plot_ringbuffers:
            if plot_ringbuffer is not None:
                plot_ringbuffer.clear()
        for mean_ringbuffer in self.mean_ringbuffers:
            if mean_ringbuffer is not None:
                mean_ringbuffer.clear()

        self.start_streaming(self.device_info['streams'])

    def stop_for_recreate(self):
        self.stop_streaming()

        for panel in self.panels:
            panel.stop()

        self.display_timer.stop()

    def stop_and_close(self):
        self.rgb_disconnected()

        self.stop_streaming()

        for panel in self.panels:
            panel.stop()

        self.start_usb_operation(self.close_device_op)

        self.display_timer.stop()
        if self.proxy:
            self.proxy.close_connection()

    def close_cb(self):
        self.stop_and_close()
        self.close_pressed.emit()

    def set_user_tag(self, index):
        if not self.device_info:
            # error
            self.logger.exception("No device info available")
            QtWidgets.QMessageBox.critical(self, self.tr("Error"),
                                           self.tr("Not yet connected!"))
            return

        # find the current setting
        tag_key = "user_tag_" + str(index + 1)
        old_str = self.device_info[tag_key]

        # ask the user for the new string
        new_str, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("New Tag"), self.tr("New Tag:"),
            QtWidgets.QLineEdit.Normal, old_str)

        if not ok:
            return

        # find the offset and length
        offset, length = self.device_info['tag_locations'][index]

        # write the new tag
        self.start_usb_operation(self.write_user_tag_op, offset, length,
                                 new_str)
        self.device_info[tag_key] = new_str

        # update the UI
        if index == 0:
            if new_str:
                self.userTag1.setText(new_str)
                self.display_name = new_str
                self.name_update.emit(new_str)
            else:
                self.userTag1.setText("<INVALID>")
        else:
            if new_str:
                self.userTag2.setText(new_str)
            else:
                self.userTag2.setText("<INVALID>")

    def set_user_tag_1(self):
        self.set_user_tag(0)

    def set_user_tag_2(self):
        self.set_user_tag(1)

    def get_firmware_file(self, firm_dir, firm_name):
        settings = QtCore.QSettings()

        board_name, board_rev = self.device_info['board_info']
        short_board_name = board_name.replace(" ", "")

        keys = ["firmDirectory/{}/Rev{}".format(short_board_name, board_rev),
                "firmDirectory/{}/last".format(short_board_name),
                "firmDirectory/last"]

        # find the directory from settings
        firm_dir = None
        for key in keys:
            test_dir = settings.value(key)
            if test_dir and type(test_dir) == str:
                if os.path.isdir(test_dir):
                    firm_dir = test_dir
                    break
        if not firm_dir:
            firm_dir = ""

        # ask the user for the file name
        caption = self.tr("Open Firmware File")
        file_filter = self.tr("Firmware Files (*.firmware);;All Files (*.*)")
        val = QtWidgets.QFileDialog.getOpenFileName(self, caption, firm_dir,
                                                    file_filter)
        output_path = val[0]

        if output_path:
            # save the directory
            output_dir = os.path.dirname(output_path)
            for key in keys:
                settings.setValue(key, output_dir)
            return output_path
        else:
            return None

    def do_bootloader_latest_stable(self):
        self.do_bootloader_web(build_type="firmware", branch="master")

    def do_bootloader_from_branch(self):
        branch, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Firmware Branch"), self.tr("Firmware Branch:"),
            QtWidgets.QLineEdit.Normal, "master")
        if not ok:
            return

        branch = branch.strip()

        self.do_bootloader_web(build_type=None, branch=branch)

    def do_bootloader_from_commit(self):
        commit, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Firmware Commit"), self.tr("Firmware Commit:"),
            QtWidgets.QLineEdit.Normal, "")
        if not ok:
            return

        commit = commit.strip()

        self.do_bootloader_web(build_type=None, commit=commit)

    def do_bootloader_web(self, build_type, branch=None, commit=None):
        self.bootloader_progress.setMinimum(0)
        self.bootloader_progress.setMaximum(0)
        self.bootloader_progress.setValue(0)
        self.bootloader_progress.setLabelText(
            self.tr("Searching for firmware..."))
        self.bootloader_progress.forceShow()

        self.firmware_finder.find_firmware(
            build_type, self.device_info['board_info'], branch=branch,
            commit=commit)

    def firmware_finder_error(self, error_str):
        self.bootloader_progress.reset()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    def firmware_finder_completed(self, build_urls):
        self.bootloader_progress.reset()
        build_types = sorted(build_urls.keys())
        if 'firmware' in build_types:
            # move it to the front
            build_types.remove('firmware')
            build_types.insert(0, 'firmware')

        if len(build_types) == 1:
            # choose the only option available
            build_type = build_types[0]
        else:
            value, ok = QtWidgets.QInputDialog.getItem(
                self, self.tr("Select Build Type"),
                self.tr("Select Build Type"), build_types, 0,
                editable=False)
            if not ok:
                return
            build_type = value

        url = build_urls[build_type]

        self.logger.info("Downloading firmware from %s", url)

        self.bootloader_progress.setMinimum(0)
        self.bootloader_progress.setMaximum(0)
        self.bootloader_progress.setValue(0)
        self.bootloader_progress.setLabelText(
            self.tr("Downloading firmware..."))
        self.bootloader_progress.forceShow()

        file = io.BytesIO()
        self.downloader.start_download(url, file,
                                       self.download_update_progress)

    def download_update_progress(self, written_bytes, total_length):
        self.bootloader_progress_set_max.emit(total_length)
        self.bootloader_progress_set_value.emit(written_bytes)

    def download_error(self, file, error_str):
        self.bootloader_progress_timer.stop()
        self.bootloader_progress.reset()
        file.close()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    def download_completed(self, file):
        try:
            firm_data = bootloader.decode_firm_bytes(file.getvalue())
        except:
            self.bootloader_progress.reset()
            self.logger.exception('Error decoding downloaded firmware')
            m = self.tr('Error decoding downloaded firmware!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            return
        finally:
            file.close()
        self.do_bootloader(firm_data)

    def do_bootloader_from_file(self):
        firm_dir, firm_name = bootloader.get_default_file(self.device_info)

        if not firm_dir:
            firm_file = self.get_firmware_file(firm_dir, firm_name)
        else:
            firm_file = os.path.join(firm_dir, firm_name)

            message = self.tr("Use {}?").format(firm_file)
            ret = QtWidgets.QMessageBox.warning(
                self, self.tr("Update Firmware"), message,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
            if ret == QtWidgets.QMessageBox.Cancel:
                return False
            if ret == QtWidgets.QMessageBox.No:
                firm_file = self.get_firmware_file(firm_dir, firm_name)

        if not firm_file:
            return  # user cancelled

        try:
            firm_data = bootloader.decode_firm_file(firm_file)
        except:
            self.logger.exception('Error loading firmware from "%s"',
                                  firm_file)
            m = self.tr('Error loading firmware from file!').format(firm_file)
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            return

        self.do_bootloader(firm_data)

    def do_bootloader(self, firm_data):
        if not bootloader.is_board_supported(firm_data, self.device_info):
            self.bootloader_progress.reset()
            self.logger.error("Firmware file does not support this board!")
            message = self.tr("Firmware file does not support this board!")
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)
            return

        if bootloader.already_programmed(firm_data, self.device_info):
            self.bootloader_progress.reset()
            self.logger.info("Firmware already present!")
            message = self.tr("Firmware already present!")
            QtWidgets.QMessageBox.information(self, self.tr("Error"), message)
            return

        self.set_disconnected(self.tr("Updating Firmware..."))
        self.stop_for_recreate()
        rx, tx = multiprocessing.Pipe(False)
        self.bootloader_rx_pipe = rx
        self.bootloader_tx_pipe = tx

        self.start_usb_operation(self.bootloader_op, firm_data,
                                 self.bootloader_tx_pipe)

        # setup the progress dialog
        self.bootloader_progress.setMinimum(0)
        self.bootloader_progress.setMaximum(0)
        self.bootloader_progress.setValue(0)
        self.bootloader_progress.setLabelText(
            self.tr("Stopping Streaming..."))
        self.bootloader_progress.forceShow()

        self.bootloader_progress_timer.start(20)  # 20 milliseconds

    def bootloader_progress_cb(self):
        last_value = None
        while self.bootloader_rx_pipe.poll():
            try:
                data = self.bootloader_rx_pipe.recv()
                if isinstance(data, str):
                    self.bootloader_progress.setLabelText(data)
                if isinstance(data, tuple):
                    self.bootloader_progress.setMinimum(data[0])
                    self.bootloader_progress.setMaximum(data[1])
                if isinstance(data, int):
                    last_value = data
            except EOFError:
                break
        if last_value is not None:
            self.bootloader_progress.setValue(last_value)

    def do_bootloader_cb(self):
        self.bootloader_progress_timer.stop()
        self.bootloader_progress.reset()

        # close the pipes
        self.bootloader_rx_pipe.close()
        self.bootloader_tx_pipe.close()

        self.plotmain.recreate_tab(self)

    def bootloader_error(self):
        self.bootloader_progress_timer.stop()
        self.bootloader_progress.reset()

        # close the pipes
        self.bootloader_rx_pipe.close()
        self.bootloader_tx_pipe.close()

        self.close_cb()
        message = self.tr("Error while loading firmware!")
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)

    def force_run_bootloader(self):
        self.set_disconnected(self.tr("Connecting to Bootloader..."))
        self.stop_for_recreate()
        self.start_usb_operation(self.force_bootloader_op)

    def force_run_application(self):
        self.set_disconnected(self.tr("Connecting to Application..."))
        self.stop_for_recreate()
        self.start_usb_operation(self.force_application_op)

    def force_reset(self):
        self.set_disconnected(self.tr("Resetting Device..."))
        self.stop_for_recreate()
        self.start_usb_operation(self.force_reset_op)

    def force_reset_cb(self):
        self.plotmain.recreate_tab(self)

    def force_reset_error(self):
        self.close_cb()
        message = self.tr("Error while reconnecting!")
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)

    def do_explode(self):
        explode_op = hyperborea.proxy.DeviceOperation(explode)
        self.start_usb_operation(explode_op)

    def write_nvm(self, nvm):
        nvm = bytes(nvm)
        self.device_info['nvm'] = nvm
        self.start_usb_operation(self.write_nvm_op, nvm)

    def recover_nvm(self):
        # ask the user for the file name
        apd_dir = self.base_dir
        caption = self.tr("Open Data File")
        file_filter = self.tr("Data Files (*.apd);;All Files (*.*)")
        val = QtWidgets.QFileDialog.getOpenFileName(self, caption, apd_dir,
                                                    file_filter)
        filename = val[0]
        if filename == "":
            return

        # open file and decompress
        fp = lzma.open(filename, 'rb')

        # read the header from the file
        header_leader = struct.unpack(">dI", fp.read(12))
        header_bytes = fp.read(header_leader[1])
        header_str = header_bytes.decode("UTF-8")
        header = json.loads(header_str)
        new_nvm = bytes.fromhex(header['nvm'])

        # check the nvm lengths
        new_length = len(new_nvm)
        current_length = len(self.device_info['nvm'])
        if new_length != current_length:
            # need to add a popup here #
            message = self.tr("NVM sizes do not match!")
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)
            return

        # write the nvm
        self.write_nvm(new_nvm)

    def show_packet_stats(self):
        with self.lost_packet_lock:
            lost_packet_count = self.lost_packet_count
            lost_packet_last_time = self.lost_packet_last_time

        count_since_last = lost_packet_count - self.last_displayed_packet_count
        self.last_displayed_packet_count = lost_packet_count

        now = datetime.datetime.utcnow()

        if self.last_displayed_packet_time is not None:
            last_check_str = self.last_displayed_packet_time.strftime(
                "%Y-%m-%dT%H:%M:%SZ")  # use ISO 8601 representation
        else:
            last_check_str = self.tr("Never")
        self.last_displayed_packet_time = now

        if lost_packet_last_time is not None:
            delta = now - lost_packet_last_time

            # remove microseconds
            delta = delta - datetime.timedelta(microseconds=delta.microseconds)
            last_loss_str = str(delta)
        else:
            last_loss_str = self.tr("N/A")

        msg = ("All Time Lost Packets: {}\nTime since last packet loss: {}\n"
               "Lost Since Last Check: {}\nTime of last check: {}".format(
                   lost_packet_count, last_loss_str, count_since_last,
                   last_check_str))

        QtWidgets.QMessageBox.information(self, self.tr("Packet Loss Stats"),
                                          msg)

    def change_active_streams(self):
        dialog = ChangeStreamDialog(self.device_info['streams'],
                                    self.device_info['channels'],
                                    self.stream_list, parent=self)
        ret = dialog.exec_()
        if ret == 0:
            return  # user cancelled

        self.stop_for_recreate()
        self.stream_list = dialog.get_new_stream_list()
        self.plotmain.recreate_tab(self)  # will use self.stream_list

    def show_device_info(self):
        dialog = InfoDialog(self.device_info, parent=self)
        dialog.exec_()

    def run_tests(self):
        self.stop_streaming()
        self.set_disconnected(self.tr("Running Hardware Tests..."))
        dialog = HardwareTestDialog(self.device_info, self.proxy, parent=self)
        dialog.start_tests()
        dialog.exec_()
        self.start_usb_operation(self.get_reconnect_info_op)

    def set_device_mode(self):
        new_mode, ok = QtWidgets.QInputDialog.getInt(
            self, self.tr("Device Mode"), self.tr("Input new device mode"),
            self.device_info['device_mode'], 0, 255)
        if not ok:
            return
        self.start_usb_operation(self.set_device_mode_op, new_mode)

    def set_device_mode_cb(self, ret):
        success, new_mode = ret
        if success:
            self.device_info['device_mode'] = new_mode
        else:
            self.logger.warning("Bad device mode {}".format(new_mode))
            QtWidgets.QMessageBox.critical(
                self, self.tr("Bad Device Mode"),
                self.tr("Bad Device Mode {}!").format(new_mode))

    def calibrate(self, junk=None):
        if self.actionCalibrate.isChecked():
            # start
            self.actionCalibrate.setText(self.tr("Stop Calibration"))
            self.calibration_panel.setVisible(True)
        else:
            # stop
            self.actionCalibrate.setText(self.tr("Start Calibration"))
            self.calibration_panel.setVisible(False)

    def edit_settings(self):
        settings = self.device_info['settings']
        nvm_bytes = self.device_info['nvm']
        custom_enums = self.device_info['custom_enums']
        setting_categories = self.device_info['setting_categories']
        dialog = SettingDialog(settings, nvm_bytes, custom_enums,
                               setting_categories, parent=self)
        ret = dialog.exec_()
        if ret == 0:
            return  # user cancelled

        try:
            new_nvm = bytearray(nvm_bytes)
            dialog.update_nvm(new_nvm)
        except:
            self.logger.exception("Unhandled Exception in edit_settings")
            QtWidgets.QMessageBox.critical(self, self.tr("Error"),
                                           self.tr("Error parsing settings!"))
            return

        self.write_nvm(new_nvm)

    def write_nvm_cb(self):
        # ask if the user wants to reset
        ret = QtWidgets.QMessageBox.question(
            self, self.tr("Reset?"), self.tr("NVM Written. Reset Device?"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if ret == QtWidgets.QMessageBox.Yes:
            self.force_reset()

    def write_nvm_error(self):
        self.close_cb()
        message = self.tr("Error while writing NVM!")
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)

    def create_rgb_widget(self, index, initial_values):
        def set_values(values):
            self.start_usb_operation(self.set_rgb_op, index, values)

        widget = RGBControlWidget(set_values, initial_values, parent=self)
        self.LEDLayout.addWidget(widget)
        self.rgb_widgets.append(widget)

    def create_led_widget(self, index, initial_value):
        def set_value(value):
            self.start_usb_operation(self.set_led_op, index, value)

        widget = LEDControlWidget(set_value, initial_value, parent=self)
        self.LEDLayout.addWidget(widget)
        self.led_widgets.append(widget)

    def create_ctrl_var_widget(self, index, name, ctrl_var_info, setting):
        def set_value(value):
            self.start_usb_operation(self.set_ctrl_var_op, index, value)

        widget = CtrlVarWidget(set_value, name, ctrl_var_info, setting,
                               parent=self)
        self.ctrl_var_widgets.append(widget)

    def create_ctrl_var_panel(self, indexes):
        self.ctrl_var_panel = CtrlVarPanel(parent=self)
        for i in indexes:
            self.ctrl_var_panel.add_ctrl_var_widget(self.ctrl_var_widgets[i])
        self.add_panel(self.ctrl_var_panel)

    def create_rf_power_panel(self, status):
        def enable_func(enable):
            self.start_usb_operation(self.set_rf_power_op, enable)

        def reset_timeout_func(timeout):
            self.start_usb_operation(self.reset_rf_power_timeout_op, timeout)

        self.rf_power_panel = RFPowerPanel(enable_func, reset_timeout_func,
                                           status, parent=self)
        self.add_panel(self.rf_power_panel)
        self.plotmain.register_rf_power_panel(self.rf_power_panel)

    def create_radio_panel(self):
        self.radio_panel = RadioPanel(self.start_usb_operation, parent=self)
        self.add_panel(self.radio_panel)

    def create_remote_panel(self):
        self.remote_panel = RemotePanel(parent=self)
        self.add_panel(self.remote_panel)

    def add_panel(self, panel):
        self.panels.append(panel)
        self.panelLayout.addWidget(panel)

    def capture_func(self, channel_index):
        ringbuffer = self.mean_ringbuffers[channel_index]
        if len(ringbuffer) > 0:
            d = ringbuffer.get_contents()
            uf = self.unit_formatters[channel_index]
            mean = numpy.mean(d, axis=0).item(0)
            mean = (mean - uf.conversion_offset) / uf.conversion_scale
            std_dev = numpy.std(d, axis=0).item(0)
            std_dev = std_dev / uf.conversion_scale
            return (mean, std_dev)
        else:
            return (math.nan, math.nan)

    def create_calibration_panel(self):
        channel_calibration = self.device_info['channel_calibration']
        cals = []
        for channel_id, calibration_info in enumerate(channel_calibration):
            if calibration_info is not None:
                if channel_id in self.channel_indexes:
                    index = self.channel_indexes[channel_id]
                    name = self.channel_names[index]
                    capture = functools.partial(self.capture_func, index)
                    cals.append((name, calibration_info, capture,
                                 self.unit_formatters[index]))
        self.calibration_panel = CalibrationPanel(
            self.device_info, cals, self.logger, parent=self)
        self.calibration_panel.setVisible(False)

        # NOTE: don't add to self.panels, as it doesn't support the panel funcs

        self.panelLayout.insertWidget(0, self.calibration_panel)

    def create_device_decoder(self, filler_bits, id_bits, streams, channels):
        if self.disable_streaming:
            streams_to_activate = []
        elif self.stream_list is True:
            streams_to_activate = list(range(len(streams)))
        else:
            streams_to_activate = self.stream_list

        info_list = []
        for i, stream in enumerate(streams):
            if i not in streams_to_activate:
                continue
            channel_info_list = []
            indexes = stream.channel_index_list[0:stream.channel_count]
            for ch_index in indexes:
                channel_info_list.append(channels[ch_index])
            info_list.append((i, stream, channel_info_list))

        self.device_decoder = asphodel.nativelib.create_device_decoder(
            info_list, filler_bits, id_bits)

        # create the device decoder
        self.device_decoder.set_unknown_id_callback(self.unknown_id_cb)

        # key: channel_id, value: (stream_id, channel, decoder)
        channel_decoders = {}

        # set unknown_id and lost packet callbacks, and fill channel_decoders
        for i, stream_decoder in enumerate(self.device_decoder.decoders):
            stream_id = self.device_decoder.stream_ids[i]
            lost_packet_cb = self.create_lost_packet_callback(
                stream_id, streams[stream_id])
            stream_decoder.set_lost_packet_callback(lost_packet_cb)
            for j, channel_decoder in enumerate(stream_decoder.decoders):
                channel_id = stream_decoder.stream_info.channel_index_list[j]
                channel = channels[channel_id]
                channel_decoders[channel_id] = (stream_id, channel,
                                                channel_decoder)

        # operate on the channel decoders sorted by channel index
        for channel_id in sorted(channel_decoders.keys()):
            stream_id, channel, channel_decoder = channel_decoders[channel_id]
            self.setup_channel(stream_id, streams[stream_id], channel_id,
                               channel, channel_decoder)

        # fill the combo box
        for channel_name in self.channel_names:
            self.graphChannelComboBox.addItem(channel_name)
        self.graphChannelComboBox.setCurrentIndex(0)

        self.start_streaming(streams)

    def log_thread_safe(self, level, message):
        self.log_message.emit(level, message)

    def log_callback(self, level, message):
        self.logger.log(level, message)

    def unknown_id_cb(self, unknown_id):
        msg = "Unknown ID {} while decoding packet".format(unknown_id)
        self.log_thread_safe(logging.ERROR, msg)

    def create_lost_packet_callback(self, stream_id, stream):
        def lost_packet_callback(current, last):
            lost = (current - last - 1) & 0xFFFFFFFFFFFFFFFF

            now = datetime.datetime.utcnow()

            with self.lost_packet_lock:
                self.lost_packet_count += lost
                self.recent_lost_packet_count += lost
                self.lost_packet_last_time = now

            self.lost_packet_deque.append((now, lost))

            for channel_index, stream_index in enumerate(self.channel_streams):
                if stream_index == stream_id:
                    fft_ringbuffer = self.fft_ringbuffers[channel_index]
                    if fft_ringbuffer is not None:
                        fft_ringbuffer.clear()

        return lost_packet_callback

    def setup_channel(self, stream_id, stream, channel_id, channel,
                      channel_decoder):
        unit_formatter = hyperborea.unit_preferences.create_unit_formatter(
            self.settings, channel.unit_type, channel.minimum, channel.maximum,
            channel.resolution)

        channel_decoder.set_conversion_factor(unit_formatter.conversion_scale,
                                              unit_formatter.conversion_offset)

        # figure out if the unit formatter follows SI rules
        unit_scale = None
        unit_str = unit_formatter.unit_html
        if unit_formatter.conversion_offset == 0.0:
            uf_1000x = hyperborea.unit_preferences.create_unit_formatter(
                self.settings, channel.unit_type, channel.minimum * 1000.0,
                channel.maximum * 1000.0, channel.resolution)
            ratio = unit_formatter.conversion_scale / uf_1000x.conversion_scale
            if numpy.isclose(1000.0, ratio):
                # it's probably a SI unit formatter
                unit_scale = 1.0 / unit_formatter.conversion_scale

                # find the base string
                uf_base = hyperborea.unit_preferences.create_unit_formatter(
                    self.settings, channel.unit_type, 1.0, 1.0, 1.0)
                unit_str = uf_base.unit_html

        subchannel_fields = []

        for i in range(channel_decoder.subchannels):
            subchannel_name = channel_decoder.subchannel_names[i]
            label = QtWidgets.QLabel(subchannel_name)

            mean_field = MeasurementLineEdit()
            std_dev_field = MeasurementLineEdit()
            sampling_rate_field = MeasurementLineEdit()

            sampling_rate = channel.samples * stream.rate
            sampling_rate_field.setText("{:g} sps".format(sampling_rate))

            row = self.channelLayout.rowCount()
            self.channelLayout.addWidget(label, row, 0)
            self.channelLayout.addWidget(mean_field, row, 1)
            self.channelLayout.addWidget(std_dev_field, row, 2)
            self.channelLayout.addWidget(sampling_rate_field, row, 3)
            subchannel_fields.append((mean_field, std_dev_field))

        index = len(self.channel_names)  # for checking against the combobox
        self.channel_indexes[channel_id] = index
        self.channel_names.append(channel_decoder.channel_name)
        self.channel_streams.append(stream_id)
        self.subchannel_names.append(channel_decoder.subchannel_names)
        self.unit_info.append((unit_str, unit_scale))
        self.unit_formatters.append(unit_formatter)
        self.subchannel_fields.append(subchannel_fields)

        rate_info = self.device_info['stream_rate_info'][stream_id]
        self.channel_rate_infos.append(rate_info)

        self.channel_samples.append(channel.samples)
        channel_rate = channel.samples * stream.rate
        self.channel_rates.append(channel_rate)

        # figure out how much data to collect
        sample_len = math.ceil(10.0 * channel_rate)  # 10 seconds
        # round up to next power of 2 (for faster FFT)
        sample_len = 2 ** (math.ceil(math.log2(sample_len)))

        mean_len = math.ceil(1.0 * channel_rate)  # 1 second

        if self.downsample and sample_len > 32768:
            downsample = True
            self.channel_downsample.append(channel.samples)
            plot_len = sample_len // channel.samples
        else:
            downsample = False
            self.channel_downsample.append(1)
            plot_len = sample_len

        fft_sample_len = min(sample_len, 32768)
        self.fft_shortened.append((fft_sample_len != sample_len,
                                   fft_sample_len / channel_rate))
        plot_rb = hyperborea.ringbuffer.RingBuffer(
            plot_len, channel_decoder.subchannels)
        self.plot_ringbuffers.append(plot_rb)
        mean_rb = hyperborea.ringbuffer.RingBuffer(
            mean_len, channel_decoder.subchannels)
        self.mean_ringbuffers.append(mean_rb)
        fft_rb = hyperborea.ringbuffer.RingBuffer(
            fft_sample_len, channel_decoder.subchannels)
        self.fft_ringbuffers.append(fft_rb)
        self.fft_freq_axes.append(numpy.fft.rfftfreq(fft_sample_len,
                                                     1 / channel_rate))
        self.fft_size.append(fft_sample_len)

        def callback(counter, data, samples, subchannels):
            d = numpy.array(data).reshape(samples, subchannels)
            if downsample:
                self.plot_ringbuffers[index].append(d[-1, :])
            else:
                self.plot_ringbuffers[index].extend(d)
            self.fft_ringbuffers[index].extend(d)
            self.mean_ringbuffers[index].extend(d)

        channel_decoder.set_callback(callback)

    def display_update_cb(self):
        # update lost packet numbers
        lost_count_too_old = 0
        now = datetime.datetime.utcnow()
        twenty_secs_ago = now - datetime.timedelta(seconds=20)
        while len(self.lost_packet_deque):
            lost_dt, lost = self.lost_packet_deque[0]
            if lost_dt < twenty_secs_ago:
                lost_count_too_old += lost
                self.lost_packet_deque.popleft()
            else:
                break

        with self.lost_packet_lock:
            self.recent_lost_packet_count -= lost_count_too_old
            if self.recent_lost_packet_count < 0:
                msg = "Negative lost packet count {}".format(
                    self.recent_lost_packet_count)
                self.logger.error(msg)
                self.recent_lost_packet_count = 0
            recent_lost_packet_count = self.recent_lost_packet_count

        self.recentLostPackets.setText(str(recent_lost_packet_count))
        if recent_lost_packet_count > 0:
            if not self.recent_lost_packet_highlight:
                self.recent_lost_packet_highlight = True
                self.recentLostPackets.setStyleSheet(
                    "* { background-color: red }")
        else:
            if self.recent_lost_packet_highlight:
                self.recent_lost_packet_highlight = False
                self.recentLostPackets.setStyleSheet("")

        # update all text boxes
        for index, ringbuffer in enumerate(self.mean_ringbuffers):
            if len(ringbuffer) > 0:
                d = ringbuffer.get_contents()
                mean = numpy.mean(d, axis=0)
                std_dev = numpy.std(d, axis=0)
                for i, fields in enumerate(self.subchannel_fields[index]):
                    mean_field, std_dev_field = fields
                    s = self.unit_formatters[index].format_utf8(mean[i])
                    mean_field.setText(s)
                    s = self.unit_formatters[index].format_utf8(std_dev[i])
                    std_dev_field.setText(s)

        channel_index = self.graphChannelComboBox.currentIndex()
        if channel_index == -1:
            return

        if self.last_channel_index != channel_index:
            if self.channel_downsample[channel_index] == 1:
                self.timePlot.setTitle("Time Domain")
            else:
                s = "Time Domain (Downsampled {}x)".format(
                    self.channel_downsample[channel_index])
                self.timePlot.setTitle(s)

        # update rate info if it is variable
        rate_info = self.channel_rate_infos[channel_index]
        if rate_info.available:
            rate_channel_index = self.channel_indexes[rate_info.channel_index]
            ringbuffer = self.fft_ringbuffers[rate_channel_index]
            rate_data = ringbuffer.get_contents()
            if len(rate_data) != 0:
                raw_rate = numpy.average(rate_data)

                # compute channel rate
                stream_rate = raw_rate * rate_info.scale + rate_info.offset
                if rate_info.invert:
                    if stream_rate != 0.0:
                        stream_rate = 1 / stream_rate
                    else:
                        stream_rate = 0.0  # no divide by zero please

                # undo the formatter
                uf = self.unit_formatters[rate_channel_index]
                stream_rate = (stream_rate - uf.conversion_offset) * \
                    uf.conversion_scale

                channel_rate = (stream_rate *
                                self.channel_samples[channel_index])

                fft_sample_len = self.fft_size[channel_index]
                self.fft_freq_axes[channel_index] = \
                    numpy.fft.rfftfreq(fft_sample_len, 1 / channel_rate)
            else:
                # no data available to compute rate yet
                channel_rate = self.channel_rates[channel_index]
        else:
            channel_rate = self.channel_rates[channel_index]

        plot_rate = channel_rate / self.channel_downsample[channel_index]

        plot_array = self.plot_ringbuffers[channel_index].get_contents()
        if len(plot_array) > 0:
            length = len(plot_array)
            start = -(length - 1) / plot_rate
            time_axis = numpy.linspace(start, 0, length)
            for array, curve in zip(plot_array.transpose(),
                                    self.time_curves):
                curve.setData(time_axis, array.flatten())

        subchannel_index = self.fftSubchannelComboBox.currentIndex()
        if subchannel_index == -1:
            return

        ringbuffer = self.fft_ringbuffers[channel_index]
        fft_array = ringbuffer.get_contents()
        if ringbuffer.maxlen != len(fft_array):
            if not self.buffering:
                self.fftPlot.setTitle("Frequency Domain (Buffering)")
                self.buffering = True
            if self.last_channel_index != channel_index:
                # clear the FFT plot, as we don't have data for this channel,
                # and we can't keep displaying data from a different channel.
                self.fft_curve.clear()
        else:
            if self.buffering:
                self.fftPlot.setTitle("Frequency Domain")
                self.buffering = False
            fft_array = fft_array[:, subchannel_index].flatten()
            fft_array -= numpy.mean(fft_array)
            fft_size = self.fft_size[channel_index]
            fft_array = fft_array[0:fft_size]
            fft_data = numpy.abs(numpy.fft.rfft(fft_array)) * 2 / fft_size
            self.fft_curve.setData(self.fft_freq_axes[channel_index], fft_data)

        self.last_channel_index = channel_index

    def status_callback(self, status):
        if (status.startswith("error")):
            self.logger.error("Error in status: {}".format(status))
            self.stop_and_close()
            self.set_disconnected(self.tr("Error"))
        elif (status == "connected"):
            self.set_connected()
        else:
            self.logger.info("Status: {}".format(status))

    def status_thread_run(self):
        pipe = self.status_rx_pipe
        try:
            while True:
                # check if should exit
                if self.streaming_stopped.is_set():
                    break

                if pipe.poll(0.1):  # 100 ms
                    try:
                        data = pipe.recv()
                    except EOFError:
                        break

                    # send the data to status_callback()
                    self.status_received.emit(data)
        finally:
            self.status_rx_pipe.close()
            self.status_tx_pipe.close()

    def packet_callback(self, packet_list):
        for packet in packet_list:
            self.device_decoder.decode(packet)

    def packet_thread_run(self):
        pipe = self.packet_rx_pipe
        try:
            while True:
                # check if should exit
                if self.streaming_stopped.is_set():
                    break

                if pipe.poll(0.1):  # 100 ms
                    try:
                        packet_list = pipe.recv()
                    except EOFError:
                        break

                    for packet in packet_list:
                        self.device_decoder.decode(packet)
        finally:
            self.packet_rx_pipe.close()
            self.packet_tx_pipe.close()

    def start_streaming(self, streams):
        if self.streaming:
            raise AssertionError("Already Streaming")

        compression_level = self.settings.value("CompressionLevel")
        if compression_level is not None:
            try:
                compression_level = int(compression_level)
            except:
                compression_level = None  # default

        self.device_decoder.reset()

        if self.disable_streaming:
            indexes = []
        elif self.stream_list is True:
            indexes = list(range(len(streams)))
        else:
            indexes = [i for i in self.stream_list if i < len(streams)]

        if len(indexes) == 0:
            # No streams: can't start streaming
            self.set_connected()
            return

        warm_up_time = 0.0
        for stream in streams:
            if stream.warm_up_delay > warm_up_time:
                warm_up_time = stream.warm_up_delay

        active_streams = [s for i, s in enumerate(streams) if i in indexes]

        stream_counts = asphodel.nativelib.get_streaming_counts(
            active_streams, response_time=0.05, buffer_time=0.5, timeout=1000)

        header_dict = self.device_info.copy()
        header_dict['stream_counts'] = stream_counts
        header_dict['streams_to_activate'] = indexes
        header_dict['warm_up_time'] = warm_up_time

        self.streaming = True
        self.streaming_stopped.clear()

        rx, tx = multiprocessing.Pipe(False)
        self.status_rx_pipe = rx
        self.status_tx_pipe = tx
        self.status_thread = threading.Thread(target=self.status_thread_run)
        self.status_thread.start()

        rx, tx = multiprocessing.Pipe(False)
        self.packet_rx_pipe = rx
        self.packet_tx_pipe = tx
        self.packet_thread = threading.Thread(target=self.packet_thread_run)
        self.packet_thread.start()

        if self.upload_manager is not None:
            rx, tx = multiprocessing.Pipe(False)
            self.upload_rx_pipe = rx
            self.upload_tx_pipe = tx
            self.upload_manager.register_upload_pipe(self.upload_rx_pipe)
        else:
            self.upload_tx_pipe = None

        self.start_usb_operation(self.start_streaming_op, indexes,
                                 warm_up_time, stream_counts, header_dict,
                                 self.packet_tx_pipe, self.status_tx_pipe,
                                 self.display_name, self.base_dir,
                                 self.disable_archiving, compression_level,
                                 self.upload_tx_pipe)
        self.display_timer.start(100)  # 100 milliseconds

    def stop_streaming(self):
        if self.streaming:
            self.start_usb_operation(self.stop_streaming_op)
            self.streaming = False

    def stop_streaming_cb(self):
        # can't stop the threads until the stop_streaming_op has finished
        self.streaming_stopped.set()
        if self.status_thread:
            self.status_thread.join()
        if self.packet_thread:
            self.packet_thread.join()

    def get_plot_pens(self, subchannel_count):
        if subchannel_count == 1:
            return ['c']

        pens = ['b', 'g', 'r']
        if subchannel_count <= 3:
            return pens[:subchannel_count]

        return pens + ['c'] * (subchannel_count - len(pens))

    def graph_channel_changed(self, junk=None):
        index = self.graphChannelComboBox.currentIndex()
        if index == -1:
            return

        if self.last_channel_index is not None:
            self.save_plot_range(self.last_channel_index)

        self.fftSubchannelComboBox.clear()
        for subchannel_name in self.subchannel_names[index]:
            self.fftSubchannelComboBox.addItem(subchannel_name)
        if len(self.subchannel_names[index]) > 1:
            self.fftSubchannelComboBox.setEnabled(True)
        else:
            self.fftSubchannelComboBox.setEnabled(False)

        self.timePlot.clear()
        self.time_curves.clear()
        subchannel_count = len(self.subchannel_names[index])

        # remove the legend
        if self.legend:
            self.legend.scene().removeItem(self.legend)
            self.timePlot.legend = None
            self.legend = None

        if subchannel_count > 1:
            self.legend = self.timePlot.addLegend()

        pens = self.get_plot_pens(subchannel_count)
        for pen, subchannel_name in zip(pens, self.subchannel_names[index]):
            curve = self.timePlot.plot(pen=pen, name=subchannel_name)
            self.time_curves.append(curve)

        unit_str, unit_scale = self.unit_info[index]
        timeAxis = self.timePlot.getAxis('left')
        fftAxis = self.fftPlot.getAxis('left')
        if unit_scale is None:
            timeAxis.setScale(1.0)
            timeAxis.setLabel(unit_str, units="")
            fftAxis.setScale(1.0)
            fftAxis.setLabel(unit_str, units="")
        else:
            timeAxis.setScale(unit_scale)
            timeAxis.setLabel("", units=unit_str)
            fftAxis.setScale(unit_scale)
            fftAxis.setLabel("", units=unit_str)

        # add region for FFT size
        shortened, duration = self.fft_shortened[index]
        if shortened:
            lr = pyqtgraph.LinearRegionItem([-duration, 0], movable=False)
            self.timePlot.addItem(lr)

        self.restore_plot_range(index)

    def save_plot_range(self, index):
        save_dict = self.saved_plot_ranges.setdefault(index, {})

        time_vb = self.timePlot.getViewBox()
        time_autorange = time_vb.autoRangeEnabled()
        time_range = time_vb.targetRange()
        save_dict['time'] = (time_autorange, time_range)

        if self.fft_curve.getData()[0] is not None:
            fft_vb = self.fftPlot.getViewBox()
            fft_autorange = fft_vb.autoRangeEnabled()
            fft_range = fft_vb.targetRange()
            save_dict['fft'] = (fft_autorange, fft_range)

    def restore_plot_range(self, index):
        save_dict = self.saved_plot_ranges.get(index, {})

        def restore(vb, autorange, targetrange):
            x_autorange, y_autorange = autorange

            # restore the autorange
            vb.enableAutoRange(x=x_autorange, y=y_autorange)

            if not x_autorange:
                vb.setXRange(*targetrange[0], update=False, padding=0.0)
            if not y_autorange:
                vb.setYRange(*targetrange[1], update=False, padding=0.0)

        if 'time' in save_dict:
            restore(self.timePlot.getViewBox(), *save_dict['time'])
        else:
            restore(self.timePlot.getViewBox(), [True, True], [])

        if 'fft' in save_dict:
            restore(self.fftPlot.getViewBox(), *save_dict['fft'])
        else:
            restore(self.fftPlot.getViewBox(), [True, True], [])

    def rgb_set(self, color):
        if self.auto_rgb:
            try:
                rgb_widget = self.rgb_widgets[0]
                rgb_widget.set_color_from_button(color)
            except IndexError:
                pass

    def rgb_connected(self):
        if self.device_info['supports_radio']:
            self.rgb_set((0, 255, 255))  # cyan
        else:
            self.rgb_set((0, 0, 255))  # blue

    def rgb_disconnected(self):
        self.rgb_set((255, 0, 0))  # red

    def rgb_streaming(self):
        if self.device_info['supports_radio']:
            pass
        else:
            self.rgb_set((0, 255, 0))  # green

    def rgb_remote_connected(self):
        self.rgb_set((0, 0, 255))  # blue

    def rgb_remote_disconnected(self):
        self.rgb_set((0, 255, 255))  # cyan

    def rgb_remote_streaming(self):
        self.rgb_set((0, 255, 0))  # green
