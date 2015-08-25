# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_book/book_layout.ui'
#
# Created: Mon Aug 24 21:06:59 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookLayout(object):
    def setupUi(self, BookLayout):
        BookLayout.setObjectName("BookLayout")
        BookLayout.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(BookLayout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(BookLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(100, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_view_page = QtWidgets.QWidget(self.widget_2)
        self.tree_view_page.setObjectName("tree_view_page")
        self.tree_view_layout = QtWidgets.QVBoxLayout(self.tree_view_page)
        self.tree_view_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_view_layout.setObjectName("tree_view_layout")
        self.verticalLayout.addWidget(self.tree_view_page)
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(BookLayout)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.stackedWidget.addWidget(self.page_4)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.previous = QtWidgets.QPushButton(self.widget_4)
        self.previous.setEnabled(False)
        self.previous.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/24x24/previous"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous.setIcon(icon)
        self.previous.setFlat(True)
        self.previous.setObjectName("previous")
        self.horizontalLayout_3.addWidget(self.previous)
        self.next = QtWidgets.QPushButton(self.widget_4)
        self.next.setEnabled(False)
        self.next.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/24x24/next"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon1)
        self.next.setFlat(True)
        self.next.setObjectName("next")
        self.horizontalLayout_3.addWidget(self.next)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(BookLayout)
        QtCore.QMetaObject.connectSlotsByName(BookLayout)

    def retranslateUi(self, BookLayout):
        _translate = QtCore.QCoreApplication.translate
        BookLayout.setWindowTitle(_translate("BookLayout", "Form"))

import resources_rc
