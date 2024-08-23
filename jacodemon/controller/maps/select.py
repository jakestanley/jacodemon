from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.maps import MapSet

from jacodemon.wad import GetMapEntriesFromFiles


_SINGLETON = None

class MapsSelectController:
    def __init__(self) -> None:
        if _SINGLETON is not None:
            raise Exception("MapsSelectController MUST only be instantiated once")
        super().__init__()

    def Open(self, parent, mapSetId):
        mapSet: MapSet = GetConfig().GetMapSetById(mapSetId)
        mapentries = GetMapEntriesFromFiles([path.path for path in mapSet.paths if path.enabled])

        return

def GetMapsSelectController() -> MapsSelectController:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = MapsSelectController()
    return _SINGLETON
