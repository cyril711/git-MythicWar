from PyQt5.Qt import QWidget, QVBoxLayout, QLabel, QIcon, QSize, QFont
from PyQt5 import QtCore
from python_modules.view.view_kingdom.ui_book_world_army import Ui_BookWorldArmy
from python_modules.view.heros_vignette import HerosButton, HerosLabel,\
    TempleButton, TempleLabel
from python_modules.config import Config
from python_modules.model.temple import Temple
# basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   


        
class BookWorldArmy (QWidget, Ui_BookWorldArmy):
    def __init__(self, model, parent):
        super(BookWorldArmy, self).__init__()
        self.setupUi(self)
        self.current_page = 0
        self.model = model
        self.settings = Config().instance.settings

    def connections (self):
        self.description_gauche.textChanged.connect(self.onChanges)
        self.comboBoxColorLeft.currentIndexChanged.connect(self.onChanges)
        self.description_droite.textChanged.connect(self.onChanges)
        self.comboBoxColorRight.currentIndexChanged.connect(self.onChanges)
        
    def onChanges(self):
        if self.sender()==self.description_gauche:
            self.groupe_left.changeDescription(self.description_gauche.text())
        elif self.sender()==self.description_gauche:
            self.groupe_left.changeDescription(self.description_gauche.text())
        elif self.sender()== self.comboBoxColorRight:
            self.groupe_right.changeColor(self.comboBoxColorRight.currentText().replace(" ", ""))
            self.right_page.setStyleSheet("#label_vignette_right{background-image: url(:/textures/" + self.groupe_right.attribs['color'] + ");}")
            self.title_droite.setStyleSheet("#title_droite{background-image: url(:/textures/"+self.groupe_right.attribs['color']+");}")
        elif self.sender()== self.comboBoxColorLeft :
            self.groupe_left.changeColor(self.comboBoxColorLeft.currentText().replace(" ", ""))
            self.left_page.setStyleSheet("#label_vignette_left{background-image: url(:/textures/"+ self.groupe_left.attribs['color'] + ");}")
            self.title_gauche.setStyleSheet("#title_gauche{background-image: url(:/textures/"+self.groupe_left.attribs['color']+");}")

    def updateContent (self):
        pass
    def setEnableEditableItems (self, enable):
        self.description_gauche.setEnabled(enable)
        self.description_droite.setEnabled(enable)    
        self.comboBoxColorLeft.setEnabled(enable)
        self.comboBoxColorRight.setEnabled(enable)
        
    def setTemple (self,temples_ids,left):
        if left == True:
            self.title_gauche.setText("Temples")
            self.current_page = 0
        else:
            self.title_droite.setText("Temples")
            self.current_page = 1
        self.nb_row = 0
        self.nb_col = 0
        for t in temples_ids:
            temple = self.model.getTempleById(t)
            if temple != None:
                self.addVignette(temple)
        
    def setLeftContent (self, groupe, sub_groupe=None):
        if sub_groupe != None : 
            self.groupe_left = sub_groupe
        else : 
            self.groupe_left = groupe
        self.left_page.setStyleSheet("#label_vignette_left{background-image: url(:/textures/"+ self.groupe_left.attribs['color'] + ");}")

        # self.left_page.setStyleSheet("#vignettes_gauche{background-image: url(:/textures/"+self.groupe_left.attribs['color']+");}")
        self.title_gauche.setText(groupe.name.replace("_"," "))
        self.title_gauche.setStyleSheet("#title_gauche{background-image: url(:/textures/"+self.groupe_left.attribs['color']+");}")
        self.description_gauche.setPlainText(self.groupe_left.attribs['description'])
        # self.description_gauche.setEnabled(False)
        self.nb_row = 0
        self.nb_col = 0
        self.current_page = 0
        if sub_groupe != None : 
            sub_groupe_name = QLabel(self.left_page)
            sub_groupe_name.setText(sub_groupe.name)
            sub_groupe_name.setAlignment(QtCore.Qt.AlignHCenter)
            font = self.title_gauche.font()
            self.verticalLayout.insertWidget(1, sub_groupe_name)
            font.setPointSize(font.pointSize() / 2.0)
            font.setStyle(QFont.StyleItalic)
            sub_groupe_name.setFont(font)
        self.comboBoxColorLeft.addItem("")
        
        for key, icon in zip(self.model.groupe_color_icons.keys(), self.model.groupe_color_icons.values()):
            self.comboBoxColorLeft.addItem(icon, key)       
            if key == groupe.attribs['color']:
                self.comboBoxColorLeft.setCurrentIndex(self.comboBoxColorLeft.count() - 1)
        # self.comboBoxColorLeft.setEnabled(False)
    def setRightContent (self, groupe, sub_groupe=None):
        if sub_groupe != None : 
            self.groupe_right = sub_groupe
        else : 
            self.groupe_right = groupe
        # self.right_page.setObjectName("vignette_droite"+groupe.name)
        print ('self.groupe_right.attribs[]', Config().instance.path_to_texture() + "/" + self.groupe_right.attribs['color'].strip())
        self.right_page.setStyleSheet("#label_vignette_right{background-image: url(:/textures/"+ self.groupe_right.attribs['color'] + ");}")
        
        # self.title_droite.setStyleSheet("#title_droite{background-image: url(:/textures/"+self.groupe_right.attribs['color']+");}")
        self.title_droite.setText(groupe.name.replace("_"," "))
        self.title_droite.setStyleSheet("#title_droite{background-image: url(:/textures/"+self.groupe_right.attribs['color']+");}")        
        self.description_droite.setPlainText(self.groupe_right.attribs['description'])
      # self.description_droite.setEnabled(False)
        self.current_page = 1
        self.nb_row = 0
        self.nb_col = 0    
        if sub_groupe != None : 
            sub_groupe_name = QLabel(self.right_page)
            sub_groupe_name.setText(sub_groupe.name)
            font = self.title_droite.font()
            self.verticalLayout_2.insertWidget(1, sub_groupe_name)
            font.setPointSize(font.pointSize() / 2.0)
            font.setStyle(QFont.StyleItalic)
            sub_groupe_name.setFont(font)
        self.comboBoxColorRight.addItem("")
        for key, icon in zip(self.model.groupe_color_icons.keys(), self.model.groupe_color_icons.values()):
            self.comboBoxColorRight.addItem(icon, key)
            if key == groupe.attribs['color']:
                self.comboBoxColorRight.setCurrentIndex(self.comboBoxColorRight.count() - 1)
      #  self.comboBoxColorRight.setEnabled(False)
        self.connections()        
    def addVignette (self, warrior):
        label_name = "label_vignette_left"
        if self.current_page == 0 : 
            widget_vignette = QWidget(self.vignettes_gauche)
        else:
            label_name = "label_vignette_right"
            widget_vignette = QWidget(self.vignettes_droite)        
        # widget_vignette.setObjectName("toto")
        # widget_vignette.setStyleSheet("#toto { background-color: rgb(170, 255, 0,0);}")
        layout_one_vignette = QVBoxLayout(widget_vignette)
        layout_one_vignette.setSpacing(0)
        layout_one_vignette.setContentsMargins(0, 0, 0, 0)
        if type(warrior)== Temple:
            warrior_button = TempleButton(self.model, warrior, widget_vignette)
        else:
            warrior_button = HerosButton(self.model, warrior, widget_vignette)
        warrior_button.connect()
        layout_one_vignette.setAlignment(QtCore.Qt.AlignCenter)
