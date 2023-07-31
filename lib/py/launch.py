import os
from datetime import datetime

from lib.py.config import Config
from lib.py.map import FlatMap
from lib.py.map_utils import *
from lib.py.options import Options

ULTRA_VIOLENCE = 4
DEFAULT_SKILL = ULTRA_VIOLENCE

class LaunchConfig:
    def __init__(self, options, config):
        self._options: Options = options
        self._config: Config = config
        self._timestr = None
        self._map: FlatMap = None
        self._skill = DEFAULT_SKILL
        self._comp_level = None
        self._window = True
        self._demo_prefix = ""
        self._port_override = None

    def get_comp_level(self):
        # initialise final comp level only
        final_comp_level = 9

        # if comp level has been overridden
        if self._comp_level:
            final_comp_level = self._comp_level
        # or if map has a comp level
        elif self._map.CompLevel:
            final_comp_level = self._map.CompLevel
        # or use default comp level
        else:
            final_comp_level = int(self._config.default_complevel)

        return final_comp_level

    def build_chocolate_doom_args(self):
        
        choccy_args = self.build_args()

        if len(self._map.merges) > 0:
            choccy_args.append("-merge")
            choccy_args.extend(self._map.merges)

        choccy_args.extend(["-config", self._config['chocolatedoom_cfg_default']])
        choccy_args.extend(["-extraconfig", self._config['chocolatedoom_cfg_extra']])

        return choccy_args
    
    def build_dsda_doom_args(self):

        dsda_args = self.build_args()

        final_comp_level = self.get_comp_level()

        dsda_args.extend(['-complevel', str(final_comp_level)])
        # the usual
        dsda_args.extend(['-window', '-levelstat'])

        if self._config.dsdadoom_hud_lump:
            dsda_args.extend(['-hud', self._config.dsdadoom_hud_lump])

        if self._config.dsda_cfg:
            dsda_args.extend(['-config', self._config.dsda_cfg])

        return dsda_args

    def build_args(self):

        doom_args = []

        if len(self._map.dehs) > 0:
            doom_args.append("-deh")
            doom_args.extend(self._map.dehs)

        files = []
        if len(self._map.patches) > 0:
            files.extend(self._map.patches)

        if self._options.mods and len(self._config.mods) > 0:
            files.extend(self._config.mods)

        if len(files) > 0:
            doom_args.append("-file")
            doom_args.extend(files)

        doom_args.extend(['-iwad', os.path.join(self._config.iwad_dir, get_inferred_iwad(self._map.MapId))])
        
        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(self._map.MapId))

        if self._options.record_demo:
            doom_args.append("-record")
            doom_args.append(os.path.join(self._config.demo_dir, self.get_demo_name() + ".lmp"))

        if not self._options.music:
            doom_args.append('-nomusic')

        doom_args.extend(['-skill', f"{self._skill}"])

        return doom_args

    def set_map(self, map):
        self._map = map
    
    # demo_name
    def get_demo_name(self):
        if self._timestr is None:
            self._timestr = datetime.now().strftime("%Y-%m-%dT%H%M%S")

        map_prefix = self._map.GetMapPrefix()
        return f"{map_prefix}-{self._timestr}"

    def get_port(self):

        # default port
        final_port = "dsdadoom"
        if (self._port_override):
            final_port = self._port_override
        elif (self._map.Port):
            final_port = self._map.Port

        # TODO if crispy override set.
        # port_override > crispy override > chocolate
        if final_port == "chocolate" and self._port_override is None:
            if self._config.crispy:
                final_port = "crispy"
            else:
                final_port = "chocolate"

        return final_port

    def get_command(self):

        port = self.get_port()

        command = []
        if port in ["chocolate", "crispy"]:
            if port == ["chocolate"]:
                command.append(self._config.chocolatedoom_path)
            else:
                command.append(self._config.crispydoom_path)
            command.extend(self.build_chocolate_doom_args())
        elif port == "dsdadoom":
            command.append(self._config.dsda_path)
            command.extend(self.build_dsda_doom_args())

        return command
