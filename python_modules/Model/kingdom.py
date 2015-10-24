from PyQt5.Qt import QFile, QColor
from python_modules.config import Config
import os
from python_modules.model.groupe import Groupe
from python_modules.utils.export_to_sqlite import ExportToSqlite
from python_modules.utils.sqlite_model import SqliteModel
class Kingdom :
    def __init__(self, id_i, name,attribs,parent):
        self.id = id_i
        self.name = name
        self.attribs = attribs
        self.color=QColor(attribs["red"],attribs["green"],attribs["blue"],attribs["alpha"])
        self.groupes = {}
        self.temples = []
        self.parent = parent
        self.settings = Config().instance.settings
    def addGroupe (self, groupe):
        self.groupes[groupe.name] = groupe
    def addTemple (self,temple):
        self.temples.append(temple)
        
    def delete (self):
        while (len(self.groupes)!= 0):
            for groupe in self.groupes.values():
                groupe.delete()
                break
        self.model().database._delete("gm_kingdom","ID="+str(self.id))
        self.empire().kingdoms.pop(self.name) 
        
    def createGroupe (self,name, default_values={}):
        
        result = self.model().database.select("ID+1","gm_groupe",False,"ID + 1 not in (select ID from gm_groupe)","ID")
        result.first()
        if 'groupe' in default_values :
            params = default_values['groupe']
        else:
            params = {}
            params ['rank']=1
            params ['description']=''
            params ['color']='saphir'
        groupe = Groupe(result.value("ID+1"), name,params,self)
        self.addGroupe(groupe)
        attribs = groupe.attribs
        attribs['parent']=0
        attribs['name']=groupe.name
        attribs['ID'] =  groupe.id
        attribs['ID_kingdom']=self.id
        self.model().database.insert("gm_groupe",attribs)
        groupe.updateFromDisk(default_values)

    def updateFromDisk (self,default={}):
        path = os.path.join(Config().instance.path_to_pic(),self.faction().name,self.empire().name)
        currentPath = os.path.join(path,self.name)
        print ('current path',currentPath)
        if os.path.exists(currentPath) and os.path.exists(os.path.join(currentPath,'Picture')):
            currentPath = os.path.join(currentPath,'Picture')
            list_group = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
            #on supprime les groupe qui n existe plus
            list_groupe_to_delete = []
            for groupe in self.groupes.values() :
                if (groupe.name in list_group) == False :
                    print ('groupe demande delete',groupe.name)
                    list_groupe_to_delete.append(groupe)
            for g in list_groupe_to_delete:
                g.delete()
            
            for groupe_name in list_group :
                # on met a jours les groupes existant
                if groupe_name in self.groupes:
                    print ('groupe demande update',groupe_name)
                    self.groupes[groupe_name].updateFromDisk(default)
                else:
                    #on cree un nouveau groupe
                    print ('kingodm demande delete',groupe_name)
                    self.createGroupe(groupe_name, default)

        else:
            print ('kingdom suppresion',self.name)
            self.delete()

#     def getAllGroupes (self):
#         dict_groupes = {}
#         for groupe in self.groupes.values():
#             dict_groupes[groupe.id] = groupe
#             if groupe.isSub() == True : 
#                 for sg in groupe.sub_groupes :
#                     dict_groupes[sg.id] = sg
#         return dict_groupes
#     
#     def getAllWarriors (self):
#         dict_heros = {}
#         for groupe in self.groupes.values():
#             dict_heros.update(groupe.getAllWarriors())
#             if groupe.isSub() == True : 
#                 for sg in groupe.sub_groupes :
#                     dict_heros.update(sg.getAllWarriors())
#         return dict_heros



    def getDictAttributes (self):
        attribs = {}
        attribs['armee'] = self.attribs['armee']
        attribs['description'] = self.attribs["description"]
        attribs['couleur'] = str(self.color.red())+','+str(self.color.green())+','+str(self.color.blue())+','+str(self.color.alpha())
        attribs['name'] = self.name
        attribs['ID'] = self.id
        attribs['ID_empire'] = self.parent.id
        temples = None
        for t_id in self.attribs['temples']:
            if temples == None:
                temples=str(t_id)
            else:
                temples=temples+","+str(t_id)
        print ('kingdom temples',temples)
        attribs['temples'] = temples
        return attribs 
    
    def getWarriorList(self, func=None):
        warrior_list = []
        for groupe in self.groupes.values():
            warrior_list+=groupe.getWarriorList(func)
        return warrior_list

    def removeGroupe(self,groupe_name):
        print ('groupes',self.groupes)
        for groupe in self.groupes.values():
            if groupe.name == groupe_name:
                self.model().database._delete("gm_groupe","ID="+str(groupe.id))
                self.groupes.pop(groupe.name)
                return
            else:
                for sub in groupe.sub_groupes:
                    if sub.name == groupe_name :
                        groupe.removeSubGroupe(sub)
                        print ('ooo',len(groupe.sub_groupes)) 
                        if len(groupe.sub_groupes)== 0:
                            print ('suppresion du groupe parent')
                            self.model().database._delete("gm_groupe","ID="+str(groupe.id))
                            self.groupes.pop(groupe.name)                            
                        return 
            
    def faction (self):
        return self.empire().parent
    
    def model (self):
        return self.faction().parent
    
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