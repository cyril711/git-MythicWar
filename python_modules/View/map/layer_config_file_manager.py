import os
import xml.etree.ElementTree
from python_modules.utils import global_helper 
from python_modules.config import Config
class LevelManager( object ):
    ''' Singleton to store the global configuration of the application '''
    __metaclass__ = global_helper.Singleton

    def __init__( self ):
        ''' Init the tile manager, responsible for reading config file '''
        # get all z-directory from Map tiles
        print('r',Config().instance.settings.value("map/google_tile_dir"))
        tiles_dir = os.path.join( Config().instance.settings.value("map/google_tile_dir"), 'Map' )
        print ('tiledir',tiles_dir)
        self.levels = [int( name ) for name in os.listdir( tiles_dir ) if os.path.isdir( os.path.join( tiles_dir, name ) )]

    def getMinLevel( self ):
        ''' return min level '''
        return min( self.levels )

    def getMaxLevel( self ):
        ''' return max level '''
        return max( self.levels )

class WebMercatorTileManager( object ):
    ''' Singleton to store the global configuration of the application '''
    __metaclass__ = global_helper.Singleton

    def __init__( self, tile_config_xml ):
        ''' Init the google map manager, responsible for reading the google map config file '''
        # load the XML DOM
        self.root = xml.etree.ElementTree.parse( tile_config_xml ).getroot()

    def getBasesMapName( self ):
        ''' return all base map name '''
        bases_map = []
        for base_map in self.root.findall( 'layer' ):
            bases_map.append( base_map.get( 'name' ) )
        return bases_map

    def getExtension( self, base_map_name ):
        ''' return extension from base map '''
        for base_map in self.root.findall( 'layer' ):
            if base_map.get( 'name' ) == base_map_name:
                return base_map.get( 'extension' )
        return None
