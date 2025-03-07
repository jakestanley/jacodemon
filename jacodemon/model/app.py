import logging

from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.model.launch import LaunchMode, LaunchSpec, LaunchSession

from jacodemon.service.config_service import ConfigService
from jacodemon.service.map_service import MapService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.launch.launch_service import LaunchService
from jacodemon.service.obs_service import ObsService
from jacodemon.service.options_service import OptionsService

class AppModel(QObject):

    launch_completed = Signal()
    
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

        self.config_service: ConfigService = Registry.get(ConfigService)
        self.map_service: MapService = Registry.get(MapService)
        self.stats_service: StatsService = Registry.get(StatsService)
        self.options_service: OptionsService = Registry.get(OptionsService)
        self.obs_service: ObsService = Registry.get(ObsService)
        self.launch_service: LaunchService = Registry.get(LaunchService)

    def Launch(self):

        launch_spec: LaunchSpec = None

        # only save last map if we are not replaying a demo
        if self.options_service.GetMode() != LaunchMode.REPLAY_DEMO:
            self.map_service.SaveLastMap()

        if self.options_service.GetMode() == LaunchMode.REPLAY_DEMO:
            launch_spec = self.stats_service.selected_statistics.GetLaunchSpec(self.map_service.selected_map)
            # TODO verify launch spec
        else:
            launch_spec = self.launch_service.CreateLaunchSpec(self.config_service.config, self.options_service.options, self.map_service.selected_map)

        launch_session = LaunchSession(
            executable=self.config_service.GetExecutableForSourcePort(self.launch_service.GetSourcePortName()),
            cfg_path=self.config_service.GetCfgPathForSourcePort(self.launch_service.GetSourcePortName()),
            iwad_dir=self.config_service.GetIwadDir(),
            demo_dir=self.config_service.GetDemoDir(),
            maps_dir=self.config_service.GetMapsDir(),
            mods_dir=self.config_service.GetModsDir(),
            mode=self.options_service.GetMode(),
            music=self.options_service.options.music)

        self.obs_service.UpdateMapTitle(self.map_service.selected_map.GetTitle())
        self.obs_service.SetDemoName(launch_spec.name)
        self.obs_service.SetScene(self.config_service.config.play_scene)
        self.obs_service.StartRecording()

        stats = self.launch_service.Launch(
            launch_spec=launch_spec, 
            launch_session=launch_session)
        
        if stats:
            self.stats_service.Save(stats)

        self.obs_service.StopRecording()
        self.obs_service.SetScene(self.config_service.config.wait_scene)

        self.launch_completed.emit()
