from PyQt5 import QtCore
from python_modules.View.map import layer_adapter

class Layer( QtCore.QObject ):

    def __init__( self, scene, z_value, scene_coord=None, parent=None ):
        ''' initialisation of the layer parent class '''
        super( Layer, self ).__init__( parent )
        self.scene = scene
        self.scene_coord = scene_coord
        self.z_value = z_value
        self.items = {}
        self.map_rotation = 0.0
        self.widget = None
        self.simulation = None
        self.touch_mode = False

    def getProperties( self ):
        ''' return properties ordered alphabetically '''
        l = []
        for prop_name in layer_adapter.properties:
            l.append( ( prop_name, None ) )
        for prop_name in self.properties:
            if self.special_delegates.has_key( prop_name ):
                l.append( ( prop_name, self.special_delegates[prop_name] ) )
            else:
                l.append( ( prop_name, None ) )
        return l

#    def getName( self ):
#        ''' return layer name '''
#        return self.name

    def getGuiWidget( self ):
        ''' return layer widget '''
        return self.widget

    def update( self, scene_bounding_box ):
        ''' update layer '''
        pass

    def getProjection( self ):
        ''' return default projection name '''
        return self.__class__.projection( self.__class__ )

    def clearItems( self ):
        ''' to delete items from scene after layers list removal '''
        for item in self.items:
            try:
                if self.items[item].scene() == self.scene:
                    self.scene.removeItem( self.items[item] )
            except:
                pass
        if self.simulation != None:
            self.disconnections()
        self.items.clear()

    def updateZValue( self ):
        ''' update tiles Z value '''
        for item in self.scene.items():
            try:
                self.items[item].setZValue( self.z_value )
            except:
                pass

    def updateRotation( self, value ):
        ''' set the current map rotation '''
        self.map_rotation = value

    def doubleClick( self, position ):
        ''' Personalisation of the double click action '''
        pass

    def isUnderMouse( self, mouse_pos, item ):
        ''' return true if item is under mouse position '''
        r = self.scene_coord.getRealResolution()
        b = item.bounding_rect
        rect = QtCore.QRectF( item.pos().x() + r * b.x(), item.pos().y() + r * b.y(), r * b.width(), r * b.height() )
        return rect.contains( mouse_pos )

    def setTouchMode( self, value ):
        self.touch_mode = value
        for item in self.items:
            self.items[item].touch_mode = value

    def contextMenu( self, pos, menu ):
        ''' Personalisation of the contextual menu action '''
        pass

    def isNoMoreSelected( self ):
        pass

    def isSelected( self ):
        pass

    def getZValue( self ):
        return self.z_value

    def decreaseZValue( self ):
        self.z_value -= 1
        self.updateZValue()
