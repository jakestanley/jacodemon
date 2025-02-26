from dataclasses import dataclass
from typing import List

from jacodemon.model.options import Options

@dataclass(frozen=True)
class LaunchConfig:
    """
    Immutable launch properties that affect playback or demo compatibility
    """
    name: str
    timestamp: str
    map_id: str
    # files
    iwad: str
    wads: List[str]
    dehs: List[str]
    mods: List[str]
    # modifiers
    fast_monsters: bool
    skill: int
    comp_level: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            timestamp=data['timestamp'],
            map_id=data['map_id'],
            iwad=data['iwad'],
            wads=data['wads'],
            dehs=data['dehs'],
            mods=data['mods'],
            fast_monsters=data['fast_monsters'],
            skill=data['skill'],
            comp_level=data['comp_level']
        )
    
    def to_dict(self):
        return {
            'name': self.name,
            'timestamp': self.timestamp,
            'map_id': self.map_id,
            'iwad': self.iwad,
            'wads': self.wads,
            'dehs': self.dehs,
            'mods': self.mods,
            'fast_monsters': self.fast_monsters,
            'skill': self.skill,
            'comp_level': self.comp_level
        }

class LaunchConfigMutables:
    """
    Extra launch config options that do not affect playback or demo compatibility
    """
    def __init__(self, options: Options):
        self.record_demo = options.record_demo
        self.music = options.music
