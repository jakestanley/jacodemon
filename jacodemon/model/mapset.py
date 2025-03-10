import os
import uuid
from typing import List

class MapSetPath:
    def __init__(self, path, enabled=True):
        self.path = path
        self.enabled = enabled

    def to_dict(self):
        return {
            "path": self.path,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.path = data.get('path')
        instance.enabled = data.get('enabled', True)

        return instance
    

class MapSet:

    def __init__(self, paths: List[MapSetPath], name = None, id=None, iwad=None, compLevel=None) -> None:
        self.id = str(uuid.uuid4()) if id is None else id
        self.name = name
        self.paths: List[MapSetPath] = paths
        self.iwad = iwad
        self.compLevel = compLevel
        self.text = ""

    def HasInvalidConfiguration(self):
        for path in self.paths:
            if not os.path.exists(path.path):
                return True
        return False

    def AddFile(self, path: str):
        self.paths.append(MapSetPath(path))
        self.notify_change()

    def RemoveFile(self, path: str):
        self.paths = [p for p in self.paths if p.path != path]
        self.notify_change()

    """
    To identify this map set for statistics when storing, choose the first 
    alphabetically in order of extension starting with WAD, DEH
    """
    def GetMapSetPrefix(self):
        mod_prefix = None

        paths = sorted([path.path for path in self.paths if path.enabled])

        mod_prefix = next((p for p in paths if p.lower().endswith(".wad")), None)
        
        if mod_prefix is None:
            mod_prefix = next((p for p in paths if p.lower().endswith(".deh")), None)

        mod_prefix = os.path.basename(mod_prefix) if mod_prefix is not None else None

        if mod_prefix is not None:
            mod_prefix = os.path.splitext(os.path.basename(mod_prefix))[0]
        else:
            raise Exception("Error: Could not get a prefix as there were no files!")
        
        return mod_prefix

    def to_dict(self):
        return {
            # in case UUID is not set, i.e before this code was added, set it
            "id": str(self.id) if self.id else uuid.uuid4(),
            "name": self.name,
            "iwad": self.iwad,
            "compLevel": self.compLevel,
            "paths": [path.to_dict() for path in self.paths],
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.id = data.get('id')
        instance.name = data.get('name')
        instance.iwad = data.get('iwad')
        instance.compLevel = data.get('compLevel')
        instance.paths = [MapSetPath.from_dict(path_data) for path_data in data.get('paths', [])]

        return instance

