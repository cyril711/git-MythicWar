from PyQt5.Qt import QSettings
import os
from python_modules.model.univers import Univers

class SuperModel:
    class __SuperModel:
        def __init__(self, database,progressBar):
            self.univers = Univers(database,progressBar)
        def __str__(self):
            return repr(self) + self.val
    
    instance = None
    def __init__(self, database,progressBar):
        if not SuperModel.instance:
            SuperModel.instance = SuperModel.__Config(database,progressBar)

    def __getattr__(self, name):
        return getattr(self.instance, name)
    
