from PyQt5.Qt import QPointF




class Temple:
    #levels un dictionnaire avec comme key le nom du level et en valeur le nom du background associe
    def __init__ (self, id_i, name, kingdom, pos, levels,master=0):
        self.id = id_i
        self.name = name
        self.levels = levels
        self.parent = kingdom
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
        attribs['ID'] = self.id
        print ('position x temple',self.position.x())
        attribs['longitude'] = self.position.y()
        attribs['master'] = self.master
        print ('position y temple',self.position.y())
        return attribs
    def setOwner (self,kingdom):
        self.owner = kingdom
    
    def changePosition (self, lat, lon):
        self.position.setX(  lat)
        self.position.setY (lon)
        
    def kingdom (self):
        return self.parent
    
    def empire (self):
        return self.kingdom().empire()
    def addHeros (self,heros):
        print ('add heros',heros.name)
        self.heros.append(heros)
        