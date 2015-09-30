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
        


    def updateFromDisk (self,default={}):
        path = os.path.join(Config().instance.path_to_pic(),self.faction().name,self.empire().name,self.kingdom().name,"Picture")
        print ('update from disk ',path)
        currentPath = os.path.join(path,self.name)
        print ('default : ',default)
        print ('current path',currentPath)
        if os.path.exists(currentPath):
            print ('le groupe',self.name," exist")
            if (ExportToSqlite.hasSubGroup(currentPath)):
                list_sub_group = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
                #on supprime les sous groupe devenus inutiles
                list_sub_to_delete = []
                for sg in self.sub_groupes:
                    if (sg.name in list_sub_group) == False:
                        print ('suppression de sous groupes obsoletes',sg.name)    
                        list_sub_to_delete.append(sg)
                for sg in list_sub_to_delete:
                    sg.delete()
                        #self.removeSubGroupe(sg)
                for sub in list_sub_group :
                    # on ajoute un sous groupe si besoin
                    print ('list des sub')
                    subGroupe = self.containGroupe(sub)
                    if subGroupe == None:
                        print ('ajout d un nouveau subgroupe',sub)
                        if not ('groupe' in default) or default['groupe'] == {}:
                            attribs = {'description':Config().instance.settings.value ("database/default_groupe_description="),'color':Config().instance.settings.value ("database/default_groupe_color"),'rank':Config().instance.settings.value ("database/default_groupe_rank")}
                        else:
                            attribs = default['groupe']
                        result = self.model().database.select("ID+1","gm_groupe",True,"ID + 1 not in (select ID from gm_groupe)","ID")
                        result.first()
                        groupe = Groupe(result.value("ID+1"), sub,attribs,self,True)
                        attribs['parent']=self.id
                        attribs['name']=groupe.name
                        attribs['ID'] =  groupe.id
                        attribs['ID_kingdom']=self.kingdom().id
                        self.model().database.insert("gm_groupe",attribs)
                        self.addSubGroupe(groupe)
                    else:
                        groupe = subGroupe
                    list_heros = list(filter(SqliteModel.isValid,os.listdir(os.path.join(currentPath,sub))))
                    groupe.updateHeros(list_heros,default)
            else:
                list_heros = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
                self.updateHeros(list_heros,default)
        else:
            self.delete()
        print ('resultat de l update',self.warriors)
        for sg in self.sub_groupes :
            print ('sub.name',sg.name)
            for w in sg.warriors.values():
                print ('warrior name',w.name)
    
    
    def updateHeros (self,list_heros_name,default={}):
        #on supprime les heros qui n existent plus
        for warrior in self.getWarriorList():
            if (warrior.name in list_heros_name) == False:
                print ('suppression de heros',warrior.name)
                warrior.delete()
        # on ajoute les nouveaux heros
        print ('list_heros_name',list_heros_name)
        for heros in list_heros_name :
            print ('traitement du heros',heros)
            if not self.containWarrior(heros):
                #ExportToSqlite.createDescriptionFile( heros, path_file)
                print ('ajout de heros',heros)
                if not "heros" in default or default['heros'] == {}:
                    print ('cas 1')
                    attribs = {} 
                    attribs['latitude'] = float(Config().instance.settings.value ("database/default_heros_latitude"))
                    attribs['longitude'] = float(Config().instance.settings.value ("database/default_heros_longitude"))
                    attribs['place'] = int(Config().instance.settings.value ("database/default_heros_place"))
                    attribs['level'] = int(Config().instance.settings.value ("database/default_heros_level"))
                    attribs['leader'] = bool(Config().instance.settings.value ("database/default_heros_leader"))
                    attribs['rank'] = int(Config().instance.settings.value ("database/default_heros_rank"))
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
                    attribs['victoires'] = 0
                    attribs['defaites'] = 0
                    attribs['egalites'] = 0
                    attribs['kills'] = 0
                    attribs['description'] = Config().instance.settings.value ("database/default_heros_description")
                    attribs['techniques'] = Config().instance.settings.value ("database/default_heros_techniques")
                    attribs['historique'] = Config().instance.settings.value ("database/default_heros_historique")
                    attribs['complete'] = int(Config().instance.settings.value ("database/default_heros_complete"))
                    #TODO compute state with history and life state
                    attribs['status'] = Config().instance.settings.value ("database/default_heros_status")
                else:
                    print ('cas 2')
                    #print ('la',default['heros'])
                    attribs = default['heros']
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
                    attribs['complete'] = 0
                    attribs['victoires'] = 0
                    attribs['defaites'] = 0
                    attribs['egalites'] = 0
                    attribs['kills'] = 0
                
                self.model().database.setVerbose(True)
                result = self.model().database.select("ID+1","gm_perso",True,"ID + 1 not in (select ID from gm_perso)","ID")
                result.first()
                warrior = Warrior(result.value("ID+1"), heros, attribs, self)
                self.addWarrior(warrior)
                attribs['name']=warrior.name
                attribs['ID'] =  warrior.id
                attribs['ID_groupe']=self.id
                print ('attribs',attribs)
                self.model().database.insert("gm_perso",attribs)
        else:
            print ('heros deja present on ne fait rien')
        
    def delete (self):
        print ('delete groupe', self.name)
        if len(self.sub_groupes) > 0:
            for sub in self.sub_groupes:
                sub.delete()
                #sub.parent.sub_groupes.remove(sub)

        while (len(self.warriors)!= 0):
            
            for warrior in self.warriors.values():
                warrior.delete()
                break


        self.model().database._delete("gm_groupe","ID="+str(self.id))
        if self.isSub():
            self.parent.sub_groupes.remove(self)
        else:
            self.kingdom().groupes.pop(self.name)    
#     def removeWarrior (self,warrior):
#         self.model().database._delete("gm_perso","ID="+str(warrior.id))
#         self.warriors.pop(warrior.id)
    
#     def getAllWarriors (self):
#         dict_heros = {}
#         for w in self.warriors.values():
#             dict_heros[w.id] = w
#             
#         return dict_heros
    
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
                return g
        return None
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