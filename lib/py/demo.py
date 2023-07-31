import glob
import json
import os

from itertools import groupby

from lib.py.map import FlatMap

class Demo:
    def __init__(self, lump_path, stats_path=None):
        self.path = lump_path
        self.name, _ = os.path.splitext(os.path.basename(lump_path))
        self.stats = None
        if stats_path:
            with(open(stats_path)) as f:
                self.stats = json.load(f)

    def Dictify(self):
        dic = {}

        dic['Lump'] = self.path
        if self.stats:
            dic['Stats'] = self.stats
        else:
            dic['Stats'] = 'No stats available'

        return dic

# Function to extract the common part before the suffixes
def extract_prefix(filename):
    for suffix in ("-STATS.json", ".lmp"):
        if filename.endswith(suffix):
            return filename.rsplit(suffix, 1)[0]
    return filename


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