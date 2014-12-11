
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