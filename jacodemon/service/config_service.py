import logging

from typing import List

from jacodemon.model.config import Config, GetConfig
from jacodemon.model.mod import Mod

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import Event, EventService

from PySide6.QtCore import QObject, Signal

class ConfigService(QObject):

    _mods_updated = Signal()

    def __init__(self) -> Config:
        # intrinsics
        self.is_ready = False
        self._logger = logging.getLogger(self.__class__.__name__)

        # register signals
        Registry.get(EventService).register_signal(Event.MODS_UPDATED, self._mods_updated)

        # data
        self.config = GetConfig()

    def initialise(self):
        if self.is_ready:
            return

        self.is_ready = True

    def GetExecutableForSourcePort(self, source_port_name: str) -> str:
        if source_port_name == "dsdadoom":
            return self.config.dsda_path
        
    def GetCfgPathForSourcePort(self, source_port_name: str) -> str:
        if source_port_name == "dsdadoom":
            return self.config.dsda_cfg
        
    def SetDemoDir(self, dir):
        self.config.demo_dir = dir
        self.config.Save()
    
    def SetIwadDir(self, dir):
        self.config.iwad_dir = dir
        self.config.Save()
    
    def SetMapsDir(self, dir):
        self.config.maps_dir = dir
        self.config.Save()
    
    def SetModsDir(self, dir):
        self.config.mods_dir = dir
        self.config.Save()

    def SetDefaultCompLevel(self, level):
        self.config.default_complevel = level
        self.config.Save()

    def SetDefaultSkillLevel(self, skill):
        self.config.skill = skill
        self.config.Save()
    
    def SetMods(self, mods: List[Mod]):
        self.config.mods = [mod.to_dict() for mod in mods]
        self.config.Save()
        self._mods_updated.emit()

    def SetDsdaPath(self, path):
        self.config.dsda_path = path
        self.config.Save()
    
    def SetDsdaCfgPath(self, path):
        self.config.dsda_cfg = path
        self.config.Save()

    def SetDsdaHudLump(self, path):
        self.config.dsdadoom_hud_lump = path
        self.config.Save()

    def GetDemoDir(self):
        return self.config.demo_dir
    
    def GetIwadDir(self):
        return self.config.iwad_dir

    def GetMapsDir(self):
        return self.config.maps_dir

    def GetModsDir(self):
        return self.config.mods_dir

    def GetDefaultCompLevel(self):
        return self.config.default_complevel

    def GetDefaultSkillLevel(self):
        return self.config.skill

    def GetDsdaPath(self):
        return self.config.dsda_path

    def GetDsdaCfgPath(self):
        return self.config.dsda_cfg

    def GetDsdaHudLump(self):
        return self.config.dsdadoom_hud_lump
    
    def Save(self):
        self.config.Save()

    # attempting to abstract away JacodemonConfig
    def GetMods(self) -> List[Mod]:
        return [Mod.from_dict(mod) for mod in self.config.mods]
