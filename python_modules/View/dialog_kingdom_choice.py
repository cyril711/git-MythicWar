from PyQt5.Qt import QTextEdit, QLayout, QPushButton, QLabel, QVBoxLayout,\
     QHBoxLayout, QDialog, QDockWidget, QPixmap, QWidget, QListWidgetItem
from PyQt5 import QtCore
     
from python_modules.View.ui_dialog_kingdom_choice import Ui_DialogKingdomChoice
     
class DialogKingdomChoice (QDialog, Ui_DialogKingdomChoice):
    def __init__ (self,model,parent=None):
        super(DialogKingdomChoice,self).__init__(parent)
        self.setupUi(self)
        self.model = model

    def init (self):
        pass
    