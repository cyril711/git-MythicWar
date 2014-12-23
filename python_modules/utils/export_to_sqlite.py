from PyQt5.QtWidgets import QProgressDialog
from PyQt5 import QtCore
import os
from PyQt5.Qt import QPointF, QMessageLogger
from python_modules.utils.sqlite_model import SqliteModel
from python_modules.config import Config



class ExportToSqlite (SqliteModel):
    
    def __init__ (self,basepath, database):
        super(ExportToSqlite,self).__init__(basepath)
        self.database = database
        self.defaultColorString = "125,125,125,255"
        self.defaultText = ""
        self.defaultColorStringFaction = "0,0,255,255"
        #par defautl on met les position de la tour eiffel
        self.defaultPos = QPointF(48.858093,2.294694)
        self.nb_heros_inserted = {" ajout de Heros ":0}
        self.nb_groupes_inserted = {" ajout de Groupes":0}
        self.nb_kingdom_inserted = {" ajout de Royaumes ":0}
        self.nb_empire_inserted = {" ajout d' Empires ":0}
        self.nb_faction_inserted = {" ajout de Factions ":0}
        self.nb_heros_unchanged= {" unchanged Heros ":0}
        self.nb_groupes_unchanged= {" unchanged Groupes":0}
        self.nb_kingdom_unchanged= {" unchanged Royaumes ":0}
        self.nb_empire_unchanged= {" unchanged Empires ":0}
        self.nb_faction_unchanged= {" unchanged Factions ":0}
        self.defaultRankGroup = 0




    def setDefaultValues (self, default_dict):
        self.defaultValues = default_dict
        
    def addFaction (self, faction_name):
        result = self.database.select("*","gm_faction",True,"name="+faction_name)
        if result.size() == 0 : 
            attribs = {"name":faction_name,'couleur':self.defaultColorStringFaction}
            self.database.insert("gm_faction",attribs)
            result = self.database.select("*","gm_faction",True,"name="+faction_name)
            self.nb_faction_inserted.value()[0] = self.nb_faction_inserted.value()[0] = 1
        else:
            self.nb_empire_unchanged.value()[0] = self.nb_empire_unchanged.value()[0] = 1
        return result
    def addEmpire (self, empire_name,id_faction):
        result = self.database.select("*","gm_empire",True,"name="+empire_name)
        if result.size() == 0 : 
            attribs = {"name":empire_name,"ID_faction":id_faction}
            self.database.insert("gm_empire",attribs)        
            result = self.database.select("*","gm_empire",True,"name="+empire_name)
            self.nb_empire_inserted.value()[0] = self.nb_empire_inserted.value()[0] = 1
        else:
            self.nb_empire_unchanged.value()[0] = self.nb_empire_unchanged.value()[0] = 1
        return result 

    def addKingdom (self, kingdom_name, id_empire):
        result = self.database.select("*","gm_kingdom",True,"name="+kingdom_name)
        if result.size() == 0 : 
            attribs = {"name":kingdom_name,"ID_empire":id_empire,"armee":self.defaultText,"description":self.defaultText,"couleur":self.defaultColorString}
            self.database.insert("gm_kingdom",attribs) 
            result = self.database.select("*","gm_kingdom",True,"name="+kingdom_name)
            self.nb_kingdom_inserted.value()[0] = self.nb_kingdom_inserted.value()[0] = 1
        else:
            self.nb_kingdom_unchanged.value()[0] = self.nb_kingdom_unchanged.value()[0] = 1
        return result

    def addGroupe(self, group,id_kingdom,id_group_parent=0):
        #on suppose que chaque groupe a un nom unique pour un royaume donne
        result = self.database.select("*","gm_groupe",True,"name="+group+" AND ID_kingdom="+id_kingdom)
        if result.size() == 0 : 
            attribs = {'name':group,'ID_kingdom':id_kingdom,'description':self.defaultText,'color':"",'rank':self.defaultRankGroup,'parent':id_group_parent,'temples':""}
            self.database.insert("gm_groupe",attribs) 
            result = self.database.select("*","gm_groupe",True,"name="+group+" AND ID_kingdom="+id_kingdom)
            self.nb_groupe_inserted.value()[0] = self.nb_groupe_inserted.value()[0] = 1
        else:
            self.nb_groupe_unchanged.value()[0] = self.nb_groupe_unchanged.value()[0] = 1 
        return result
    
    def addHeros (self,heros,id_groupe):
        #on suppose que chaque heros a un nom unique pour un groupe
        result = self.database.select("*","gm_perso",True,"name="+heros+" AND ID_groupe="+id_groupe)
        if result.size() == 0 : 
            attribs = {'name':heros,'ID_groupe':id_groupe,'description':self.defaultText,'techniques':self.defaultText,'historique':self.defaultText,'latitude':self.defaultPosition.x(),'longitude':self.defaultPosition.y(),'place':"","level":"",'leader':False,'rank':self.defaultRankGroup,'status':self.default_heros_status,'HP':1,'MP':1,'HP_max':1,'MP_max':1,'ATK':0,'DEF':0,'MATK':0,'MATK':0,'AGL':0,'LUCK':0}
            self.database.insert("gm_perso",attribs) 
            result = self.database.select("*","gm_perso",True,"name="+heros+" AND ID_groupe="+id_groupe)
            self.nb_heros_inserted.value()[0] = self.nb_heros_inserted.value()[0] = 1
        else:
            self.nb_heros_unchanged.value()[0] = self.nb_heros_unchanged.value()[0] = 1 
        return result
    
    def hasSubGroup (self,path):
        sub_list = os.listdir (path)
        if os.path.isdir(os.path.join(path,sub_list[0])):
            sub_list2 = os.listdir(os.path.join(path,sub_list[0]))
            if os.path.isdir(os.path.join(path,sub_list[0],sub_list2[0])):
                return True
        return False
    


    def process (self, faction,empire,kingdom):
        super(ExportToSqlite,self).process(faction,empire,kingdom)
        
        nb_heros = 0        
        #si la faction n existe pas encore la creer
        result = self.addFaction (self.faction)
        id_faction = result.value("ID")
        #si l empire n existe pas encore le creer
        result = self.addEmpire(self.empire,id_faction)
        id_empire= result.value("ID")
        #si le royaume n existe pas encore le creer
        result = self.addKingdom(self.kingdom,id_empire) 
        id_kingdom= result.value("ID")            
        
        list_group = list(filter(self.isValid,os.listdir (self.fullPath)))
        for group in list_group : 
            result = self.addGroupe(group,id_kingdom)
            id_groupe= result.value("ID")            
            currentPath = os.path.join(self.fullPath,group)
            if (self.hasSubGroup(currentPath)):
                list_sub_group = list(filter(self.isValid,os.listdir(currentPath))) 
                for sub in list_sub_group :
                    result = self.addGroupe(sub, id_kingdom, id_groupe)
                    id_groupe= result.value("ID")
                    list_heros = list(filter(self.isValid,os.listdir(os.path.join(currentPath,group,sub))))
                    for heros in list_heros :
                        self.addHeros(heros,id_groupe)
                        nb_heros+=1
                        self.progress.setValue(nb_heros)      
            else:
                list_heros = list(filter(self.isValid,os.listdir(os.path.join(currentPath,group))))
                for heros in list_heros :
                    self.addHeros(heros,id_groupe)
                    nb_heros+=1       
                    self.progress.setValue(nb_heros)
            if self.stop == True :
                break
            
        self.progress.setValue(self.total_heros)
        result_info = dict(self.nb_faction_inserted.items()+self.nb_empire_inserted.items()+self.nb_kingdom_inserted.items()+self.nb_groupes_inserted.items()+self.nb_heros_inserted.items()+self.nb_faction_unchanged.items()+self.nb_empire_unchanged.items()+self.nb_kingdom_unchanged.items()+self.nb_groupes_unchanged.items()+self.nb_heros_inserted.items())
        self.showResultInfos(result_info)



