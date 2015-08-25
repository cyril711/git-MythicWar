# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_kingdom/kingdom_layout.ui'
#
# Created: Mon Aug 24 21:06:56 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_KingdomLayout(object):
    def setupUi(self, KingdomLayout):
        KingdomLayout.setObjectName("KingdomLayout")
        KingdomLayout.resize(625, 448)
        KingdomLayout.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(KingdomLayout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.previous_button = QtWidgets.QPushButton(KingdomLayout)
        self.previous_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_button.sizePolicy().hasHeightForWidth())
        self.previous_button.setSizePolicy(sizePolicy)
        self.previous_button.setMinimumSize(QtCore.QSize(10, 0))
        self.previous_button.setObjectName("previous_button")
        self.horizontalLayout.addWidget(self.previous_button)
        self.stackedWidget = QtWidgets.QStackedWidget(KingdomLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(200, 200))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.next_button = QtWidgets.QPushButton(KingdomLayout)
        self.next_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setMinimumSize(QtCore.QSize(10, 0))
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)

        self.retranslateUi(KingdomLayout)
        QtCore.QMetaObject.connectSlotsByName(KingdomLayout)

    def retranslateUi(self, KingdomLayout):
        _translate = QtCore.QCoreApplication.translate
        KingdomLayout.setWindowTitle(_translate("KingdomLayout", "Form"))
        self.previous_button.setText(_translate("KingdomLayout", "Previous"))
        self.next_button.setText(_translate("KingdomLayout", "Next"))

