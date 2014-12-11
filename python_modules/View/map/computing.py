from PyQt5 import QtGui, QtWidgets
import math as M
from python_modules.View.map import layer_config_file_manager

class Computing():
    def __init__( self ):
        ''' initialisation of the computing classe '''
        self.manager = layer_config_file_manager.LevelManager()
        self.z_value = 1000

    def hasToChangeLevel( self, transform, resolution, resolution_down, level ):
        ''' return the new level if needed '''
        scale = M.sqrt( transform.m11() * transform.m11() + transform.m12() * transform.m12() )
        if scale > 2.0 / resolution:
            if level < self.manager.getMaxLevel():
                scale_to_level = ( 2.0 / resolution ) / scale
                return scale_to_level, level + 1
        elif scale < 2.0 / resolution_down:
            if level > self.manager.getMinLevel():
                scale_to_level = ( 2.0 / resolution_down ) / scale
                return scale_to_level, level - 1
        return None, None

    def getViewScale( self, transform, resolution ):
        ''' return the scale associates to the new level resolution '''
        scale = M.sqrt( transform.m11() * transform.m11() + transform.m12() * transform.m12() )
        return ( 1.0 / resolution ) / scale

    def getCenter( self, rect ):
        ''' return the center of the rectangle parameter '''
        return rect.x() + rect.width() / 2.0, rect.y() + rect.height() / 2.0

    def drawDistance( self, origin, destination, scene_coord, rotation_value ):
        ''' display distance entre two coordinates points on right click '''
        r = scene_coord.getRealResolution()
        distance_line = QtWidgets.QGraphicsLineItem( origin.x(), origin.y(), destination.x(), destination.y() )
        inside_line = QtWidgets.QGraphicsLineItem( origin.x(), origin.y(), destination.x(), destination.y(), distance_line )
        start_point = QtWidgets.QGraphicsEllipseItem( origin.x() - r * 5 , origin.y() - r * 5, r * 10, r * 10, distance_line )
        end_point = QtWidgets.QGraphicsEllipseItem( destination.x() - r * 5, destination.y() - r * 5, r * 10, r * 10, distance_line )
        distance_line.setZValue( self.z_value - 1 )
        distance = scene_coord.getDistance( origin, destination )
        distance_value = QtWidgets.QGraphicsTextItem( '%.2f km' % distance, distance_line )
        distance_value.setFont( QtGui.QFont( 'MS Shell Dlg 2', 25 * scene_coord.getRealResolution() ) )
        distance_value.setPos( destination.x(), destination.y() )
        distance_value.setRotation( -rotation_value )
        distance_value.setZValue( self.z_value )
        distance_line.setPen( QtGui.QPen( QtGui.QColor( 0, 0, 0 ), 6 * r ) )
        inside_line.setPen( QtGui.QPen( QtGui.QColor( 255, 255, 0 ), 4 * r ) )
        start_point.setPen( QtGui.QPen( QtGui.QColor( 255, 255, 0 ), 6 * r ) )
        end_point.setPen( QtGui.QPen( QtGui.QColor( 255, 255, 0 ), 6 * r ) )
        return distance_line
