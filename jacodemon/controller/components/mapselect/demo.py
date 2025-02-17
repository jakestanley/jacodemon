from PySide6.QtCore import QObject, Signal

from jacodemon.model.app import AppModel

from jacodemon.view.components.mapselect.demo import DemoTableView

class ControllerDemoTable(QObject):

    def __init__(self, app_model: AppModel, view: DemoTableView):
        super().__init__()
        self.app_model = app_model
        self.view = view

        self.app_model.selected_map_updated.connect(self.on_map_updated)
        self.view.demo_selected.connect(self._HandleSelectDemo)

    def on_map_updated(self):
        pass

    def _HandleSelectDemo(self, index):
        if index == -1:
            self._selected_demo = None
            self.view.play_demo_button.setEnabled(False)
        else:
            self._selected_demo = index
            self.view.play_demo_button.setEnabled(True)
