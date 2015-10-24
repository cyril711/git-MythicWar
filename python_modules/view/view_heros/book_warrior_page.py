from PyQt5.Qt import QPixmap, QWidget,QColor, QRect, QPainter, QPoint,QBrush, QPainterPath,\
    QPushButton, QSize, QIcon, QPalette, QImage, QListWidgetItem, QLabel,\
    QGridLayout, QSizePolicy, QToolTip
from PyQt5 import QtCore, QtWidgets
     
from python_modules.view.view_heros.ui_book_warrior_page import Ui_BookWarriorPage
from python_modules.view.view_heros.ui_book_warrior_page_reverse import Ui_BookWarriorPageReverse

import math
from python_modules.config import Config
import os
from python_modules.view.view_book.page_widget import PageWidget
#basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   



class ImagePopup(QLabel):
    """
    The ImagePopup class is a QLabel that displays a popup, zoomed image
    on top of another label.
    """
    def __init__(self, parent):
        super(QLabel, self).__init__(parent)

        # set pixmap and size, which is the double of the original pixmap
        thumb = parent.pixmap()
        imageSize = thumb.size()
        factor = 126/imageSize.width()
        #factor = 0.5
        imageSize.setWidth(imageSize.width()*factor)
        imageSize.setHeight(imageSize.height()*factor)
        self.setPixmap(thumb.scaled(imageSize,QtCore.Qt.KeepAspectRatioByExpanding))

        # center the zoomed image on the thumb
        position = self.cursor().pos()
        position.setX(position.x() - thumb.size().width()*factor)
        position.setY(position.y() - thumb.size().height()*factor)
        self.move(position)

        # FramelessWindowHint may not work on some window managers on Linux
        # so I force also the flag X11BypassWindowManagerHint
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.WindowStaysOnTopHint
                            | QtCore.Qt.FramelessWindowHint
                            | QtCore.Qt.X11BypassWindowManagerHint)

    def leaveEvent(self, event):
        """ When the mouse leave this widget, destroy it. """
        self.destroy()


class ImageLabel(QLabel):
    """ This widget displays an ImagePopup when the mouse enters its region """
    def __init__(self, parent,path_pic):
        super(QLabel, self).__init__(parent)
        self.p = None
        #self.setStyleSheet("#QToolTip { color: #ff0000; background-color: #ff0000;}")
        self.path_pic = path_pic
    def enterEvent(self, event): 
        print ('enter event label')
        #self.p = ImagePopup(self)
        #self.p.show()

        self.setToolTip('<span style="background-color:red;"><img src="'+self.path_pic+'"width="420"></span>')

        event.accept()
    def paintEvent(self,event): 
        painter = QPainter(self)
        if self.pixmap().width()!= 0:
            factor_w = 100/self.pixmap().width()
            factor_h = 123/self.pixmap().height()
            painter.scale(factor_w,factor_h)
            painter.drawPixmap(QRect(0,0,self.pixmap().width(),self.pixmap().height()),self.pixmap(),QRect(0,0,self.pixmap().width(),self.pixmap().height()))
#     def leaveEvent(self, event):
#         if self.p != None :
#             self.p.destroy()
        


class ProfilHeroWidget (QPushButton):
        
    def __init__ (self,picture,parent):

        super(ProfilHeroWidget, self).__init__(parent)
        if picture.width()> picture.height() :
            self.setFixedSize(QSize(500,500*2.0/3.0))
        else:
            self.setFixedSize(QSize(500*2.0/3.0,500))
        size_pic_height = self.height()-20
        size_pic_width = self.width()-20
        ratio_h = picture.height() / size_pic_height
        ratio_v = picture.width()/ size_pic_width
        if ratio_h < ratio_v :
            #self.setFixedSize(QSize(500,500*2.0/3.0))
            if not picture.isNull():
                picture = picture.scaledToHeight(size_pic_height)
                diff =  picture.width() - size_pic_width
                picture = picture.copy(diff/2.0,0,size_pic_width,size_pic_height)
        else:
            #self.setFixedSize(QSize(500*2.0/3.0,500))
            if not picture.isNull():
                picture = picture.scaledToWidth(size_pic_width)
                diff = picture.height() - size_pic_height
                picture = picture.copy(0,diff/2.0,size_pic_width,size_pic_height)            
        
        icon = QIcon(picture)
        self.setIcon(icon)
        self.setIconSize(self.size())
