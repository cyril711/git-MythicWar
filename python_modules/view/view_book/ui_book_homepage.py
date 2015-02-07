# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_book/book_homepage.ui'
#
# Created: Mon Jan 19 21:23:03 2015
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
        self.Tree_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(24)
        self.Tree_label.setFont(font)
        self.Tree_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Tree_label.setObjectName("Tree_label")
        self.verticalLayout.addWidget(self.Tree_label)
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
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_3)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.vignettes = QtWidgets.QWidget()
        self.vignettes.setGeometry(QtCore.QRect(0, 0, 150, 244))
        self.vignettes.setObjectName("vignettes")
        self.gridLayout = QtWidgets.QGridLayout(self.vignettes)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.vignettes)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(BookHomepage)
        QtCore.QMetaObject.connectSlotsByName(BookHomepage)

    def retranslateUi(self, BookHomepage):
        _translate = QtCore.QCoreApplication.translate
        BookHomepage.setWindowTitle(_translate("BookHomepage", "Form"))
        self.Tree_label.setText(_translate("BookHomepage", "Sommaire"))

