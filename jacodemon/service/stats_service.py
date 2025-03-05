import glob
import json

from PySide6.QtCore import QObject, Signal

from jacodemon.misc.files import ParseTimestampFromPath

from jacodemon.model.map import Map
from jacodemon.model.launch import LaunchSpec
from jacodemon.model.stats import Statistics
import os
import logging

class StatsService(QObject):

    # when a user selects stats from the list
    selected_statistics_updated = Signal()

    def __init__(self, stats_dir):
        super().__init__()

        self._logger = logging.getLogger(self.__class__.__name__)
        self.stats_dir = stats_dir

    def initialise(self):
        pass

    def SetStatistics(self, index):

        self.selected_statistics = self.selected_map.Statistics[index]
        self.selected_statistics_updated.emit()

    # TODO rename this to get statistics for map? idk
    def LoadStatistics(self, stats_path) -> Statistics:

        # TODO persistence service for this
        stats = None
        if stats_path:
            with open(stats_path, "r") as stats_file:
                try:
                    raw_json = json.load(stats_file)
                except json.JSONDecodeError as e:
                    self._logger.error(f"Failed to parse stats: {stats_file}")
                    return None
                stats = Statistics.from_dict(raw_json)
                if stats.timestamp is None:
                    stats.timestamp = ParseTimestampFromPath(stats_path)

        return stats

    """
    Badges:
    - bronze: finished, 
    - silver: all kills, 
    - gold: above + all secrets and items
    """
    def AddStatsToMap(self, map: Map):
        prefix = map.GetPrefix()
        stats_files = glob.glob(self.stats_dir + f"/{prefix}*-STATS.json")

        if stats_files:
            for stats_file in stats_files:
                # hard coded ignore for demos/stats named test, i have loads
                if stats_file.find("test") >= 0:
                    continue
                stats = self.LoadStatistics(stats_file)
                if stats:
                    map.Statistics.append(stats)

        for stats in map.Statistics:
            new_badge = stats.get_badge()
            if new_badge > map.Badge:
                map.Badge = new_badge

    def Save(self, statistics: Statistics):
        
        stats_path = f"{self.stats_dir}/{statistics.launch_spec.name}-STATS.json"
        with open(stats_path, "w") as stats_file:
            stats_file.write(json.dumps(statistics.to_dict(), indent=2))
