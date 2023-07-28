import re

regex_warp = r'E(\d)M(\d)|MAP(\d{2})'

def get_warp(MapId: str):
    warp = []
    for group in re.match(regex_warp, MapId).groups():
        if group:
            # converts "01" to 1 then back to "1" cz i'm lazy
            warp.append(str(int(group)))

    return warp

def get_inferred_iwad(MapId: str):
    groups = re.match(regex_warp, MapId).groups()
    matches = []
    for group in groups:
        if group:
            matches.append(group)
    
    iwad = 'DOOM2.WAD'
    if len(matches) > 1:
        iwad = 'DOOM.WAD'

    return iwad