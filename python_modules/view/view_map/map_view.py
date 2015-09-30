from PyQt5 import QtCore, QtWidgets
import math as M
from python_modules.view.view_map.map_scene import MapScene
from python_modules.view.view_map.layer_manager import LayerManager
from python_modules.view.view_map.computing import Computing 
from python_modules.config import Config
#from foreground_items import ForegroundItems
#from touch_event import TouchEvent
#from marker_item import MarkerItem
from python_modules.view.view_map.map_item import TempleItem

from python_modules.utils import projection
from PyQt5.Qt import QMenu, QAction, QRectF, QCursor, QBrush, QColor,\
    QPen, QPointF

from PyQt5.QtWidgets import QGraphicsEllipseItem
from enum import Enum

from python_modules.model.univers import ActionType

class Mode (Enum):
        Normal = 0
        Move = 1
        Attack = 2

class MapWindow( QtWidgets.QGraphicsView ):

    level_changed = QtCore.pyqtSignal( int )
    minus_level = QtCore.pyqtSignal()
    major_level = QtCore.pyqtSignal()
    center_changed = QtCore.pyqtSignal( float, float )
    update_labels = QtCore.pyqtSignal( float, float, int, int, int, int )
    rotation_changed = QtCore.pyqtSignal( int )
    double_click = QtCore.pyqtSignal( QtCore.QPointF )
    contextMenu = QtCore.pyqtSignal( QtCore.QPointF, QtWidgets.QMenu )
    mode_free = QtCore.pyqtSignal()
    #move_heroes = QtCore.pyqtSignal()
    def __init__( self,univers, parent=None ):
        ''' Initialisation of the QGraphicsView '''
        super( MapWindow, self ).__init__( parent )
        self.univers = univers
        self.univers.askForMap.connect(self.goToHeros)
        # scene coordinates
        self.scene_coord = None
        self.settings = Config().instance.settings
        # add a scene
        self.scene = MapScene( self )
        self.setScene( self.scene )
#         zoom_in = QShortcut()
#         zoom_in.setKey("Ctrl+A")
#         zoom_in.activated.connect.onZoomIn()
#         zoom_out = QShortcut()
#         zoom_out.setKey("Ctrl+Q")
#         zoom_out.activated.connect.onZoomOut()
        # init the flags
        self.setFlags()

        # manual drag
        self.pressed_pos = None
        self.origin = None
        self.destination = None
        self.cursor_shape = self.viewport().cursor().shape()

        # add a layer manager
        self.manager = LayerManager( self.scene,self.univers, self )


        # update tiles with timer
        self.timer = QtCore.QTimer()
        # self.timer.setSingleShot( True )
        self.timer.timeout.connect( self.updateTiles )
        self.timer.start( 50 )

        # calculations made outside
        self.computing = Computing()

        # init scale on foreground
        #self.foreground_items = ForegroundItems()
        self.rotate_value = 0

        # center mode
        self.mode = None
        self.observer_x, self.observer_y = 0, 0

        self.mode_action = Mode.Normal
        # members variables used in viewportEvent
        #self.touch_event = TouchEvent( self )
        self.drag = {}
        self.distances = []
        self.distance_line = QtWidgets.QGraphicsLineItem()
        self.draw_distance = False

        #move warriors
        self.dispatch_item = None
        self.shape = "Circle"
        self.changeSizeMoveShape = False

        self.width_movable_region = 100000
        self.height_movable_region = 100000
        self.marker_item = None
        self.marker_items = []

        layers_list = self.settings.value("map/instanciated_layers",[])
        first = True
        print ('len layer_list',len(layers_list), layers_list)
        for layer in layers_list:
            print ('layer list item : ',layer)
            self.onLayerAdded(layer,first)
            first = False
            
        self.current_action  = {}
    def viewportEvent( self, event ):
        ''' viewport event manager '''
        if event.type() == QtCore.QEvent.TouchBegin or event.type() == QtCore.QEvent.TouchUpdate or event.type() == QtCore.QEvent.TouchEnd:
            if self.scene_coord and self.mode == 'Free' and not self.draw_distance :
                self.touch_event.touchEvent( event )
            return True
        return super( MapWindow, self ).viewportEvent( event )



    def setFlags( self ):
        ''' set graphics view flags '''
        # remove scrollbar displaying
        #self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        #self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )

        # scale regarding the cursor
        self.setTransformationAnchor( QtWidgets.QGraphicsView.AnchorViewCenter )
        # resize maintaining view center
        self.setResizeAnchor( QtWidgets.QGraphicsView.AnchorViewCenter )
        # OpenGL viewport
        #if Config().opengl_isActivated:
        #    pass # self.setViewport( QtOpenGL.QGLWidget( QtOpenGL.QGLFormat( QtOpenGL.QGL.SampleBuffers ) ) )
        # move entities without streak
        self.setViewportUpdateMode( QtWidgets.QGraphicsView.FullViewportUpdate )
        # to send cursor informations
        self.setMouseTracking( True )
        self.setDragMode( QtWidgets.QGraphicsView.ScrollHandDrag )

