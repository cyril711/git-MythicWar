from PyQt5.Qt import QWidget
from PyQt5 import QtCore
     
from python_modules.view.view_heros.ui_warrior_layout import Ui_WarriorLayout
from python_modules.view.view_heros.book_warrior_homepage import BookWarriorHomepage
from python_modules.view.view_heros.book_warrior_page import BookWarriorPage


class WarriorLayout (QWidget, Ui_WarriorLayout):
    modified = QtCore.pyqtSignal(int)
    def __init__ (self, model, parent=None):
        super(WarriorLayout, self).__init__(parent)
        self.setupUi(self)
        self.model = model
        # self.widget.setStyleSheet("#widget{background-image: url(:/textures/saphir)}")
        self.connections()
        self.homepage = None

        self.ind_warrior = 0

        self.selection2 = []
        self.init(model)
        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.new_page = None
        self.editable = True

        # self.preset_all_button.setStyleSheet("border-top: 3px transparent;border-bottom: 3px transparent;border-right: 10px transparent;border-left: 10px transparent;");
    def connections (self):
        self.next_button.clicked.connect(self.goNextWarrior)
        self.previous_button.clicked.connect(self.goPreviousWarrior)

        self.preset_all_button.clicked.connect(self.onPresetAll)
        self.preset_filtre_button.clicked.connect(self.onPresetFilter)
        self.preset_selection_button.clicked.connect(self.onPresetSelection)
        self.model.askForHerosPage.connect(self.onPresetFromModel)

    def onPresetFromModel (self, heros):
        print ('XXXonpreset from model', len(self.selection2))
        self.selection2 = []
        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)
        ind = None
        i = 0
        for h in heros.groupe().warriors.values():
            if h.name == heros.name :
                ind = i
            self.selection2.append(h)
            i = i + 1
        self.homepage.setRightContent(self.selection2)
        print ('onpreset from model', len(self.selection2))
        if len(self.selection2) >= 1:
            self.next_button.setEnabled(True)
        self.goWarriorPage(ind)
    def onPresetSelection (self):
        print ('XXXonPresetSelecctio:', len(self.selection2))
        self.selection2 = self.model.selectedWarriors()
        print ('onPresetSelecctio:', len(self.selection2))
        if len(self.selection2) >= 1:
            self.next_button.setEnabled(True)
        self.homepage.setRightContent(self.selection2)
    def onPresetFilter (self):
        print ('XXXonPresetFilter:', len(self.selection2))
        self.selection2 = self.model.filteredWarriors()
        print ('onPresetFilter:', len(self.selection2))
        if len(self.selection2) >= 1:
            self.next_button.setEnabled(True)
        self.homepage.setRightContent(self.selection2)
    
    # null ca
    def onPresetFromHomepage  (self):
        print ('XXXonPreseFromeHompage:', len(self.selection2))
        if self.homepage != None :
            self.selection2 = self.homepage.list_warrior
            print ('XXXonPreseFromeHompage:', len(self.selection2))
            if len(self.selection2) >= 1:
                self.next_button.setEnabled(True)
    
    def onPresetAll (self):
        print('XXXpreserall', len(self.model.allWarriors()))
        self.selection2 = self.model.allWarriors()
        if len(self.selection2) >= 1:
            self.next_button.setEnabled(True)
        self.homepage.setRightContent(self.selection2)
    def init (self, model):
        self.model = model
        # lecture du fichier de config pour charger les presets
        if self.homepage != None :
            self.horizontalLayout.removeWidget(self.homepage)
            self.homepage.setParent(None)
        self.homepage = BookWarriorHomepage(self.model, self)
        self.homepage.updateSelection.connect(self.onPresetFromHomepage)
        self.homepage.setLeftPage()
        self.horizontalLayout.insertWidget(1, self.homepage)
        self.preset_all_button.click()
#         self.homepage.setLeftPage("config.xml")
        # self.central_widget = self.homepage
        
    def setEnableEditableItems (self, enable):
        print ('XXX4', len(self.selection2))
        self.editable = enable
        if self.new_page != None:
            self.new_page.setEnabled(enable)
    def goNextWarrior (self):
        print ('XXX5', len(self.selection2))
        self.ind_warrior = (self.ind_warrior + 1) % len(self.selection2)
        
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None
        else:
            self.homepage.setParent(None)
            self.horizontalLayout.removeWidget(self.homepage)
        self.new_page = BookWarriorPage (self, self.selection2[self.ind_warrior])
        self.new_page.setEnabled(self.editable)
       # self.setStyleSheet('BookWarriorPageN{background-image: url(:/background/grec)}')
        self.horizontalLayout.insertWidget(1, self.new_page)

#     def mouseMoveEvent(self, event):
#         super(WarriorLayout,self).mouseMoveEvent(event)
#         print ('oooooooooooo')
#         return super(WarriorLayout,self).mouseMoveEvent(event)

    def onHome (self):
        if self.new_page != None :
            self.horizontalLayout.removeWidget(self.new_page)
            self.new_page.setParent(None)
            self.new_page = None
        else:
            self.horizontalLayout.removeWidget(self.homepage)
            self.homepage.setParent(None)
        self.homepage = BookWarriorHomepage(self.model, self)
        self.homepage.updateSelection.connect(self.onPresetFromHomepage)
        self.homepage.setLeftPage()
        self.horizontalLayout.insertWidget(1, self.homepage)

    def goPreviousWarrior(self):
        print ('XXX3', len(self.selection2))        
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None

        self.ind_warrior = (self.ind_warrior - 1) % len(self.selection2)
        self.new_page = BookWarriorPage (self, self.selection2[self.ind_warrior])
        self.horizontalLayout.insertWidget(1, self.new_page)
            
    def goWarriorPage (self , ind=None):
        print ('XXX2', len(self.selection2))
        if self.new_page != None :
            self.new_page.setParent(None)
            self.new_page = None
        else:
            self.homepage.setParent(None)
            self.horizontalLayout.removeWidget(self.homepage)
        if ind == None:
            self.ind_warrior = int(self.sender().objectName())
        else:
            self.ind_warrior = ind
        print ('goWarriorPage : ', len(self.selection2))
        self.new_page = BookWarriorPage (self, self.selection2[self.ind_warrior])
        self.new_page.setEnabled(self.editable)
        self.horizontalLayout.insertWidget(1, self.new_page)
    
