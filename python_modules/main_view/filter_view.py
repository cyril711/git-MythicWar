from PyQt5.Qt import QDialog, QStandardItem, QStandardItemModel, QWidget,\
    QComboBox, QListView, QTableView, QVBoxLayout
from PyQt5 import QtCore

class FilterView (QDialog):
    def init(self,univers,parent):
        super (FilterView).__init(parent)
        self.initialise(univers)
    
    
    def initialise (self, univers):
        model = QStandardItemModel (3,1)
    
        i = 0
        for faction in univers.faction_list :
            item = QStandardItem(faction.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled);
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole);

            model.setItem(i, 0, item)
            i = i + 1

        combo = QComboBox()
        combo.setModel(model)

        list_v = QListView()
        list_v.setModel(model)

        table = QTableView()
        table.setModel(model)

        container = QWidget()
        containerLayout = QVBoxLayout()
        container.setLayout(containerLayout)
        containerLayout.addWidget(combo)
        containerLayout.addWidget(list_v)
        containerLayout.addWidget(table)