#     def keyPressEvent(self, event):
#         
#         if event.key() == QtCore.Qt.Key_Control:
#             print ('press Ctrl')
#             self.setDragMode( QtWidgets.QGraphicsView.NoDrag )        
#     def keyReleaseEvent(self, event):
#             
#         if event.key() == QtCore.Qt.Key_Control:
#             print ('press Ctrl')
#             self.setDragMode( QtWidgets.QGraphicsView.ScrollHandDrag )        
        

    def initGraphicsView( self, projection_name, level, lat, lon ):
        ''' init the graphics view with the projection '''

        # set the QGraphicsScene
        self.scene_coord = getattr( projection, str( projection_name ) )()
        self.scene_coord.setLevel( level )
        self.setSceneRect( self.scene_coord.getSceneRect() )
        
        # init view's scale
        scale_factor = 1.0 / self.scene_coord.getResolution()
        self.scale( scale_factor, scale_factor )

        # init view's position
        self.centerOnLatLong( lat, lon )

    def viewFromScratch( self ):
        ''' reset if the layers widget become empty again '''
        self.resetTransform()
        self.scene_coord.reset()
        self.scene_coord = None
        self.update_labels.emit( 0, 0, 0, 0, 0, 0 )

#     def drawForeground( self, painter, rect ):
#         ''' draw the scale on the foreground '''
#         if self.scene_coord:
#             p = self.mapToScene( 0, 0 )
#             lat1, lon1 = self.scene_coord.MetersToLatLon( p.x(), p.y() )
#             p = self.mapToScene( self.width(), 0 )
#             lat2, lon2 = self.scene_coord.MetersToLatLon( p.x(), p.y() )
#             self.foreground_items.paintScale( painter, -self.rotate_value, lat1, lon1, lat2, lon2, self.width(), self.height(), self.scene_coord.getResolution() )

    def updateTiles( self ):
        ''' update displaying '''

        if 'dist' in self.drag:
            if self.drag['dist'].manhattanLength() < 100:
                self.drag = {}
                self.timer.start( 50 )
            else:
                length = self.drag['end'] - self.drag['begin']
                drag_pos = QtCore.QPointF( self.drag['dist'].x(), self.drag['dist'].y() ) # QPoint to QPointF, required to centerOn
                self.centerOn( self.getSceneViewCenter() + drag_pos )
                self.drag['dist'] = self.drag['dist'] / ( 1 + length )
                self.timer.start( 10 )
        self.manager.update( self.getSceneBoundingBox() )

    def centerOnLatLong( self, lat, lon ):
        ''' center the view on the latitude/longitude parameters '''
        if self.scene_coord:
            mx, my = self.scene_coord.LatLonToScene( lat, lon )
            self.centerOn( mx, my )

    def goToHeros (self,lat,lon):
        self.centerOnLatLong(lat, lon)
        

    def getSceneViewCenter( self ):
        ''' return the point in the view center '''
        return self.mapToScene( self.viewport().rect() ).boundingRect().center() # more accurate with boundingRect

    def centerOnObserver( self ):
        ''' center the view on the observer '''
        if self.viewport().cursor().shape() == QtCore.Qt.ClosedHandCursor:
            self.mode_free.emit() # on se deplace dans la scene : passage automatique en mode 'Free'
        else:
            self.centerOn( self.observer_x, self.observer_y )
            self.update()

    def getSceneBoundingBox( self ):
        ''' get the part of the scene viewable '''
        rect_viewport = QtCore.QRect( 0, 0, self.width(), self.height() )
        poly_scene = self.mapToScene( rect_viewport )
        return poly_scene.boundingRect()

    def wheelEvent( self, event=None, scale_center=None, scale_factor=None ):
        ''' Scale event '''
        if self.scene_coord:
            if event:
                scale_factor = 1
                if event.angleDelta().y() > 0:
                    scale_factor += ( self.scene_coord.getResolution() / self.scene_coord.getLevelResolution( self.scene_coord.getLevel() + 1 ) ) / 50
                else:
                    scale_factor -= ( self.scene_coord.getLevelResolution( self.scene_coord.getLevel() - 1 ) / self.scene_coord.getResolution() ) / 50
                self.scale( scale_factor, scale_factor )
            else:
                center_before_scale = self.mapToScene( scale_center.toPoint() )
                self.scale( scale_factor, scale_factor )
                center_after_scale = self.mapToScene( scale_center.toPoint() )
                shift = center_after_scale - center_before_scale
                self.centerOn( self.getSceneViewCenter() - shift )

            # update items resolution
            self.scene_coord.setRealResolution( self.scene_coord.getRealResolution() / scale_factor )
            res = self.scene_coord.getRealResolution()
            for item in self.marker_items:
                item.setScale( res )

            current_level = self.scene_coord.getLevel()
            view_scale, new_level = self.computing.hasToChangeLevel( self.transform(), self.scene_coord.getResolution(), self.scene_coord.getLevelResolution( current_level - 1 ), current_level )
            if new_level:
                self.updateLevel( view_scale, new_level )

    def keyPressEvent(self, event):
        if event.key()== QtCore.Qt.Key_Control:
            self.setDragMode( QtWidgets.QGraphicsView.RubberBandDrag )
        if self.dispatch_item != None : 
            if event.key() == QtCore.Qt.Key_Shift :
                self.changeSizeMoveShape = True
            elif  event.key() == QtCore.Qt.Key_A and  self.changeSizeMoveShape == True :
                self.width_movable_region = self.width_movable_region+ 100000
                self.height_movable_region = self.height_movable_region+ 100000
                self.dispatch_item.setRect(QRectF(-self.width_movable_region/2,-self.height_movable_region/2,self.width_movable_region,self.height_movable_region))
            elif  event.key() == QtCore.Qt.Key_Q and  self.changeSizeMoveShape == True :
                self.width_movable_region = self.width_movable_region- 100000
                self.height_movable_region = self.height_movable_region- 100000                
                self.dispatch_item.setRect(QRectF(-self.width_movable_region/2,-self.height_movable_region/2,self.width_movable_region,self.height_movable_region))
    def keyReleaseEvent(self, event):
        if event.key()== QtCore.Qt.Key_Control:
            self.setDragMode( QtWidgets.QGraphicsView.ScrollHandDrag  )

        if self.dispatch_item != None : 
            if event.key() == QtCore.Qt.Key_Shift :
                self.changeSizeMoveShape = False

    def mousePressEvent( self, event ):
        ''' allows target or view displacement '''

        print ('mouse press event')
        super( MapWindow, self ).mousePressEvent( event )
        if self.mode_action == Mode.Normal:
            if self.scene_coord:
                if self.draw_distance and not self.origin:
                    self.origin = self.destination = self.mapToScene( event.pos() )

        elif self.mode_action == Mode.Move :
            print ('....action move')
            if len(self.univers.selectedWarriors())> 1:
                self.scene.removeItem(self.dispatch_item)
                self.dispatch_item = None
                l_positions = self.univers.dispatchCircleWarriors (self.scene_coord,self.mapToScene( event.pos() ),self.width_movable_region/2)
            else:
                print ('type de left',type(self.univers.selectedWarriors()),len(self.univers.selectedWarriors()))
                mx,my = self.mapToScene( event.pos()).x(),self.mapToScene( event.pos()).y()
                pos_dest = self.scene_coord.SceneToLatLon(mx,my)
                pos_dest = QPointF(-pos_dest[0],pos_dest[1])
                l_positions = [pos_dest]

            self.univers.addAction(self.current_action["type"],self.current_action["value"],self.univers.getSelectionList(),l_positions)
            self.mode_action = Mode.Normal
        elif self.mode_action == Mode.Attack:
            pass
            
        elif self.mode_action == Mode.Heal :
            pass
            
        
 
