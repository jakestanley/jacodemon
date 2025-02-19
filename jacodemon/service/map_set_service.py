import os

from PySide6.QtWidgets import QInputDialog

from jacodemon.misc.files import FindDoomFiles

from jacodemon.model.config import JacodemonConfig
from jacodemon.model.mapset import MapSetPath, MapSet

def _LoadMapSet(dict) -> MapSet:
    paths = []
    for path in dict["paths"]:
        paths.append(MapSetPath(path["path"], path["enabled"]))

    return MapSet(paths=paths, 
                  name=dict["name"], 
                  id=dict.get("id"), 
                  iwad=dict.get("iwad"), 
                  compLevel=dict.get("compLevel"))

# TODO CONSIDER: should this output the mapsets updated signal instead of AppModel?
class MapSetService:

    def __init__(self, configuration: JacodemonConfig):
        self.maps_dir = configuration.maps_dir
        self.configuration = configuration
        self.mapSets = [_LoadMapSet(ms) for ms in self.configuration.sets]
    
    def TouchMapSet(self, mapSet):
        self.mapSets.remove(mapSet)
        self.mapSets.append(mapSet)
        self.configuration.UpdateMapSets(self.mapSets)
    
    def CreateMapSet(self):

        paths = FindDoomFiles(self.maps_dir)

        if paths is None or len(paths) == 0:
            return

        title, ext = os.path.splitext(os.path.basename(paths[0]))
        if ext.startswith("."):
            ext = ext[1:]

        # TODO use wad service to populate this
        gameinfo = {}
        # gameinfo = GetInfoFromFiles(paths)
        # if "Title" in gameinfo and gameinfo["Title"] is not None:
        #     title = gameinfo["Title"]

        # a small bit of ui here isn't toooo bad
        title, ok = QInputDialog.getText(None, "Map set name", "Enter a reference for this map set:", text=title)
        if not ok:
            return False
        
        mapSet = MapSet(
            paths=[MapSetPath(path) for path in paths], 
            name=title,
            iwad= gameinfo.get("IWAD", "DOOM2.WAD"),
            compLevel=gameinfo.get("complevel", None)
        )

        self.mapSets.append(mapSet)

        self.configuration.UpdateMapSets(self.mapSets)

    def RemoveMapSet(self, mapset: MapSet):
        for set in self.mapSets:
            if set.id == mapset.id:
                self.mapSets.remove(set)

        self.configuration.UpdateMapSets(self.mapSets)
