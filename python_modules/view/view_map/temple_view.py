from PyQt5 import QtCore, QtWidgets

from python_modules.view.view_map.map_scene import MapScene 
from python_modules.config import Config

from PyQt5.Qt import QPointF,  QRectF
from python_modules.view.view_map.map_item import *


class TempleView( QtWidgets.QGraphicsView ):

    def __init__( self, parent=None ):
        ''' Initialisation of the QGraphicsView '''
        super( TempleView, self ).__init__( parent )

        # scene coordinates
        self.items_heroes = []
#        self.scene_coord = None
        self.settings = Config().instance.settings
        # add a scene
        self.scene = MapScene( self )
        self.setScene( self.scene )
        self.temple = None
        # init the flags
        self.setFlags()

        self.setSceneRect( QRectF(0,0,500,500) )

    def setTemple (self,temple):
        print ('----------------setTemple')
        self.temple = temple
        for item in self.items_heroes : 
            self.scene.removeItem(item)
        for heros in self.temple.heros  :
            h = HerosItem(heros,20)
            h.setPos(QPointF(heros.attribs['latitude'],heros.attribs['longitude']))
            self.items_heroes.append(h)
            self.scene.addItem(h)
    def viewportEvent( self, event ):
        ''' viewport event manager '''
        return super( TempleView, self ).viewportEvent( event )



    def setFlags( self ):
        ''' set graphics view flags '''
        # scale regarding the cursor
        self.setTransformationAnchor( QtWidgets.QGraphicsView.AnchorViewCenter )
        # resize maintaining view center
        self.setResizeAnchor( QtWidgets.QGraphicsView.AnchorViewCenter )
        # to send cursor informations
        self.setMouseTracking( True )
        self.setDragMode( QtWidgets.QGraphicsView.ScrollHandDrag )


    def getSceneBoundingBox( self ):
        ''' get the part of the scene viewable '''
        rect_viewport = QtCore.QRect( 0, 0, self.width(), self.height() )
        poly_scene = self.mapToScene( rect_viewport )
        return poly_scene.boundingRect()


    def resizeEvent( self, event ):
        ''' window is resizing '''
        super( TempleView, self ).resizeEvent( event )



    def getSceneCoord( self ):
        ''' return the projection manager '''
        return self.scene_coord
