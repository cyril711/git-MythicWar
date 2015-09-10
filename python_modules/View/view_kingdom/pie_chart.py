from PyQt5.Qt import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QSize,\
    QGraphicsSimpleTextItem, QTransform, QPointF, QGraphicsRectItem, QColor,\
    QRect, QRectF, QGraphicsProxyWidget, QComboBox, QBrush, QPen
from PyQt5 import QtCore

class Section (QGraphicsEllipseItem):
    def __init__(self,x,y,width,height):
        super(Section,self).__init__(x,y,width,height)
        

class PieChart (QGraphicsView):
    def __init__(self,parent,total_value):
        super(PieChart,self).__init__(parent)
        self.my_scene = QGraphicsScene()
        #self.my_scene.setSceneRect(self.sceneRect())
        self.setScene(self.my_scene)
        #self.setBackgroundBrush(QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern));
        self.total_value = total_value

        self.initialize = False
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.margin = {'top':10,'bottom':10,'left':10,'right':10}        

        self.space = 30


        self.pie_items = []

    def setTotal (self, total):
        self.total_value = total
#     def setData (self,list_item):
# 
#         rect = QGraphicsRectItem(self.sceneRect())
#         rect.setBrush(QColor("red"))
#         self.scene().addItem(rect)
    
    def setData (self,list_items):
        size = min(self.frameSize().width()/2.0,self.frameSize().height())
        self.size_pie = QSize(size,size)
        print ('size pie ',self.size_pie)
        if self.initialize == False:
            self.c_box = QComboBox()
            self.c_box.addItem("all")
            self.c_box.addItem("alive")
            self.c_box.addItem("dead")
            self.c_box.currentIndexChanged.connect(self.update)
            proxy = self.my_scene.addWidget(self.c_box)
            x = self.size_pie.width()+ self.space
            proxy.setPos(QPointF(x,self.margin['top']))    
            self.initialize = True

        self.data = list_items
        self.update()

    def update(self):

        restant = 360
        i = 0
        #self.my_scene.clear()
        for item in self.pie_items :
            self.my_scene.removeItem(item)
        self.pie_items = []
        self.scene().setSceneRect(QRectF(0,0,self.frameSize().width(),self.frameSize().height()))
        print ('size',self.scene().sceneRect())
        #proxy = QGraphicsProxyWidget ()

        for item in self.data :
            if (i==len(self.data)-1 ):
                angle = restant
            else:
                try : 
                    angle = int(360*item[self.c_box.currentText()]/self.total_value[self.c_box.currentText()])
                except ZeroDivisionError:
                    angle = 0 
                    
            ellipse = Section(0,0,self.size_pie.width(),self.size_pie.height())

            y = (self.parent().size().height()-self.size_pie.height())/2.0
            x_pie = ((self.parent().size().width()/2.0)-self.size_pie.height())/2.0
            ellipse.setPos(x_pie,y)
 
            ellipse.setStartAngle(16*(360-restant))
            ellipse.setSpanAngle(angle*16)
            ellipse.setBrush(item['color'])
            self.my_scene.addItem(ellipse)
            self.pie_items.append(ellipse)
            # text pourcentage a afficher dans les portions de disque
            try :
                v = (item[self.c_box.currentText()]/self.total_value[self.c_box.currentText()])*100
            except ZeroDivisionError :
                v = 0
            text = QGraphicsSimpleTextItem("{0:5.2f}".format(v)+"%")
            trans = QTransform().translate(x_pie+self.size_pie.width()/2.0,y+self.size_pie.height()/2.0).rotate(((360-restant)+angle/2.0)*-1)
            pts = trans.map(QPointF(self.size_pie.width()/3.0,0))
            text.setPos(pts.x(),pts.y())
            self.my_scene.addItem(text)            
            self.pie_items.append(text)
            
            #libelle 
            rect = QGraphicsRectItem(0,0,10,10)
            x = x_pie + self.size_pie.width()+ self.space 
            interval_height = (self.parent().size().height()-self.margin['top']-self.margin['bottom'])/(len(self.data)+1)
            rect.setPos(QPointF(x,self.margin['top']+((i+1)*interval_height)))
            rect.setBrush(item['color'])
            self.my_scene.addItem(rect)
            self.pie_items.append(rect)
            text = QGraphicsSimpleTextItem(item['label']+ " ("+str(int(item[self.c_box.currentText()]))+")")
            pts = rect.pos()
            transform = QTransform().translate(30, 0)
            pts = transform.map(pts)
            text.setPos(pts)            
            self.my_scene.addItem(text)
            self.pie_items.append(text)
            restant = restant - angle
            i +=1

     #   self.fitInView(self.scene.sceneRect())