from typing import List

from jacodemon.model.mapset import MapSet

from jacodemon.model.map import Map
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

        # TODO re-introduce caching if you want
        return self.LoadMapsFromMapSet(mapSet)
