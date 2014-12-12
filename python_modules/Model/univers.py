from python_modules.model.faction import Faction
from python_modules.model.empire import Empire
from python_modules.model.kingdom import Kingdom
from python_modules.model.warrior import Warrior
from python_modules.model.groupe import Groupe
from python_modules.model.temple import Temple
from python_modules.utils.database import DatabaseManager
from PyQt5.Qt import qDebug, QIcon, qWarning, QPointF, QFile
from PyQt5.QtCore import QObject, pyqtSignal
from python_modules.config import Config
from random import randint
import math
class Univers (QObject):
    #selection_changed = pyqtSignal()
    selection_updated = pyqtSignal()
    filtered_changed = pyqtSignal()
    askForHerosPage = pyqtSignal(Warrior)
    def __init__ (self,filename,parent=None):
        super(Univers,self).__init__(parent)

        self.settings = Config().instance.settings
        self.factions = {}
        self.temples = {}
        self.database = DatabaseManager(self.settings.value("global/database"))
        self.database.createConnection()
        self.database.setVerbose(False)
        
        self.loadFromFile(filename)
        self.currentFaction = None
        self.currentEmpire = None
        self.currentKingdom= None
        self.currentGroupe= None     
        self.selected_Warriors = []
        self.filtered_Warriors = []

        colors =  self.settings.value ("global/groupe_color").split(",")
        self.groupe_color_icons = {}
        for color in colors :
            icon = QIcon(":/textures/"+color)
            self.groupe_color_icons[color] = icon            
            
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
            print ('remove from selected warriors',warrior.name)
            self.selection_updated.emit()
        elif (warrior not in self.selected_Warriors) and (flag == True):
            self.selected_Warriors.append(warrior)
            print ('append from selected warriors',warrior.name)
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

    def dispatchCircleWarriors(self, origin, radius):
        for heros in self.selectedWarriors():
            x = randint(int(-radius),int(radius))
            y = (radius*radius) - (x*x)
            print ('sqrt(y)',math.sqrt(y))
            print ('rrr',origin,radius,y,x)
            print ('randrange',int(origin.y()-math.sqrt(y)),int(origin.y()+math.sqrt(y)))
            y = randint (int(-math.sqrt(y)),int(math.sqrt(y)))
            heros.latitude = origin.x()  +x 
            heros.longitude = origin.y()  +y 

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
    
    def save (self):
        print ("sauvegarde")
        for temple in self.temples.values() :
            attribs = temple.getDictAttributes ()
            self.database.update("gm_temple",attribs,"IDTemple="+str(temple.id))