#     def paintEvent (self,event):
# 
#         groupe_name = self.warrior.groupe().name
#         if self.warrior.masterGroupe() != None : 
#             groupe_name = self.warrior.masterGroupe().name+"/"+groupe_name
#         
#         kingdom_name = self.warrior.kingdom().name
#         empire_name = self.warrior.empire().name
#         faction_name = self.warrior.faction().name
#         picture = QPixmap(self.settings.value("global/resources_path")+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.warrior.name+"/portrait.jpg")
#         #print (basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.warrior.name+"/portrait.jpg")
#         if picture.isNull():
#             print ('iiiiiiiiiiiiiiks')
#         
#         size_h = 500*2/3
#         size_v = 500
#         self.invert = False
#         if picture.width()> picture.height():
#             size_h,size_v = size_v,size_h
#             self.invert = True
#         painter = QPainter(self)
#         brush = QBrush ()
#         try :
#             groupe_color = self.warrior.groupe().attribs['color']
#             groupe_color = "saphir"
#             if self.warrior.masterGroupe() != None : 
#                 groupe_color = self.warrior.masterGroupe().attribs['color']
#             pixmap = QPixmap(":/textures/"+groupe_color)
#             if pixmap.isNull():
#                 print ('blue est nll')
#         #painter.drawPixmap(QPoint(0,0),pixmap.copy(QRect(0,0,size_h,size_v)))
#             brush = QBrush(pixmap.copy(QRect(0,0,size_h,size_v)))
#             painter.setBrush(brush)
#         except : 
#             pass
#         painter.drawRoundedRect(QRect(0,0,size_h,size_v), 5, 5)
# 
# 
#         
#         size_pic_height = size_v-40
#         size_pic_width = size_h-40
#         ratio_h = picture.height() / size_pic_height
#         ratio_v = picture.width()/ size_pic_width
#         if ratio_h < ratio_v :
#             if not picture.isNull():
#                 picture = picture.scaledToHeight(size_pic_height)
#                 diff =  picture.width() - size_pic_width
#                 picture = picture.copy(diff/2.0,0,size_pic_width,size_pic_height)
#         else:
#             if not picture.isNull():
#                 picture = picture.scaledToWidth(size_pic_width)
#                 diff = picture.height() - size_pic_height
#                 picture = picture.copy(0,diff/2.0,size_pic_width,size_pic_height)            
#         painter.drawPixmap(QPoint(20,20),picture)
#         brush = QBrush (QColor(0,255,255))
#         painter.setBrush(brush)
#         for i in range (10):
#             painter.drawRect(QRect(size_h+10,size_v - ((i+1)*10),10,10))
#         #painter.setBrush (QtCore.Qt.NoBrush)
      
        

class BookWarriorPage ( QWidget):

    def __init__ (self,model,parent=None,warrior=None):
        super(BookWarriorPage,self).__init__(parent)
#         self.setObjectName("BookWarriorPage")
        self.warrior = warrior
        self.model = model

        groupe_name = warrior.groupe().name
        if warrior.masterGroupe() != None : 
            groupe_name = warrior.masterGroupe().name+"/"+groupe_name
         
        kingdom_name = warrior.kingdom().name
        empire_name = warrior.empire().name
        faction_name = warrior.faction().name
        path = os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom_name,'Picture',groupe_name,warrior.name)
        picture = QPixmap(path+"/portrait.jpg")
        print ("book warrior page pic path :",path)
        print ('picture size',picture.height(),picture.width())
        if picture.height() < picture.width():
            self.ui = Ui_BookWarriorPageReverse()
        else: 
            self.ui = Ui_BookWarriorPage()

        self.ui.setupUi(self)

   
        self.ui.warrior_name.setText(self.warrior.name.replace("_"," "))
        self.ui.warrior_name.setObjectName("Warrior_name")
        couleur = self.warrior.groupe().attribs['color']
        if self.warrior.masterGroupe() != None : 
            couleur = self.warrior.masterGroupe().attribs['color']
        #print ('couleur',couleur)

       # self.setStyleSheet("#Warrior_name{background-image: url(:/textures/"+couleur+")}")

