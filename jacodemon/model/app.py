from typing import List
from PySide6.QtCore import QObject, Signal

from jacodemon.model.map import Map

# TODO consider last map service? :D
# TODO move this into map service?
from jacodemon.last import GetLastMap
from jacodemon.model.mod import Mod
from jacodemon.service.config_service import ConfigService
from jacodemon.service.map_service import MapService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.demo_service import DemoService

# TODO move Options into model?
from jacodemon.options import Options
from jacodemon.service.options_service import OptionsService

from jacodemon.options import MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

class AppModel(QObject):

    mods_updated = Signal()
    maps_updated = Signal()

    # map changes, we must update demos, stats, etc on map select view.
    selected_map_updated = Signal()

    # mapset changes, we must update map select view
    selected_mapset_updated = Signal()

    # used for when we add, remove, edit, touch map sets
    mapsets_updated = Signal()

    # most generic signal that isn't covered by the others
    config_updated = Signal()
    
    def __init__(self, config_service: ConfigService, map_set_service: MapSetService, 
                 map_service: MapService, stats_service: StatsService, 
                 demo_service: DemoService, options_service: OptionsService):
        super().__init__()

        self.config_service = config_service
        self.map_set_service = map_set_service
        self.map_service = map_service
        self.stats_service = stats_service
        self.demo_service = demo_service
        self.options_service = options_service

        self.config = self.config_service.config
        self.options: Options = self.options_service.GetOptions()

        # map sets (CONSIDER: do we want to load map sets in the constructor?)
        self.mapSets = self.map_set_service.LoadMapSets(self.config.sets)
        self.selected_map_set = None

        # maps
        self.maps = []
        self.selected_map = None

        # demoes
        self.demoes = []
        self.selected_demo = None

    def update(self):
        self.mods_updated.emit()
        self.maps_updated.emit()
        self.selected_map_updated.emit()
        self.selected_mapset_updated.emit()
        self.mapsets_updated.emit()
        self.config_updated.emit()

    # attempting to abstract away JacodemonConfig
    def GetDemoDir(self):
        return self.config.demo_dir
    
    def SetDemoDir(self, dir):
        self.config.demo_dir = dir
        self.config_updated.emit()
    
    def GetIwadDir(self):
        return self.config.iwad_dir
    
    def SetIwadDir(self, dir):
        self.config.iwad_dir = dir
        self.config_updated.emit()
    
    def GetMapsDir(self):
        return self.config.maps_dir
    
    def SetMapsDir(self, dir):
        self.config.map_dir = dir
        self.config_updated.emit()
    
    def GetModsDir(self):
        return self.config.mods_dir
    
    def SetModsDir(self, dir):
        self.config.mods_dir = dir
        self.config_updated.emit()
    
    def GetDefaultCompLevel(self):
        return self.config.default_complevel

    # TODO where does the save go? :D
    def SetDefaultCompLevel(self, level):
        self.config.default_complevel = level
        self.config_updated.emit()

    def GetMods(self) -> List[Mod]:
        mods = [Mod.from_dict(mod) for mod in self.config.mods]
        return mods

    def IsRecordDemoEnabled(self) -> bool:
        return self.options.record_demo and not self.options.mode == MODE_REPLAY
    
    def CanRecordDemo(self) -> bool:
        return self.options.mode != MODE_REPLAY
    
    def IsAutoRecordEnabled(self) -> bool:
        return self.options.auto_record and self.options.obs
    
    def CanAutoRecord(self) -> bool:
        return self.options.obs
    
    def IsModsEnabled(self) -> bool:
        return self.options.mods
    
    def IsMusicEnabled(self) -> bool:
        return self.options.music
    
    def IsObsEnabled(self) -> bool:
        return self.options.obs
    
    def GetMode(self) -> int:
        return self.options.mode
    
    def GetLastMap(self) -> Map:
        return GetLastMap()
    
    def _TouchMapSet(self, mapSet):
        self.mapSets.remove(mapSet)
        self.mapSets.append(mapSet)

    def _LoadDemoes(self):
        self.demo_service
        pass

    def SetMap(self, index):
        
        # TODO bounds check
        self.selected_map = self.maps[index]
        self.selected_map_updated.emit()

    def SetMapSet(self, mapSetId):

        # don't do anything if mapset hasn't changed
        if self.selected_map_set is not None and self.selected_map_set.id == mapSetId:
            return
        
        # clear the selected map
        self.selected_map = None

        for mapSet in self.mapSets:
            if mapSet.id == mapSetId:
                self.selected_map_set = mapSet
                break

        self._TouchMapSet(mapSet)

        self.maps = self.map_service.LoadMaps(mapSet)
        for map in self.maps:
            map.MapSet = mapSet
            self.stats_service.AddStatsToMap(map)
            self.demo_service.AddDemoesToMapStats(map)

        self.selected_map_updated.emit()
        self.selected_mapset_updated.emit()

def InitialiseAppModel():
    """Pretty please don't call this more than once. Used for initial setup 
    and individual components testing"""

    config_service = ConfigService()
    map_set_service = MapSetService()
    map_service = MapService(config_service.config.maps_dir)
    stats_service = StatsService(config_service.config.stats_dir)
    demo_service = DemoService(config_service.config.demo_dir)
    options_service = OptionsService()

    # model, view, controller setup
    return AppModel(
        config_service=config_service, 
        map_set_service=map_set_service,
        map_service=map_service,
        stats_service=stats_service,
        demo_service=demo_service,
        options_service=options_service)
