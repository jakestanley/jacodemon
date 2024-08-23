import os
import re
import subprocess
from typing import List

regex_mapentries = '\t(E\dM\d|MAP\d\d)'
regex_lumps = '\t(UMAPINFO|MAPINFO)'
DOOM_regex = r'^E(\d)M(\d)$'
DOOM2_regex = r'^MAP(\d+)$'

def IsValidWadPath(path):
    return os.path.isfile(path)

def IsDoom1(mapId):
    return re.match(DOOM_regex, mapId)

def IsDoom2(mapId):
    return re.match(DOOM2_regex, mapId)

def GetDoom1Warp(mapId):
    episodeno = (re.match(DOOM_regex, mapId).group(1))
    mapno = (re.match(DOOM_regex, mapId).group(2))
    return [episodeno, mapno]

def GetDoom2Warp(mapId):
    map = re.match(DOOM2_regex, mapId).group(1)
    return [f"{int(map)}"]

def GetMapEntriesFromFiles(files: List[str], maps_dir):

    # TODO UMAPINFO support
    maps = []

    for file in files:
        ext = os.path.splitext(file)[1]
        if ext.lower() == ".wad":
            if os.path.exists(file):
                final_path = file
            else:
                final_path = os.path.join(maps_dir, file)
            wadls = f"wad-ls {final_path}"
            output = subprocess.check_output(wadls, shell=True, universal_newlines=True)
            lumps = list(set(re.findall(regex_lumps, output)))
            mapentries = list(set(re.findall(regex_mapentries, output)))
            if "MAPINFO" in lumps:
                wadread = f"wad-read {final_path} MAPINFO"
                output = subprocess.check_output(wadread, shell=True, universal_newlines=True)
                mapentries = re.findall("(E\dM\d|MAP\d\d) \"(.*)\"", output)
                for mapentry in mapentries:
                    map = {}
                    map['MapId'] = mapentry[0]
                    map['MapName'] = mapentry[1]
                    maps.append(map)
            else:
                mapentries.sort()
                for mapentry in mapentries:
                    map = {}
                    map['MapId'] = mapentry
                    map['MapName'] = ""
                    maps.append(map)

    return maps
