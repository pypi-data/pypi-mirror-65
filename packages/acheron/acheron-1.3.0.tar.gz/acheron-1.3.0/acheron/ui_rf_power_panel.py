# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rf_power_panel.ui',
# licensing of 'rf_power_panel.ui' applies.
#
# Created: Sun Mar 31 19:42:18 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_RFPowerPanel(object):
    def setupUi(self, RFPowerPanel):
        RFPowerPanel.setObjectName("RFPowerPanel")
        RFPowerPanel.resize(111, 99)
        self.verticalLayout = QtWidgets.QVBoxLayout(RFPowerPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.enableButton = QtWidgets.QPushButton(RFPowerPanel)
        self.enableButton.setObjectName("enableButton")
        self.verticalLayout.addWidget(self.enableButton)
        self.disableButton = QtWidgets.QPushButton(RFPowerPanel)
        self.disableButton.setObjectName("disableButton")
        self.verticalLayout.addWidget(self.disableButton)
        self.ctrlVarLayout = QtWidgets.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(RFPowerPanel)
        QtCore.QMetaObject.connectSlotsByName(RFPowerPanel)

    def retranslateUi(self, RFPowerPanel):
        RFPowerPanel.setWindowTitle(QtWidgets.QApplication.translate("RFPowerPanel", "RF Power Panel", None, -1))
        RFPowerPanel.setTitle(QtWidgets.QApplication.translate("RFPowerPanel", "RF Power", None, -1))
        self.enableButton.setText(QtWidgets.QApplication.translate("RFPowerPanel", "Enable RF Power", None, -1))
        self.disableButton.setText(QtWidgets.QApplication.translate("RFPowerPanel", "Disable RF Power", None, -1))