#         for faction in self.factions.values() :
#             #attribs = faction.getDictAttributes ()
#             #self.database.update("gm_faction",attribs,"IDFaction="+str(faction.id))
#             for empire in faction.empires.values():
#                 #attribs = empire.getDictAttributes ()
#                 #self.database.update("gm_empire",attribs,"IDEmpire="+str(empire.id))
#                 for kingdom in empire.kingdoms.values():
#                     attribs = kingdom.getDictAttributes ()
#                     self.database.update("gm_kingdom",attribs,"IDKingdom="+str(kingdom.id))
#                     for groupe in kingdom.groupes.values():
#                         attribs = groupe.getDictAttributes ()
#                         self.database.update("gm_groupes",attribs,"IDGroupe="+str(groupe.id))
#                         for sub_groupe in groupe.sub_groupes:
#                             attribs = groupe.getDictAttributes ()
#                             self.database.update("gm_groupes",attribs,"IDGroupe="+str(groupe.id))
#                             for perso in sub_groupe.warriors.values():
#                                 attribs = perso.getDictAttributes ()
#                                 self.database.update("gm_perso",attribs,"IDPerso="+str(perso.id))
#                         for perso in groupe.warriors.values():
#                             attribs = perso.getDictAttributes ()
#                             self.database.update("gm_perso",attribs,"IDPerso="+str(perso.id))
        db_name = self.database.database.databaseName()
        try :
            QFile.remove(self.settings.value("global/database"))
        except OSError :
            qWarning("echec suppression ")
            pass

        if QFile.copy(db_name,self.settings.value("global/database")):
            qWarning("sauvegarde reussit")
        else:
            qDebug("Echec sauvegarde")
    def loadFromFile (self, filename):
        qWarning("debut chargement de la bdd")
        temples_sqlite = self.database.select("*", "gm_temple",False,None,"IDTemple ASC")
        while temples_sqlite.next():
            level_dict = {}
            for name,background in zip(temples_sqlite.value("Levels").split(','),temples_sqlite.value("Background").split(',')):
                level_dict[name] = background
            print ('temple :',temples_sqlite.value("Name"),temples_sqlite.value("Latitude"),temples_sqlite.value("Longitude"))
            pos = QPointF(float(temples_sqlite.value("Latitude")),float(temples_sqlite.value("Longitude")))
            temple = Temple(temples_sqlite.value("IDTemple"), temples_sqlite.value("Name"),pos,level_dict)
            self.addTemple (temple)
        faction_sqlite = self.database.select("*", "gm_faction",False,None,"IDFaction ASC")
        while faction_sqlite.next():
            attribs = {} 

            faction = Faction(faction_sqlite.value("IDFaction"), faction_sqlite.value("Name"),attribs)
            self.addFaction(faction)
            empire_sqlite = self.database.select("*", "gm_empire",False, "Faction=="+str(faction_sqlite.value("IDFaction")),"IDEmpire ASC")         
            while empire_sqlite.next():
                attribs = {}
                empire = Empire(empire_sqlite.value("IDEmpire"), empire_sqlite.value("Name"),attribs,faction)
                faction.addEmpire(empire)
                kingdom_sqlite = self.database.select("*", "gm_kingdom",False,"IDEmpire=="+str(empire_sqlite.value("Faction")),"IDKingdom ASC")
                while kingdom_sqlite.next():
                    attribs = {'armee':kingdom_sqlite.value("Armee"),'description':kingdom_sqlite.value("Description"),'red':int(kingdom_sqlite.value("Couleur").split(",")[0]),'green':int(kingdom_sqlite.value("Couleur").split(",")[1]),'blue':int(kingdom_sqlite.value("Couleur").split(",")[2]),'alpha':int(kingdom_sqlite.value("Couleur").split(",")[3])}
                    kingdom = Kingdom(kingdom_sqlite.value("IDKingdom"), kingdom_sqlite.value("Name"),attribs,empire)
                    empire.addKingdom(kingdom)
                    for t in kingdom_sqlite.value("Temples").split(','):
                        if t in self.temples: 
                            self.temples[t].setOwner(kingdom)      
                    groupe_sqlite = self.database.select("*", "gm_groupe",False,"IDKingdom=="+str(kingdom_sqlite.value("IDKingdom"))+" and Parent==0","IDGroupe ASC")
                    while groupe_sqlite.next():
                        attribs = {'description':groupe_sqlite.value("Description"),'color':groupe_sqlite.value("color")}
                        groupe = Groupe(groupe_sqlite.value("IDGroupe"), groupe_sqlite.value("Name"),attribs,kingdom)
                        kingdom.addGroupe(groupe)        
                        warrior_sqlite = self.database.select("*", "gm_perso",False,"IDGroup=="+str(groupe_sqlite.value("IDGroupe")),"IDPerso ASC")
                        while warrior_sqlite.next():
                            attribs = {}
                            attribs['picture'] = warrior_sqlite.value("RepresentativPic") 
                            attribs['latitude'] = warrior_sqlite.value("Latitude") 
                            attribs['longitude'] = warrior_sqlite.value("Longitude") 
                            attribs['place'] = warrior_sqlite.value("Place")
                            attribs['Level'] = warrior_sqlite.value("Level") 
                            attribs['leader'] = bool(warrior_sqlite.value("Leader")) 
                            warrior = Warrior(warrior_sqlite.value("IDPerso"), warrior_sqlite.value("Name"),attribs, groupe)
                            groupe.addWarrior(warrior)
                            warrior.selection_changed.connect(self.onSelectionChanged)
                            if warrior_sqlite.value("Place")!= '':
                                self.temples[int(warrior_sqlite.value("Place"))].addHeros(warrior)

        #gestion des sous groupes
        groupe_sqlite = self.database.select("*", "gm_groupe",False,"Parent!= 0","IDGroupe ASC")
        while groupe_sqlite.next():
            attribs = {'description':groupe_sqlite.value("Description"),'color':groupe_sqlite.value("color")}
            parent_groupe = self.findGroupeFromID(groupe_sqlite.value("Parent"))
            groupe = Groupe(groupe_sqlite.value("IDGroupe"), groupe_sqlite.value("Name"),attribs,parent_groupe,True)
            warrior_sqlite = self.database.select("*", "gm_perso",False,"IDGroup=="+str(groupe_sqlite.value("IDGroupe")),"IDPerso ASC")
            while warrior_sqlite.next():
                attribs = {}
                attribs['picture'] = warrior_sqlite.value("RepresentativPic") 
                attribs['latitude'] = warrior_sqlite.value("Latitude") 
                attribs['longitude'] = warrior_sqlite.value("Longitude")
                attribs['place'] = warrior_sqlite.value("Place")
                attribs['Level'] = warrior_sqlite.value("Level")
                attribs['leader'] = bool(warrior_sqlite.value("Leader"))
                warrior = Warrior(warrior_sqlite.value("IDPerso"), warrior_sqlite.value("Name"),attribs, groupe)
                groupe.addWarrior(warrior)
                if warrior_sqlite.value("Place"):
                    self.temples[int(warrior_sqlite.value("Place"))].addHeros(warrior)
                    
            if parent_groupe != None : 
                parent_groupe.addSubGroupe(groupe)
        #warrior_sqlite = self.database.select("*", "gm_perso",False,"IDPerso=="+str(125))
        qWarning("Fin chargement de la bdd")
            
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
                        kingdom.attribs['lat'] = lat 
                        kingdom.attribs['lon'] = lon
                    
    def addFaction (self, faction):
        self.factions[faction.name] = faction
        
    def addTemple (self, temple):
        self.temples[temple.id] = temple
        