# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hardware_tests.ui',
# licensing of 'hardware_tests.ui' applies.
#
# Created: Tue Apr  2 19:21:47 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_HardwareTestDialog(object):
    def setupUi(self, HardwareTestDialog):
        HardwareTestDialog.setObjectName("HardwareTestDialog")
        HardwareTestDialog.resize(754, 426)
        self.verticalLayout = QtWidgets.QVBoxLayout(HardwareTestDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.testOutput = QtWidgets.QPlainTextEdit(HardwareTestDialog)
        self.testOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.testOutput.setReadOnly(True)
        self.testOutput.setObjectName("testOutput")
        self.verticalLayout.addWidget(self.testOutput)
        self.buttonBox = QtWidgets.QDialogButtonBox(HardwareTestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HardwareTestDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), HardwareTestDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), HardwareTestDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HardwareTestDialog)

    def retranslateUi(self, HardwareTestDialog):
        HardwareTestDialog.setWindowTitle(QtWidgets.QApplication.translate("HardwareTestDialog", "Hardware Tests", None, -1))

