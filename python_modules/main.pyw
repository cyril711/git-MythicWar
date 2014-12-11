from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog)
from python_modules.Model.univers import Univers
from python_modules.View.main_window import MainWindow
import sys
from python_modules.utils.resourceLoader import ResourceLoader
from python_modules.utils.thumbnail_generator import ThumbnailGenerator
from PyQt5.Qt import QSettings
from python_modules.resources_rc import *
from python_modules.config import Config
if __name__ == '__main__':



    app = QApplication(sys.argv)
    settings = Config("config.ini")
#      settings.setValue("all",{"kingdom":0,"empire":1})
#      settings.endGroup()

#     rl = ResourceLoader("../ressources/images/La_Guerre_Mythique")
#     rl.kingdomLoader("Lumiere", "Grec", "Artemis")
    #tg = ThumbnailGenerator("../ressources/images/La_Guerre_Mythique")
    #tg.generateFor1Kingdom("Lumiere", "Grec", "Artemis")
    #rl.finish()
    filename = ""
    univers = Univers(filename)
    mainWin = MainWindow(univers)
    mainWin.show()
    mainWin.showMaximized()
    sys.exit(app.exec_())