from enum import Enum, auto

from dataclasses import dataclass
from typing import List

from jacodemon.misc.files import ParseTimestampFromPath

class LaunchMode(Enum):
    RECORD_DEMO = auto()
    REPLAY_DEMO = auto()

@dataclass(frozen=True)
class LaunchSpec:
    """
    Immutable launch properties that affect playback or demo compatibility
    """
    name: str
    timestamp: str
    map_id: str
    # files (thinking about saving hashes)
    iwad: str
    wads: List[tuple[str, str]]
    dehs: List[tuple[str, str]]
    mods: List[tuple[str, str]]
    # modifiers
    fast_monsters: bool
    skill: int
    comp_level: str

    @classmethod
    def from_dict(cls, data):

        if data is None:
            return None

        return cls(
            name=data['name'],
            timestamp=data.get('timestamp', ParseTimestampFromPath(data['name'])),
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

@dataclass
class LaunchSession:
    executable: str
    cfg_path: str
    iwad_dir: str
    demo_dir: str
    maps_dir: str
    mods_dir: str
    mode: LaunchMode
    music: bool
