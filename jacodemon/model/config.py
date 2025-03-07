import logging
import os

from typing import List
from common_py.config import Config

from jacodemon.model.mapset import MapSet
from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL

_CONFIG_SINGLETON = None

_KEY_IWAD_DIR = 'iwad_dir'
_KEY_MAPS_DIR = 'maps_dir'
_KEY_DEMO_DIR = 'demo_dir'
_KEY_MODS_DIR = 'mods_dir'
_KEY_MODS = 'mods'
_KEY_DEFAULT_COMPLEVEL = 'default_complevel'
_KEY_DSDA_PATH = 'dsda_path'
_KEY_DSDA_CFG = 'dsda_cfg'
_KEY_DSDADOOM_HUD_LUMP = 'dsdadoom_hud_lump'
_KEY_PLAY_SCENE = 'play_scene'
_KEY_WAIT_SCENE = 'wait_scene'
_KEY_BROWSER_SCENE = 'browser_scene'
_KEY_TITLE_SOURCE = 'title_source'
_KEY_SETS = 'sets'
_KEY_SKILL = 'skill'

class JacodemonConfig(Config):

    # TODO this needs a rewrite it's a reyt mess
    def __init__(self) -> None:
        super().__init__("jacodemon")
        self._logger = logging.getLogger(self.__class__.__name__)

        # general
        self.default_complevel = self.config.get(_KEY_DEFAULT_COMPLEVEL, DEFAULT_COMP_LEVEL)

        self.skill = self.config.get(_KEY_SKILL, DEFAULT_SKILL)

        # dsda doom
        self.dsda_path = self.config.get(_KEY_DSDA_PATH)
        self.dsda_cfg = self.config.get(_KEY_DSDA_CFG)
        self.dsdadoom_hud_lump = self.config.get(_KEY_DSDADOOM_HUD_LUMP)

        # OBS
        self.play_scene = self.config.get(_KEY_PLAY_SCENE)
        self.wait_scene = self.config.get(_KEY_WAIT_SCENE)
        self.browser_scene = self.config.get(_KEY_BROWSER_SCENE)
        self.title_source = self.config.get(_KEY_TITLE_SOURCE)

        # files/directories
        self.iwad_dir = self.config.get(_KEY_IWAD_DIR)
        self.maps_dir = self.config.get(_KEY_MAPS_DIR)

        # TODO this is being too prescriptive. we want the persistence back end to be flexible
        #   reusing DEMO_DIR for now
        #self.stats_dir = self.config.get(_KEY_STATS_DIR)
        self.stats_dir = self.config.get(_KEY_DEMO_DIR)

        self.demo_dir = self.config.get(_KEY_DEMO_DIR)
        self.mods_dir = self.config.get(_KEY_MODS_DIR)

        # TODO from cls blah blah
        self.mods = self.config.get(_KEY_MODS, [])
        # self.sets = [maps.LoadMapSet(ms) for ms in self.config.get(_KEY_SETS, [])]
        self.sets = self.config.get(_KEY_SETS, [])

    def _PrepareSave(self):

        self.config[_KEY_IWAD_DIR] = self.iwad_dir
        self.config[_KEY_MAPS_DIR] = self.maps_dir
        self.config[_KEY_DEMO_DIR] = self.demo_dir
        self.config[_KEY_MODS_DIR] = self.mods_dir
        self.config[_KEY_MODS] = self.mods
        self.config[_KEY_DEFAULT_COMPLEVEL] = self.default_complevel
        self.config[_KEY_DSDA_PATH] = self.dsda_path
        self.config[_KEY_DSDA_CFG] = self.dsda_cfg
        self.config[_KEY_DSDADOOM_HUD_LUMP] = self.dsdadoom_hud_lump
        self.config[_KEY_PLAY_SCENE] = self.play_scene
        self.config[_KEY_WAIT_SCENE] = self.wait_scene
        self.config[_KEY_BROWSER_SCENE] = self.browser_scene
        self.config[_KEY_TITLE_SOURCE] = self.title_source
        self.config[_KEY_SETS] = self.sets
        self.config[_KEY_SKILL] = self.skill

    def _DefaultConfig(self):
        cfg: dict = {}
        cfg[_KEY_MODS] = []
        cfg[_KEY_SETS] = []
        return cfg

    def set_dsda_path(self, path):
        if os.path.isfile(path):
            self.dsda_path = path
        elif os.path.basename(path).endswith(".app"):
            self.dsda_path = os.path.join(path, "Contents/Resources/dsda-doom")
        else:
            self._logger.error(f"could not set dsda_path to '{path}'")

    def UpdateMapSets(self, mapSets: List[MapSet]):
        self.sets = [mapSet.to_dict() for mapSet in mapSets]
        self.Save()

"""
If dummy is true, returns a DummyConfig instead of a JacodemonConfig
"""
def GetConfig(dummy=False):
    global _CONFIG_SINGLETON
    if _CONFIG_SINGLETON is None:
        if dummy:
            from jacodemon.misc.dummy import DummyConfig
            _CONFIG_SINGLETON = DummyConfig()
        else:
            _CONFIG_SINGLETON = JacodemonConfig()
    return _CONFIG_SINGLETON
