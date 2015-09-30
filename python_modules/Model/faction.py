from python_modules.config import Config
from python_modules.utils.sqlite_model import SqliteModel
from python_modules.model.empire import Empire
import os

class Faction:
    def __init__ (self, id_i, name,attribs,parent):
        self.id = id_i
        self.name = name
        self.empires= {}
        self.attribs = attribs
        self.parent = parent
        
    def model (self):
        return self.parent
    def addEmpire (self, empire):
        self.empires[empire.name] = empire
    
    def getAllGroupes (self):
        dict_groupes = {}
        for empire in self.empires.values() :
                dict_groupes.update(empire.getAllGroupes())
        return dict_groupes

    def getAllWarriors(self):
        dict_heros= {}
        for empire in self.empires.values :
                dict_heros.update(empire.getAllWarriors())
        return dict_heros
    
    def getDictAttributes(self):
        attribs = {}
        attribs['ID']=self.id
        attribs['name']=self.name

        attribs['icon']=self.attribs['icon']  
        return attribs

    def delete (self):
        while (len(self.empires)!= 0):
            for empire in self.empires.values():
                empire.delete()
                break
        self.model().database._delete("gm_faction","ID="+str(self.id))
        self.model().factions.pop(self.name)

    def createEmpire (self,name, default_values):
        result = self.model().database.select("ID+1","gm_empire",False,"ID + 1 not in (select ID from gm_empire)","ID")
        result.first()
        params = {}
        if 'empire' in default_values :
           # params = default_values['empire']
            params["color"]="255,0,0,0"
        else:
            params["color"]="255,0,0,0"
        empire = Empire(result.value("ID+1"), name,params,self)
        self.addEmpire(empire)
        attribs = empire.getDictAttributes()
        self.model().database.insert("gm_empire",attribs)
        empire.updateFromDisk(default_values)

    def updateFromDisk (self,default={}):
        path = os.path.join(Config().instance.path_to_pic())
        currentPath = os.path.join(path,self.name)
        print ('current path',currentPath)
        if os.path.exists(currentPath):
            list_empires = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
            #on supprime les groupe qui n existe plus
            print ('list_empires',list_empires)
            for empire in self.empires.values():
                if (empire.name in list_empires) == False :
                    empire.delete()
            
            for empire_name in list_empires:
                # on met a jours les groupes existant
                if empire_name in self.empires:
                    self.empires[empire_name].updateFromDisk(default)
                else:
                    #on cree un nouveau groupe
                    self.createEmpire(empire_name, default)
        else:
            self.delete()
    
    def getWarriorList(self):
        warrior_list = []
        for empire in self.empires.values() :
            warrior_list+=empire.getWarriorList()
        return warrior_list