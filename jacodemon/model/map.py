import os
import sys
import copy
from typing import List

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

        # set files - are these used any more?
        self.dehs = []
        self.patches = []
        self.merges = []

    """
    Get map prefix (used for naming demos and recordings) based on Files or 
    Merges, and MapId
    """
    def GetMapPrefix(self) -> str:

        if len(self.patches) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self.patches[0]))[0]
        elif len(self.merges) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self.merges[0]))[0]
        elif len(self.dehs) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self.dehs[0]))[0]
        else:
            print("Error: Could not get a prefix as there were no files!")
            sys.exit(1)

        if self.MapId:
            return f"{mod_prefix}-{self.MapId}"
        else:
            print("Error: Could not get a prefix as there was no MapId set")
            sys.exit(1)

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
        dic['Badge'] = self.Badge

        return dic