#         else:
#             # on fait le dispatch
#             print ('on fait le dispatch on est en coordonne scene')
#             self.univers.dispatchCircleWarriors (self.scene_coord,self.mapToScene( event.pos() ),self.width_movable_region/2)
# 
# 
#             self.scene.removeItem(self.moveShape)            
#             self.moveShape = None

    def mouseMoveEvent( self, event ):
        ''' allows target or view displacement or carrier displacement '''
        super( MapWindow, self ).mouseMoveEvent( event )
        if self.origin:
            self.destination = self.mapToScene( event.pos() )
            if self.distance_line.scene() == self.scene:
                self.scene.removeItem( self.distance_line )
            self.distance_line = self.computing.drawDistance( self.origin, self.destination, self.scene_coord, self.rotate_value )
            self.scene.addItem( self.distance_line )
        elif self.scene_coord:
            self.collectAndSendCursorInformations()
        if self.mode_action == Mode.Move and len(self.univers.selectedWarriors())> 1:
            if self.changeSizeMoveShape == True : 
                self.incrSizeMoveShape = self.mapToScene( event.pos() ) - self.dispatch_item.pos()
                self.width_movable_region = self.width_movable_region + self.incrSizeMoveShape.x()
                self.height_movable_region= self.width_movable_region
                self.dispatch_item.setRect(QRectF(-self.width_movable_region/2,-self.height_movable_region/2,self.width_movable_region,self.height_movable_region))
            else:
                pos = self.mapToScene( event.pos() )
                #self.moveShape.setRect(QRectF(pos.x(),pos.y(),self.width_movable_region*1000,self.height_movable_region*1000))
                self.dispatch_item.setPos(QPointF(pos.x(),pos.y()))
                item = self.itemAt(event.pos())
                if item and type(item) == TempleItem: 
                    self.dispatch_item.hide()
                else:
                    self.dispatch_item.show()
    def mouseReleaseEvent( self, event ):
        ''' allows target or view displacement '''
        super( MapWindow, self ).mouseReleaseEvent( event )
        if self.scene_coord:
            self.pressed_pos = None
            if self.origin:
                if event.button() != QtCore.Qt.RightButton:
                    self.origin = self.destination
                    self.distances.append( self.distance_line )
                    self.distance_line = QtWidgets.QGraphicsLineItem()
                else:
                    if self.distance_line.scene() == self.scene:
                        self.scene.removeItem( self.distance_line )
                    if len( self.distances ):
                        line_item = self.distances.pop( len( self.distances ) - 1 )
                        line = line_item.line()
                        self.origin = line.p1()
                        if line_item.scene() == self.scene:
                            self.scene.removeItem( line_item )
                        if not len( self.distances ):
                            self.origin = self.destination = None
            elif event.button() == QtCore.Qt.LeftButton:
                self.updateLatLongCenter()
        if event.button() == QtCore.Qt.LeftButton:
            self.manager.releaseEvent( event.pos(), self.mapToScene( event.pos() ) )



    def menuHeros(self,event):
        #====== Menu Move ==========
        print ('context menu event de heros')
        menu_move = QMenu("Move")
        moveNormal = QAction("Normal",None)
        moveNormal.setData(1.0)
        moveNormal.triggered.connect(self.onActionMove)
        menu_move.addAction(moveNormal)
        moveSlow= QAction("Slow",None)
        moveSlow.setData(0.5)
        menu_move.addAction(moveSlow)
        moveVerySlow= QAction("Very Slow",None)
        moveVerySlow.setData(0.25)
        menu_move.addAction(moveVerySlow)
        moveFast= QAction("Fast",None)
        moveFast.setData(2.0)
        menu_move.addAction(moveFast)
        moveVeryFast= QAction("Very Fast",None)
        moveVeryFast.setData(4.0)
        menu_move.addAction(moveVeryFast)
        actionTeleport= QAction("Teleport",None)
        menu_move.addAction(actionTeleport)        
        #========== Menu Actions ========
        menu_actions = QMenu("Action")
        actionAttack= QAction("Attack",None)
        menu_actions.addAction(actionAttack)
        actionHeal= QAction("Soigne",None)
        menu_actions.addAction(actionHeal)        
        
        #======== MENU GENERAL ================
        menu = QMenu()
        menu.addMenu(menu_move)
        menu.addMenu(menu_actions)
        actionPlacement= QAction("Placement",None)
        menu.addAction(actionPlacement)
        action_running = False
        for w in self.univers.selectedWarriors():
            if w.attribs['status']!= "Attente":
                action_running = True
                
        if action_running == True :
            actionCancel= QAction("Cancel",None)
            menu.addAction(actionCancel)            
                
        if len(self.univers.selectedWarriors())==1 : 
            if self.univers.selectedWarriors()[0].attribs['HP']== 0:
                actionRebirth= QAction("Rebirth",None)
                menu.addAction(actionRebirth)  
            else:
                actionKill= QAction("Kill",None)
                menu.addAction(actionKill)
                    
        #menu.exec_(event.screenPos())
        #event.accept()
        menu.exec_(event.globalPos())


    def onActionMove(self):
        self.sender().data()
        self.current_action["type"]= ActionType.MoveToPosition
        self.current_action["value"] = self.sender().data()
        if len(self.univers.selectedWarriors()) > 1 : 
            if self.dispatch_item!= None : 
                self.scene.removeItem(self.moveShape)
            self.dispatch_item = QGraphicsEllipseItem()
            brush = QBrush(QColor(255,0,0,125))
            pen = QPen(QColor(255,0,0))
            self.dispatch_item.setRect(QRectF(-self.width_movable_region/2,-self.height_movable_region/2,self.width_movable_region,self.height_movable_region))
            self.dispatch_item.setPen(pen)
            self.dispatch_item.setBrush(brush)
            self.dispatch_item.setZValue(2)
            self.scene.addItem(self.dispatch_item)
        self.mode_action = Mode.Move
        
    def contextMenuEvent(self,event):
        #super(MapWindow,self).contextMenuEvent(event)
        
        if len(self.univers.selectedWarriors()) != 0 : 
            self.menuHeros(event)
            
     
