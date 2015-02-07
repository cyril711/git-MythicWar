from PyQt5.Qt import  QObject, QFile, qDebug
import xml.etree.ElementTree as ET
from PyQt5 import QtCore
from python_modules.utils import global_helper





class Chapitre (QObject):
    def __init__(self,parent,title,filename=None):
        self.parent=parent
        self.title = title
        self.children = []
        self.content = filename
        self.indice = -1
    def addChild(self,chapter):
        self.children.append(chapter)
    def setContent (self, filename):
        self.content = filename
    def getParent (self):
        return self.parent

class Book (QObject):
    def __init__(self):
        super(Book,self).__init__()
        

    def load (self,filename):
        self.filename = filename
        doc_xml = ET.parse(filename)
        root_node = doc_xml.getroot()
        for node_book in root_node.iter("book"):
            self.root = Chapitre(None,node_book.get('title'),node_book.get('content'))
            break 
        for node in root_node.iter("chapitre_nv1"):
            self.processChapter(self.root,node,1) 
           
    def processChapter(self,parent,node,niveau):

        chapter = Chapitre(parent,node.get('title'),node.get('content'))
        parent.addChild(chapter)
        print ('load book :',node.get('title'))
        niveau +=niveau            
        node_name = "chapitre_nv"+str(niveau)
        for node_chapter in node.iter(node_name) :
                self.processChapter(chapter, node_chapter, niveau)

    def print_(self):
        print (self.root.title,self.root.content)
        for c in self.root.children:
            self.process_print_chapter(c,1)
    def process_print_chapter (self, chapter,level):
        print ('ooo')
        print (str(level),'- ',chapter.title,chapter.content,len(chapter.children),chapter.getParent().title)
        for c in chapter.children:
            self.process_print_chapter ( c,level+1)
            
    def save (self):
        print ('SAVVVEE')
        QtCore.QFile.remove(self.filename)
        book = ET.Element('book',{'title':self.root.title,'content':self.root.content})
        for c in self.root.children:
           # chapterNode = ET.SubElement(book,{'title':c.title,'content':c.content} )
            self.processSave(book,c)
        global_helper.writePrettyXml(book,self.filename)
    def processSave (self,c_node, c_model):
        chapterNode = ET.SubElement(c_node,{'title':c_model.title,'content':c_model.content} )
        for c in c_model.children:
            self.processS ( chapterNode,c)
        