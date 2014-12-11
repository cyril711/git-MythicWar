from PyQt5 import QtWidgets




class Tile (QtWidgets.QGraphicsPixmapItem):
    def __init__(self,tile_type,level,parent=None):
        super (Tile,self).__init__(parent)
        self.level = level
        self.tile_type = tile_type
        
    def getLevel (self):
        return self.level
    
    def getType (self):
        return self.tile_type