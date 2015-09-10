from python_modules.model.warrior import Warrior
from python_modules.utils.sqlite_model import SqliteModel
import os
from python_modules.config import Config
from python_modules.utils.export_to_sqlite import ExportToSqlite
class Groupe:
    
    def __init__ (self, id_i, name, attrib,parent,sub=False):
        self.id = id_i
        self.name = name
        self.attribs = attrib
        self.warriors = {}
        self.parent = parent
        self.sub_groupes = []
        #indique que c est un sous groupe
        self.sub = sub
        self.modification = False

    def isSub (self):
        return self.sub

    def onChange (self,type_modif="update"):
        if self.modification == False :
            self.modification = True
            print ('dd modificationn')
            self.model().addModifications(self,type_modif)

    def kingdom (self):
        if self.isSub():
            return self.parent.parent
        else:
            return self.parent
        
    def empire (self):
        return self.kingdom().parent

    def faction (self):
        return self.empire().parent
    
    def model (self):
        return self.faction().parent
    
    def changeColor (self,color_str):
        self.attribs['color']= color_str
        self.onChange("update")
        
    def changeDescription (self,decsription):
        self.attribs['description']= decsription
        self.onChange("update")
        
    def updateFromDisk (self):
        print ('update from disk ',Config().instance.basepath(),self.faction,self.empire,self.kingdom)
        path = os.path.join(Config().instance.basepath(),self.faction,self.empire,self.kingdom,"Picture")
        currentPath = os.path.join(path,self.name)
        if os.path.exists(currentPath):
            if (ExportToSqlite.hasSubGroup(currentPath)):
                list_sub_group = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
                #on supprime les sous groupe devenus inutiles
                for sg in self.sub_groupes:
                    if (sg.name in list_sub_group) == False:
                        self.removeSubGroupe(sg)
                for sub in list_sub_group :
                    # on ajoute un sous groupe si besoin
                    if not self.containGroupe(sub):
                        attribs = {'description':Config().instance.settings.value ("database/default_groupe_description="),'color':Config().instance.settings.value ("database/default_groupe_color"),'rank':Config().instance.settings.value ("database/default_groupe_rank")}
                        result = self.model().database.select("ID+1","gm_groupe",True,"ID + 1 not in (select ID from table)","ID")
                        groupe = Groupe(result.next().value("ID"), sub,attribs,self.kingdom())
                        self.addSubGroupe(groupe)
                    list_heros = list(filter(SqliteModel.isValid,os.listdir(os.path.join(currentPath,sub))))
                    sub.updateHeros(list_heros)
            else:
                list_heros = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
                self.updateHeros(list_heros)
        else:
            self.empire().pop(self)
    
    
    def updateHeros (self,list_heros_name):
        #on supprime les heros qui n existent plus
        for warrior in self.getWarriorList():
            if (warrior in list_heros_name) == False:
                self.removeWarrior()
        # on ajoute les nouveaux heros
        for heros in list_heros_name :
            if not self.containWarrior(heros):
                #ExportToSqlite.createDescriptionFile( heros, path_file)
                attribs = {} 
                attribs['latitude'] = Config().instance.settings.value ("database/default_heros_latitude")
                attribs['longitude'] = Config().instance.settings.value ("database/default_heros_longitude")
                attribs['place'] = Config().instance.settings.value ("database/default_heros_place")
                attribs['level'] = Config().instance.settings.value ("database/default_heros_level")
                attribs['leader'] = Config().instance.settings.value ("database/default_heros_leader")
                attribs['rank'] = Config().instance.settings.value ("database/default_heros_rank")
                attribs['HP'] = 1000
                attribs['MP'] = 1000
                attribs['HP_max'] = 1000
                attribs['MP_max'] = 1000
                attribs['ATK'] = 0
                attribs['DEF'] = 0
                attribs['MATK'] = 0
                attribs['MDEF'] = 0
                attribs['AGL'] = 0
                attribs['LUCK'] = 0
                attribs['description'] = Config().instance.settings.value ("database/default_heros_description")
                attribs['complete'] = Config().instance.settings.value ("database/default_heros_complete")
                #TODO compute state with history and life state
                attribs['state'] = Config().instance.settings.value ("database/default_heros_status")
                result = self.model().database.select("ID+1","gm_perso",True,"ID + 1 not in (select ID from table)","ID")
                warrior = Warrior(result.next.value("ID"), heros, attribs, self)
                self.addWarrior(warrior)
        
    def removeSubGroupe (self,sub):
        self.sub_groupes.remove(sub)
        
    def removeWarrior (self,warrior):
        self.warriors.pop(warrior.id)
    def getDictAttributes (self):
        attribs = {}
        attribs ['description']=self.attribs['description']
        attribs['color']=str(self.attribs["color"])
        attribs['rank']=int(self.attribs["rank"])
        attribs['name']=self.name
        attribs['ID']=self.id
        if self.isSub():
            attribs['parent'] = self.parent.id
            attribs['ID_kingdom'] =  self.parent.parent.id
        else:
            attribs['parent']=0
            attribs['ID_kingdom'] =  self.parent.id
        return attribs
    
    def containWarrior(self,name):
        if len(self.sub_groupes)!=0:
            for g in self.sub_groupes :
                if g.containWarrior()== True:
                    return True
        else:
            for w in self.warriors.values():
                if w.name == name:
                    return True
        return False

    def containGroupe(self,name):
        for g in self.sub_groupes :
            if g.name == name :
                return True
        return False
    def getWarriorList(self,func=None):
        warrior_list = []
        if len(self.sub_groupes)!=0:
            for g in self.sub_groupes :
                warrior_list+=g.getWarriorList(func)
        else:
            for w in self.warriors.values():
                if (func == None) or (func(w)==True):
                    warrior_list.append(w)
        return warrior_list
    
    def getAverageRank (self):
        rank_sum = 0
        power_total = 0
        nb = 0
        if len(self.sub_groupes)!=0:
            for g in self.sub_groupes :
                sum_tmp,nb_tmp = g.getPower()
                rank_sum+=sum_tmp
                nb+=nb_tmp
        else:
            for w in self.warriors.values():
                rank_sum+=w.attribs['rank']
                power_total+=w.attribs['rank']*10
                nb+=1
        return rank_sum,nb,power_total
    
    def warriorsList(self):
        if len(self.sub_groupes)!=0:
            warriors = {}
            for g in self.sub_groupes :
                warriors.update(g.warriorsList())
            return warriors
        else:
            return self.warriors
    def addSubGroupe (self,groupe):
        self.sub_groupes.append(groupe)
    def addWarrior(self, warrior):
        self.warriors[warrior.id] = warrior