#         try : 
#             self.ui.warrior_description.setPlainText(self.warrior.attribs['description'])
#             self.ui.warrior_techniques.setPlainText(self.warrior.attribs['techniques'])
#         except KeyError : 
#             pass
        profil_widget = ProfilHeroWidget(picture,self.ui.picture_widget)
        #profil_widget.setPicture(picture)
        self.ui.picture_layout_2.addWidget(profil_widget)
        if picture.height() >= picture.width():
            separator = QtWidgets.QWidget(self.ui.picture_widget)
            separator.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.ui.picture_layout_2.addWidget(separator)


        self.ui.progressBar_HP.setStyleSheet("  QProgressBar {border-radius: 5px;} QProgressBar::chunk {     background-color: #05B8CC;width: 20px;}")
        self.ui.progressBar_HP.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.progressBar_MP.setStyleSheet("  QProgressBar {border-radius: 5px;} QProgressBar::chunk {     background-color: #05B8CC;width: 20px;}")
        self.ui.progressBar_MP.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.profil_completion_button.setIcon(QIcon(":/icons/128x128/state_"+str(self.warrior.attribs['complete']+1)))
        self.ui.profil_completion_button.setStyleSheet("#"+self.ui.profil_completion_button.objectName()+"{background-color:transparent;}")
        self.ui.profil_completion_button.clicked.connect(self.onChangeCompletion)
 #       self.ui.progressBar_MP.setStyleSheet(" QProgressBar::chunk {background-color: blue; }")
       # self.ui.progressBar_HP.setStyleSheet(" QProgressBar {background-color: #green; };QProgressBar::chunk {background-color: #red; }")
        #self.ui.label_avancement.setText(str(self.warrior.kingdom().avancement()))

        try:
            hp_percent = float(self.warrior.attribs['HP'] / self.warrior.attribs['HP_max'])* 100
            mp_percent = float(self.warrior.attribs['MP'] / self.warrior.attribs['MP_max'])* 100
        except (ZeroDivisionError,KeyError) as e :
            hp_percent =0
            mp_percent =0
        self.ui.progressBar_HP.setValue(int(hp_percent))
        self.ui.progressBar_MP.setValue(int(mp_percent))
        #rank_widget = RankWidget(warrior,self.ui.rank_widget)
        #self.ui.layout_rank.addWidget(rank_widget)

        self.ui.big_star.clicked.connect(self.onRankChanged)
        self.ui.big_star.setStyleSheet("#"+self.ui.big_star.objectName()+"{border-width: 0px;background-color:transparent;}")
        self.l_stars = []
        self.l_stars.append(self.ui.star_1)
        self.l_stars.append(self.ui.star_2)
        self.l_stars.append(self.ui.star_3)
        self.l_stars.append(self.ui.star_4)
        self.l_stars.append(self.ui.star_5) 
        for w in self.l_stars:
            w.setStyleSheet("#"+w.objectName()+"{border-width: 0px;background-color:transparent;}")
            w.clicked.connect(self.onRankChanged)
        print ('init book warrior page',self.warrior.attribs["rank"])
        self.updateRank(self.warrior.attribs["rank"]) 

        #self.profil_layout.insertWidget(0,profil_widget)
        
        groupe_name = self.warrior.groupe().name
        print ('groupe.name',groupe_name)
        if self.warrior.masterGroupe() != None : 
            groupe_name = self.warrior.masterGroupe().name+"/"+groupe_name
        path_warrior = os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom_name,'Picture',groupe_name,self.warrior.name)
        
        self.ui.groupe_texture_button.setText(groupe_name.replace("_"," "))
        self.ui.groupe_texture_button.clicked.connect(self.onGroupClicked)
        groupe_color = self.warrior.groupe().attribs['color']
        if self.warrior.masterGroupe() != None : 
            groupe_color = self.warrior.masterGroupe().attribs['color']

        self.ui.groupe_texture_button.setStyleSheet("#"+self.ui.groupe_texture_button.objectName()+"{background-image:url(:/textures/"+groupe_color+");}")
        #self.ui.groupe_texture_button.setStyleSheet("#"+self.ui.groupe_texture_button.objectName()+"{background-image: url("+Config().instance.path_to_texture()+"/"+groupe_color+".jpg)0 0 0 0 stretch stretch ;color:white}")
        #self.ui.groupe_texture_button.setFlat(True)
        #self.ui.groupe_texture_button.setAutoFillBackground(True)
        path = os.path.join(Config().instance.path_to_icons(),"faction","32x32",self.warrior.faction().name)
        self.ui.iconFaction.setIcon(QIcon(path))
        self.ui.iconFaction.setToolTip(self.warrior.faction().name)
        path = os.path.join(Config().instance.path_to_icons(),"empire","32x32",self.warrior.empire().name)
        self.ui.iconEmpire.setIcon(QIcon(path))
        self.ui.iconEmpire.setToolTip(self.warrior.empire().name)
        self.ui.iconEmpire.clicked.connect(self.onEmpireClicked)
        path = os.path.join(Config().instance.path_to_icons(),"kingdom","32x32",self.warrior.kingdom().name)
        self.ui.iconKingdom.setIcon(QIcon(path))
        self.ui.iconKingdom.setToolTip(self.warrior.kingdom().name)
        self.ui.iconKingdom.clicked.connect(self.onKingdomClicked)
        path = os.path.join(Config().instance.path_to_icons(),"actions",self.warrior.attribs['status'])
        print ('path icon ',path)
        self.ui.iconState.setPixmap(QPixmap(path).scaledToHeight(64))
        
        self.ui.iconState.setToolTip(self.warrior.attribs['status'])
        filename= os.path.join(path_warrior,"description.html")
        if (os.path.exists(filename)):
            self.description_widget = PageWidget(filename,self.ui.right_page)
            #self.ui.right_page_layout.addWidget(self.description_widget)
            self.ui.right_page_layout.insertWidget(1,self.description_widget)


        list_pic = list(filter(self.isValid,os.listdir (path_warrior)))
        nb_row = 0
        nb_col = 0
        max_col = 4
        for pic in list_pic : 
            pic_widget = ImageLabel(self,os.path.join(path_warrior,pic))
            print(pic)
            pic_widget.setPixmap(QPixmap(os.path.join(path_warrior,pic)))
            self.ui.gridLayout.addWidget(pic_widget, nb_row, nb_col)
            nb_col = (nb_col +1)%max_col
            if nb_col == 0 :
                nb_row+=1
