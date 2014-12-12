from PyQt5.Qt import QDialog
from python_modules.config import Config
     
from python_modules.main_view.ui_dialog_settigns import Ui_DialogSettings
     
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
    
    