# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/main_view/dialog_settings.ui'
#
# Created: Sat Jan 31 23:25:09 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSettings(object):
    def setupUi(self, DialogSettings):
        DialogSettings.setObjectName("DialogSettings")
        DialogSettings.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogSettings)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBoxMapGoogleTile = QtWidgets.QComboBox(DialogSettings)
        self.comboBoxMapGoogleTile.setGeometry(QtCore.QRect(140, 50, 69, 22))
        self.comboBoxMapGoogleTile.setObjectName("comboBoxMapGoogleTile")
        self.actionActionSettings = QtWidgets.QAction(DialogSettings)
        self.actionActionSettings.setObjectName("actionActionSettings")

        self.retranslateUi(DialogSettings)
        self.buttonBox.accepted.connect(DialogSettings.accept)
        self.buttonBox.rejected.connect(DialogSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogSettings)

    def retranslateUi(self, DialogSettings):
        _translate = QtCore.QCoreApplication.translate
        DialogSettings.setWindowTitle(_translate("DialogSettings", "Dialog"))
        self.actionActionSettings.setText(_translate("DialogSettings", "actionSettings"))

