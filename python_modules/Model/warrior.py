from PyQt5.Qt import QPixmap, QObject
from python_modules.config import Config
from PyQt5 import QtCore
class Warrior (QObject):
    selection_changed = QtCore.pyqtSignal(bool,object)
    def __init__(self, id_i, name, attribs, parent):
        super(Warrior,self).__init__()
        self.id = id_i
        self.name = name
        self.attribs = attribs
        self.selected = False
        self.parent = parent
        self.leader = attribs['leader']
        self.latitude = attribs['latitude']
        self.longitude = attribs['longitude']
        groupe_name = self.parent.name
        self.settings = Config().instance.settings
        if self.masterGroupe() != None : 
            groupe_name = self.masterGroupe().name+"/"+groupe_name
        
        kingdom_name = self.kingdom().name
        empire_name = self.empire().name
        faction_name = self.faction().name
        basepath = self.settings.value("global/resources_path")
        self.thumb = QPixmap(basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.name+"/portrait_thumbnail.jpg")
       # print ('pixmap_name:',basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+self.name+"/portrait_thumbnail.jpg")
    def masterGroupe (self):
        if self.parent.isSub():
            return self.parent.parent
        else:
            return None

    def getDictAttributes (self):
        attribs = {}
        attribs['RepresentativPic'] = self.attribs['picture']
        
        attribs['Latitude'] = 48.858093#self.attribs['latitude']
        attribs['Longitude'] = 2.294694#self.attribs['longitude']
        if self.attribs['place']!= '':
            attribs['Place'] = self.attribs['place']
        else:
            attribs['Place'] = 0
        if self.attribs['Level'] != '':
            attribs['Level'] = self.attribs['Level']
        else:
            attribs['Level'] = 0

        attribs['Leader'] = self.attribs['leader']
        return attribs

    def setSelected (self, flag):
        if flag != self.selected :
            self.selected = flag
            self.selection_changed.emit(flag,self)

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