#                 testAction = QAction('Move', None)
#                 testAction.triggered.connect(self.onMoveMode)

#         actionAddTemple = QAction('Add Temple', None)
#         actionAddTemple.triggered.connect(self.onAddTemple)
#         menu.addAction(actionAddTemple)
#         menu.exec_(event.globalPos())
            
    def onAddTemple (self):
        print ('add temple')
        #todo
        return False


    
       


#     def contextMenuEvent( self, event ):
#         super(MapWindow,self).contextMenuEvent(event)
#         print ('k')
#         if not self.draw_distance :
#             context_menu = QtWidgets.QMenu( self )
#             styleSheet = \
#             '''
#             QMenu{ background-color:white; border:1px solid black;}
#             QMenu::item {padding:2px 25px 2px 20px;background-color:transparent;}
#             QMenu:item::selected{border-color:darkblue;background:#33CCBB;}
#             '''
#             context_menu.setStyleSheet( styleSheet )
# #             location_marker = QtWidgets.QAction( 'Add a location marker', context_menu )
# #             pos = self.mapToScene( event.pos() )
# #             location_marker.setObjectName( str( pos.x() ) + ' ' + str( pos.y() ) )
# #             location_marker.triggered.connect( self.onLocationMarkerAdded )
# #             context_menu.addAction( location_marker )
# 
# #             res = self.scene_coord.getRealResolution()
# #             for row, item in enumerate( self.marker_items ):
# #                 rect = QtCore.QRectF( item.pos(), QtCore.QSizeF( item.pixmap().width() * res, item.pixmap().height() * res ) )
# #                 if rect.contains( self.mapToScene( event.pos() ) ):
# #                     remove_marker = QtWidgets.QAction( 'Remove marker', context_menu )
# #                     remove_marker.setObjectName( str( row ) )
# #                     remove_marker.triggered.connect( self.onRemoveMarker )
# #                     context_menu.addAction( remove_marker )
#             context_menu.addSeparator()
#             self.contextMenu.emit( self.mapToScene( event.pos() ), context_menu )
#             context_menu.exec_( event.globalPos() )

    def mouseDoubleClickEvent( self, event ):
        ''' change tracking point or carrier position'''
        self.double_click.emit( self.mapToScene( event.pos() ) )

    def resizeEvent( self, event ):
        ''' window is resizing '''
        super( MapWindow, self ).resizeEvent( event )
        if self.scene_coord:
            self.updateLatLongCenter()

    def updateLatLongCenter( self ):
        ''' centering the view after latitude/longitude change '''
        scene_bounding_box = self.getSceneBoundingBox()
        center_position_x, center_position_y = self.computing.getCenter( scene_bounding_box )
        lat, lon = self.scene_coord.MetersToLatLon( center_position_x, center_position_y )
        self.center_changed.emit( lat, lon )

    def updateLevel( self, scale, level, fromGraphicsView=True ):
        ''' update the current level '''
        self.scale( scale, scale )
        self.scene_coord.setLevel( level )
        if fromGraphicsView:
            self.level_changed.emit( level )
        else:
            self.scene_coord.setRealResolution( self.scene_coord.getResolution() ) # update items resolution
            for item in self.marker_items:
                item.setScale( self.scene_coord.getRealResolution() )

    def collectAndSendCursorInformations( self ):
        ''' update the labels value '''
        # mouse position
        mouse_position = self.mapToScene( self.mapFromGlobal( self.cursor().pos() ) )
        # lat long
        lx, ly = self.scene_coord.MetersToLatLon( mouse_position.x(), mouse_position.y() )
        # meters
        mx, my = self.scene_coord.MetersToScene( mouse_position.x(), mouse_position.y() )
        # tiles
        tx, ty = self.scene_coord.MetersToTile( mouse_position.x(), mouse_position.y() )

        self.update_labels.emit( lx, ly, mx, my, tx, ty )

