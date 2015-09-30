from PyQt5.Qt import QDialog, QPixmap, QWidget, QColor, QSize, QIcon, QColorDialog, \
    QPushButton, QMenu, QGraphicsDropShadowEffect, QLabel, QFont, QSizePolicy, \
    QTimer, QImage
from PyQt5 import  QtWidgets, QtCore
     
from python_modules.view.view_kingdom.ui_book_world_main_page import Ui_BookWorldMainpage
from python_modules.config import Config
from python_modules.view.heros_vignette import HerosButton, HerosLabel
import os
from python_modules.utils.export_to_sqlite import ExportToSqlite
from python_modules.view.view_kingdom.pie_chart import PieChart
from python_modules.view.base_widget import Title
from python_modules.view.view_kingdom.histo_chart import HistoChart
from python_modules.main_view.dialog_groupe_import import DialogGroupeImport
from python_modules.view.view_kingdom.buttonK import ButtonK




class GroupeButton (ButtonK):
    def __init__ (self, groupe, parent=None):
        super(GroupeButton, self).__init__(groupe,parent)
        self.groupe = self.item

    def onUpdate(self):
        # print ('type sender ',type(self.sender()))
        self.groupe.updateFromDisk()
        self.groupe.model().askForKingdomReload.emit(self.groupe.kingdom().name)
    def onDelete (self):
        print ('on delete')
        self.groupe.kingdom().removeGroupe(self.groupe.name)
        self.groupe.model().askForKingdomReload.emit(self.groupe.kingdom().name)
    def onClicked(self):
        if self.groupe != None :
            print ('goToGroupe', self.groupe.name,type(self.groupe.model()))
            self.groupe.model().askForGroup.emit(self.groupe)
        elif self.text() == "Temple":
            # TO do go and seen temples
            pass
        else:
            # To DO add kingdom
            pass


