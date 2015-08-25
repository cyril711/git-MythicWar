from PyQt5.Qt import QDialog, QPixmap, QWidget, QSize, QIcon, QColorDialog
from PyQt5 import  QtWidgets
     
from python_modules.view.view_kingdom.ui_book_world_main_page import Ui_BookWorldMainpage
from python_modules.config import Config
from python_modules.view.heros_vignette import HerosButton,HerosLabel
import os

class BookWorldMainPage ( QWidget,Ui_BookWorldMainpage):
    def __init__ (self,model,parent=None):
        super(BookWorldMainPage,self).__init__(parent)
        self.setupUi(self)
        self.nb_col = 0
        self.nb_row = 0
        self.model = model
        self.settings = Config().instance.settings

    def connections (self):

        self.historyTextEdit.textChanged.connect(self.onModificationKingdom)
        self.descriptionTextEdit.textChanged.connect(self.onModificationKingdom)
        


    def onModificationKingdom(self):
        self.parent().parent().modifiedKingdom.emit(self.kingdom)        
        
    def onUpdateColorKingdom (self):
        dlg = QColorDialog(self.kingdom.color)
        dlg.setOption(QColorDialog.ShowAlphaChannel,True)
        if dlg.exec_() == QDialog.Accepted:
            self.kingdom.color = dlg.currentColor()
            self.setStyleSheet("QLineEdit,QFrame{ border: 2px solid rgb("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+");background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            
            #self.setStyleSheet("QPlainTextEdit{ background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.button_color.setStyleSheet("#button_color{background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.button_color.show()
        else:
            dlg.close()
    def setContent (self, kingdom):
        self.kingdom = kingdom
        faction_name = kingdom.parent.parent.name
        empire_name = kingdom.parent.name
        #self.setStyleSheet("QPlainTextEdit{ border: 2px solid rgb("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+";)}")
        self.setStyleSheet("QLineEdit,QFrame{ border: 2px solid rgb("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+";)}")

        self.button_color.setStyleSheet("#button_color{background-color: rgba("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+","+str(kingdom.color.alpha())+");}")
        self.button_color.clicked.connect(self.onUpdateColorKingdom)
        self.land_picture.setScaledContents(True)
        self.land_picture.setPixmap(QPixmap(os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom.name,"Land.jpg")))
        self.army_picture.setPixmap(QPixmap(os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom.name,"Army.png")))        
        self.army_picture.setScaledContents(True)        
        self.Title.setText( kingdom.name)
        self.historyTextEdit.appendPlainText(kingdom.attribs['armee'])
        self.descriptionTextEdit.appendPlainText(kingdom.attribs['description'])
        avancement = kingdom.avancement ()
        self.button_color.setText("( "+str(avancement)+" % ) ")
        self.connections()

    def setEnableEditableItems (self,enable):
        self.historyTextEdit.setEnabled(enable)
        self.descriptionTextEdit.setEnabled(enable)
        self.comboBoxColor.setEnabled(enable)
        
  