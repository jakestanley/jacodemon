from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.options_service import OptionsService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.map_service import MapService

from jacodemon.view.mapselect import ViewMapSelect

from jacodemon.controller.components.mapselect.map_overview import ControllerMapOverview

class ControllerMapSelect(QObject):

    accept_signal = Signal()
    reject_signal = Signal()

    # TODO map select/demo select update, etc
    def __init__(self, view_map_select: ViewMapSelect):
        super().__init__()
        self.view = view_map_select

        # services
        self.options_service: OptionsService = Registry.get(OptionsService)
        self.map_set_service: MapSetService = Registry.get(MapSetService)
        self.map_service: MapService = Registry.get(MapService)

        # service event listeners
        event_service: EventService = Registry.get(EventService)
        event_service.connect(Event.MAPS_UPDATED, self.on_maps_updated)
        event_service.connect(Event.SELECTED_MAPSET_UPDATED, self.on_mapset_updated)

        # i'm sure this was deffo getting GC'd without the assignment
        self._cMapOverview = ControllerMapOverview(self.view.mapOverviewWidget)

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

    def on_mapset_updated(self, mapSet):
        self.view.on_map_set_change(mapSet)

    def _HandleSelection(self, index):

        # TODO don't use index it's crap
        self.map_service.SetSelectedMapByIndex(index)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.arguments import DummyArgs
    from jacodemon.model.options import InitialiseOptions

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    view = ViewMapSelect()
    
    controller = ControllerMapSelect(view)
    view.show()
    sys.exit(app.exec())
