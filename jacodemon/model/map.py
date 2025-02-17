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
        self.Badge              = 0

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
        if self.MapName:
            return self.MapName
        return self.MapId

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
