import os
import sys
import copy
from typing import List
from jacodemon.wad import GetMapEntriesFromFiles

class FlatMap:
    def __init__(self, ModName, Files, MapId=None, MapName=None, Author=None, 
                 CompLevel=None, Merges: str = "", Port=None, 
                 Notes=None):

        # public, required
        self.ModName = ModName

        # public, optional
        self.MapId = MapId
        self.Port = Port
        self.CompLevel = CompLevel

        # private, required
        self._Files = Files.split('|')

        # private, optional
        self._MapName = MapName
        self._Author = Author
        self._Merges = Merges.split('|')
        
        self._Notes = Notes
        self.Badge = 0

        # set files
        self.dehs = []
        self.patches = []
        self.merges = []

    def SetMapId(self, MapId: str):
        if self.MapId:
            print(f"Warning: setting MapId: '{MapId}' on a map that already has a MapId ('{self.MapId}')")

        self.MapId = MapId

    def SetMapName(self, MapName: str):
        self._MapName = MapName

    def SetAuthor(self, Author: str):
        self._Author = Author

    """
    Populate DEHs, patches and merges based on the patch directory
    Jury's still out on whether or not this should be done in the constructor
    """
    def ProcessFiles(self, maps_dir: str):

        # build lists of map specific files we need to pass in
        patches = [patch for patch in self._Files if patch]
        for patch in patches:
            ext = os.path.splitext(patch)[1]
            path = os.path.join(maps_dir, patch)
            if ext.lower() == ".deh":
                self.dehs.append(path)
            elif ext.lower() == ".wad":
                self.patches.append(path)
            else:
                print(f"Ignoring unsupported file "'{patch}'"with extension '{ext}'")

        # for chocolate doom/vanilla wad merge emulation
        merges = [merge for merge in self._Merges if merge]
        for merge in merges:
            self.merges.append(os.path.join(maps_dir, merge))

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
        if self._MapName:
            return self._MapName
        return self.MapId

    def Dictify(self):
        dic = {}

        dic['Badge'] = ''
        if self.Badge == 1:
            dic['Badge'] = '🥉'
        elif self.Badge == 2:
            dic['Badge'] = '🥈'
        elif self.Badge == 3:
            dic['Badge'] = '🥇'

        dic['ModName'] = self.ModName
        dic['MapId'] = self.MapId
        dic['MapName'] = self._MapName
        dic['Author'] = self._Author
        dic['CompLevel'] = self.CompLevel
        dic['Files'] = ", ".join(self._Files)
        dic['Merge'] = ",".join(self._Merges)
        dic['Port'] = self.Port
        dic['Notes'] = self._Notes

        return dic

def EnrichMaps(config, raw_maps):

    enriched_maps = []

    for map in raw_maps:
        map.ProcessFiles(config.maps_dir)

        # if there isn't a MapId, we need to look up the maps
        if not map.MapId:
            mapentries = GetMapEntriesFromFiles(map.GetFiles(), config.maps_dir)
            for mapentry in mapentries:
                enriched_map = copy.deepcopy(map)
                enriched_map.SetMapId(mapentry["MapId"])
                enriched_map.SetMapName(mapentry["MapName"])
                enriched_maps.append(enriched_map)
        else:
            enriched_maps.append(map)

    return enriched_maps
