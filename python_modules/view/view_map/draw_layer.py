from PyQt5 import QtCore, QtGui, QtWidgets
from python_modules.view.view_map import layer
from python_modules.view.view_map import layer_adapter
from python_modules.view.view_map import map_items.polygon_item

class DrawAdapter( layer_adapter.AbstractLayerAdapter ):
    ''' Adapter for using properties and animation '''
    def __init__( self, object_to_animate ):
        super( DrawAdapter, self ).__init__( object_to_animate )

    @QtCore.pyqtProperty( int )
    def border_size( self ):
        return self.o.border_size
    @border_size.setter
    def border_size( self, value ):
        self.o.border_size = value
        for item in self.o.items:
            self.o.items[item].prepareGeometryChange()
            self.o.items[item].size = self.o.border_size
            self.o.items[item].update()

class DrawLayer( layer.Layer ):

    properties = ['border_size']

    special_delegates = {}

    @staticmethod
    def name( cls ):
        ''' return name of layer without instantied itself '''
        return 'Draw'

    @staticmethod
    def projection( cls ):
        ''' return projection of layer without instantied itself '''
        return None

    def __init__( self, scene, z_value, simulation, scene_coord, parent=None ):
        ''' initialisation of the draw layer '''
        super( DrawLayer, self ).__init__( scene, z_value, scene_coord, parent )

        # init the projection
        self.is_drawing = False
        self.current_item = None
        self.item_to_remove = None
        self.count = 0
        self.border_size = 2
        self.start_pos = QtCore.QPoint()

        # init member variables
        self.items = {}

        self.adapter = DrawAdapter( self )

    def isSelected( self ):
        for item in self.items:
            self.items[item].setFlag( QtWidgets.QGraphicsItem.ItemIsSelectable )
            self.items[item].setFlag( QtWidgets.QGraphicsItem.ItemIsMovable )

    def isNoMoreSelected( self ):
        for item in self.items:
            self.items[item].setFlag( QtWidgets.QGraphicsItem.ItemIsSelectable, False )
            self.items[item].setFlag( QtWidgets.QGraphicsItem.ItemIsMovable, False )

    def contextMenu( self, pos, menu ):
        if self.is_drawing == True:
            finish_Polygon = QtWidgets.QAction( 'Finish Polygon', menu )
            finish_Polygon.triggered.connect( self.onFinishPolygon )
            menu.addAction( finish_Polygon )
        else:
            for item in self.items:
                if self.isUnderMouse( pos, self.items[item] ):
                    self.item_to_remove = self.items[item]
                    pixmap = QtGui.QPixmap( 16, 16 )
                    pixmap.fill( self.items[item].color )
                    icon = QtGui.QIcon( pixmap )
                    remove_polygon = QtWidgets.QAction( icon, 'Remove Polygone', menu )
                    remove_polygon.triggered.connect( self.onRemovePolygon )
                    menu.addAction( remove_polygon )
                    menu.addSeparator()
            add_Polygon = QtWidgets.QAction( 'Add Polygon', menu )
            add_Polygon.triggered.connect( self.onAddPolygon )
            menu.addAction( add_Polygon )

    def onRemovePolygon( self ):
        if self.item_to_remove.scene() == self.scene:
            self.scene.removeItem( self.item_to_remove )
        items = {}
        for item in self.items:
            if self.items[item] != self.item_to_remove:
                items[item] = self.items[item]
        self.items = items
        self.item_to_remove = None

    def onFinishPolygon( self ):
        color = QtWidgets.QColorDialog().getColor( self.current_item.color, None, 'Select Polygon Color', QtWidgets.QColorDialog.ShowAlphaChannel )
        if color.isValid():
            self.current_item.color = QtGui.QColor( color )
        self.current_item.completed = True
        self.current_item.setFlag( QtWidgets.QGraphicsItem.ItemIsSelectable )
        self.current_item.setFlag( QtWidgets.QGraphicsItem.ItemIsMovable )
        self.item_to_remove = None
        self.current_item = None
        self.is_drawing = False

    def onAddPolygon( self ):
        self.current_item = map_items.polygon_item.PolygonItem()
        item = '%d' % ( self.count )
        self.items[item] = self.current_item
        self.scene.addItem( self.items[item] )
        self.items[item].setZValue( self.z_value )
        self.items[item].size = self.border_size

        self.is_drawing = True
        self.item_to_remove = None
        self.count += 1

    def releaseEvent( self, pos, scene_pos ):
        if self.current_item != None:
            if self.current_item.pts == []:
                self.start_pos = pos
                self.current_item.setPos( scene_pos.x(), scene_pos.y() )
                self.current_item.pts.append( QtCore.QPoint( 0, 0 ) )
            else:
                self.current_item.pts.append( QtCore.QPoint( pos.x() - self.start_pos.x(), pos.y() - self.start_pos.y() ) )
