from PyQt5.QtWidgets import QAction, QMainWindow, QWidget
from PyQt5.Qt import  QKeySequence,QDialog, QProgressDialog
from python_modules.main_view.explorer_view import ExplorerWidget
from python_modules.view.view_map.map_view import MapWindow
from python_modules.view.view_kingdom.kingdom_layout import KingdomLayout
from python_modules.main_view.ui_main_window import Ui_MainWindow
from python_modules.view.view_heros.warrior_layout import WarriorLayout
from python_modules.config import Config
from python_modules.main_view.dialog_save import DialogSave
from python_modules.main_view.dialog_settings import DialogSettings
from python_modules.main_view.dialog_thumb_generator import DialogThumbGenerator
from python_modules.utils.thumbnail_generator import ThumbnailGenerator
from python_modules.main_view.dialog_kingdom_import import DialogKingdomImport
from python_modules.utils.export_to_sqlite import ExportToSqlite
from python_modules.model.univers import Univers
import os
from PyQt5 import QtWidgets, QtCore
class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Mythic War")
        self.settings = Config().instance.settings
        self.msgBox = QtWidgets.QMessageBox()

        self.progress = QProgressDialog ()
        self.progress.setWindowModality(QtCore.Qt.WindowModal)        
        filename = None
        if os.path.exists(self.settings.value("global/current_database")):
            filename = self.settings.value("global/current_database")
        elif os.path.exists(self.settings.value("global/default_database")):
            filename = self.settings.value("global/default_database")
        if filename != None :
            print ('filename',filename)
            self.init(filename)
        else:
            self.msgBox.setIcon( 3)
            self.msgBox.setText("Impossible de charger le model de base de donnee, l'application va se fermer");
            self.msgBox.exec_()
            #information 
  
 
    def init(self,filename):
        self.univers = Univers(filename,self.progress)
        self.modified_royaumes =[]
        self.modified_groupes = []
        self.modified_heros = []

        nb_etapes= 4
        avancement = self.progress.value()
        step = avancement/nb_etapes
        self.progress.setLabelText("Etape 2/2 : Interface - Kingdom Layout")
        self.kingdomLayout = KingdomLayout(self.univers,self.kingdoms)
        self.setStyleSheet("background-color: rgb(22, 249, 200);")
        self.k_layout.addWidget(self.kingdomLayout)        
        self.progress.setValue(self.progress.value()+step)

        self.progress.setLabelText("Etape 2/2 : Interface - Warrior Layout")
        self.warriorLayout = WarriorLayout(self.univers,self.warriors)
        self.w_layout.addWidget (self.warriorLayout)
        self.progress.setValue(self.progress.value()+step)

        self.progress.setLabelText("Etape 2/2 : Interface - Map")
        self.map = MapWindow(self.univers)
        self.map_layout.addWidget (self.map)
        self.progress.setValue(self.progress.value()+step)        

        self.progress.setLabelText("Etape 2/2 : Interface - Explorer")
        self.explorerWidget = ExplorerWidget(self.univers)        
        self.explorerWidget.setParent(self.explorer_content)
        self.progress.setValue(self.progress.value()+step)
        self.connections()
        self.univers.showResultInfos()

       
    def connections(self):
        self.univers.askForHerosPage.connect(self.onGoToWarriorPage)
        self.warriorLayout.modified.connect(self.onModificationsHeros)
        self.kingdomLayout.modifiedGroupe.connect(self.onModificationsGroupes)
        self.kingdomLayout.modifiedKingdom.connect(self.onModificationsRoyaumes)
        self.actionQuit.triggered.connect(self.onQuit)
        self.actionLock.toggled.connect(self.onLock)
        self.actionSave.triggered.connect(self.onSave)
        self.actionSettings.triggered.connect(self.onEditSettings)
        self.actionReset_attributes.triggered.connect(self.onResetAttributes)
        self.actionAdd_Kingdom.triggered.connect(self.onAddKingdom)
        self.actionGenerate_Thumbnail.triggered.connect(self.onGenerateThumbnail)

    def onGenerateThumbnail(self):
        dlg = DialogThumbGenerator(self.univers,self)
        if dlg.exec_() == QDialog.Accepted :
            faction = dlg.currentFaction.name
            empire = dlg.currentEmpire.name
            kingdom = dlg.currentKingdom.name
            print ('Thumb generator faction',faction)
            tg = ThumbnailGenerator(self.settings.value("global/resources_path"))
            tg.process(faction,empire,kingdom)
        else :
            dlg.close()
        
            

    def onResetAttributes (self):
        pass
    
    def onAddKingdom (self):
        dlg = DialogKingdomImport(self.univers,self)
        if dlg.exec_() == QDialog.Accepted :
            faction = dlg.factioName()
            empire = dlg.empireName()
            kingdom = dlg.kingdomName()
            dlg.validate()
            
            tg = ExportToSqlite(self.settings.value("global/resources_path"))
            tg.setDefaultValues(dlg.defaults_values)
            tg.process(faction,empire,kingdom)
        else :
            dlg.close()
        


    def onGoToWarriorPage (self):
        self.tabWidget.setCurrentIndex(2)
    def onModificationsHeros (self,id_heros):
        self.modified_heros.append(id_heros)
        if not self.actionSave.isEnabled():
            self.actionSave.setEnabled(True)
    
    def onModificationsGroupes (self,id_groupe):
        self.modified_groupes.append(id_groupe)
        if not self.actionSave.isEnabled():
            self.actionSave.setEnabled(True)
            
    def onModificationsRoyaumes (self,id_royaume):
        self.modified_royaumes.append(id_royaume)
        if not self.actionSave.isEnabled():
            self.actionSave.setEnabled(True)
            
    def onLock(self,locked):
        self.warriorLayout.setEnableEditableItems(locked)
        self.kingdomLayout.setEnableEditableItems(locked)

    def onQuit (self):
        self.close()
    
    
    def onEditSettings (self):
        dlg = DialogSettings (self)    
        if dlg.exec_() == QDialog.Accepted :
            dlg.applyChanges ()
        else :
            dlg.close()
    def onSave (self):
        #sauvegarde
        dlg = DialogSave (self.univers,self)
        for heros in self.modified_heros :
            dlg.addHeros (heros)
        for kingdom_id in self.modified_royaumes:
            dlg.addRoyaume( kingdom_id)        
        for groupe_id in self.modified_groupes :
            dlg.addGroupe (groupe_id)
            
            
        self.modified_heros.clear()
        self.modified_royaumes.clear()
        self.modified_groupes.clear()
        if dlg.exec_() == QDialog.Accepted :
            self.univers.save()
#             for id_heros in dlg.list_modified_heros.selectedItems():
#                 self.univers.saveHeros(id_heros)

        dlg.close()
    def closeEvent(self,event):
        print ('closevent')
        self.settings.setValue ("explorer/faction",self.explorerWidget.factions.currentText())
        self.settings.setValue ("explorer/empire",self.explorerWidget.empires.currentText())
        self.settings.setValue ("explorer/kingdom",self.explorerWidget.kingdoms.currentText())
        self.settings.setValue ("explorer/groupe",self.explorerWidget.groupes.currentText())
        

    def createActions(self):
        self.editFilters = QAction(QIcon(':/images/new.png'), "&EditFilters",
                self, shortcut=QKeySequence('F'),
                statusTip="Create a new form letter", triggered=self.onEditFilters) 
        self.showProfil = QAction(QIcon(':/images/new.png'), "&ShowProfil",
                self, shortcut=QKeySequence('P'),
                statusTip="Show Profil View", triggered=self.onShowProfil) 
        
    def onShowProfil (self):
        self.profilView.open()
        pass
    
    def onEditFilters (self):
        self.filterView = FilterView(self.univers,self)
        self.filterView.open()
        pass
