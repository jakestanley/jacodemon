#!/usr/bin/env python3

import copy
import subprocess

import lib.py.arguments as args
import lib.py.logs as logs
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
from lib.py.io import IO, GetIo
from lib.py.scenes import SceneManager
from lib.py.keys import *

options: Options = args.get_args()

# set up logging now that we have arguments
logs.configure()
lman = logs.LogManager(options)

logger = lman.GetLogger(__name__)
logger.info("Starting application...")

config: Config = LoadConfig()

# if last selected, skip the gui
if not options.last():
    OpenConfigDialog(config)
    config.Save()

    OpenOptionsGui(options)

logger = lman.GetLogger(__name__)

notifications: Notifications = GetNotifications(lman)
io: IO = GetIo(lman)
launch = LaunchConfig(options, config)

if options.obs:
    obsController = ObsController(config, notifications, io, lman)
else:
    obsController = NoObsController(notifications, lman)

obsController.Setup()
sceneManager = SceneManager(obsController, config)

obsController.SetScene(config.wait_scene)

map = None
if options.last():
    map = GetLastMap()

if not map:

    if not os.path.exists(options.playlist):
        logger.critical(f"Could not find playlist file: {options.playlist}")
        sys.exit(1)

    if not csv_is_valid(options.playlist):
        logger.critical("CSV header is invalid. See output")
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
    logger.info("A map was not selected. Exiting normally")
    sys.exit(0)

if options.replay():
    demos = GetDemosForMap(map, config.demo_dir)
    demo = OpenDemoSelection(demos)
    if not demo:
        logger.info("A demo was not selected. Exiting normally")
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

macros: Macros = GetMacros()
# TODO move this to configuration somehow
macros.add_hotkey_callback(KEY_NUMPAD_0, callback=obsController.SaveReplay)
macros.add_hotkey_callback(KEY_DOT, callback=obsController.CancelRecording)
macros.add_hotkey_callback(KEY_DEL, callback=obsController.CancelRecording)
macros.add_hotkey_callback(KEY_NUMPAD_3, callback=sceneManager.SwitchToBrowserScene)
macros.listen()

if options.auto_record:
    obsController.StartRecording()

if not options.replay():
    statistics: Statistics = NewStatistics(launch, config.demo_dir)

logger.debug(f"Running command: {' '.join(command)}")
running = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# update stats and save
if not options.replay():
    statistics.set_level_stats()
    statistics.write_stats()

if options.auto_record:
    obsController.StopRecording()

obsController.SetScene(config.wait_scene)
