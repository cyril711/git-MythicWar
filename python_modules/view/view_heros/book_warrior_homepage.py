from PyQt5.Qt import QPushButton, QVBoxLayout,QPixmap, QWidget,QSizePolicy, QIcon, QTreeWidgetItem,\
    QTreeView, QModelIndex, QAbstractItemModel, pyqtSignal
from PyQt5 import QtCore
     
from python_modules.view.view_heros.ui_book_warrior_homepage import Ui_BookWarriorHomepage
from python_modules.view.heros_vignette import HerosButton, HerosLabel
from python_modules.config import Config
#basepath = "C:/Users/cyril/Documents/Travail/Workspace/MythicWar/ressources/images/La_Guerre_Mythique"   



class BaseTreeItem(object):
    """
    an item that can be used to populate a tree view, knowing it's place in the model
    """
    def __init__(self, inParentItem):
        """
        Derive specific tree item objects from this guy
        Override the specific methods that the model needs
        @param inParentItem: The parent of a type BaseTreeItem
        """ 
        self.parent = inParentItem
        self.children = []
        
    def addChild(self, inChild):
        """
        @param inChild: The child to add, of a type BaseTreeItem
        """
        self.children.append(inChild)
    
    def getChildCount(self):
        """
        @return: The number of children this item holds
        """
        return len(self.children)
        
    def getChild(self, row):
        """
        @return: The child living at that specific row index (starting from 0)
        """
        return self.children[row]
    
    def getParent(self):
        """
        @return: simply returns the parent for this item, of a type BaseTreeItem
        """
        return self.parent
    
    def columnCount(self):
        """
        @return: The amount of columns this tree item has
        needs to be implemented by derived classes
        """
        raise Exception("Column Count Not Specified!!")
    
    def data(self, inColumn):
        """
        @return: Returns the data to display!
        Needs the be implemented by derived classes
        """
        raise Exception("Data gather method not implemented!")
    

    
    def row(self):
        """
        @return the row this item resides on (int)
        """
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    
   
class RootTreeItem(BaseTreeItem):
    """
    Represents the root of the tree
    """
    
    def __init__(self):
        """
        The root has no parents and no data it needs to retrieve info from
        """
        super(RootTreeItem, self).__init__(None)
        
    def columnCount(self):
        """
        Holds only 1 column
        """    
        return 1
    
    def data(self, inColumn):
        """
        The root doesn't get displayed and for that reason has no meaning
        But because I like providing meaning, i give it a return value
        """
        if inColumn == 0:
            return 'Sommaire'
        return ""
    

        
 
class NodeTreeItem(BaseTreeItem):
    """
    represents a stamp item
    """
    
    def __init__(self, inParent, node):
        """
        Initializes itself with a BaseTreeItem derived object and a stamp
        @param inParent: A Root Tree Item
        @param inStamp:  A Stamp object
        """  
        super(NodeTreeItem, self).__init__(inParent)
        self.node = node
        
    def columnCount(self):
        """
        Holds only 1 column
        """
        return 1
    
    def data(self, inColumn):
        """
        @return: The name of the stamp
        """
        if inColumn == 0:
            return self.node.name
        if inColumn == 1:
            return self.node
        return ""
    


