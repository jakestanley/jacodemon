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

        # self.view.mapOverviewWidget.play_signal.connect(self._HandlePlay)
        # self.view.mapOverviewWidget.play_demo_signal.connect(self._HandlePlayDemo)

        self.app_model.selected_mapset_updated.connect(self.on_mapset_updated)
        self.app_model.selected_map_updated.connect(self.on_map_updated)

    def on_mapset_updated(self):

        # TODO you may wish to reset demo, map, etc etc
        maps = [map.to_dict() for map in self.app_model.maps]
        self.view.mapTableWidget.populate(maps)

    def _HandleSelection(self, index):
        self.app_model.SetMap(index)

# def OpenSelectMapDialog() -> str:
#     """Returns MapId of the selected map or None"""

#     # at this point a map set and its maps MUST have been loaded
#     table_rows = [map.to_dict() for map in GetMapsSelectController().maps]
#     dialog = ViewMapSelect(table_rows, GetMapsSelectController().mapSet)

#     if dialog.exec() == QDialog.DialogCode.Rejected:
#         # clear the selected map set
#         GetMapsSelectController().mapSet = None

#         return None, None

#     if dialog.selectedIndex is None:
#         return None, None
#     else:
#         map = GetMapsSelectController().maps[dialog.selectedIndex]
#         if dialog.selectedDemo is not None:
#             return map, dialog.selectedDemo
#         return map, None
        pass

    def on_map_updated(self):
        pass

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.arguments import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewMapSelect()
    
    controller = ControllerMapSelect(app_model, view)
    view.show()
    sys.exit(app.exec())
