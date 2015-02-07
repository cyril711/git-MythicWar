from PyQt5 import QtCore
from python_modules.view.view_map.layer import Layer
#import map_items.entity_item

from python_modules.view.view_map import layer_adapter
from python_modules.view.view_map.map_item import TempleItem, HerosItem
#import shapes
import math
from python_modules.config import Config

#import property_delegate
#import menu_item

class KingdomItemAdapter( layer_adapter.AbstractLayerAdapter ):
    ''' Adapter for using properties and animation '''
    def __init__( self, object_to_animate ):
        super( KingdomItemAdapter, self ).__init__( object_to_animate )

#     @QtCore.pyqtProperty( QtGui.QColor )
#     def carrier_color( self ):
#         return self.o.items['carrier'].color
#     @carrier_color.setter
#     def carrier_color( self, value ):
#         self.o.items['carrier'].color = value
#         self.o.items['carrier'].update()
# 
#     @QtCore.pyqtProperty( int )
#     def carrier_size( self ):
#         return self.o.items['carrier'].size
#     @carrier_size.setter
#     def carrier_size( self, value ):
#         self.o.items['carrier'].prepareGeometryChange()
#         self.o.items['carrier'].size = value
#         self.o.items['carrier'].update()


   
   

class KingdomLayer( Layer ):

#     properties = ['carrier_color', 'carrier_size']
# 
#     special_delegates = {
#                          'carrier_color' : property_delegate.ColorPropertyDelegate(),
#                          }

    @staticmethod
    def name( cls ):
        ''' return name of layer without instantied itself '''
        return 'Kingdom Layer'

    @staticmethod
    def projection( cls ):
        ''' return projection of layer without instantied itself '''
        return None

    def __init__( self, scene, z_value, model, scene_coord, parent=None ):
        ''' initialisation of the carrier pod layer '''
        super( KingdomLayer, self ).__init__( scene, z_value, scene_coord, parent )

        # init member variables
        self.model = model
        self.mx, self.my = 0, 0
        self.elapsed_time = 0.0
        self.dial_action, self.slider_action = None, None
        self.items_heros = []
        self.items_temples = []
        # init
        #self.instantiateItems()
        self.instantiateTemplesItems(self.model.temples)
        self.connections()

        # adapter
        self.adapter = KingdomItemAdapter( self )
        


    def connections( self ):
        ''' make connections between simulation and items '''
        #view = self.parent().parent()
        self.model.filtered_changed.connect (self.instantiateHerosItems)
        self.parent().parent().move_heroes.connect(self.instantiateHerosItems)
        self.model.selection_updated.connect (self.reloadHerosItems)
    def reloadHerosItems (self):
        print ('relods heros items')
        for heros_item in self.items_heros :
            if heros_item.isSelected()!= heros_item.heros.selected :
                heros_item.setSelected(heros_item.heros.selected)
    def disconnections( self ):
        #self.simulation.carrier_position.disconnect()
        pass

    def instantiateTemplesItems( self ,temples):
        ''' instantiates items and adds them to the scene '''
        for key,value in zip(temples.keys(),temples.values()):
            t_item =  TempleItem(value,10)
            
            try:
                lat = value.position.x()
                lon = value.position.y()
            except KeyError :
                lat = float(Config().instance.settings.value("map/initial_lat"))
                lon = float(Config().instance.settings.value("map/initial_lon"))
            mx,my = self.scene_coord.LatLonToScene(lat,lon)

            #ittt.setScale( self.scene_coord.getResolution() )
            t_item.setPos( mx,my )
            t_item.setZValue( self.z_value+10 )
            self.items_temples.append( t_item)
            self.scene.addItem( t_item )

                    #self.items[kingdom.id].setPos(0.0, -6261721.357121639)


                    #self.items[kingdom.id].item_change_callback = self.onKingdomPositionChanged#self.onCarrierItemChange
                   # self.items[kingdom.id].position_changed.connect(self.onKingdomPositionChanged)

    def instantiateHerosItems (self):
        for heros_item in self.items_heros :
            self.scene.removeItem(heros_item)
        self.items_heros.clear()
        for heros in self.model.filteredWarriors():
            if heros.attribs['place'] == '':
                try:
                    lat = heros.attribs['latitude']
                    lon = heros.attribs['longitude']
                except KeyError :
                    lat = 0.0
                    lon = 0.0
                lat = float(Config().instance.settings.value("map/initial_lat"))
                lon = float(Config().instance.settings.value("map/initial_lon"))
                mx,my = self.scene_coord.LatLonToScene(lat,lon)
                item = HerosItem(heros,50)
                item.setPos( mx,my )
                item.setZValue( self.z_value+10 )
                self.items_heros.append(item)
                self.scene.addItem( item)

    def onKingdomPositionChanged (self,kingdom_id,mx,my):
        lat, lon = self.scene_coord.SceneToLatLon( mx, my)
        lat = math.radians( lat )
        lon = math.radians( lon )
        self.model.updateKingdom(kingdom_id,lat,lon)

