from PyQt5.Qt import  QImage, qDebug, QMessageLogger
import os


from python_modules.utils.sqlite_model import SqliteModel
from python_modules.config import Config

class ThumbnailGenerator (SqliteModel):
    def __init__(self,basepath):
        super(ThumbnailGenerator,self).__init__(basepath)
        self.thumb_width = 100
        self.thumb_ext = "portrait_thumbnail"
        self.portrait_ext = "portrait"        
        # resultats info
        self.nb_echec_thumb_creation = ["echecs de creation de miniatures",0]
        self.nb_success_thumb_creation = ["miniatures crees",0]
        self.nb_rename = ["images renomees",0]
        self.nb_rename_failed = ["echecs de renommage",0]


    def setParameters (self, thumb_width):
        self.thumb_width = thumb_width
        





    def createThumb (self,path_to_perso):

        list_pic = os.listdir (path_to_perso)
        if len(list_pic) > 0 : 
            find = False
            for pic in list_pic :
                self.success = True
                if self.thumb_ext not in pic : 
                    if "portrait" in pic :
                        find = True    
                        thumbnail = QImage(os.path.join(path_to_perso,pic))
                        if (thumbnail.isNull()):
                            print ('IMAGE NULL',os.path.join(path_to_perso,pic))
                        thumbnail = thumbnail.scaledToWidth(self.thumb_width)
                        pic_basename = pic.split(".")
                        result = thumbnail.save(os.path.join(path_to_perso,self.thumb_ext+".jpg"))
                            
                        try:
                            os.rename(os.path.join(path_to_perso,pic),os.path.join(path_to_perso,self.portrait_ext+".jpg"))
                            self.nb_rename[1] = self.nb_rename[1]+1
                        except FileExistsError :
                            self.nb_rename_failed[1] = self.nb_rename_failed[1]+1
                            pass
                        if result == False :
                            self.nb_echec_thumb_creation[1] = self.nb_echec_thumb_creation[1]+ 1
                            try : 
                                qDebug("Echec de la creation de la miniature :"+os.path.join(path_to_perso,self.thumb_ext+".jpg"))
                                self.echec_list.append("FAILED save"+str(os.path.join(path_to_perso,self.thumb_ext+".jpg")))
                                
                            except UnicodeEncodeError :
                                qDebug("echec sauvegarde ****")

                        else:
                            self.nb_success_thumb_creation[1] = self.nb_success_thumb_creation[1]+1
                    else :
                        pass 
            #une image principale n existe pas
            if find == False : 
                #on fait l hypothese que portrai_ext et thumb_ext contienne tous 2 le mot "portrait"
                thumbnail = QImage(os.path.join(path_to_perso,pic))
                thumbnail = thumbnail.scaledToWidth(self.thumb_width)
                pic_basename = pic.split(".")
                result = thumbnail.save(os.path.join(path_to_perso,self.thumb_ext+".jpg"))
                if result == False : 
                    try : 
                        qDebug("Echec de la creation de la miniature :"+str(os.path.join(path_to_perso,self.thumb_ext+".jpg")))
                        self.echec_list.append("FAILED save"+str(os.path.join(path_to_perso,self.thumb_ext+".jpg")))
                    except UnicodeEncodeError :
                        qDebug("echec sauvegarde ****")
                    self.nb_echec_thumb_creation[1] = self.nb_echec_thumb_creation[1]+1
                else:
                    self.nb_success_thumb_creation[1] = self.nb_success_thumb_creation[1] + 1
                try:
                    os.rename(os.path.join(path_to_perso,pic), os.path.join(path_to_perso,self.portrait_ext+".jpg"))
                    self.nb_rename[1] = self.nb_rename[1] + 1
                except FileExistsError :
                    self.nb_rename_failed[1] = self.nb_rename_failed[1] + 1
                    pass
            else: 
                self.echec_list.append("FAILED no portrait found"+str(path_to_perso))



    def process (self,faction,empire,kingdom):
        #QMessageLogger(str(Config().instance.settings.value("global/log"),0,"DEBUT CREATION THUMBS ("+faction+","+empire+","+kingdom+")"))
        super(ThumbnailGenerator,self).process(faction,empire,kingdom)
        nb_perso = 0
        self.progress.setLabelText("Creation des miniatures")
        self.progress.setCancelButton("Cancel")
        self.progress.setMinimum(0)
        self.progress.setMaximum(self.total_heros)
        try:
            if os.path.exists(self.fullPath):
                list_group = list(filter(self.isValid,os.listdir (self.fullPath)))
                for group in list_group : 
                    currentPath = os.path.join(self.fullPath ,group)              
                    list_perso = os.listdir (currentPath)
                    if os.path.isdir(currentPath+"\\"+list_perso[0]):
                        list_perso_tmp = os.listdir(os.path.join(currentPath,list_perso[0]))
                        if os.path.isdir(os.path.join(currentPath,list_perso[0],list_perso_tmp[0])):
                            sub_group = list_perso[0]
                            currentPath = currentPath + "\\"+sub_group
                            list_perso = os.listdir(currentPath)
                    else:
                        print(' not dir')
                    for perso in list(filter(self.isValid,list_perso)):
                        path_to_perso = os.path.join(currentPath,perso)
                        self.createThumb(path_to_perso)
                        nb_perso +=1
                        self.progress.setValue(nb_perso)
                        if self.stop == True :
                            break
                    if self.stop == True :
                        break
                            
        except FileNotFoundError :
            pass
        self.progress.setValue(self.total_heros)
        result_info = [self.nb_success_thumb_creation,self.nb_echec_thumb_creation,self.nb_rename,self.nb_rename_failed]
        self.showResultInfos(result_info)
        #QMessageLogger(str(Config().instance.settings.value("global/log"),0,"FIN CREATION THUMB"))
 