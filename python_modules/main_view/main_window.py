from PyQt5.QtWidgets import QAction, QMainWindow, QWidget, QFileDialog
from PyQt5.Qt import  QKeySequence, QDate, QTime,QDialog, QProgressDialog,QIcon, QTextStream,\
    QApplication, QSizePolicy, QPushButton, QTimer, QComboBox, \
    QDateTime, QLabel, QRectF
from python_modules.main_view.explorer_view import ExplorerWidget
from python_modules.main_view.profil_view import ProfilWidget
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
from python_modules.model.groupe import Groupe
from python_modules.model.warrior import Warrior
from python_modules.model.kingdom import Kingdom
from python_modules.view.view_map.map_item import ColorMode
class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Mythic War")
        self.timer_update = QTimer()
        self.timer_update.timeout.connect(self.updateContent)
        self.timer_update.start(500)
        self.settings = Config().instance.settings
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
    
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        separator = QtWidgets.QWidget(self)
        separator.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.toolBar.addWidget(separator)
        self.toolBar.addActions([self.actionHome,self.actionQuit,self.actionSave,self.actionSettings])
        self.toolBarPreset = QtWidgets.QToolBar(self)
        self.toolBarPreset.setObjectName("toolBarPreset")
        self.toolBarPreset.addActions([self.actionAll,self.actionSelection,self.actionFilter])
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarPreset)

        # MENU MAP #
        self.actionColorizeFaction = QAction(self)
        self.actionColorizeFaction .setIcon(QIcon(":/icons/256x256/letter_F"))
        self.actionColorizeFaction.triggered.connect(self.onActionColorizeFaction)
        self.actionColorizeFaction.setCheckable(True)
        self.actionColorizeEmpire = QAction(self)
        self.actionColorizeEmpire.setIcon(QIcon(":/icons/256x256/letter_E"))
        self.actionColorizeEmpire.triggered.connect(self.onActionColorizeEmpire)
        self.actionColorizeEmpire.setCheckable(True)
        self.actionColorizeKingdom= QAction(self)
        self.actionColorizeKingdom.setIcon(QIcon(":/icons/256x256/letter_K"))
        self.actionColorizeKingdom.triggered.connect(self.onActionColorizeKingdom)
        self.actionColorizeKingdom.setCheckable(True)
        self.actionColorizeGroupe= QAction(self)
        self.actionColorizeGroupe.setIcon(QIcon(":/icons/256x256/letter_G"))
        self.actionColorizeGroupe.triggered.connect(self.onActionColorizeGroupe)
        self.actionColorizeGroupe.setCheckable(True)
        self.toolBarMap = QtWidgets.QToolBar(self)
        self.toolBarMap.setObjectName("toolBarMap")
        self.toolBarMap.addActions([self.actionColorizeFaction, self.actionColorizeEmpire, self.actionColorizeKingdom,self.actionColorizeGroupe])
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarMap)

        self.play_button = QAction(self)
        self.play_button.setIcon(QIcon(":/icons/24x24/player"))
        self.play_button.triggered.connect(self.onPlay)
        self.toolBarPlay = QtWidgets.QToolBar(self)
        self.toolBarPlay.setObjectName("toolBarPlay")
        self.toolBarPlay.addAction(self.play_button)
        self.time = QDateTime()
        if self.settings.contains("time") :
            self.time.setTime(self.settings.value["time"])
        else:
            self.time.setDate(QDate(2000,1,1))
            self.time.setTime(QTime(0,0,0))

        self.time_label = QLabel(self)

        self.time_label.setText(self.time.toString("ddd MMM hh:mm:ss"))
        self.toolBarPlay.addWidget(self.time_label)
        self.global_timer = QTimer()
        self.global_timer.timeout.connect(self.onUpdateTime)
        self.c_box_speed = QComboBox(self)
        self.c_box_speed.addItem('1x', 1)
        self.c_box_speed.addItem('2x', 2)
        self.c_box_speed.addItem('4x', 4)
        self.c_box_speed.addItem('8x', 8)
        self.c_box_speed.addItem('16x', 16)
        self.toolBarPlay.addWidget(self.c_box_speed)

        separator2 = QtWidgets.QWidget(self)
        separator2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.toolBarPlay.addWidget(separator2)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarPlay)
        self.toolBarHistory = QtWidgets.QToolBar(self)
        self.toolBarHistory.setObjectName("toolBarHistory")
        button_fight = QPushButton(self)
        button_fight.setIcon(QIcon(":/icons/16x16/validate"))
        button_fight.setText("0 combat en attente")
        self.toolBarHistory.addWidget(button_fight)
        button_in_progress = QPushButton(self)
        button_in_progress.setText("0 in progress")
        self.toolBarHistory.addWidget(button_in_progress)
        button_history= QPushButton(self)

        self.toolBarHistory.addWidget(button_history)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarHistory)
        self.msgBox = QtWidgets.QMessageBox()

        self.kingdomLayout = None
        self.bookLayout = None
        self.map = None
        self.warriorLayout = None
        self.explorerWidget = None
        self.profilWidget = None
        self.univers = None
        self.progress = QProgressDialog ()
        self.progress.setWindowModality(QtCore.Qt.WindowModal)        
        filename = None
        if os.path.exists(os.path.join(Config().instance.path_to_sqlite(),self.settings.value("global/current_database"))):
            filename = os.path.join(Config().instance.path_to_sqlite(),self.settings.value("global/current_database"))
        elif os.path.exists(os.path.join(Config().instance.path_to_sqlite(),self.settings.value("global/default_database"))):
            filename = os.path.join(Config().instance.path_to_sqlite(),self.settings.value("global/default_database"))
        if filename != None :
            print ('filename',filename)
            self.init(filename)
            self.actionQuit.triggered.connect(self.onQuit)
            self.actionSave.triggered.connect(self.onSave)
            self.actionSave.setEnabled(True)
            self.actionOpen.triggered.connect(self.onOpen)
            self.actionSave_As.triggered.connect(self.onSaveAs)
            self.actionSettings.triggered.connect(self.onEdit)
            self.actionReset_attributes.triggered.connect(self.onResetAttributes)
            self.actionAdd_Kingdom.triggered.connect(self.onAddKingdom)
            self.actionGenerate_Thumbnail.triggered.connect(self.onGenerateThumbnail)
            self.actionNew.triggered.connect(self.onNew)
            self.actionStylesheet.triggered.connect(self.onEditStyleSheet)
            self.actionHome.triggered.connect(self.onHome)
            self.actionAll.triggered.connect(self.onPresetAll)
            self.actionSelection.triggered.connect(self.onPresetFilter)
            self.actionFilter.triggered.connect(self.onPresetSelection)
        else:
            self.msgBox.setIcon( 3)
            self.msgBox.setText("Impossible de charger le model de base de donnee, l'application va se fermer");
            self.msgBox.exec_()

 

    def onEditStyleSheet(self):
        editor = StyleSheetEditor(self)
        editor.changeStyleSheet.connect(self.onChangeStylesheet)
        editor.setWindowModality(QtCore.Qt.ApplicationModal)
        editor.resize(500, 300)
        editor.show()
  
  
    def onPlay (self):
        if self.global_timer.isActive():
            self.play_button.setIcon(QIcon(":/icons/24x24/player"))
            self.global_timer.stop()
        else:
            self.play_button.setIcon(QIcon(":/icons/24x24/pause"))
            self.global_timer.start(1000)
    def onUpdateTime (self):
        deltaT = self.c_box_speed.currentData()
        new_date = self.time.addSecs(deltaT)
        self.time.setDate(new_date.date())
        self.time.setTime(new_date.time())
        self.time_label.setText(self.time.toString("ddd MMM hh:mm:ss"))
        self.univers.updateActions(deltaT)
    def onChangeStylesheet(self, css):
        self.current_css = css
    def onOpen(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open Database', directory=self.settings.value("global/current_dir"), filter='Database (*.sqlite)')
        if filename[0]!= '' :
            print ('filename',filename,type(filename))
            self.init(filename[0])
 
 
 
    def init(self,filename=None):
        if filename != None : 
            self.database = DatabaseManager(filename)
            self.database.createConnection()
            self.database_history = DatabaseManager(filename)
            self.database_history.createConnection()            

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
        self.bookModel.load(Config().instance.path_to_book()+"\\book.xml")
        



        nb_etapes= 4
        avancement = self.progress.value()
        step = avancement/nb_etapes
        self.progress.setLabelText("Etape 2/5: Interface - Kingdom Layout")
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


        self.progress.setLabelText("Etape 3/5: Interface - Warrior Layout")
        self.progress.setValue(self.progress.value()+step)
        if self.warriorLayout == None:
            self.warriorLayout = WarriorLayout(self.univers,self.warriors)
            self.w_layout.addWidget (self.warriorLayout)
        else:
            self.warriorLayout.init(self.univers)
        


        self.progress.setLabelText("Etape 4/5: Interface - Map")
        self.progress.setValue(self.progress.value()+step)
        self.map = MapWindow(self.univers)
        self.map_layout.addWidget (self.map)
        

        self.progress.setLabelText("Etape 5/5: Interface - Explorer")
        self.progress.setValue(self.progress.value()+step)
        if self.explorerWidget == None :
            self.explorerWidget = ExplorerWidget(self.univers)
        else:
            self.explorerWidget.initView(self.univers)
        self.explorerWidget.hide()
        self.explorerWidget.setWindowModality(QtCore.Qt.WindowModal)
        #self.explorerWidget.setParent(self.explorer_content)
        
        if self.profilWidget == None :
            self.profilWidget= ProfilWidget(self.univers)
        else:
            self.profilWidget.initView(self.univers)
        self.profilWidget.setParent(self.profil_content)
        #self.dockWidget.setParent(self.dockWidgetContents)
        self.tabifyDockWidget(self.profilDockWidget,self.explorerDockWidget)
        self.progress.setValue(self.progress.maximum())
        #self.connections()
        self.univers.showResultInfos()
        # connections
        self.univers.askForHerosPage.connect(self.onGoToWarriorPage)
        self.univers.askForKingdomPage.connect(self.onGoToKingdomPage)
        self.univers.askForKingdomHomePage.connect(self.onGoToKingdomPage)
        self.univers.askForGroup.connect(self.onGoToKingdomPage)
        self.univers.askForMap.connect(self.onGoToMap)
        self.univers.askForProfil.connect(self.onUpdateProfil)
        self.univers.selection_updated.connect(self.explorerWidget.updateSelectionList)
        self.univers.selection_updated.connect(self.profilWidget.updateSelectionList) 
        self.univers.askForKingdomReload.connect(self.onKingdomReload)
        self.univers.saveEnabled.connect(self.onSaveEnabled)



        self.current_css = ""
        if self.settings.value("mainView/stylesheet")!= "":
            file = QtCore.QFile(os.path.join(Config().instance.path_to_qss(),self.settings.value("mainView/stylesheet")))
            if file.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text):
                text = QTextStream(file)
                QApplication.instance().setStyleSheet(text.readAll())
                QApplication.setStyle(self.settings.value("mainView/style"))       
                self.current_css = self.settings.value("mainView/stylesheet")
        
        self.tabWidget.setCurrentIndex(2)
        self.actionAll.setChecked(True)
        self.actionColorizeEmpire.setChecked(True)
        self.onPresetAll()
        self.tabWidget.setCurrentIndex(int(self.settings.value("mainView/ind_current_tab")))

    def onSaveEnabled(self,enable):
        self.actionSave.setEnabled(enable)
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
        
    def onKingdomReload (self, kingdom_name):
        #self.kingdomLayout.init(self.univers)
        self.kingdomLayout.loadKingdom(kingdom_name)
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
        
    def onGoToKingdomPage(self):
        self.tabWidget.setCurrentIndex(1)

    def onUpdateProfil (self,warrior):
        self.profilWidget.update(warrior)

    def onGoToMap (self):
        self.tabWidget.setCurrentIndex(0)
        


    def onQuit (self):
        self.close()


    def onActionColorizeFaction (self):
        self.actionColorizeEmpire.setChecked(False)
        self.actionColorizeKingdom.setChecked(False)
        self.actionColorizeGroupe.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget.objectName() == "map":
            self.map.changeColorMode(ColorMode.Faction)
            self.map.update(QtCore.QRect(0,0,999999999,99999999))
            
    def onActionColorizeEmpire (self):
        self.actionColorizeFaction.setChecked(False)
        self.actionColorizeKingdom.setChecked(False)
        self.actionColorizeGroupe.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget.objectName() == "map":
            self.map.changeColorMode(ColorMode.Empire)
            self.map.update(QtCore.QRect(0,0,999999999,99999999))
    def onActionColorizeKingdom(self):
        self.actionColorizeFaction.setChecked(False)
        self.actionColorizeEmpire.setChecked(False)
        self.actionColorizeGroupe.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget.objectName() == "map":
            self.map.changeColorMode(ColorMode.Kingdom)
            self.map.update(QtCore.QRect(0,0,999999999,99999999))
    def onActionColorizeGroupe(self):
        self.actionColorizeFaction.setChecked(False)
        self.actionColorizeKingdom.setChecked(False)
        self.actionColorizeEmpire.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget.objectName() == "map":
            self.map.changeColorMode(ColorMode.Groupe)
            self.map.update(QtCore.QRect(0,0,999999999,99999999))
            
    def onPresetAll(self):
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        self.actionFilter.setChecked(False)
        self.actionSelection.setChecked(False)
        if widget == self.warriors :
            self.warriorLayout.onPresetAll()
    def onPresetSelection(self):
        self.actionFilter.setChecked(False)
        self.actionAll.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget == self.warriors :
            self.warriorLayout.onPresetSelection()
    def onPresetFilter(self):
        self.actionAll.setChecked(False)
        self.actionSelection.setChecked(False)
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget == self.warriors :
            self.warriorLayout.onPresetFilter()
    
    def onEdit (self):
        current_index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(current_index)
        if widget == self.book :
            self.bookLayout.onEdit()
        elif widget == self.warriors:
            self.warriorLayout.onEdit()
