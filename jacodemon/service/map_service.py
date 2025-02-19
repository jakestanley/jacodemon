import os
import json
import jsonpickle

from typing import Optional
from typing import List

from jacodemon.model.mapset import MapSet

from jacodemon.model.map import Map
from jacodemon.service.wad_service import WadService

from jacodemon.service.maps.cache import LoadMapsFromCache, AddMapsToCache

_LAST_JSON = "./last.json"

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
    
    def LoadLastMap(self) -> Optional[Map]:

        if os.path.exists(_LAST_JSON):
            with(open(_LAST_JSON)) as f:

                # pickle will only return a decoded instance if a type 
                #   matching the type under "py/object" exists
                unpickled = jsonpickle.decode(json.load(f))

                # the persisted map set may be stale, so we must clear it
                unpickled.MapSet = None
                return unpickled
        else:
            print("Cannot select last map as '{LAST_JSON}' was not found")
            return None

    def SaveLastMap(self, map: Map):
        # saves selected map for last
        with open(_LAST_JSON, 'w') as f:
            pickled = jsonpickle.encode(map, max_depth=1)
            json.dump(pickled, f)
