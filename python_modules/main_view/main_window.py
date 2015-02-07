from PyQt5.QtWidgets import QAction, QMainWindow, QWidget, QFileDialog
from PyQt5.Qt import  QKeySequence,QDialog, QProgressDialog, QTextStream,\
    QApplication
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
from python_modules.model.book import Book
import os
from PyQt5 import QtWidgets, QtCore
from python_modules.utils.database import DatabaseManager
from python_modules.view.view_book.book_layout import BookLayout
from python_modules.tools.stylesheet.stylesheeteditor import StyleSheetEditor
class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Mythic War")
        self.settings = Config().instance.settings
        self.msgBox = QtWidgets.QMessageBox()

        self.kingdomLayout = None
        self.bookLayout = None
        self.map = None
        self.warriorLayout = None
        self.explorerWidget = None
        self.univers = None
        self.progress = QProgressDialog ()
        self.progress.setWindowModality(QtCore.Qt.WindowModal)        
        filename = None
        if os.path.exists(os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/current_database"))):
            filename = os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/current_database"))
        elif os.path.exists(os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/default_database"))):
            filename = os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/default_database"))
        if filename != None :
            print ('filename',filename)
            self.init(filename)
            self.actionQuit.triggered.connect(self.onQuit)
            self.actionLock.toggled.connect(self.onLock)
            self.actionSave.triggered.connect(self.onSave)
            self.actionOpen.triggered.connect(self.onOpen)
            self.actionSave_As.triggered.connect(self.onSaveAs)
            self.actionSettings.triggered.connect(self.onEdit)
            self.actionReset_attributes.triggered.connect(self.onResetAttributes)
            self.actionAdd_Kingdom.triggered.connect(self.onAddKingdom)
            self.actionGenerate_Thumbnail.triggered.connect(self.onGenerateThumbnail)
            self.actionNew.triggered.connect(self.onNew)
            self.actionStylesheet.triggered.connect(self.onEditStyleSheet)
            self.actionHome.triggered.connect(self.onHome)
        else:
            self.msgBox.setIcon( 3)
            self.msgBox.setText("Impossible de charger le model de base de donnee, l'application va se fermer");
            self.msgBox.exec_()

# 
#     def onApplyStylesheet(self,filename,style):
#         #filename = QFileDialog.getOpenFileName(self, caption='Choisissez un stylsheet', directory=self.settings.value("global/resources_qss"), filter='')
#         if filename != None :
#             file = QtCore.QFile(os.path.join(self.settings.value("global/resources_qss"),filename))
#             if file.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text):
#                 text = QTextStream(file)
#                 QApplication.instance().setStyleSheet(text.readAll())
#                 QApplication.setStyle(style)
#                 self.settings.setValue ("mainView/stylesheet",filename)
#                 self.settings.setValue ("mainView/style",style)
                

    def onEditStyleSheet(self):
        editor = StyleSheetEditor(self)
        editor.changeStyleSheet.connect(self.onChangeStylesheet)
        editor.setWindowModality(QtCore.Qt.ApplicationModal)
        editor.resize(500, 300)
        editor.show()
  
  
    def onChangeStylesheet(self, css):
        self.current_css = css
    def onOpen(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open Database', directory=self.settings.value("global/current_dir"), filter='Database (*.sqlite)')
        if filename :
            print ('filename',filename,type(filename))
            self.init(filename[0])
 
 
 
    def init(self,filename=None):
        print ('INITITITITITITITI')
        if filename != None : 
            self.database = DatabaseManager(filename)
            self.database.createConnection()

#         if self.kingdomLayout != None :
#             self.kingdomLayout.disconnect()
#             self.kingdomLayout.setParent(None)
        if self.map != None :
            self.map.disconnect()
            self.map.setParent(None)
#         if self.warriorLayout != None :
#             self.warriorLayout.disconnect()
#             self.warriorLayout.setParent(None)
        if self.univers != None :

            self.univers.disconnect()
            self.univers = Univers(self.database,self.progress)
        else:
            self.univers = Univers(self.database,self.progress)

#         if self.explorerWidget != None :
#             self.explorerWidget.disconnect()
#             self.explorerWidget.setParent(None)

        self.bookModel = Book()
        self.bookModel.load("C:\\Users\\cyril\\Documents\\Travail\\Workspace\\databases\\book\\book.xml")
        

        self.modified_royaumes =[]
        self.modified_groupes = []
        self.modified_heros = []

        nb_etapes= 4
        avancement = self.progress.value()
        step = avancement/nb_etapes
        self.progress.setLabelText("Etape 2/2 : Interface - Kingdom Layout")
        if self.kingdomLayout == None:
            self.kingdomLayout = KingdomLayout(self.univers,self.kingdoms)
            self.k_layout.addWidget (self.kingdomLayout )        
        else:
            self.kingdomLayout.init(self.univers)
        if self.bookLayout == None:
            self.bookLayout = BookLayout(self.book)
            self.bookLayout.load(self.bookModel)
            self.b_layout.addWidget (self.bookLayout )        
        else:
            self.bookLayout.load(self.bookModel)

        #self.setStyleSheet("background-color: rgb(22, 249, 200);")
        #self.k_layout.addWidget(self.kingdomLayout)        
        self.progress.setValue(self.progress.value()+step)

        self.progress.setLabelText("Etape 2/2 : Interface - Warrior Layout")
        if self.warriorLayout == None:
            self.warriorLayout = WarriorLayout(self.univers,self.warriors)
            self.w_layout.addWidget (self.warriorLayout)
            self.warriorLayout.modified.connect(self.onModificationsHeros)
        else:
            self.warriorLayout.init(self.univers)

        self.progress.setValue(self.progress.value()+step)

        self.progress.setLabelText("Etape 2/2 : Interface - Map")
        self.map = MapWindow(self.univers)
        self.map_layout.addWidget (self.map)
        self.progress.setValue(self.progress.value()+step)        

        self.progress.setLabelText("Etape 2/2 : Interface - Explorer")
        if self.explorerWidget == None :
            self.explorerWidget = ExplorerWidget(self.univers)
        else:
            self.explorerWidget.initView(self.univers)        
        self.explorerWidget.setParent(self.explorer_content)
        self.progress.setValue(self.progress.value()+step)
        #self.connections()
        self.univers.showResultInfos()
        # connections
        self.univers.askForHerosPage.connect(self.onGoToWarriorPage)
        self.univers.selection_updated.connect(self.explorerWidget.updateSelectionList) 
        self.kingdomLayout.modifiedGroupe.connect(self.onModificationsGroupes)
        self.kingdomLayout.modifiedKingdom.connect(self.onModificationsRoyaumes)


        self.current_css = ""
        if self.settings.value("mainView/stylesheet")!= "":
            file = QtCore.QFile(os.path.join(self.settings.value("global/resources_qss"),self.settings.value("mainView/stylesheet")))
            if file.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text):
                text = QTextStream(file)
                QApplication.instance().setStyleSheet(text.readAll())
                QApplication.setStyle(self.settings.value("mainView/style"))       
                self.current_css = self.settings.value("mainView/stylesheet")


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
        
    def onNew (self):
        filename = os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/default_database"))
        if not os.path.exists(filename):
            filename = None

        if filename != None :
            #self.explorerWidget.setParent(None)
            self.univers.clear()
            self.explorerWidget.initView(self.univers)
            self.database.database.close()
            self.init(filename)
            self.univers.database = self.database
        else:
            self.msgBox.setIcon( 3)
            self.msgBox.setText("Impossible de creer un nouveau projet car "+filename+" n a put etre trouve");
            self.msgBox.exec_()
        

    def onResetAttributes (self):
        pass
    
    def onAddKingdom (self):
        dlg = DialogKingdomImport(self.univers,self)
        if dlg.exec_() == QDialog.Accepted :
            faction = dlg.factionName()
            empire = dlg.empireName()
            kingdom = dlg.kingdomName()
            dlg.validate()
            
            ex = ExportToSqlite(self.settings.value("global/resources_path"),self.database)
            ex.setDefaultValues(dlg.defaults_values)
            ex.process(faction,empire,kingdom)

            self.init()
            #self.univers.loadFromFile()
            #self.explorerWidget.initView(self.univers)
        

        else :
            dlg.close()
            print ("close add kingdom")        


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
    
    
    def onEdit (self):
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget == self.book :
            self.bookLayout.onEdit()
#         dlg = Dialogds (self)    
#         if dlg.exec_() == QDialog.Accepted :
#             dlg.applyChanges ()
#         else :
#             dlg.close()

    def onHome (self):
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget == self.warriors :
            self.warriorLayout.onHome()

    
    def onSaveAs (self):
        filename = QFileDialog.getSaveFileName(self, caption='Save Database', directory=self.settings.value("global/current_dir"), filter='Database (*.sqlite)')
        if filename :
            self.univers.save(filename)
    
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
            self.bookModel.save()
#             for id_heros in dlg.list_modified_heros.selectedItems():
#                 self.univers.saveHeros(id_heros)

        dlg.close()
    def closeEvent(self,event):
        print ('closevent')
        self.settings.setValue ("explorer/faction",self.explorerWidget.factions.currentText())
        self.settings.setValue ("explorer/empire",self.explorerWidget.empires.currentText())
        self.settings.setValue ("explorer/kingdom",self.explorerWidget.kingdoms.currentText())
        self.settings.setValue ("explorer/groupe",self.explorerWidget.groupes.currentText())
        self.settings.setValue ("mainView/stylesheet",self.current_css)
        self.settings.setValue ("mainView/style",QApplication.style())

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
