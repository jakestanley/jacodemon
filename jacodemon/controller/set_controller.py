import os

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from PySide6.QtWidgets import QInputDialog

_SINGLETON = None

class SetController:
    def __init__(self):
        if _SINGLETON is not None:
            raise Exception("SetController MUST only be instantiated once")
        super().__init__()

    def Add(self, paths) -> MapSet:

        name, ext = os.path.splitext(os.path.basename(paths[0]))
        if ext.startswith("."):
            ext = ext[1:]

        # a small bit of ui here isn't toooo bad
        # TODO need to do a directory insert select instead
        name, ok = QInputDialog.getText(None, "Map set name", "Enter a reference for this map set:", text=name)
        if not ok:
            return False

        ms: MapSet = MapSet(paths, name)
        GetConfig().AddMapSet(ms)

        GetConfig().Save()
        return ms

def GetSetController():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = SetController()
    return _SINGLETON
