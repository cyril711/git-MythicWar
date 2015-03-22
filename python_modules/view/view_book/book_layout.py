from PyQt5.Qt import QWidget, QTreeView, QAbstractItemModel, QModelIndex, QMenu, \
    QAction, QFileDialog, QIcon
from python_modules.model.book import Chapitre, Book
from python_modules.view.view_book.ui_book_layout import Ui_BookLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from python_modules.view.view_book.page_widget import PageWidget
import math
from python_modules.main_view.book_edit_window import BookEditWindow
from functools import partial
from python_modules.config import Config
import os
import resources_rc
from python_modules.tools.pyhtmleditor.htmleditor import HtmlEditor

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
    

        
 
class ChapterTreeItem(BaseTreeItem):
    """
    represents a stamp item
    """
    
    def __init__(self, inParent, chapter):
        """
        Initializes itself with a BaseTreeItem derived object and a stamp
        @param inParent: A Root Tree Item
        @param inStamp:  A Stamp object
        """  
        super(ChapterTreeItem, self).__init__(inParent)
        self.chapter = chapter
        
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
            return self.chapter.title
        if inColumn == 1:
            return self.chapter.indice
        if inColumn == 2:
            return self.chapter
        if inColumn == 4 : 
            return self.chapter.children
        return ""
    


class TreeModel(QAbstractItemModel):                                    
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        
        self.rootItem = RootTreeItem()
        self.setupModelData(data, self.rootItem)

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction
    
    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()
        if len(item.data(4))==0:
            if role == QtCore.Qt.DecorationRole:
                return QIcon(":/icons/16x16/page")
#         else:
#             if role == QtCore.Qt.DecorationRole:
#                 return QIcon(":/icons/16x16/page")
        
        if role != QtCore.Qt.DisplayRole:
            return None
        
        return item.data(index.column())

    
    def metadata_indice(self, index, role):
        if not index.isValid():
            return None


        item = index.internalPointer()
        
        return item.data(1)

    def metadata_model(self, index, role):
        if not index.isValid():
            return None


        item = index.internalPointer()
        
        return item.data(2)

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

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
        first_item = ChapterTreeItem(self.rootItem, data.root)
        self.rootItem.addChild(first_item)
        for chap in data.root.children:
            chapTreeItem = ChapterTreeItem(first_item, chap)
            self.setupChapitre (chap, chapTreeItem)
            first_item.addChild(chapTreeItem)
    def setupChapitre (self, model_chapitre, tree_chapitre):
        for chap in model_chapitre.children :
            chapTreeItem = ChapterTreeItem(tree_chapitre, chap)
            tree_chapitre.addChild(chapTreeItem)
            self.setupChapitre (chap, chapTreeItem)



class CustomTreeView (QTreeView):
    def __init__(self,parent=None):
        super(CustomTreeView,self).__init__(parent)
    def dropEvent(self,item):
        super(CustomTreeView,self).dropEvent(item)

class BookLayout (QWidget, Ui_BookLayout):
    def __init__ (self,  parent=None):
        super(BookLayout, self).__init__(parent)
        self.setupUi(self)
        self.next.clicked.connect(self.goNext)
        self.previous.clicked.connect(self.goPrevious)
        self.treeView = None
        self.pages_widget = []
        self.model = None

        
    def load (self,model=None):
        if model!=None:
            self.model = model
            self.model.print_()
        if self.treeView != None:
            self.treeView.disconnect()
            self.treeView.setParent(None)
            self.tree_view_layout.removeWidget(self.treeView)
            self.tree_model.disconnect()
            self.tree_model.setParent(None)
        else:
            self.stackedWidget.removeWidget(self.page_3)
            self.stackedWidget.removeWidget(self.page_4)
        for page_widget in self.pages_widget :
            page_widget.setParent(None)
            self.stackedWidget.removeWidget(page_widget)
        self.pages_widget .clear()
        
        
        self.treeView = CustomTreeView(self.tree_view_page)
#         self.treeView.setDragEnabled(True)
#         self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeView.setObjectName("treeView")
        self.tree_view_layout.addWidget(self.treeView)
        self.treeView.setIndentation(10)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.onContextMenu)
        self.treeView.activated.connect(self.changeCurrentPage)
        self.tree_model = TreeModel(self.model)
        self.tree_model.dataChanged.connect(self.updateModel)
        self.treeView.setModel(self.tree_model)
        self.treeView.setWindowTitle("Simple Tree Model")
        self.treeView.header().hide()
        self.treeView.setAlternatingRowColors(True)
        self.contextMenu = QMenu(self.treeView)


        for child in self.model.root.children:
            self.processChapter(child)

        print ('nombre de page :',self.stackedWidget.count())
        if self.stackedWidget.count() >= 1 :
            self.next.setEnabled(True)

#         self.stackedWidget.removeWidget(self.page)
#         self.stackedWidget.removeWidget(self.page_2)
#         self.stackedWidget.addWidget(self.book_homepage)
        self.stackedWidget.setCurrentIndex(0)



    def reload (self):
        print("-----------------")
        self.model.print_()
        if self.treeView != None:
            self.treeView.setParent(None)
            self.tree_view_layout.removeWidget(self.treeView)
        else:
            self.stackedWidget.removeWidget(self.page_3)
            self.stackedWidget.removeWidget(self.page_4)
        for page_widget in self.pages_widget :
            page_widget.setParent(None)
            self.stackedWidget.removeWidget(page_widget)
        self.pages_widget.clear()
        
        
        self.treeView = CustomTreeView(self.tree_view_page)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeView.setObjectName("treeView")
        self.tree_view_layout.addWidget(self.treeView)
        self.treeView.setIndentation(10)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.onContextMenu)
        self.treeView.activated.connect(self.changeCurrentPage)
        self.tree_model = TreeModel(self.model)
        self.tree_model.dataChanged.connect(self.updateModel)
        self.treeView.setModel(self.tree_model)
        self.treeView.setWindowTitle("Simple Tree Model")
        self.treeView.header().hide()
        self.treeView.setAlternatingRowColors(True)
        self.contextMenu = QMenu(self.treeView)
        
