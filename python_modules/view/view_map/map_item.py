from PyQt5.QtWidgets import  QFrame
from PyQt5.Qt import QColor, QRectF, QPen, QBrush,\
    QAction, QMenu, QPainterPath, QPointF, QLinearGradient, QVBoxLayout,\
    QGraphicsItem, QLabel, QPixmap, QTimer, QTextStream, QApplication
from PyQt5 import QtGui, QtCore
from python_modules.view.view_map.temple_view import TempleView
from PyQt5 import QtWidgets
from python_modules.config import Config
from functools import partial
import os
import PyQt5
class TempleItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    def __init__(self,temple,size,parent=None):
        super (TempleItem,self).__init__(parent)
        self.polygon  = self.getTriangle (size)
        self.rotation = 0.0
        self.color = QColor(0,0,125)
        self.name_visible = True
        self.name = temple.name
        self.model = temple
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
    def boundingRect(self):
        return self.polygon.boundingRect()
        
    def getTriangle (self,size):
        pts = []
        pts.append(QtCore.QPointF(-size,size))
        pts.append(QtCore.QPointF(0,-2*size))
        pts.append(QtCore.QPointF(size,size))
        return QtGui.QPolygonF(pts)


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged :
            self.model.position = value
            print ('new position ',self.model.position)
        else:
            return QGraphicsItem.itemChange(self,change,value)
    def paint (self,painter,option, widget):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.rotate(self.rotation)
        #painter.scale(300,600)
        if self.isSelected() == True : 
            pen = QPen(QColor(255,0,0,self.color.alpha()))
        else:   
            pen = QPen(QColor(255-self.color.red(),255-self.color.green(),255-self.color.blue(),self.color.alpha()))
        painter.setPen(pen)
        brush = QBrush(self.color)
        painter.setBrush(brush)
        
        painter.drawPolygon(self.polygon)
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
    SIZE_MULTIPLICATOR = 2
    def __init__(self,temple,size,parent=None):
        super (ActionsItem,self).__init__(parent)
        self.polygon  = self.getTriangle (size)
        self.rotation = 0.0
        self.color = QColor(0,0,125)
        self.name_visible = True
        self.name = temple.name
        self.model = temple
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

        
    def boundingRect(self):
        return self.polygon.boundingRect()
        



    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged :
            self.model.position = value
            print ('new position ',self.model.position)
        else:
            return QGraphicsItem.itemChange(self,change,value)
    def paint (self,painter,option, widget):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.rotate(self.rotation)
        #painter.scale(300,600)
        if self.isSelected() == True : 
            pen = QPen(QColor(255,0,0,self.color.alpha()))
        else:   
            pen = QPen(QColor(255-self.color.red(),255-self.color.green(),255-self.color.blue(),self.color.alpha()))
        painter.setPen(pen)
        brush = QBrush(self.color)
        painter.setBrush(brush)
        
        painter.drawPolygon(self.polygon)
        if self.name_visible == True :
            painter.setPen(QPen(QColor('black')))
            painter.translate(0,10)
            painter.drawText (self.boundingRect(),QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom, self.name)






class HerosItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    on_action = QtCore.pyqtSignal()
    def __init__(self,model,warrior,size,scene_coord,parent=None):
        super (HerosItem,self).__init__(parent)
        self.settings = Config().instance.settings
        self.heros = warrior
        self.model = model
        self.scene_coord = scene_coord
        self.heros.on_move.connect(self.updatePos)
#        self.image  = warrior.thumb
#        self.ratio = 1.29
#        if not self.image.isNull():
#            self.image = self.image.scaled(0.8*size,0.8*self.ratio*size)#.scaledToWidth(0.8*size)
#        self.path = self.getShape(size)
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
        self.setFlag(QGraphicsItem.ItemIsMovable)
        #if warrior.selected == True : 
        self.setSelected(warrior.selected)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents (True)
        self.framePicture = None


    def showPicture (self):
        self.model.askForProfil.emit(self.heros)

    def updatePos(self):
        print ('update pos',self.heros.attribs['place'] )
        if int(self.heros.attribs['place']) == 0:
            lat = self.heros.attribs['latitude']
            lon = self.heros.attribs['longitude']
   
            mx,my = self.scene_coord.LatLonToScene(lat,lon)
            self.setPos(mx,my)

    def itemChange (self, change,value):
        if change == QGraphicsItem.ItemSelectedChange :
            self.heros.setSelected(value)
    #    return super(HerosItem,self).itemChange(change,value) 
        #if (change == QGraphicsItem.ItemPositionChange) and (self.pos().x()!= self.pos().y()) and (self.pos().x()!=0) :
            #self.heros.attribs['latitude'],self.heros.attribs['longitude'] = self.scene_coord.SceneToLatLon(self.pos().x(),self.pos().y())
            #print ('position changed',self.heros.attribs['latitude'],self.heros.attribs['longitude']) 
        return QGraphicsItem.itemChange(self,change,value)
    def boundingRect(self):
       # return self.path.boundingRect()
        return QRectF(0,0,self.size,self.size)#self.image.boundingRect()
        
 #   def getShape (self,size):
 ##       path = QPainterPath ()
 #       height = size*self.ratio
