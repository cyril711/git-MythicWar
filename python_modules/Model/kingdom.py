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
        attribs['name'] = self.name
        attribs['ID'] = self.id
        attribs['ID_empire'] = self.parent.id
        temples = ""
        for t_id in self.attribs['temples']:
            temples=temples+","+str(t_id)
        attribs['temples'] = temples
        return attribs 
    
    def getWarriorList(self, func=None):
        warrior_list = []
        for groupe in self.groupes.values():
            warrior_list+=groupe.getWarriorList(func)
        return warrior_list

    def removeGroupe(self,groupe_name):
        for groupe in self.groupes.values():
            if groupe.name == groupe_name:
                self.groupes.pop(groupe.id)
            else:
                for sub in groupe.sub_groupes:
                    if sub.name == groupe_name :
                        groupe.removeSubGroupe(sub)
            
        
    
    def empire (self):
        return self.parent
    
    def findGroupeFromName(self,name):
        for groupe in self.groupes.values():
            print ('name ;',groupe.name)
            if groupe.name == name:
                return groupe
            for sub in groupe.sub_groupes:
                if sub.name == name:
                    return sub
        return None
    def avancement (self):
        warrior_list = self.getWarriorList()
        nb_complete = 0
        nb_alive= 0
        for w in warrior_list :
            if w.attribs['complete']==2:
                nb_complete +=1
            if w.attribs['HP'] > 0:
                nb_alive += 1
        return len(warrior_list),nb_complete,nb_alive