
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
        self.empire_selected_name = None

    def updateContent(self):
        widget = self.ui.stackedWidget.currentWidget()
        widget.updateContent()

    def connections (self):
        self.ui.next_button.clicked.connect(self.goNextPage)
        self.ui.previous_button.clicked.connect(self.goPreviousPage)
        self.model.askForKingdomPage.connect(self.goToKingdom)
        self.model.askForKingdomHomePage.connect(self.goToEmpire)
        self.model.askForGroup.connect(self.goToGroupe)
    def init (self,model):
        self.model = model
        #chapitre World - kingdoms
        if self.kingdom_homepage != None :
            self.ui.stackedWidget.removeWidget(self.kingdom_homepage)
            self.kingdom_homepage.setParent(None)
            self.removeAllKingdomWidgets()
        self.kingdom_widgets_list = []
        faction = []
        for value in self.model.factions.values() :
            faction.append(value)
        self.kingdom_homepage = BookWorldHomepage (self,self.ui.stackedWidget)
        if len(faction)!= 0:
            if len(faction)==1:
                print ('taille faction empires',len(faction[0].empires))
                self.kingdom_homepage.setLeftPage("", faction[0].name, {}, faction[0].empires)
            else:
                self.kingdom_homepage.setLeftPage(faction[0].name, faction[1].name, faction[0].empires, faction[1].empires)
                
        self.ui.stackedWidget.removeWidget(self.ui.page)
        self.ui.stackedWidget.removeWidget(self.ui.page_2)
        self.ui.stackedWidget.addWidget(self.kingdom_homepage)
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.count())
    
    def onHome(self):
        if self.empire_selected_name!= None : 
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)
    def setEnableEditableItems (self, enable):
        # a faire  rrrrrr
        for i in range (self.ui.stackedWidget.count()):
            widget = self.ui.stackedWidget.widget(i)
            try :
                widget.setEnableEditableItems(enable)
            except AttributeError :
                pass
        
    def resetEmpireSelection (self): 
        self.removeKingdomWidgets()
        for widget in self.kingdom_homepage.list_buttons :
            widget.setParent (None)

    def removeKingdomWidgets (self): 
        print ('remove all widget')
        for widget in self.kingdom_widgets_list :
            widget.setParent(None)
            self.ui.stackedWidget.removeWidget(widget)
        self.kingdom_widgets_list.clear()
                   
    def loadKingdom(self,kingdom_name):
        self.removeKingdomWidgets()
        #on est dans le cas ou la methode est appellee depuis le click sur un boutton kingdom
        if (type(kingdom_name)==bool):
            kingdom_name = self.sender().objectName()
        # dans la cas depuis un chargement depuis l exterieur de la page

        print ('load Kingdom empire name',self.empire_selected_name)
        empire = self.model.getEmpireFromName(self.empire_selected_name)
        if empire == None :
            return
        kingdom = empire.getKingdomFromName(kingdom_name)
        kingdom_widget = BookWorldMainPage (self.model,self.ui.stackedWidget)
        kingdom_widget.setContent (kingdom)
        self.kingdom_widgets_list.append(kingdom_widget)
        self.ui.stackedWidget.addWidget(kingdom_widget)
        first_page_ind = self.ui.stackedWidget.count()-1
        self.nb_pages =  0      
        for groupe in kingdom.groupes.values() :
            if len(groupe.sub_groupes)==0 : 
                if (self.nb_pages%2)==0 : 
                    kingdom_widget = BookWorldArmy (self.model,self.ui.stackedWidget)
                    kingdom_widget.setLeftContent (groupe)
                    self.kingdom_widgets_list.append(kingdom_widget)
                    self.ui.stackedWidget.addWidget(kingdom_widget)

                else:
                    kingdom_widget.setRightContent(groupe)
                self.nb_pages+=1
                for warrior in groupe.warriorsList().values():
                    kingdom_widget.addVignette(warrior)                
            else: 
                for sg in groupe.sub_groupes:
                    if self.nb_pages == 1 : 
                        kingdom_widget.setRightContent(groupe,sg)
                    else:
                        if (self.nb_pages%2)==0 : 
                            kingdom_widget = BookWorldArmy (self.model,self.ui.stackedWidget)
                            kingdom_widget.setLeftContent (groupe,sg)
                            self.kingdom_widgets_list.append(kingdom_widget)
                            self.ui.stackedWidget.addWidget(kingdom_widget)
                        else:
                            kingdom_widget.setRightContent(groupe,sg)
                    self.nb_pages+=1
                    for warrior in sg.warriorsList().values():
                        kingdom_widget.addVignette(warrior)
        #ajout de la page pour les temples
        if self.nb_pages%2 == 0:
            kingdom_widget = BookWorldArmy (self.model,self.ui.stackedWidget)
            kingdom_widget.setTemple (True)
            self.kingdom_widgets_list.append(kingdom_widget)
            self.ui.stackedWidget.addWidget(kingdom_widget)
        else:
            kingdom_widget.setTemple (kingdom.attribs['temples'],False)
        self.ui.next_button.setEnabled(True)                      
        self.ui.stackedWidget.setCurrentIndex(first_page_ind)
        
