# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_modules/main_view/explorer.ui'
#
# Created: Sat Dec 20 22:14:09 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExplorerWidget(object):
    def setupUi(self, ExplorerWidget):
        ExplorerWidget.setObjectName("ExplorerWidget")
        ExplorerWidget.setWindowModality(QtCore.Qt.WindowModal)
        ExplorerWidget.resize(151, 651)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExplorerWidget.sizePolicy().hasHeightForWidth())
        ExplorerWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(ExplorerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.list_selected = QtWidgets.QListWidget(ExplorerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_selected.sizePolicy().hasHeightForWidth())
        self.list_selected.setSizePolicy(sizePolicy)
        self.list_selected.setDragEnabled(True)
        self.list_selected.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.list_selected.setObjectName("list_selected")
        self.verticalLayout.addWidget(self.list_selected)
        self.widget = QtWidgets.QWidget(ExplorerWidget)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.faction_label = QtWidgets.QLabel(self.widget)
        self.faction_label.setObjectName("faction_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.faction_label)
        self.factions = QtWidgets.QComboBox(self.widget)
        self.factions.setObjectName("factions")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.factions)
        self.empire_label = QtWidgets.QLabel(self.widget)
        self.empire_label.setObjectName("empire_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.empire_label)
        self.kinngdom_label = QtWidgets.QLabel(self.widget)
        self.kinngdom_label.setObjectName("kinngdom_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.kinngdom_label)
        self.groupe_label = QtWidgets.QLabel(self.widget)
        self.groupe_label.setObjectName("groupe_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.groupe_label)
        self.empires = QtWidgets.QComboBox(self.widget)
        self.empires.setObjectName("empires")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.empires)
        self.kingdoms = QtWidgets.QComboBox(self.widget)
        self.kingdoms.setObjectName("kingdoms")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.kingdoms)
        self.groupes = QtWidgets.QComboBox(self.widget)
        self.groupes.setObjectName("groupes")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.groupes)
        self.verticalLayout.addWidget(self.widget)
        self.list_filtered = QtWidgets.QListWidget(ExplorerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_filtered.sizePolicy().hasHeightForWidth())
        self.list_filtered.setSizePolicy(sizePolicy)
        self.list_filtered.setDragEnabled(True)
        self.list_filtered.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_filtered.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_filtered.setMovement(QtWidgets.QListView.Free)
        self.list_filtered.setResizeMode(QtWidgets.QListView.Adjust)
        self.list_filtered.setObjectName("list_filtered")
        self.verticalLayout.addWidget(self.list_filtered)

        self.retranslateUi(ExplorerWidget)
        QtCore.QMetaObject.connectSlotsByName(ExplorerWidget)

    def retranslateUi(self, ExplorerWidget):
        _translate = QtCore.QCoreApplication.translate
        ExplorerWidget.setWindowTitle(_translate("ExplorerWidget", "Form"))
        self.faction_label.setText(_translate("ExplorerWidget", "Faction"))
        self.empire_label.setText(_translate("ExplorerWidget", "Empire"))
        self.kinngdom_label.setText(_translate("ExplorerWidget", "Kingdom"))
        self.groupe_label.setText(_translate("ExplorerWidget", "Groupe"))

