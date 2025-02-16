from typing import List

from jacodemon.logs import LogManager, GetLogManager
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from jacodemon.model.flatmap import FlatMap, EnrichMaps, GetMapEntriesFromFiles
from jacodemon.model.demo import GetDemosForMap, AddBadgesToMap
from jacodemon.service.maps.cache import LoadMapsFromCache, AddMapsToCache

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
            MapName=map.get('MapName')))
        
    return maps

class MapsSelectService:

    def __init__(self) -> None:
        if _SINGLETON is not None:
            raise Exception("MapsSelectController MUST only be instantiated once")
        super().__init__()
        self.mapSet: MapSet = None
        self.maps: List[FlatMap] = []

    def LoadMaps(self, mapSetId) -> bool:

        logger = GetLogManager().GetLogger(__name__)

        # TODO: if files change, evict cache
        self.mapSet: MapSet = GetConfig().GetMapSetById(mapSetId)
        self.maps = LoadMapsFromCache(mapSetId)
        
        if self.maps:
            logger.info(f"Loaded {len(self.maps)} maps from cache")
            return
        
        logger.info("Cache miss. Loading maps from scratch")

        raw_maps = LoadRawMapsFromMapSet(self.mapSet)
        self.maps = EnrichMaps(raw_maps)
        AddMapsToCache(mapSetId, self.maps)

    def Open(self, mapSetId):

        GetConfig().TouchMapSet(mapSetId)

        self.LoadMaps(mapSetId)
        # TODO: retrigger on map select reload, i.e after completing a level
        for map in self.maps:
            AddBadgesToMap(map, GetConfig().demo_dir)

        # return true if successfully loaded maps. not sure if this is 
        #   intuitive or not though rn
        if len(self.maps) > 0:
            return True
        return False

def GetMapsSelectController() -> MapsSelectService:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = MapsSelectService()
    return _SINGLETON
