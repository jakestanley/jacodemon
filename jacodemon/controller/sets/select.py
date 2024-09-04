import os

from typing import List

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet, MapSetPath

from PySide6.QtWidgets import QInputDialog, QMainWindow

_SINGLETON = None

def EnrichMapSet(ms: MapSet):
    pass

class SelectSetController:
    def __init__(self):
        if _SINGLETON is not None:
            raise Exception("SetController MUST only be instantiated once")
        super().__init__()

    def Add(self, paths) -> MapSet:

        if paths is None or len(paths) == 0:
            return

        name, ext = os.path.splitext(os.path.basename(paths[0]))
        if ext.startswith("."):
            ext = ext[1:]

        # a small bit of ui here isn't toooo bad
        # TODO need to do a directory insert select instead
        name, ok = QInputDialog.getText(None, "Map set name", "Enter a reference for this map set:", text=name)
        if not ok:
            return False

        ms: MapSet = MapSet([MapSetPath(path) for path in paths], name)
        EnrichMapSet(ms)
        GetConfig().AddMapSet(ms)
        return ms

    def Remove(self, ms: MapSet):
        GetConfig().RemoveMapSet(ms)
        # TODO redraw

    def SetMainWindow(self, mainWindow: QMainWindow):
        self._mainWindow = mainWindow

    def Close(self):
        self._mainWindow.close()

def GetSetController():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = SelectSetController()
    return _SINGLETON
