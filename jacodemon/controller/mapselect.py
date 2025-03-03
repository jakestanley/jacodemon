from PySide6.QtCore import QObject, Signal

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

        # i'm sure this was deffo getting GC'd without the assignment
        self._cMapOverview = ControllerMapOverview(self.app_model, self.view.mapOverviewWidget)

        self.view.mapTableWidget.row_selected.connect(self._HandleSelection)

        self.app_model.selected_mapset_updated.connect(self.on_mapset_updated)

        self._cMapOverview.play_signal.connect(self.play)
        self._cMapOverview.play_demo_signal.connect(self.play_demo)

        self.view.button_box.accepted.connect(self.play)
        self.view.button_box.rejected.connect(self.reject_signal.emit)

    def play(self):
        self.app_model.SetPlayMode()
        self.accept_signal.emit()

    def play_demo(self):
        self.app_model.SetReplayMode()
        self.accept_signal.emit()

    def on_mapset_updated(self):

        # TODO you may wish to reset demo, map, etc etc
        maps = [map.to_dict() for map in self.app_model.maps]
        self.view.mapTableWidget.populate(maps, self.app_model.GetSelectedMapIndex())
        self.view.on_map_set_change(self.app_model.selected_map_set)

    def _HandleSelection(self, index):
        self.app_model.SetMap(index)

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