#     def addKingdomWidget (self, kingdom):
#         self.kingdom_homepage.addButton (kingdom.name, self.ui.stackedWidget.count())
#         kingdom_widgets_list = BookWorldMainPage (self.model,self.ui.stackedWidget)
#         kingdom_widgets_list.setContent (kingdom)
#         self.kingdom_widgets_list.append(kingdom_widgets_list)
#         self.ui.stackedWidget.addWidget(kingdom_widgets_list)
#         self.nb_pages =  0      
#         for groupe in kingdom.groupes.values() :
#             if len(groupe.sub_groupes)==0 : 
#                 if (self.nb_pages%2)==0 : 
#                     kingdom_widgets_list = BookWorldArmy (self.model,self.ui.stackedWidget)
#                     kingdom_widgets_list.setLeftContent (groupe)
#                     self.kingdom_widgets_list.append(kingdom_widgets_list)
#                     self.ui.stackedWidget.addWidget(kingdom_widgets_list)
# 
#                 else:
#                     kingdom_widgets_list.setRightContent(groupe)
#                 self.nb_pages+=1
#                 for warrior in groupe.warriorsList().values():
#                     kingdom_widgets_list.addVignette(warrior)                
#             else: 
#                 for sg in groupe.sub_groupes:
#                     if self.nb_pages == 1 : 
#                         kingdom_widgets_list.setRightContent(groupe,sg)
#                     else:
#                         if (self.nb_pages%2)==0 : 
#                             kingdom_widgets_list = BookWorldArmy (self.model,self.ui.stackedWidget)
#                             kingdom_widgets_list.setLeftContent (groupe,sg)
#                             self.kingdom_widgets_list.append(kingdom_widgets_list)
#                             self.ui.stackedWidget.addWidget(kingdom_widgets_list)
#                         else:
#                             kingdom_widgets_list.setRightContent(groupe,sg)
#                     self.nb_pages+=1
#                     for warrior in sg.warriorsList().values():
#                         kingdom_widgets_list.addVignette(warrior)
# 
# #             for sg in groupe.sub_groupes :
# #                 kingdom_widgets_list.addGroupe(sg)
# #                 for warrior in sg.warriorsList().values():
# #                     kingdom_widgets_list.addVignette(warrior)
#         self.ui.next_button.setEnabled(True)                            

    def goNextPage (self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
        if self.ui.stackedWidget.currentIndex() == (self.ui.stackedWidget.count()-1):
            self.ui.next_button.setEnabled(False)

        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.previous_button.setEnabled(False)
        else :
            self.ui.previous_button.setEnabled (True)

    def goToKingdom (self, kingdom):
        print ('goToKingdom...',kingdom.name)
        if self.kingdom_homepage != None :
            self.kingdom_homepage.onEmpireSelected(kingdom.empire().name)
        self.loadKingdom(kingdom.name)
#             buttons = self.kingdom_homepage.list_buttons
#             ind= -1
#             for b in buttons:
#                 if b.text()== kingdom.name :
#                     ind = int(b.objectName())
#                 elif b.text().split('/').replace(" ","") == kingdom.name :
#                     ind = int(b.objectName())
#             if ind != -1 :
#                 self.ui.stackedWidget.setCurrentIndex(ind)
#     
        
    def goToGroupe (self,groupe):
        self.goToKingdom(groupe.kingdom())
        for i  in  range (self.ui.stackedWidget.count()):
            w = self.ui.stackedWidget.widget(i)
            try : 
                if w.groupe_left.name == groupe.name or w.groupe_right.name == groupe.name :
                    self.ui.stackedWidget.setCurrentIndex(i)
                    break
            except AttributeError:
                pass
    
    def goToEmpire(self, empire):
        print ('goToEmpire...')
        if self.kingdom_homepage != None :
            self.kingdom_homepage.onEmpireSelected(empire.name)
        self.ui.stackedWidget.setCurrentIndex(0)
                
    def goPreviousPage (self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()-1)
        if self.ui.stackedWidget.currentIndex() == (self.ui.stackedWidget.count()-1):
            self.ui.next_button.setEnabled(False)
        else :
            self.ui.next_button.setEnabled(True)
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.previous_button.setEnabled(False)


#     def changeKingdomPage (self ):
#         id_widget = self.sender().objectName()
#         self.ui.stackedWidget.setCurrentIndex(int(id_widget))
    