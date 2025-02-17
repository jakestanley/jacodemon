import glob
import json

from jacodemon.model.map import Map
from jacodemon.model.stats import Statistics

class StatsService:
    def __init__(self, stats_dir):
        self.stats_dir = stats_dir
        pass

    # TODO rename this to get statistics for map? idk
    def LoadStatistics(self, stats_path) -> Statistics:

        # TODO persistence service for this
        if stats_path:
            with open(stats_path, "r") as stats_file:
                raw_json = json.load(stats_file)
                return Statistics.from_dict(raw_json)

        return None

    """
    Badges:
    - bronze: finished, 
    - silver: all kills, 
    - gold: above + all secrets and items
    """
    def AddBadgesToMap(self, map: Map):
        prefix = map.GetPrefix()
        stats_files = glob.glob(self.stats_dir + f"/{prefix}*-STATS.json")

        if stats_files:
            for stats_file in stats_files:
                # hard coded ignore for demos/stats named test, i have loads
                if stats_file.find("test") >= 0:
                    continue
                stats = self.LoadStatistics(stats_file)


                new_badge = stats.get_badge()
                if new_badge > map.Badge:
                    map.Badge = new_badge