#        height_arrow = -5
#        path.cubicTo(QPointF(0.0,height_arrow), QPointF(-size/4.0,height_arrow), QPointF(-size/2.0,height_arrow))
 #       path.lineTo(QPointF(-size/2.0,-height+height_arrow))
 #       path.lineTo(QPointF(size/2.0,-height+height_arrow))
 #       path.lineTo(QPointF(size/2.0,height_arrow))
 #       path.cubicTo(QPointF(0,height_arrow), QPointF(size/4.0,0), QPointF(0,0))
 #       return path


    def drawFactionShape(self,painter,size):
        if self.iconShape == 0 :
            painter.drawEllipse(0,0,self.size,self.size)
        elif self.iconShape == 1 :
            painter.drawRect(self.boundingRect())
            
    def drawEmpireShape(self,painter,size,empire_color):
        #print ('empire_color',empire_color)
        if empire_color == "foudre" :
            brush = QBrush(QColor(102,0,153))
        else:
            brush = QBrush(QColor(0,0,0))

        painter.setBrush(brush)
        pen = QPen()
        pen.setStyle(QtCore.Qt.NoPen)
        painter.setPen(pen)
        size = size/2
        painter.translate(size*0.25,size)
        painter.rotate(-45)
        painter.drawRect(0,0,size,size)    

        painter.rotate(45)
        painter.translate(-size*0.25,-size)

#     def showPicture (self):
# 
#         self.framePicture  = QFrame()
#         self.framePicture.setWindowModality(QtCore.Qt.WindowModal)
#         if self.settings.value("mainView/stylesheet")!= "":
#             file = QtCore.QFile(os.path.join(self.settings.path_to_qss(),self.settings.value("mainView/stylesheet")))
#             if file.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text):
#                 text = QTextStream(file)
#                 QApplication.instance().setStyleSheet(text.readAll())
#         self.framePicture.setObjectName("Frame")
#         self.framePicture.setFrameShape(QFrame.NoFrame)
#         #self.framePicture.setFrameShadow(QFrame.Raised)
#         self.verticalLayout = QVBoxLayout(self.framePicture)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.picture = QLabel()
#         self.picture.setFrameShape(QFrame.NoFrame)
#         groupe_name = self.heros.groupe().name
#         if self.heros.masterGroupe() != None : 
#             groupe_name = self.heros.masterGroupe().name+"/"+groupe_name
#         kingdom_name = self.heros.kingdom().name
#         empire_name = self.heros.empire().name
#         faction_name = self.heros.faction().name
#         pixmap = QPixmap(self.settings.value("global/resources_path")+"/"+faction_name+"/"+empire_name+"-"+self.heros.empire().attrib['color']+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.heros.name+"/portrait.jpg")
#         print ('ppppppppp:',)
#         if not pixmap.isNull():
#             pixmap = pixmap.scaled(pixmap.width()/5.0,pixmap.height()/5.0)
#             self.picture.setPixmap(pixmap)
#             self.verticalLayout.addWidget(self.picture)
#             self.title = QLabel()
#             self.title.setAlignment(QtCore.Qt.AlignHCenter)
#             self.title.setFrameShape(QFrame.NoFrame)
#             self.framePicture.setGeometry(QtGui.QCursor().pos().x()+30,QtGui.QCursor().pos().y()+50,pixmap.width(),pixmap.height())
#           
#             self.title.setText(self.heros.name)
#             self.verticalLayout.addWidget(self.title)
#             self.framePicture.show()
#         else:
#             print ('picture is null')
                    
    def hoverEnterEvent(self, event):
        self.showPicture()

        return QGraphicsItem.hoverEnterEvent(self,event)

    def hoverLeaveEvent(self,event):
        print ('leave event')

        return QGraphicsItem.hoverLeaveEvent(self,event)
        
    def dropEvent(self, event):
        print ('leave drag event')
        self.setSelected(False)

        return QGraphicsItem.dropEvent(self,event)
    def paint (self,painter,option, widget):
        #painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.rotate(self.rotation)
        #painter.scale(300,600)
        c = self.model.groupe_color_value[self.heros.groupe().attribs['color']]
        pen = QPen(c)
        if self.isSelected() == True : 
            pen.setWidth(4)
        else:   
            pen.setWidth(2)
        painter.setPen(pen)
#         brush = QBrush(self.color)
        #linearGradient = QLinearGradient(0, 0, 100, 100)
        #linearGradient.setColorAt(0.0, QColor('green'))
        #linearGradient.setColorAt(0.2, QColor('white'))
        #linearGradient.setColorAt(1.0, QColor('green'))
        #brush = QBrush(linearGradient)

        brush = QBrush(self.heros.kingdom().color)
        painter.setBrush(brush)
        self.drawFactionShape(painter,self.size)
        self.drawEmpireShape(painter,self.size,self.heros.empire().attrib['color'])
        
        ##painter.drawPath(self.path)
        #diff_height = self.path.boundingRect().height() - self.image.height()
       # painter.translate(-self.image.width()/2.0,-self.path.boundingRect().height()+diff_height/2.0)
       # painter.drawPixmap(0,0,self.image)
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