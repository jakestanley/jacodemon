from jacodemon.model.mapset import MapSetPath, MapSet

def _LoadMapSet(dict) -> MapSet:
    paths = []
    for path in dict["paths"]:
        paths.append(MapSetPath(path["path"], path["enabled"]))

    return MapSet(paths=paths, 
                  name=dict["name"], 
                  id=dict.get("id"), 
                  iwad=dict.get("iwad"), 
                  compLevel=dict.get("compLevel"))

class MapSetService:

    def __init__(self):
        pass

    def LoadMapSets(self, sets):
        return [_LoadMapSet(ms) for ms in sets]
