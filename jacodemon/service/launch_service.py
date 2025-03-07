import logging

from PySide6.QtCore import QObject, Signal

from jacodemon.model.launch import LaunchMode, LaunchSpec, LaunchSession

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.config_service import ConfigService
from jacodemon.service.doom_service import DoomService
from jacodemon.service.map_service import MapService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.obs_service import ObsService
from jacodemon.service.options_service import OptionsService

# TODO: this really should be launch service, and we should do away with inheritance for now
class LaunchService(QObject):

    _launch_completed = Signal()
    
    def __init__(self):
        super().__init__()

        # intrinsics
        self._is_ready = False
        self._logger = logging.getLogger(self.__class__.__name__)

        # services
        self.doom_service: DoomService = None
        self.config_service: ConfigService = None
        self.map_service: MapService = None
        self.stats_service: StatsService = None
        self.options_service: OptionsService = None
        self.obs_service: ObsService = None

        # register events
        Registry.get(EventService).register_signal(Event.LAUNCH_COMPLETED, self._launch_completed)

    def initialise(self):
        if self._is_ready:
            return       

        self.doom_service = Registry.get(DoomService)
        self.config_service = Registry.get(ConfigService)
        self.map_service = Registry.get(MapService)
        self.stats_service = Registry.get(StatsService)
        self.options_service = Registry.get(OptionsService)
        self.obs_service = Registry.get(ObsService)

        self._is_ready = True 

    def Launch(self):

        launch_spec: LaunchSpec = None

        # only save last map if we are not replaying a demo
        if self.options_service.GetMode() != LaunchMode.REPLAY_DEMO:
            self.map_service.SaveLastMap()

        if self.options_service.GetMode() == LaunchMode.REPLAY_DEMO:
            launch_spec = self.stats_service.selected_statistics.GetLaunchSpec(self.map_service.selected_map)
            # TODO verify launch spec
        else:
            launch_spec = self.doom_service.CreateLaunchSpec(self.config_service.config, self.options_service.options, self.map_service.selected_map)

        launch_session = LaunchSession(
            executable=self.config_service.GetExecutableForSourcePort(self.doom_service.GetSourcePortName()),
            cfg_path=self.config_service.GetCfgPathForSourcePort(self.doom_service.GetSourcePortName()),
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

        stats = self.doom_service.Launch(
            launch_spec=launch_spec, 
            launch_session=launch_session)
        
        if stats:
            self.stats_service.Save(stats)

        self.obs_service.StopRecording()
        self.obs_service.SetScene(self.config_service.config.wait_scene)

        self._launch_completed.emit()
