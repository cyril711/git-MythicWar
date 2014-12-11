from python_modules.utils.globalmaptiles import GlobalMercator
from PyQt5.uic.Compiler.qtproxies import QtCore
from PyQt5.Qt import QRectF, QPointF
import math as M

class WebMercator ():
    R = 6378.137
    def __init__(self):
        print ('PROJECTION CONSTRUCtEUR')
        self.mercator = GlobalMercator()
        self.projection_name = 'WebMercator'
        self.level = 0
        self.real_resolution = 0
    def getProjectionName (self):
        return self.projection_name
    
    def getSceneRect (self):
        return QRectF (-9000000,-9000000,2*9000000,2*9000000)
    
    def getSceneTileBounds (self,tx,ty):
        minx,miny,maxx,maxy = self.mercator.TileBounds(tx, ty, self.level)
        return minx,-maxy,maxx,-miny
    
    def getLevelSceneTileBound (self,tx,ty,level):
        minx,miny,maxx,maxy = self.mercator.TileBounds(tx, ty, level)
        return minx,-maxy,maxx,-miny 
    
    def getTilePos (self,tx,ty):
        x,_,_,y = self.mercator.TileBounds(tx, ty, self.level)
        return QPointF(x,-y)
    
    def getLevelTilePos (self,tx,ty,level):
        x,_,_,y = self.mercator.TileBounds(tx, ty, level)
        return QPointF(x,-y)
    
    def getTilesToLoad (self,rect):
        top_left_x = rect.x()
        top_left_y = -(rect.y() + rect.height())
        bottom_right_x = rect.x()+ rect.width() 
        bottom_right_y = -rect.y()
        tminx,tminy = self.mercator.MetersToTile (top_left_x,top_left_y,self.level)
        tmaxx,tmaxy = self.mercator.MetersToTile (bottom_right_x,bottom_right_y,self.level)
        
        return tminx,tminy,tmaxx,tmaxy
    
    def getLevelTilesToLoad (self,rect,level):
        top_left_x = rect.x()
        top_left_y = -(rect.y() + rect.height())
        bottom_right_x = rect.x()+ rect.width() 
        bottom_right_y = -rect.y()
        tminx,tminy = self.mercator.MetersToTile (top_left_x,top_left_y,level)
        tmaxx,tmaxy = self.mercator.MetersToTile (bottom_right_x,bottom_right_y,level)
        return tminx,tminy,tmaxx,tmaxy
    
    def getResolution (self):
        return self.mercator.Resolution(self.level)
    
    def getLevelResolution (self,level):
        return self.mercator.Resolution(level)
    
    def getRealResolution (self):
        return self.real_resolution
    
    def MetersToLatLon (self,mx,my):
        return self.mercator.MetersToLatLon(mx, my)
        
    def MetersToTile (self,mx,my):
        return self.mercator.MetersToTile(mx, my, self.level)
    
    def MetersToLevelTile (self,mx,my,level):
        return self.mercator.MetersToTile(mx, my, level)
    
    def MetersToScene (self,mx,my):
        return mx,-my
    def SceneToLatLon (self,mx,my):
        return self.mercator.MetersToLatLon(mx, my)
    def LatLonToScene (self,lat,lon):
        mx,my = self.mercator.LatLonToMeters(lat, lon)
        return self.MetersToScene(mx, my)
    
    def getLevel (self):
        return self.level
    def setLevel (self,level):
        if level > self.level :
            self.real_resolution = self.getLevelResolution(level)
        else:
            self.real_resolution = self.getLevelResolution(level+1)
            
        self.level = level
    def setRealResolution (self, res):
        self.real_resolution = res
        
    def getDistance (self,start,end):
        lat_start,lon_start= self.MetersToLatLon(start.x()), start.y()
        lat_end,lon_end = self.MetersToLatLon(end.x()), end.y()
        lat_start = M.radians(lat_start)
        lat_end = M.radians(lat_end)
        lon = M.radians(lon_end - lon_start)
        sin_s = M.sin(lat_start)*M.sin(lat_end)
        cos_s = M.sin(lat_start)*M.sin(lat_end)*M.cos(lon)
        return self.R*M.acos(cos_s+sin_s)