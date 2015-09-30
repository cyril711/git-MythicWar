from python_modules.config import Config
from python_modules.utils.sqlite_model import SqliteModel
from python_modules.model.kingdom import Kingdom
import os

class Empire:
    
    def __init__ (self, id_i, name, attrib,parent):
        self.id = id_i
        self.name = name
        self.attrib = attrib
        self.attrib['icon'] = self.name+".png"
        self.kingdoms = {}
        self.parent= parent
    
    def getDictAttributes (self):
        attribs = {}
        attribs['name'] = self.name
        attribs['color']=self.attrib['color']
        attribs['icon']=self.attrib['icon']
        attribs['ID']=self.id
        attribs['ID_faction']=self.parent.id
        return attribs 
  
    def faction (self):
        return self.parent
    
    def model (self):
        return self.faction().parent
    def createKingdom (self,name, default_values = {}):
        
        result = self.model().database.select("ID+1","gm_kingdom",False,"ID + 1 not in (select ID from gm_kingdom)","ID")
        result.first()
        if 'kingdom' in default_values :
            params = default_values['kingdom']
        else:
            params = {}
            params ['armee']=''
            params ['description']=''
            params ['red']=255
            params ['green']=255
            params ['blue']=0
            params ['alpha']=255
        params['temples']=[]
        kingdom = Kingdom(result.value("ID+1"), name,params,self)
        self.addKingdom(kingdom)
        attribs = kingdom.getDictAttributes()
        self.model().database.insert("gm_kingdom",attribs)
        kingdom.updateFromDisk(default_values)
  
  
    def delete (self):
        while (len(self.kingdoms)!= 0):
            for kingdom in self.kingdoms.values():
                kingdom.delete()
                break
        self.model().database._delete("gm_empire","ID="+str(self.id))
        self.faction().empires.pop(self.name)
  
    def updateFromDisk (self,default={}):
        path = os.path.join(Config().instance.path_to_pic(),self.faction().name)
        currentPath = os.path.join(path,self.name)
        print ('current path',currentPath)
        if os.path.exists(currentPath):
            list_kingdoms = list(filter(SqliteModel.isValid,os.listdir(currentPath)))
            #on supprime les groupe qui n existe plus
            for kingdom in self.kingdoms.values():
                if (kingdom.name in list_kingdoms) == False :
                    print ('kingodm demande delete')
                    kingdom.delete()
            
            for kingdom_name in list_kingdoms:
                # on met a jours les groupes existant
                if kingdom_name in self.kingdoms:
                    print ('kingodm update')
                    self.kingdoms[kingdom_name].updateFromDisk(default)
                else:
                    print ('kingodm creation')
                    #on cree un nouveau groupe
                    self.createKingdom(kingdom_name, default)
        else:
            self.delete()
#     def getAllGroupes (self):
#         dict_groupes = {}
#         for kingdom in self.kingdoms.values():
#                 dict_groupes.update(kingdom.getAllGroupes())
#         return dict_groupes
#         
#     def getAllWarriors (self):
#         dict_heros= {}
#         for kingdom in self.kingdoms.values():
#                 dict_heros.update(kingdom.getAllWarriors())
#         return dict_heros        

    def addKingdom(self, kingdom):
        self.kingdoms[kingdom.name] = kingdom

    def getKingdomFromName (self,kingdom_name):        
        for kingdom in self.kingdoms.values():
            if kingdom.name == kingdom_name:
                return kingdom
        return None
    
    def getWarriorList(self,func=None):
        warrior_list = []
        for kingdom in self.kingdoms.values():
            warrior_list+=kingdom.getWarriorList(func)
        return warrior_list