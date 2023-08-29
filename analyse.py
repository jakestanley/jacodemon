#!/usr/bin/env python3
import json
import glob

import lib.py.arguments as args
import lib.py.logs as logs
from lib.py.options import Options
from lib.py.config import Config, LoadConfig
from lib.py.map import FlatMap, EnrichMaps
from lib.py.csv import load_raw_maps
from lib.py.demo import AddBadgesToMap

options: Options = args.get_analyse_args()
config: Config = LoadConfig(options.config)

# set up logging now that we have arguments
logs.configure()
logs.InitLogManager(options)
logger = logs.GetLogManager().GetLogger(__name__)
logger.info("Starting application...")

# TODO update analyse for V3
raw_maps = load_raw_maps(options.playlist)
maps = EnrichMaps(config, raw_maps)

for map in maps:
    AddBadgesToMap(map, config.demo_dir)

for map in maps:
    map: FlatMap = map
    pfx = map.GetMapPrefix()
    files = glob.glob(config.demo_dir + f"/{pfx}*")
    stats = []
    lumps = []
    for file in files:
        if file.endswith('STATS.json'):
            stats.append(file)
        elif file.endswith('.lmp'):
            lumps.append(file)

    for stat in stats:
        statfile = json.load(open(stat))
        if statfile['levelStats']:
            levelStats = statfile['levelStats']
            print("has levelStats")

    print("go")
