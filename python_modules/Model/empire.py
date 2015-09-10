
class Empire:
    
    def __init__ (self, id_i, name, attrib,parent):
        self.id = id_i
        self.name = name
        self.attrib = attrib
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