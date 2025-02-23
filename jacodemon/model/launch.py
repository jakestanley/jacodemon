from jacodemon.model.config import JacodemonConfig
from jacodemon.model.map import Map
from jacodemon.misc.map_utils import *
from jacodemon.model.options import Options

from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL

# TODO later if we wish to properly implement multi port support, we may 
#   wish to make this a super class. as a fun exercise we should make a 
#   DsdaLaunchConfig subclass sooner than later
class LaunchConfig:
    def __init__(self, config: JacodemonConfig, options: Options, map: Map, demo_index: int):
        self.timestamp = None
        self.map: Map = map
        self.window = True
        self.demo_index = demo_index

        if config.skill:
            self.skill = config.skill
        else:
            self.skill = DEFAULT_SKILL

        if map.MapSet.compLevel:
            self.comp_level = map.MapSet.compLevel
        elif config.default_complevel:
            self.comp_level = config.default_complevel
        else:
            self.comp_level = DEFAULT_COMP_LEVEL

        if options.record_demo:
            self.record_demo = True
        else:
            self.record_demo = False

        if options.music:
            self.music = True
        else:
            self.music = False

        if options.mods:
            self.mods = True
        else:
            self.mods = False

        if options.fast:
            self.fast = True
        else:
            self.fast = False

    def set_replay(self, demo):
        self._demo_path = demo.path
        # FIXME: hack, should use method for this idk
        self._comp_level = demo.stats._stats.get('compLevel', self.get_comp_level())
