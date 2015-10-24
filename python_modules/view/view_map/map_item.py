from PyQt5.QtWidgets import  QFrame
from PyQt5.Qt import QColor, QRectF, QPen, QBrush,\
    QAction, QMenu, QPainterPath, QPointF, QPoint, QLinearGradient, QVBoxLayout,\
    QGraphicsItem, QLabel, QPixmap, QTimer, QTextStream, QApplication,\
    QRadialGradient, QGraphicsColorizeEffect, QPolygon, qDebug, QSize,\
    QGraphicsLineItem
from PyQt5 import QtGui, QtCore
from python_modules.view.view_map.temple_view import TempleView
from PyQt5 import QtWidgets
from python_modules.config import Config
from enum import Enum

import os
from python_modules.model.actions import ActionMoveToPosition
class ColorMode (Enum):
    Empire = 1
    Kingdom = 2
    Groupe = 3
    Faction = 4


class TempleItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    def __init__(self,view, scene_coord,temple,size,parent=None):
        super (TempleItem,self).__init__(parent)
        #self.polygon  = self.getTriangle (size)
        self.rotation = 0.0
        self.color = QColor(0,0,125)
        self.name_visible = True
        self.name = temple.name
        self.model = temple
        self.view = view
        self.size = QSize(32,32)
        self.scene_coord = scene_coord
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
#     self.graphics_effect = QGraphicsColorizeEffect()
#     color = self.model.kingdom().color
#     self.graphics_effect.setColor(QColor(color.red(),color.green(),color.blue(),125))
#     self.setGraphicsEffect(self.graphics_effect )
#     self.graphics_effect.setEnabled(True)


        
        
    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size.width(),self.size.height())
        



    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged :
            self.model.position = value
            #pos = self.view.mapToScene(value.x(),value.y())
            lat,lon = self.scene_coord.SceneToLatLon(value.x(),value.y())
            self.model.changePosition (lat,lon)
            print ('new position ',self.model.position)
        else:
            return QGraphicsItem.itemChange(self,change,value)
    def paint (self,painter,option, widget):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.rotate(self.rotation)
        painter.translate(-16,-16) # taille fixe correspondant a la pixmap utilisee pour generer la geometry
        painter.scale(1.5,1.5)

        
        if self.isSelected() == True : 
            pen = QPen(QtCore.Qt.red)
            pen.setWidth(1)
        else:
            pen = QPen(QtCore.Qt.black)   
            pen.setWidth(1)
        painter.setPen(pen)
        radialGradient = QRadialGradient(self.size.width()/2, self.size.height()/2,self.size.width()*0.8, self.size.width(), self.size.height())
        radialGradient.setColorAt(0.0, QtCore.Qt.white)
        #radialGradient.setColorAt(0.2, self.heros.kingdom().color)
        if self.view.color_mode == ColorMode.Empire : 
            color = self.model.empire().color
        else :
            color = self.model.kingdom().color
        

        radialGradient.setColorAt(0.2, color)
        radialGradient.setColorAt(1.0, QtCore.Qt.black)
        painter.setBrush(QBrush(radialGradient))
        #brush = QBrush(self.color)
        #painter.setBrush(brush)
        geometry = self.model.empire().geometry
        #qDebug("info : map_item Temple : nombre de polygones %d"%len(geometry['polygon']))
        for p in geometry['polygon']:
            painter.drawPolygon(QPolygon(p))
#         
#         painter.drawPolygon(self.polygon)
#         path = os.path.join(Config().instance.path_to_icons(),'kingdom','32x32')
#         path+="/temple_artemis.png"
#         print ('path icon',path)
#         pix = QPixmap(path)
# 
#         painter.drawPixmap(-pix.width()/2.0,-pix.height()/2.0,pix)
        if self.name_visible == True :
            painter.setPen(QPen(QColor('black')))
            painter.translate(0,10)
            painter.drawText (self.boundingRect(),QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom, self.name)

    def contextMenuEvent(self, event):
        menu = QMenu()
        testAction = QAction('Go Inside', None)
        testAction.triggered.connect(self.showTempleView)
        menu.addAction(testAction)
        menu.exec_(event.screenPos())
        event.accept()
    def showTempleView (self):
        self.frame = QFrame()
        self.frame.setWindowTitle(self.kingdom.name)
        self.frame.setObjectName("Frame")
        self.frame.resize(400, 300)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view = TempleView(self.frame)
        self.view.setTemple(self.kingdom)
        self.verticalLayout.addWidget(self.view)
        self.frame.show()


