from PySide6.QtCore import QObject

from jacodemon.model.app import AppModel

from jacodemon.view.components.mapselect.statistics import StatisticsTableView

class ControllerStatisticsTable(QObject):

    def __init__(self, app_model: AppModel, view: StatisticsTableView):
        super().__init__()
        self.app_model = app_model
        self.view = view

        self.app_model.selected_map_updated.connect(self.on_map_updated)
        self.view.statistics_selected.connect(self._HandleSelectDemo)

    def on_map_updated(self):
        if self.app_model.selected_map is None:
            self.view.Update([])
            return

        self.view.Update(self.app_model.selected_map.Statistics)

    def _HandleSelectDemo(self, index):
        self.app_model.SetStatistics(index)
