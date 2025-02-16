from typing import List

from jacodemon.logs import LogManager, GetLogManager
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from jacodemon.model.flatmap import FlatMap, EnrichMaps, GetMapEntriesFromFiles
from jacodemon.model.demo import GetDemosForMap, AddBadgesToMap
from jacodemon.service.maps.cache import LoadMapsFromCache, AddMapsToCache

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

class MapService:

    def __init__(self) -> None:
        pass

    def LoadMaps(self, mapSet: MapSet) -> List[FlatMap]:

        logger = GetLogManager().GetLogger(__name__)

        # TODO: if files change, evict cache
        # self.maps = LoadMapsFromCache(mapSet.id)
        
        # if self.maps:
            # logger.info(f"Loaded {len(self.maps)} maps from cache")
            # return
        
        logger.info("Cache miss. Loading maps from scratch")

        raw_maps = LoadRawMapsFromMapSet(mapSet)
        enriched_maps = EnrichMaps(raw_maps)
        # AddMapsToCache(mapSet.id, enriched_maps)

        [AddBadgesToMap(map) for map in enriched_maps]

        return enriched_maps

    # def Open(self, mapSetId):

    #     GetConfig().TouchMapSet(mapSetId)

    #     self.LoadMaps(mapSetId)
    #     # TODO: retrigger on map select reload, i.e after completing a level
    #     for map in self.maps:
    #         AddBadgesToMap(map, GetConfig().demo_dir)

    #     # return true if successfully loaded maps. not sure if this is 
    #     #   intuitive or not though rn
    #     if len(self.maps) > 0:
    #         return True
    #     return False

