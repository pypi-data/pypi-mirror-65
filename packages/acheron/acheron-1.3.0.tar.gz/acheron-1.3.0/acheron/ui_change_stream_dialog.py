# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_stream_dialog.ui',
# licensing of 'change_stream_dialog.ui' applies.
#
# Created: Sun Mar 31 19:42:15 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ChangeStreamDialog(object):
    def setupUi(self, ChangeStreamDialog):
        ChangeStreamDialog.setObjectName("ChangeStreamDialog")
        ChangeStreamDialog.resize(403, 49)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ChangeStreamDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChangeStreamDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ChangeStreamDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ChangeStreamDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ChangeStreamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeStreamDialog)

    def retranslateUi(self, ChangeStreamDialog):
        ChangeStreamDialog.setWindowTitle(QtWidgets.QApplication.translate("ChangeStreamDialog", "Change Streams", None, -1))

