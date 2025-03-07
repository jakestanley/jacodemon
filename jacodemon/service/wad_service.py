import os
from pathlib import Path

from typing import List
from omg import wad as omgwad

from jacodemon.model.map import Map
from jacodemon.model.wad import WadsData

from jacodemon.service.wads.lumps.umapinfo import parse_umapinfo
from jacodemon.service.wads.lumps.gameinfo import parse_gameinfo
from jacodemon.service.wads.lumps.complevel import parse_complevel
from jacodemon.service.wads.lumps.zmapinfo import parse_zmapinfo

# TODO don't do this every freakin time unless you click refresh
def _GetMapEntriesFromWad(file) -> List[Map]:
    if not os.path.exists(file):
        raise Exception(f"WAD {file} not found")
        
    maps = []

    wad = omgwad.WAD(file)

    # get the basic list of maps
    maps.extend([Map(string) for string in wad.maps.keys()])

    # try and get more info
    if "UMAPINFO" in wad.data:
        umapinfo = parse_umapinfo(wad.data['UMAPINFO'].data)
        _EnrichMapsFromUmapinfo(maps, umapinfo)

    if "ZMAPINFO" in wad.data:
        zmapinfo = parse_zmapinfo(wad.data['ZMAPINFO'].data)
        _EnrichMapsFromZmapinfo(maps, zmapinfo)

    return maps

def _EnrichMapsFromUmapinfo(maps: List[Map], umapinfo):
    for map in maps:
        mapId = map.MapId
        if mapId in umapinfo:
            mapUmapinfo = umapinfo[mapId]

            # concisely populate from umapinfo and default to originals if not found
            map.MapName         = mapUmapinfo.get('levelname', map.MapName)
            map.ParTime         = mapUmapinfo.get('partime', map.ParTime)
            map.NextMapId       = mapUmapinfo.get('next', map.NextMapId)
            map.Author          = mapUmapinfo.get('author', map.Author)
            map.NextSecretMapId = mapUmapinfo.get('nextsecret', map.NextSecretMapId)

            # other interesting fields available are:
            # - episode
            # - intertext

def _EnrichMapsFromZmapinfo(maps: List[Map], zmapinfo):
    for map in maps:
        mapId = map.MapId
        if mapId in zmapinfo:
            mapZmapinfo = zmapinfo[mapId]

            # concisely populate from zmapinfo and default to originals if not found
            map.MapName         = mapZmapinfo.get('levelname', map.MapName)

class WadService:
    """
    WadService creates maps but adds info obtained from the WADs only.
    """

    def __init__(self, maps_dir):
        self.maps_dir = maps_dir

    def _GetWadPath(self, file: str):
        ext = os.path.splitext(file)[1]
        if ext.lower() == ".wad":
            if os.path.exists(file):
                return file
            else:
                return os.path.join(self.maps_dir, file)

        return None
    
    def GetTextFileContentsFromWadName(self, wad_path):
        path = Path(wad_path)

        # Search for a case-insensitive .txt file in the same directory
        for txt_file in path.parent.glob(f"{path.stem}.*"):
            if txt_file.suffix.lower() == ".txt":
                for encoding in ("utf-8", "latin-1", "windows-1252"):
                    try:
                        return txt_file.read_text(encoding=encoding)
                    except UnicodeDecodeError:
                        continue

        return None  # Return None if no matching file is found
    
    # TODO: user added data in MapSet to be added separately
    def GetDataFromWads(self, wads: List[str]) -> WadsData:

        # TODO cache me, possibly keyed on MapSetId
        data = WadsData()

        for file in wads:

            path = self._GetWadPath(file)
            if path:
                wad = omgwad.WAD(path)

                # case conversion on keys, it's not in the GAME/UMAPinfo standards
                if "GAMEINFO" in wad.data:
                    lump = parse_gameinfo(wad.data['GAMEINFO'].data)
                    data.title = lump.get('Title', data.title)
                    data.iwad = lump.get('IWAD', data.iwad)
                elif "gameinfo" in wad.data:
                    lump = parse_gameinfo(wad.data['gameinfo'].data)
                    data.title = lump.get('Title', data.title)
                    data.iwad = lump.get('IWAD', data.iwad)
                
                if "COMPLVL" in wad.data:
                    lump = parse_complevel(wad.data['COMPLVL'].data)
                    data.complevel = lump.get('complevel', data.complevel)
                elif "complevel" in wad.data:
                    lump = parse_complevel(wad.data['complevel'].data)
                    data.complevel = lump.get('complevel', data.complevel)

                if "CREDITS" in wad.data:
                    data.credits = wad.data['CREDITS'].data.decode('utf-8')
                elif "credits" in wad.data:
                    data.credits = wad.data['credits'].data.decode('utf-8')
                
                # WADINFO may be necessary if a TXT file is not present
                if "WADINFO" in wad.data:
                    data.text = wad.data['WADINFO'].data.decode('utf-8')
                elif "wadinfo" in wad.data:
                    data.text = wad.data['wadinfo'].data.decode('utf-8')
                else:
                    data.text = self.GetTextFileContentsFromWadName(file)

            else:
                continue

        return data

    def GetMapsFromWads(self, wads: List[str]) -> List[Map]:

        maps = []
        for file in wads:
            
            path = self._GetWadPath(file)
            if path:
                maps.extend(_GetMapEntriesFromWad(path))
            else:
                continue

        return sorted(maps, key=lambda x: x.MapId)

if __name__ == '__main__':

    import sys

    service = WadService("tests/data")
    path = "thirdparty/eviternity2.wad"

    maps = service.GetMapsFromWads([path])
    data = service.GetDataFromWads([path])

    # stick a breakpoint here if you need it
    sys.exit(0)
