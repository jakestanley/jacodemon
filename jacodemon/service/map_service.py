from typing import List

from jacodemon.logs import LogManager, GetLogManager
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from jacodemon.model.map import Map, EnrichMaps, GetMapEntriesFromFiles
from jacodemon.service.wad_service import WadService
from jacodemon.service.maps.cache import LoadMapsFromCache, AddMapsToCache

class MapService:
    """
    There is a lot of overlap between WadService and MapService. 
    MapService handles caching, and may also add Jacodemon flavour.
    """

    def __init__(self, maps_dir) -> None:
        self.maps_dir = maps_dir
        self.wad_service = WadService(self.maps_dir)

    def LoadMapsFromMapSet(self, mapSet: MapSet) -> List[Map]:

        # read files in the map set and get map entries
        files = [path.path for path in mapSet.paths if path.enabled]
        return self.wad_service.GetMapsFromWads(files)

    def LoadMaps(self, mapSet: MapSet) -> List[Map]:

        logger = GetLogManager().GetLogger(__name__)

        # TODO: if files change, evict cache
        # self.maps = LoadMapsFromCache(mapSet.id)
        
        # if self.maps:
            # logger.info(f"Loaded {len(self.maps)} maps from cache")
            # return
        
        logger.info("Cache miss. Loading maps from scratch")

        raw_maps = LoadMapsFromMapSet(mapSet)
        enriched_maps = EnrichMaps(raw_maps)
        # AddMapsToCache(mapSet.id, enriched_maps)

        # [AddBadgesToMap(map) for map in enriched_maps]

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

