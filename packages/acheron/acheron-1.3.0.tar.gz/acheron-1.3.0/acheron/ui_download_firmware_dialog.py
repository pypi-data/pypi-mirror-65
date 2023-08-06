# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_firmware_dialog.ui',
# licensing of 'download_firmware_dialog.ui' applies.
#
# Created: Mon May 13 14:06:33 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DownloadFirmwareDialog(object):
    def setupUi(self, DownloadFirmwareDialog):
        DownloadFirmwareDialog.setObjectName("DownloadFirmwareDialog")
        DownloadFirmwareDialog.resize(374, 147)
        self.formLayout = QtWidgets.QFormLayout(DownloadFirmwareDialog)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.boardRadioButton = QtWidgets.QRadioButton(DownloadFirmwareDialog)
        self.boardRadioButton.setChecked(False)
        self.boardRadioButton.setObjectName("boardRadioButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.boardRadioButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.boardName = QtWidgets.QLineEdit(DownloadFirmwareDialog)
        self.boardName.setMinimumSize(QtCore.QSize(200, 0))
        self.boardName.setObjectName("boardName")
        self.horizontalLayout.addWidget(self.boardName)
        self.revLabel = QtWidgets.QLabel(DownloadFirmwareDialog)
        self.revLabel.setObjectName("revLabel")
        self.horizontalLayout.addWidget(self.revLabel)
        self.boardRev = QtWidgets.QSpinBox(DownloadFirmwareDialog)
        self.boardRev.setMaximum(255)
        self.boardRev.setProperty("value", 1)
        self.boardRev.setObjectName("boardRev")
        self.horizontalLayout.addWidget(self.boardRev)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.repoRadioButton = QtWidgets.QRadioButton(DownloadFirmwareDialog)
        self.repoRadioButton.setObjectName("repoRadioButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.repoRadioButton)
        self.repoName = QtWidgets.QLineEdit(DownloadFirmwareDialog)
        self.repoName.setEnabled(False)
        self.repoName.setObjectName("repoName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.repoName)
        self.branchRadioButton = QtWidgets.QRadioButton(DownloadFirmwareDialog)
        self.branchRadioButton.setChecked(True)
        self.branchRadioButton.setObjectName("branchRadioButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.branchRadioButton)
        self.branchName = QtWidgets.QLineEdit(DownloadFirmwareDialog)
        self.branchName.setObjectName("branchName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.branchName)
        self.commitRadioButton = QtWidgets.QRadioButton(DownloadFirmwareDialog)
        self.commitRadioButton.setObjectName("commitRadioButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.commitRadioButton)
        self.commitHash = QtWidgets.QLineEdit(DownloadFirmwareDialog)
        self.commitHash.setEnabled(False)
        self.commitHash.setObjectName("commitHash")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.commitHash)
        self.buttonBox = QtWidgets.QDialogButtonBox(DownloadFirmwareDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(DownloadFirmwareDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DownloadFirmwareDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DownloadFirmwareDialog.reject)
        QtCore.QObject.connect(self.boardRadioButton, QtCore.SIGNAL("toggled(bool)"), self.boardName.setEnabled)
        QtCore.QObject.connect(self.boardRadioButton, QtCore.SIGNAL("toggled(bool)"), self.boardRev.setEnabled)
        QtCore.QObject.connect(self.repoRadioButton, QtCore.SIGNAL("toggled(bool)"), self.repoName.setEnabled)
        QtCore.QObject.connect(self.branchRadioButton, QtCore.SIGNAL("toggled(bool)"), self.branchName.setEnabled)
        QtCore.QObject.connect(self.commitRadioButton, QtCore.SIGNAL("toggled(bool)"), self.commitHash.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(DownloadFirmwareDialog)
        DownloadFirmwareDialog.setTabOrder(self.boardRadioButton, self.boardName)
        DownloadFirmwareDialog.setTabOrder(self.boardName, self.boardRev)
        DownloadFirmwareDialog.setTabOrder(self.boardRev, self.repoRadioButton)
        DownloadFirmwareDialog.setTabOrder(self.repoRadioButton, self.repoName)
        DownloadFirmwareDialog.setTabOrder(self.repoName, self.branchRadioButton)
        DownloadFirmwareDialog.setTabOrder(self.branchRadioButton, self.branchName)
        DownloadFirmwareDialog.setTabOrder(self.branchName, self.commitRadioButton)
        DownloadFirmwareDialog.setTabOrder(self.commitRadioButton, self.commitHash)
        DownloadFirmwareDialog.setTabOrder(self.commitHash, self.buttonBox)

    def retranslateUi(self, DownloadFirmwareDialog):
        DownloadFirmwareDialog.setWindowTitle(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Download Firmware", None, -1))
        self.boardRadioButton.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Board", None, -1))
        self.revLabel.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Rev", None, -1))
        self.repoRadioButton.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Repository", None, -1))
        self.branchRadioButton.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Branch", None, -1))
        self.branchName.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "master", None, -1))
        self.commitRadioButton.setText(QtWidgets.QApplication.translate("DownloadFirmwareDialog", "Commit", None, -1))

