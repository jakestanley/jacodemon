#!/usr/bin/env python3

import copy
import subprocess

import lib.py.arguments as args
from lib.py.config import Config, LoadConfig
from lib.py.csv import csv_is_valid, load_raw_maps
from lib.py.last import *
from lib.py.launch import LaunchConfig
from lib.py.obs import *
from lib.py.stats import Statistics
from lib.py.ui.mapselect import OpenMapSelection
from lib.py.ui.options import OpenOptionsGui
from lib.py.ui.config import OpenConfigDialog
from lib.py.wad import GetMapEntriesFromFiles

p_args = args.get_args()

config: Config = LoadConfig()
OpenConfigDialog(config)
config.Save()

if not p_args.no_gui:
    p_args = OpenOptionsGui(p_args)

launch = LaunchConfig(config)
launch.no_mods = p_args.no_mods
launch.record_demo = not p_args.no_demo

obsController = ObsController(not p_args.no_obs)
obsController.Setup()

obsController.SetScene("Waiting")

map = None
if p_args.last:
    map = GetLastMap()

if not map:

    if not os.path.exists(p_args.playlist):
        print(f"Could not find playlist file: {p_args.playlist}")
        sys.exit(1)

    if not csv_is_valid(p_args.playlist):
        print("CSV header is invalid. See output")
        sys.exit(1)

    raw_maps = load_raw_maps(p_args.playlist)
    maps = []
    for map in raw_maps:
        map.ProcessFiles(config.maps_dir)

        # if there isn't a MapId, we need to look up the maps
        if not map.MapId:
            mapentries = GetMapEntriesFromFiles(map.GetFiles(), config.maps_dir)
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

if not map:
    print("A map was not selected. Exiting normally")
    sys.exit(0)

launch.set_map(map)
demo_name = launch.get_demo_name()
command = launch.get_command()

obsController.SetScene(config.play_scene)
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

obsController.SetScene(config.wait_scene)
