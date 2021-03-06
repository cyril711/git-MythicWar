from PyQt5.Qt import QTextEdit, QFile, QTextCodec
from PyQt5 import QtCore
from python_modules.config import Config
import os


class PageWidget (QTextEdit):
    def __init__(self, filename, parent=None):
        super(PageWidget, self).__init__(parent)

        self.filename= filename#os.path.join(basepath,filename)
        print ('filename',self.filename)
        self.load()
        
        
    def load(self):
        if not QFile.exists(self.filename):
            print ('-------file not exist : ',self.filename)
            return None

        fh = QFile(self.filename)
        if not fh.open(QFile.ReadOnly):
            print ('echec ouverture fichier')
            return None
    
        data = fh.readAll()
    
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)
        if QtCore.Qt.mightBeRichText(unistr):
            self.setHtml(unistr)
        else:
            self.setPlainText(unistr)
