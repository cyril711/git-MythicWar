# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/main_view/dialog_thumb_generator.ui'
#
# Created: Sat Jan 31 23:25:09 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogThumbGenerator(object):
    def setupUi(self, DialogThumbGenerator):
        DialogThumbGenerator.setObjectName("DialogThumbGenerator")
        DialogThumbGenerator.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DialogThumbGenerator)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(DialogThumbGenerator)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.factionComboBox = QtWidgets.QComboBox(self.widget)
        self.factionComboBox.setObjectName("factionComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.factionComboBox)
        self.empireComboBox = QtWidgets.QComboBox(self.widget)
        self.empireComboBox.setObjectName("empireComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.empireComboBox)
        self.kingdomComboBox = QtWidgets.QComboBox(self.widget)
        self.kingdomComboBox.setObjectName("kingdomComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.kingdomComboBox)
        self.horizontalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogThumbGenerator)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogThumbGenerator)
        self.buttonBox.accepted.connect(DialogThumbGenerator.accept)
        self.buttonBox.rejected.connect(DialogThumbGenerator.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogThumbGenerator)

    def retranslateUi(self, DialogThumbGenerator):
        _translate = QtCore.QCoreApplication.translate
        DialogThumbGenerator.setWindowTitle(_translate("DialogThumbGenerator", "Dialog"))
        self.label.setText(_translate("DialogThumbGenerator", "Faction :"))
        self.label_2.setText(_translate("DialogThumbGenerator", "Empire :"))
        self.label_3.setText(_translate("DialogThumbGenerator", "Kingdom :"))

