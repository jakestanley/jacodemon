from lib.py.wad import *

import csv

required_header_names = ['Season','Ranking','Title','Author','Notes','DoomWiki','IWAD','Files','Port','Merge','CompLevel']

def VerifyModListCsvHeader(reader):
    for required in required_header_names:
        if not required in reader.fieldnames:
            print(f"""
    Error: Missing required column '{required}' in header.
    Header contained '{reader.fieldnames}'
            """)
            exit(1)
    return reader;

def GetMaps(mod_list, pwad_dir):
    if(mod_list):
        try:
            _csv = open(mod_list)
        except FileNotFoundError:
            print(f"""
    Error: Could not find file 
        '{mod_list}'
            """)
            exit(1)
        verified = VerifyModListCsvHeader(csv.DictReader(_csv))
        return GetMapsFromModList(verified, pwad_dir)
    else:
        return []