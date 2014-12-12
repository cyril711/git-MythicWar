from PyQt5.Qt import QPushButton, QVBoxLayout,QPixmap, QWidget,QSizePolicy, QIcon, QTreeWidgetItem
from PyQt5 import QtCore
     
from python_modules.view.view_heros.ui_book_warrior_homepage import Ui_BookWarriorHomepage
from python_modules.view.heros_vignette import HerosButton, HerosLabel
from python_modules.config import Config
#basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   


class BookWarriorHomepage ( QWidget,Ui_BookWarriorHomepage):
    def __init__ (self,model,parent=None):
        super(BookWarriorHomepage,self).__init__(parent)
        self.setupUi(self)
        self.max_vignettes = 20
        self.nb_col = 0
        self.nb_row = 0
        self.vignettes_liste = []
        self.model = model
        self.settings = Config().instance.settings
    def setLeftPage(self):
        i = 0
        for faction in self.model.factions.values() :
            item_f = QTreeWidgetItem(self.treeKingdom)
            self.treeKingdom.insertTopLevelItem(i,item_f)
            item_f.setText(i,faction.name)
            i = i +1
            for empire in faction.empires.values():
                item_e = QTreeWidgetItem()
                item_e.setText(i,empire.name)
                item_f.addChild(item_e)
                for kingdom in empire.kingdoms.values():
                    item_k = QTreeWidgetItem()
                    item_k.setText(i,kingdom.name)
                    item_e.addChild(item_k)
                    for groupe in kingdom.groupes.values():
                        item_g = QTreeWidgetItem()
                        item_g.setText(i,groupe.name)
                        item_k.addChild(item_g)
    
    def setRightContent (self, list_warrior):
        for v in self.vignettes_liste : 
            v.setParent(None)
            self.gridLayout.removeWidget(v)
#         while self.gridLayout.takeAt(0) !=  None :
#             del self.gridLayout.takeAt(0).widget
#             item =  self.gridLayout.takeAt(0)
#             print ('ll')
#             del item
        self.nb_col = 0
        self.nb_row = 0
        self.vignettes_liste = []
        for i in range (min(len(list_warrior),self.max_vignettes)):
            self.addVignette(list_warrior[i],i)

        
    def addVignette (self,warrior,i):
        widget_vignette = QWidget(self.vignettes)        
        layout_one_vignette = QVBoxLayout(widget_vignette)
        layout_one_vignette.setSpacing(0)
        layout_one_vignette.setContentsMargins(0, 0, 0, 0)
        warrior_button = QPushButton(widget_vignette)
        warrior_button.setObjectName(str(i))
        warrior_button.clicked.connect(self.parent().goWarriorPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        warrior_button.setFixedSize(QtCore.QSize(100,120))
        warrior_button.setSizePolicy(sizePolicy)
        layout_one_vignette.addWidget(warrior_button)
        
        # label
        warrior_label = HerosLabel(warrior,widget_vignette)
#         warrior_label.setText(warrior.name)
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(warrior_label.sizePolicy().hasHeightForWidth())
#         warrior_label.setSizePolicy(sizePolicy)
#         warrior_label.setMinimumSize(QtCore.QSize(0, 10))
#         warrior_label.setAlignment(QtCore.Qt.AlignCenter)
        layout_one_vignette.addWidget(warrior_label)
        
        max_col  = 3
        spliter = warrior.attribs['picture'].split("/")
        picture_name = spliter[len(spliter)-1]
        groupe_name = warrior.groupe().name
        if warrior.masterGroupe() != None : 
            groupe_name = warrior.masterGroupe().name+"/"+groupe_name
        
        kingdom_name = warrior.kingdom().name
        empire_name = warrior.empire().name
        faction_name = warrior.faction().name
        icon = QIcon(QPixmap(self.settings.value("global/resources_path")+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+warrior.name+"/portrait_thumbnail.jpg"))

        #print (basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+warrior.name+"/portrait_thumbnail.jpg")
        warrior_button.setIcon(icon)
        warrior_button.setIconSize(QtCore.QSize(100,120))

        if self.nb_col == 0:
            self.nb_row = self.nb_row + 1


        self.gridLayout.addWidget(widget_vignette,self.nb_row,self.nb_col)
        self.vignettes_liste.append(widget_vignette)
        self.nb_col = (self.nb_col +1)%max_col