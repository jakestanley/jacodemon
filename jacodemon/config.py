import sys
import os 
import appdirs
import json

from common_py.config import GetConfigPath

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

class Config:
    def __init__(self, data):

        # general
        self.default_complevel = data.get('default_complevel')

        # dsda doom
        self.dsda_path = data.get(_KEY_DSDA_PATH)
        self.dsda_cfg = data.get(_KEY_DSDA_CFG)
        self.dsdadoom_hud_lump = data.get(_KEY_DSDADOOM_HUD_LUMP)

        # OBS
        self.play_scene = data.get(_KEY_PLAY_SCENE)
        self.wait_scene = data.get(_KEY_WAIT_SCENE)
        self.browser_scene = data.get(_KEY_BROWSER_SCENE)
        self.title_source = data.get(_KEY_TITLE_SOURCE)

        # chocolate/crispy doom
        self.chocolatedoom_path = data.get(_KEY_CHOCOLATEDOOM_PATH)
        self.chocolatedoom_cfg_default = data.get(_KEY_CHOCOLATEDOOM_CFG_DEFAULT)
        self.chocolatedoom_cfg_extra = data.get(_KEY_CHOCOLATEDOOM_CFG_EXTRA)
        self.crispydoom_path = data.get(_KEY_CRISPYDOOM_PATH)

        # files/directories
        self.iwad_dir = data.get(_KEY_IWAD_DIR)
        self.maps_dir = data.get(_KEY_MAPS_DIR)
        self.demo_dir = data.get(_KEY_DEMO_DIR)
        loaded_mods = data.get(_KEY_MODS, [])
        self.mods = []
        for mod in loaded_mods:
            if isinstance(mod, str):
                self.mods.append(Mod(mod))
            else:
                self.mods.append(Mod(mod.get('path'), mod.get('enabled', True)))

    def Save(self):
        config_path = GetConfigPath("jacodemon")
        
        settings = {}
        settings[_KEY_IWAD_DIR] = self.iwad_dir
        settings[_KEY_MAPS_DIR] = self.maps_dir
        settings[_KEY_DEMO_DIR] = self.demo_dir
        settings[_KEY_MODS] = [mod.Dictify() for mod in self.mods]
        settings[_KEY_DEFAULT_COMPLEVEL] = self.default_complevel
        settings[_KEY_DSDA_PATH] = self.dsda_path
        settings[_KEY_DSDA_CFG] = self.dsda_cfg
        settings[_KEY_DSDADOOM_HUD_LUMP] = self.dsdadoom_hud_lump
        settings[_KEY_PLAY_SCENE] = self.play_scene
        settings[_KEY_WAIT_SCENE] = self.wait_scene
        settings[_KEY_BROWSER_SCENE] = self.browser_scene
        settings[_KEY_TITLE_SOURCE] = self.title_source
        settings[_KEY_CHOCOLATEDOOM_PATH] = self.chocolatedoom_path
        settings[_KEY_CHOCOLATEDOOM_CFG_DEFAULT] = self.chocolatedoom_cfg_default
        settings[_KEY_CHOCOLATEDOOM_CFG_EXTRA] = self.chocolatedoom_cfg_extra
        settings[_KEY_CRISPYDOOM_PATH] = self.crispydoom_path

        with open(config_path, "w") as config_file:
            json.dump(settings, config_file, indent=4)

    def set_dsda_path(self, path):
        if os.path.isfile(path):
            self.dsda_path = path
        elif os.path.basename(path).endswith(".app"):
            self.dsda_path = os.path.join(path, "Contents/Resources/dsda-doom")
        else:
            print(f"Error: could not set dsda_path to '{path}'")

def LoadConfig() -> Config:

    config_path = GetConfigPath("jacodemon")
    print(f"Loading config from {config_path}")

    try:
        with open(config_path, "r") as config_file:
            return Config(json.load(config_file))
    except (FileNotFoundError):
        print("Warning: no configuration found. Creating a new one")
        return Config({})
    except (json.JSONDecodeError):
        print("Error: Got a JSONDecodeError when loading configuration. Check or remove the file")
        sys.exit(1)
