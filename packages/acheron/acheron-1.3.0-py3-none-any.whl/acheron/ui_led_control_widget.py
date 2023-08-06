# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'led_control_widget.ui',
# licensing of 'led_control_widget.ui' applies.
#
# Created: Sun Mar 31 19:42:17 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LEDControlWidget(object):
    def setupUi(self, LEDControlWidget):
        LEDControlWidget.setObjectName("LEDControlWidget")
        LEDControlWidget.resize(176, 20)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(LEDControlWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.slider = QtWidgets.QSlider(LEDControlWidget)
        self.slider.setMinimumSize(QtCore.QSize(128, 0))
        self.slider.setMaximum(255)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout_3.addWidget(self.slider)
        self.spinBox = QtWidgets.QSpinBox(LEDControlWidget)
        self.spinBox.setMaximum(255)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)

        self.retranslateUi(LEDControlWidget)
        QtCore.QObject.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"), self.spinBox.setValue)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.slider.setValue)
        QtCore.QMetaObject.connectSlotsByName(LEDControlWidget)
        LEDControlWidget.setTabOrder(self.slider, self.spinBox)

    def retranslateUi(self, LEDControlWidget):
        LEDControlWidget.setWindowTitle(QtWidgets.QApplication.translate("LEDControlWidget", "LED Control Widget", None, -1))

