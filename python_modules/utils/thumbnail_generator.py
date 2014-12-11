from PyQt5.Qt import  QXmlStreamWriter, QFile, QImage, qDebug
import os
from PyQt5 import QtCore

class ThumbnailGenerator ():
    def __init__(self,basepath):
        self.dir = None
        self.basepath = basepath
        self.low_ext = "-low"
        self.midle_ext = "-mid"
        self.thumb_width = 100
        self.thumb_ext = "portrait_thumbnail"
        self.portrait_ext = "portrait"
    def generateFor1Kingdom (self,faction,empire,kingdom):
        self.fullPath = self.basepath+"\\"+faction+"\\"+empire+"\\"+kingdom 
        list_data = os.listdir (self.fullPath)
        find = False
        for data in list_data : 
            if data == "Picture" :
                find = True
                break
        if find == True :
            self.fullPath = self.fullPath+"\\"+"Picture"
            list_group = os.listdir (self.fullPath)
            for group in list_group : 
                currentPath = self.fullPath +"\\"+group
                if group[0] != '~' :
                    print ("Group Name Th generator: ", group)                    
                    list_perso = os.listdir (currentPath)
                    if os.path.isdir(currentPath+"\\"+list_perso[0]):
                        list_perso_tmp = os.listdir(currentPath+"\\"+list_perso[0])
                        if os.path.isdir(currentPath+"\\"+list_perso[0]+"\\"+list_perso_tmp[0]):
                            sub_group = list_perso[0]
                            currentPath = currentPath + "\\"+sub_group
                            list_perso = os.listdir(currentPath)
                            print ('sub groupe',sub_group)
                    else:
                        print(' not dir')
                    for perso in list_perso:
                        if (perso [0] != '~') and (os.path.isdir(currentPath+"\\"+perso)):
                            list_pic = os.listdir (currentPath+"\\"+perso)
                            print ('perso',perso)
                            if len(list_pic) > 0 : 
                                find = False
                                #indice = 0
                                for pic in list_pic :
                                    if self.thumb_ext not in pic : 
                                        if "portrait" in pic :
                                            find = True    
                                            thumbnail = QImage(currentPath+"\\"+perso+"\\"+pic)
                                            thumbnail = thumbnail.scaledToWidth(self.thumb_width)
                                            pic_basename = pic.split(".")
                                            result = thumbnail.save(currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                            try:
                                                gg = os.rename(currentPath+"\\"+perso+"\\"+pic, currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
                                                print ("IN ",currentPath+"\\"+perso+"\\"+pic)
                                                print ("OUT ",currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
                                                print ('resultat rename = ',gg)
                                            except FileExistsError :
                                                pass
                                            print (currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                            if result == False :
                                                try : 
                                                    print (perso)
                                                    qDebug("Echec de la creation de la miniature :"+currentPath+"\\"+perso+"\\"+pic_basename[0]+self.thumb_ext+"."+pic_basename[1])
                                                except UnicodeEncodeError :
                                                    qDebug("echec sauvegarde ****")
                                        else :
                                            pass 
                                            #self.writer.writeAttribute("alias", midle_path+"\\"+perso+"\\pic-0"+str(indice))
                                            #indice = indice + 1
                                if find == False : 
                                    find2 = False
                                    for pic in list_pic :
                                        if self.thumb_ext not in pic :
                                            find2 = True
                                            break
                                    if find2 == True :  
                                        thumbnail = QImage(currentPath+"\\"+perso+"\\"+pic)
                                        thumbnail = thumbnail.scaledToWidth(self.thumb_width)
                                        pic_basename = pic.split(".")
                                        result = thumbnail.save(currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                        if result == False : 
                                            try : 
                                                qDebug("Echec de la creation de la miniature :"+currentPath+"\\"+perso+"\\"+pic_basename[0]+self.thumb_ext+"."+pic_basename[1])
                                            except UnicodeEncodeError :
                                                qDebug("echec sauvegarde ****")
                                        try:
                                            gg = os.rename(currentPath+"\\"+perso+"\\"+pic, currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
                                        except FileExistsError :
                                            pass
                                    else: 
                                        qDebug("no portrait found")
                            else :
                                pass