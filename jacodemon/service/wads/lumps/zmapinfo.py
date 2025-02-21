import re

def parse_zmapinfo(data):
    """For now only reads map names"""

    lines = data.decode('utf-8').replace('\r\n', '\n').split('\n')
    maps = {}

    for line in lines:
        matches = re.match(r'^map\s+MAP(\S+)\s+"(.*)"', line)
        if matches:
            mapId = f"MAP{matches.groups()[0]}"
            maps[mapId] = {}
            maps[mapId]['levelname'] = matches.groups()[1]
            continue

        matches = re.match(r'^map\s+E(\S+)M(\S+)\s+"(.*)"', line)
        if matches:
            mapId = f"E{matches.groups()[0]}M{matches.groups()[1]}"
            maps[mapId] = {}
            maps[mapId]['levelname'] = matches.groups()[2]
            continue

    return maps

if __name__ == '__main__':
    data = b'\r\n\r\nmap MAP06 "Rite" {'
    data = parse_zmapinfo(data)