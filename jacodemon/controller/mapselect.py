from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.options_service import OptionsService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.map_service import MapService

from jacodemon.model.app import AppModel
from jacodemon.view.mapselect import ViewMapSelect

from jacodemon.controller.components.mapselect.map_overview import ControllerMapOverview

class ControllerMapSelect(QObject):

    accept_signal = Signal()
    reject_signal = Signal()

    # TODO map select/demo select update, etc
    def __init__(self, app_model: AppModel, view_map_select: ViewMapSelect):
        super().__init__()
        self.app_model = app_model
        self.view = view_map_select

        # services
        self.options_service: OptionsService = Registry.get(OptionsService)
        self.map_set_service: MapSetService = Registry.get(MapSetService)
        self.map_service: MapService = Registry.get(MapService)

        # service event listeners
        Registry.get(EventService).connect(Event.MAPS_UPDATED, self.on_maps_updated)

        # i'm sure this was deffo getting GC'd without the assignment
        self._cMapOverview = ControllerMapOverview(self.app_model, self.view.mapOverviewWidget)

        self.view.mapTableWidget.row_selected.connect(self._HandleSelection)

        self._cMapOverview.play_signal.connect(self.play)
        self._cMapOverview.play_demo_signal.connect(self.play_demo)

        self.view.button_box.accepted.connect(self.play)
        self.view.button_box.rejected.connect(self.reject_signal.emit)

    def play(self):
        self.options_service.SetPlayMode()
        self.accept_signal.emit()

    def play_demo(self):
        self.options_service.SetDemoMode()
        self.accept_signal.emit()

    # TODO can we use a list[Map] type in the signal?
    def on_maps_updated(self):

        # TODO you may wish to reset demo, map, etc etc
        maps = [map.to_dict() for map in self.map_service.maps]
        # self.view.mapTableWidget.populate(maps, self.app_model.GetSelectedMapIndex())
        self.view.mapTableWidget.populate(maps)
        self.view.on_map_set_change(self.map_set_service.selected_map_set)

    def _HandleSelection(self, index):

        # TODO don't use index it's crap
        self.map_service.SetSelectedMapByIndex(index)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.arguments import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewMapSelect()
    
    controller = ControllerMapSelect(app_model, view)
    view.show()
    sys.exit(app.exec())
