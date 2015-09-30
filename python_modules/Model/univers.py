from python_modules.model.faction import Faction
from python_modules.model.empire import Empire
from python_modules.model.kingdom import Kingdom
from python_modules.model.warrior import Warrior
from python_modules.model.groupe import Groupe
from python_modules.model.temple import Temple
from python_modules.utils.database import DatabaseManager
from PyQt5.Qt import qDebug, QIcon, qWarning, QPointF, QFile, QProgressDialog,\
    QImage, QColor
from PyQt5.QtCore import QObject, pyqtSignal
from python_modules.config import Config
from random import randint
import math
from PyQt5 import QtCore, QtWidgets
import collections
from python_modules.model.actions import ActionMoveToTargets, ActionMoveToPosition
from enum import Enum



class ActionType (Enum):
    MoveToPosition = 1
    MoveToTargets = 2
    Attack = 3


class Univers (QObject):
    #selection_changed = pyqtSignal()
    selection_updated = pyqtSignal()
    filtered_changed = pyqtSignal()
    askForHerosPage = pyqtSignal(Warrior)
    askForKingdomPage = pyqtSignal(Kingdom)
    askForKingdomHomePage = pyqtSignal (Empire)
    askForMap = pyqtSignal(float,float)
    askForGroup = pyqtSignal (Groupe)
    askForProfil = pyqtSignal (Warrior)
    askForKingdomReload = pyqtSignal(str)
    saveEnabled = pyqtSignal(bool)
    def __init__ (self,database,progressBar,parent=None):
        super(Univers,self).__init__(parent)
        self.progress = progressBar
        self.factions = {}
        self.temples = {}
        self.database = database
        self.list_actions = []
        self.modifications = []
        self.loadFromFile()
        self.currentFaction = None
        self.currentEmpire = None
        self.currentKingdom= None
        self.currentGroupe= None     
        self.selected_Warriors = []
        self.filtered_Warriors = []
        self.settings = Config().instance.settings
        colors =  self.settings.value ("global/groupe_color").split(",")
        self.groupe_color_icons = {}
        self.groupe_color_value = {}
        for color in colors :
            icon = QIcon(":textures/"+color)
            self.groupe_color_icons[color] = icon
            image = QImage(":textures/"+color)
            value = image.pixel(image.width()/2.0,image.height()/2.0)
            # pour view map donner une couleur a item warrior
            self.groupe_color_value[color]  = QColor(value)
    def getSelectionList (self):
        my_list  = []
        for heros in self.selected_Warriors:
            my_list.append(heros)
        return my_list
    def addAction (self,type_i,value,left_part,right_part):
        if type_i == ActionType.MoveToPosition:
            print ('add action',left_part,right_part,value)
            print ('type de left',type(left_part),len(left_part))
            action = ActionMoveToPosition(len(self.list_actions)+1 ,left_part,right_part,True,value)
            self.list_actions.append(action)
        elif type == ActionType.MoveToTargets:
            pass
        
    def updateActions (self, deltaT):
        print ('nombre d action dans la pile',len(self.list_actions))
        for action in self.list_actions : 
            if action.isActive() :
                print ('elle est active')
                action.process(deltaT)
            else:
                pass
    def addModifications(self,item,modification_type):
        if len(self.modifications)==0:
            self.saveEnabled.emit(True)
        self.modifications.append([item,modification_type])

    # ici on suppose que chaque empire a un nom unique
    def getEmpireFromName (self, empire_name):
        print ('getEmpireFromName',empire_name)
        for faction in self.factions.values() :
            for empire in faction.empires.values():
                if empire.name == empire_name :
                    return empire
        return None

    def getFactionFromName (self, faction_name):
        for faction in self.factions.values() :
            if faction.name == faction_name :
                    return faction
        return None


    def delete (self):
        for faction in self.factions:
            faction.delete()
        self.temples = {}
        self.currentFaction = None
        self.currentEmpire = None
        self.currentKingdom= None
        self.currentGroupe= None     
        self.selected_Warriors = []
        self.filtered_Warriors = []
        

    def clear (self):
        self.factions = {}
        self.temples = {}
        self.currentFaction = None
        self.currentEmpire = None
        self.currentKingdom= None
        self.currentGroupe= None     
        self.selected_Warriors = []
        self.filtered_Warriors = []
            
    def setCurrentFaction (self, faction):
        self.currentFaction  = faction

    def setCurrentEmpire (self, empire):
        self.currentEmpire = empire
            
    def setCurrentKingdom (self, kingdom):
        self.currentKingdom  = kingdom 
        
    def setCurrentGroupe (self, groupe):
        self.currentGroupe  = groupe           
            
    def nextSelectedWarrior (self):
        self.first_selected = (self.first_selected + 1)% len(self.selected_Warriors)

    def previousSelectedWarrior (self):
        self.first_selected = (self.first_selected - 1)% len(self.selected_Warriors)    

    def onSelectionChanged (self, flag,warrior):
        if (warrior in self.selected_Warriors) and (flag == False):
            self.selected_Warriors.remove(warrior)
           # print ('remove from selected warriors',warrior.name)
            self.selection_updated.emit()
        elif (warrior not in self.selected_Warriors) and (flag == True):
            self.selected_Warriors.append(warrior)
            #print ('append from selected warriors',warrior.name)
            self.selection_updated.emit()        
