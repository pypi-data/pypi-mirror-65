# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radio_panel.ui',
# licensing of 'radio_panel.ui' applies.
#
# Created: Fri Oct 25 09:11:21 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_RadioPanel(object):
    def setupUi(self, RadioPanel):
        RadioPanel.setObjectName("RadioPanel")
        RadioPanel.resize(115, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(RadioPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.detailScanButton = QtWidgets.QPushButton(RadioPanel)
        self.detailScanButton.setObjectName("detailScanButton")
        self.verticalLayout.addWidget(self.detailScanButton)
        self.devicesComboBox = QtWidgets.QComboBox(RadioPanel)
        self.devicesComboBox.setObjectName("devicesComboBox")
        self.verticalLayout.addWidget(self.devicesComboBox)
        self.scanButton = QtWidgets.QPushButton(RadioPanel)
        self.scanButton.setObjectName("scanButton")
        self.verticalLayout.addWidget(self.scanButton)
        self.connectButton = QtWidgets.QPushButton(RadioPanel)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.disconnectButton = QtWidgets.QPushButton(RadioPanel)
        self.disconnectButton.setObjectName("disconnectButton")
        self.verticalLayout.addWidget(self.disconnectButton)
        self.advancedMenuButton = QtWidgets.QPushButton(RadioPanel)
        self.advancedMenuButton.setObjectName("advancedMenuButton")
        self.verticalLayout.addWidget(self.advancedMenuButton)
        self.ctrlVarLayout = QtWidgets.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.goToRemoteButton = QtWidgets.QPushButton(RadioPanel)
        self.goToRemoteButton.setObjectName("goToRemoteButton")
        self.verticalLayout.addWidget(self.goToRemoteButton)
        self.actionConnectAnyBootloader = QtWidgets.QAction(RadioPanel)
        self.actionConnectAnyBootloader.setObjectName("actionConnectAnyBootloader")
        self.actionConnectSpecificBootloader = QtWidgets.QAction(RadioPanel)
        self.actionConnectSpecificBootloader.setObjectName("actionConnectSpecificBootloader")
        self.actionBootloaderScan = QtWidgets.QAction(RadioPanel)
        self.actionBootloaderScan.setObjectName("actionBootloaderScan")
        self.actionConnectNoStreaming = QtWidgets.QAction(RadioPanel)
        self.actionConnectNoStreaming.setObjectName("actionConnectNoStreaming")
        self.actionBulkClaim = QtWidgets.QAction(RadioPanel)
        self.actionBulkClaim.setObjectName("actionBulkClaim")
        self.actionBulkUpdateFirmware = QtWidgets.QAction(RadioPanel)
        self.actionBulkUpdateFirmware.setObjectName("actionBulkUpdateFirmware")

        self.retranslateUi(RadioPanel)
        QtCore.QMetaObject.connectSlotsByName(RadioPanel)

    def retranslateUi(self, RadioPanel):
        RadioPanel.setWindowTitle(QtWidgets.QApplication.translate("RadioPanel", "Radio Panel", None, -1))
        RadioPanel.setTitle(QtWidgets.QApplication.translate("RadioPanel", "Radio", None, -1))
        self.detailScanButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Detail Scan...", None, -1))
        self.scanButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Quick Scan", None, -1))
        self.connectButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Connect", None, -1))
        self.disconnectButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Disconnect", None, -1))
        self.advancedMenuButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Advanced Menu", None, -1))
        self.goToRemoteButton.setText(QtWidgets.QApplication.translate("RadioPanel", "Go To Remote Tab", None, -1))
        self.actionConnectAnyBootloader.setText(QtWidgets.QApplication.translate("RadioPanel", "Connect Any Bootloader", None, -1))
        self.actionConnectSpecificBootloader.setText(QtWidgets.QApplication.translate("RadioPanel", "Connect Specific Bootloader", None, -1))
        self.actionBootloaderScan.setText(QtWidgets.QApplication.translate("RadioPanel", "Bootloader Scan", None, -1))
        self.actionConnectNoStreaming.setText(QtWidgets.QApplication.translate("RadioPanel", "Connect (No Streaming)", None, -1))
        self.actionBulkClaim.setText(QtWidgets.QApplication.translate("RadioPanel", "Bulk Claim", None, -1))
        self.actionBulkClaim.setToolTip(QtWidgets.QApplication.translate("RadioPanel", "Bulk Claim", None, -1))
        self.actionBulkUpdateFirmware.setText(QtWidgets.QApplication.translate("RadioPanel", "Bulk Update Firmware", None, -1))

