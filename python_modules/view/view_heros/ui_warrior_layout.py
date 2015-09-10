# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_heros/warrior_layout.ui'
#
# Created: Thu Sep 10 22:05:23 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WarriorLayout(object):
    def setupUi(self, WarriorLayout):
        WarriorLayout.setObjectName("WarriorLayout")
        WarriorLayout.resize(527, 427)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WarriorLayout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(WarriorLayout)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.previous_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_button.sizePolicy().hasHeightForWidth())
        self.previous_button.setSizePolicy(sizePolicy)
        self.previous_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/24x24/previous"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous_button.setIcon(icon)
        self.previous_button.setIconSize(QtCore.QSize(24, 24))
        self.previous_button.setObjectName("previous_button")
        self.verticalLayout.addWidget(self.previous_button)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout.addWidget(self.widget)
        self.next_button = QtWidgets.QPushButton(WarriorLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/24x24/next"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_button.setIcon(icon1)
        self.next_button.setIconSize(QtCore.QSize(24, 24))
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(WarriorLayout)
        QtCore.QMetaObject.connectSlotsByName(WarriorLayout)

    def retranslateUi(self, WarriorLayout):
        _translate = QtCore.QCoreApplication.translate
        WarriorLayout.setWindowTitle(_translate("WarriorLayout", "Form"))
        self.previous_button.setShortcut(_translate("WarriorLayout", "Left"))
        self.next_button.setShortcut(_translate("WarriorLayout", "Right"))

import resources_rc
