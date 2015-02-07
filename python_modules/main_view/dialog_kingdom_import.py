from PyQt5.Qt import QDialog, qDebug, QColorDialog, QAction, QFileDialog
from python_modules.config import Config
import os
     
from python_modules.main_view.ui_dialog_import_kingdom import Ui_DialogKingdomImport
from PyQt5 import QtWidgets, QtGui
     
class DialogKingdomImport (QDialog, Ui_DialogKingdomImport):
    def __init__ (self,model,parent=None):
        super(DialogKingdomImport,self).__init__(parent)
        print ('init DialogKingdomImport')
        self.setupUi(self)
        self.model = model
        self.settings = Config().instance.settings
        self.currentEmpire = None
        self.currentFaction = None
        self.currentKingdom = None
        self.default_widgets_list = []
        self.defaults_values = {}
        self.initDefaultItems ()
#         self.factionComboBox.currentIndexChanged['QString'].connect(self.updateFromFactionCBox)
#         self.empireComboBox.currentIndexChanged['QString'].connect(self.updateFromEmpireCBox)
#         self.kingdomComboBox.currentIndexChanged['QString'].connect(self.updateFromKingdomCBox)
        self.toolButtonFaction.clicked.connect(self.onFactionChanged)
        self.toolButtonEmpire.clicked.connect(self.onEmpireChanged)
        self.toolButtonKingdom.clicked.connect(self.onKingdomChanged)
        for faction_name in self.model.factions.keys() :
            self.factionComboBox.addItem(str(faction_name))

    def onKingdomChanged (self):
        filename = QFileDialog.getExistingDirectory(self, caption='Kingdom ? ', directory=self.settings.value("global/resources_path"))
        if filename != None:
            self.lineEditKingdom.setText(os.path.basename(filename))
    
    def onFactionChanged (self):
        filename = QFileDialog.getExistingDirectory(self, caption='Faction ? ', directory=self.settings.value("global/resources_path"))
        if filename != None:
            self.lineEditFaction.setText(os.path.basename(filename))
                    
    def onEmpireChanged (self):
        filename = QFileDialog.getExistingDirectory(self, caption='Empire ? ', directory=self.settings.value("global/resources_path"))
        if filename != None:
            self.lineEditEmpire.setText(os.path.basename(filename))
    def processWidget (self, w):
        key = "database/default_"+w.objectName()
        if self.settings.contains(key):
            if type(w) == QtWidgets.QLineEdit :
                w.setText(self.settings.value(key))
            elif (type(w)== QtWidgets.QSpinBox) :
                w.setValue(int(self.settings.value(key)))
            elif (type(w)== QtWidgets.QDoubleSpinBox):
                w.setValue(float(self.settings.value(key)))
            elif type(w) == QtWidgets.QCheckBox :
                w.setChecked(bool(self.settings.value(key)))
            elif type(w) == QtWidgets.QComboBox:
                print ('combo BOx',w.objectName())
                key_multiple_choice = "database/available_"+w.objectName()
                if self.settings.contains(key_multiple_choice) :
                    values = self.settings.value(key_multiple_choice)
                    current_ind = 0
                    for i in range (len(values)) :
                        if values[i] == self.settings.value(key):
                            current_ind = i 
                        w.addItem(values[i])
                        print ('addItem',values[i])
                    w.setCurrentIndex(current_ind)
                else : 
                    qDebug("missing available  choice")
            elif type(w) == QtWidgets.QPushButton:
                #on espere qu il n y a qu un push button pour gerer la couleur des kingdoms
                color = self.settings.value(key)
                self.colorKingdom = QtGui.QColor(int(color[0]),int(color[1]),int(color[2]),int(color[3]))
                w.clicked.connect(self.onColorKingdomClicked)
                w.setStyleSheet("#"+w.objectName()+"{background-color: rgba("+str(self.colorKingdom.red())+","+str(self.colorKingdom.green())+","+str(self.colorKingdom.blue())+","+str(self.colorKingdom.alpha())+");}")
                w.show()
        else:
            qDebug("erreur dans le fichier config la valeur par default n est pas definit",key)                    
        self.default_widgets_list.append(w)


        
    def initDefaultItems (self):
        self.default_widgets_list = []
        self.processWidget(self.groupe_color)
        self.processWidget(self.groupe_rank)
        self.processWidget(self.groupe_description)
        self.processWidget(self.kingdom_armee)
        self.processWidget(self.kingdom_description)
        self.processWidget(self.kingdom_couleur) 
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
            
    def factionName (self):
        return self.lineEditFaction.text()

    def empireName (self):
        return self.lineEditEmpire.text()
    
    def kingdomName (self):
        return self.lineEditKingdom.text()
    

    def onColorKingdomClicked (self):
        
        dlg = QColorDialog(self.colorKingdom )
        dlg.setOption(QColorDialog.ShowAlphaChannel,True)
        if dlg.exec_() == QDialog.Accepted:
            self.colorKingdom  = dlg.currentColor()
            self.sender().setStyleSheet("#"+self.sender().objectName()+"{background-color: rgba("+str(self.colorKingdom.red())+","+str(self.colorKingdom.green())+","+str(self.colorKingdom.blue())+","+str(self.colorKingdom.alpha())+");}")
            self.sender().show()                    
        else:
            dlg.close()
    
    
    def validate (self):
        self.defaults_values = {}
        for w in self.default_widgets_list:
            if type(w) == QtWidgets.QLineEdit :
                self.defaults_values[w.objectName()] = w.text()

            elif (type(w)== QtWidgets.QSpinBox) or (type(w)== QtWidgets.QDoubleSpinBox):
                self.defaults_values[w.objectName()] = w.value()
            elif type(w) == QtWidgets.QCheckBox :
                self.defaults_values[w.objectName()] = w.isChecked()
            elif type(w) == QtWidgets.QComboBox:
                self.defaults_values[w.objectName()] = w.currentText()
            elif type(w) == QtWidgets.QPushButton :
                color = [self.colorKingdom.red(),self.colorKingdom.green(),self.colorKingdom.blue(),self.colorKingdom.alpha()]
                self.defaults_values[w.objectName()] = color
            key = "database/default_"+w.objectName()
            print ('key:',key)
            self.settings.setValue(key,self.defaults_values[w.objectName()])    
    
