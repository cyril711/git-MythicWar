from PyQt5.Qt import QDialog, QFileDialog
from python_modules.config import Config
import os
     
from python_modules.main_view.ui_dialog_import_groupe import Ui_DialogGroupeImport
from PyQt5 import QtWidgets, QtGui
     
class DialogGroupeImport (QDialog, Ui_DialogGroupeImport):
    def __init__ (self, path, parent=None):
        super(DialogGroupeImport, self).__init__(parent)
        print ('init DialogGroupeImport')
        self.setupUi(self)
        self.settings = Config().instance.settings
        self.default_widgets_list = []
        self.defaults_values = {}
        self.initDefaultItems ()
        self.path = path
        self.toolButton.clicked.connect(self.onGroupeChanged)

#        for faction_name in self.model.factions.keys() :
#            self.factionComboBox.addItem(str(faction_name))

    def onGroupeChanged (self):
        filename = QFileDialog.getExistingDirectory(self, caption='', directory=self.path)
        if filename != None:
            self.lineEditGroupe.setText(os.path.basename(filename))

    def processWidget (self, w):
        key = "database/default_" + w.objectName()
        if self.settings.contains(key):
            if type(w) == QtWidgets.QLineEdit :
                w.setText(self.settings.value(key))
            elif (type(w) == QtWidgets.QSpinBox) :
                w.setValue(int(self.settings.value(key)))
            elif (type(w) == QtWidgets.QDoubleSpinBox):
                w.setValue(float(self.settings.value(key)))
            elif type(w) == QtWidgets.QCheckBox :
                w.setChecked(bool(self.settings.value(key)))
            elif type(w) == QtWidgets.QComboBox:
                print ('combo BOx', w.objectName())
                key_multiple_choice = "database/available_" + w.objectName()
                if self.settings.contains(key_multiple_choice) :
                    values = self.settings.value(key_multiple_choice)
                    current_ind = 0
                    for i in range (len(values)) :
                        if values[i] == self.settings.value(key):
                            current_ind = i 
                        w.addItem(values[i])
                        print ('addItem', values[i])
                    w.setCurrentIndex(current_ind)
                else : 
                    qDebug("missing available  choice")
            elif type(w) == QtWidgets.QPushButton:
                # on espere qu il n y a qu un push button pour gerer la couleur des kingdoms
                color = self.settings.value(key)
                self.colorKingdom = QtGui.QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
                w.clicked.connect(self.onColorKingdomClicked)
                w.setStyleSheet("#" + w.objectName() + "{background-color: rgba(" + str(self.colorKingdom.red()) + "," + str(self.colorKingdom.green()) + "," + str(self.colorKingdom.blue()) + "," + str(self.colorKingdom.alpha()) + ");}")
                w.show()
        else:
            qDebug("erreur dans le fichier config la valeur par default n est pas definit", key)                    
        self.default_widgets_list.append(w)


        
    def initDefaultItems (self):
        self.default_widgets_list = []
        self.processWidget(self.groupe_color)
        self.processWidget(self.groupe_rank)
        self.processWidget(self.groupe_description)
        self.processWidget(self.heros_description) 
        self.processWidget(self.heros_historique) 
        self.processWidget(self.heros_latitude) 
        self.processWidget(self.heros_leader)
        self.processWidget(self.heros_level)
        self.processWidget(self.heros_longitude)
        self.processWidget(self.heros_place)
        self.processWidget(self.heros_rank)
        self.processWidget(self.heros_status)
        self.processWidget(self.heros_techniques)
        


            
    def iterateWidgets (self, w):
        if len(w.children()) == 0 :
            self.processWidget(w)
        else:
            for w1 in w.children():
                self.iterateWidgets(w1)
            
    def groupeName (self):
        return self.lineEditGroupe.text()

    
    
    
    def validate (self):
        self.defaults_values = {}
        self.defaults_values['groupe'] = {}
        self.defaults_values['heros'] = {}
        default_values_temp = {}
        for w in self.default_widgets_list:
            if type(w) == QtWidgets.QLineEdit :
                default_values_temp[w.objectName()] = w.text()

            elif (type(w) == QtWidgets.QSpinBox) or (type(w) == QtWidgets.QDoubleSpinBox):
                default_values_temp[w.objectName()] = w.value()
            elif type(w) == QtWidgets.QCheckBox :
                default_values_temp[w.objectName()] = w.isChecked()
            elif type(w) == QtWidgets.QComboBox:
                default_values_temp[w.objectName()] = w.currentText()
            elif type(w) == QtWidgets.QPushButton :
                color = [self.colorKingdom.red(), self.colorKingdom.green(), self.colorKingdom.blue(), self.colorKingdom.alpha()]
                default_values_temp[w.objectName()] = color
           # key = "database/default_"+w.objectName()
            # print ('key:',key)
            # self.settings.setValue(key,self.defaults_values[w.objectName()])    
        dict_heros = {}
        dict_groupe = {}
        for key ,value in zip(default_values_temp.keys(),default_values_temp.values()) :
            print('key',key)
            text_split = key.split("_")
            print ('text split',text_split)
            
            if text_split[0]=="heros":
                dict_heros[text_split[1]] = value
            elif  text_split[0]=="groupe":
                dict_groupe[text_split[1]] = value
        self.defaults_values['heros'] = dict_heros
        self.defaults_values['groupe'] = dict_groupe
        return self.defaults_values