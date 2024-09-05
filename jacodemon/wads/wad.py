import os
import re
import subprocess

from typing import List
from omg import wad as omgwad
from jacodemon.wads.lumps.umapinfo import parse_umapinfo
from jacodemon.wads.lumps.gameinfo import parse_gameinfo
from jacodemon.wads.lumps.complevel import parse_complevel
from jacodemon.wads.lumps.zmapinfo import parse_zmapinfo

def EnrichMapsFromUmapinfo(maps, umapinfo):
    for map in maps:
        mapId = map['MapId']
        if mapId in umapinfo:
            if 'MapName' not in map or map['MapName'] is None:
                map['MapName'] = umapinfo[mapId].get('levelname')
            if 'ParTime' not in map or map['ParTime'] is None:
                map['ParTime'] = umapinfo[mapId].get('partime')
            if 'NextSecretMap' not in map or map['NextSecretMap'] is None:
                map['NextSecretMap'] = umapinfo[mapId].get('nextsecret')
            if 'Author' not in map or map['Author'] is None:
                map['Author'] = umapinfo[mapId].get('author')
            if 'NextMap' not in map or map['NextMap'] is None:
                map['NextMap'] = umapinfo[mapId].get('next')

def EnrichMapsFromZmapinfo(maps, zmapinfo):
    for map in maps:
        mapId = map['MapId']
        if mapId in zmapinfo:
            if 'MapName' not in map or map['MapName'] is None:
                map['MapName'] = zmapinfo[mapId].get('levelname')

# TODO don't do this every freakin time unless you click refresh
def GetMapEntriesFromWad(file) -> List[dict]:
    if not os.path.exists(file):
        raise Exception(f"WAD {file} not found")
        
    maps = []

    wad = omgwad.WAD(file)

    # get the basic list of maps
    maps.extend([{"MapId": string} for string in wad.maps.keys()])

    # try and get more info
    if "UMAPINFO" in wad.data:
        umapinfo = parse_umapinfo(wad.data['UMAPINFO'].data)
        EnrichMapsFromUmapinfo(maps, umapinfo)

    if "ZMAPINFO" in wad.data:
        zmapinfo = parse_zmapinfo(wad.data['ZMAPINFO'].data)
        EnrichMapsFromZmapinfo(maps, zmapinfo)

    return maps

def GetMapEntriesFromFiles(files: List[str], maps_dir = None) -> List[dict]:

    # TODO UMAPINFO support
    maps = []

    for file in files:
        
        ext = os.path.splitext(file)[1]
        # TODO: .pk3 handling
        if ext.lower() == ".wad":
            if os.path.exists(file):
                final_path = file
            else:
                final_path = os.path.join(maps_dir, file)
            maps.extend(GetMapEntriesFromWad(final_path))
        else:
            continue

    return sorted(maps, key=lambda x: x['MapId'])

def GetInfoFromWad(file) -> dict:

    if not os.path.exists(file):
        raise Exception(f"WAD {file} not found")

    wad = omgwad.WAD(file)

    gameinfo = {}

    if "GAMEINFO" in wad.data:
        gameinfo.update(parse_gameinfo(wad.data['GAMEINFO'].data))
    
    if "COMPLVL" in wad.data:
        gameinfo.update(parse_complevel(wad.data['COMPLVL'].data))
    
    # WADINFO may be necessary if a TXT file is not present
    if "WADINFO" in wad.data:
        gameinfo.update({'wadinfo': wad.data['WADINFO'].data})

    return gameinfo

def GetInfoFromFiles(files: List[str], maps_dir = None) -> dict:

    gameinfo = {}

    for file in files:

        ext = os.path.splitext(file)[1]
        if ext.lower() == ".wad":
            if os.path.exists(file):
                final_path = file
            else:
                final_path = os.path.join(maps_dir, file)
            gameinfo.update(GetInfoFromWad(final_path))

    return gameinfo

if __name__ == '__main__':
    import sys

    path = "tests/data/thirdparty/eviternity2.wad"
    entries = GetMapEntriesFromFiles([path])
    gameinfo = GetInfoFromWad(path)

    # stick a breakpoint here if you need it
    sys.exit(0)
