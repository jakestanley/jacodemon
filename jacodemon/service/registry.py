from typing import Type, Any

from jacodemon.service.config_service import ConfigService

from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.map_service import MapService
from jacodemon.service.stats_service import StatsService
from jacodemon.service.demo_service import DemoService
from jacodemon.service.launch.launch_service import LaunchService
from jacodemon.service.launch.dsda_service import DsdaService
from jacodemon.service.options_service import OptionsService
from jacodemon.service.obs_service import ObsService
from jacodemon.service.obs.mock_obs_service import MockObsService
from jacodemon.service.wad_service import WadService

class Registry:
    _services: dict[Type[Any], Any] = {}

    @staticmethod
    def register(cls, instance):
        Registry._services[cls] = instance

    @staticmethod
    def get(cls):
        return Registry._services[cls]
    
def CreateAndRegisterServices():

    config_service = ConfigService()
    options_service = OptionsService()

    Registry.register(ConfigService, config_service)
    Registry.register(MapService, MapService(config_service.config.maps_dir))
    Registry.register(MapSetService, MapSetService(config_service.config))
    Registry.register(StatsService, StatsService(config_service.config.stats_dir))
    Registry.register(DemoService, DemoService(config_service.config.demo_dir))
    Registry.register(LaunchService, DsdaService())
    Registry.register(OptionsService, options_service)
    Registry.register(WadService, WadService(config_service.config.maps_dir))

    Registry.get(ConfigService).initialise()
    Registry.get(MapService).initialise()
    Registry.get(MapSetService).initialise()
    Registry.get(StatsService).initialise()
    Registry.get(DemoService).initialise()
    Registry.get(LaunchService).initialise()
    Registry.get(OptionsService).initialise()
    Registry.get(WadService).initialise()

def CreateAndRegisterObsService() -> bool:
    """
    Creates and registers the OBS service. Returns True if successful, False otherwise.
    """

    from jacodemon.service.obs_service import ObsServiceException
    from PyQt6.QtWidgets import QMessageBox

    options_service: OptionsService = Registry.get(OptionsService)
    config_service: ConfigService = Registry.get(ConfigService)
    
    obs_service = None
    if options_service.IsObsEnabled():
        try:
            obs_service = ObsService(config_service.config)
        except ObsServiceException as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(e.cause)
            msg_box.setWindowTitle("Error")
            msg_box.exec()
            return False
    else:
        obs_service = MockObsService(config_service.config)

    Registry.register(ObsService, obs_service)

    return True
