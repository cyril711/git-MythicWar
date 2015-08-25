
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

    def kingdom (self):
        if self.isSub():
            return self.parent.parent
        else:
            return self.parent

    def getDictAttributes (self):
        attribs = {}
        attribs ['description']=self.attribs['description']
        attribs['color']=str(self.attribs["color"])
        attribs['rank']=int(self.attribs["rank"])
        attribs['name']=self.name
        attribs['ID']=self.id
        if self.isSub():
            attribs['parent'] = self.parent.id
            attribs['ID_kingdom'] =  self.parent.parent.id
        else:
            attribs['parent']=0
            attribs['ID_kingdom'] =  self.parent.id
        return attribs

    def getWarriorList(self):
        warrior_list = []
        if len(self.sub_groupes)!=0:
            for g in self.sub_groupes :
                warrior_list+=g.getWarriorList()
        else:
            for w in self.warriors.values():
                warrior_list.append(w)
        return warrior_list
    
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