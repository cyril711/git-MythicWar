# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/view/view_heros/book_warrior_page_reverse.ui'
#
# Created: Wed Oct 21 21:03:18 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookWarriorPageReverse(object):
    def setupUi(self, BookWarriorPageReverse):
        BookWarriorPageReverse.setObjectName("BookWarriorPageReverse")
        BookWarriorPageReverse.resize(963, 835)
        BookWarriorPageReverse.setStyleSheet("")
        self.formLayout_2 = QtWidgets.QFormLayout(BookWarriorPageReverse)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.widget = QtWidgets.QWidget(BookWarriorPageReverse)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.picture_widget = QtWidgets.QWidget(self.widget_2)
        self.picture_widget.setMinimumSize(QtCore.QSize(333, 500))
        self.picture_widget.setObjectName("picture_widget")
        self.picture_layout_2 = QtWidgets.QVBoxLayout(self.picture_widget)
        self.picture_layout_2.setContentsMargins(0, 0, 0, 0)
        self.picture_layout_2.setObjectName("picture_layout_2")
        self.verticalLayout_2.addWidget(self.picture_widget)
        self.infos_widget = QtWidgets.QWidget(self.widget_2)
        self.infos_widget.setObjectName("infos_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.infos_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_5 = QtWidgets.QWidget(self.infos_widget)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.belong_widget = QtWidgets.QWidget(self.widget_5)
        self.belong_widget.setObjectName("belong_widget")
        self.belong_layout = QtWidgets.QHBoxLayout(self.belong_widget)
        self.belong_layout.setSpacing(0)
        self.belong_layout.setContentsMargins(-1, 0, -1, -1)
        self.belong_layout.setObjectName("belong_layout")
        self.iconFaction = QtWidgets.QPushButton(self.belong_widget)
        self.iconFaction.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/flags/blue_flag"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iconFaction.setIcon(icon)
        self.iconFaction.setIconSize(QtCore.QSize(32, 32))
        self.iconFaction.setFlat(True)
        self.iconFaction.setObjectName("iconFaction")
        self.belong_layout.addWidget(self.iconFaction)
        self.iconEmpire = QtWidgets.QPushButton(self.belong_widget)
        self.iconEmpire.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/empireIcon/greek_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iconEmpire.setIcon(icon1)
        self.iconEmpire.setIconSize(QtCore.QSize(32, 32))
        self.iconEmpire.setFlat(True)
        self.iconEmpire.setObjectName("iconEmpire")
        self.belong_layout.addWidget(self.iconEmpire)
        self.iconKingdom = QtWidgets.QPushButton(self.belong_widget)
        self.iconKingdom.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/32x32/fiche_royaume"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iconKingdom.setIcon(icon2)
        self.iconKingdom.setIconSize(QtCore.QSize(32, 32))
        self.iconKingdom.setFlat(True)
        self.iconKingdom.setObjectName("iconKingdom")
        self.belong_layout.addWidget(self.iconKingdom)
        self.profil_completion_button = QtWidgets.QPushButton(self.belong_widget)
        self.profil_completion_button.setText("")
        self.profil_completion_button.setIconSize(QtCore.QSize(32, 32))
        self.profil_completion_button.setObjectName("profil_completion_button")
        self.belong_layout.addWidget(self.profil_completion_button)
        self.verticalLayout_3.addWidget(self.belong_widget)
        self.groupe_texture_button = QtWidgets.QPushButton(self.widget_5)
        self.groupe_texture_button.setMinimumSize(QtCore.QSize(0, 30))
        self.groupe_texture_button.setText("")
        self.groupe_texture_button.setObjectName("groupe_texture_button")
        self.verticalLayout_3.addWidget(self.groupe_texture_button)
        self.widget_7 = QtWidgets.QWidget(self.widget_5)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self.widget_7)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.progressBar_HP = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_HP.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"")
        self.progressBar_HP.setProperty("value", 24)
        self.progressBar_HP.setTextVisible(True)
        self.progressBar_HP.setInvertedAppearance(False)
        self.progressBar_HP.setObjectName("progressBar_HP")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.progressBar_HP)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.progressBar_MP = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_MP.setProperty("value", 24)
        self.progressBar_MP.setObjectName("progressBar_MP")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.progressBar_MP)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.verticalLayout_3.addWidget(self.widget_7)
        self.jauges_widget = QtWidgets.QWidget(self.widget_5)
        self.jauges_widget.setObjectName("jauges_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.jauges_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.jauges_widget)
        self.horizontalLayout_4.addWidget(self.widget_5)
        self.widget_8 = QtWidgets.QWidget(self.infos_widget)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.rank_widget = QtWidgets.QWidget(self.widget_8)
        self.rank_widget.setObjectName("rank_widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.rank_widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.star_1 = QtWidgets.QPushButton(self.rank_widget)
        self.star_1.setText("")
        self.star_1.setObjectName("star_1")
        self.horizontalLayout_6.addWidget(self.star_1)
        self.star_2 = QtWidgets.QPushButton(self.rank_widget)
        self.star_2.setText("")
        self.star_2.setObjectName("star_2")
        self.horizontalLayout_6.addWidget(self.star_2)
        self.star_3 = QtWidgets.QPushButton(self.rank_widget)
        self.star_3.setText("")
        self.star_3.setObjectName("star_3")
        self.horizontalLayout_6.addWidget(self.star_3)
        self.star_4 = QtWidgets.QPushButton(self.rank_widget)
        self.star_4.setText("")
        self.star_4.setObjectName("star_4")
        self.horizontalLayout_6.addWidget(self.star_4)
        self.star_5 = QtWidgets.QPushButton(self.rank_widget)
        self.star_5.setText("")
        self.star_5.setAutoDefault(False)
        self.star_5.setDefault(False)
        self.star_5.setFlat(True)
        self.star_5.setObjectName("star_5")
        self.horizontalLayout_6.addWidget(self.star_5)
        self.rank_text = QtWidgets.QLabel(self.rank_widget)
        self.rank_text.setObjectName("rank_text")
        self.horizontalLayout_6.addWidget(self.rank_text)
        self.verticalLayout_6.addWidget(self.rank_widget)
        self.widget_6 = QtWidgets.QWidget(self.widget_8)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.map_button = QtWidgets.QPushButton(self.widget_6)
        self.map_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/128x128/target"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.map_button.setIcon(icon3)
        self.map_button.setIconSize(QtCore.QSize(64, 64))
        self.map_button.setFlat(True)
        self.map_button.setObjectName("map_button")
        self.horizontalLayout_5.addWidget(self.map_button)
        self.iconState = QtWidgets.QLabel(self.widget_6)
        self.iconState.setObjectName("iconState")
        self.horizontalLayout_5.addWidget(self.iconState)
        self.verticalLayout_6.addWidget(self.widget_6)
        self.horizontalLayout_4.addWidget(self.widget_8)
        self.informations_widget = QtWidgets.QWidget(self.infos_widget)
        self.informations_widget.setObjectName("informations_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.informations_widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.informations_widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_4.setObjectName("widget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.widget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_10 = QtWidgets.QLabel(self.widget_4)
        self.label_10.setObjectName("label_10")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget_4)
        self.spinBox_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_2.setAccelerated(True)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_11 = QtWidgets.QLabel(self.widget_4)
        self.label_11.setObjectName("label_11")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.label_13 = QtWidgets.QLabel(self.widget_4)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtWidgets.QLabel(self.widget_4)
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.spinBox_3 = QtWidgets.QSpinBox(self.widget_4)
        self.spinBox_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_3.setAccelerated(True)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_3)
        self.spinBox_5 = QtWidgets.QSpinBox(self.widget_4)
        self.spinBox_5.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_5.setAccelerated(True)
        self.spinBox_5.setObjectName("spinBox_5")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_5)
        self.spinBox_6 = QtWidgets.QSpinBox(self.widget_4)
        self.spinBox_6.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_6.setAccelerated(True)
        self.spinBox_6.setObjectName("spinBox_6")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox_6)
        self.horizontalLayout.addWidget(self.widget_4)
        self.widget_9 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout.addWidget(self.widget_9)
        self.widget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_3.setObjectName("widget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.widget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.widget_3)
        self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox.setAccelerated(True)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_9 = QtWidgets.QLabel(self.widget_3)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_12 = QtWidgets.QLabel(self.widget_3)
        self.label_12.setObjectName("label_12")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_15 = QtWidgets.QLabel(self.widget_3)
        self.label_15.setObjectName("label_15")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.label_16 = QtWidgets.QLabel(self.widget_3)
        self.label_16.setObjectName("label_16")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.spinBox_4 = QtWidgets.QSpinBox(self.widget_3)
        self.spinBox_4.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_4.setAccelerated(True)
        self.spinBox_4.setObjectName("spinBox_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_4)
        self.spinBox_7 = QtWidgets.QSpinBox(self.widget_3)
        self.spinBox_7.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_7.setAccelerated(True)
        self.spinBox_7.setProperty("showGroupSeparator", False)
        self.spinBox_7.setObjectName("spinBox_7")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_7)
        self.spinBox_8 = QtWidgets.QSpinBox(self.widget_3)
        self.spinBox_8.setFrame(False)
        self.spinBox_8.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_8.setAccelerated(True)
        self.spinBox_8.setObjectName("spinBox_8")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox_8)
        self.horizontalLayout.addWidget(self.widget_3)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_4.addWidget(self.informations_widget)
        self.verticalLayout_2.addWidget(self.infos_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widget)
        self.right_page = QtWidgets.QWidget(BookWarriorPageReverse)
        self.right_page.setObjectName("right_page")
        self.right_page_layout = QtWidgets.QVBoxLayout(self.right_page)
        self.right_page_layout.setContentsMargins(0, 0, 0, 0)
        self.right_page_layout.setObjectName("right_page_layout")
        self.warrior_name = QtWidgets.QLabel(self.right_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warrior_name.sizePolicy().hasHeightForWidth())
        self.warrior_name.setSizePolicy(sizePolicy)
        self.warrior_name.setMinimumSize(QtCore.QSize(0, 10))
        font = QtGui.QFont()
        font.setFamily("Nyala")
        font.setPointSize(24)
        self.warrior_name.setFont(font)
        self.warrior_name.setFrameShape(QtWidgets.QFrame.Panel)
        self.warrior_name.setFrameShadow(QtWidgets.QFrame.Raised)
        self.warrior_name.setAlignment(QtCore.Qt.AlignCenter)
        self.warrior_name.setObjectName("warrior_name")
        self.right_page_layout.addWidget(self.warrior_name)
        self.label_5 = QtWidgets.QLabel(self.right_page)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setObjectName("label_5")
        self.right_page_layout.addWidget(self.label_5)
        self.listWidget = QtWidgets.QListWidget(self.right_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 100))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listWidget.setObjectName("listWidget")
        self.right_page_layout.addWidget(self.listWidget)
        self.label_6 = QtWidgets.QLabel(self.right_page)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName("label_6")
        self.right_page_layout.addWidget(self.label_6)
        self.scrollArea = QtWidgets.QScrollArea(self.right_page)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.gallery = QtWidgets.QWidget()
        self.gallery.setGeometry(QtCore.QRect(0, 0, 144, 602))
        self.gallery.setObjectName("gallery")
        self.gridLayout = QtWidgets.QGridLayout(self.gallery)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.gallery)
        self.right_page_layout.addWidget(self.scrollArea)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.right_page)

        self.retranslateUi(BookWarriorPageReverse)
        QtCore.QMetaObject.connectSlotsByName(BookWarriorPageReverse)

    def retranslateUi(self, BookWarriorPageReverse):
        _translate = QtCore.QCoreApplication.translate
        BookWarriorPageReverse.setWindowTitle(_translate("BookWarriorPageReverse", "Form"))
        self.groupBox.setTitle(_translate("BookWarriorPageReverse", "State"))
        self.label.setText(_translate("BookWarriorPageReverse", "Santé"))
        self.label_2.setText(_translate("BookWarriorPageReverse", "Vitalité"))
        self.label_3.setText(_translate("BookWarriorPageReverse", "TextLabel"))
        self.rank_text.setText(_translate("BookWarriorPageReverse", "TextLabel"))
        self.iconState.setText(_translate("BookWarriorPageReverse", "TextLabel"))
        self.groupBox_2.setTitle(_translate("BookWarriorPageReverse", "Attributes"))
        self.label_10.setText(_translate("BookWarriorPageReverse", "ATK"))
        self.label_11.setText(_translate("BookWarriorPageReverse", "HP"))
        self.label_13.setText(_translate("BookWarriorPageReverse", "MATK"))
        self.label_14.setText(_translate("BookWarriorPageReverse", "AGL"))
        self.label_9.setText(_translate("BookWarriorPageReverse", "DEF"))
        self.label_12.setText(_translate("BookWarriorPageReverse", "END"))
        self.label_15.setText(_translate("BookWarriorPageReverse", "MDEF"))
        self.label_16.setText(_translate("BookWarriorPageReverse", "LUCK"))
        self.warrior_name.setText(_translate("BookWarriorPageReverse", "TextLabel"))
        self.label_5.setText(_translate("BookWarriorPageReverse", "Historique"))
        self.label_6.setText(_translate("BookWarriorPageReverse", "Gallerie"))

import resources_rc
