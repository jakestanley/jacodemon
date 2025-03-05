from PySide6.QtCore import QObject

from jacodemon.service.registry import Registry
from jacodemon.service.map_service import MapService
from jacodemon.service.stats_service import StatsService

from jacodemon.model.map import Map

from jacodemon.view.components.mapselect.statistics import StatisticsTableView

class ControllerStatisticsTable(QObject):

    def __init__(self, view: StatisticsTableView):
        super().__init__()
        self.view = view

        # services
        self.map_service: MapService = Registry.get(MapService)
        self.stats_service: StatsService = Registry.get(StatsService)

        # service event listeners
        self.map_service.selected_map_updated.connect(self.on_map_updated)

        # ui events
        self.view.statistics_selected.connect(self._HandleSelectDemo)

    def on_map_updated(self, map: Map):
        if map is None:
            self.view.Update([])
            return

        self.view.Update(map.Statistics)

    def _HandleSelectDemo(self, index):
        self.stats_service.SetStatistics(index)