#     def setSelection (self, list_id):
#         self.selected_Warriors = []
#         for w in self.filtered_Warriors:
#             try :
#                 if w.id == list_id[len(self.selected_Warriors)]:
#                     self.selected_Warriors.append(w)
#             except IndexError :
#                 pass
#         self.first_selected = 0
#         self.selection_changed.emit()

    def dispatchCircleWarriors(self,scene_coord, origin, radius):
        print ('dispatch circle warriors')
        l = []
        for heros in self.selectedWarriors():
            try:
                x = randint(int(-radius),int(radius))
                y = (radius*radius) - (x*x)
                print ('sqrt(y)',math.sqrt(y))
                print ('rrr',origin,radius,y,x)
                print ('randrange',int(origin.y()-math.sqrt(y)),int(origin.y()+math.sqrt(y)))
                y = randint (int(-math.sqrt(y)),int(math.sqrt(y)))
                latitude = origin.x()  +x 
                longitude = -origin.y()  +y
                print ('position AVT dispatch :',heros.attribs['latitude'],heros.attribs['longitude'])
                #heros.attribs['latitude'],heros.attribs['longitude'] = scene_coord.SceneToLatLon(latitude,longitude)
                #print ('position du dispatch :',heros.attribs['latitude'],heros.attribs['longitude']) 
                #heros.on_move.emit()
                mx,my = scene_coord.SceneToLatLon(latitude,longitude)
                new_pos = QPointF(mx,my)
            except ValueError :
                new_pos = QPointF(heros.attribs['latitude'],heros.attribs['longitude'] )
            l.append(new_pos)
        return l

    def selectedWarriors (self):
        return self.selected_Warriors
    def filteredWarriors (self):
        return self.filtered_Warriors
    
    def allWarriors (self):
        l = []
        for faction in self.factions.values() :
            for empire in faction.empires.values():
                for kingdom in empire.kingdoms.values():
                    for groupe in kingdom.groupes.values():
                        for sub_groupe in groupe.sub_groupes:
                            for perso in sub_groupe.warriors.values():
                                l.append(perso)
                        for perso in groupe.warriors.values():
                            l.append(perso)
        return l
    def clearSelection (self):
        l = self.allWarriors()
        for warrior in l : 
            warrior.setSelected(False)
        
    def updateFilteredWarrior(self):
        self.filtered_Warriors = []
        for faction_name, faction in zip(self.factions.keys(),self.factions.values()):
            if (self.currentFaction == None or faction_name == self.currentFaction.name):
                for empire_name, empire in zip(faction.empires.keys(), faction.empires.values()):
                    if (self.currentEmpire == None or empire_name == self.currentEmpire.name):
                        for kingdom_name, kingdom in zip(empire.kingdoms.keys(), empire.kingdoms.values()):
                            if (self.currentKingdom== None or kingdom_name == self.currentKingdom.name):
                                for groupe_name, groupe in zip(kingdom.groupes.keys(), kingdom.groupes.values()):
                                    if (self.currentGroupe== None or groupe_name == self.currentGroupe.name):
                                        for key,perso in zip(groupe.warriorsList().keys(),groupe.warriorsList().values()):
                                            self.filtered_Warriors.append(perso)
        self.filtered_changed.emit()                          
        return self.filtered_Warriors
    
    def getTempleById (self,temple_id):
        try :
            result = self.temples[temple_id]
        except KeyError:
            result = None
        return result

