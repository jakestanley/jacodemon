import json
import os
import re

from jacodemon.model.launch import LaunchConfig
from jacodemon.logs import GetLogManager

LEVELSTAT_TXT = "./levelstat.txt"

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

# TODO bin, make these part of the app model? idk
def NewStatistics(launch: LaunchConfig, demo_dir: str) -> Statistics:
    
    if os.path.exists(LEVELSTAT_TXT):
        os.remove(LEVELSTAT_TXT)
    statistics = Statistics(launch.timestamp, launch.get_comp_level(), 
                            "dsda-doom", launch.get_command(), 
                            launch.get_demo_name(), demo_dir)

    return statistics
