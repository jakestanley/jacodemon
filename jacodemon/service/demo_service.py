import glob

from jacodemon.misc.files import ParseTimestampFromPath

from jacodemon.model.stats import Statistics
from jacodemon.model.map import Map

class DemoService:
    def __init__(self, demo_dir):
        self.demo_dir = demo_dir

    def AddDemoesToMapStats(self, map: Map):

        demos = {}

        prefix = map.GetPrefix()
        files = glob.glob(self.demo_dir + f"/{prefix}*.lmp")

        for file in files:
            timestamp = ParseTimestampFromPath(file)
            if not timestamp:
                continue

            demos[timestamp] = file

        # this adds a demo to existing stats if there are stats for it
        for stats in map.Statistics:
            if stats.timestamp in demos:
                stats.demo = demos[stats.timestamp]
                demos.pop(stats.timestamp)

        # this creates empty statistics for any demos that don't have stats,
        #   i.e failed attempts
        for timestamp in demos:
            map.Statistics.append(Statistics(demo=demos[timestamp]))

        return
