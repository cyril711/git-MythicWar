from PyQt5.Qt import QTextEdit, QLayout, QPushButton, QLabel, QVBoxLayout,\
     QHBoxLayout, QDialog, QDockWidget, QPixmap, QWidget, QObject,\
    QXmlStreamReader, QSizePolicy, QIcon, QColor, QRect, QPainter, QPoint,\
    QBrush, QPolygonF, QPen, QPainterPath
from PyQt5 import QtCore, QtWidgets
     
from python_modules.View.ui_book_warrior_page import Ui_BookWarriorPage
from PyQt5.uic.Compiler.qtproxies import QtGui
import math

basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   


class RankWidget (QtWidgets.QWidget):
    def __init__ (self,parent):

        super(RankWidget, self).__init__(parent)    

    def paintEvent (self,event):    

        painter = QPainter(self)
        brush = QBrush ()#brush = QBrush ()
        #brush.setTexture(QPixmap("C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/background/gold.png"))
        texture = QPixmap("C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/background/gold.png")
        if texture.isNull():
            print ('pb gold texture')
#         starPolygon = QPolygonF ()
#         starPolygon.append(QtCore.QPointF(1.0, 0.5))
#         for i in range (5):
#             starPolygon.append(QtCore.QPointF(0.5 + 0.5 * math.cos(0.8 * i * 3.14),0.5 + 0.5 * math.sin(0.8 * i * 3.14)))
#         #painter.scale(20,20)
        painter.setPen(QtCore.Qt.NoPen)
        brush = QBrush (texture)
        painter.setBrush(brush)
        nb_stars = 5
        #painter.drawPolygon(starPolygon,QtCore.Qt.WindingFill)
#         for i in range (nb_stars):
#             painter.translate(2.0,0.0)
            #painter.drawPolygon(starPolygon)
        
        #starPath.moveTo(90, 50)
        for s in range (nb_stars):
            starPath = QPainterPath()
            starPath.moveTo(QtCore.QPointF(20,10))
            for  i in range (5):
                starPath.lineTo(10 + 10 * math.cos(0.8 * i * math.pi),10 + 10 * math.sin(0.8 * i * math.pi))
            starPath.closeSubpath()
            starPath.setFillRule(QtCore.Qt.WindingFill)
            painter.translate(QtCore.QPointF(30,0))
            painter.drawPath(starPath)
       # painter.setBrush(QtCore.Qt.NoBrush)

class ProfilHeroWidget (QtWidgets.QWidget):
        
    def __init__ (self,parent):

        super(ProfilHeroWidget, self).__init__(parent)
        #self.setGeometry(QRect(0,0,888999,8888))
    def setWarrior (self, warrior):
        self.warrior = warrior
    
    def paintEvent (self,event):

        groupe_name = self.warrior.groupe().name
        if self.warrior.masterGroupe() != None : 
            groupe_name = self.warrior.masterGroupe().name+"/"+groupe_name
        
        kingdom_name = self.warrior.kingdom().name
        empire_name = self.warrior.empire().name
        faction_name = self.warrior.faction().name
        picture = QPixmap(basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.warrior.name+"/portrait.jpg")
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
        self.ui.picture_layout.addWidget(profil_widget)
        kingdom_name = self.warrior.kingdom().name
        empire_name = self.warrior.empire().name
        faction_name = self.warrior.faction().name
        self.ui.label_faction.setText(faction_name)
        self.ui.label_empire.setText(empire_name)
        self.ui.label_royaume.setText(kingdom_name)
        self.ui.label_avancement.setText(str(self.warrior.kingdom().avancement()))
        rank_widget = RankWidget(self.ui.rank_widget)
        self.ui.layout_rank.addWidget(rank_widget)
        #self.profil_layout.insertWidget(0,profil_widget)
        self.connections ()
    def connections (self):
        self.ui.warrior_description.textChanged.connect(self.onModification)
        self.ui.warrior_techniques.textChanged.connect(self.onModification)
        
    def onModification (self):
        print ('modification')
        self.parent().modified.emit(self.warrior.id)
        
        
        
    def paintEvent(self, event):
        super(BookWarriorPage,self).paintEvent(event)