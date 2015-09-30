from PyQt5.QtWidgets import QProgressDialog
from PyQt5 import QtCore
import os
from PyQt5.Qt import QPointF, QMessageLogger, QFile, QTextDocumentWriter,\
    QTextEdit
from python_modules.utils.sqlite_model import SqliteModel
from python_modules.config import Config



class ExportToSqlite (SqliteModel):
    
    def __init__ (self,basepath, database):
        super(ExportToSqlite,self).__init__(basepath)
        self.database = database
        self.defaultColorStringFaction = "0,0,255,255"
        self.nb_heros_inserted = [" ajout de Heros ",0]
        self.nb_groupes_inserted = [" ajout de Groupes",0]
        self.nb_kingdom_inserted = [" ajout de Royaumes ",0]
        self.nb_empire_inserted = [" ajout d' Empires ",0]
        self.nb_faction_inserted = [" ajout de Factions ",0]
        self.nb_heros_unchanged= [" unchanged Heros ",0]
        self.nb_groupes_unchanged= [" unchanged Groupes",0]
        self.nb_kingdom_unchanged= [" unchanged Royaumes ",0]
        self.nb_empire_unchanged= [" unchanged Empires ",0]
        self.nb_faction_unchanged= [" unchanged Factions ",0]





    def setDefaultValues (self, default_dict):
        self.defaultValues = default_dict
        
    def addFaction (self, faction_name):
        result = self.database.select("*","gm_faction",True,'name=="'+faction_name+'"')

        if result.first() == 0 :
            print ('faction inexistante') 
            attribs = {"name":faction_name,'icon':faction_name+'.png'}
            self.database.insert("gm_faction",attribs)
            result = self.database.select("*","gm_faction",False,'name=="'+faction_name+'"')
            self.nb_faction_inserted[1] = self.nb_faction_inserted[1] + 1
        else:
            print ('faction deja persante')
            self.nb_empire_unchanged[1] = self.nb_empire_unchanged[1] + 1
        return result
    def addEmpire (self, empire_name,id_faction,empire_color=""):
        result = self.database.select("*","gm_empire",True,'name=="'+empire_name+'"')
        if result.first() == 0 : 
            attribs = {"name":empire_name,"ID_faction":id_faction,"icon":str(empire_name)+".png","color":empire_color}
            self.database.insert("gm_empire",attribs)        
            result = self.database.select("*","gm_empire",True,'name=="'+empire_name+'"')
            self.nb_empire_inserted[1] = self.nb_empire_inserted[1] + 1
        else:
            self.nb_empire_unchanged[1] = self.nb_empire_unchanged[1] + 1
        return result 

    def addKingdom (self, kingdom_name, id_empire):
        result = self.database.select("*","gm_kingdom",True,'name=="'+kingdom_name+'"')
        if result.first() == 0 :
            default_couleur = str(self.defaultValues['kingdom_couleur'][0]) +','+ str(self.defaultValues['kingdom_couleur'][1])+','+str(self.defaultValues['kingdom_couleur'][2])+','+str(self.defaultValues['kingdom_couleur'][3]) 
            attribs = {"name":kingdom_name,"ID_empire":id_empire,"armee":self.defaultValues['kingdom_armee'],"description":self.defaultValues['kingdom_description'],"couleur":default_couleur}
            self.database.insert("gm_kingdom",attribs) 
            result = self.database.select("*","gm_kingdom",True,'name=="'+kingdom_name+'"')
            self.nb_kingdom_inserted[1] = self.nb_kingdom_inserted[1] + 1
        else:
            self.nb_kingdom_unchanged[1] = self.nb_kingdom_unchanged[1] + 1
        return result

    def addGroupe(self, group,id_kingdom,id_group_parent=0):
        #on suppose que chaque groupe a un nom unique pour un royaume donne
        result = self.database.select("*","gm_groupe",True,'name=="'+group+'" AND ID_kingdom=='+str(id_kingdom))
        if result.first() == 0 : 
            attribs = {'name':group,'ID_kingdom':id_kingdom,'description':self.defaultValues['groupe_description'],'color':self.defaultValues['groupe_color'],'rank':self.defaultValues['groupe_rank'],'parent':id_group_parent}
            self.database.insert("gm_groupe",attribs) 
            result = self.database.select("*","gm_groupe",True,'name=="'+group+'" AND ID_kingdom=='+str(id_kingdom))
            print ('add groupe ',group,id_kingdom)
            self.nb_groupes_inserted[1] = self.nb_groupes_inserted[1] + 1
        else:
            self.nb_groupe_unchanged[1] = self.nb_groupe_unchanged[1] + 1 
        return result
    
    def addHeros (self,heros,id_groupe):
        #on suppose que chaque heros a un nom unique pour un groupe
        result = self.database.select("*","gm_perso",True,'name=="'+heros+'" AND ID_groupe=='+str(id_groupe))
        if result.first() == 0 : 
            attribs = {'name':heros,'ID_groupe':id_groupe,'description':self.defaultValues['heros_description'],'techniques':self.defaultValues['heros_techniques'],'historique':self.defaultValues['heros_historique'],'latitude':self.defaultValues['heros_latitude'],'longitude':self.defaultValues['heros_longitude'],'place':self.defaultValues['heros_place'],"level":"",'leader':self.defaultValues['heros_level'],'rank':self.defaultValues['heros_rank'],'status':self.defaultValues['heros_status'],'complete':1,'HP':1,'MP':1,'HP_max':1,'MP_max':1,'ATK':0,'DEF':0,'MATK':0,'MATK':0,'AGL':0,'LUCK':0}
            self.database.insert("gm_perso",attribs) 
            #print ('attribs',attribs)
            result = self.database.select("*","gm_perso",True,'name=="'+heros+'" AND ID_groupe=='+str(id_groupe))
            self.nb_heros_inserted[1] = self.nb_heros_inserted[1] + 1
        else:
            self.nb_heros_unchanged[1] = self.nb_heros_unchanged[1] + 1 
        return result
    
    @staticmethod
    def hasSubGroup (path):
        sub_list = os.listdir (path)
        print ('hasSubGroup',sub_list)
        if len(sub_list)!= 0 and os.path.isdir(os.path.join(path,sub_list[0])):
            sub_list2 = os.listdir(os.path.join(path,sub_list[0]))
            print ('sub_list_2',sub_list2)
            if os.path.isdir(os.path.join(path,sub_list[0],sub_list2[0])):
                print ('return true')
                return True
        return False
    


    def process (self, faction,empire,kingdom):
        super(ExportToSqlite,self).process(faction,empire,kingdom)
        self.progress.setLabelText("Export to sqlite")
        self.progress.setMinimum(0)
        self.progress.setMaximum(self.total_heros)
        
        self.success = False
        nb_heros = 0        
        #si la faction n existe pas encore la creer
        result = self.addFaction (self.faction)
        result.next()
        print ('result',result.value("name"))
        id_faction = result.value("ID")
        print ('ID faction',id_faction)
        #si l empire n existe pas encore le creer
        color = ""
        empire = self.empire
        if len(self.empire.split["-"])>=2 :
            color = self.empire.split["-"][1]
            empire = self.empire.split["-"][0]
        result = self.addEmpire(empire,id_faction,color)
        result.next()
        id_empire= result.value("ID")
        print ('ID empire',id_empire)
        #si le royaume n existe pas encore le creer
        result = self.addKingdom(self.kingdom,id_empire)
        result.next() 
        id_kingdom= result.value("ID")            
        print ('ID kingdom',id_kingdom)
        list_group = list(filter(SqliteModel.isValid,os.listdir (self.fullPath)))
        for group in list_group : 
            result = self.addGroupe(group,id_kingdom)
            result.next()
            id_groupe= result.value("ID")            
            currentPath = os.path.join(self.fullPath,group)
            if (ExportToSqlite.hasSubGroup(currentPath)):
                list_sub_group = list(filter(SqliteModel.isValid,os.listdir(currentPath))) 
                id_master_group = id_groupe
                for sub in list_sub_group :
                    result = self.addGroupe(sub, id_kingdom, id_master_group)
                    result.next()
                    id_groupe= result.value("ID")
                    list_heros = list(filter(SqliteModel.isValid,os.listdir(os.path.join(currentPath,sub))))
                    for heros in list_heros :
                        self.createDescriptionFile(heros,os.path.join(currentPath,sub,heros))
                        self.addHeros(heros,id_groupe)
                        nb_heros+=1
                        self.progress.setValue(nb_heros)      
            else:
                list_heros = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
                for heros in list_heros :
                    self.createDescriptionFile(heros,os.path.join(currentPath,heros))
                    self.success = True
                    self.addHeros(heros,id_groupe)
                    nb_heros+=1       
                    self.progress.setValue(nb_heros)
            if self.stop == True :
                break
            
        self.progress.setValue(self.total_heros)
        result_info = [self.nb_faction_inserted,self.nb_empire_inserted,self.nb_kingdom_inserted,self.nb_groupes_inserted,self.nb_heros_inserted,self.nb_faction_unchanged,self.nb_empire_unchanged,self.nb_kingdom_unchanged,self.nb_groupes_unchanged,self.nb_heros_unchanged]
        self.showResultInfos(result_info)



    def createDescriptionFile(self, name, path_file):
        file_name = "description.html"

        file = open(os.path.join(Config().instance.settings.value("global/resources_path"),"template_profil.html"))
        ddd = file.read()
        print ('ooooo',type(ddd))
        ddd = ddd.replace("tname",name)
        print ('mmmm',ddd)
        chemin = os.path.join(path_file,file_name)
        if (not os.path.exists(chemin)):
            self.textEdit = QTextEdit()

            self.textEdit.setText(ddd)
            writer = QTextDocumentWriter(chemin)
            success = writer.write(self.textEdit.document())
        