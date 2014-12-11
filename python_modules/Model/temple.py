



class Temple:
    #levels un dictionnaire avec comme key le nom du level et en valeur le nom du background associe
    def __init__ (self, id_i, name,pos, levels):
        self.id = id_i
        self.name = name
        self.levels = levels
        self.owner = None
        self.heros = []
        self.position = pos
        
        
    def getDictAttributes (self):
        attribs = {}
        attribs['name'] = self.name
        lvl = ''
        background = ''
        for key,value in zip(self.levels.keys(),self.levels.values()):
            if lvl != '':
                lvl = lvl+","
                background = background+","
            lvl = lvl+key
            background = background+value
        attribs['Levels'] = lvl
        attribs['Background'] = background
        attribs['Latitude'] = self.position.x()
        attribs['Longitude'] = self.position.y()
        return attribs
    def setOwner (self,kingdom):
        self.owner = kingdom
        
    def addHeros (self,heros):
        print ('add heros',heros.name)
        self.heros.append(heros)
        