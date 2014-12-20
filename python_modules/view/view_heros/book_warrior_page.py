from PyQt5.Qt import QPixmap, QWidget,QColor, QRect, QPainter, QPoint,QBrush, QPainterPath
from PyQt5 import QtCore, QtWidgets
     
from python_modules.view.view_heros.ui_book_warrior_page import Ui_BookWarriorPage

import math
from python_modules.config import Config
#basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   


class RankWidget (QtWidgets.QWidget):
    def __init__ (self,warrior,parent):
        super(RankWidget, self).__init__(parent)    
        self.texture = QPixmap()
        self.stars = []
        self.warrior = warrior
        self.initialized = False
        self.rank = 4#self.warrior.attribs['rank']
        self.setMouseTracking(True)



        self.updateGeom()

    def updateGeom (self):

        
        if self.rank == 5 : 
            self.texture = QColor("yellow")
        elif self.rank == 4 : 
            self.texture = QColor("blue")
        elif self.rank == 3 : 
            self.texture = QColor("green")
        elif self.rank == 2 : 
            self.texture = QColor("red")
        elif self.rank == 1 : 
            self.texture = QColor("gray")

        self.initialized = True

    def paintEvent (self,event):    
        if self.initialized == True : 
            painter = QPainter(self)
           
            #painter.setPen(QtCore.Qt.NoPen)
            brush = QBrush (self.texture)
            nb_stars = 5
    
            for s in range (nb_stars):
                starPath = QPainterPath()
                starPath.moveTo(QtCore.QPointF(20,10))
                for  i in range (5):
                    starPath.lineTo(10 + 10 * math.cos(0.8 * i * math.pi),10 + 10 * math.sin(0.8 * i * math.pi))
                starPath.closeSubpath()
                starPath.setFillRule(QtCore.Qt.WindingFill)
                painter.translate(QtCore.QPointF(20,0))
                if (nb_stars-s) > self.rank :
                    print ('i no',self.rank)
                    painter.setBrush(QtCore.Qt.NoBrush)
                else:
                    print ('yes')
                    painter.setBrush(brush)
                painter.drawPath(starPath)
                self.stars.append(starPath)
           # painter.setBrush(QtCore.Qt.NoBrush)
    def mouseMoveEvent(self,event):
        print ('oooot')
        for i in range (len(self.stars)):
            if (5-i) > 2:#self.warrior.attribs['rank']:
                if self.stars[i].contains(event.pos):
                    print ('event pos',event.pos)
                    self.rank = i
                    self.updateGeom()
        

        
        

class ProfilHeroWidget (QtWidgets.QWidget):
        
    def __init__ (self,parent):

        super(ProfilHeroWidget, self).__init__(parent)
        self.settings = Config().instance.settings
        
    def setWarrior (self, warrior):
        self.warrior = warrior
    
    def paintEvent (self,event):

        groupe_name = self.warrior.groupe().name
        if self.warrior.masterGroupe() != None : 
            groupe_name = self.warrior.masterGroupe().name+"/"+groupe_name
        
        kingdom_name = self.warrior.kingdom().name
        empire_name = self.warrior.empire().name
        faction_name = self.warrior.faction().name
        picture = QPixmap(self.settings.value("global/resources_path")+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.warrior.name+"/portrait.jpg")
        #print (basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.warrior.name+"/portrait.jpg")
        if picture.isNull():
            print ('iiiiiiiiiiiiiiks')
        
        size_h = 500*2/3
        size_v = 500
        self.invert = False
        if picture.width()> picture.height():
            size_h,size_v = size_v,size_h
            self.invert = True
        painter = QPainter(self)
        brush = QBrush ()
        try :
            groupe_color = self.warrior.groupe().attribs['color']
            groupe_color = "saphir"
            if self.warrior.masterGroupe() != None : 
                groupe_color = self.warrior.masterGroupe().attribs['color']
            pixmap = QPixmap(":/textures/"+groupe_color)
            if pixmap.isNull():
                print ('blue est nll')
        #painter.drawPixmap(QPoint(0,0),pixmap.copy(QRect(0,0,size_h,size_v)))
            brush = QBrush(pixmap.copy(QRect(0,0,size_h,size_v)))
            painter.setBrush(brush)
        except : 
            pass
        painter.drawRoundedRect(QRect(0,0,size_h,size_v), 5, 5)


        
        size_pic_height = size_v-40
        size_pic_width = size_h-40
        ratio_h = picture.height() / size_pic_height
        ratio_v = picture.width()/ size_pic_width
        if ratio_h < ratio_v :
            if not picture.isNull():
                picture = picture.scaledToHeight(size_pic_height)
                diff =  picture.width() - size_pic_width
                picture = picture.copy(diff/2.0,0,size_pic_width,size_pic_height)
        else:
            if not picture.isNull():
                picture = picture.scaledToWidth(size_pic_width)
                diff = picture.height() - size_pic_height
                picture = picture.copy(0,diff/2.0,size_pic_width,size_pic_height)            
        painter.drawPixmap(QPoint(20,20),picture)
        brush = QBrush (QColor(0,255,255))
        painter.setBrush(brush)
        for i in range (10):
            painter.drawRect(QRect(size_h+10,size_v - ((i+1)*10),10,10))
        #painter.setBrush (QtCore.Qt.NoBrush)
      
        

