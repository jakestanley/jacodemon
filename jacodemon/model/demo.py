import glob
import json
import os

from itertools import groupby

import jacodemon.model.demo_constants as DemoConstants

from jacodemon.map import FlatMap
from jacodemon.stats import Statistics, LoadStatistics

class Demo:
    def __init__(self, lump_path, stats_path=None):
        self.path = lump_path
        self.name, _ = os.path.splitext(os.path.basename(lump_path))
        self.stats: Statistics = None
        if stats_path:
            self.stats = LoadStatistics(self.name, stats_path)
                

    def Dictify(self):
        dic = {}

        dic[DemoConstants.KEY_LUMP] = self.path
        dic[DemoConstants.KEY_TIMESTAMP] = 'N/A'
        dic[DemoConstants.KEY_TIME] = 'N/A'
        dic[DemoConstants.KEY_KILLS] = 'N/A'
        dic[DemoConstants.KEY_ITEMS]  ='N/A'
        dic[DemoConstants.KEY_SECRETS] = 'N/A'

        if self.stats:
            dic[DemoConstants.KEY_TIMESTAMP] = self.stats.get_timestamp()
            dic[DemoConstants.KEY_TIME] = self.stats.get_time()
            dic[DemoConstants.KEY_KILLS] = self.stats.get_kills()
            dic[DemoConstants.KEY_ITEMS] = self.stats.get_items()
            dic[DemoConstants.KEY_SECRETS] = self.stats.get_secrets()

        return dic

# Function to extract the common part before the suffixes
def extract_prefix(filename):
    for suffix in ("-STATS.json", ".lmp"):
        if filename.endswith(suffix):
            return filename.rsplit(suffix, 1)[0]
    return filename

"""
Badges:
- bronze: finished, 
- silver: all kills, 
- gold: above + all secrets and items
"""
def AddBadgesToMap(map: FlatMap, demo_dir):

    prefix = map.GetMapPrefix()
    stats_files = glob.glob(demo_dir + f"/{prefix}*-STATS.json")

    if stats_files:
        for stats_file in stats_files:
            # hard coded ignore for demos/stats named test, i have loads
            if stats_file.find("test") >= 0:
                continue
            stats = LoadStatistics(None, stats_file)
            new_badge = stats.get_badge()
            if new_badge > map.Badge:
                map.Badge = new_badge

def GetDemosForMap(map: FlatMap, demo_dir):

    demos = []

    prefix = map.GetMapPrefix()
    files = glob.glob(demo_dir + f"/{prefix}*")

    # Sort the filenames list to group similar combinations together
    files.sort(key=extract_prefix)

    # Group filenames by the common part before the suffixes
    groups = {key: list(group) for key, group 
              in groupby(files, key=extract_prefix)}
    
    for _, group in groups.items():
        demo_files = sorted(group, key=lambda x: x.endswith("-STATS.json"))
        if len(demo_files) > 1:
            demos.append(Demo(demo_files[0], demo_files[1]))
        elif len(demo_files) > 0:
            if demo_files[0].endswith(".lmp"):
                demos.append(Demo(demo_files[0]))

    return demos