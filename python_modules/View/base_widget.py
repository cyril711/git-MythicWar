from PyQt5.Qt import QLabel, QFont
from PyQt5 import QtCore
class Title (QLabel):
    def __init__ (self,parent=None):
        super(Title,self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        font = QFont()
        #font.setFamily("Nyala")
        font.setFamily("Old English Text MT")
        font.setPointSize(24)
        self.setFont(font)
    def paintEvent(self, event):
        super(Title,self).paintEvent(event)
        pass