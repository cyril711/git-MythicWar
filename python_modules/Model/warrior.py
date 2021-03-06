from PyQt5.Qt import QPixmap, QObject
from python_modules.config import Config
from PyQt5 import QtCore
import os
from enum import Enum

# attene combat moving

class Warrior (QObject):
    selection_changed = QtCore.pyqtSignal(bool, object, bool)
    on_move = QtCore.pyqtSignal()
    
    def __init__(self, id_i, name, attribs, parent):
        super(Warrior,self).__init__()
        self.id = id_i
        self.name = name
        self.attribs = attribs
        self.selected = False
        self.parent = parent
        self.leader = attribs['leader']
        self.modification = False
        if attribs['rank']=='':
            attribs['rank'] = self.parent.attribs['rank']
        groupe_name = self.parent.name
        if self.masterGroupe() != None : 
            groupe_name = self.masterGroupe().name+"/"+groupe_name

        kingdom_name = self.kingdom().name
        empire_name = self.empire().name
        faction_name = self.faction().name
        path = os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,kingdom_name,'Picture',groupe_name,self.name)
        self.thumb = QPixmap(path+"/portrait_thumbnail.jpg")
#         self.setDefaultValue()
#     
#     
#     # initialise a des valeurs par defaults les champs non renseignes
#     def setDefaultValue(self):
#         if self.attribs['HP_max'] == '':
#             self.attribs['HP_max'] =



    def onChange (self,type_modif="update"):
        if self.modification == False :
            self.modification = True
            self.model().addModifications(self,type_modif)

    def delete (self):
        self.model().database._delete("gm_heros","ID="+str(self.id))
        self.groupe().warriors.pop(self.id)
            
    def changeLeaderStatus (self,value):
        self.leader = value
        self.onChange()
    
    def changeRank(self, value):
        self.attribs["rank"] = value 
        self.onChange()
    
    def masterGroupe (self):
        if self.parent.isSub():
            return self.parent.parent
        else:
            return None

    def model(self):
        return self.faction().parent
    
    def move(self,lat,lon):
        self.attribs['latitude'] = lat
        self.attribs['longitude'] = lon
        self.on_move.emit()
    def getDictAttributes (self):
        attribs = {}
        for key,value in zip (self.attribs.keys(),self.attribs.values()):
            attribs[key] = value
        attribs['leader'] = self.leader
        attribs['ID'] = self.id
        attribs['name'] = self.name
        attribs['ID_Groupe'] = self.groupe().id
        return attribs

    def setSelected (self, flag, first_selection):
        if flag != self.selected :
            self.selected = flag
            self.selection_changed.emit(flag,self,first_selection)

    def groupe (self):
        return self.parent
    
    def kingdom (self):
        if self.groupe().isSub() : 
            return self.groupe().parent.parent
        return self.groupe().parent
    
    def empire (self):
        return self.kingdom().parent
    
    def faction (self):
        return self.empire().parent