class ActionsItem (QtWidgets.QGraphicsItem):

    def __init__(self,view,actions,scene_coord,parent=None):
        super (ActionsItem,self).__init__(parent)
        self.rotation = 0.0
        self.color = QColor(125,125,125)
        self.scene_coord = scene_coord
        self.liste_actions = actions
        self.view = view
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        
        
    def boundingRect(self):
        return self.view.sceneRect()

    
        

    def paint (self,painter,option, widget):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        pen = QPen(self.color)
        pen.setWidth(2)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)

        for action in self.liste_actions.values() :
            if action.isActive():
                if type(action) == ActionMoveToPosition:
                    i = 0
                    for heros in action.list_left:
                        start_x, start_y = self.scene_coord.LatLonToScene(heros.attribs['latitude'], heros.attribs['longitude'])
                        destination = action.list_right[i]
                        end_x,end_y = self.scene_coord.LatLonToScene(destination.x(), destination.y())
                        i = (i +1)%len(action.list_right)
    
                        self.setPos(QPointF(start_x,start_y))
                        dest = self.view.mapFromScene(QPoint(end_x,end_y))
                        str =  self.view.mapFromScene(QPoint(start_x,start_y))
    
                        dest = dest-str
                        painter.drawLine(QPointF(0,0),dest)
                        #painter.drawRect(0,0,1000,1000)
             #           print ('ooo',start_x,start_y,end_x,end_y)


class HerosItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    on_action = QtCore.pyqtSignal()
    def __init__(self,view,model,warrior,size,scene_coord,parent=None):
        super (HerosItem,self).__init__(parent)
        self.settings = Config().instance.settings
        self.heros = warrior
        self.model = model
        self.view = view
        self.scene_coord = scene_coord
        self.heros.on_move.connect(self.updatePos)

        self.rotation = 0.0
        self.size = size
        self.color = QColor(125,125,125)
        self.name_visible = True
        self.name = warrior.name
        self.iconShape = 0
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        #self.setFlag(QGraphicsItem.ItemIsMovable)
        #if warrior.selected == True : 
        self.setSelected(warrior.selected)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents (True)
        self.framePicture = None


    def getTriangle (self,size):
        pts = []
        pts.append(QtCore.QPointF(-size,size))
        pts.append(QtCore.QPointF(0,-2*size))
        pts.append(QtCore.QPointF(size,size))
        return QtGui.QPolygonF(pts)

    def showPicture (self):
        self.model.askForProfil.emit(self.heros)

    def updatePos(self):
        #print ('update pos',self.heros.attribs['place'] )
        if int(self.heros.attribs['place']) == 0:
            lat = self.heros.attribs['latitude']
            lon = self.heros.attribs['longitude']
   
            mx,my = self.scene_coord.LatLonToScene(lat,lon)
            self.setPos(mx,my)

    def itemChange (self, change,value):
        if change == QGraphicsItem.ItemSelectedChange :
            self.heros.setSelected(value,self.view.first_selection)
    #    return super(HerosItem,self).itemChange(change,value) 
        #if (change == QGraphicsItem.ItemPositionChange) and (self.pos().x()!= self.pos().y()) and (self.pos().x()!=0) :
            #self.heros.attribs['latitude'],self.heros.attribs['longitude'] = self.scene_coord.SceneToLatLon(self.pos().x(),self.pos().y())
            #print ('position changed',self.heros.attribs['latitude'],self.heros.attribs['longitude']) 
        return QGraphicsItem.itemChange(self,change,value)
    def boundingRect(self):
       # return self.path.boundingRect()
      #  return self.view.sceneRect()
        return QRectF(-self.size/2,-self.size/2,self.size,self.size)#self.image.boundingRect()
        


    def drawFactionShape(self,painter,size):
        if self.iconShape == 0 :
            painter.drawEllipse(0,0,self.size,self.size)
        elif self.iconShape == 1 :
            painter.drawRect(self.boundingRect())
            


                    
    def hoverEnterEvent(self, event):
        self.showPicture()

        return QGraphicsItem.hoverEnterEvent(self,event)

    def hoverLeaveEvent(self,event):
        print ('leave event')

        return QGraphicsItem.hoverLeaveEvent(self,event)
        
