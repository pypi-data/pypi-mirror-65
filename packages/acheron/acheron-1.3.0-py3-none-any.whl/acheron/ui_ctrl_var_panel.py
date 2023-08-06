# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctrl_var_panel.ui',
# licensing of 'ctrl_var_panel.ui' applies.
#
# Created: Sun Mar 31 19:42:15 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CtrlVarPanel(object):
    def setupUi(self, CtrlVarPanel):
        CtrlVarPanel.setObjectName("CtrlVarPanel")
        CtrlVarPanel.resize(99, 41)
        self.verticalLayout = QtWidgets.QVBoxLayout(CtrlVarPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ctrlVarLayout = QtWidgets.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(CtrlVarPanel)
        QtCore.QMetaObject.connectSlotsByName(CtrlVarPanel)

    def retranslateUi(self, CtrlVarPanel):
        CtrlVarPanel.setWindowTitle(QtWidgets.QApplication.translate("CtrlVarPanel", "Control Variable Panel", None, -1))
        CtrlVarPanel.setTitle(QtWidgets.QApplication.translate("CtrlVarPanel", "Control Variables", None, -1))

