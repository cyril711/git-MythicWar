from PyQt5.QtWidgets import QApplication
from python_modules.model.univers import Univers
from python_modules.main_view.main_window import MainWindow
import sys
from python_modules.utils.resourceLoader import ResourceLoader
from python_modules.utils.thumbnail_generator import ThumbnailGenerator
from python_modules.resources_rc import *
from python_modules.config import Config
if __name__ == '__main__':



    app = QApplication(sys.argv)
    settings = Config("config.ini")

#      settings.setValue("all",{"kingdom":0,"empire":1})
#      settings.endGroup()

#     rl = ResourceLoader("../ressources/images/La_Guerre_Mythique")
#     rl.kingdomLoader("Lumiere", "Grec", "Artemis")

    #rl.finish()
    filename = ""

    mainWin = MainWindow()
    mainWin.show()
    mainWin.showMaximized()
    sys.exit(app.exec_())