import json
import os
import re

from jacodemon.launch import LaunchConfig
from jacodemon.logs import GetLogManager

# constants
LEVELSTAT_TXT = "./levelstat.txt"
_KEY_TIMESTAMP = 'timestamp'
_KEY_COMP_LEVEL = 'compLevel'
_KEY_SOURCE_PORT = 'sourcePort'
_KEY_ARGS = 'args'
_KEY_LEVEL_STATS = 'levelStats'

def ParseLevelStats(rawLevelStats):

    levelStats = {}
    levelStats['Time'] = "???"
    levelStats['Kills'] = "???"
    levelStats['Secrets'] = "???"
    levelStats['Items'] = "???"

    regex_time = '(\d+:\d+\.\d+)'
    mtch = re.search(regex_time, rawLevelStats)
    if re.search(regex_time, rawLevelStats):
        levelStats['Time'] = re.search(regex_time, rawLevelStats).group(1)

    regex_kills = 'K: (\d+\/\d+)'
    if re.search(regex_kills, rawLevelStats):
        levelStats["Kills"] = re.search(regex_kills, rawLevelStats).group(1)

    regex_secrets = 'S: (\d+\/\d+)'
    if re.search(regex_secrets, rawLevelStats):
        levelStats["Secrets"] = re.search(regex_secrets, rawLevelStats).group(1)

    regex_items = 'I: (\d+\/\d+)'
    if re.search(regex_items, rawLevelStats):
        levelStats["Items"] = re.search(regex_items, rawLevelStats).group(1)

    return levelStats

class Statistics:

    def __init__(self, timestamp, comp_level, sourcePort, 
                 command, demo_name, demo_dir=None, levelStats=None):

        self._stats = {}
        # TODO stop using a `dict`, rather use dictify
        self.timestamp = timestamp
        self.comp_level = comp_level
        self._stats[_KEY_SOURCE_PORT]   = sourcePort
        self._stats[_KEY_ARGS]       = command
        self._stats[_KEY_LEVEL_STATS]   = levelStats
        self._demo_name = demo_name
        self._demo_dir = demo_dir
        self._logger = GetLogManager().GetLogger(__name__)

    def has_level_stats(self):
        if self._stats.get(_KEY_LEVEL_STATS):
            return True
        else:
            return False
        
    def get_timestamp(self):
        if self._stats:
            return self._stats.get(_KEY_TIMESTAMP)
        return None

    def get_time(self):
        if self._stats[_KEY_LEVEL_STATS]:
            return self._stats[_KEY_LEVEL_STATS]['Time']
        return "N/A"
    
    def get_kills(self):
        if self._stats[_KEY_LEVEL_STATS]:
            return self._stats[_KEY_LEVEL_STATS]['Kills']
        return "N/A"
    
    def get_items(self):
        if self._stats[_KEY_LEVEL_STATS]:
            return self._stats[_KEY_LEVEL_STATS]['Items']
        return "N/A"
    
    def get_secrets(self):
        if self._stats[_KEY_LEVEL_STATS]:
            return self._stats[_KEY_LEVEL_STATS]['Secrets']
        return "N/A"
    
    def get_badge(self) -> int:
        badge = 0
        if self._stats[_KEY_LEVEL_STATS]:
            badge += 1
            kills = self._stats[_KEY_LEVEL_STATS]['Kills'].split('/')
            items = self._stats[_KEY_LEVEL_STATS]['Items'].split('/')
            secrets = self._stats[_KEY_LEVEL_STATS]['Secrets'].split('/')
            if kills[0] == kills[1]:
                badge += 1
            if secrets[0] == secrets[1] and items[0] == items[1]:
                badge += 1
        return badge

    def set_level_stats(self):
        if os.path.exists(LEVELSTAT_TXT):
            with(open(LEVELSTAT_TXT)) as raw_level_stats:
                if not os.path.exists("./tmp"):
                    os.mkdir("./tmp")
                self._stats['levelStats'] = ParseLevelStats(raw_level_stats.read())
                archived_level_stat_txt = f"./tmp/levelstat_{self._demo_name}.txt"
            raw_level_stats.close()
            os.rename(LEVELSTAT_TXT, archived_level_stat_txt)
        else:
            self._logger.info("No levelstat.txt found. I assume you didn't finish the level or aren't using dsda-doom")

    def write_stats(self):
        stats_json_path = os.path.join(self._demo_dir, self._demo_name + "-STATS.json")
        with(open(stats_json_path, 'w')) as j:
            json.dump(self._stats, j)

def NewStatistics(launch: LaunchConfig, demo_dir: str) -> Statistics:
    
    os.remove(LEVELSTAT_TXT)
    statistics = Statistics(launch.timestamp, launch.get_comp_level(), 
                            launch.get_port(), launch.get_command(), 
                            launch.get_demo_name(), demo_dir)

    return statistics

def LoadStatistics(demo_name, stats_path) -> Statistics:

    if stats_path:
        with open(stats_path, "r") as stats_file:
            raw_json = json.load(stats_file)
            statistics = Statistics(raw_json.get(_KEY_TIMESTAMP), 
                                    raw_json.get(_KEY_COMP_LEVEL),
                                    raw_json.get(_KEY_SOURCE_PORT),
                                    raw_json.get(_KEY_ARGS),
                                    demo_name, None, 
                                    raw_json.get(_KEY_LEVEL_STATS))
    else:
        statistics = Statistics(None, None, None, None, demo_name)
        
    return statistics
