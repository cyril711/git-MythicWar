from PyQt5.Qt import QDialog, QPixmap, QWidget, QSize, QIcon, QColorDialog
from PyQt5 import  QtWidgets
     
from python_modules.view.view_kingdom.ui_book_world_main_page import Ui_BookWorldMainpage
from python_modules.config import Config
from python_modules.view.heros_vignette import HerosButton,HerosLabel
import os
#basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"
class BookWorldMainPage ( QWidget,Ui_BookWorldMainpage):
    def __init__ (self,model,parent=None):
        super(BookWorldMainPage,self).__init__(parent)
        self.setupUi(self)
        self.nb_col = 0
        self.nb_row = 0
        self.model = model
        self.settings = Config().instance.settings

    def connections (self):
        self.description_groupe.textChanged.connect(self.onModificationGroupe)
        self.comboBoxColor.currentIndexChanged.connect(self.onModificationGroupe)
        self.historyTextEdit.textChanged.connect(self.onModificationKingdom)
        self.descriptionTextEdit.textChanged.connect(self.onModificationKingdom)
        
    def onModificationGroupe(self):
        self.parent().parent().modifiedGroupe.emit(self.groupe)

    def onModificationKingdom(self):
        self.parent().parent().modifiedKingdom.emit(self.kingdom)        
        
    def onUpdateColorKingdom (self):
        dlg = QColorDialog(self.kingdom.color)
        dlg.setOption(QColorDialog.ShowAlphaChannel,True)
        if dlg.exec_() == QDialog.Accepted:
            self.kingdom.color = dlg.currentColor()
            #self.setStyleSheet("QPlainTextEdit{ border: 2px solid rgb("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+");background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.setStyleSheet("QPlainTextEdit{ background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.button_color.setStyleSheet("#button_color{background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.button_color.show()
        else:
            dlg.close()
    def setContent (self, kingdom):
        self.kingdom = kingdom
        faction_name = kingdom.parent.parent.name
        empire_name = kingdom.parent.name
        self.setStyleSheet("QPlainTextEdit{ border: 2px solid rgb("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+";)}")
        
        self.button_color.setStyleSheet("#button_color{background-color: rgba("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+","+str(kingdom.color.alpha())+");}")
        self.button_color.clicked.connect(self.onUpdateColorKingdom)
        self.land_picture.setPixmap(QPixmap(os.path.join(self.settings.value("global/resources_path"),faction_name,empire_name,kingdom.name,"Land.jpg")).scaledToHeight(200))
        self.army_picture.setPixmap(QPixmap(os.path.join(self.settings.value("global/resources_path"),faction_name,empire_name,kingdom.name,"Army.png")).scaledToHeight(200))        
        self.Title.setText( kingdom.name)
        self.historyTextEdit.appendPlainText(kingdom.attribs['armee'])
        self.historyTextEdit.setEnabled(False)
        self.descriptionTextEdit.appendPlainText(kingdom.attribs['description'])
        self.descriptionTextEdit.setEnabled(False)
        avancement = kingdom.avancement ()
        self.button_color.setText("( "+str(avancement)+" % ) ")
        self.connections()

    def setEnableEditableItems (self,enable):
        self.historyTextEdit.setEnabled(enable)
        self.descriptionTextEdit.setEnabled(enable)
        self.comboBoxColor.setEnabled(enable)
        
    def addVignette (self,warrior):
        widget_vignette = QtWidgets.QWidget(self.vignettes)
        layout_one_vignette = QtWidgets.QVBoxLayout(widget_vignette)
        layout_one_vignette.setSpacing(0)
        layout_one_vignette.setContentsMargins(0, 0, 0, 0)

        warrior_button = HerosButton(self.model,warrior,widget_vignette)
        warrior_button.connect()
        layout_one_vignette.addWidget(warrior_button)
        
        # label
        warrior_label = HerosLabel(warrior,widget_vignette)
        warrior_label.connect()
        layout_one_vignette.addWidget(warrior_label)

        max_col  = 3

  
        size_pic_height = warrior_button.size().height()
        size_pic_width = warrior_button.size().width()
        ratio_h = warrior.thumb.height() / size_pic_height
        ratio_v = warrior.thumb.width()/ size_pic_width
        picture = warrior.thumb
        if ratio_h < ratio_v :
            if not warrior.thumb.isNull():
                picture = warrior.thumb.scaledToHeight(size_pic_height)
                diff =  picture.width() - size_pic_width
                picture = picture.copy(diff/2.0,0,size_pic_width,size_pic_height)
        else:
            if not warrior.thumb.isNull():
                picture = warrior.thumb.scaledToWidth(size_pic_width)
                diff = picture.height() - size_pic_height
                picture = picture.copy(0,diff/2.0,size_pic_width,size_pic_height)

        icon = QIcon(picture)
        warrior_button.setIcon(icon)
        warrior_button.setIconSize(QSize(picture.width()-3,picture.height()-3))

        if self.nb_col == 0:
            self.nb_row = self.nb_row + 1

        self.gridLayout.addWidget(widget_vignette,self.nb_row,self.nb_col)
        self.nb_col = (self.nb_col +1)%max_col
#         for w in warriors : 
#             vignette

    def onColorGroupChanged (self,text):
        self.groupe.attribs['color'] = self.comboBoxColor.currentText().replace(" ","")
        self.right_page.setStyleSheet("#vignettes{background-image: url(:/textures/"+self.groupe.attribs['color']+");}")
        self.onModificationKingdom()
    def setContentRightPage (self,groupe,sub_groupe=None):
        if sub_groupe != None : 
            self.groupe= sub_groupe
        else : 
            self.groupe= groupe
        self.comboBoxColor.addItem("")
        for key,icon in zip(self.model.groupe_color_icons.keys(),self.model.groupe_color_icons.values()):
            self.comboBoxColor.addItem(icon,key)
            if key == groupe.attribs['color']:
                self.comboBoxColor.setCurrentIndex(self.comboBoxColor.count()-1)
        self.right_page.setStyleSheet("#vignettes{background-image: url(:/textures/"+self.groupe.attribs['color']+");}")
        self.groupe_name.setText( groupe.name)
        self.comboBoxColor.currentTextChanged.connect (self.onColorGroupChanged)
        self.description_groupe.appendPlainText(self.groupe.attribs['description'])
        if sub_groupe != None : 
            sub_groupe_name = QtWidgets.QLabel(self.description_groupe.parent())
            font = self.description_groupe.font()
            font.setPointSize(font.pointSize()-4)
            sub_groupe_name.setFont(font)
            
            
            
            