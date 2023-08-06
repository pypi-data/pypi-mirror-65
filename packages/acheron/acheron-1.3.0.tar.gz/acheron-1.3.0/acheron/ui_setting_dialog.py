# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_dialog.ui',
# licensing of 'setting_dialog.ui' applies.
#
# Created: Sun Mar 31 19:42:18 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(400, 53)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(SettingDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SettingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SettingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        SettingDialog.setWindowTitle(QtWidgets.QApplication.translate("SettingDialog", "Device Settings", None, -1))

