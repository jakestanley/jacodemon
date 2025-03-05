from jacodemon.model.options import GetOptions, Options

from jacodemon.model.launch import LaunchMode

class OptionsService:
    def __init__(self):
        self.options: Options = GetOptions()

    def initialise(self):
        pass
    
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
    
    def GetMode(self) -> int:
        return self.options.mode
