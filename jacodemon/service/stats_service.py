import glob

from jacodemon.model.map import Map
from jacodemon.model.statistics import Statistics

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

class StatsService:
    def __init__(self, stats_dir):
        self.stats_dir = stats_dir
        pass

    """
    Badges:
    - bronze: finished, 
    - silver: all kills, 
    - gold: above + all secrets and items
    """
    def AddBadgesToMap(self, map: Map):
        prefix = map.GetMapPrefix()
        stats_files = glob.glob(self.stats_dir + f"/{prefix}*-STATS.json")

        if stats_files:
            for stats_file in stats_files:
                # hard coded ignore for demos/stats named test, i have loads
                if stats_file.find("test") >= 0:
                    continue
                stats = LoadStatistics(None, stats_file)
                new_badge = stats.get_badge()
                if new_badge > map.Badge:
                    map.Badge = new_badge
