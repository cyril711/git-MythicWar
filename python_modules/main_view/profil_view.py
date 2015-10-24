from PyQt5.Qt import  QWidget, QListWidgetItem, QPalette, QImage, QColor, QIcon,\
    QPixmap, QSize

from python_modules.config import Config
from python_modules.main_view.ui_profil_widget import Ui_ProfilWidget
import os


class HerosListWidgetItem (QListWidgetItem):
    def __init__(self, heros, parent=0):
        super(HerosListWidgetItem, self).__init__(parent)
        self.heros = heros
        self.setText(self.heros.name)
        
class ProfilWidget (QWidget,Ui_ProfilWidget):
    def __init__(self,model,parent=None):
        super(ProfilWidget,self).__init__(parent)
        self.setupUi(self)
      #  self.tableWidget.setUpdatesEnabled(True)    
        self.settings = Config().instance.settings
        self.list_selected.hide()
        self.list_selected2.hide()
        self.connections()
        self.initView(model)        

    def initView (self,model):
        self.model = model



    def connections (self):
        self.list_selected.itemDoubleClicked.connect(self.onUnselectItem)
        self.list_selected.itemClicked.connect(self.onSelectItem)


    def onSelectItem (self, item):
        self.update(item.heros)
        
    def onUnselectItem (self, item):
        item.heros.setSelected(False)
        #self.list_selected.removeItemWidget(item)
            
    def updateSelectionList (self):
        self.list_selected.clear()
        if len(self.model.selectedWarriors())!= 0 and self.list_selected.isHidden(): 
            self.list_selected.show()
        elif len(self.model.selectedWarriors())== 0 and self.list_selected.isHidden()== False: 
            self.list_selected.hide()
        for item in self.model.selectedWarriors():
            item_list = HerosListWidgetItem (item,self.list_selected)
            self.list_selected.addItem(item_list)
            
    def update (self,warrior):
        self.warrior = warrior
        groupe_name = warrior.groupe().name
        if warrior.masterGroupe() != None : 
            groupe_name = warrior.masterGroupe().name+"/"+groupe_name
         
        kingdom_name = warrior.kingdom().name
        empire_name = warrior.empire().name
        faction_name = warrior.faction().name
        path = os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom_name,'Picture',groupe_name,warrior.name)
        picture = QPixmap(path+"/portrait.jpg").scaledToWidth(self.picture.width())
   
        self.warrior_name.setText(warrior.name.replace("_"," "))
        self.warrior_name.setObjectName("Warrior_name")
        couleur = warrior.groupe().attribs['color']
        if warrior.masterGroupe() != None : 
            couleur = warrior.masterGroupe().attribs['color']

        self.picture.setPixmap(picture)


        self.progressBar_life.setStyleSheet("  QProgressBar{ background-color: red;}")
        #self.ui.progressBar_life.setAlignment(QtCore.Qt.AlignCenter)
        #self.progressBar_energy.setStyleSheet("  QProgressBar::chunk {     background-color: #05B8CC;width: 20px;}")
        #self.ui.progressBar_MP.setAlignment(QtCore.Qt.AlignCenter)
        try:
            hp_percent = float(self.warrior.attribs['HP'] / self.warrior.attribs['HP_max'])* 100
            mp_percent = float(self.warrior.attribs['MP'] / self.warrior.attribs['MP_max'])* 100
        except (ZeroDivisionError,KeyError) as e :
            hp_percent =0
            mp_percent =0
        self.progressBar_life.setValue(int(hp_percent))
        self.progressBar_energy.setValue(int(mp_percent))
        self.profil_completion.setPixmap(QPixmap(":/icons/128x128/state_"+str(warrior.attribs['complete']+1)).scaledToHeight(32))
        self.profil_completion.setStyleSheet("#"+self.profil_completion.objectName()+"{background-color:transparent;}")

        pal = QPalette(self.rank_text.palette())
        image = QImage(os.path.join(Config().instance.path_to_icons(),"rank")+"/star_"+warrior.groupe().attribs["color"]+".png")
        value = image.pixel(image.width()/2.0,image.height()/2.0)
        pal.setColor(QPalette.WindowText, QColor(value))
        self.rank_text.setPalette(pal)
        self.rank_text.setText(str(warrior.attribs["rank"]))
        #Boutton Faction 
        path = os.path.join(Config().instance.path_to_icons(),"faction","32x32",faction_name)
        self.iconFaction.setIcon(QIcon(path))
        self.iconFaction.setToolTip(warrior.faction().name)
        #Boutton Empire 
        path = os.path.join(Config().instance.path_to_icons(),"empire","32x32",empire_name)
        self.iconEmpire.setIcon(QIcon(path))
        self.iconEmpire.setToolTip(warrior.empire().name)
        self.iconEmpire.clicked.connect(self.onEmpireClicked)
        #Boutton Kingdom
        path = os.path.join(Config().instance.path_to_icons(),"kingdom","32x32",kingdom_name)
        self.iconKingdom.setIcon(QIcon(path))
        self.iconKingdom.setToolTip(self.warrior.kingdom().name)
        self.iconKingdom.clicked.connect(self.onKingdomClicked)
        #Boutton Groupe
        self.iconGroupe.setText(groupe_name.replace("_"," "))
        groupe_color = self.warrior.groupe().attribs['color']
        if self.warrior.masterGroupe() != None : 
            groupe_color = self.warrior.masterGroupe().attribs['color']
        self.iconGroupe.setStyleSheet("#"+self.iconGroupe.objectName()+"{background-image:url(:/textures/"+groupe_color+");}")
        self.iconGroupe.clicked.connect(self.onGroupClicked)
        path = os.path.join(Config().instance.path_to_icons(),"actions",warrior.attribs['status'])
        # Icone d etat
        self.iconState.setPixmap(QPixmap(path).scaledToHeight(64))


    def onGroupClicked (self):
        self.model.askForGroup.emit(self.warrior.groupe())
    def onKingdomClicked (self):
        self.model.askForKingdomPage.emit(self.warrior.kingdom())
    def onEmpireClicked (self):
        self.model.askForKingdomHomePage.emit(self.warrior.empire())

 