#     
#     def updateFromFactionCBox (self, value):
#  #       self.empireComboBox.blockSignals(True)
#         self.empireComboBox.clear()  
#   #      self.kingdomComboBox.blockSignals(True)
#         self.kingdomComboBox.clear()
#         if value in self.model.factions :
#             self.currentFaction = self.model.factions[value]
#             print ('current Faction ', self.currentFaction)
#             for empire in self.currentFaction.empires.values() :
#                 self.empireComboBox.addItem(str(empire.name))
#         else:
#             self.currentFaction = None
#    #     self.empireComboBox.blockSignals(False)
#    #     self.kingdomComboBox.blockSignals(False)
#         
#     def updateFromEmpireCBox (self, value):
#     #    self.kingdomComboBox.blockSignals(True)
#         self.kingdomComboBox.clear()
#         self.currentKingdom = None
#         if self.currentFaction != None :
#             if value in self.currentFaction.empires.keys() :
#                 self.currentEmpire = self.currentFaction.empires[value]
# 
#                 for kingdom in self.currentEmpire.kingdoms.values():
#                     self.kingdomComboBox.addItem(str(kingdom.name))
#             else:
#                 self.currentEmpire = None
# 
#      #   self.kingdomComboBox.blockSignals(False)
# 
# 
#     def updateFromKingdomCBox (self, value):
#         if self.currentEmpire != None :
#             if value in self.model.currentEmpire.kingdoms:
#                 self.currentKingdom = self.model.currentEmpire.kingdoms[value]
#         print ('sss',self.currentEmpire)