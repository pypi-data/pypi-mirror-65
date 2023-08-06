# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radio_scan_dialog.ui',
# licensing of 'radio_scan_dialog.ui' applies.
#
# Created: Fri Apr 19 13:54:54 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_RadioScanDialog(object):
    def setupUi(self, RadioScanDialog):
        RadioScanDialog.setObjectName("RadioScanDialog")
        RadioScanDialog.resize(1000, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(RadioScanDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(RadioScanDialog)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView.setSortingEnabled(True)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.activeScan = QtWidgets.QCheckBox(RadioScanDialog)
        self.activeScan.setObjectName("activeScan")
        self.horizontalLayout.addWidget(self.activeScan)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.filterLabel = QtWidgets.QLabel(RadioScanDialog)
        self.filterLabel.setObjectName("filterLabel")
        self.horizontalLayout.addWidget(self.filterLabel)
        self.filterSlider = QtWidgets.QSlider(RadioScanDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterSlider.sizePolicy().hasHeightForWidth())
        self.filterSlider.setSizePolicy(sizePolicy)
        self.filterSlider.setMinimumSize(QtCore.QSize(200, 0))
        self.filterSlider.setMinimum(-100)
        self.filterSlider.setMaximum(0)
        self.filterSlider.setOrientation(QtCore.Qt.Horizontal)
        self.filterSlider.setObjectName("filterSlider")
        self.horizontalLayout.addWidget(self.filterSlider)
        self.filterSpinBox = QtWidgets.QSpinBox(RadioScanDialog)
        self.filterSpinBox.setMinimum(-100)
        self.filterSpinBox.setMaximum(0)
        self.filterSpinBox.setObjectName("filterSpinBox")
        self.horizontalLayout.addWidget(self.filterSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(RadioScanDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RadioScanDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), RadioScanDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), RadioScanDialog.reject)
        QtCore.QObject.connect(self.filterSlider, QtCore.SIGNAL("valueChanged(int)"), self.filterSpinBox.setValue)
        QtCore.QObject.connect(self.filterSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.filterSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(RadioScanDialog)

    def retranslateUi(self, RadioScanDialog):
        RadioScanDialog.setWindowTitle(QtWidgets.QApplication.translate("RadioScanDialog", "Radio Scan", None, -1))
        self.activeScan.setText(QtWidgets.QApplication.translate("RadioScanDialog", "Active Scan", None, -1))
        self.filterLabel.setText(QtWidgets.QApplication.translate("RadioScanDialog", "Filter", None, -1))
        self.filterSpinBox.setSuffix(QtWidgets.QApplication.translate("RadioScanDialog", " dBm", None, -1))

