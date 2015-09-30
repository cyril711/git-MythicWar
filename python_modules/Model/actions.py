from python_modules.utils.globalmaptiles import GlobalMercator
from PyQt5 import QtCore
from PyQt5.Qt import QVector2D
from python_modules.config import Config

g_threshold = 1
class Action:
    def __init__ (self, id_i,list_left,list_right,activ, parent_action=-1):
        self.list_left = list_left
        self.list_right = list_right
        self.id =  id_i
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


class ActionMoveToPosition(Action):
    def __init__(self, id_i,list_left,list_right,activ,speed_factor, parent_action=-1):
        super(ActionMoveToPosition,self).__init__(id_i,list_left,list_right,activ, parent_action)
        print ('vvvvv',id_i,type(list_left),list_left,type(self.list_left),self.list_left)
        self.speed_factor = speed_factor
    def process (self,deltaT):
        i = 0
        print ('nombre de heros a deaplcer',len(self.list_left))
        for heros in self.list_left:
            x,y = self.global_mercator.LatLonToMeters(heros.attribs['latitude'], heros.attribs['longitude'])
            posDepart = QVector2D(x,y)
            destination = self.list_right[i]
            x,y = self.global_mercator.LatLonToMeters(destination.x(), destination.y())
            posFinale = QVector2D(x,y)
            vec = posFinale - posDepart
            print ('vec.length()',vec.length())
            eloignement = vec.length()

            vec.normalize()
            base_speed = int(Config().instance.settings.value('global/heros_speed'))
            deplacement = vec*(base_speed*self.speed_factor*deltaT)
            if deplacement.length() > eloignement : 
                resultat = destination
                self.disable()
            else:
                resultat = posDepart+deplacement
            lat,lon = self.global_mercator.MetersToLatLon(resultat.x(), resultat.y())
            heros.move(lat,lon)
            i = (i +1)%len(self.list_right)
    
class ActionMoveToTargets(Action):
    def __init__(self, id_i,list_left,list_right,activ,speed, parent_action=-1):
        super(ActionMoveToTargets,self).__init__(id_i,list_left,list_right,activ, parent_action)
        self.speed = speed
    def process (self):
        pass

class ActionAttack(Action):
    def __init__(self, id_i,list_left,list_right,activ,duration, parent_action=-1):
        super(ActionAttack,self).__init__(id_i,list_left,list_right,activ, parent_action)
        self.duration = duration
    def process (self):
        pass

class ActionHeal(Action):
    def __init__(self, id_i,list_left,list_right,activ,duration, parent_action=-1):
        super(ActionHeal,self).__init__(id_i,list_left,list_right,activ, parent_action)
        self.duration = duration
    def process (self):
        pass