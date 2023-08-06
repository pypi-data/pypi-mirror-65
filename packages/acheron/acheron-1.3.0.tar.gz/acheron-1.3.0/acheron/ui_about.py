# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui',
# licensing of 'about.ui' applies.
#
# Created: Fri Mar 27 10:22:04 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(302, 232)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.productLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.productLabel.setFont(font)
        self.productLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.productLabel.setObjectName("productLabel")
        self.verticalLayout.addWidget(self.productLabel)
        self.companyLabel = QtWidgets.QLabel(AboutDialog)
        self.companyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.companyLabel.setOpenExternalLinks(True)
        self.companyLabel.setObjectName("companyLabel")
        self.verticalLayout.addWidget(self.companyLabel)
        self.copyrightLabel = QtWidgets.QLabel(AboutDialog)
        self.copyrightLabel.setTextFormat(QtCore.Qt.RichText)
        self.copyrightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.copyrightLabel.setObjectName("copyrightLabel")
        self.verticalLayout.addWidget(self.copyrightLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.version = QtWidgets.QLabel(AboutDialog)
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setObjectName("version")
        self.verticalLayout.addWidget(self.version)
        self.buildDate = QtWidgets.QLabel(AboutDialog)
        self.buildDate.setAlignment(QtCore.Qt.AlignCenter)
        self.buildDate.setObjectName("buildDate")
        self.verticalLayout.addWidget(self.buildDate)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.libraryVersionsLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.libraryVersionsLabel.setFont(font)
        self.libraryVersionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.libraryVersionsLabel.setObjectName("libraryVersionsLabel")
        self.verticalLayout.addWidget(self.libraryVersionsLabel)
        self.libraryVersions = QtWidgets.QLabel(AboutDialog)
        self.libraryVersions.setObjectName("libraryVersions")
        self.verticalLayout.addWidget(self.libraryVersions)
        spacerItem2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtWidgets.QApplication.translate("AboutDialog", "About Acheron", None, -1))
        self.productLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "Acheron", None, -1))
        self.companyLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "by <a href=\"http://suprocktech.com/\">Suprock Technologies</a>", None, -1))
        self.copyrightLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "&copy; 2019", None, -1))
        self.version.setText(QtWidgets.QApplication.translate("AboutDialog", "Version", None, -1))
        self.buildDate.setText(QtWidgets.QApplication.translate("AboutDialog", "Build Date", None, -1))
        self.libraryVersionsLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "Libraries", None, -1))
        self.libraryVersions.setText(QtWidgets.QApplication.translate("AboutDialog", "library: version", None, -1))