#     def onLocationMarkerAdded( self ):
#         pixmap = QtGui.QPixmap( ':/icons 16x16/resources/16x16/marker.png' )
#         self.marker_item = MarkerItem( pixmap )
#         self.marker_item.setZValue( sys.maxint )
#         res = self.scene_coord.getRealResolution()
#         self.marker_item.setScale( res )
# 
#         sender = self.sender()
#         x, y = sender.objectName().split( ' ' )
#         rect = self.marker_item.boundingRect()
#         self.marker_item.setPos( float( x ) - 0.5 * rect.width(), float( y ) - rect.height() )
# 
#         self.scene.addItem( self.marker_item )
# 
#         self.marker_items.append( self.marker_item )
# 
#     def onRemoveMarker( self ):
#         sender = self.sender()
#         item = self.marker_items[int( sender.objectName() )]
#         if item:
#             if item.scene() == self.scene:
#                 self.scene.removeItem( item )
#             self.marker_items.remove( item )

    def onLevelChanged( self, level ):
        ''' scaling after a change of spin box level '''
        if self.scene_coord:
            scale = self.computing.getViewScale( self.transform(), self.scene_coord.getLevelResolution( level ) )
            self.updateLevel( scale, level, False )

    def onLastLayerRemoved( self, layer ):
        ''' the last layer was removed (slot) '''
        self.onLayerRemoved( layer )
        self.viewFromScratch()

    def onLayerAdded( self, layer, first ):
        ''' a layer was added (slot) '''

        if first == True:
            print ('init graphicsView')
            self.initGraphicsView( 'WebMercator', int(self.settings.value("map/initial_level",6)), float(self.settings.value("map/initial_lat",48.858093)), float(self.settings.value("map/initial_lon",2.294694)) )
        self.manager.addLayer( layer )
        print ('add layer finished ',layer)
    def onLayerRemoved( self, layer ):
        ''' a layer was removed (slot) '''
        self.manager.removeLayer( layer )

    def onRotationSliderValueChanged( self, value ):
        ''' update rotation value '''
        self.rotate( value )
        self.rotate_value += value
        for item in self.marker_items:
                item.setRotation( -self.rotate_value )
        self.manager.updateRotation( self.rotate_value )

    def onResetRotation( self ):
        ''' reset rotaiton value '''
        self.rotate( -self.rotate_value )
        self.rotate_value = 0
        for item in self.marker_items:
                item.setRotation( self.rotate_value )
        self.manager.updateRotation( self.rotate_value )

    def updateRotation( self, rotation_value ):
        self.rotate( rotation_value )
        self.rotate_value += rotation_value
        for item in self.marker_items:
                # item.setRotation( rotation_value )
            item.setRotation( -self.rotate_value )
        self.rotation_changed.emit( self.rotate_value )
        self.manager.updateRotation( self.rotate_value )

    def onCarrierPositionChanged( self, c_mx, c_my, alt=0.0 ):
        ''' update observer coordinates if it's the carrier '''
        if self.mode == 'CenterOnCarrierOrientNorth' or self.mode == 'CenterOnCarrier':
            self.observer_x, self.observer_y = c_mx, c_my
            self.centerOnObserver()

    def onCarrierRotationChanged( self, rotation_value ):
        ''' update observer rotation if needed '''
        if self.mode == 'CenterOnCarrier' or self.mode == 'CenterOnBarycenter':
            rotation_value = M.degrees( -rotation_value )
            self.rotate( rotation_value - self.rotate_value )
            self.rotate_value = rotation_value
            self.rotation_changed.emit( self.rotate_value )
            self.manager.updateRotation( self.rotate_value )

    def onTargetPositionChanged( self, mx, my ):
        ''' update observer coordinates if it's the target'''
        if self.mode == 'CenterOnTarget':
            self.observer_x, self.observer_y = mx, my
            self.centerOnObserver()

    def onBarycenterPositionChanged( self, c_mx, c_my, mx, my ):
        ''' update observer coordinates if it's baryenter between carrier and target '''
        if self.mode == 'CenterOnBarycenterOrientNorth' or self.mode == 'CenterOnBarycenter':
            self.observer_x, self.observer_y = ( c_mx + mx ) / 2.0, ( c_my + my ) / 2.0
            self.centerOnObserver()
            self.optimizeObserverLevel( c_mx, c_my, mx, my )

    def optimizeObserverLevel( self, c_mx, c_my, mx, my ):
            scene_bounding_box = self.getSceneBoundingBox()
            if not scene_bounding_box.contains( c_mx, c_my ) or not scene_bounding_box.contains( mx, my ):
                self.minus_level.emit()
