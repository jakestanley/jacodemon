import os

from common_py.config import Config

_CONFIG_SINGLETON = None

_KEY_IWAD_DIR = 'iwad_dir'
_KEY_MAPS_DIR = 'maps_dir'
_KEY_DEMO_DIR = 'demo_dir'
_KEY_MODS = 'mods'
_KEY_DEFAULT_COMPLEVEL = 'default_complevel'
_KEY_DSDA_PATH = 'dsda_path'
_KEY_DSDA_CFG = 'dsda_cfg'
_KEY_DSDADOOM_HUD_LUMP = 'dsdadoom_hud_lump'
_KEY_PLAY_SCENE = 'play_scene'
_KEY_WAIT_SCENE = 'wait_scene'
_KEY_BROWSER_SCENE = 'browser_scene'
_KEY_TITLE_SOURCE = 'title_source'
_KEY_CHOCOLATEDOOM_PATH = 'chocolatedoom_path'
_KEY_CHOCOLATEDOOM_CFG_DEFAULT = 'chocolatedoom_cfg_default'
_KEY_CHOCOLATEDOOM_CFG_EXTRA = 'chocolatedoom_cfg_extra'
_KEY_CRISPYDOOM_PATH = 'crispydoom_path'

class Mod:
    def __init__(self, path: str, enabled: bool = True):
        self.path = path
        self.enabled = enabled

    def Dictify(self):
        dic = {}
        dic['path'] = self.path
        dic['enabled'] = self.enabled
        return dic

class JacodemonConfig(Config):

    def __init__(self) -> None:
        super().__init__("jacodemon")

        # general
        self.default_complevel = self.config.get(_KEY_DEFAULT_COMPLEVEL)

        # dsda doom
        self.dsda_path = self.config.get(_KEY_DSDA_PATH)
        self.dsda_cfg = self.config.get(_KEY_DSDA_CFG)
        self.dsdadoom_hud_lump = self.config.get(_KEY_DSDADOOM_HUD_LUMP)

        # OBS
        self.play_scene = self.config.get(_KEY_PLAY_SCENE)
        self.wait_scene = self.config.get(_KEY_WAIT_SCENE)
        self.browser_scene = self.config.get(_KEY_BROWSER_SCENE)
        self.title_source = self.config.get(_KEY_TITLE_SOURCE)

        # chocolate/crispy doom
        self.chocolatedoom_path = self.config.get(_KEY_CHOCOLATEDOOM_PATH)
        self.chocolatedoom_cfg_default = self.config.get(_KEY_CHOCOLATEDOOM_CFG_DEFAULT)
        self.chocolatedoom_cfg_extra = self.config.get(_KEY_CHOCOLATEDOOM_CFG_EXTRA)
        self.crispydoom_path = self.config.get(_KEY_CRISPYDOOM_PATH)

        # files/directories
        self.iwad_dir = self.config.get(_KEY_IWAD_DIR)
        self.maps_dir = self.config.get(_KEY_MAPS_DIR)
        self.demo_dir = self.config.get(_KEY_DEMO_DIR)
        loaded_mods = self.config.get(_KEY_MODS, [])

        self.mods = []
        for mod in loaded_mods:
            if isinstance(mod, str):
                self.mods.append(Mod(mod))
            else:
                self.mods.append(Mod(mod.get('path'), mod.get('enabled', True)))

    def _PrepareSave(self):

        self.config[_KEY_IWAD_DIR] = self.iwad_dir
        self.config[_KEY_MAPS_DIR] = self.maps_dir
        self.config[_KEY_DEMO_DIR] = self.demo_dir
        self.config[_KEY_MODS] = [mod.Dictify() for mod in self.mods]
        self.config[_KEY_DEFAULT_COMPLEVEL] = self.default_complevel
        self.config[_KEY_DSDA_PATH] = self.dsda_path
        self.config[_KEY_DSDA_CFG] = self.dsda_cfg
        self.config[_KEY_DSDADOOM_HUD_LUMP] = self.dsdadoom_hud_lump
        self.config[_KEY_PLAY_SCENE] = self.play_scene
        self.config[_KEY_WAIT_SCENE] = self.wait_scene
        self.config[_KEY_BROWSER_SCENE] = self.browser_scene
        self.config[_KEY_TITLE_SOURCE] = self.title_source
        self.config[_KEY_CHOCOLATEDOOM_PATH] = self.chocolatedoom_path
        self.config[_KEY_CHOCOLATEDOOM_CFG_DEFAULT] = self.chocolatedoom_cfg_default
        self.config[_KEY_CHOCOLATEDOOM_CFG_EXTRA] = self.chocolatedoom_cfg_extra
        self.config[_KEY_CRISPYDOOM_PATH] = self.crispydoom_path

    def _DefaultConfig(self):
        cfg: dict = {}
        cfg[_KEY_MODS] = []
        return cfg

    def set_dsda_path(self, path):
        if os.path.isfile(path):
            self.dsda_path = path
        elif os.path.basename(path).endswith(".app"):
            self.dsda_path = os.path.join(path, "Contents/Resources/dsda-doom")
        else:
            print(f"Error: could not set dsda_path to '{path}'")

def GetConfig():
    global _CONFIG_SINGLETON
    if _CONFIG_SINGLETON is None:
        _CONFIG_SINGLETON = JacodemonConfig()
    return _CONFIG_SINGLETON