import os

from typing import List

from jacodemon.model.config import JacodemonConfig, GetConfig
from jacodemon.model.mapset import MapSet, MapSetPath

from jacodemon.wads.wad import GetMapEntriesFromFiles
from jacodemon.wads.wad import GetInfoFromFiles

from PySide6.QtWidgets import QInputDialog, QMainWindow

_SINGLETON = None

class SelectSetController:
    def __init__(self):
        if _SINGLETON is not None:
            raise Exception("SetController MUST only be instantiated once")
        super().__init__()

    def Add(self, paths) -> MapSet:

        if paths is None or len(paths) == 0:
            return

        title, ext = os.path.splitext(os.path.basename(paths[0]))
        if ext.startswith("."):
            ext = ext[1:]

        # a small bit of ui here isn't toooo bad
        gameinfo = GetInfoFromFiles(paths)
        if "Title" in gameinfo and gameinfo["Title"] is not None:
            title = gameinfo["Title"]

        title, ok = QInputDialog.getText(None, "Map set name", "Enter a reference for this map set:", text=title)
        if not ok:
            return False
        
        ms: MapSet = MapSet(
            paths=[MapSetPath(path) for path in paths], 
            name=title,
            iwad= gameinfo.get("IWAD"),
            compLevel=gameinfo.get("complevel")
        )

        GetConfig().AddMapSet(ms)
        return ms

    def Remove(self, ms: MapSet):
        GetConfig().RemoveMapSet(ms)

    def SetMainWindow(self, mainWindow: QMainWindow):
        self._mainWindow = mainWindow

    def Close(self):
        self._mainWindow.close()

def GetSetController():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = SelectSetController()
    return _SINGLETON

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ms: MapSet = GetSetController().Add(["tests/data/thirdparty/eviternity2.wad"])
    sys.exit(0)
