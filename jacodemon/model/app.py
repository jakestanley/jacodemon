import logging

from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.model.launch import LaunchMode, LaunchSpec, LaunchSession

from jacodemon.service.config_service import ConfigService
from jacodemon.service.map_service import MapService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.demo_service import DemoService
from jacodemon.service.launch.launch_service import LaunchService
from jacodemon.service.obs_service import ObsService
from jacodemon.service.wad_service import WadService
from jacodemon.service.options_service import OptionsService

class AppModel(QObject):

    # used for when we switch to prelaunch
    mode_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

        self.config_service: ConfigService = Registry.get(ConfigService)
        self.map_set_service: MapSetService = Registry.get(MapSetService)
        self.map_service: MapService = Registry.get(MapService)
        self.stats_service: StatsService = Registry.get(StatsService)
        self.demo_service: DemoService = Registry.get(DemoService)
        self.options_service: OptionsService = Registry.get(OptionsService)
        self.obs_service: ObsService = Registry.get(ObsService)
        self.wad_service: WadService = Registry.get(WadService)
        self.launch_service: LaunchService = Registry.get(LaunchService)

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
        self.ReloadMaps()

        self.selected_mapset_updated.emit()
