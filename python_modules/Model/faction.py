

class Faction:
    def __init__ (self, id_i, name,attribs):
        self.id = id_i
        self.name = name
        self.empires= {}
        self.attribs = attribs
        
    def addEmpire (self, empire):
        self.empires[empire.name] = empire
        
    def getDictAttributes(self):  
        return self.attribs
    
    def getWarriorList(self):
        warrior_list = []
        for empire in self.empires.values() :
            warrior_list+=empire.getWarriorList()
        return warrior_list