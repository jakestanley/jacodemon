

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
def AddBadgesToMap(self, map: FlatMap):

    prefix = map.GetMapPrefix()
    stats_files = glob.glob(stats_dir + f"/{prefix}*-STATS.json")

    if stats_files:
        for stats_file in stats_files:
            # hard coded ignore for demos/stats named test, i have loads
            if stats_file.find("test") >= 0:
                continue
            stats = LoadStatistics(None, stats_file)
            new_badge = stats.get_badge()
            if new_badge > map.Badge:
                map.Badge = new_badge