from typing import Type, Any

class Context:
    _services: dict[Type[Any], Any] = {}

    @staticmethod
    def register(cls, instance):
        Context._services[cls] = instance

    @staticmethod
    def get(cls):
        return Context._services[cls]
    
def InitialiseContext():

    from jacodemon.service.config_service import ConfigService
    from jacodemon.service.map_service import MapService
    from jacodemon.service.map_set_service import MapSetService
    from jacodemon.service.stats_service import StatsService
    from jacodemon.service.demo_service import DemoService
    from jacodemon.service.launch.dsda_service import DsdaService
    from jacodemon.service.options_service import OptionsService
    from jacodemon.service.obs_service import ObsService
    from jacodemon.service.obs.mock_obs_service import MockObsService
    from jacodemon.service.wad_service import WadService

    config_service = ConfigService()
    options_service = OptionsService()

    obs_service = None
    if options_service.GetOptions().obs:
        obs_service = ObsService(config_service.config)
    else:
        obs_service = MockObsService(config_service.config)

    Context.register(ConfigService, config_service)
    Context.register(MapService, MapService(config_service.config.maps_dir))
    Context.register(MapSetService, MapSetService(config_service.config))
    Context.register(StatsService, StatsService(config_service.config.stats_dir))
    Context.register(DemoService, DemoService(config_service.config.demo_dir))
    Context.register(DsdaService, DsdaService())
    Context.register(OptionsService, options_service)
    Context.register(ObsService, obs_service)
    Context.register(WadService, WadService(config_service.config.maps_dir))
