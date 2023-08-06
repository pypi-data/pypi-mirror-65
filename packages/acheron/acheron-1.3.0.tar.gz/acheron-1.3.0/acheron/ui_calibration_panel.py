# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calibration_panel.ui',
# licensing of 'calibration_panel.ui' applies.
#
# Created: Fri Oct 25 09:11:18 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CalibrationPanel(object):
    def setupUi(self, CalibrationPanel):
        CalibrationPanel.setObjectName("CalibrationPanel")
        CalibrationPanel.resize(95, 158)
        self.verticalLayout = QtWidgets.QVBoxLayout(CalibrationPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(CalibrationPanel)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CalibrationPanel)
        QtCore.QMetaObject.connectSlotsByName(CalibrationPanel)

    def retranslateUi(self, CalibrationPanel):
        CalibrationPanel.setWindowTitle(QtWidgets.QApplication.translate("CalibrationPanel", "Calibration", None, -1))
        CalibrationPanel.setTitle(QtWidgets.QApplication.translate("CalibrationPanel", "Calibration", None, -1))

