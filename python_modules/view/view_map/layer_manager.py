from PyQt5 import QtCore

import importlib
from PyQt5.Qt import QSettings

instantiates = 0

class LayerManager( QtCore.QObject ):

    # signals declaration
    update_available_layers = QtCore.pyqtSignal( list, list )
    update_instantiated_layers = QtCore.pyqtSignal( list )

    def __init__( self, scene,model, parent=None ):
        ''' initialisation of the laye manager '''
        super( LayerManager, self ).__init__( parent )
        self.scene = scene
        self.model = model
        self.settings = QSettings("config.ini",QSettings.IniFormat)
        self.projection = None
        self.scene_bounding_box = None
        self.instantiated_layers = []
        self.instantiable_layers = []
        self.available_layers = []
        self.initLayers()
        

    def initLayers( self ):
        ''' list all instantiable layers '''
        layers_list = self.settings.value("map/available_layers",[])
        print ("layer_list",layers_list)
        for layer in layers_list:
            print ('layer ',layer)
            module_name, module_class = layer.split( '.' )
            print ('module_name',module_name,module_class)
            module = importlib.import_module( "python_modules.view.view_map."+module_name )
            print('module',module)
            self.instantiable_layers.append( getattr( module, module_class ) )

    def getProjection( self ):
        ''' return projection '''
        return self.projection

    def update( self, scene_bounding_box ):
        ''' update instantiated layers '''
        for layer in self.instantiated_layers:
            layer.update( scene_bounding_box )
        self.scene_bounding_box = scene_bounding_box

    def addLayer( self, layer_name ):
        ''' create layer '''
        # instantiation
        global instantiates
        instantiates += 1
        for layer in self.instantiable_layers:
            print ('add layer names :',layer.name( layer ))
            if layer.name( layer ) == layer_name:
                print (type(self.parent()))
                self.instantiated_layers.append( layer( self.scene, instantiates, self.model, self.parent().getSceneCoord(), self ) )
                self.update_instantiated_layers.emit( self.instantiated_layers )

        # update projection
        if self.projection == None:
            self.projection = self.instantiated_layers[0].getProjection()
            print ('recuperation de la projection du premier layer cree',self.projection)

        self.updateAvailableLayers()

    def removeLayer( self, layer_name ):
        ''' delete layer '''
        global instantiates
        instantiates -= 1

        # get z value
        for instantiated_layer in self.instantiated_layers:
            if instantiated_layer.__class__.name( instantiated_layer.__class__ ) == layer_name:
                z_value = instantiated_layer.getZValue()
                break

        # update others z value
        for instantiated_layer in self.instantiated_layers:
            if instantiated_layer.__class__.name( instantiated_layer.__class__ ) == layer_name:
                layer_to_remove = instantiated_layer
            elif instantiated_layer.getZValue() > z_value:
                instantiated_layer.decreaseZValue()

        # destruction
        self.instantiated_layers.remove( layer_to_remove )
        layer_to_remove.clearItems()
        self.update_instantiated_layers.emit( self.instantiated_layers )

        # update projection or opacity
        if self.instantiated_layers == []:
            self.projection = None
            self.updateAvailableLayers()

    def updateAvailableLayers( self ):
        ''' update available layers list '''
        self.available_layers = []
        # if projection is null, only layers with specific projection can be instantiate
        if self.projection == None:
            for layer in self.instantiable_layers:
                if layer.projection( layer ) != None:
                    self.available_layers.append( layer.name( layer ) )
        # if a projection is already activated, layers without projection are added and layers with other projection become unavailable
        else:
            for layer in self.instantiable_layers:
                if layer.projection( layer ) == self.projection or layer.projection( layer ) == None:
                        self.available_layers.append( layer.name( layer ) )
        self.update_available_layers.emit( self.available_layers, self.instantiable_layers )

    def updateRotation( self, value ):
        for instantiated_layer in self.instantiated_layers:
            instantiated_layer.updateRotation( value )

    def releaseEvent( self, pos, scene_pos ):
        for instantiated_layer in self.instantiated_layers:
            if instantiated_layer.__class__.name( instantiated_layer.__class__ ) == 'Draw':
                instantiated_layer.releaseEvent( pos, scene_pos )
