import os
import json
import jsonpickle
import logging

from typing import Optional

from PySide6.QtCore import QObject, Signal

from jacodemon.model.mapset import MapSet
from jacodemon.model.map import Map

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.wad_service import WadService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.demo_service import DemoService

from jacodemon.service.maps.cache import LoadMapsFromCache, AddMapsToCache

_LAST_JSON = "./last.json"

class MapService(QObject):
    """
    There is a lot of overlap between WadService and MapService. 
    MapService handles caching, and may also add Jacodemon flavour.
    """
    _selected_map_updated = Signal(Map)
    _maps_updated = Signal()
    _last_map_updated = Signal(Map)

    def __init__(self, maps_dir) -> None:
        super().__init__()

        # intrinsics
        self._is_ready = False
        self._logger = logging.getLogger(self.__class__.__name__)

        # services
        self.wad_service: WadService = None
        self.map_set_service: MapSetService = None
        self.stats_service: StatsService = None
        self.demo_service: DemoService = None

        # register events. all must be registered before service initialisation
        Registry.get(EventService).register_signal(Event.SELECTED_MAP_UPDATED, self._selected_map_updated)
        Registry.get(EventService).register_signal(Event.MAPS_UPDATED, self._maps_updated)
        Registry.get(EventService).register_signal(Event.LAST_MAP_UPDATED, self._last_map_updated)

        # data
        self.maps_dir = maps_dir
        self.selected_map = None
        self.last_map = None
        self.maps = []

    def initialise(self):

        if self._is_ready:
            return

        # connect to events
        event_service: EventService = Registry.get(EventService)
        event_service.connect(Event.SELECTED_MAPSET_UPDATED, self.LoadMapsFromMapSet)
        event_service.connect(Event.MAPSETS_UPDATED, self._LoadLastMap)

        self.wad_service = Registry.get(WadService)
        self.map_set_service = Registry.get(MapSetService)
        self.stats_service = Registry.get(StatsService)
        self.demo_service = Registry.get(DemoService)

        self._is_ready = True

    def LoadMapsFromMapSet(self, mapSet: MapSet):

        self.selected_map = None

        if mapSet is None:
            self.maps = []

        # read files in the map set and get map entries
        files = [path.path for path in mapSet.paths if path.enabled]
        self.maps = self.wad_service.GetMapsFromWads(files)

        for map in self.maps:
            map.SetMapSet(mapSet)
            # TODO: do i really need to add stats to maps?
            self.stats_service.AddStatsToMap(map)
            self.demo_service.AddDemoesToMapStats(map)

        self._maps_updated.emit()
    
    def _LoadLastMap(self):

        self.last_map = None

        if os.path.exists(_LAST_JSON):
            with(open(_LAST_JSON)) as f:

                # pickle will only return a decoded instance if a type 
                #   matching the type under "py/object" exists
                pickled = json.load(f)

                try:
                    unpickled = jsonpickle.decode(pickled)
                    unpickled.MapSet = self.map_set_service.GetMapSetById(unpickled.MapSetId)
                    self.last_map = None
                except AttributeError as ae:
                    self._logger.error("Cannot parse last map config. Returning nothing")
                    self._logger.debug(ae)

                self.last_map = unpickled
        else:
            self._logger.warning("Cannot select last map as '{LAST_JSON}' was not found")

        self._last_map_updated.emit(self.last_map)

    def SaveLastMap(self):
        # saves selected map for last

        # TODO: save this into the jacodemon config directory, not local directory
        with open(_LAST_JSON, 'w') as f:
            pickled = jsonpickle.encode(self.selected_map, max_depth=2)
            json.dump(pickled, f)

        self.last_map = self.selected_map

        self._last_map_updated.emit(self.selected_map)

    def SetSelectedMapByIndex(self, mapIndex: int):
        if mapIndex is None:
            self.selected_map = None
        else:
            self.selected_map = self.maps[mapIndex]

        self._selected_map_updated.emit(self.selected_map)

    def SetMapByMapId(self, mapId: str):

        if mapId is None:
            self.selected_map = None
        else:
            for map in self.maps:
                if map.MapId == mapId:
                    self.selected_map = map
                    break

        self._selected_map_updated.emit(self.selected_map)