#            else:
#                res = self.scene_coord.getRealResolution()
#                res_level_up = self.scene_coord.getLevelResolution( self.scene_coord.getLevel() + 1 )
#                scale_factor = res_level_up / res
#                w, h = scene_bounding_box.width(), scene_bounding_box.height()
#                scene_bounding_box = scene_bounding_box.adjusted( 0.5 * w * scale_factor, 0.5 * h * scale_factor, -0.5 * w * scale_factor, -0.5 * h * scale_factor )
#                if scene_bounding_box.contains( c_mx, c_my ) or scene_bounding_box.contains( mx, my ):
#                    self.major_level.emit()

    def setMode( self, mode ):
        ''' update observer mode '''
        self.mode = mode
        if self.mode == 'CenterOnCarrierOrientNorth' or self.mode == 'CenterOnTarget' or self.mode == 'CenterOnBarycenterOrientNorth':
            self.onResetRotation()
            self.rotation_changed.emit( self.rotate_value )

    def getManager( self ):
        ''' return the layer manager '''
        return self.manager

#     def getTouchEvent( self ):
#         ''' return the touch event manager '''
#         return self.touch_event

    def getSceneCoord( self ):
        ''' return the projection manager '''
        return self.scene_coord

    def setDrawDistance( self, activated ):
        self.draw_distance = activated
        if not self.draw_distance:
            for line_item in self.distances:
                if line_item.scene() == self.scene:
                    self.scene.removeItem( line_item )
            self.distances = []
            self.origin = self.destination = None
            if self.distance_line.scene() == self.scene:
                self.scene.removeItem( self.distance_line )
            self.viewport().setCursor( self.cursor_shape )
        else:
            self.cursor_shape = self.viewport().cursor().shape()
            self.viewport().setCursor( QtCore.Qt.CrossCursor )

#     def updateSunlightDirection( self, azimuth=None ):
#         self.foreground_items.setSunlightDirection( azimuth )
