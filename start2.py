#!/usr/bin/env python3

import copy
import subprocess

import lib.py.arguments as args
from lib.py.config import Config, LoadConfig
from lib.py.csv import csv_is_valid, load_raw_maps
from lib.py.last import *
from lib.py.launch import LaunchConfig
from lib.py.obs import *
from lib.py.options import Options
from lib.py.stats import Statistics, NewStatistics
from lib.py.ui.demoselect import OpenDemoSelection
from lib.py.ui.mapselect import OpenMapSelection
from lib.py.ui.options import OpenOptionsGui
from lib.py.ui.config import OpenConfigDialog
from lib.py.wad import GetMapEntriesFromFiles
from lib.py.demo import GetDemosForMap, AddBadgesToMap
from lib.py.macros import Macros, GetMacros
from lib.py.notifications import Notifications, GetNotifications

options: Options = args.get_args()
config: Config = LoadConfig()

# if last selected, skip the gui
if not options.last():
    OpenConfigDialog(config)
    config.Save()

    OpenOptionsGui(options)

notifications: Notifications = GetNotifications()
launch = LaunchConfig(options, config)

obsController = ObsController(options.obs, config, notifications)
obsController.Setup()

obsController.SetScene(config.wait_scene)

map = None
if options.last():
    map = GetLastMap()

if not map:

    if not os.path.exists(options.playlist):
        print(f"Could not find playlist file: {options.playlist}")
        sys.exit(1)

    if not csv_is_valid(options.playlist):
        print("CSV header is invalid. See output")
        sys.exit(1)

    raw_maps = load_raw_maps(options.playlist)
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

    for map in maps:
        AddBadgesToMap(map, config.demo_dir)

    if options.random():
        import random
        map = random.choice(maps)
    else:
        map = OpenMapSelection(maps)

if not map:
    print("A map was not selected. Exiting normally")
    sys.exit(0)

if options.replay():
    demos = GetDemosForMap(map, config.demo_dir)
    demo = OpenDemoSelection(demos)
    if not demo:
        print("A demo was not selected. Exiting normally")
        sys.exit(0)
elif not options.random():
    SaveSelectedMap(map)

launch.set_map(map)

if options.replay():
    demo_name = demo.name
    launch.set_replay(demo.path)
else:
    demo_name = launch.get_demo_name()

command = launch.get_command()

obsController.SetScene(config.play_scene)
obsController.UpdateMapTitle(f"{map.ModName}: {map.GetTitle()}")
obsController.SetDemoName(demo_name)

macros: Macros = GetMacros(obsController)

if options.auto_record:
    obsController.StartRecording()

if not options.replay():
    statistics: Statistics = NewStatistics(launch, config.demo_dir)

print(f"Running command\n\t{command}")
running = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# update stats and save
if not options.replay():
    statistics.set_level_stats()
    statistics.write_stats()

if options.auto_record:
    obsController.StopRecording()

obsController.SetScene(config.wait_scene)
