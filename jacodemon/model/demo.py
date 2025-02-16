import glob
import json
import os

from itertools import groupby

import jacodemon.model.demo_constants as DemoConstants

from jacodemon.model.flatmap import FlatMap
from jacodemon.service.dsda.stats import Statistics, LoadStatistics

class Demo:
    def __init__(self, lump_path, stats_path=None):
        self.path = lump_path
        self.name, _ = os.path.splitext(os.path.basename(lump_path))
        self.stats: Statistics = LoadStatistics(self.name, stats_path)            

    def to_dict(self):
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
