import os

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QInputDialog

from jacodemon.misc.files import FindDoomFiles

from jacodemon.model.config import JacodemonConfig
from jacodemon.model.mapset import MapSetPath, MapSet

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.wad_service import WadService

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
class MapSetService(QObject):

    _selected_mapset_updated = Signal(MapSet)
    _mapsets_updated = Signal()

    def __init__(self, configuration: JacodemonConfig):
        super().__init__()

        self.is_ready = False
        self.maps_dir = configuration.maps_dir
        self.wad_service: WadService = None

        self.configuration = configuration
        self.selected_map_set = None

        # register events. all must be registered before service initialisation
        Registry.get(EventService).register_signal(Event.SELECTED_MAPSET_UPDATED, self._selected_mapset_updated)
        Registry.get(EventService).register_signal(Event.MAPSETS_UPDATED, self._mapsets_updated)

    def initialise(self):

        if self.is_ready:
            return

        from jacodemon.service.registry import Registry

        # connect to signals
        event_service = Registry.get(EventService)
        self.wad_service = Registry.get(WadService)

        self.mapSets = [_LoadMapSet(ms) for ms in self.configuration.sets]

        self._mapsets_updated.emit()

        self.is_ready = True
    
    def TouchMapSet(self, mapSet):
        self.mapSets.remove(mapSet)
        self.mapSets.append(mapSet)
        self.configuration.UpdateMapSets(self.mapSets)
    
    def GetMapSetById(self, mapSetId: str) -> MapSet:
        return next((ms for ms in self.mapSets if ms.id.lower() == self.last_map.MapSetId), None)

    def CreateMapSet(self):

        paths = FindDoomFiles(self.maps_dir)

        if paths is None or len(paths) == 0:
            return

        title, ext = os.path.splitext(os.path.basename(paths[0]))
        if ext.startswith("."):
            ext = ext[1:]

        # a small bit of ui here isn't toooo bad
        title, ok = QInputDialog.getText(None, "Map set name", "Enter a reference for this map set:", text=title)
        if not ok:
            return False
        
        wadsData = self.wad_service.GetDataFromWads(paths)
        iwad = wadsData.iwad if wadsData.iwad else None
        compLevel = wadsData.complevel if wadsData.complevel else None

        mapSet = MapSet(
            paths=[MapSetPath(path) for path in paths], 
            name=title,
            iwad= iwad,
            compLevel=compLevel
        )

        self.mapSets.append(mapSet)

        self.configuration.UpdateMapSets(self.mapSets)

        self._mapsets_updated.emit()

    def RemoveMapSetById(self, mapSetId: str):

        if self.selected_map_set and self.selected_map_set.id == mapSetId:
            self.selected_map_set = None

        for set in self.mapSets:
            if str(set.id) == mapSetId:
                self.mapSets.remove(set)

        if self.selected_map_set and self.selected_map_set.id == mapSetId:
            self.selected_map_set = None

        self.configuration.UpdateMapSets(self.mapSets)

        # TODO: think more about firing two events one after the other for unintended behaviour
        # self.selected_mapset_updated.emit()
        self._mapsets_updated.emit()

    def SetMapSet(self, mapSetId: str):

        # don't do anything if mapset hasn't changed
        if self.selected_map_set is not None and self.selected_map_set.id == mapSetId:
            return

        for mapSet in self.mapSets:
            if mapSet.id == mapSetId:
                self.selected_map_set = mapSet
                wads_data = self.wad_service.GetDataFromWads([p.path for p in self.selected_map_set.paths])
                self.selected_map_set.text = wads_data.text
                # TODO more with wads_data
                break

        # TODO fix that map sets are in many places, here, map set service and jacodemon config
        self.TouchMapSet(self.selected_map_set)

        self._selected_mapset_updated.emit(self.selected_map_set)
