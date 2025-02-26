#!/usr/bin/env python3
import json
import glob

from typing import List
import jacodemon.arguments as args
import jacodemon.logs as logs
from jacodemon.model.options import Options
from jacodemon.model.config import JacodemonConfig, GetConfig
from jacodemon.model.map import Map, EnrichMaps
from jacodemon.csv import load_raw_maps
from jacodemon.model.demo import Demo, GetDemosForMap, AddBadgesToMap

class Badge:
    def __init__(self, rank, attempt, timestamp) -> None:
        self.rank: int = rank
        self.attempt: int = attempt
        self.timestamp: str = timestamp

    # if self is better than badge
    def isBetterThan(self, badge):
        if not badge:
            return True
        if self.rank > badge.rank:
            return True
        if self.rank == badge.rank:
            # TODO convert to int. remember we want to know if it was _faster_
            if self.timestamp != 'N/A':
                return True
            if self.timestamp < badge.timestamp:
                return True
        return False
    
    def serialize(self):
        dic = {}
        dic['rank'] = self.rank
        dic['attempt'] = self.attempt
        dic['timestamp'] = self.timestamp
        return dic

class MapReport:
    def __init__(self, map: Map) -> None:
        self.map = map
        self.best_badge = None
        self.badges: List[Badge] = []

    def add_badge(self, rank, attempt, timestamp):
        badge = Badge(rank, attempt, timestamp)
        if self.best_badge:
            if self.best_badge.isBetterThan(badge):
                pass
            else:
                self.best_badge = badge
                self.badges.append(badge)
        else:
            self.best_badge = badge
            self.badges.append(badge)

    def serialize(self):

        dic = {}
        dic['MapId'] = self.map.MapId
        dic['Author'] = self.map._Author
        dic['MapName'] = self.map._MapName
        dic['ModName'] = self.map.ModName

        badges = []
        for badge in self.badges:
            badges.append(badge.serialize())

        dic['badges'] = badges
        return dic
            

map_reports = []

options: Options = args.get_analyse_args()
config: JacodemonConfig = GetConfig()

# set up logging now that we have arguments
logs.configure()
logs.InitLogManager(options)
logger = logs.GetLogManager().GetLogger(__name__)
logger.info("Starting application...")

raw_maps = load_raw_maps(options.playlist)
maps = EnrichMaps(config, raw_maps)

for map in maps:
    demos = GetDemosForMap(map, config.demo_dir)
    map_report = MapReport(map)
    for attempts, item in enumerate([demo for demo in demos if demo.stats and demo.stats.has_level_stats()]):
        demo: Demo = item
        if demo.stats:
            map_report.add_badge(demo.stats.get_badge(), attempts+1, demo.stats.get_time())

    map_reports.append(map_report)

with open("report.json", 'w', encoding="utf-8") as f:
    serialized = []
    for map_report in map_reports:
        serialized.append(map_report.serialize())
    json.dump(serialized, f, ensure_ascii=False, indent=4)

logger.info("Analysis complete")