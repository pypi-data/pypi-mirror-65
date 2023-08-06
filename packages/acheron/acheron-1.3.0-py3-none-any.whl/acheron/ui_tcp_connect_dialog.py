# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tcp_connect_dialog.ui',
# licensing of 'tcp_connect_dialog.ui' applies.
#
# Created: Fri Oct 25 09:11:22 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TCPConnectDialog(object):
    def setupUi(self, TCPConnectDialog):
        TCPConnectDialog.setObjectName("TCPConnectDialog")
        TCPConnectDialog.resize(915, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(TCPConnectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(TCPConnectDialog)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.automaticRescan = QtWidgets.QCheckBox(TCPConnectDialog)
        self.automaticRescan.setObjectName("automaticRescan")
        self.verticalLayout.addWidget(self.automaticRescan)
        self.buttonBox = QtWidgets.QDialogButtonBox(TCPConnectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TCPConnectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), TCPConnectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), TCPConnectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TCPConnectDialog)

    def retranslateUi(self, TCPConnectDialog):
        TCPConnectDialog.setWindowTitle(QtWidgets.QApplication.translate("TCPConnectDialog", "TCP Devices", None, -1))
        self.tableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Serial", None, -1))
        self.tableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Tag 1", None, -1))
        self.tableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Tag 2", None, -1))
        self.tableWidget.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Board Info", None, -1))
        self.tableWidget.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Build Info", None, -1))
        self.tableWidget.horizontalHeaderItem(5).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Build Date", None, -1))
        self.tableWidget.horizontalHeaderItem(6).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Bootloader", None, -1))
        self.tableWidget.horizontalHeaderItem(7).setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Available", None, -1))
        self.automaticRescan.setText(QtWidgets.QApplication.translate("TCPConnectDialog", "Automatic Rescan", None, -1))

