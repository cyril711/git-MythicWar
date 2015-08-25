from PyQt5.Qt import QPushButton, QSizePolicy, QSize

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
    def connect(self):
        self.clicked.connect(self.onSelectedHeros)    
    def onSelectedHeros (self):
        self.model.askForHerosPage.emit(self.heros)
    
class HerosLabel (QPushButton):
    def __init__(self,heros,parent):
        super(HerosLabel,self).__init__()
        self.heros = heros
        if self.heros.leader == False : 
            self.setStyleSheet("QPushButton { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("QPushButton { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
        self.setText(heros.name)
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
        self.heros.leader = not self.heros.leader
        if self.heros.leader == False : 
            self.setStyleSheet("QPushButton { background-color: white;border-style: outset; border-width: 2px; border-color: beige;}")
        else:
            self.setStyleSheet("QPushButton { background-color: yellow;border-style: outset; border-width: 2px; border-color: beige;}")
        