#     def save (self,filename = None):
#         print ("sauvegarde")
#         try :
#             temp_filename = "mon_test.sqlite"
#             if QFile.remove(temp_filename) == False :
#                 qWarning("echec suppression ")
#         except OSError :
#             qWarning("echec suppression ")
#             pass
#         result = QFile.copy(Config().instance.model_database(),temp_filename)
#         if result == True :
#             print("copy du model reussit")
#         else:
#             print("echec de la copy ",Config().instance.model_database(),temp_filename)
#         database = DatabaseManager(temp_filename,True)
#         database.createConnection()
#         database.setVerbose(True)
#        # self.database.setVerbose(True)
#         print ('nb temples',len(self.temples.values() ))
#         for temple in self.temples.values() :
#             attribs = temple.getDictAttributes ()
#             database.insert("gm_temple",attribs)
#         for faction in self.factions.values() :
#             attribs = faction.getDictAttributes ()
#             print ('ajout faction')
#             #attribs = {"name":faction.name,'icon':faction.name+'.png'}
#             database.insert("gm_faction",attribs)
#             #id_faction = self.database.select("*","gm_faction",False,'name=="'+faction.name+'"')
#             for empire in faction.empires.values():
#                 #attribs = {"name":empire.name,"ID_faction":id_faction,"icon":str(empire.name)+".png","color":empire.attribs['color']}
#                 attribs = empire.getDictAttributes()
#                 print ('ajout empire')
#                 database.insert("gm_empire",attribs)        
#                 for kingdom in empire.kingdoms.values():
#                     print ('ajour kingdom')
#                     attribs = kingdom.getDictAttributes()
#                     database.insert("gm_kingdom",attribs) 
#                     for groupe in kingdom.groupes.values():
#                         print ('ajout groupe')
#                         attribs = groupe.getDictAttributes ()
#                         database.insert("gm_groupe",attribs)
#                         for sub_groupe in groupe.sub_groupes:
#                             print ('ajout sub groupe')                            
#                             attribs = sub_groupe.getDictAttributes ()
#                             database.insert("gm_groupe",attribs)
#                             for perso in sub_groupe.warriors.values():
#                                 print ('ajout perso 1')
#                                 attribs = perso.getDictAttributes ()
#                                 database.insert("gm_perso",attribs)
#                         for perso in groupe.warriors.values():
#                             print ('ajout perso2')
#                             attribs = perso.getDictAttributes ()
#                             if perso.name == "Artemis":
#                                 print ("artemie pos pour test",attribs["latitude"],attribs["longitude"])
#                             database.insert("gm_perso",attribs)
#         print ("FIN AJOUT DES ELEMENTS")
#         if filename == None : 
#             filename = Config().instance.current_database()
#             try :
#                 print ('filename',type(filename))
#                 print ('value',filename)
#                 if QFile.remove(filename) == False :
#                     qWarning("echec suppression ")
#                     
#             except OSError :
#                 qWarning("echec suppression ")
#                 pass
# 
# 
#         if QFile.copy(database.databaseName(),filename):
#             print("sauvegarde reussit db name",database.databaseName(), filename)
#             self.modifications = []
#             self.saveEnabled.emit(False)
#         else:
#             qDebug("Echec sauvegarde")
#             print ('kkk',database.databaseName(),filename)


    def getFirstFreeGroupId(self):
        dict_groupes = self.getAllGroupes ()
        dict_groupes = {'0':'llll','2':'ooooo','5':'lllll'}
        print ('type sorted',type(sorted(dict_groupes)),sorted(dict_groupes.items()))   
        l = collections.OrderedDict(sorted(dict_groupes.items()))
        id = 0
        for item in l : 
            if item[0] == id : 
                id+=1
            else:
                
                return id
    def getFirstFreeherosId(self):
        dict_heros = self.getAllWarriors()   
        print ('type sorted',type(sorted(dict_heros)),sorted(dict_heros))   
        l = collections.OrderedDict(sorted(dict_heros.items()))
        id = 0
        for item in l : 
            if item[0] == id : 
                id+=1
            else:
                
                return id
    def getAllWarriors(self):            
        dict_heros = {}
        for faction in self.factions.values() :
            dict_heros.update(faction.getAllWarriors())
        return dict_heros
    def getAllGroupes (self):
        dict_groupes = {}
        for faction in self.factions.values() :
            dict_groupes.update(faction.getAllGroupes())
            
        return dict_groupes
    def save (self,filename = None):
        print ("sauvegarde")
       # self.database.setVerbose(True)
        for temple in self.temples.values() :
            attribs = temple.getDictAttributes ()
            self.database.update("gm_temple",attribs,"ID="+str(temple.id))
        for faction in self.factions.values() :
            attribs = faction.getDictAttributes ()
            self.database.update("gm_faction",attribs,"ID="+str(faction.id))
            for empire in faction.empires.values():
                attribs = empire.getDictAttributes ()
                self.database.update("gm_empire",attribs,"ID="+str(empire.id))
                for kingdom in empire.kingdoms.values():
                    attribs = kingdom.getDictAttributes ()
                    self.database.update("gm_kingdom",attribs,"ID="+str(kingdom.id))
                    for groupe in kingdom.groupes.values():
                        attribs = groupe.getDictAttributes ()
                        self.database.update("gm_groupe",attribs,"ID="+str(groupe.id))
                        for sub_groupe in groupe.sub_groupes:
                            attribs = sub_groupe.getDictAttributes ()
                            self.database.update("gm_groupe",attribs,"ID="+str(sub_groupe.id))
                            for perso in sub_groupe.warriors.values():
                                attribs = perso.getDictAttributes ()
                                self.database.update("gm_perso",attribs,"ID="+str(perso.id))
                        for perso in groupe.warriors.values():
                            attribs = perso.getDictAttributes ()
                            if perso.name == "Artemis":
                                print ("artemie pos pour test",attribs["latitude"],attribs["longitude"])
                            self.database.update("gm_perso",attribs,"ID="+str(perso.id))
        db_name = self.database.database.databaseName()
        if filename == None : 
            filename = self.settings.value("global/current_database")
        try :
            print ('filename',type(filename))
            print ('value',filename)
            if QFile.remove(filename) == False :
                qWarning("echec suppression ")
                
        except OSError :
            qWarning("echec suppression ")
            pass

        if QFile.copy(db_name,filename):
            print("sauvegarde reussit db name",db_name, filename)
        else:
            qDebug("Echec sauvegarde")
            print ('kkk',db_name,filename)
    def loadFromFile (self):
        all_sqlite = self.database.select("*", "gm_perso",False,None)
        nb_total = 0
        while all_sqlite.next():
            nb_total+=1
        nb_heros_added = 0
        self.progress.setLabelText("Etape 1/2 : Chargement de la base de donnee")
        self.progress.setMinimum (0)
        self.progress.setMaximum (nb_total*2)
        qWarning("debut chargement de la bdd progess max = ")
        temples_sqlite = self.database.select("*", "gm_temple",False,None,"ID")
        while temples_sqlite.next():
            level_dict = {}
            for name,background in zip(temples_sqlite.value("levels").split(','),temples_sqlite.value("backgrounds").split(',')):
                level_dict[name] = background
            print ('temple :',temples_sqlite.value("name"),temples_sqlite.value("latitude"),temples_sqlite.value("longitude"))
            pos = QPointF(float(temples_sqlite.value("latitude")),float(temples_sqlite.value("longitude")))
            master = temples_sqlite.value("master")
            temple = Temple(temples_sqlite.value("ID"), temples_sqlite.value("name"),pos,level_dict,master)
            self.addTemple (temple)
        faction_sqlite = self.database.select("*", "gm_faction",False,None,"ID ASC")
        while faction_sqlite.next():
            attribs = {'icon':faction_sqlite.value("icon")} 
            faction = Faction(faction_sqlite.value("ID"), faction_sqlite.value("name"),attribs,self)
            self.addFaction(faction)
            empire_sqlite = self.database.select("*", "gm_empire",False, "ID_faction=="+str(faction_sqlite.value("ID")),"ID ASC")         
            while empire_sqlite.next():
                attribs = {'color':str(empire_sqlite.value("color"))}
                print ('coloooooor',str(empire_sqlite.value("icon")),empire_sqlite.value("name"),str(empire_sqlite.value("color")))
                empire = Empire(empire_sqlite.value("ID"), empire_sqlite.value("name"),attribs,faction)
                faction.addEmpire(empire)
                kingdom_sqlite = self.database.select("*", "gm_kingdom",False,"ID_empire=="+str(empire_sqlite.value("ID")),"ID ASC")
                while kingdom_sqlite.next():
                    attribs = {'armee':kingdom_sqlite.value("armee"),'description':kingdom_sqlite.value("description"),'red':int(kingdom_sqlite.value("couleur").split(",")[0]),'green':int(kingdom_sqlite.value("couleur").split(",")[1]),'blue':int(kingdom_sqlite.value("couleur").split(",")[2]),'alpha':int(kingdom_sqlite.value("couleur").split(",")[3])}
                    attribs['temples'] = kingdom_sqlite.value("temples").split(',')
                    kingdom = Kingdom(kingdom_sqlite.value("ID"), kingdom_sqlite.value("name"),attribs,empire)
                    empire.addKingdom(kingdom)
                    for t in kingdom_sqlite.value("temples").split(','):
                        if t in self.temples: 
                            self.temples[t].setOwner(kingdom)      
                    groupe_sqlite = self.database.select("*", "gm_groupe",False,"ID_kingdom=="+str(kingdom_sqlite.value("ID"))+" and parent==0","ID ASC")
                    while groupe_sqlite.next():
                        attribs = {'description':groupe_sqlite.value("description"),'color':groupe_sqlite.value("color"),'rank':groupe_sqlite.value("rank")}
                        groupe = Groupe(groupe_sqlite.value("ID"), groupe_sqlite.value("name"),attribs,kingdom)
                        kingdom.addGroupe(groupe)        
                        warrior_sqlite = self.database.select("*", "gm_perso",False,"ID_groupe=="+str(groupe_sqlite.value("ID")),"ID ASC")
                        while warrior_sqlite.next():
                            attribs = {}
                            attribs['latitude'] = warrior_sqlite.value("latitude") 
                            attribs['longitude'] = warrior_sqlite.value("longitude") 
                            attribs['place'] = warrior_sqlite.value("place")
                            attribs['level'] = warrior_sqlite.value("level") 
                            attribs['leader'] = bool(warrior_sqlite.value("leader")) 
                            attribs['rank'] = int(warrior_sqlite.value("rank"))
                            attribs['HP'] = int(warrior_sqlite.value("HP"))
                            attribs['MP'] = int(warrior_sqlite.value("MP"))
                            attribs['HP_max'] = int(warrior_sqlite.value("HP_max"))
                            attribs['MP_max'] = int(warrior_sqlite.value("MP_max"))
                            attribs['ATK'] = int(warrior_sqlite.value("ATK"))
                            attribs['DEF'] = int(warrior_sqlite.value("DEF"))
                            attribs['MATK'] = int(warrior_sqlite.value("MATK"))
                            attribs['MDEF'] = bool(warrior_sqlite.value("MDEF"))
                            attribs['AGL'] = int(warrior_sqlite.value("AGL"))
                            attribs['LUCK'] = int(warrior_sqlite.value("LUCK"))
                            attribs['description'] = bool(warrior_sqlite.value("description"))
                            try : 
                                attribs['complete'] = int(warrior_sqlite.value("complete"))
                            except ValueError: 
                                attribs['complete'] = 0
                            attribs['status'] = "repos"
                            warrior = Warrior(warrior_sqlite.value("ID"), warrior_sqlite.value("name"),attribs, groupe)
                            nb_heros_added+=1
                            self.progress.setValue(nb_heros_added)
                            groupe.addWarrior(warrior)
                            warrior.selection_changed.connect(self.onSelectionChanged)
                            if int(warrior_sqlite.value("place"))!= 0:
                                try:
                                    self.temples[int(warrior_sqlite.value("place"))].addHeros(warrior)
                                except KeyError:
                                    pass
        #gestion des sous groupes
        groupe_sqlite = self.database.select("*", "gm_groupe",False,"parent!= 0","ID ASC")
        while groupe_sqlite.next():
            attribs = {'description':groupe_sqlite.value("description"),'color':groupe_sqlite.value("color"),'rank':groupe_sqlite.value("rank")}
            parent_groupe = self.findGroupeFromID(groupe_sqlite.value("parent"))
            groupe = Groupe(groupe_sqlite.value("ID"), groupe_sqlite.value("name"),attribs,parent_groupe,True)
            warrior_sqlite = self.database.select("*", "gm_perso",False,"ID_groupe=="+str(groupe_sqlite.value("ID")),"ID ASC")
            while warrior_sqlite.next():
                attribs = {} 
                attribs['latitude'] = warrior_sqlite.value("latitude") 
                attribs['longitude'] = warrior_sqlite.value("longitude")
                attribs['place'] = warrior_sqlite.value("place")
                attribs['level'] = warrior_sqlite.value("level")
                attribs['leader'] = bool(warrior_sqlite.value("leader"))
                attribs['rank'] = int(warrior_sqlite.value("rank"))
                attribs['HP'] = int(warrior_sqlite.value("HP"))
                attribs['MP'] = int(warrior_sqlite.value("MP"))
                attribs['HP_max'] = int(warrior_sqlite.value("HP_max"))
                attribs['MP_max'] = int(warrior_sqlite.value("MP_max"))
                attribs['ATK'] = int(warrior_sqlite.value("ATK"))
                attribs['DEF'] = int(warrior_sqlite.value("DEF"))
                attribs['MATK'] = int(warrior_sqlite.value("MATK"))
                attribs['MDEF'] = bool(warrior_sqlite.value("MDEF"))
                attribs['AGL'] = int(warrior_sqlite.value("AGL"))
                attribs['LUCK'] = int(warrior_sqlite.value("LUCK"))
                attribs['description'] = bool(warrior_sqlite.value("description"))
                try : 
                    attribs['complete'] = int(warrior_sqlite.value("complete"))
                except ValueError: 
                    attribs['complete'] = 0
                #TODO compute state with history and life state
                attribs['status'] = "repos"
                warrior = Warrior(warrior_sqlite.value("ID"), warrior_sqlite.value("name"),attribs, groupe)
                nb_heros_added+=1
                self.progress.setValue(nb_heros_added)
                groupe.addWarrior(warrior)
                if warrior_sqlite.value("place"):
                    self.temples[int(warrior_sqlite.value("place"))].addHeros(warrior)
                    
            if parent_groupe != None : 
                parent_groupe.addSubGroupe(groupe)
        #warrior_sqlite = self.database.select("*", "gm_perso",False,"IDPerso=="+str(125))
        self.progress.setValue(nb_total)
        qWarning("Fin chargement de la bdd")

    def showResultInfos (self):
        msgBox = QtWidgets.QMessageBox()
        if len(self.factions) == 0:
            msgBox.setIcon( 2)
            msgBox.setText("Attention la base de donne semble etre vide: ("+self.database.database_name+")");
        else:
            #warning
            msgBox.setIcon( 1)
            msgBox.setText("Chargement effectue avec success")
        nb_faction=nb_empire=nb_kingdom=nb_groupe=nb_sub_group=nb_perso=0
        for faction in self.factions.values() :
            nb_faction+=1
            for empire in faction.empires.values():
                nb_empire+=1
                for kingdom in empire.kingdoms.values():
                    nb_kingdom+=1
                    for groupe in kingdom.groupes.values():
                        nb_groupe+=1
                        for sub_groupe in groupe.sub_groupes:
                            nb_sub_group+=1
                            for perso in sub_groupe.warriors.values():
                                nb_perso+=1
                        for perso in groupe.warriors.values():
                            nb_perso+=1
        

        informative_text = "<p>Le model charge contient : "
        informative_text = "<br>"+str(nb_faction)+" : factions"
        informative_text+="<br>"+str(nb_empire)+" : empires"
        informative_text+="<br>"+str(nb_kingdom)+" : kingdoms"
        informative_text+="<br>"+str(nb_groupe)+" : groupes"
        informative_text+="<br>"+str(nb_sub_group)+" : sous groupes"
        informative_text+="<br>"+str(nb_perso)+" : heros </p>"
        msgBox.setInformativeText(informative_text);

        msgBox.exec_()


            
    def findGroupeFromID (self, ident): 
        for faction in self.factions.values() :
            for empire in faction.empires.values():
                for kingdom in empire.kingdoms.values():
                    for groupe in kingdom.groupes.values():
                        if groupe.id == ident :
                            return groupe
        return None                

    def updateKingdom(self, id_kingdom,lat,lon):
        for faction in self.factions.values() :
            for empire in faction.empires.values():
                for kingdom in empire.kingdoms.values():
                    if kingdom.id == id_kingdom :
                        kingdom.attribs['latitude'] = lat 
                        kingdom.attribs['longitude'] = lon
                    
    def addFaction (self, faction):
        self.factions[faction.name] = faction
        
    def addTemple (self, temple):
        self.temples[temple.id] = temple


        