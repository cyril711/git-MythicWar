from PyQt5.Qt import QDialog
from python_modules.config import Config
     
from python_modules.main_view.ui_dialog_thumb_generator import Ui_DialogThumbGenerator
     
class DialogThumbGenerator (QDialog, Ui_DialogThumbGenerator):
    def __init__ (self,model,parent=None):
        super(DialogThumbGenerator,self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.settings = Config().instance.settings
        self.currentFaction = None
        self.currentEmpire = None
        self.currentKingdom = None
        self.factionComboBox.currentIndexChanged['QString'].connect(self.updateFromFactionCBox)
        self.empireComboBox.currentIndexChanged['QString'].connect(self.updateFromEmpireCBox)
        self.kingdomComboBox.currentIndexChanged['QString'].connect(self.updateFromKingdomCBox)
        
        for faction_name in self.model.factions.keys() :
            self.factionComboBox.addItem(str(faction_name))

    
    def updateFromFactionCBox (self, value):
 #       self.empireComboBox.blockSignals(True)
        self.empireComboBox.clear()  
  #      self.kingdomComboBox.blockSignals(True)
        self.kingdomComboBox.clear()
        self.currentEmpire = None
        self.currentKingdom = None
        if value in self.model.factions :
            self.currentFaction = self.model.factions[value]
            print ('current Faction ', self.currentFaction)
            for empire in self.currentFaction.empires.values() :
                self.empireComboBox.addItem(str(empire.name))
        else:
            self.currentFaction = None
   #     self.empireComboBox.blockSignals(False)
   #     self.kingdomComboBox.blockSignals(False)
        
    def updateFromEmpireCBox (self, value):
    #    self.kingdomComboBox.blockSignals(True)
        self.kingdomComboBox.clear()
        self.currentKingdom = None
        if self.currentFaction != None :
            if value in self.currentFaction.empires.keys() :
                self.currentEmpire = self.currentFaction.empires[value]

                for kingdom in self.currentEmpire.kingdoms.values():
                    self.kingdomComboBox.addItem(str(kingdom.name))
            else:
                self.currenEmpire = None

     #   self.kingdomComboBox.blockSignals(False)


    def updateFromKingdomCBox (self, value):
        if self.currentEmpire != None :
            if value in self.model.currentEmpire.kingdoms:
                self.currentKingdom = self.model.currentEmpire.kingdoms[value]
        print ('sss',self.currentEmpire)