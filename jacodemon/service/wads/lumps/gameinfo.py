import csv
from io import StringIO

def parse_gameinfo(data):

    raw_gameinfo = {}
    lines = data.decode('utf-8').replace('\r\n', '\n').split('\n')

    for line in [line for line in lines if len(line) > 0]:
        key = line.split("=")[0].strip()
        raw_values = line.split("=")[1].strip()
        f = StringIO(raw_values)
        reader = csv.reader(f)
        values = next(reader)
        
        raw_gameinfo[key] = values

    gameinfo = {}
    
    if 'STARTUPTITLE' in raw_gameinfo:
        gameinfo['Title'] = raw_gameinfo['STARTUPTITLE'][0]

    if 'IWAD' in raw_gameinfo:
        gameinfo['IWAD'] = raw_gameinfo['IWAD'][0]

    return gameinfo