from jacodemon.model.maps import MapSetPath, MapSet

def LoadMapSet(dict) -> MapSet:
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
        return [LoadMapSet(ms) for ms in sets]
