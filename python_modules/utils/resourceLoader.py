from PyQt5.Qt import  QXmlStreamWriter, QFile
import os
from PyQt5 import QtCore

class ResourceLoader ():
    def __init__(self,basepath):
        self.dir = None
        self.basepath = basepath
        self.thumb_ext = "portrait_thumbnail"
        fileName = "../resources.qrc"
        self.file = QFile(fileName)                
        self.file.open(QtCore.QIODevice.WriteOnly | QFile.Text);
        self.writer = QXmlStreamWriter(self.file)

        self.writer.setAutoFormatting(True)
        self.writer.writeStartDocument()
        self.writer.writeEmptyElement ("!DOCTYPE RCC")
        self.writer.writeStartElement("RCC")
        self.writer.writeAttribute("version", str(1.0))
        self.writer.writeStartElement("qresource")
        

    def finish (self):
        self.writer.writeEndElement()
        self.writer.writeEndElement()
        self.writer.writeEndDocument()
        self.file.close()
    def kingdomLoader (self,faction,empire,kingdom):
        self.fullPath = self.basepath+"/"+faction+"/"+empire+"/"+kingdom 

        list_data = os.listdir (self.fullPath)
        find = False

        for data in list_data : 
            if data == "Picture" :
                find = True
                break
        if find == True :
            self.fullPath = self.fullPath+"/"+"Picture"
            list_group = os.listdir (self.fullPath)
            for group in list_group : 
                sub_group = ""
                if group[0] != '~' :                    
                    currentPath = self.fullPath+"/"+group
                    alias = faction+"/"+empire+"/"+kingdom +"/"+group
                    list_perso = os.listdir (currentPath)
                    # gestion des sous groupes
                    if os.path.isdir(list_perso[0]):
                        sub_group = list_perso[0]
                        currentPath = currentPath + "/"+sub_group
                        alias = alias +"/"+sub_group
                        list_perso = os.listdir (currentPath)
                    for perso in list_perso:
                        if (perso [0] != '~') and (not "Thumb" in perso) and (os.path.isdir(currentPath+ "/"+perso)):
                            list_pic = os.listdir (currentPath+ "/"+perso)
                            if len(list_pic) > 0 : 
                                find = False
                                indice = 0
                                for pic in list_pic :
                                    self.writer.writeStartElement("file")
                                    if "portrait" in pic :
                                        find = True    
                                        if self.thumb_ext not in pic:
                                            self.writer.writeAttribute("alias", alias+"/"+perso+"/portrait")
                                        else :
                                            self.writer.writeAttribute("alias", alias+"/"+perso+"/portrait_thumbnail")
                                    else : 
                                        self.writer.writeAttribute("alias", alias+"/"+perso+"/pic-0"+str(indice))
                                        indice = indice + 1
                                    self.writer.writeCharacters(currentPath+ "/"+perso+"/"+pic)
                                    self.writer.writeEndElement()
                                if find == False : 
                                    ind_portrait = -1
                                    ind_thumb = -1
                                    indice = 0
                                    for pic in list_pic :
                                        if self.thumb_ext not in pic :
                                            ind_thumb = indice
                                        else:
                                            ind_portrait = indice
                                        indice = indice + 1
                                    if ind_portrait != -1 : 
                                        self.writer.writeStartElement("File")
                                        self.writer.writeAttribute("alias", alias+"/"+perso+"/portrait")
                                        self.writer.writeCharacters(currentPath+ "/"+perso+"/"+list_pic[ind_portrait])
                                        self.writer.writeEndElement()
                                    if ind_thumb != -1 : 
                                        self.writer.writeStartElement("File")
                                        self.writer.writeAttribute("alias", alias+"/"+perso+"/portrait_thumbnail")
                                        self.writer.writeCharacters(currentPath+ "/"+perso+"/"+list_pic[ind_thumb])
                                        self.writer.writeEndElement()
                            else :
                                print ("ALERT : no picture found for ", perso)

                                
