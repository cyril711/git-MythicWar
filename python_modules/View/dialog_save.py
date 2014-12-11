from PyQt5.Qt import QDialog, QListWidgetItem
from PyQt5 import QtCore
     
from python_modules.View.ui_dialog_save import Ui_DialogSave
     
class DialogSave (QDialog, Ui_DialogSave):
    def __init__ (self,model,parent=None):
        super(DialogSave,self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    def init (self):
        pass
    
    
    def addHeros (self,heros_id):
        self.model.database.setVerbose(True)
        warrior_sqlite = self.model.database.select("*", "gm_perso",False,"IDPerso=="+str(heros_id))
        while (warrior_sqlite.next()):
            text = str(warrior_sqlite.value("IDPerso"))+"->"+ str(warrior_sqlite.value("Name"))
            item = QListWidgetItem(text)
            item.setCheckState(QtCore.Qt.Checked)
            self.list_modified_heros.addItem(item)
    
    def addRoyaume (self,royaume_id):
        self.model.database.setVerbose(True)
        kingdom_sqlite = self.model.database.select("*", "gm_kingdom",False,"IDKingdom=="+str(royaume_id))
        while (kingdom_sqlite.next()):
            text = str(kingdom_sqlite.value("IDKingdom"))+"->"+ str(kingdom_sqlite.value("Name"))
            item = QListWidgetItem(text)
            item.setCheckState(QtCore.Qt.Checked)
            self.list_modified_kingdom.addItem(item)
    
    def addGroupe (self,groupe_id):
        self.model.database.setVerbose(True)
        groupe_sqlite = self.model.database.select("*", "gm_groupes",False,"IDGroupe=="+str(groupe_id))
        while (groupe_sqlite.next()):
            text = str(groupe_sqlite.value("IDGroupe"))+"->"+ str(groupe_sqlite.value("Name"))
            item = QListWidgetItem(text)
            item.setCheckState(QtCore.Qt.Checked)
            self.list_modified_groupe.addItem(item)