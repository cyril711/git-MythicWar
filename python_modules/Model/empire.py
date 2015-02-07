
class Empire:
    
    def __init__ (self, id_i, name, attrib,parent):
        self.id = id_i
        self.name = name
        self.attrib = attrib
        self.kingdoms = {}
        self.parent= parent
    
    def getDictAttributes (self):
        attribs = {}
        
        return attribs 
        
    def addKingdom(self, kingdom):
        self.kingdoms[kingdom.name] = kingdom
        
    def getWarriorList(self):
        warrior_list = []
        for kingdom in self.kingdoms.values():
            warrior_list+=kingdom.getWarriorList()
        return warrior_list