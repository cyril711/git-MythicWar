from PyQt5.QtWidgets import QAction, QMainWindow, QWidget
from PyQt5.Qt import  QKeySequence,QDialog
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
class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self, univers):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #self.setFixedSize(QSize(1200,1080))
        self.univers = univers
        self.settings = Config().instance.settings
        self.modified_royaumes =[]
        self.modified_groupes = []
        self.modified_heros = []
        #self.centralwidget.setStyleSheet("#centralwidget{background-image: url(:/textures/saphir)}")
        #self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
        #self.stackedWidget = QStackedWidget(self)
        #self.setCentralWidget(self.stackedWidget)
        #self.centralwidget.setWindowOpacity(0.5) 
        self.kingdomLayout = KingdomLayout(self.univers,self.kingdoms)
        self.setStyleSheet("background-color: rgb(22, 249, 200);")
#         self.tabWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
#         self.tabWidget.setWindowOpacity(0.5)
# 
#         
#         self.kingdoms.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
#         self.tabWidget.setWindowOpacity(0.5)
        self.k_layout.addWidget(self.kingdomLayout)

        self.warriorLayout = WarriorLayout(self.univers,self.warriors)
        self.w_layout.addWidget (self.warriorLayout)
        
        
        self.map = MapWindow(self.univers)
        self.map_layout.addWidget (self.map)

        
        self.explorerWidget = ExplorerWidget(self.univers)
        #self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.profilDock)        
        self.explorerWidget.setParent(self.explorer_content)
#         self.explorer_content = self.explorerWidget
        self.univers.askForHerosPage.connect(self.onGoToWarriorPage)
        self.warriorLayout.modified.connect(self.onModificationsHeros)
        self.kingdomLayout.modifiedGroupe.connect(self.onModificationsGroupes)
        self.kingdomLayout.modifiedKingdom.connect(self.onModificationsRoyaumes)
        self.actionQuit.triggered.connect(self.onQuit)
        self.actionLock.toggled.connect(self.onLock)
        self.actionSave.triggered.connect(self.onSave)
        self.actionSettings.triggered.connect(self.onEditSettings)
        self.actionReset_attributes.triggered.connect(self.onResetAttributes)
        #self.actionAdd_Kingdom.triggered.connect(self.onAddKingdom)
        self.actionGenerate_Thumbnail.triggered.connect(self.onGenerateThumbnail)
        #self.explorerDock = ExplorerDockWidget(self.univers)
        #self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.explorerDock)
        #self.showFullScreen()
            
        #self.univers.selection_changed.connect (self.profilWidget.onSelectionChange)
        #self.mapView = MapView (self.stackedWidget)
       
        self.setWindowTitle("Mythic War")


    def onGenerateThumbnail(self):
        dlg = DialogThumbGenerator(self.univers,self)
        if dlg.exec_() == QDialog.Accepted :
           # try : 
            faction = dlg.currentFaction.name
            empire = dlg.currentEmpire.name
            kingdom = dlg.currentKingdom.name
#             except AttributeError : 
#                 faction = empire = kingdom = ''
            print ('Thumb generator faction',faction)
            tg = ThumbnailGenerator(self.settings.value("global/resources_path"))
            tg.generateFor1Kingdom(faction,empire,kingdom)
        else :
            dlg.close()
        
            

    def onResetAttributes (self):
        pass
    
    def onAddKingdom (self):
        pass
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
