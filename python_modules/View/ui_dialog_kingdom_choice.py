# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/View/dialog_kingdom_choice.ui'
#
# Created: Tue Dec  9 22:08:16 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogKingdomChoice(object):
    def setupUi(self, DialogKingdomChoice):
        DialogKingdomChoice.setObjectName("DialogKingdomChoice")
        DialogKingdomChoice.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogKingdomChoice)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(DialogKingdomChoice)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBoxFaction = QtWidgets.QComboBox(self.widget)
        self.comboBoxFaction.setObjectName("comboBoxFaction")
        self.verticalLayout.addWidget(self.comboBoxFaction)
        self.comboBoxEmpire = QtWidgets.QComboBox(self.widget)
        self.comboBoxEmpire.setObjectName("comboBoxEmpire")
        self.verticalLayout.addWidget(self.comboBoxEmpire)
        self.comboBoxKingdom = QtWidgets.QComboBox(self.widget)
        self.comboBoxKingdom.setObjectName("comboBoxKingdom")
        self.verticalLayout.addWidget(self.comboBoxKingdom)
        self.verticalLayout_2.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogKingdomChoice)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(DialogKingdomChoice)
        self.buttonBox.accepted.connect(DialogKingdomChoice.accept)
        self.buttonBox.rejected.connect(DialogKingdomChoice.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogKingdomChoice)

    def retranslateUi(self, DialogKingdomChoice):
        _translate = QtCore.QCoreApplication.translate
        DialogKingdomChoice.setWindowTitle(_translate("DialogKingdomChoice", "Dialog"))

