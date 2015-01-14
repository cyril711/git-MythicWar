
from PyQt5 import QtCore
     
from python_modules.view.view_kingdom.ui_kingdom_layout import Ui_KingdomLayout
from python_modules.view.view_kingdom.book_world_homepage import BookWorldHomepage
from python_modules.view.view_kingdom.book_world_main_page import BookWorldMainPage
from python_modules.view.view_kingdom.book_world_army import BookWorldArmy     
from PyQt5.Qt import QWidget

class KingdomLayout ( QWidget):
    modifiedGroupe = QtCore.pyqtSignal(int)
    modifiedKingdom = QtCore.pyqtSignal(int)
    def __init__ (self,model,parent=None):
        super(KingdomLayout,self).__init__(parent)
        self.ui = Ui_KingdomLayout()
        self.ui.setupUi(self)
        self.model = model
        self.kingdom_homepage = None
        self.connections()
        self.init(model)
        self.nb_pages = 0

    def connections (self):
        self.ui.next_button.clicked.connect(self.goNextKingdom)
        self.ui.previous_button.clicked.connect(self.goPreviousKingdom)
    
    def init (self,model):
        self.model = model
        #chapitre World - kingdoms
        if self.kingdom_homepage != None :
            self.ui.stackedWidget.removeWidget(self.kingdom_homepage)
            self.kingdom_homepage.setParent(None)
            self.removeAllKingdomWidgets()
        self.kingdom_widget = []
        faction = []
        for value in self.model.factions.values() :
            faction.append(value)
        self.kingdom_homepage = BookWorldHomepage (self,self.ui.stackedWidget)
        if len(faction)!= 0:
            if len(faction)==1:
                print ('taille faction empires',len(faction[0].empires))
                self.kingdom_homepage.setLeftPage(faction[0].name, faction[0].name, faction[0].empires, faction[0].empires)
            else:
                self.kingdom_homepage.setLeftPage(faction[0].name, faction[1].name, faction[0].empires, faction[1].empires)
                
        self.ui.stackedWidget.removeWidget(self.ui.page)
        self.ui.stackedWidget.removeWidget(self.ui.page_2)
        self.ui.stackedWidget.addWidget(self.kingdom_homepage)
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.count())
        
    def setEnableEditableItems (self, enable):
        # a faire  rrrrrr
        for i in range (self.ui.stackedWidget.count()):
            widget = self.ui.stackedWidget.widget(i)
            try :
                widget.setEnableEditableItems(enable)
            except AttributeError :
                pass
        
    def removeAllKingdomWidgets (self): 
        print ('remove all widget')
        for widget in self.kingdom_widget :
            widget.setParent(None)
            self.ui.stackedWidget.removeWidget(widget)
        self.kingdom_widget.clear()
        for widget in self.kingdom_homepage.list_buttons :
            widget.setParent (None)
    
    def addKingdomWidget (self, kingdom):
        self.kingdom_homepage.addButton (kingdom.name, self.ui.stackedWidget.count())
        kingdom_widget = BookWorldMainPage (self.model,self.ui.stackedWidget)
        kingdom_widget.setContent (kingdom)
        self.kingdom_widget.append(kingdom_widget)
        self.ui.stackedWidget.addWidget(kingdom_widget)
        self.nb_pages =  1      
        for groupe in kingdom.groupes.values() :
            if len(groupe.sub_groupes)==0 : 
                if self.nb_pages == 1 : 
                    kingdom_widget.setContentRightPage(groupe)

                else:
                    if (self.nb_pages%2)==0 : 
                        kingdom_widget = BookWorldArmy (self.model,self.ui.stackedWidget)
                        kingdom_widget.setLeftContent (groupe)
                        self.kingdom_widget.append(kingdom_widget)
                        self.ui.stackedWidget.addWidget(kingdom_widget)

                    else:
                        kingdom_widget.setRightContent(groupe)
                self.nb_pages+=1
                for warrior in groupe.warriorsList().values():
                    kingdom_widget.addVignette(warrior)                
            else: 
                for sg in groupe.sub_groupes:
                    if self.nb_pages == 1 : 
                        kingdom_widget.setContentRightPage(groupe,sg)
                    else:
                        if (self.nb_pages%2)==0 : 
                            kingdom_widget = BookWorldArmy (self.model,self.ui.stackedWidget)
                            kingdom_widget.setLeftContent (groupe,sg)
                            self.kingdom_widget.append(kingdom_widget)
                            self.ui.stackedWidget.addWidget(kingdom_widget)
                        else:
                            kingdom_widget.setRightContent(groupe,sg)
                    self.nb_pages+=1
                    for warrior in sg.warriorsList().values():
                        kingdom_widget.addVignette(warrior)

#             for sg in groupe.sub_groupes :
#                 kingdom_widget.addGroupe(sg)
#                 for warrior in sg.warriorsList().values():
#                     kingdom_widget.addVignette(warrior)
        self.ui.next_button.setEnabled(True)                            

    def goNextKingdom (self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
        if self.ui.stackedWidget.currentIndex() == (self.ui.stackedWidget.count()-1):
            self.ui.next_button.setEnabled(False)

        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.previous_button.setEnabled(False)
        else :
            self.ui.previous_button.setEnabled (True)

    def goPreviousKingdom (self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()-1)
        if self.ui.stackedWidget.currentIndex() == (self.ui.stackedWidget.count()-1):
            self.ui.next_button.setEnabled(False)
        else :
            self.ui.next_button.setEnabled(True)
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.previous_button.setEnabled(False)


    def changeKingdomPage (self ):
        id_widget = self.sender().objectName()
        self.ui.stackedWidget.setCurrentIndex(int(id_widget))
    