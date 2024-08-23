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

def GetMapEntriesFromFiles(files: List[str], maps_dir = None):

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

import struct

def read_wad_file(file_path):
    with open(file_path, 'rb') as f:
        # Read the header
        wad_type = f.read(4).decode('ascii')  # "IWAD" or "PWAD"
        num_lumps = struct.unpack('<I', f.read(4))[0]  # Number of lumps
        directory_offset = struct.unpack('<I', f.read(4))[0]  # Offset to directory

        # Read the directory
        f.seek(directory_offset)
        directory = []
        for _ in range(num_lumps):
            offset = struct.unpack('<I', f.read(4))[0]
            size = struct.unpack('<I', f.read(4))[0]
            name = f.read(8).decode('ascii').rstrip('\x00')  # Read the lump name
            directory.append({'offset': offset, 'size': size, 'name': name})

        print(f'{"Name":<8} {"Offset":<8} {"Size":<8}')
        print('-' * 30)
        for entry in directory:
            print(f"{entry['name']:<8} {entry['offset']:<8} {entry['size']:<8}")
            
        # Optionally, read the lumps data
        lumps_data = {}
        for entry in directory:
            f.seek(entry['offset'])
            lumps_data[entry['name']] = f.read(entry['size'])

        return directory

def read_specific_lump(file_path, lump_name, directory):
    with open(file_path, 'rb') as f:
        # Find the lump in the directory
        for entry in directory:
            if entry['name'] == lump_name:
                f.seek(entry['offset'])
                lump_data = f.read(entry['size'])
                return lump_data

    # If the lump name is not found, return None
    print(f"Lump '{lump_name}' not found in the WAD file.")
    return None



# TODO this does not belong in this repo. too much of it is from chatgpt
if __name__ == '__main__':
    import sys
    # Usage example
    wad_file_path = '/Users/jake/Dropbox/Games/Doom/WADs/Maps/d2isov2/D2ISOv2.wad'
    directory = read_wad_file(wad_file_path)

    # attempt to find maps
    mapentries = []
    for entry in directory:
        if re.match('(E\dM\d|MAP\d\d)', entry['name']):
            mapentries.append(entry)

    # Read specific lump by name
    lump_name = 'ZMAPINFO'
    lump_data = read_specific_lump(wad_file_path, lump_name, directory)

    if lump_data is not None:
        print(f"Read {len(lump_data)} bytes from lump '{lump_name}'")
    else:
        print("Lump data could not be read.")
    sys.exit(0)
