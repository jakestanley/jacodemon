from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.stats_service import StatsService

from jacodemon.model.app import AppModel
from jacodemon.model.map import Map
from jacodemon.model.stats import Statistics

from jacodemon.view.components.mapselect.map_overview import MapOverviewWidget

from jacodemon.controller.components.mapselect.statistics import ControllerStatisticsTable

class ControllerMapOverview(QObject):

    play_signal = Signal()
    play_demo_signal = Signal()

    def __init__(self, app_model: AppModel, view: MapOverviewWidget):
        super().__init__()
        self.app_model = app_model
        self.view = view

        # services
        self.stats_service: StatsService = Registry.get(StatsService)

        # service event listeners
        event_service: EventService = Registry.get(EventService)
        event_service.connect(Event.SELECTED_MAP_UPDATED, self.on_map_updated)
        event_service.connect(Event.SELECTED_STATS_UPDATED, self.on_statistics_updated)

        # i'm sure this was deffo getting GC'd without the assignment.
        #   perhaps these nested controller declarations might get a little unwieldy? we'll see
        self._cDemoTable = ControllerStatisticsTable(self.view.demo_table)

        self.view.play_button.setEnabled(False)
        self.view.play_demo_button.setEnabled(False)

        # ui event listeners
        self.view.play_button.clicked.connect(self._HandlePlay)
        self.view.play_demo_button.clicked.connect(self._HandlePlayDemo)



    def on_map_updated(self, map: Map):

        self.view.play_demo_button.setEnabled(False)
        if map is not None:
            self.view.play_button.setEnabled(True)

    def on_statistics_updated(self, stats: Statistics):

        if stats:
            self.view.play_demo_button.setEnabled(True)
        else:
            self.view.play_demo_button.setEnabled(False)

    def _HandlePlay(self):
        self.play_signal.emit()

    def on_demo_updated(self):
        enabled = self.app_model.selected_demo is not None
        self.view.play_demo_button.setEnabled(enabled)

    def _HandlePlayDemo(self):
        self.play_demo_signal.emit()

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = MapOverviewWidget(None)
    view.resize(800, 600)
    
    controller = ControllerMapOverview(app_model, view)
    view.show()
    app.exec()
