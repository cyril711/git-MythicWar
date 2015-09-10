



class Temple:
    #levels un dictionnaire avec comme key le nom du level et en valeur le nom du background associe
    def __init__ (self, id_i, name,pos, levels,master=0):
        self.id = id_i
        self.name = name
        self.levels = levels
        self.owner = None
        self.heros = []
        self.position = pos
        self.master = master
        self.thumb = None
        
        
    def getDictAttributes (self):

        attribs = {}
        lvl = ''
        background = ''
        for key,value in zip(self.levels.keys(),self.levels.values()):
            if lvl != '':
                lvl = lvl+","
                background = background+","
            lvl = lvl+key
            background = background+value
        attribs['name'] = self.name
        attribs['levels'] = lvl
        attribs['backgrounds'] = background
        attribs['latitude'] = self.position.x()
        print ('position x temple',self.position.x())
        attribs['longitude'] = self.position.y()
        attribs['master'] = self.master
        print ('position y temple',self.position.y())
        return attribs
    def setOwner (self,kingdom):
        self.owner = kingdom
        
    def addHeros (self,heros):
        print ('add heros',heros.name)
        self.heros.append(heros)
        