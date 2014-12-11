from PyQt5.Qt import QTextEdit, QLayout, QPushButton, QLabel, QVBoxLayout,\
     QHBoxLayout, QDialog, QDockWidget, QPixmap, QWidget, QObject, QSizePolicy
from PyQt5 import QtCore, QtWidgets
     
from python_modules.View.ui_book_world_homepage import Ui_BookWorldHomepage
from PyQt5.uic.Compiler.qtproxies import QtGui

     
class BookWorldHomepage ( QWidget,Ui_BookWorldHomepage):
    def __init__ (self,book,parent=None):
        super(BookWorldHomepage,self).__init__(parent)
        self.setupUi(self)
        self.book = book
        self.list_buttons = []
    def setLeftPage(self,faction1_name, faction2_name, empires1_list, empires2_list):
        self.listEmpire1 = empires1_list
        self.listEmpire2 = empires2_list
        self.faction_left.setText(faction1_name)
        self.faction_right.setText(faction2_name)

        sp = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        for value in empires1_list.values() :
            button = QtWidgets.QPushButton()

            button.setSizePolicy(sp)
            button.setText(value.name)
            button.setObjectName(value.name)
            button.clicked.connect(self.onEmpireSelected)
            self.empire_right_layout.addWidget(button)

        for value in empires2_list.values():
            button = QtWidgets.QPushButton()
            button.setSizePolicy(sp)
            button.clicked.connect(self.onEmpireSelected)
            button.setText(value.name)
            button.setObjectName(value.name)
            self.empire_right_layout.addWidget(button)

    def onEmpireSelected (self):
        self.book.removeAllKingdomWidgets ()
        name = self.sender().objectName()
        self.right_empire_name.setText(name)
        list_kingdoms = []
        if name in self.listEmpire1 :
            list_kingdoms= self.listEmpire1[name].kingdoms
        elif name in self.listEmpire2:
            list_kingdoms = self.listEmpire2[name].kingdoms
        for kingdom in list_kingdoms.values() :
            self.book.addKingdomWidget(kingdom)


    def addButton (self, kingdom_name, id_widget):
        sp = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.button_k = ButtonKingom(self)
        self.button_k.setSizePolicy(sp)
        self.button_k.setText(kingdom_name)
        self.list_buttons.append (self.button_k)
        self.button_k.setObjectName(str(id_widget))
        self.button_k.connectTo(self.book.changeKingdomPage )        
        self.verticalLayout_2.addWidget(self.button_k)


class ButtonKingom (QPushButton):
    def __init__(self,parent=None):
        super(ButtonKingom,self).__init__(parent)
        
    def connectTo(self,slot):  
        self.clicked.connect(slot)          