class TreeModel(QAbstractItemModel):                                    
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        
        self.rootItem = RootTreeItem()
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None


        item = index.internalPointer()
        if role != QtCore.Qt.DisplayRole:
            return None
        
        return item.data(index.column())

    def metadata(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
        
        return item.data(1)

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.getChild(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.getParent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.getChildCount()

    def setupModelData(self, data, parent):

        for faction in data.factions.values() :
            factionTreeItem = NodeTreeItem(self.rootItem,faction)
            self.rootItem.addChild(factionTreeItem)
            for empire in faction.empires.values():     
                empireTreeItem = NodeTreeItem(factionTreeItem,empire)
                factionTreeItem.addChild(empireTreeItem)
                for kingdom in empire.kingdoms.values():
                    kingdomTreeItem = NodeTreeItem(empireTreeItem,kingdom)
                    empireTreeItem.addChild(kingdomTreeItem)
                    for groupe in kingdom.groupes.values():
                        groupeTreeItem = NodeTreeItem(kingdomTreeItem,groupe) 
                        kingdomTreeItem.addChild(groupeTreeItem)

class BookWarriorHomepage ( QWidget,Ui_BookWarriorHomepage):
    updateSelection = pyqtSignal()
    def __init__ (self,model,parent=None):
        super(BookWarriorHomepage,self).__init__(parent)
        self.setupUi(self)
        self.max_vignettes = 20
        self.nb_col = 0
        self.nb_row = 0
        self.vignettes_liste = []
        self.model = model
        self.settings = Config().instance.settings
        self.list_warrior = []  # utilise pour maj selection depuis warrrior layout
    def setLeftPage(self):

        self.treeView = QTreeView(self)
        self.treeView.setObjectName("treeView")
        self.left_page_Layout.addWidget(self.treeView)
        self.treeView.activated.connect(self.changeCurrentSet)
        self.tree_model = TreeModel(self.model)
        self.treeView.setModel(self.tree_model)
        self.treeView.setWindowTitle("Simple Tree Model")
        self.treeView.header().hide()
        self.treeView.setAlternatingRowColors(True)
#         i = 0
#         self.treeKingdom.setColumnCount(3)
#         for faction in self.model.factions.values() :
#             item_f = QTreeWidgetItem(self.treeKingdom)
#             #self.treeKingdom.insertTopLevelItem(i,item_f)
#             item_f.setText(i,faction.name)
#             i = i +1
#             for empire in faction.empires.values():
#                 item_e = QTreeWidgetItem()
#                 item_e.setText(i,empire.name)
#                 item_f.addChild(item_e)
#                 for kingdom in empire.kingdoms.values():
#                     item_k = QTreeWidgetItem()
#                     item_k.setText(i,kingdom.name)
#                     item_e.addChild(item_k)
#                     for groupe in kingdom.groupes.values():
#                         item_g = QTreeWidgetItem()
#                         item_g.setText(i,groupe.name)
#                         print ('groupe',groupe.name)
#                         item_k.addChild(item_g)
    
    def setRightContent (self, list_warrior):
        self.list_warrior = list_warrior
        for v in self.vignettes_liste : 
            v.setParent(None)
            self.gridLayout.removeWidget(v)
#         while self.gridLayout.takeAt(0) !=  None :
#             del self.gridLayout.takeAt(0).widget
#             item =  self.gridLayout.takeAt(0)
#             print ('ll')
#             del item
        self.nb_col = 0
        self.nb_row = 0
        self.vignettes_liste = []
        for i in range (min(len(list_warrior),self.max_vignettes)):
            self.addVignette(list_warrior[i],i)

        
    def addVignette (self,warrior,i):
        widget_vignette = QWidget(self.vignettes)        
        layout_one_vignette = QVBoxLayout(widget_vignette)
        layout_one_vignette.setSpacing(0)
        layout_one_vignette.setContentsMargins(0, 0, 0, 0)
        warrior_button = QPushButton(widget_vignette)
        warrior_button.setObjectName(str(i))
        warrior_button.clicked.connect(self.parent().goWarriorPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        warrior_button.setFixedSize(QtCore.QSize(100,120))
        warrior_button.setSizePolicy(sizePolicy)
        layout_one_vignette.addWidget(warrior_button)
        
        # label
        warrior_label = HerosLabel(warrior,widget_vignette)
#         warrior_label.setText(warrior.name)
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(warrior_label.sizePolicy().hasHeightForWidth())
#         warrior_label.setSizePolicy(sizePolicy)
#         warrior_label.setMinimumSize(QtCore.QSize(0, 10))
#         warrior_label.setAlignment(QtCore.Qt.AlignCenter)
        layout_one_vignette.addWidget(warrior_label)
        
        max_col  = 3
        groupe_name = warrior.groupe().name
        if warrior.masterGroupe() != None : 
            groupe_name = warrior.masterGroupe().name+"/"+groupe_name
        
        kingdom_name = warrior.kingdom().name
        empire_name = warrior.empire().name
        faction_name = warrior.faction().name
        icon = QIcon(QPixmap(self.settings.value("global/resources_path")+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+warrior.name+"/portrait_thumbnail.jpg"))

        #print (basepath+"/"+faction_name+"/"+empire_name+"/"+kingdom_name+"/Picture/"+groupe_name+"/"+warrior.name+"/portrait_thumbnail.jpg")
        warrior_button.setIcon(icon)
        warrior_button.setIconSize(QtCore.QSize(100,120))

        if self.nb_col == 0:
            self.nb_row = self.nb_row + 1


        self.gridLayout.addWidget(widget_vignette,self.nb_row,self.nb_col)
        self.vignettes_liste.append(widget_vignette)
        self.nb_col = (self.nb_col +1)%max_col
        
    def changeCurrentSet(self,index):
        print ('changecurrentset:')
        item = self.tree_model.metadata(index, QtCore.Qt.DecorationRole)
        list_warrior = item.getWarriorList()
        self.setRightContent(list_warrior)
        self.updateSelection.emit()