#         print ('len(self.model.children())', len(self.model.children()))
 
        for child in self.model.root.children:
            self.processChapter(child)
#
        print ('nombre de page :',self.stackedWidget.count())
        if self.stackedWidget.count() >= 1 :
            self.next.setEnabled(True)

        self.stackedWidget.setCurrentIndex(0)


    def updateModel(self):
        print ('change drag and drop')
        root = self.tree_model.rootItem
        self.model = Book()
        self.model.root = Chapitre(None,root.data(0),root.data(1))
        for child in root.children:
            self.processUpdateModel(self.model.root,child)
            
    def processUpdateModel(self,parent,node):
        print ('processUpdateModel')
        chap = Chapitre(parent,node.data(0),node.data(1))
        parent.addChild(chap)
        for c in node.children:
            self.processUpdateModel(chap,c)
            
            

    def processChapter (self, chapitre):
        if len(chapitre.children) != 0:
            for sub in chapitre.children :
                self.processChapter(sub)
            
        else:
            if chapitre.content != None :
                basepath = Config().instance.settings.value("global/resources_book_path")
                filename= os.path.join(basepath,chapitre.content)
                w_page = PageWidget (filename, self)
                self.stackedWidget.addWidget(w_page)
                self.pages_widget.append(w_page)
                chapitre.indice = self.stackedWidget.count() - 1
            else:
                print ('pppppppppp')

    def onContextMenu(self, point):
        print ('onCOntextMenu')
        index = self.treeView.indexAt(point)
        chapter = self.tree_model.metadata_model(index, QtCore.Qt.EditRole)
        if index.isValid() :
            self.contextMenu.clear()
            action_add = QAction("ajout sous chapitre", self.treeView)
            action_add.triggered.connect(partial(self.onAddChapter, chapter))
            self.contextMenu.addAction(action_add)
            action_add_page = QAction("ajout Page", self.treeView)
            action_add_page.triggered.connect(partial(self.onAddPage, chapter))
            self.contextMenu.addAction(action_add_page)
            action_remove = QAction("remove", self.treeView)
            action_remove.triggered.connect(partial(self.onRemove, chapter))
            self.contextMenu.addAction(action_remove)
            self.contextMenu.exec_(self.treeView.mapToGlobal(point))

    def onAddChapter(self, chapter):
        print ('onAddChapter')
        if chapter.content != None:
            chapitre = chapter.getParent()
        else:
            chapitre = chapter
        test = Chapitre(chapitre, "undefined")
        chapitre.addChild(test)
        self.load()

    def onRemove (self, chapter):
        print ('onRemove')
        if chapter.parent() != None:
            chapter.parent.children.remove(chapter)
            self.load()
    def onAddPage(self, chapter):
        print ('onAddPage')
        filename = QFileDialog.getOpenFileName(self, caption='Choisir le contenu de la page', directory=Config().instance.settings.value("global/resources_book_path"))
        if filename :
            if chapter.content != None:
                chapitre = chapter.getParent()
            else:
                chapitre = chapter
            print ('chapitre partnt',chapitre.title)
            test = Chapitre(chapitre, "undefined", os.path.basename(filename[0]))
            chapitre.addChild(test)
            self.model.print_()
            self.reload()

    def goPrevious (self):
        print ('goPrevious')
        new_index = max(0, self.stackedWidget.currentIndex() - 1)
        self.stackedWidget.setCurrentIndex(new_index)
        if new_index == 0:
            self.previous.setEnabled(False)
        self.next.setEnabled(True)    

    def goNext (self):
        print ('goNext')
        new_index = min(self.stackedWidget.count() - 1, self.stackedWidget.currentIndex() + 1)
        self.stackedWidget.setCurrentIndex(new_index)
        if new_index == (self.stackedWidget.count() - 1):
            self.next.setEnabled(False)        

        self.previous.setEnabled(True)
            
    def onEdit (self):
        print ('onEdit')
        current = None
        for child in self.model.root.children:
            if len(child.children) != 0:
                for sub in child.children :
                    if sub.indice == self.stackedWidget.currentIndex():
                        current = sub
                        break
            else:
                if child.indice == self.stackedWidget.currentIndex():
                    current = child
                    break
        if current != None :    
            textEdit = HtmlEditor(self)#BookEditWindow(self.stackedWidget.currentIndex(),current.content, self)
            textEdit.fileSaved.connect(self.onUpdatePage)
            textEdit.load(os.path.join(Config().instance.settings.value("global/resources_book_path"),current.content))
            #textEdit.setWindowModality(QtCore.Qt.ApplicationModal)
            #textEdit.resize(700, 800)
            textEdit.show()

    
    def onUpdatePage (self):
        print ('onUpdatePage')
        widget = self.stackedWidget.currentWidget()
        ind = self.stackedWidget.currentIndex()
        widget.load()
        self.stackedWidget.setCurrentIndex(ind)
    def changeCurrentPage(self, index):
        print ('changeCurrentPage')
        indice = self.tree_model.metadata_indice(index, QtCore.Qt.DecorationRole)
        self.stackedWidget.setCurrentIndex(indice)
