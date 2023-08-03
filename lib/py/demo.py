import glob
import json
import os

from itertools import groupby

from lib.py.map import FlatMap
from lib.py.stats import Statistics, LoadStatistics

class Demo:
    def __init__(self, lump_path, stats_path=None):
        self.path = lump_path
        self.name, _ = os.path.splitext(os.path.basename(lump_path))
        self.stats: Statistics = None
        if stats_path:
            self.stats = LoadStatistics(self.name, stats_path)
                

    def Dictify(self):
        dic = {}

        dic['Lump'] = self.path
        dic['Time'] = 'N/A'
        dic['Kills'] = 'N/A'
        dic['Items'] = 'N/A'
        dic['Secrets'] = 'N/A'

        if self.stats:
            dic['Time'] = self.stats.get_time()
            dic['Kills'] = self.stats.get_kills()
            dic['Items'] = self.stats.get_items()
            dic['Secrets'] = self.stats.get_secrets()

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