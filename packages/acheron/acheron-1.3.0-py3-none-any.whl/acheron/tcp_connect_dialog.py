import logging

from PySide2 import QtCore, QtGui, QtWidgets

from hyperborea.preferences import read_bool_setting

from .ui_tcp_connect_dialog import Ui_TCPConnectDialog

logger = logging.getLogger(__name__)


class TCPConnectDialog(QtWidgets.QDialog, Ui_TCPConnectDialog):
    def __init__(self, devices, connected_location_strs, rescan_func,
                 parent=None):
        super().__init__(parent)

        self.connected_location_strs = connected_location_strs
        self.rescan_func = rescan_func

        self.settings = QtCore.QSettings()

        self.device_by_row = []

        self.setupUi(self)
        self.extra_ui_setup()

        self.tableWidget.itemSelectionChanged.connect(self.selection_changed)

        self.add_device_rows(devices)
        self.selection_changed()

    def extra_ui_setup(self):
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.rescanButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Reset)
        self.rescanButton.setText(self.tr("Rescan"))
        self.rescanButton.clicked.connect(self.rescan)

        self.tableWidget.cellDoubleClicked.connect(self.double_click_cb)
        self.tableWidget.itemDoubleClicked.connect(self.double_click_cb)

        self.rescan_timer = QtCore.QTimer(self)
        self.rescan_timer.timeout.connect(self.rescan)

        self.automaticRescan.toggled.connect(self.set_automatic_rescan)

        automatic_rescan = read_bool_setting(self.settings, "AutomaticRescan",
                                             True)
        self.automaticRescan.setChecked(automatic_rescan)

        self.finished.connect(self.rescan_timer.stop)

    def set_automatic_rescan(self, junk=None):
        if self.automaticRescan.isChecked():
            self.settings.setValue("AutomaticRescan", 1)
            self.rescan_timer.start(1000)
        else:
            self.settings.setValue("AutomaticRescan", 0)
            self.rescan_timer.stop()

    def double_click_cb(self, row=None, column=None):
        self.accept()

    def sort_devices(self, all_devices):
        def key_func(t):
            device, _connected_bool = t
            adv = device.tcp_get_advertisement()
            return (adv.connected, adv.serial_number)
        return sorted(all_devices, key=key_func)

    def add_device_row(self, device, connected):
        # add a blank row
        row_index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_index)
        self.device_by_row.append(device)

        adv = device.tcp_get_advertisement()
        is_boot = device.supports_bootloader_commands()

        if connected:
            item_flags = QtCore.Qt.NoItemFlags
            available_str = "No (tab already open)"
        elif adv.connected:
            item_flags = QtCore.Qt.NoItemFlags
            available_str = "No (in use)"
        else:
            item_flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            available_str = "Yes"

        serial_number_item = QtWidgets.QTableWidgetItem(adv.serial_number)
        serial_number_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 0, serial_number_item)

        user_tag1_item = QtWidgets.QTableWidgetItem(adv.user_tag1)
        user_tag1_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 1, user_tag1_item)

        user_tag2_item = QtWidgets.QTableWidgetItem(adv.user_tag2)
        user_tag2_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 2, user_tag2_item)

        board_info_str = "{} rev {}".format(adv.board_type, adv.board_rev)
        board_info_item = QtWidgets.QTableWidgetItem(board_info_str)
        board_info_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 3, board_info_item)

        build_info_item = QtWidgets.QTableWidgetItem(adv.build_info)
        build_info_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 4, build_info_item)

        build_date_item = QtWidgets.QTableWidgetItem(adv.build_date)
        build_date_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 5, build_date_item)

        if is_boot:
            bootloader_item = QtWidgets.QTableWidgetItem("Running")
            font = QtGui.QFont()
            font.setBold(True)
            bootloader_item.setFont(font)
        else:
            bootloader_item = QtWidgets.QTableWidgetItem("")
        bootloader_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 6, bootloader_item)

        available_item = QtWidgets.QTableWidgetItem(available_str)
        available_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 7, available_item)

        # highlight the whole row yellow if it's a bootloader
        if is_boot:
            brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.yellow))
            serial_number_item.setBackground(brush)
            user_tag1_item.setBackground(brush)
            user_tag2_item.setBackground(brush)
            board_info_item.setBackground(brush)
            build_info_item.setBackground(brush)
            build_date_item.setBackground(brush)
            bootloader_item.setBackground(brush)
            available_item.setBackground(brush)

    def add_device_rows(self, devices):
        all_devices = []
        for device in devices:
            location_str = device.get_location_string()
            connected_bool = location_str in self.connected_location_strs
            all_devices.append((device, connected_bool))

        for device, connected_bool in self.sort_devices(all_devices):
            self.add_device_row(device, connected_bool)

    def get_selected_devices(self):
        selected_devices = []
        for index in self.tableWidget.selectionModel().selectedRows():
            selected_devices.append(self.device_by_row[index.row()])
        return selected_devices

    def get_selected_serials(self):
        selected_devices = self.get_selected_devices()
        serials = []
        for device in selected_devices:
            adv = device.tcp_get_advertisement()
            serials.append(adv.serial_number)
        return serials

    def select_serials(self, serials):
        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)

        for i, device in enumerate(self.device_by_row):
            adv = device.tcp_get_advertisement()
            serial = adv.serial_number
            if serial in serials:
                self.tableWidget.selectRow(i)

        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

        self.selection_changed()

    def selection_changed(self):
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if self.tableWidget.selectionModel().hasSelection():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    def rescan(self):
        self.rescanButton.setEnabled(False)

        selected_serials = self.get_selected_serials()

        # clear the existing devices
        self.tableWidget.setRowCount(0)
        self.device_by_row.clear()

        new_devices = self.rescan_func()
        self.add_device_rows(new_devices)

        self.select_serials(selected_serials)

        self.rescanButton.setEnabled(True)
