# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_kingdom/book_world_main_page.ui'
#
# Created: Wed Jan 14 21:14:50 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookWorldMainpage(object):
    def setupUi(self, BookWorldMainpage):
        BookWorldMainpage.setObjectName("BookWorldMainpage")
        BookWorldMainpage.resize(566, 407)
        self.horizontalLayout = QtWidgets.QHBoxLayout(BookWorldMainpage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(BookWorldMainpage)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Title = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Old English Text MT")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title)
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_content2 = QtWidgets.QWidget(self.widget_4)
        self.widget_content2.setObjectName("widget_content2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_content2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_7 = QtWidgets.QWidget(self.widget_content2)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.widget_7)
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.button_color = QtWidgets.QPushButton(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_color.sizePolicy().hasHeightForWidth())
        self.button_color.setSizePolicy(sizePolicy)
        self.button_color.setAutoFillBackground(True)
        self.button_color.setText("")
        self.button_color.setObjectName("button_color")
        self.horizontalLayout_6.addWidget(self.button_color)
        self.verticalLayout_3.addWidget(self.widget_7)
        self.descriptionTextEdit = QtWidgets.QPlainTextEdit(self.widget_content2)
        self.descriptionTextEdit.setEnabled(True)
        self.descriptionTextEdit.setBackgroundVisible(False)
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.verticalLayout_3.addWidget(self.descriptionTextEdit)
        self.horizontalLayout_2.addWidget(self.widget_content2)
        self.horizontalLayout_2.setStretch(0, 4)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_content = QtWidgets.QWidget(self.widget_3)
        self.widget_content.setObjectName("widget_content")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_content)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget_content)
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.historyTextEdit = QtWidgets.QPlainTextEdit(self.widget_content)
        self.historyTextEdit.setEnabled(True)
        self.historyTextEdit.setBackgroundVisible(False)
        self.historyTextEdit.setObjectName("historyTextEdit")
        self.verticalLayout_4.addWidget(self.historyTextEdit)
        self.horizontalLayout_3.addWidget(self.widget_content)
        self.horizontalLayout_3.setStretch(0, 4)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_5 = QtWidgets.QWidget(self.widget)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.army_picture = QtWidgets.QLabel(self.widget_5)
        self.army_picture.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.army_picture.setFrameShadow(QtWidgets.QFrame.Raised)
        self.army_picture.setObjectName("army_picture")
        self.horizontalLayout_4.addWidget(self.army_picture)
        self.land_picture = QtWidgets.QLabel(self.widget_5)
        self.land_picture.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.land_picture.setFrameShadow(QtWidgets.QFrame.Raised)
        self.land_picture.setObjectName("land_picture")
        self.horizontalLayout_4.addWidget(self.land_picture)
        self.verticalLayout.addWidget(self.widget_5)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 10)
        self.horizontalLayout.addWidget(self.widget)
        self.right_page = QtWidgets.QWidget(BookWorldMainpage)
        self.right_page.setObjectName("right_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.right_page)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_6 = QtWidgets.QWidget(self.right_page)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupe_name = QtWidgets.QLabel(self.widget_6)
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(18)
        self.groupe_name.setFont(font)
        self.groupe_name.setObjectName("groupe_name")
        self.horizontalLayout_5.addWidget(self.groupe_name)
        self.comboBoxColor = QtWidgets.QComboBox(self.widget_6)
        self.comboBoxColor.setObjectName("comboBoxColor")
        self.horizontalLayout_5.addWidget(self.comboBoxColor)
        self.verticalLayout_2.addWidget(self.widget_6)
        self.description_groupe = QtWidgets.QPlainTextEdit(self.right_page)
        self.description_groupe.setEnabled(True)
        self.description_groupe.setBackgroundVisible(False)
        self.description_groupe.setObjectName("description_groupe")
        self.verticalLayout_2.addWidget(self.description_groupe)
        self.scrollArea = QtWidgets.QScrollArea(self.right_page)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.vignettes = QtWidgets.QWidget()
        self.vignettes.setGeometry(QtCore.QRect(0, 0, 251, 241))
        self.vignettes.setObjectName("vignettes")
        self.gridLayout = QtWidgets.QGridLayout(self.vignettes)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.vignettes)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 20)
        self.horizontalLayout.addWidget(self.right_page)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(BookWorldMainpage)
        QtCore.QMetaObject.connectSlotsByName(BookWorldMainpage)

    def retranslateUi(self, BookWorldMainpage):
        _translate = QtCore.QCoreApplication.translate
        BookWorldMainpage.setWindowTitle(_translate("BookWorldMainpage", "Form"))
        self.Title.setText(_translate("BookWorldMainpage", "TextLabel"))
        self.label.setText(_translate("BookWorldMainpage", "Description"))
        self.label_2.setText(_translate("BookWorldMainpage", "Histoire"))
        self.army_picture.setText(_translate("BookWorldMainpage", "TextLabel"))
        self.land_picture.setText(_translate("BookWorldMainpage", "TextLabel"))
        self.groupe_name.setText(_translate("BookWorldMainpage", "TextLabel"))

