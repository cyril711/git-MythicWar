from PyQt5.Qt import  QXmlStreamWriter, QFile, QImage, qDebug
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QProgressDialog

class ThumbnailGenerator ():
    def __init__(self,basepath):
        self.dir = None
        self.basepath = basepath
#         self.low_ext = "-low"
#         self.midle_ext = "-mid"
        self.stop = False
        self.thumb_width = 100
        self.thumb_ext = "portrait_thumbnail"
        self.portrait_ext = "portrait"
    def setParameters (self, thumb_width):
        self.thumb_width = thumb_width
        
    def estimateNbPerso (self, fullpath):

        nombre_heros = 0
        try:
            list_data = os.listdir (fullpath)
            find = False
            for data in list_data : 
                if data == "Picture" :
                    find = True
                    break
            if find == True :
                fullpath = os.path.join(fullpath,"Picture")
                list_group = os.listdir (fullpath)
                for group in list_group : 
                    currentPath = os.path.join(fullpath,group)
                    if group[0] != '~' :                   
                        list_perso = os.listdir (currentPath)
                        if os.path.isdir(os.path.join(currentPath,list_perso[0])):
                            list_perso_tmp = os.listdir(os.path.join(currentPath,list_perso[0]))
                            if os.path.isdir(os.path.join(currentPath,list_perso[0],list_perso_tmp[0])):
                                sub_group = list_perso[0]
                                currentPath = os.path.join(currentPath,sub_group)
                                list_perso = os.listdir(currentPath)
                        for perso in list_perso:
                            if (perso [0] != '~') and (os.path.isdir(os.path.join(currentPath,perso))):
                                nombre_heros+=1
        except FileNotFoundError :
            pass        

        return nombre_heros

    def onCanceled (self):
        self.stop = True

    def generateFor1Kingdom (self,faction,empire,kingdom):
        self.faction = faction
        self.empire = empire
        self.kingdom = kingdom
        self.nb_echec_thumb_creation = 0
        self.nb_success_thumb_creation = 0
        self.nb_rename = 0
        self.nb_rename_failed = 0
        self.sucess = False
        self.echec_list = []
        self.fullPath = os.path.join(self.basepath,faction,empire,kingdom) 
        total_perso = self.estimateNbPerso(self.fullPath)
        progress = QProgressDialog ("Creation des miniatures","Cancel",0,total_perso)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.canceled.connect(self.onCanceled)
        
        nb_perso = 0

        try:
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
                     #   print ("Group Name Th generator: ", group)                    
                        list_perso = os.listdir (currentPath)
                        if os.path.isdir(currentPath+"\\"+list_perso[0]):
                            list_perso_tmp = os.listdir(currentPath+"\\"+list_perso[0])
                            if os.path.isdir(currentPath+"\\"+list_perso[0]+"\\"+list_perso_tmp[0]):
                                sub_group = list_perso[0]
                                currentPath = currentPath + "\\"+sub_group
                                list_perso = os.listdir(currentPath)
                    #            print ('sub groupe',sub_group)
                        else:
                            print(' not dir')
                        for perso in list_perso:
                            if (perso [0] != '~') and (os.path.isdir(currentPath+"\\"+perso)):
                                list_pic = os.listdir (currentPath+"\\"+perso)
                            #    print ('perso',perso)
                                if len(list_pic) > 0 : 
                                    find = False
                                    #indice = 0
                                    for pic in list_pic :
                                        self.sucess = True
                                        if self.thumb_ext not in pic : 
                                            if "portrait" in pic :
                                                find = True    
                                                thumbnail = QImage(currentPath+"\\"+perso+"\\"+pic)
                                                if (thumbnail.isNull()):
                                                    print ('IMAGE NULL',currentPath+"\\"+perso+"\\"+pic)
                                                thumbnail = thumbnail.scaledToWidth(self.thumb_width)
                                                pic_basename = pic.split(".")
                                                result = thumbnail.save(currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                                try:
                                                    gg = os.rename(currentPath+"\\"+perso+"\\"+pic, currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
#                                                     print ("IN ",currentPath+"\\"+perso+"\\"+pic)
#                                                     print ("OUT ",currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
#                                                     print ('resultat rename = ',gg)
                                                    self.nb_rename+=1
                                                except FileExistsError :
                                                    self.nb_rename_failed+=1
                                                    pass
                                                print (currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                                if result == False :
                                                    self.nb_echec_thumb_creation += 1
                                                    try : 
                                                        print (perso)
                                                        qDebug("Echec de la creation de la miniature :"+currentPath+"\\"+perso+"\\"+pic_basename[0]+self.thumb_ext+"."+pic_basename[1])
                                                        self.echec_list.append(currentPath+"\\"+perso+"\\"+self.thumb_ext+".jpg")
                                                        
                                                    except UnicodeEncodeError :
                                                        qDebug("echec sauvegarde ****")

                                                else:
                                                    self.nb_success_thumb_creation += 1
                                            else :
                                                pass 
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
                                                    self.echec_list.append(currentPath+"\\"+perso+"\\"+pic_basename[0]+self.thumb_ext+"."+pic_basename[1])
                                                except UnicodeEncodeError :
                                                    qDebug("echec sauvegarde ****")
                                                self.nb_echec_thumb_creation += 1
                                            else:
                                                self.nb_success_thumb_creation += 1
                                            try:
                                                gg = os.rename(currentPath+"\\"+perso+"\\"+pic, currentPath+"\\"+perso+"\\"+self.portrait_ext+".jpg")
                                                self.nb_rename+=1
                                            except FileExistsError :
                                                self.nb_rename_failed+=1
                                                pass
                                        else: 
                                            qDebug("no portrait found")
                                else :
                                    pass
                            nb_perso +=1
                            progress.setValue(nb_perso)
        except FileNotFoundError :
            pass
        progress.setValue(total_perso)
        self.showResultInfos()
        
    def showResultInfos (self):
        msgBox = QtWidgets.QMessageBox()
       # msgBox.setIcon(QtWidgets.QMessageBox.Information);
        #msgBox.setStandardButton()
        if self.sucess == True :
            msgBox.setIcon( 1)
            msgBox.setText("Generation de miniatures details : ("+self.faction+"-"+self.empire+"-"+self.kingdom+")");

            #information 
        else:
            #warning
            msgBox.setIcon( 2)
            msgBox.setText("Attention : il semblerait que les champs ne soient pas correctement renseignes ou que l arborescence des fichiers de nsoit pas bonne")
        msgBox.setInformativeText("<p><br>"+str(self.nb_success_thumb_creation)+" : miniatures crees <br>"+str(self.nb_echec_thumb_creation)+" : echec creation miniature<br>"+str(self.nb_rename)+" : fichiers renomes<br>"+str(self.nb_rename_failed)+" : echec de renomage</p>");        
        if len(self.echec_list) != 0:
            detailed_text = ''
            for text in self.echec_list :
                detailed_text = detailed_text + " \n " + text
            msgBox.setDetailedText(detailed_text)
        msgBox.exec_()
