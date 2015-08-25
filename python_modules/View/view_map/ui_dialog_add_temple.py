# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_map/add_temple_dialog.ui'
#
# Created: Mon Aug 24 21:06:59 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogAddTemple(object):
    def setupUi(self, DialogAddTemple):
        DialogAddTemple.setObjectName("DialogAddTemple")
        DialogAddTemple.resize(464, 301)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAddTemple)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(DialogAddTemple)
        self.widget.setGeometry(QtCore.QRect(26, 19, 151, 230))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MainCheckBox = QtWidgets.QCheckBox(self.widget)
        self.MainCheckBox.setObjectName("MainCheckBox")
        self.verticalLayout.addWidget(self.MainCheckBox)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.formLayout = QtWidgets.QFormLayout(self.widget_2)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.factionComboBOx = QtWidgets.QComboBox(self.widget_2)
        self.factionComboBOx.setObjectName("factionComboBOx")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.factionComboBOx)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.empireComboBox = QtWidgets.QComboBox(self.widget_2)
        self.empireComboBox.setObjectName("empireComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.empireComboBox)
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.kingdomComboBox = QtWidgets.QComboBox(self.widget_2)
        self.kingdomComboBox.setObjectName("kingdomComboBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.kingdomComboBox)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.addButton = QtWidgets.QPushButton(self.widget_2)
        self.addButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/24x24/add"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QtCore.QSize(16, 16))
        self.addButton.setFlat(True)
        self.addButton.setObjectName("addButton")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.addButton)
        self.removeButton = QtWidgets.QPushButton(self.widget_2)
        self.removeButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/24x24/quit"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon1)
        self.removeButton.setFlat(True)
        self.removeButton.setObjectName("removeButton")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.removeButton)
        self.verticalLayout.addWidget(self.widget_2)
        self.EtagesWidget = QtWidgets.QWidget(self.widget)
        self.EtagesWidget.setObjectName("EtagesWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.EtagesWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.EtagesWidget)

        self.retranslateUi(DialogAddTemple)
        self.buttonBox.accepted.connect(DialogAddTemple.accept)
        self.buttonBox.rejected.connect(DialogAddTemple.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAddTemple)

    def retranslateUi(self, DialogAddTemple):
        _translate = QtCore.QCoreApplication.translate
        DialogAddTemple.setWindowTitle(_translate("DialogAddTemple", "Dialog"))
        self.MainCheckBox.setText(_translate("DialogAddTemple", "Main"))
        self.label.setText(_translate("DialogAddTemple", "Faction"))
        self.label_4.setText(_translate("DialogAddTemple", "Empire"))
        self.label_2.setText(_translate("DialogAddTemple", "Kingdom"))
        self.label_3.setText(_translate("DialogAddTemple", "Etages :"))

import resources_rc
