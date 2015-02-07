from PyQt5.Qt import QAbstractItemModel, QModelIndex, QWidget, QTreeView
from python_modules.view.view_book.ui_book_homepage import Ui_BookHomepage
from PyQt5 import QtCore





class BookTreeView (QTreeView):
    def __init__(self,parent):
        super(BookTreeView,self).__init__(parent)

        

class BookHomepage (QWidget,Ui_BookHomepage):
    def __init__(self,model_book,parent=None):
        super(BookHomepage ,self).__init__(parent)
        self.setupUi(self)

        self.treeView = BookTreeView(self.left_page)
        self.treeView.setObjectName("treeView")
        self.left_page_layout.addWidget(self.treeView)

        self.tree_model = TreeModel(model_book)
        self.treeView.setModel(self.tree_model)
        self.treeView.setWindowTitle("Simple Tree Model")
        self.treeView.setAlternatingRowColors(True)
