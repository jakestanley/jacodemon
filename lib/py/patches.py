import os
import subprocess
import re

import lib.py.wad as wad
from lib.py.mod import *

regex_mapentries = '(E\dM\d|MAP\d\d|MAPINFO)'




def GetMod(mod, pwad_dir) -> Mod:
    dehs = []
    pwads = []
    mwads = []

    # build lists of map specific files we need to pass in
    patches = [patch for patch in mod['Files'].split('|') if patch]
    for patch in patches:
        ext = os.path.splitext(patch)[1]
        if ext.lower() == ".deh":
            dehs.append(f"{pwad_dir}/{patch}")
        elif ext.lower() == ".wad":
            pwads.append(f"{pwad_dir}/{patch}")
        else:
            print(f"Ignoring unsupported file "'{patch}'"with extension '{ext}'")

    # for chocolate doom/vanilla wad merge emulation
    merges = [merge for merge in mod['Merge'].split('|') if merge]
    for merge in merges:
        mwads.append(f"{pwad_dir}/{merge}")

    maps = wad.GetMapsForMod(mod, pwad_dir)
    iwad = mod['iwad']

    return Mod(iwad, dehs, pwads, mwads, maps)
