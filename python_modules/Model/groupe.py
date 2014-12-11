
class Groupe:
    
    def __init__ (self, id_i, name, attrib,parent,sub=False):
        self.id = id_i
        self.name = name
        self.attribs = attrib
        self.warriors = {}
        self.parent = parent
        self.sub_groupes = []
        #indique que c est un sous groupe
        self.sub = sub

    def isSub (self):
        return self.sub

    def getDictAttributes (self):
        attribs = {}
        attribs ["Description"]=self.attribs['description']
        attribs['color']=self.attribs["color"]
        return attribs
    
    def warriorsList(self):
        if len(self.sub_groupes)!=0:
            warriors = {}
            for g in self.sub_groupes :
                warriors.update(g.warriorsList())
            return warriors
        else:
            return self.warriors
    def addSubGroupe (self,groupe):
        self.sub_groupes.append(groupe)
    def addWarrior(self, warrior):
        self.warriors[warrior.id] = warrior