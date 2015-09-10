from PyQt5.Qt import QSettings
import os

class Config:
    class __Config:
        def __init__(self, filename):
            self.settings = QSettings(filename,QSettings.IniFormat)
        def __str__(self):
            return repr(self) + self.val
        def basepath (self):
            return self.settings.value("global/resources_path")
        def path_to_pic(self):
            return os.path.join(self.settings.value("global/resources_path"),self.settings.value("global/resources_pic"))
        def path_to_qss(self):
            return os.path.join(self.settings.value("global/resources_path"),self.settings.value("global/resources_qss"))
        def path_to_book(self):
            return os.path.join(self.settings.value("global/resources_path"),self.settings.value("global/resources_book"))
        def path_to_texture(self):
            return os.path.join(self.settings.value("global/resources_path"),self.settings.value("global/resources_texture"))
        def path_to_icons(self):
            return os.path.join(self.settings.value("global/resources_path"),self.settings.value("global/resources_icons"))

        def model_database (self):
            return os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/default_database"))
        def current_database (self):
            return os.path.join(self.settings.value("global/current_dir"),self.settings.value("global/current_database"))        
    
    instance = None
    def __init__(self, arg=None):
        if not Config.instance:
            Config.instance = Config.__Config(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
    
