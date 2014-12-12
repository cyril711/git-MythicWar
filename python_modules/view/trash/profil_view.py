from PyQt5.Qt import QTextEdit, QLayout, QPushButton, QLabel, QVBoxLayout,\
     QHBoxLayout, QDialog, QDockWidget, QPixmap, QWidget
from PyQt5 import QtCore
     
from python_modules.View.ui_profil_widget import Ui_profilWidget

     
class ProfilWidget (QWidget, Ui_profilWidget):
    def __init__ (self,model,parent=None):
        super(ProfilWidget,self).__init__(parent)
        self.setupUi(self)
        self.model = model
      #  self.setStyleSheet("#dockWidgetContents{background-image: url(C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/background/background03.jpg)}")

    def init (self):
        pass
        
    def onSelectionChange (self):
        warrior = self.model.selectedWarrior[self.model.first_selected]
        p = QPixmap(warrior.attribs['picture'])
        diff_V = p.height()/self.picture.height()
        diff_H = p.width()/self.picture.width()
        if not p.isNull():
            if diff_V < diff_H:
                p = p.scaledToHeight(self.picture.height())
            else:
                p = p.scaledToWidth(self.picture.width())
        self.picture.setPixmap(p)
        self.Title.setText(warrior.name)
        self.faction_name.setText(warrior.faction().name)
        self.empire_name.setText(warrior.empire().name)
        self.royaume_name.setText(warrior.kingdom().name)
        self.groupe_name.setText(warrior.groupe().name)
    
    def connections (self):
        self.previousButton.clicked.connect(self.onPreviousButtonClicked)
        self.nextButton.clicked.connect(self.onPreviousButtonClicked)
    
    def onPreviousButtonClicked (self):
        self.current_profil_ind = (self.current_profil_ind -1)%len(self.profils)
        
    def onNextButtonClicked (self):
        self.current_profil_ind = (self.current_profil_ind +1)%len(self.profils)