#             #item = QListWidgetItem()
#             item = ImageLabel()
#             item.setPixmap(QPixmap(os.path.join(path_warrior,pic)))
#             self.ui.gallery.addItem(item)
        self.ui.map_button.clicked.connect(self.onMapClicked)

        self.connections ()
        
    def onMapClicked (self):
        self.model.clearSelection()
        self.warrior.setSelected(True,True)
        self.model.askForMap.emit(self.warrior.attribs['latitude'],self.warrior.attribs['longitude'])
    def onGroupClicked (self):
        self.model.askForGroup.emit(self.warrior.groupe())
    def onKingdomClicked (self):
        self.model.askForKingdomPage.emit(self.warrior.kingdom())
    def onEmpireClicked (self):
        self.model.askForKingdomHomePage.emit(self.warrior.empire())
    def isValid (self, name):
        return (name != "portrait.jpg" and name!="portrait_thumbnail.jpg" and name!= "description.html")
    
    def onRankChanged (self):
        print ('onRankChanged')
        if self.sender().objectName()== "big_star":
            new_rank = 5
        elif (self.warrior.attribs['rank']==5) and (int(self.sender().objectName().split("_")[1])==self.warrior.attribs['rank']):
            new_rank = 6
        else:
            new_rank = int(self.sender().objectName().split("_")[1])
        self.warrior.changeRank(new_rank)
        print ('new rank',new_rank)
        self.updateRank(new_rank)
    def updateRank(self,rank):
        print ('update rank',rank)
        pal = QPalette(self.ui.rank_text.palette())
        image = QImage(os.path.join(Config().instance.path_to_icons(),"rank")+"/star_"+self.warrior.groupe().attribs["color"]+".png")
        value = image.pixel(image.width()/2.0,image.height()/2.0)
        pal.setColor(QPalette.WindowText, QColor(value))
        self.ui.rank_text.setPalette(pal)
        self.ui.rank_text.setText(str(rank))
        if rank== 6 :
            self.ui.rank_widget_layout.removeWidget(self.ui.rank_text)
            for star in self.l_stars :
                self.ui.rank_widget_layout.removeWidget(star)
                star.setParent(None)
                self.ui.rank_text.setParent(None)
            self.ui.rank_widget_layout.addWidget(self.ui.big_star)
            self.ui.rank_widget_layout.addWidget(self.ui.rank_text)    
            self.ui.big_star.setIcon(QIcon(os.path.join(Config().instance.path_to_icons(),"rank")+"/big/star_"+self.warrior.groupe().attribs["color"]+".png"))
        else:
            self.ui.rank_widget_layout.removeWidget(self.ui.big_star)
            self.ui.rank_widget_layout.removeWidget(self.ui.rank_text)
            self.ui.big_star.setParent(None)
            for star in self.l_stars :
                self.ui.rank_widget_layout.addWidget(star)    
            self.ui.rank_widget_layout.addWidget(self.ui.rank_text)
        for i in range (len(self.l_stars)) :
            if i < rank:
                self.l_stars[i].setIcon(QIcon(os.path.join(Config().instance.path_to_icons(),"rank")+"/star_"+self.warrior.groupe().attribs["color"]+".png"))
            else:
                self.l_stars[i].setIcon(QIcon(os.path.join(Config().instance.path_to_icons(),"rank")+"/star_white.png"))                

    def connections (self):
        pass
#         self.ui.warrior_description.textChanged.connect(self.onModification)
#         self.ui.warrior_techniques.textChanged.connect(self.onModification)
    def onChangeCompletion (self):
        self.warrior.attribs['complete'] = (self.warrior.attribs['complete']+1)%3 
        self.ui.profil_completion_button.setIcon(QIcon(":/icons/128x128/state_"+str(self.warrior.attribs['complete']+1)))
    def mousePressEvent(self, event):
        print ('q')
        return super(BookWarriorPage,self).mouseMoveEvent(event)
        

        
        
    def paintEvent(self, event):
        super(BookWarriorPage,self).paintEvent(event)