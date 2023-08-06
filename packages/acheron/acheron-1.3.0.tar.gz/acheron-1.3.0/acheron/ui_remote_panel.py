# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remote_panel.ui',
# licensing of 'remote_panel.ui' applies.
#
# Created: Sun Mar 31 19:42:17 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_RemotePanel(object):
    def setupUi(self, RemotePanel):
        RemotePanel.setObjectName("RemotePanel")
        RemotePanel.resize(112, 182)
        self.verticalLayout = QtWidgets.QVBoxLayout(RemotePanel)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.goToParentButton = QtWidgets.QPushButton(RemotePanel)
        self.goToParentButton.setObjectName("goToParentButton")
        self.verticalLayout.addWidget(self.goToParentButton)

        self.retranslateUi(RemotePanel)
        QtCore.QMetaObject.connectSlotsByName(RemotePanel)

    def retranslateUi(self, RemotePanel):
        RemotePanel.setWindowTitle(QtWidgets.QApplication.translate("RemotePanel", "Remote Device Panel", None, -1))
        RemotePanel.setTitle(QtWidgets.QApplication.translate("RemotePanel", "Remote Device", None, -1))
        self.goToParentButton.setText(QtWidgets.QApplication.translate("RemotePanel", "Go To Radio Tab", None, -1))

