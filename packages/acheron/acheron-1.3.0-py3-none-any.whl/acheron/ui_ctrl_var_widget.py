# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctrl_var_widget.ui',
# licensing of 'ctrl_var_widget.ui' applies.
#
# Created: Sun Mar 31 19:42:16 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CtrlVarWidget(object):
    def setupUi(self, CtrlVarWidget):
        CtrlVarWidget.setObjectName("CtrlVarWidget")
        CtrlVarWidget.resize(121, 19)
        self.horizontalLayout = QtWidgets.QHBoxLayout(CtrlVarWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameLabel = QtWidgets.QLabel(CtrlVarWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.horizontalLayout.addWidget(self.nameLabel)
        self.slider = QtWidgets.QSlider(CtrlVarWidget)
        self.slider.setMinimumSize(QtCore.QSize(50, 0))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)

        self.retranslateUi(CtrlVarWidget)
        QtCore.QMetaObject.connectSlotsByName(CtrlVarWidget)

    def retranslateUi(self, CtrlVarWidget):
        CtrlVarWidget.setWindowTitle(QtWidgets.QApplication.translate("CtrlVarWidget", "Ctrl Var Widget", None, -1))
        self.nameLabel.setText(QtWidgets.QApplication.translate("CtrlVarWidget", "Ctrl Var Name", None, -1))

