import platform
import os
from datetime import datetime

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.map import FlatMap
from jacodemon.map_utils import *
from jacodemon.options import Options, GetOptions

ULTRA_VIOLENCE = 4
DEFAULT_SKILL = ULTRA_VIOLENCE

# TODO later if we wish to properly implement multi port support, we may 
#   wish to make this a super class. as a fun exercise we should make a 
#   DsdaLaunchConfig subclass sooner than later
class LaunchConfig:
    def __init__(self):
        self.timestamp = None
        self._map: FlatMap = None
        self._mapSet = None
        self._skill = DEFAULT_SKILL
        self._comp_level = None
        self._window = True
        self._demo_path = None

    def get_comp_level(self):
        # this will be overridden in all branches
        final_comp_level = 9

        # if comp level has been overridden
        if self._comp_level:
            final_comp_level = self._comp_level
        # or if map has a comp level
        elif self._map.CompLevel:
            final_comp_level = self._map.CompLevel
        # or if the map set has a comp level
        elif self._mapSet.compLevel:
            final_comp_level = self._mapSet.compLevel
        # or use default comp level
        else:
            final_comp_level = str(GetConfig().default_complevel)

        # only numbers allowed as args
        if final_comp_level == 'vanilla':
            # https://doomwiki.org/wiki/COMPLVL
            final_comp_level = 4

        if final_comp_level == 'mbf21':
            final_comp_level = 21

        return final_comp_level

    def build_chocolate_doom_args(self):
        
        choccy_args = self.build_args()

        if len(self._map.merges) > 0:
            choccy_args.append("-merge")
            choccy_args.extend(self._map.merges)

        choccy_args.extend(["-config", GetConfig()['chocolatedoom_cfg_default']])
        choccy_args.extend(["-extraconfig", GetConfig()['chocolatedoom_cfg_extra']])

        return choccy_args
    
    def build_dsda_doom_args(self):

        dsda_args = self.build_args()

        final_comp_level = self.get_comp_level()

        dsda_args.extend(['-complevel', str(final_comp_level)])
        dsda_args.append('-levelstat')

        if platform.system() == "Darwin":
            dsda_args.extend(['-geom', '1920x1080f'])
        else:
            dsda_args.append('-window')
        

        if GetConfig().dsdadoom_hud_lump:
            dsda_args.extend(['-hud', GetConfig().dsdadoom_hud_lump])

        if GetConfig().dsda_cfg:
            dsda_args.extend(['-config', GetConfig().dsda_cfg])

        return dsda_args

    def build_args(self):

        doom_args = []

        if len(self._map.dehs) > 0:
            doom_args.append("-deh")
            doom_args.extend(self._map.dehs)

        files = []
        if len(self._map.patches) > 0:
            files.extend(self._map.patches)

        if GetOptions().mods:
            enabled_mods = [mod for mod in GetConfig().mods if mod.enabled]
            if len(enabled_mods) > 0:
                files.extend(mod.path for mod in enabled_mods)

        if len(files) > 0:
            doom_args.append("-file")
            doom_args.extend(files)

        doom_args.extend(['-iwad', os.path.join(GetConfig().iwad_dir, get_inferred_iwad(self._map.MapId))])
        
        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(self._map.MapId))

        if self._demo_path:
            doom_args.append("-playdemo")
            doom_args.append(self._demo_path)
        elif GetOptions().record_demo:
            doom_args.append("-record")
            doom_args.append(os.path.join(GetConfig().demo_dir, self.get_demo_name() + ".lmp"))

        if not GetOptions().music:
            doom_args.append('-nomusic')

        doom_args.extend(['-skill', f"{self._skill}"])

        return doom_args

    def set_map(self, map):
        self._map = map

    def set_map_set(self, mapSet):
        self._mapSet = mapSet
    
    def set_replay(self, demo):
        self._demo_path = demo.path
        # FIXME: hack, should use method for this idk
        self._comp_level = demo.stats._stats.get('compLevel', self.get_comp_level())

    # demo_name
    def get_demo_name(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")

        map_prefix = self._map.GetMapPrefix()
        return f"{map_prefix}-{self.timestamp}"

    # TODO: consider when we are replaying a demo should we get and tweak the args from the stats file?
    def get_command(self):

        command = [GetConfig().dsda_path]
        # TODO: check dsda-doom path is set before attempting to launch
        command.extend(self.build_dsda_doom_args())

        return command
