from PyQt5.Qt import QWidget
from PyQt5 import QtCore
     
from python_modules.view.view_heros.ui_warrior_layout import Ui_WarriorLayout
from python_modules.view.view_heros.book_warrior_homepage import BookWarriorHomepage
from python_modules.view.view_heros.book_warrior_page import BookWarriorPage


class WarriorLayout ( QWidget,Ui_WarriorLayout):
    modified = QtCore.pyqtSignal(int)
    def __init__ (self,model,parent=None):
        super(WarriorLayout,self).__init__(parent)
        self.setupUi(self)
        self.model = model
        #self.widget.setStyleSheet("#widget{background-image: url(:/textures/saphir)}")
        self.connections()
        self.init()
        self.ind_warrior = 0
        self.selection = []
        self.preset_all_button.click()
        self.new_page = None
        self.editable = False

        #self.preset_all_button.setStyleSheet("border-top: 3px transparent;border-bottom: 3px transparent;border-right: 10px transparent;border-left: 10px transparent;");
    def connections (self):
        self.next_button.clicked.connect(self.goNextWarrior)
        self.previous_button.clicked.connect(self.goPreviousWarrior)
        self.preset_all_button.clicked.connect(self.onPresetAll)
        self.preset_filtre_button.clicked.connect(self.onPresetFilter)
        self.preset_selection_button.clicked.connect(self.onPresetSelection)
        self.model.askForHerosPage.connect(self.onPresetFromModel)

    def onPresetFromModel (self,heros):
        self.selection = []
        ind = None
        i = 0
        for h in heros.groupe().warriors.values():
            if h.name == heros.name :
                ind = i
            self.selection.append(h)
            i = i + 1
        self.homepage.setRightContent(self.selection)
        self.goWarriorPage(ind)
    def onPresetSelection (self):
        self.selection = self.model.selectedWarriors()
        self.homepage.setRightContent(self.selection)
    def onPresetFilter (self):
        self.selection = self.model.filteredWarriors()
        self.homepage.setRightContent(self.selection)        
    def onPresetAll (self):
        self.selection = self.model.allWarriors()
        self.homepage.setRightContent(self.selection)
    def init (self):
        #lecture du fichier de config pour charger les presets
        
        self.homepage = BookWarriorHomepage(self.model,self)
        self.homepage.setLeftPage()
        self.horizontalLayout.insertWidget(1,self.homepage)

#         self.homepage.setLeftPage("config.xml")
        #self.central_widget = self.homepage
        
    def setEnableEditableItems (self, enable):
        self.editable = enable
        if self.new_page!= None:
            self.new_page.setEnabled(enable)
    def goNextWarrior (self):
        self.ind_warrior = (self.ind_warrior+1)%len(self.selection)
        
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None
        else:
            self.homepage.setParent(None)
            self.horizontalLayout.removeWidget(self.homepage)
        self.new_page = BookWarriorPage (self,self.selection[self.ind_warrior])
        self.new_page.setEnabled(self.editable)
       # self.setStyleSheet('BookWarriorPageN{background-image: url(:/background/grec)}')
        self.horizontalLayout.insertWidget(1,self.new_page)



    def goPreviousWarrior(self):
        
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None

        self.ind_warrior = (self.ind_warrior-1)%len(self.selection)
        self.new_page = BookWarriorPage (self,self.selection[self.ind_warrior])
        self.horizontalLayout.insertWidget(1,self.new_page)
            
    def goWarriorPage (self ,ind=None):
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None
        else:
            self.homepage.setParent(None)
            self.horizontalLayout.removeWidget(self.homepage)
        if ind==None:
            self.ind_warrior = int(self.sender().objectName())
        else:
            self.ind_warrior = ind
        self.new_page = BookWarriorPage (self,self.selection[self.ind_warrior])
        self.new_page.setEnabled(self.editable)
        self.horizontalLayout.insertWidget(1,self.new_page)
    