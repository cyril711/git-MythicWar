from PyQt5.Qt import QFile, QColor
from python_modules.config import Config
import os
class Kingdom :
    def __init__(self, id_i, name,attribs,parent):
        self.id = id_i
        self.name = name
        self.attribs = attribs
        self.color=QColor(attribs["red"],attribs["green"],attribs["blue"],attribs["alpha"])
        self.groupes = {}
        self.parent = parent
        self.settings = Config().instance.settings
    def addGroupe (self, groupe):
        self.groupes[groupe.name] = groupe
        
    def getDictAttributes (self):
        attribs = {}
        attribs['armee'] = self.attribs['armee']
        attribs['description'] = self.attribs["description"]
        attribs['couleur'] = str(self.color.red())+','+str(self.color.green())+','+str(self.color.blue())+','+str(self.color.alpha())
        return attribs 
    
    def getWarriorList(self):
        warrior_list = []
        for groupe in self.groupes.values():
            warrior_list+=groupe.getWarriorList()
        return warrior_list
    
    def avancement (self):
        total = 4.0 # description + armee + picture armee + picture land
        completed = 0.0
        if self.attribs['armee']:
            completed = completed + 1
        if self.attribs['description']:
            completed = completed + 1
        faction_name = self.parent.parent.name
        empire_name = self.parent.name
        if QFile(os.path.join(self.settings.value("global/resources_path"),faction_name,empire_name,self.name,"Land.jpg")).exists():
            completed = completed + 1
        if QFile(os.path.join(self.settings.value("global/resources_path"),faction_name,empire_name,self.name,"Army.png")).exists():
            completed = completed + 1    
        for g in self.groupes.values():
            if len (g.sub_groupes)!=0:
                for sub in  g.sub_groupes:
                    if sub.attribs['description']!= '':
                        completed = completed + 1
                    total = total + 1
            else:
                if g.attribs['description']!= '':
                    completed = completed + 1
                total = total + 1
        return int((completed/total)*100)