from typing import List

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from jacodemon.map import FlatMap, EnrichMaps, GetMapEntriesFromFiles
from jacodemon.csv import load_raw_maps_from_wad
from jacodemon.demo import GetDemosForMap, AddBadgesToMap

_SINGLETON = None

def LoadRawMapsFromMapSet(mapSet: MapSet) -> List[FlatMap]:

    files = [path.path for path in mapSet.paths if path.enabled]
    maps = []
    mapentries = GetMapEntriesFromFiles(files)
    
    for map in mapentries:
        maps.append(FlatMap(
            ModName=mapSet.name, 
            Files=files,
            MapId=map['MapId'],
            MapName=map['MapName']))
        
    return maps

class MapsSelectController:

    def __init__(self) -> None:
        if _SINGLETON is not None:
            raise Exception("MapsSelectController MUST only be instantiated once")
        super().__init__()
        self.mapSet: MapSet = None
        self.maps: List[FlatMap] = []

    def Open(self, mapSetId):
        # TODO: not sure if this should all be in here
        self.mapSet: MapSet = GetConfig().GetMapSetById(mapSetId)
        raw_maps = LoadRawMapsFromMapSet(self.mapSet)
        self.maps = EnrichMaps(raw_maps)
        for map in self.maps:
            AddBadgesToMap(map, GetConfig().demo_dir)

        # return true if successfully loaded maps. not sure if this is 
        #   intuitive or not though rn
        if len(self.maps) > 0:
            return True
        return False

def GetMapsSelectController() -> MapsSelectController:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = MapsSelectController()
    return _SINGLETON
