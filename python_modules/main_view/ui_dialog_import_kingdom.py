# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/main_view/dialog_import_kingdom.ui'
#
# Created: Thu Sep 10 22:05:25 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogKingdomImport(object):
    def setupUi(self, DialogKingdomImport):
        DialogKingdomImport.setObjectName("DialogKingdomImport")
        DialogKingdomImport.resize(504, 611)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DialogKingdomImport)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(DialogKingdomImport)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButtonFaction = QtWidgets.QToolButton(self.widget_2)
        self.toolButtonFaction.setObjectName("toolButtonFaction")
        self.gridLayout.addWidget(self.toolButtonFaction, 0, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 2, 0, 1, 1)
        self.lineEditFaction = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditFaction.setObjectName("lineEditFaction")
        self.gridLayout.addWidget(self.lineEditFaction, 0, 3, 1, 1)
        self.toolButtonEmpire = QtWidgets.QToolButton(self.widget_2)
        self.toolButtonEmpire.setObjectName("toolButtonEmpire")
        self.gridLayout.addWidget(self.toolButtonEmpire, 1, 4, 1, 1)
        self.lineEditEmpire = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditEmpire.setObjectName("lineEditEmpire")
        self.gridLayout.addWidget(self.lineEditEmpire, 1, 3, 1, 1)
        self.lineEditKingdom = QtWidgets.QLineEdit(self.widget_2)
        self.lineEditKingdom.setObjectName("lineEditKingdom")
        self.gridLayout.addWidget(self.lineEditKingdom, 2, 3, 1, 1)
        self.toolButtonKingdom = QtWidgets.QToolButton(self.widget_2)
        self.toolButtonKingdom.setObjectName("toolButtonKingdom")
        self.gridLayout.addWidget(self.toolButtonKingdom, 2, 4, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setObjectName("label_18")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.groupe_description = QtWidgets.QLineEdit(self.groupBox_3)
        self.groupe_description.setObjectName("groupe_description")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.groupe_description)
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setObjectName("label_19")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.groupe_rank = QtWidgets.QSpinBox(self.groupBox_3)
        self.groupe_rank.setObjectName("groupe_rank")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.groupe_rank)
        self.label_20 = QtWidgets.QLabel(self.groupBox_3)
        self.label_20.setObjectName("label_20")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.groupe_color = QtWidgets.QComboBox(self.groupBox_3)
        self.groupe_color.setObjectName("groupe_color")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.groupe_color)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.widget_6 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_6.setObjectName("widget_6")
        self.formLayout_3 = QtWidgets.QFormLayout(self.widget_6)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_14 = QtWidgets.QLabel(self.widget_6)
        self.label_14.setObjectName("label_14")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.kingdom_armee = QtWidgets.QLineEdit(self.widget_6)
        self.kingdom_armee.setObjectName("kingdom_armee")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.kingdom_armee)
        self.kingdom_couleur = QtWidgets.QPushButton(self.widget_6)
        self.kingdom_couleur.setObjectName("kingdom_couleur")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.kingdom_couleur)
        self.kingdom_description = QtWidgets.QLineEdit(self.widget_6)
        self.kingdom_description.setObjectName("kingdom_description")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.kingdom_description)
        self.label_16 = QtWidgets.QLabel(self.widget_6)
        self.label_16.setObjectName("label_16")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.verticalLayout_3.addWidget(self.widget_6)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.groupBox)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.heros_latitude = QtWidgets.QDoubleSpinBox(self.widget_3)
        self.heros_latitude.setObjectName("heros_latitude")
        self.horizontalLayout_3.addWidget(self.heros_latitude)
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.heros_longitude = QtWidgets.QDoubleSpinBox(self.widget_3)
        self.heros_longitude.setObjectName("heros_longitude")
        self.horizontalLayout_3.addWidget(self.heros_longitude)
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.heros_place = QtWidgets.QSpinBox(self.widget_3)
        self.heros_place.setMinimum(-1)
        self.heros_place.setObjectName("heros_place")
        self.horizontalLayout_3.addWidget(self.heros_place)
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.heros_level = QtWidgets.QSpinBox(self.widget_3)
        self.heros_level.setMinimum(-1)
        self.heros_level.setObjectName("heros_level")
        self.horizontalLayout_3.addWidget(self.heros_level)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.formLayout = QtWidgets.QFormLayout(self.widget_4)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.heros_description = QtWidgets.QLineEdit(self.widget_4)
        self.heros_description.setObjectName("heros_description")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.heros_description)
        self.label_8 = QtWidgets.QLabel(self.widget_4)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(self.widget_4)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.heros_techniques = QtWidgets.QLineEdit(self.widget_4)
        self.heros_techniques.setObjectName("heros_techniques")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.heros_techniques)
        self.heros_historique = QtWidgets.QLineEdit(self.widget_4)
        self.heros_historique.setObjectName("heros_historique")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.heros_historique)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.groupBox)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.widget_5)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.heros_leader = QtWidgets.QCheckBox(self.widget_5)
        self.heros_leader.setText("")
        self.heros_leader.setObjectName("heros_leader")
        self.horizontalLayout_5.addWidget(self.heros_leader)
        self.label_10 = QtWidgets.QLabel(self.widget_5)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.heros_rank = QtWidgets.QSpinBox(self.widget_5)
        self.heros_rank.setObjectName("heros_rank")
        self.horizontalLayout_5.addWidget(self.heros_rank)
        self.label_11 = QtWidgets.QLabel(self.widget_5)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.heros_status = QtWidgets.QComboBox(self.widget_5)
        self.heros_status.setObjectName("heros_status")
        self.horizontalLayout_5.addWidget(self.heros_status)
        self.verticalLayout_2.addWidget(self.widget_5)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogKingdomImport)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogKingdomImport)
        self.buttonBox.accepted.connect(DialogKingdomImport.accept)
        self.buttonBox.rejected.connect(DialogKingdomImport.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogKingdomImport)

    def retranslateUi(self, DialogKingdomImport):
        _translate = QtCore.QCoreApplication.translate
        DialogKingdomImport.setWindowTitle(_translate("DialogKingdomImport", "Dialog"))
        self.toolButtonFaction.setText(_translate("DialogKingdomImport", "..."))
        self.label.setText(_translate("DialogKingdomImport", "Faction"))
        self.label_12.setText(_translate("DialogKingdomImport", "Empire"))
        self.label_13.setText(_translate("DialogKingdomImport", "Kingdom"))
        self.toolButtonEmpire.setText(_translate("DialogKingdomImport", "..."))
        self.toolButtonKingdom.setText(_translate("DialogKingdomImport", "..."))
        self.groupBox_3.setTitle(_translate("DialogKingdomImport", "Paramètres par defaut Groupes"))
        self.label_18.setText(_translate("DialogKingdomImport", "Description"))
        self.label_19.setText(_translate("DialogKingdomImport", "Rank"))
        self.label_20.setText(_translate("DialogKingdomImport", "Color"))
        self.groupBox_2.setTitle(_translate("DialogKingdomImport", "Paramètres par defaut Kingdom"))
        self.label_17.setText(_translate("DialogKingdomImport", "TextLabel"))
        self.label_14.setText(_translate("DialogKingdomImport", "Armee"))
        self.kingdom_couleur.setText(_translate("DialogKingdomImport", "Color Kingdom"))
        self.label_16.setText(_translate("DialogKingdomImport", "Description"))
        self.groupBox.setTitle(_translate("DialogKingdomImport", "Parametres par default Heros : "))
        self.label_2.setText(_translate("DialogKingdomImport", "Lat :"))
        self.label_3.setText(_translate("DialogKingdomImport", "Lon :"))
        self.label_5.setText(_translate("DialogKingdomImport", "Place"))
        self.label_6.setText(_translate("DialogKingdomImport", "Level"))
        self.label_4.setText(_translate("DialogKingdomImport", "Description"))
        self.label_8.setText(_translate("DialogKingdomImport", "Techniques"))
        self.label_9.setText(_translate("DialogKingdomImport", "Historique"))
        self.label_7.setText(_translate("DialogKingdomImport", "Leader"))
        self.label_10.setText(_translate("DialogKingdomImport", "Rank"))
        self.label_11.setText(_translate("DialogKingdomImport", "Status"))

