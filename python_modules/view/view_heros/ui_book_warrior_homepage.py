# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_heros/book_warrior_homepage.ui'
#
# Created: Sat Dec 20 22:14:12 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookWarriorHomepage(object):
    def setupUi(self, BookWarriorHomepage):
        BookWarriorHomepage.setObjectName("BookWarriorHomepage")
        BookWarriorHomepage.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(BookWarriorHomepage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(BookWarriorHomepage)
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
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeKingdom = QtWidgets.QTreeWidget(self.widget_4)
        self.treeKingdom.setAnimated(True)
        self.treeKingdom.setObjectName("treeKingdom")
        self.treeKingdom.headerItem().setText(0, "1")
        self.treeKingdom.header().setVisible(False)
        self.horizontalLayout_2.addWidget(self.treeKingdom)
        self.verticalLayout.addWidget(self.widget_4)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(BookWarriorHomepage)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_3)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.vignettes = QtWidgets.QWidget()
        self.vignettes.setGeometry(QtCore.QRect(0, 0, 150, 201))
        self.vignettes.setObjectName("vignettes")
        self.gridLayout = QtWidgets.QGridLayout(self.vignettes)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.vignettes)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(BookWarriorHomepage)
        QtCore.QMetaObject.connectSlotsByName(BookWarriorHomepage)

    def retranslateUi(self, BookWarriorHomepage):
        _translate = QtCore.QCoreApplication.translate
        BookWarriorHomepage.setWindowTitle(_translate("BookWarriorHomepage", "Form"))
        self.Tree_label.setText(_translate("BookWarriorHomepage", "Par Royaume"))
        self.label.setText(_translate("BookWarriorHomepage", "Heros"))

