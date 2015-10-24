from python_modules.utils.globalmaptiles import GlobalMercator
from PyQt5 import QtCore
from PyQt5.Qt import QVector2D
from python_modules.config import Config

g_threshold = 1
class Action:
    def __init__ (self, id_i,list_left,list_right,activ,offline, parent_action=-1):
        self.list_left = list_left
        self.list_right = list_right
        self.id =  id_i
        self.offline = offline
        self.active = activ
        self.parent_action = parent_action
        self.global_mercator = GlobalMercator()
        
    def isActive (self):
        return self.active
    def activate (self):
        self.active = True
    def disable (self):
        self.active = False
    def process (self):
        pass
    
    
    def resetHeroesStatus (self):
        for w in self.list_left :
            w.attribs["status"] = "repos"
    def LeftPartContainHeros (self, id_heros):
        for item in self.list_left:
            if item.id == id_heros:
                return True
        return False


class ActionMoveToPosition(Action):
    def __init__(self, id_i,list_left,list_right,activ,speed_factor, offline, parent_action=-1):
        super(ActionMoveToPosition,self).__init__(id_i,list_left,list_right,activ, offline, parent_action)
        print ('vvvvv',id_i,type(list_left),list_left,type(self.list_left),self.list_left)
        self.speed_factor = speed_factor
        self.id = id_i
    def process (self,deltaT):
        if self.isActive():
            finish = True
            i = 0
            print ('nombre de heros a deaplcer',len(self.list_left))
            for heros in self.list_left:
                x,y = self.global_mercator.LatLonToMeters(heros.attribs['latitude'], heros.attribs['longitude'])
                heros.attribs["status"] = "moving"
                posDepart = QVector2D(x,y)
                destination = self.list_right[i]
              #  print ('ddesitnaiton dans action',destination)
                x,y = self.global_mercator.LatLonToMeters(destination.x(), destination.y())
                posFinale = QVector2D(x,y)
                vec = posFinale - posDepart
               # print ('vec.length()',vec.length())
                eloignement = vec.length()
    
                vec.normalize()
                base_speed = int(Config().instance.settings.value('global/heros_speed'))
                if self.speed_factor > 0:
                    deplacement = vec*(base_speed*self.speed_factor*deltaT)
                else:
                    deplacement = vec*eloignement*2.0
                if deplacement.length() >= eloignement : 
                    resultat = posFinale
                    #self.disable()
                    
                else:
                    finish = False
                    resultat = posDepart+deplacement
                lat,lon = self.global_mercator.MetersToLatLon(resultat.x(), resultat.y())
                heros.move(lat,lon)
                i = (i +1)%len(self.list_right)
            return finish
    
class ActionMoveToTargets(Action):
    def __init__(self, id_i,list_left,list_right,activ,speed, offline , parent_action=-1):
        super(ActionMoveToTargets,self).__init__(id_i,list_left,list_right,activ, offline , parent_action)
        self.speed = speed
    def process (self):
        pass

class ActionAttack(Action):
    def __init__(self, id_i,list_left,list_right,activ,duration, offline, parent_action=-1):
        super(ActionAttack,self).__init__(id_i,list_left,list_right,activ, offline, parent_action)
        self.duration = duration
    def process (self):
        pass

class ActionHeal(Action):
    def __init__(self, id_i,list_left,list_right,activ,duration, offline , parent_action=-1):
        super(ActionHeal,self).__init__(id_i,list_left,list_right,activ,offline,  parent_action)
        self.duration = duration
    def process (self):
        pass