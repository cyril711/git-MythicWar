from PyQt5.QtWidgets import  QFrame
from PyQt5.Qt import QColor, QRectF, QPen, QBrush,\
    QAction, QMenu, QPainterPath, QPointF, QLinearGradient, QVBoxLayout,\
    QGraphicsItem
from PyQt5 import QtGui, QtCore
from python_modules.view.view_map.temple_view import TempleView
from PyQt5 import QtWidgets


class TempleItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    def __init__(self,kingdom,size,parent=None):
        super (TempleItem,self).__init__(parent)
        self.polygon  = self.getTriangle (size)
        self.rotation = 0.0
        self.color = QColor(0,0,125)
        self.name_visible = True
        self.name = kingdom.name
        self.kingdom = kingdom
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




class HerosItem (QtWidgets.QGraphicsItem):
    SIZE_MULTIPLICATOR = 2
    def __init__(self,warrior,size,parent=None):
        super (HerosItem,self).__init__(parent)
        self.heros = warrior
        self.image  = warrior.thumb
        self.ratio = 1.29
        if not self.image.isNull():
            self.image = self.image.scaled(0.8*size,0.8*self.ratio*size)#.scaledToWidth(0.8*size)
        self.path = self.getShape(size)
        self.rotation = 0.0
        self.size = size
        self.color = QColor(125,125,125)
        self.name_visible = True
        self.name = warrior.name
        #set flags
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        #if warrior.selected == True : 
        self.setSelected(warrior.selected)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)



    def itemChange (self, change,value):
        if change == QGraphicsItem.ItemSelectedChange :
            self.heros.setSelected(value)
        return super(HerosItem,self).itemChange(change,value) 

    def boundingRect(self):
        return self.path.boundingRect()
        return QRectF(0,0,self.image.width(),self.image.height())#self.image.boundingRect()
        
    def getShape (self,size):
        path = QPainterPath ()
        height_arrow = -5
        height = size*self.ratio
        path.cubicTo(QPointF(0.0,height_arrow), QPointF(-size/4.0,height_arrow), QPointF(-size/2.0,height_arrow))
        path.lineTo(QPointF(-size/2.0,-height+height_arrow))
        path.lineTo(QPointF(size/2.0,-height+height_arrow))
        path.lineTo(QPointF(size/2.0,height_arrow))
        path.cubicTo(QPointF(0,height_arrow), QPointF(size/4.0,0), QPointF(0,0))
        return path

    def paint (self,painter,option, widget):
        #painter.setRenderHints(QtGui.QPainter.Antialiasing)
        
        painter.rotate(self.rotation)
        #painter.scale(300,600)
        if self.isSelected() == True : 
            pen = QPen(QColor(255,0,0,self.color.alpha()))
        else:   
            pen = QPen(QColor(255-self.color.red(),255-self.color.green(),255-self.color.blue(),self.color.alpha()))
        painter.setPen(pen)
#         brush = QBrush(self.color)
        linearGradient = QLinearGradient(0, 0, 100, 100)
        linearGradient.setColorAt(0.0, QColor('green'))
        linearGradient.setColorAt(0.2, QColor('white'))
        linearGradient.setColorAt(1.0, QColor('green'))
        brush = QBrush(linearGradient)
        painter.setBrush(brush)
        painter.drawPath(self.path)
        diff_height = self.path.boundingRect().height() - self.image.height()
        painter.translate(-self.image.width()/2.0,-self.path.boundingRect().height()+diff_height/2.0)
        painter.drawPixmap(0,0,self.image)
        if self.name_visible == True :
            painter.setPen(QPen(QColor('black')))
            painter.translate(0,10)
            rect = QRectF(0,0,self.size,self.size*self.ratio)
            painter.drawText (rect,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom, self.name)

    def contextMenuEvent(self, event):
        menu = QMenu()
        testAction = QAction('Test', None)
        testAction.triggered.connect(self.print_out)
        menu.addAction(testAction)
        menu.exec_(event.screenPos())
        
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