#     def onCarrierPositionChanged( self, mx, my, alt ):
#         ''' update items position '''
#         self.items['carrier'].setFlag( QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False )
#         self.items['carrier'].setPos( mx, my )
#         self.items['carrier'].setFlag( QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True )
#         self._setCarrierVector( mx, my )
#         self._setTrajectory( mx, my )
#         # retains position
#         self.mx, self.my = mx, my



#     def contextMenu( self, pos, menu ):
#         if self.isUnderMouse( pos, self.items['temple'] ):
#             self.slider_action = menu_item.SliderAction( 'Define Altitude :' )
#             self.slider_action.slider().valueChanged.connect( self.changeCarrierAlt )
#             self.slider_action.slider().setValue( self.carrier_alt )
#             menu.addAction( self.slider_action )
#             menu.addSeparator()
#             self.dial_action = menu_item.DialAction( 'Define Rotation :' )
#             self.dial_action.dialBox().valueChanged.connect( self.rotateCarrier )
#             self.dial_action.dialBox().setValue( self.items['carrier'].rotation )
#             if self.items['carrier'].touch_mode == True:
#                 self.dial_action.dialBox().setMinimumSize( 150, 150 )
#             menu.addAction( self.dial_action )


    def doubleClick( self, pos ):
#         lat, lon = self.scene_coord.SceneToLatLon( pos.x(), pos.y() )
#         self.simulation.publishCamera( M.radians( lat ), M.radians( lon ) )
        pass

    

    def setTouchMode( self, value ):
        self.items['temple'].touch_mode = value


   

#     def _convertRGLPToScene( self, pts_rglp, observer_transform, earth_model, carier_posRT, groundHeight ) :
#         ''' converti un pts exprime dans le repere RGLP dans le repere de la scene '''
#         # conversion RGLP -> repere terrestre
#         pts_RT = observer_transform.positionRglpToRt( pts_rglp )
#         # calcul de la distance entre carrier et l intersection des rayons avec la terre
#         dist = earth_model.intersectionDistanceToGround( pegase.Vector3( carier_posRT ), pts_RT - carier_posRT, groundHeight )
#         if dist >= 0 :
#             pts_on_earth = pegase.Vector3( carier_posRT ) + ( pegase.Vector3( pts_RT - carier_posRT ).normalize() * dist )
#             pts_geo = earth_model.positionRtToGeo( pts_on_earth )
#             lat_merc, lon_merc = self.scene_coord.LatLonToScene( M.degrees( pts_geo.x ), M.degrees( pts_geo.y ) )
#             return QtCore.QPoint( lat_merc, lon_merc ), dist, pts_RT
#         else :
#             return QtCore.QPoint( 0, 0 ), dist, pts_RT

    def _setCarrierVector( self, mx, my ):
        ''' update vector shape '''
        # vector length
        if self.items['speed_vector'].elapsed_time != 0:
            length = ( self.items['speed_vector'].forecasting / self.items['speed_vector'].elapsed_time ) * M.sqrt( ( mx - self.mx ) ** 2 + ( my - self.my ) ** 2 )
            length /= self.scene_coord.getRealResolution()
            self.items['speed_vector'].setArrow( length, 0.25 * length, 0.5 * length )

        # vector rotation
        north_line = QtCore.QLineF( self.mx, self.my, self.mx, self.my - 1 )
        current_line = QtCore.QLineF( self.mx, self.my, mx, my )
        if current_line.dx() != 0 and current_line.dy() != 0 :
            self.items['speed_vector'].rotation = current_line.angleTo( north_line )


