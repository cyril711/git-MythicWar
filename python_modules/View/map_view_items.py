from PyQt5.Qt import QGraphicsItem, QPixmap
class MapViewItems (QGraphicsItem):
    def init (self,parent):
        super (MapViewItems).init(parent)
        
        
        
        
        
        
class PersoMapItem (MapViewItems):
    def init (self,picture_filename, name, life,parent):
        super (PersoMapItem).init(parent)
        self.pict = QPixmap(picture_filename)
        self.name = name
        self.life = life
        
    def render (self, painter):   
        # draw picture
        painter.drawPixmap(self.pict)
        # draw life jauge