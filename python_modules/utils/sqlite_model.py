from PyQt5.Qt import QMessageLogger
from python_modules.config import Config
from PyQt5.QtWidgets import QProgressDialog
from PyQt5 import QtCore, QtWidgets
import os


class SqliteModel ():
    def __init__(self,basepath):
        self.basepath = basepath

        self.stop = False
        self.echec_list = [] 
        
        
    def estimateNbPerso (self, fullpath):
        nombre_heros = 0
        try:
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
    
    def process(self,faction_name,empire_name,kingdom_name):

        self.faction = faction_name
        self.empire = empire_name
        self.kingdom = kingdom_name
        self.fullPath = os.path.join(self.basepath,self.faction,self.empire,self.kingdom,"Picture") 
        self.total_heros = self.estimateNbPerso(self.fullPath)
        self.progress = QProgressDialog ()
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.canceled.connect(self.onCanceled)



    def isValid (self, name):
        return name[0] != '~'

   

       
    def showResultInfos (self, infos_list):
        msgBox = QtWidgets.QMessageBox()
        if self.success == True :
            msgBox.setIcon( 1)
            msgBox.setText("Generation de miniatures details : ("+self.faction+"-"+self.empire+"-"+self.kingdom+")");

            #information 
        else:
            #warning
            msgBox.setIcon( 2)
            msgBox.setText("Attention : il semblerait que les champs ne soient pas correctement renseignes ou que l arborescence des fichiers de nsoit pas bonne")
        informative_text = "<p>"
        for item  in infos_list:
            informative_text+="<br>"+str(item[0])+" : "+str(item[1])+" "
        informative_text+="</p>"
        msgBox.setInformativeText(informative_text);        
        if len(self.echec_list) != 0:
            detailed_text = ''
            for text in self.echec_list :
                detailed_text = detailed_text + " \n " + text
            msgBox.setDetailedText(detailed_text)
        msgBox.exec_()
