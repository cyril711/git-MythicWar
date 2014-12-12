from PyQt5 import QtCore, QtGui
from python_modules.view.view_map import layer
from python_modules.view.view_map import web_mercator_tile_worker
from python_modules.view.view_map import layer_config_file_manager
#from python_modules.utils import projection
from python_modules.view.view_map import tile
from python_modules.config import Config
from python_modules.view.view_map import layer_adapter


#from python_modules.View.map.place_item import TempleItem
#import property_delegate

class WebMercatorTileAdapter( layer_adapter.AbstractLayerAdapter ):
    ''' Adapter for using properties and animation '''
    def __init__( self, object_to_animate ):
        super( WebMercatorTileAdapter, self ).__init__( object_to_animate )

    @QtCore.pyqtProperty( tuple )
    def base_map( self ):
        return ( self.o.manager.getBasesMapName(), self.o.index )
    @base_map.setter
    def base_map( self, value ):
        self.o.clearItems() # always before change base_map
        self.o.index = [index for index, base_map in enumerate( self.o.manager.getBasesMapName() ) if base_map == value][0]
        self.o.base_map = self.o.manager.getBasesMapName()[self.o.index]
        self.o.extension = self.o.manager.getExtension( self.o.base_map )

    @QtCore.pyqtProperty( bool )
    def visibility( self ):
        return self.o.visibility
    @visibility.setter
    def visibility( self, value ):
        self.o.visibility = bool( value )

    @QtCore.pyqtProperty( float )
    def opacity( self ):
        return self.o.opacity
    @opacity.setter
    def opacity( self, value ):
        self.o.opacity = min( max( 0.0, value ), 1.0 )

    @QtCore.pyqtProperty( QtGui.QColor )
    def color( self ):
        return self.o.color
    @color.setter
    def color( self, value ):
        self.o.color = value

class WebMercatorTileLayer( layer.Layer ):

    properties = ['base_map']

#     special_delegates = {
#                          'base_map' : property_delegate.DropdownListPropertyDelegate(),
#                          }

    tile_to_load = QtCore.pyqtSignal( str, QtGui.QImage, int, int, int, str )

    @staticmethod
    def name( cls ):
        ''' return name of layer without instantied itself '''
        return 'WebMercator Tiles'

    @staticmethod
    def projection( cls ):
        ''' return projection of layer without instantied itself '''
        return 'WebMercator'

    def __init__( self, scene, z_value, simulation=None, scene_coord=None, parent=None ):
        ''' initialisation of the web mercator layer '''
        print ('init webmercator layer')
        super( WebMercatorTileLayer, self ).__init__( scene, z_value,scene_coord, parent )
        # create the manager responsible for the properties file
        self.manager = layer_config_file_manager.WebMercatorTileManager( Config().instance.settings.value("map/google_tiles" ))

        # init member variables
        
        self.index = 0
        self.base_map = self.manager.getBasesMapName()[self.index]
        self.extension = self.manager.getExtension( self.base_map )
        self.visibility = True
        self.opacity = 1.0
        self.tiles_loading = 0

        # create a thread
        self.thread = QtCore.QThread()
        # create the class that will do the job, and change its thread affinity to the new thread
        self.worker = web_mercator_tile_worker.WebMercatorTileWorker()
        self.worker.moveToThread( self.thread )
        # connect to the worker class
        self.connections()
        # start the thread, thus its event loop
        self.thread.start()

        # adapter
        self.adapter = WebMercatorTileAdapter( self )



    def __del__( self ):
        ''' to stop thread before exiting '''
        self.thread.terminate()

    def clearItems( self ):
        ''' to delete item from scene on remove from layers list '''
        for item in self.scene.items():
            if type( item ) == tile.Tile and item.getType() == self.base_map:
                self.scene.removeItem( item )

    def connections( self ):
        ''' make connections between layer and worker '''
        self.tile_to_load.connect( self.worker.addImgToLoad )
        self.worker.tile_loaded.connect( self.addImgLoaded )
        self.worker.tile_not_loaded.connect( self.imgNotLoaded )

    def disconnections( self ):
        ''' disconnections between layer and worker '''
        self.tile_to_load.disconnect()
        self.worker.tile_loaded.disconnect()
        self.worker.tile_not_loaded.disconnect()

    def update( self, scene_bounding_box ):
        ''' update tiles '''
        if self.visibility:
            # delete tiles invisible
            self.deleteInvisibleItems( scene_bounding_box )
            # get the bounds of the tiles to load
            
            tminx, tminy, tmaxx, tmaxy = self.scene_coord.getTilesToLoad( scene_bounding_box )
            if self.tiles_loading == 0:
                # emit tiles to load in the thread
                for ty in range( tminy, tmaxy + 1 ):
                    for tx in range( tminx, tmaxx + 1 ):
                        minx, miny, maxx, maxy = self.scene_coord.getSceneTileBounds( tx, ty )
                        # draw tile only if it isn't already drawn
                        if self.noTileAlreadyDrawn( minx, maxx, miny, maxy ):
                            self.tile_to_load.emit( self.base_map, QtGui.QImage(), self.scene_coord.getLevel(), tx, ty, self.extension )
                            self.tiles_loading += 1

    def addImgLoaded( self, image, tx, ty, level ):
        ''' add loading tiles to the scene '''
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage( image )
        item = tile.Tile( self.base_map, level )
        item.setPixmap( pixmap )
        item.setOpacity( self.opacity )
        item.setScale( self.scene_coord.getResolution() )
        item.setPos( self.scene_coord.getTilePos( tx, ty ) )


        item.setZValue( self.z_value )
        self.scene.addItem( item )
        self.tiles_loading -= 1
        if self.tiles_loading == 0:
            self.deleteTilesFromAnotherLevel()

    def imgNotLoaded( self ):
        ''' decreases flag if tile not correctly loaded '''
        self.tiles_loading -= 1
        if self.tiles_loading == 0:
            self.deleteTilesFromAnotherLevel()

    def deleteTilesFromAnotherLevel( self ):
        ''' delete tiles from another level after current level tiles added (smoother transition)'''
        for item in self.scene.items():
            if type( item ) == tile.Tile and item.getType() == self.base_map and item.getLevel() != self.scene_coord.getLevel():
                self.scene.removeItem( item )
                del item

    def deleteInvisibleItems( self, scene_bounding_box ):
        ''' delete items not visible in the view '''
        visible_items = self.scene.items( scene_bounding_box.x(), scene_bounding_box.y(), scene_bounding_box.width(), scene_bounding_box.height(), QtCore.Qt.IntersectsItemBoundingRect, QtCore.Qt.AscendingOrder )
        for item in self.scene.items():
            if item not in visible_items and type( item ) == tile.Tile and item.getType() == self.base_map:
                self.scene.removeItem( item )
                del item

    def noTileAlreadyDrawn( self, minx, maxx, miny, maxy ):
        ''' checks if no tile is already drawn at this location '''
        items = self.scene.items( QtCore.QPointF( ( minx + maxx ) / 2, ( miny + maxy ) / 2 ), QtCore.Qt.IntersectsItemBoundingRect, QtCore.Qt.AscendingOrder )
        for item in items:
            if type( item ) == tile.Tile and item.getType() == self.base_map and item.getLevel() == self.scene_coord.getLevel():
                return False
        return True