#         warrior_button.setStyleSheet("QPushButton { background-color: rgb(170, 255, 0);border-style: outset; border-width: 2px; border-color: beige;}")
        # warrior_button.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
        layout_one_vignette.addWidget(warrior_button)
        
        # label
        if (type(warrior)==Temple):
            warrior_label = TempleLabel(warrior, widget_vignette)
        else:
            warrior_label = HerosLabel(warrior, widget_vignette)
        warrior_label.connect()
        warrior_label.setObjectName(label_name)
        layout_one_vignette.addWidget(warrior_label)
        

#         warrior_button.setFixedSize(QSize(100,120))
        max_col = 3

#         groupe_name = warrior.groupe().name
#         if warrior.masterGroupe() != None : 
#             groupe_name = warrior.masterGroupe().name + "/" + groupe_name
        
 
        
        size_pic_height = warrior_button.size().height()
        size_pic_width = warrior_button.size().width()
        ratio_h = warrior.thumb.height() / size_pic_height
        ratio_v = warrior.thumb.width() / size_pic_width
        picture = warrior.thumb
        if ratio_h < ratio_v :
            if not warrior.thumb.isNull():
                picture = warrior.thumb.scaledToHeight(size_pic_height)
                diff = picture.width() - size_pic_width
                picture = picture.copy(diff / 2.0, 0, size_pic_width, size_pic_height)
        else:
            if not warrior.thumb.isNull():
                picture = warrior.thumb.scaledToWidth(size_pic_width)
                diff = picture.height() - size_pic_height
                picture = picture.copy(0, diff / 2.0, size_pic_width, size_pic_height)

        icon = QIcon(picture)
        warrior_button.setIcon(icon)
        warrior_button.setIconSize(QSize(picture.width() - 3, picture.height() - 3))

            

        if self.nb_col == 0:
            self.nb_row = self.nb_row + 1

        if self.current_page == 0 : 
            self.gridLayout.addWidget(widget_vignette, self.nb_row, self.nb_col)
        else:
            self.gridLayout_2.addWidget(widget_vignette, self.nb_row, self.nb_col)
        self.nb_col = (self.nb_col + 1) % max_col
#         for w in warriors : 
#             vignette