class BookWorldMainPage (QWidget, Ui_BookWorldMainpage):
    def __init__ (self, model, parent=None):
        super(BookWorldMainPage, self).__init__(parent)
        self.setupUi(self)

        self.kingdom = None
        self.model = model
        self.settings = Config().instance.settings
        self.tabWidget.setCurrentWidget(self.pie_page)
        self.tabWidget.setCurrentIndex(2)

        self.pie = PieChart(self.pie_page, {})
        self.histoWarrior = HistoChart(self.histo_warrior_page)

        self.connections()
        self.pie_layout.addWidget(self.pie)
        self.histo_warrior_layout.addWidget(self.histoWarrior)
    def connections (self):
        self.historyTextEdit.textChanged.connect(self.onModificationKingdom)
        self.descriptionTextEdit.textChanged.connect(self.onModificationKingdom)
        self.button_color.clicked.connect(self.onUpdateColorKingdom)

    def updateContent(self):
        if self.kingdom != None:
            total = {'all':len(self.kingdom.getWarriorList()), 'dead':len(self.kingdom.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(self.kingdom.getWarriorList(lambda x:x.attribs['HP'] > 0))}
            self.pie.setTotal(total)
            data = []
            dataHisto = {}
            for groupe in self.kingdom.groupes.values() :
                if len(groupe.sub_groupes) == 0 : 
                    image = QImage(":/textures/" + groupe.attribs['color'])
                    value = image.pixel(image.width() / 2.0, image.height() / 2.0)
                    data_item = {'color':QColor(value), 'all':len(groupe.getWarriorList()), 'dead':len(groupe.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(groupe.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'label':groupe.name}
                    data.append(data_item)

                 #   dataHisto[groupe] = [len(groupe.getWarriorList()),len(groupe.getWarriorList(lambda x:x.attribs['HP']>0))]
                    total, nb, power = groupe.getAverageRank()
                   # print ('total,nb,power',total/nb,power)
                    try:
                        rank_average = total/nb
                    except ZeroDivisionError:
                        rank_average = 0
                    dataHisto[groupe] = {'warrior':len(groupe.getWarriorList()), 'alive':len(groupe.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'power':power, 'rank':rank_average}

                else: 
                    for sg in groupe.sub_groupes:
                        image = QImage(":/textures/" + sg.attribs['color'])
                        value = image.pixel(image.width() / 2.0, image.height() / 2.0)
                        data_item = {'color':QColor(value), 'all':len(sg.getWarriorList()), 'dead':len(sg.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(sg.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'label':sg.name}
                        data.append(data_item)
                        total, nb, power = sg.getAverageRank()
                        try:
                            rank_average = total/nb
                        except ZeroDivisionError:
                            rank_average = 0
                        dataHisto[sg] = {'warrior':len(sg.getWarriorList()), 'alive':len(sg.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'rank':rank_average, 'power':power}

            self.pie.setData(data)
            self.histoWarrior.setData(dataHisto)
            
            for i in range (self.groupes_bouttons_layout.count()):
                button = self.groupes_bouttons_layout.itemAt(i).widget()
                if (type(button) == GroupeButton):
                    try:
                        groupe_color = button.groupe.attribs['color']

                        button.setStyleSheet("#" + button.objectName() + "{background-image:url(:/textures/" + groupe_color + ");}")            
                    except AttributeError :
                        # dans le cas de la page temple il peut ne pas y avoir de groupe
                        pass


    def onModificationKingdom(self):
        self.parent().parent().modifiedKingdom.emit(self.kingdom)        
        
    def onUpdateColorKingdom (self):
        dlg = QColorDialog(self.kingdom.color)
        dlg.setOption(QColorDialog.ShowAlphaChannel, True)
        if dlg.exec_() == QDialog.Accepted:
            self.kingdom.color = dlg.currentColor()
            self.setStyleSheet("QLineEdit,QFrame{ border: 1px solid rgb(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + ");background-color: rgba(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + "," + str(self.kingdom.color.alpha()) + ");}")
            
            # self.setStyleSheet("QPlainTextEdit{ background-color: rgba("+str(self.kingdom.color.red())+","+str(self.kingdom.color.green())+","+str(self.kingdom.color.blue())+","+str(self.kingdom.color.alpha())+");}")
            self.button_color.setStyleSheet("#button_color{background-color: rgba(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + "," + str(self.kingdom.color.alpha()) + ");}")
            self.button_color.show()
        else:
            dlg.close()
    def setContent (self, kingdom=None):
        if kingdom != None:
            self.kingdom = kingdom
        self.setContentLeftPage()
        self.setContentRightPage()


    def setContentLeftPage (self):
        # self.setStyleSheet("QPlainTextEdit{ border: 2px solid rgb("+str(kingdom.color.red())+","+str(kingdom.color.green())+","+str(kingdom.color.blue())+";)}")
        self.setStyleSheet("QLineEdit,QFrame{ border: 1px solid rgb(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + ";)}")

        self.Title.setText(self.kingdom.name)
#         self.Title.setObjectName("toto")
        self.Title.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + "))");
        self.historyTextEdit.appendPlainText(self.kingdom.attribs['armee'])
        self.descriptionTextEdit.appendPlainText(self.kingdom.attribs['description'])
        [total, complete, alive] = self.kingdom.avancement ()
        self.button_color.setText(str(alive) + " / " + str(total))
        pct = alive / total
        
        if pct > 0.5 :
            c = "green"
        elif pct > 0.25 :
            c = "orange"
        else : 
            c = "red"
        self.button_color.setStyleSheet("#button_color{color:" + c + ";background-color: rgba(" + str(self.kingdom.color.red()) + "," + str(self.kingdom.color.green()) + "," + str(self.kingdom.color.blue()) + "," + str(self.kingdom.color.alpha()) + ");}")

        try:
            percent = float(complete / total) * 100
        except (ZeroDivisionError, KeyError) :
            percent = 0

        if percent >= 50 :
            c = "green"
        elif percent >= 25:
            c = "orange"
        else : 
            c = "red"
        self.progressBar.setStyleSheet("  QProgressBar {border-radius: 5px;} QProgressBar::chunk {     background-color: " + c + ";width: 20px;}")
        # self.ui.progressBar_life.setAlignment(QtCore.Qt.AlignCenter)

        self.progressBar.setValue(int(percent)) 




    def setContentRightPage(self):
        faction_name = self.kingdom.parent.parent.name
        empire_name = self.kingdom.parent.name
        # taille = min(self.army_page.size().width(),self.army_page.size().height())
        # self.land_picture.setScaledContents(True)
        # self.land_picture.setPixmap(QPixmap(os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,self.kingdom.name,"Land.jpg")))
        # self.army_picture.setPixmap(QPixmap(os.path.join(Config().instance.path_to_pic(),faction_name,empire_name,self.kingdom.name,"Army.png")))        
       # self.army_picture.setScaledContents(True)


        pos = 0
        row = -1
        ind = 0
        total = {'all':len(self.kingdom.getWarriorList()), 'dead':len(self.kingdom.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(self.kingdom.getWarriorList(lambda x:x.attribs['HP'] > 0))}
        self.pie.setTotal(total)
        data = []
        
        nb_col = 3

        while (self.groupes_bouttons_layout.count() > 0):
            b = self.groupes_bouttons_layout.itemAt(0).widget()
            b.setParent(None)
            self.groupes_bouttons_layout(b)

        for groupe in self.kingdom.groupes.values() :
            groupe_color = groupe.attribs['color']
            ind += 1
            if len(groupe.sub_groupes) == 0 : 

                button = GroupeButton(groupe, self.groupes_buttons)
                #button.setText(groupe.name.replace("_", " "))
                sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setSizePolicy(sp)
                # menu = self.createMenuForButton(groupe.name)
                # button.setMenu(menu)
                button.setObjectName("button_0_" + str(ind))

                if pos == 0 :
                    row += 1
    
                self.groupes_bouttons_layout.addWidget(button, row, pos)
                button.setStyleSheet("#" + button.objectName() + "{background-image:url(:/textures/" + groupe_color + ");}")            
                # self.groupes_bouttons_layout.addWidget(button,row,pos)   
                pos = (pos + 1) % nb_col        
                data_item = {'color':QColor(255, 0, 0), 'all':len(groupe.getWarriorList()), 'dead':len(groupe.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(groupe.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'label':groupe.name}
                data.append(data_item)
        
            else: 
                for sg in groupe.sub_groupes:
                    # menu = self.createMenuForButton(sg.name)
                    button = GroupeButton(sg, self.groupes_buttons)
                    button.setText(groupe.name + " / " + sg.name)
                    button.setObjectName("button_1_" + str(ind))                    
                    # button.setMenu(menu)
                    sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setSizePolicy(sp)
                    if pos == 0 :
                        row += 1
        
                    self.groupes_bouttons_layout.addWidget(button, row, pos)
                    button.setStyleSheet("#" + button.objectName() + "{background-image:url(:/textures/" + groupe_color + ");}")            
                    # self.groupes_bouttons_layout.addWidget(button,row,pos)
                    data_item = {'color':QColor(255, 0, 0), 'all':len(sg.getWarriorList()), 'dead':len(sg.getWarriorList(lambda x:x.attribs['HP'] <= 0)), 'alive':len(sg.getWarriorList(lambda x:x.attribs['HP'] > 0)), 'label':sg.name}
                    data.append(data_item)
                    pos = (pos + 1) % nb_col
        self.pie.setData(data)


        # boutton speciaux
        button = GroupeButton(None,self.groupes_buttons)
        button.setText("Temples")
        button.groupe = None
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setSizePolicy(sp)
        button.setObjectName("button_temple")
        if pos == 0 :
            row += 1
        self.groupes_bouttons_layout.addWidget(button, row, pos)   
        pos = (pos + 1) % nb_col

        self.button_add = QPushButton(self.groupes_buttons)
        self.button_add.setText("add Groupe....")
        self.button_add.clicked.connect(self.onNewGroupe)
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_add.setSizePolicy(sp)
        self.button_add.setObjectName("button_add")
        if pos == 0 :
            row += 1
        self.groupes_bouttons_layout.addWidget(self.button_add, row, pos)   


    def onNewGroupe (self):
        dlg = DialogGroupeImport(os.path.join(Config().instance.path_to_pic(), self.kingdom.faction().name, self.kingdom.empire().name, self.kingdom.name, "Picture"), self)
        if dlg.exec_() == QDialog.Accepted :

            defaults_values = dlg.validate()
            print (defaults_values)
            self.kingdom.createGroupe(dlg.groupeName(), defaults_values)
            self.kingdom.model().askForKingdomReload.emit(self.kingdom.name)
        else :
            dlg.close()
            
        
    def setEnableEditableItems (self, enable):
        self.historyTextEdit.setEnabled(enable)
        self.descriptionTextEdit.setEnabled(enable)
        self.comboBoxColor.setEnabled(enable)
    