#     def dropEvent(self, event):
#         print ('leave drag event')
#         self.setSelected(False)
# 
#         return QGraphicsItem.dropEvent(self,event)

        
    def paint (self,painter,option, widget):
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.rotate(self.rotation)
        painter.translate(-self.size/2,-self.size/2)
        #painter.scale(300,600)
        #c = self.model.groupe_color_value[self.heros.groupe().attribs['color']]
        pen = QPen(QtCore.Qt.black)
        if self.isSelected() == True : 
            pen.setWidth(2)
        else:   
            pen.setWidth(1)
        painter.setPen(pen)


        radialGradient = QRadialGradient(self.size/2, self.size/2,self.size*0.8, self.size, self.size)
        radialGradient.setColorAt(0.0, QtCore.Qt.white)
        #radialGradient.setColorAt(0.2, self.heros.kingdom().color)
        if self.view.color_mode == ColorMode.Empire : 
            color = self.heros.empire().color
        elif self.view.color_mode == ColorMode.Kingdom : 
            color = self.heros.kingdom().color
        else:
            color = self.model.groupe_color_value[self.heros.groupe().attribs['color']]
        radialGradient.setColorAt(0.2, color)
        radialGradient.setColorAt(1.0, QtCore.Qt.black)
        painter.setBrush(QBrush(radialGradient))
        if self.heros.faction().name == "Lumiere":
            painter.drawEllipse(0,0,self.size,self.size)
        else:
            poly = self.getTriangle(self.Size)
            painter.drawPolygone(poly)

        if self.name_visible == True :
            painter.setPen(QPen(QColor('black')))
            painter.translate(0,10)
            self.ratio = 1.2
            rect = QRectF(0,0,self.size,self.size*self.ratio)
            painter.drawText (rect,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom, self.name)

 
    def print_out (self):
        pass

# 
# class PlaceItem (QGraphicsItem):
#     SIZE_MULTIPLICATOR = 2
#     position_changed = pyqtSignal (int,int,int)
#     def __init__(self,temple,parent=None):
#         super(PlaceItem,self).__init__(parent)
#         self.rotation = 0.0
#         self.size = 25
#         self.shape = 'Triangle'
#         self.color = QColor(125,125,125)
#         self.polygon_list = []
#         #self.item_change_callback = None
#         self.touch_mode = False
#         self.bounding_rect = QRectF(-90000,-9000,9999999,99999999)   
#         self.name  = temple.name
#         self.id_visible = True
#         size = self.size * pow(self.SIZE_MULTIPLICATOR, int(self.touch_mode))
#         self.polygon_list, self.bounding_rect = shapes.getShape(self.shape,size)     
#         #set flags
#         self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
#         self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
#         self.setFlag(QGraphicsItem.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.ItemIsMovable)
#         
#     def boundingRect(self):
#         print ('bounding rect')
#         return self.bounding_rect
#     
#     def itemChange (self, change,value):
#         if change == QGraphicsItem.ItemPositionChange :
#             self.position_changed.emit(self.id,mx,my)
#                 
#     def paint (self,painter,option, widget):
#         print ('paint')
#         painter.setRenderHints(QtGui.QPainter.Antialiasing)
#         painter.rotate(self.rotation)
#         pen = QPen(QColor(255-self.color.red(),255-self.color.green(),255-self.color.blue(),self.color.alpha()))
#         painter.setPen(pen)
#         brush = QBrush(self.color)
#         painter.setBrush(brush)
#         size = self.size * pow(self.SIZE_MULTIPLICATOR, int(self.touch_mode))
#         self.polygon_list, self.bounding_rect = self.map.shapes.getShape(self.shape,size)
#         for polygon in self.polygon_list :
#             painter.drawPolygon(polygon)
#             if self.id_visible == True :
#                 painter.setPen(QPen(QColor('white')))
#                 painter.drawtext(self.bounding_rect,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop, self.name)
#                 print ('visible')
#                 