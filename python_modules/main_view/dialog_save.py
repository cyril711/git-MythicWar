from PyQt5.Qt import QDialog, QListWidgetItem, QTableWidgetItem, QBrush
from PyQt5 import QtCore
     
from python_modules.main_view.ui_dialog_save import Ui_DialogSave
     
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
    
    def addGroupe (self,groupe_name,type_alert):
        item_name =QTableWidgetItem(groupe_name)
        item_type =QTableWidgetItem(type_alert)
        if item_type == "delete":
            item_name.setBackground(QBrush("red"))
            item_type.setBackground(QBrush("red"))
        elif item_type == "new":
            item_name.setBackground(QBrush("green"))
            item_type.setBackground(QBrush("green"))    
        self.list_modified_groupes.insertRow(0)
        self.list_modified_groupes.setItem(0,0,item_name)
        self.list_modified_groupes.setItem(0,1,item_type)