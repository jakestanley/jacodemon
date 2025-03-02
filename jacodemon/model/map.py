import os
import sys
import copy
from typing import List

from jacodemon.model.mapset import MapSet

class Map:

    # TODO set CompLevel at mod level, not map level. Why would maps in a WAD have different comp levels? Seems unlikely...
    def __init__(self, MapId):

        self.MapId              = MapId
        self.MapName            = None
        self.ParTime            = None
        self.NextMapId          = None
        self.NextSecretMapId    = None
        self.Author             = None
        self.Statistics         = []
        self.Badge              = 0
        self.MapSetId           = None

        # TODO: do not persist
        self.MapSet: MapSet     = None

    """
    Get map prefix (used for naming demos and recordings) based on Files or 
    Merges, and MapId
    """
    def GetPrefix(self) -> str:
        
        if not self.MapSet:
            raise Exception("Error: Could not get a prefix as there was no MapSet set")

        mod_prefix = self.MapSet.GetMapSetPrefix()

        if self.MapId:
            return f"{mod_prefix}-{self.MapId}"
        else:
            raise Exception("Error: Could not get a prefix as there was no MapId set")

    def GetFiles(self) -> List[str]:
        return self._Files
    
    def GetTitle(self):

        mapTitle = self.MapId
        if self.MapName:
            mapTitle = self.MapName

        return f"{self.MapSet.name} - {mapTitle}"

    def SetMapSet(self, mapSet: MapSet):

        # if we save last map, we'll want to save the mapset id for reference
        self.MapSetId = mapSet.id
        self.MapSet = mapSet

    # TODO put this in the controller
    def to_dict(self):
        dic = {}

        dic['Badge'] = ''
        if self.Badge == 1:
            dic['Badge'] = '🥉'
        elif self.Badge == 2:
            dic['Badge'] = '🥈'
        elif self.Badge == 3:
            dic['Badge'] = '🥇'

        dic['MapId'] = self.MapId
        dic['MapName'] = self.MapName
        dic['Author'] = self.Author
        dic['ParTime'] = self.ParTime
        dic['NextMapId'] = self.NextMapId
        dic['NextSecretMapId'] = self.NextSecretMapId
        dic['Author'] = self.Author

        return dic
