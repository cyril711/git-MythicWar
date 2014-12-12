from PyQt5 import QtCore

properties = []

class AbstractLayerAdapter( QtCore.QObject ):
    ''' Adapter for base properties '''
    def __init__( self, object_to_animate ):
        super( AbstractLayerAdapter, self ).__init__()
        self.o = object_to_animate
