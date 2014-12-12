from PyQt5 import QtCore, QtGui
from python_modules.config import Config

class WebMercatorTileWorker( QtCore.QObject ):
    
    tile_loaded = QtCore.pyqtSignal( QtGui.QImage, int, int, int )
    tile_not_loaded = QtCore.pyqtSignal()
    
    def __init__( self ):
        ''' initialisation of the web mercator worker '''
        super( WebMercatorTileWorker, self ).__init__()
        print ('init tile worker')
        
    def addImgToLoad( self, base_map, image, level, tx, ty, extension ):
        ''' load picture to QImage '''
        if image.load( Config().instance.settings.value("map/google_tile_dir") + "/"+base_map + '/%d/%d/%d.%s' % ( level, ty, tx, extension ) ):
            self.tile_loaded.emit( image, tx, ty, level )
            
        else:
            self.tile_not_loaded.emit()
