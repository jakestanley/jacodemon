#!/usr/bin/env python3

import subprocess
import sys

import lib.py.arguments as args
from lib.py.config import *
from lib.py.launch import LaunchConfig
from lib.py.obs import *
from lib.py.ui.mapselect import OpenMapSelection
from lib.py.ui.options import OpenOptionsGui
from lib.py.last import *
from lib.py.stats import Statistics
from lib.py.csv import csv_is_valid, load_raw_maps
from lib.py.wad import GetMapEntriesFromFiles
import copy

p_args = args.get_args()

config = LoadConfig(p_args.config)

if not p_args.no_gui:
    p_args = OpenOptionsGui(p_args)

launch = LaunchConfig(config)
launch.set_record_demo(not p_args.no_demo)

obsController = ObsController(not p_args.no_obs)
obsController.Setup()

obsController.SetScene("Waiting")

map = None
if p_args.last:
    map = GetLastMap()

if not map:

    if not os.path.exists(p_args.mod_list):
        print(f"Could not find playlist file: {p_args.mod_list}")
        sys.exit(1)

    if not csv_is_valid(p_args.mod_list):
        print("CSV header is invalid. See output")
        sys.exit(1)

    raw_maps = load_raw_maps(p_args.mod_list)
    maps = []
    for map in raw_maps:
        map.ProcessFiles(config.pwad_dir)

        # if there isn't a MapId, we need to look up the maps
        if not map.MapId:
            mapentries = GetMapEntriesFromFiles(map.GetFiles(), config.pwad_dir)
            for mapentry in mapentries:
                enriched_map = copy.deepcopy(map)
                enriched_map.SetMapId(mapentry["MapId"])
                enriched_map.SetMapName(mapentry["MapName"])
                maps.append(enriched_map)
        else:
            maps.append(map)

    if p_args.random:
        import random
        map = random.choice(maps)
    else:
        map = OpenMapSelection(maps)
        SaveSelectedMap(map)

        # TODO consider implementing this??? consider implementing saving all command line args as config
        # SaveSelectedModList(p_args.mod_list)

if not map:
    print("A map was not selected. Exiting normally")
    sys.exit(0)

launch.set_map(map)
demo_name = launch.get_demo_name()
command = launch.get_command()

obsController.SetScene('Playing')
obsController.UpdateMapTitle(f"{map.ModName}: {map.GetTitle()}")
if p_args.auto_record:
    obsController.StartRecording()

statistics = Statistics(launch, config.demo_dir)
print(f"Running command\n\t{command}")
running = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# update stats and save
statistics.set_level_stats()
statistics.write_stats()

if p_args.auto_record:
    obsController.StopRecording(demo_name)

# TODO setting for waiting scene
obsController.SetScene('Waiting')
