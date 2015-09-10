from PyQt5.Qt import  QPushButton,QWidget, QSizePolicy, QSize, QColor
from PyQt5 import  QtWidgets
     
from python_modules.view.view_kingdom.ui_book_world_homepage import Ui_BookWorldHomepage
from python_modules.view.view_kingdom.pie_chart import PieChart
import random

     
class BookWorldHomepage ( QWidget,Ui_BookWorldHomepage):
    def __init__ (self,book,parent=None):
        super(BookWorldHomepage,self).__init__(parent)
        self.setupUi(self)
        self.book = book
        self.list_buttons = []
        self.pie= PieChart(self.kingdom_contribution_page,{'all:':0,'alive:':0,'dead:':0})
        self.kingdom_page_layout.addWidget(self.pie)
        
        self.pie_faction_left = PieChart(self.faction_left_pie,{'all:':0,'alive:':0,'dead:':0})
        self.faction_left_pie_layout.addWidget(self.pie_faction_left)

        self.pie_faction_right= PieChart(self.faction_right_pie, {'all:':0,'alive:':0,'dead:':0})
        self.faction_right_pie_layout.addWidget(self.pie_faction_right)
        
        self.net_chart_button.clicked.connect(self.onNextChart)
        
    def onNextChart(self):
        new = (self.stackedWidget.currentIndex()+1)% self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(new)
        
    def setLeftPage(self,faction1_name, faction2_name, empires1_list, empires2_list):
        self.listEmpire1 = empires1_list
        self.listEmpire2 = empires2_list
        self.faction_left.setText(faction1_name)
        self.faction_right.setText(faction2_name)

        sp = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #print ('WORLD Homepage page gauche: nb empire 1 et 2 :',len(empires1_list.values()),len(empires2_list.values()))
        try : 
            total = {'all':len(self.book.model.getFactionFromName(faction1_name).getWarriorList()),'dead':len(self.book.model.getFactionFromName(faction1_name).getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(self.book.model.getFactionFromName(faction1_name).getWarriorList(lambda x:x.attribs['HP']>0))}
        except AttributeError :
            total = {'all':0,'alive':0,'dead':0}

        self.pie_faction_left.setTotal(total)
        data = []    
        for value in empires1_list.values() :
            button = QtWidgets.QPushButton()

            button.setSizePolicy(sp)
            button.setText(value.name)
            button.setObjectName(value.name)
            button.clicked.connect(self.onEmpireSelected)
            self.empire_left_layout.addWidget(button)
            data_item = {'color':QColor(random.randrange(255),random.randrange(255),random.randrange(255)),'all':len(value.getWarriorList()),'dead':len(value.getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(value.getWarriorList(lambda x:x.attribs['HP']>0)),'label':value.name}
            data.append(data_item)

        self.pie_faction_left.setData(data)
        try : 
            total = {'all':len(self.book.model.getFactionFromName(faction2_name).getWarriorList()),'dead':len(self.book.model.getFactionFromName(faction1_name).getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(self.book.model.getFactionFromName(faction1_name).getWarriorList(lambda x:x.attribs['HP']>0))}
        except AttributeError :
            total = {'all':0,'alive':0,'dead':0}

        self.pie_faction_right.setTotal(total)
        data = [] 
        for value in empires2_list.values():
            button = QtWidgets.QPushButton()
            button.setSizePolicy(sp)
            button.clicked.connect(self.onEmpireSelected)
            button.setText(value.name)
            button.setObjectName(value.name)
            self.empire_right_layout.addWidget(button)
            data_item = {'color':QColor(random.randrange(255),random.randrange(255),random.randrange(255)),'all':len(value.getWarriorList()),'dead':len(value.getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(value.getWarriorList(lambda x:x.attribs['HP']>0)),'label':value.name}
            data.append(data_item)
                        
        self.pie_faction_right.setData(data)

    def onEmpireSelected (self,empire_name=None):
        self.book.resetEmpireSelection()
        if type(empire_name) == bool:
            name = self.sender().objectName()
            print ('empire name sender',empire_name)
        else:
            name = empire_name
            print ('empire name',empire_name)
        self.right_empire_name.setText(name)

        list_kingdoms = {}
        if name in self.listEmpire1 :
            list_kingdoms= self.listEmpire1[name].kingdoms
        elif name in self.listEmpire2:
            list_kingdoms = self.listEmpire2[name].kingdoms

        total = {'all':len(self.book.model.getEmpireFromName(name).getWarriorList()),'dead':len(self.book.model.getEmpireFromName(name).getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(self.book.model.getEmpireFromName(name).getWarriorList(lambda x:x.attribs['HP']>0))}
        self.pie.setTotal(total)
        data = []    
        for kingdom in list_kingdoms.values() :
            #self.book.addKingdomWidget(kingdom)
            self.addButton (kingdom.name)
            data_item = {'color':kingdom.color,'all':len(kingdom.getWarriorList()),'dead':len(kingdom.getWarriorList(lambda x:x.attribs['HP']<=0)),'alive':len(kingdom.getWarriorList(lambda x:x.attribs['HP']>0)),'label':kingdom.name}
            data.append(data_item)
                        
        self.pie.setData(data)    
        self.book.empire_selected_name = name


    def updateContent(self):

        pass
    def addButton (self, kingdom_name):
        sp = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.button_k = ButtonKingom(self)
        self.button_k.setSizePolicy(sp)
        self.button_k.setText(kingdom_name)
        self.list_buttons.append (self.button_k)
        self.button_k.setObjectName(kingdom_name)
        #self.button_k.connectTo(self.book.changeKingdomPage )
        self.button_k.connectTo(self.book.loadKingdom )        
        self.verticalLayout_2.addWidget(self.button_k)


class ButtonKingom (QPushButton):
    def __init__(self,parent=None):
        super(ButtonKingom,self).__init__(parent)
        
    def connectTo(self,slot):  
        self.clicked.connect(slot)          