class BookWarriorPage ( QWidget):

    def __init__ (self,parent=None,warrior=None):
        super(BookWarriorPage,self).__init__(parent)
#         self.setObjectName("BookWarriorPage")
        self.warrior = warrior
        self.settings = Config().instance.settings
        self.ui = Ui_BookWarriorPage()


        self.ui.setupUi(self)
        couleur = "saphir"    

        
        self.setEnabled(False)
   
        self.ui.warrior_name.setText(self.warrior.name.replace("_"," "))
        self.ui.warrior_name.setObjectName("Warrior_name")
        couleur = self.warrior.groupe().attribs['color']
        if self.warrior.masterGroupe() != None : 
            couleur = self.warrior.masterGroupe().attribs['color']
        print ('couleur',couleur)

        self.setStyleSheet("#Warrior_name{background-image: url(:/textures/"+couleur+")}")

        try : 
            self.ui.warrior_description.setPlainText(self.warrior.attribs['description'])
            self.ui.warrior_techniques.setPlainText(self.warrior.attribs['techniques'])
        except KeyError : 
            pass
        profil_widget = ProfilHeroWidget(self.ui.picture_widget)
        profil_widget.setWarrior(self.warrior)
        self.ui.picture_layout_2.addWidget(profil_widget)
        kingdom_name = self.warrior.kingdom().name
        empire_name = self.warrior.empire().name
        faction_name = self.warrior.faction().name
        self.ui.label_faction.setText(faction_name)
        self.ui.label_empire.setText(empire_name)
        self.ui.label_royaume.setText(kingdom_name)
        self.ui.progressBar_HP.setStyleSheet("  QProgressBar {border-radius: 5px;} QProgressBar::chunk {     background-color: #05B8CC;width: 20px;}")
 #       self.ui.progressBar_MP.setStyleSheet(" QProgressBar::chunk {background-color: blue; }")
       # self.ui.progressBar_HP.setStyleSheet(" QProgressBar {background-color: #green; };QProgressBar::chunk {background-color: #red; }")
        #self.ui.label_avancement.setText(str(self.warrior.kingdom().avancement()))
        self.ui.progressBar_HP.setAlignment(QtCore.Qt.AlignCenter)
        hp_percent = float(self.warrior.attribs['HP'] / self.warrior.attribs['HP_max'])* 100
        mp_percent = float(self.warrior.attribs['MP'] / self.warrior.attribs['MP_max'])* 100
        self.ui.progressBar_HP.setValue(int(hp_percent))
        self.ui.progressBar_MP.setValue(int(mp_percent))
        rank_widget = RankWidget(warrior,self.ui.rank_widget)
        self.ui.layout_rank.addWidget(rank_widget)
        #self.profil_layout.insertWidget(0,profil_widget)
        self.connections ()
    def connections (self):
        self.ui.warrior_description.textChanged.connect(self.onModification)
        self.ui.warrior_techniques.textChanged.connect(self.onModification)
        
    def mousePressEvent(self, event):
        print ('q')
        return super(BookWarriorPage,self).mouseMoveEvent(event)
        
    def onModification (self):
        print ('modification')
        self.parent().modified.emit(self.warrior.id)
        
        
        
    def paintEvent(self, event):
        super(BookWarriorPage,self).paintEvent(event)