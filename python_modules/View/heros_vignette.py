from PyQt5.Qt import QPushButton, QSizePolicy, QSize, QGraphicsColorizeEffect,\
    QColor

class TempleButton (QPushButton):
    def __init__(self,model,temple,parent):
        super(TempleButton,self).__init__(parent)
        self.temple = temple
        self.model = model
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setFixedSize(QSize(100,120))
        self.setSizePolicy(sizePolicy)
    def connect(self):
        self.clicked.connect(self.onSelectedTemple)    
    def onSelectedTemple(self):
        pass
        #self.model.askForHerosPage.emit(self.heros)
    
class TempleLabel (QPushButton):
    def __init__(self,temple,parent):
        super(TempleLabel,self).__init__()
        self.temple= temple
        self.setObjectName(self.temple.name)
        if self.temple.master == False : 
            self.setStyleSheet("#"+self.objectName()+" { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("#"+self.objectName()+" { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
        self.setText(self.temple.name)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setFixedSize(QSize(100,20))
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        #warrior_label.setMinimumSize(QtCore.QSize(0, 10))
       # self.setAlignment(QtCore.Qt.AlignCenter)    
    def connect(self):
        self.clicked.connect(self.changeMasterFlag)
 
    def changeMasterFlag (self): 
        self.temple.master= not self.temple.master
        if self.temple.master== False : 
            self.setStyleSheet("#"+self.objectName()+" { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("#"+self.objectName()+" { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
     

class HerosButton (QPushButton):
    def __init__(self,model,heros,parent):
        super(HerosButton,self).__init__(parent)
        self.heros = heros
        self.model = model
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setFixedSize(QSize(100,120))
        self.setSizePolicy(sizePolicy)
        self.graphics_effect = QGraphicsColorizeEffect()
        self.graphics_effect .setColor(QColor(125,125,125))
        self.setGraphicsEffect(self.graphics_effect )
        self.graphics_effect.setEnabled(False)
        
    def enableEffect(self):
        self.graphics_effect.setEnabled(True)
        
    def disableEffect(self):
        self.graphics_effect.setEnabled(False)
        
    def connect(self):
        self.clicked.connect(self.onSelectedHeros)    
    def onSelectedHeros (self):
        self.model.askForHerosPage.emit(self.heros)
    
class HerosLabel (QPushButton):
    def __init__(self,heros,parent):
        super(HerosLabel,self).__init__()
        self.heros = heros
        self.setObjectName(self.heros.name)
        if self.heros.leader == False : 
            self.setStyleSheet("#"+self.objectName()+" { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("#"+self.objectName()+" { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
        self.setText(heros.name)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setFixedSize(QSize(100,20))
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.graphics_effect = QGraphicsColorizeEffect()
        self.graphics_effect .setColor(QColor(125,125,125))
        self.setGraphicsEffect(self.graphics_effect )
        self.graphics_effect.setEnabled(False)
        
    def enableEffect(self):
        self.graphics_effect.setEnabled(True)
        
    def disableEffect(self):
        self.graphics_effect.setEnabled(False)

        #warrior_label.setMinimumSize(QtCore.QSize(0, 10))
       # self.setAlignment(QtCore.Qt.AlignCenter)    
    def connect(self):
        self.clicked.connect(self.changeMasterFlag)
 
    def changeMasterFlag (self): 
        self.heros.changeLeaderStatus(not self.heros.leader)

        if self.heros.leader == False : 
            self.setStyleSheet("#"+self.objectName()+" { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("#"+self.objectName()+" { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
        