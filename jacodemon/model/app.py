from typing import List
from PySide6.QtCore import QObject, Signal

from jacodemon.model.options import Options
from jacodemon.model.launch import LaunchMode, LaunchSpec, LaunchSession
from jacodemon.model.mod import Mod

from jacodemon.service.config_service import ConfigService
from jacodemon.service.map_service import MapService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.obs.mock_obs_service import MockObsService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.demo_service import DemoService
from jacodemon.service.launch.launch_service import LaunchService
from jacodemon.service.obs_service import ObsService

from jacodemon.service.options_service import OptionsService

from jacodemon.model.options import MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

class AppModel(QObject):

    mods_updated = Signal()
    maps_updated = Signal()

    # map changes, we must update demos, stats, etc on map select view.
    selected_map_updated = Signal()

    # mapset changes, we must update map select view
    selected_mapset_updated = Signal()

    # when a user selects stats from the list
    selected_statistics_updated = Signal()

    # used for when we add, remove, edit, touch map sets
    mapsets_updated = Signal()

    # used for when we switch to prelaunch
    mode_changed = Signal()
    
    def __init__(self, config_service: ConfigService, map_set_service: MapSetService, 
                 map_service: MapService, stats_service: StatsService, 
                 demo_service: DemoService, launch_service: LaunchService,
                 options_service: OptionsService, obs_service: ObsService):
        super().__init__()

        self.config_service = config_service
        self.map_set_service = map_set_service
        self.map_service = map_service
        self.stats_service = stats_service
        self.demo_service = demo_service
        self.launch_service = launch_service
        self.options_service = options_service
        self.obs_service = obs_service

        self.config = self.config_service.config
        self.options: Options = self.options_service.GetOptions()

        # map sets (CONSIDER: do we want to load map sets in the constructor?)
        self.selected_map_set = None

        # maps
        self.maps = []
        self.selected_map = None
        self.last_map = map_service.LoadLastMap()
        if self.last_map is not None:
            self.last_map.MapSet = next((ms for ms in self.map_set_service.mapSets if ms.id.lower() == self.last_map.MapSetId), None)
        
        if self.last_map and self.last_map.MapSet is None:
            self.last_map = None

        # statistics
        self.selected_statistics = None

    def update(self):
        self.mods_updated.emit()
        self.maps_updated.emit()
        self.selected_map_updated.emit()
        self.selected_mapset_updated.emit()
        self.mapsets_updated.emit()

    # attempting to abstract away JacodemonConfig
    def GetDemoDir(self):
        return self.config.demo_dir
    
    def SetDemoDir(self, dir):
        self.config.demo_dir = dir
        self.config.Save()
    
    def GetIwadDir(self):
        return self.config.iwad_dir
    
    def SetIwadDir(self, dir):
        self.config.iwad_dir = dir
        self.config.Save()
    
    def GetMapsDir(self):
        return self.config.maps_dir
    
    def SetMapsDir(self, dir):
        self.config.maps_dir = dir
        self.config.Save()
    
    def GetModsDir(self):
        return self.config.mods_dir
    
    def SetModsDir(self, dir):
        self.config.mods_dir = dir
        self.config.Save()
    
    def GetDefaultCompLevel(self):
        return self.config.default_complevel

    def SetDefaultCompLevel(self, level):
        self.config.default_complevel = level
        self.config.Save()

    def GetDefaultSkillLevel(self):
        return self.config.skill
    
    def SetDefaultSkillLevel(self, skill):
        self.config.skill = skill
        self.config.Save()

    def GetMods(self) -> List[Mod]:
        return [Mod.from_dict(mod) for mod in self.config.mods]
    
    def SetMods(self, mods: List[Mod]):
        self.config.mods = [mod.to_dict() for mod in mods]
        self.config.Save()
        self.mods_updated.emit()

    def IsRecordDemoEnabled(self) -> bool:
        return self.options.mode == LaunchMode.RECORD_DEMO
    
    def IsAutoRecordEnabled(self) -> bool:
        return self.options.auto_record and self.options.obs
    
    def IsObsAvailable(self) -> bool:
        return self.options.obs
    
    def IsModsEnabled(self) -> bool:
        return self.options.mods
    
    def IsMusicEnabled(self) -> bool:
        return self.options.music
    
    def IsObsEnabled(self) -> bool:
        return self.options.obs
    
    def IsFastMonstersEnabled(self) -> bool:
        return self.options.fast == True
    
    def GetMode(self) -> int:
        return self.options.mode

    def GetMapSets(self):
        return self.map_set_service.mapSets

    def CreateMapSet(self):
        self.map_set_service.CreateMapSet()
        self.mapsets_updated.emit()

    def SetMapByMapId(self, mapId):
        for map in self.maps:
            if map.MapId == mapId:
                self.selected_map = map
                break
        self.selected_map_updated.emit()

    def SetMap(self, index):
        
        # TODO bounds check
        self.selected_map = self.maps[index]
        self.selected_map_updated.emit()

    def SetStatistics(self, index):

        # TODO another bounds check
        self.selected_statistics = self.selected_map.Statistics[index]
        self.selected_statistics_updated.emit()

    def SetMapSet(self, mapSetId):

        # don't do anything if mapset hasn't changed
        if self.selected_map_set is not None and self.selected_map_set.id == mapSetId:
            return
        
        # clear the selected map
        self.selected_map = None

        for mapSet in self.map_set_service.mapSets:
            if mapSet.id == mapSetId:
                self.selected_map_set = mapSet
                break

        # TODO fix that map sets are in many places, here, map set service and jacodemon config
        self.map_set_service.TouchMapSet(mapSet)

        self.maps = self.map_service.LoadMaps(mapSet)
        for map in self.maps:
            map.SetMapSet(mapSet)
            self.stats_service.AddStatsToMap(map)
            self.demo_service.AddDemoesToMapStats(map)

        self.selected_map_updated.emit()
        self.selected_mapset_updated.emit()

    def RemoveMapSet(self, mapSetId):
        self.map_set_service.RemoveMapSetById(mapSetId)
        if self.selected_map_set and self.selected_map_set.id == mapSetId:
            self.selected_map_set = None
        self.mapsets_updated.emit()

    def SetPlayMode(self):
        self.options.mode = LaunchMode.RECORD_DEMO
        self.mode_changed.emit()

    def SetReplayMode(self):
        self.options.mode = LaunchMode.REPLAY_DEMO
        self.mode_changed.emit()

    def Launch(self):

        launch_spec: LaunchSpec = None

        # only save last map if we are not replaying a demo
        if self.options.mode != LaunchMode.REPLAY_DEMO:
            self.map_service.SaveLastMap(self.selected_map)

        if self.options.mode == LaunchMode.REPLAY_DEMO:
            launch_spec = self.selected_statistics.GetLaunchSpec(self.selected_map)
            # TODO verify launch spec
        else:
            launch_spec = self.launch_service.CreateLaunchSpec(self.config, self.options, self.selected_map)

        launch_session = LaunchSession(
            executable=self.config_service.GetExecutableForSourcePort(self.launch_service.GetSourcePortName()),
            cfg_path=self.config_service.GetCfgPathForSourcePort(self.launch_service.GetSourcePortName()),
            iwad_dir=self.config.iwad_dir,
            demo_dir=self.config.demo_dir,
            maps_dir=self.config.maps_dir,
            mods_dir=self.config.mods_dir,
            mode=self.options.mode,
            music=self.options.music)

        self.obs_service.UpdateMapTitle(self.selected_map.GetTitle())
        self.obs_service.SetDemoName(launch_spec.name)
        self.obs_service.SetScene(self.config.play_scene)
        self.obs_service.StartRecording()

        stats = self.launch_service.Launch(
            launch_spec=launch_spec, 
            launch_session=launch_session)
        
        if stats:
            self.stats_service.Save(stats)

        self.obs_service.StopRecording()
        self.obs_service.SetScene(self.config.wait_scene)


        self.selected_mapset_updated.emit()

    def GetDsdaPath(self):
        return self.config.dsda_path

    def SetDsdaPath(self, path):
        self.config.dsda_path = path
        self.config.Save()

    def GetDsdaCfgPath(self):
        return self.config.dsda_cfg
    
    def SetDsdaCfgPath(self, path):
        self.config.dsda_cfg = path
        self.config.Save()

    def GetDsdaHudLump(self):
        return self.config.dsdadoom_hud_lump
    
    def SetDsdaHudLump(self, path):
        self.config.dsdadoom_hud_lump = path
        self.config.Save()

def InitialiseAppModel():

    from jacodemon.service.launch.dsda_service import DsdaService

    """Pretty please don't call this more than once. Used for initial setup 
    and individual components testing"""

    config_service = ConfigService()
    map_set_service = MapSetService(config_service.config)
    map_service = MapService(config_service.config.maps_dir)
    stats_service = StatsService(config_service.config.stats_dir)
    demo_service = DemoService(config_service.config.demo_dir)
    launch_service = DsdaService()
    options_service = OptionsService()

    obs_service = None
    if options_service.GetOptions().obs:
        obs_service = ObsService(config_service.config)
    else:
        obs_service = MockObsService(config_service.config)

    # model, view, controller setup
    return AppModel(
        config_service=config_service, 
        map_set_service=map_set_service,
        map_service=map_service,
        stats_service=stats_service,
        demo_service=demo_service,
        launch_service=launch_service,
        options_service=options_service,
        obs_service=obs_service)
