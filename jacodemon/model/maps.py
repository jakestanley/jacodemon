import os
import uuid
from typing import List

class MapSetPath:
    def __init__(self, path, enabled=True):
        self.path = path
        self.enabled = enabled
        # self.valid # TODO?

    def Copy(self):
        return MapSetPath(self.path, self.enabled)

    def dictify(self):
        return {
            "path": self.path,
            "enabled": self.enabled
        }

class MapSet:
    def __init__(self, paths: List[MapSetPath], name = None, id=None) -> None:
        self.id = uuid.uuid4() if id is None else id
        self.name = name
        self.paths: List[MapSetPath] = paths
        # TODO port
        self.port = ""

    def HasInvalidConfiguration(self):
        for path in self.paths:
            if not os.path.exists(path.path):
                return True
        return False

    def AddFile(self, path: str):
        self.paths.append(MapSetPath(path))

    def RemoveFile(self, path: str):
        self.paths = [p for p in self.paths if p.path != path]

    def Copy(self):
        return MapSet([path.Copy() for path in self.paths], self.name, self.id)

    def dictify(self):
        return {
            # in case UUID is not set, i.e before this code was added, set it
            "id": str(self.id) if self.id else uuid.uuid4(),
            "name": self.name,
            "paths": [path.dictify() for path in self.paths]
        }

def LoadMapSet(dict) -> MapSet:
    paths = []
    for path in dict["paths"]:
        paths.append(MapSetPath(path["path"], path["enabled"]))

    return MapSet(paths, dict["name"], dict.get("id"))
