import logging

from PySide6.QtCore import QObject, Signal

from jacodemon.model.options import GetOptions, Options
from jacodemon.model.launch import LaunchMode

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event

class OptionsService(QObject):

    _mode_changed = Signal(LaunchMode)

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self.options: Options = GetOptions()

        # register events
        event_service = Registry.get(EventService)
        event_service.register_signal(Event.MODE_CHANGED, self._mode_changed)
    
    def IsRecordDemoEnabled(self) -> bool:
        return self.options.mode == LaunchMode.RECORD_DEMO
    
    def IsAutoRecordEnabled(self) -> bool:
        return self.options.auto_record and self.options.obs
    
    def IsObsAvailable(self) -> bool:
        return self.options.obs
    
    def IsModsEnabled(self) -> bool:
        return self.options.mods
    
    def IsMusicEnabled(self) -> bool:
        return self.options.music
    
    def IsObsEnabled(self) -> bool:
        return self.options.obs
    
    def IsFastMonstersEnabled(self) -> bool:
        return self.options.fast == True

    def GetMode(self) -> LaunchMode:
        return self.options.mode
    
    def SetDemoMode(self):
        self.options.mode = LaunchMode.REPLAY_DEMO
        self._mode_changed.emit(self.options.mode)

    def SetPlayMode(self):
        self.options.mode = LaunchMode.RECORD_DEMO
        self._mode_changed.emit(self.options.mode)
