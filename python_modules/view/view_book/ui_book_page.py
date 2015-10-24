# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_book/book_page.ui'
#
# Created: Wed Oct 21 21:03:26 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookHomepage(object):
    def setupUi(self, BookHomepage):
        BookHomepage.setObjectName("BookHomepage")
        BookHomepage.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(BookHomepage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(BookHomepage)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.left_page = QtWidgets.QWidget(self.widget)
        self.left_page.setObjectName("left_page")
        self.left_page_layout = QtWidgets.QHBoxLayout(self.left_page)
        self.left_page_layout.setContentsMargins(0, 0, 0, 0)
        self.left_page_layout.setObjectName("left_page_layout")
        self.verticalLayout.addWidget(self.left_page)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(BookHomepage)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.right_page = QtWidgets.QWidget(self.widget_2)
        self.right_page.setObjectName("right_page")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.right_page)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.right_page)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(BookHomepage)
        QtCore.QMetaObject.connectSlotsByName(BookHomepage)

    def retranslateUi(self, BookHomepage):
        _translate = QtCore.QCoreApplication.translate
        BookHomepage.setWindowTitle(_translate("BookHomepage", "Form"))

