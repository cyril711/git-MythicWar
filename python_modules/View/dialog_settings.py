from PyQt5.Qt import QTextEdit, QLayout, QPushButton, QLabel, QVBoxLayout,\
     QHBoxLayout, QDialog, QDockWidget, QPixmap, QWidget, QListWidgetItem
from PyQt5 import QtCore
     
from python_modules.View.ui_dialog_save import Ui_DialogSettings
     
class DialogSettings (QDialog, Ui_DialogSettings):
    def __init__ (self,model,parent=None):
        super(DialogSettings,self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.settings = Config().instance.settings
        for raster in  self.settings.value("map/available_raster").split[","]: 
            self.comboBoxMapGoogleTile.addItem(raster)
            if raster == self.settings.value("map/current_raster"):
                self.comboBoxMapGoogleTile.setCurrentIndex(self.comboBoxMapGoogleTile.count()-1)
    def applyChanges (self):
        self.settings.setValue ("map/current_raster",self.comboBoxMapGoogleTile.currentText())
        
    
    
        
    def init (self):
        pass
    
    