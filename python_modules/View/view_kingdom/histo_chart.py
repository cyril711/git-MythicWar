from PyQt5.Qt import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QSize,\
    QGraphicsSimpleTextItem, QTransform, QPointF, QGraphicsRectItem, QColor,\
    QRect, QRectF, QGraphicsProxyWidget, QComboBox, QBrush, QPen, QSizeF,\
    QGraphicsTextItem, QPixmap, QGraphicsColorizeEffect, QLinearGradient
from PyQt5 import QtCore

# class Pic (QGraphicsEllipseItem):
#     def __init__(self,x,y,width,height):
#         super(Pic,self).__init__(x,y,width,height)
#         

class HistoChart (QGraphicsView):
    def __init__(self,parent,size=QSize(400,400)):
        super(HistoChart,self).__init__(parent)
        self.my_scene = QGraphicsScene()
        #self.my_scene.setSceneRect(self.sceneRect())
        self.setScene(self.my_scene)
        #self.setBackgroundBrush(QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern));
        
        
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.size_text_width = -1
        self.margin = {'top':10,'bottom':10,'left':10,'right':10}        
        self.initialize = False
        self.max_length_text = 10
        self.histo_items = []


    
    def setData (self,list_items):
        size = min(self.frameSize().width()/2.0,self.frameSize().height())
        self.size_pie = QSize(size,size)
        self.data = list_items
        if self.initialize == False:
            self.c_box = QComboBox()
            self.c_box.addItem("warrior")
            self.c_box.addItem("rank")
            self.c_box.addItem("power")
            self.c_box.currentIndexChanged.connect(self.update)
            proxy = self.my_scene.addWidget(self.c_box)
            
            proxy.setPos(QPointF(0.0,self.margin['top']))    
            self.margin['top']+=self.c_box.height()
            self.initialize = True
        self.update()

    def update(self):

        
        i = 0
        #self.my_scene.clear()
        for item in self.histo_items :
            self.my_scene.removeItem(item)
        self.histo_items = []
        self.scene().setSceneRect(QRectF(0,0,self.frameSize().width(),self.frameSize().height()))

        max = -1
        for value in self.data.values():
            if value[self.c_box.currentText()] > max:
                max = value[self.c_box.currentText()]


        size_text_number = QGraphicsTextItem(str(max)).boundingRect().width()+10
        interval= self.parent().size().height()-self.margin['top']-self.margin['bottom']
        interval = interval /len(self.data)
        

        temp = "aaaaaaaaaaaaaaaaa"
        if len(temp)> self.max_length_text:
            data = temp[:self.max_length_text]+"."
        else :
            data = temp
        self.size_text_width = QGraphicsTextItem(data).boundingRect().width()+10
        print ('width:',self.size_text_width)
        horizontal_size = self.parent().size().width()- self.margin['left']- self.margin['right']-self.size_text_width- size_text_number
        try:
            ratio = horizontal_size/ max
        except ZeroDivisionError :
            ratio = 0


        i = 0
        for groupe,value in zip(self.data.keys(),self.data.values()) :

            if self.c_box.currentText() == "warrior":
                title_str = 'Nombre de Heros'
                bar_all = QGraphicsRectItem(0,self.margin['top'],value['warrior']*ratio,interval*0.8)
                bar_all.setPos(self.size_text_width,interval*0.2+(i*interval))
                gradient = QLinearGradient(QPointF(bar_all.rect().width()/2,0),QPointF(bar_all.rect().width()/2,bar_all.rect().height()+self.margin['top']))
                gradient.setColorAt(0,QColor('white'))
                gradient.setColorAt(1,QColor('red'))
                brush = QBrush(gradient)            
                #brush.setTexture(QPixmap(":/textures/"+groupe.attribs['color']))
                bar_all.setBrush(brush)
                self.my_scene.addItem(bar_all)
                self.histo_items.append(bar_all)
    
                bar_alive = QGraphicsRectItem(0,self.margin['top'],value['alive']*ratio,interval*0.8)
                bar_alive.setPos(self.size_text_width,interval*0.2+(i*interval))
                gradient = QLinearGradient(QPointF(bar_alive.rect().width()/2,0),QPointF(bar_alive.rect().width()/2,bar_alive.rect().height()+self.margin['top']))
    #             gradient.setStart(QPointF(0.5,0))
    #             gradient.setStop(QPointF(0.5,1))
                gradient.setColorAt(0,QColor('white'))
                gradient.setColorAt(1,QColor('green'))
                brush = QBrush(gradient)
                
                bar_alive.setBrush(brush)
                self.my_scene.addItem(bar_alive)
                self.histo_items.append(bar_alive)
    
                text_nb_warriors= QGraphicsTextItem(str(value['warrior']))
                text_nb_warriors.setDefaultTextColor(QColor('green'))
                trans = QTransform().translate(bar_all.pos().x()+bar_all.rect().width()+10,interval*0.2+(i*interval)+self.margin['top'])
                pts = trans.map(QPointF(0,0.0))
                text_nb_warriors.setPos(pts.x(),pts.y())
                self.my_scene.addItem(text_nb_warriors)            
                self.histo_items.append(text_nb_warriors)


            #bar ranl
            elif self.c_box.currentText()== "rank":
                title_str = "Rank Moyen"
                bar_rank = QGraphicsRectItem(0,self.margin['top'],value['rank']*ratio,interval*0.8)
                bar_rank.setPos(self.size_text_width, interval*0.2+(i*interval))
                gradient = QLinearGradient(QPointF(bar_rank.rect().width()/2,0),QPointF(bar_rank.rect().width()/2,bar_rank.rect().height()+self.margin['top']))
    #             gradient.setStart(QPointF(0.5,0))
    #             gradient.setStop(QPointF(0.5,1))
                gradient.setColorAt(0,QColor('white'))
                gradient.setColorAt(1,QColor('red'))
                brush = QBrush(gradient)
                
                bar_rank.setBrush(brush)
                self.my_scene.addItem(bar_rank)
                self.histo_items.append(bar_rank)
    
                # value
                text_rank = QGraphicsTextItem("{0:1.1f}".format(value['rank']))
                text_rank.setDefaultTextColor(QColor('red'))
                trans = QTransform().translate(bar_rank.pos().x()+bar_rank.rect().width()+10,interval*0.2+(i*interval)+self.margin['top'])
                pts = trans.map(QPointF(0,0.0))
                text_rank.setPos(pts.x(),pts.y())
                self.my_scene.addItem(text_rank)            
                self.histo_items.append(text_rank)
    

            else:
                title_str = "Puissance"
                bar_rank = QGraphicsRectItem(0,self.margin['top'],value['power']*ratio,interval*0.8)
                bar_rank.setPos(self.size_text_width, interval*0.2+(i*interval))
                gradient = QLinearGradient(QPointF(bar_rank.rect().width()/2,0),QPointF(bar_rank.rect().width()/2,bar_rank.rect().height()+self.margin['top']))
    #             gradient.setStart(QPointF(0.5,0))
    #             gradient.setStop(QPointF(0.5,1))
                gradient.setColorAt(0,QColor('white'))
                gradient.setColorAt(1,QColor('blue'))
                brush = QBrush(gradient)
                
                bar_rank.setBrush(brush)
                self.my_scene.addItem(bar_rank)
                self.histo_items.append(bar_rank)
    
                # value
                try :
                    valeur = (value['power']/max)*100
                except ZeroDivisionError :
                    valeur = 0
                text_rank = QGraphicsTextItem("{0:1.1f}".format(valeur))
                text_rank.setDefaultTextColor(QColor('blue'))
                trans = QTransform().translate(bar_rank.pos().x()+bar_rank.rect().width()+10,interval*0.2+(i*interval)+self.margin['top'])
                pts = trans.map(QPointF(0,0.0))
                text_rank.setPos(pts.x(),pts.y())
                self.my_scene.addItem(text_rank)            
                self.histo_items.append(text_rank)


            #dessin du titre
            title = QGraphicsTextItem(title_str)
            title.setPos(self.margin['left']+self.size_text_width+horizontal_size/2.0,self.c_box.pos().y())
            self.my_scene.addItem(title)
            self.histo_items.append(title)
    
            #affichage des label colonne de gauche
            if len(groupe.name)> self.max_length_text:
                data = groupe.name[:self.max_length_text]+".."
            else :
                data = groupe.name
            text = QGraphicsTextItem(data)
            #text.setTextWidth(20)

            trans = QTransform().translate(self.margin['left'],interval*0.2+(i*interval)+self.margin['top'])
            pts = trans.map(QPointF(0,0.0))
            text.setPos(pts.x(),pts.y())
            self.my_scene.addItem(text)            
            self.histo_items.append(text)

            i +=1

     #   self.fitInView(self.scene.sceneRect())