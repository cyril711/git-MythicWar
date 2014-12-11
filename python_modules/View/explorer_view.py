from PyQt5.Qt import QGraphicsView, QTreeWidgetItem, QComboBox, QTreeWidget,\
    qDebug, QDockWidget, QFile, QWidget, QTableWidgetItem, QIcon, QBrush, QColor,\
    QListWidgetItem

from python_modules.View.ui_explorer_widget import Ui_ExplorerWidget
from python_modules.config import Config
from PyQt5 import QtCore
from test.test_importlib.import_.test___package__ import Setting__package__

class ExplorerWidget (QWidget,Ui_ExplorerWidget):
    def __init__(self,model,parent=None):
        super(ExplorerWidget,self).__init__(parent)
        self.setupUi(self)
        self.model = model
      #  self.tableWidget.setUpdatesEnabled(True)    
        self.settings = Config().instance.settings
        self.connections()
        self.initView(model)        

    def initView (self,model):
        self.factions.addItem('*')
        for faction_name in model.factions.keys() :
            self.factions.addItem(str(faction_name))
        self.empires.clear()
        self.empires.addItem('*')
        self.kingdoms.clear()
        self.kingdoms.addItem('*')
        self.groupes.clear()
        self.groupes.addItem('*')
        setting_faction = self.settings.value("explorer/faction")
        if setting_faction!= "*":
            self.factions.setCurrentText(setting_faction)
        setting_empire = self.settings.value("explorer/empire")
        if setting_empire!= "*":
             self.empires.setCurrentText(setting_empire)
        setting_kingdom = self.settings.value("explorer/kingdom")
        if setting_kingdom!= "*":
             self.kingdoms.setCurrentText(setting_kingdom)
        setting_groupe = self.settings.value("explorer/groupe")        
        if setting_groupe!= "*":
             self.groupes.setCurrentText(setting_groupe)

    def connections (self):
        self.factions.currentIndexChanged['QString'].connect(self.updateFromFactionCBox)
        self.empires.currentIndexChanged['QString'].connect(self.updateFromEmpireCBox)
        self.kingdoms.currentIndexChanged['QString'].connect(self.updateFromKingdomCBox)
        self.groupes.currentIndexChanged['QString'].connect(self.updateFromGroupeCBox)
        #self.tableWidget.itemSelectionChanged.connect(self.changeSelection)
        self.list_filtered.itemSelectionChanged.connect(self.changeSelection)
        self.model.selection_updated.connect(self.updateSelectionList)
    def changeSelection (self):
#         warriors_ID = []
        for i in range (self.list_filtered.count()):
            item = self.list_filtered.item(i)
            item.data(5).setSelected(item.isSelected())
        
#             warrior.setSelection()
#         for item in self.list_filtered.selectedItems():
#             #warriors_ID.append(item.data(5))
#             item.data(5).setSelected(True)
#             self.model.setSelection(warriors_ID)
            
    def updateSelectionList (self):
        self.list_selected.clear()
        for item in self.model.selectedWarriors():
            item = QListWidgetItem (str(item.name))
            self.list_selected.addItem(item)

    def updateFromFactionCBox (self, value):
        self.model.setCurrentFaction(None)
        self.empires.blockSignals(True)
        self.empires.clear()
        self.empires.addItem('*')
        self.model.setCurrentEmpire(None)        
        self.kingdoms.blockSignals(True)
        self.kingdoms.clear()
        self.kingdoms.addItem('*')
        self.model.setCurrentKingdom(None)
        self.groupes.blockSignals(True)
        self.groupes.clear()
        self.groupes.addItem('*')
        self.model.setCurrentGroupe(None)
        if value in self.model.factions :
            self.model.setCurrentFaction(self.model.factions[value])
            for empire in self.model.currentFaction.empires.values() :
                self.empires.addItem(str(empire.name))
        self.model.updateFilteredWarrior()        
        self.updateWarriorList ()
        self.empires.blockSignals(False)
        self.kingdoms.blockSignals(False)
        self.groupes.blockSignals(False)
    def updateFromEmpireCBox (self, value):

        self.kingdoms.blockSignals(True)
        self.kingdoms.clear()
        self.kingdoms.addItem('*')
        self.groupes.blockSignals(True)
        self.groupes.clear()
        self.groupes.addItem('*')

        self.model.setCurrentKingdom(None)
        self.model.setCurrentGroupe(None)
        if self.model.currentFaction != None : 
            if value in self.model.currentFaction.empires.keys() :
                self.model.setCurrentEmpire(self.model.currentFaction.empires[value])
                for kingdom in self.model.currentEmpire.kingdoms.values():
                    self.kingdoms.addItem(str(kingdom.name))
            else:
                self.model.setCurrentEmpire(None)
        self.model.updateFilteredWarrior()
        self.updateWarriorList ()
        self.kingdoms.blockSignals(False)
        self.groupes.blockSignals(False)

    def updateFromKingdomCBox (self, value):

        self.model.setCurrentKingdom(None)
        self.groupes.blockSignals(True)
        self.groupes.clear()
        self.groupes.addItem('*')
        self.model.setCurrentGroupe(None)
        if self.model.currentEmpire != None :
            if value in self.model.currentEmpire.kingdoms :
                self.model.setCurrentKingdom(self.model.currentEmpire.kingdoms[value])
                for groupes in self.model.currentKingdom.groupes.values():
                    self.groupes.addItem(str(groupes.name))
            else:
                self.model.setCurrentKingdom(None)
        self.groupes.blockSignals(False)
        self.model.updateFilteredWarrior()
        self.updateWarriorList ()
    def updateFromGroupeCBox (self, value):

        self.model.setCurrentGroupe(None)
        if self.model.currentKingdom!= None :
            if value in self.model.currentKingdom.groupes:
                self.model.setCurrentGroupe(self.model.currentKingdom.groupes[value])
            else:
                self.model.setCurrentGroupe(None)
        self.model.updateFilteredWarrior()
        self.updateWarriorList ()

    def updateWarriorList (self):
        row = 0
        self.item = []
        #self.tableWidget.clear()
        self.list_filtered.clear()
        for warrior in self.model.filteredWarriors() :
            item = QListWidgetItem (str(warrior.name))
            item.setData(5,warrior)
            self.list_filtered.addItem(item)
            if warrior.selected == True:
                item.setSelected(True)
                    
           # item.setCheckState(False)
#             self.tableWidget.insertRow(row)
#             item = QTableWidgetItem(str(warrior.name))
#             item.setData(1,warrior.id)
#             self.tableWidget.setItem(row,0,item)
#             item = QTableWidgetItem()
#             item.setBackground(QBrush(QColor(0,0,255)) )
#             item.setToolTip(warrior.parent.parent.name)
#             icon = QIcon("C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/icons\png/16x16/sagittarius2.png")
#             item.setIcon(icon)
#             self.tableWidget.setItem(row,1,item)
#             item = QTableWidgetItem(str(warrior.id))
#             self.tableWidget.setItem(row,8,item)
#             row = row + 1
        #self.tableWidget.viewport().update()
        #self.tableWidget.repaint()