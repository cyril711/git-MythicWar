from PyQt5.Qt import QSettings


class Config:
    class __Config:
        def __init__(self, filename):
            self.settings = QSettings(filename,QSettings.IniFormat)
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg=None):
        if not Config.instance:
            Config.instance = Config.__Config(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)