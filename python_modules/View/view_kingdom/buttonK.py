from PyQt5.Qt import QPushButton, QMenu, QIcon, QPixmap
from PyQt5 import QtWidgets


class ButtonK (QPushButton):
    def __init__ (self, item, parent=None):
        super(ButtonK, self).__init__(parent)
        print('buttonKKKK',type(item),type(parent))
        self.item = item
        if item != None :
            self.setText(item.name.replace("_", " "))
        self.clicked.connect(self.onClicked)
    def contextMenuEvent(self, event):
        if self.item != None:
            menu = QMenu(self.parent())
            self.actionUpdate = QtWidgets.QAction(self.parent())
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/16x16/update"), QIcon.Normal, QIcon.Off)
            self.actionUpdate.setIcon(icon)
            self.actionUpdate.setObjectName(self.item.name)
            self.actionUpdate.setText("Update")
            self.actionUpdate.triggered.connect(self.onUpdate)
            menu.addAction(self.actionUpdate)
            self.actionDelete = QtWidgets.QAction(self.parent())
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/16x16/delete"), QIcon.Normal, QIcon.Off)
            self.actionDelete.setIcon(icon)
            self.actionDelete.setObjectName(self.item.name)
            self.actionDelete.setText("Supprimer")
            self.actionDelete.triggered.connect(self.onDelete)
            menu.addAction(self.actionDelete)
            menu.exec_(self.mapToGlobal(event.pos()))
    def onGUpdate(self):
        pass
    def onDelete (self):
        pass
    def onClicked(self):
        pass