#         dlg = Dialogds (self)    
#         if dlg.exec_() == QDialog.Accepted :
#             dlg.applyChanges ()
#         else :
#             dlg.close()


    def updateContent(self):
        widget = self.tabWidget.currentWidget()
        if widget == self.kingdoms :
            self.kingdomLayout.updateContent()
    def onHome (self):
        #current_index = self.tabWidget.currentIndex()
        #widget = self.tabWidget.widget(current_index)
        widget = self.tabWidget.currentWidget()
        if widget == self.warriors :
            self.warriorLayout.onHome()
            self.warriorLayout.setFocus()
            if self.actionAll.isChecked() :
                self.onPresetAll()
            elif self.actionFilter.isChecked():
                self.onPresetFilter()
            else:
                self.onPresetSelection()
        elif widget == self.kingdoms :
            self.kingdomLayout.onHome()
            self.kingdomLayout.setFocus()
    
    def onSaveAs (self):
        filename = QFileDialog.getSaveFileName(self, caption='Save Database', directory=self.settings.value("global/current_dir"), filter='Database (*.sqlite)')
        if filename :
            self.univers.save(filename[0])
    
    def onSave (self):
        #sauvegarde
        print('sauvegarde')
        dlg = DialogSave (self.univers,self)
        print ('len',len(self.univers.modifications ))
        for item in self.univers.modifications :
            print ('typr',type(item[0]))
            if type(item[0]) == Warrior:
                dlg.addHeros (item[0].name)
            if type(item[0]) == Kingdom:
                dlg.addRoyaume( item[0].name)        
            if type(item[0]) == Groupe:
                dlg.addGroupe (item[0].name,item[1])
            
            
        self.univers.modifications.clear()
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
        #self.settings.setValue ("mainView/style",QApplication.style())
        self.settings.setValue("mainView/ind_currrent_tab",self.tabWidget.currentIndex())

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
    
    def keyPressEvent(self,event):
        if event.key()== QtCore.Qt.Key_F :
            if event.modifiers() == QtCore.Qt.ControlModifier :
                if self.explorerWidget.isHidden():
                    self.explorerWidget.show()
                else:
                    self.explorerWidget.hide()
            else:
                if self.menubar.isHidden():
                    self.menubar.show()
                else:
                    self.menubar.hide()
            
    def onEditFilters (self):
        self.filterView = FilterView(self.univers,self)
        self.filterView.open()
        pass
