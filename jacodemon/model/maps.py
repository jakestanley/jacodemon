import os
from typing import List

class MapSet:
    def __init__(self, paths: List[str], name = None) -> None:
        self.name = name
        self.paths = paths
        # TODO port
        self.port = ""

    def HasInvalidConfiguration(self):
        for path in self.paths:
            if not os.path.exists(path):
                return True
        return False


    def dictify(self):
        return {
            "name": self.name,
            "paths": self.paths
        }

def LoadMapSet(dict) -> MapSet:
    return MapSet(dict["paths"], dict["name"])
