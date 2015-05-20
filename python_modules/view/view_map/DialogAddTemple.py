from PyQt5.Qt import QDialog, QListWidgetItem
from PyQt5 import QtCore
     
from python_modules.view.view_map.ui_dialog_add_temple import Ui_DialogAddTemple
     
class Etage (QWidget):
    def __init__(self,parent):
        super(Etage,self).__init__(parent)
        name = QTextEdit()
        layout.addWidget(name)
        layout.addWidget(texture_path)
        tool = QToolButton()
        layout.addWidget(tool)
class DialogAddTemple (QDialog, Ui_DialogAddTemple):
    def __init__ (self,model,parent=None):
        super(DialogAddTemple,self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.etages_widgets_list = []
        self.connections ()

   def connections (self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.factionComboBox.currentIndexChanged['QString'].connect(self.updateFromFactionCBox)
        self.empireComboBox.currentIndexChanged['QString'].connect(self.updateFromEmpireCBox)
        self.kingdomComboBox.currentIndexChanged['QString'].connect(self.updateFromKingdomCBox)
        self.addButton.clicked.connect(self.onAddRow)
        self.removeButton.clicked.connect(self.onRemoveRow)
    def init (self):
        self.factionComboBox.clear()
        self.factionComboBox.addItem('*')
        if self.model != None : 
            for faction_name in self.model.factions.keys() :
                self.factionComboBox.addItem(str(faction_name))
        self.empireComboBox.clear()
        self.empireComboBox.addItem('*')
        self.kingdomComboBox.clear()
        self.kingdomComboBox.addItem('*')

   def onAddRow (self):
       w = Etage(self.EtagesWidget)
       layout = QHBoxLayout ()
       w.setLayout(layout)
       
       self.etages_widgets_list.append(w)
   def updateFromFactionCBox (self, value):
        self.empireComboBox.blockSignals(True)
        self.empireComboBox.clear()
        self.empireComboBox.addItem('*')
        self.kingdomComboBox.blockSignals(True)
        self.kingdomComboBox.clear()
        self.kingdomComboBox.addItem('*')

        if value in self.model.factions :
            for empire in self.model.factions[value].empires.values() :
                self.empireComboBox.addItem(str(empire.name))
        self.empireComboBox.blockSignals(False)
        self.kingdomComboBox.blockSignals(False)

    def updateFromEmpireCBox (self, value):

        self.kingdoms.blockSignals(True)
        self.kingdoms.clear()
        self.kingdoms.addItem('*') 
        if value in self.model.factions[factionComboBox.currentText()].empires.keys() :
            for kingdom in self.model.factions[factionComboBox.currentText()].empires[value].kingdoms.values():
                self.kingdomComboBox.addItem(str(kingdom.name))
        self.kingdoms.blockSignals(False)