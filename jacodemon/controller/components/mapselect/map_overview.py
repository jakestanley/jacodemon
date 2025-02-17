from PySide6.QtCore import QObject, Signal

from jacodemon.model.app import AppModel

from jacodemon.view.components.mapselect.map_overview import MapOverviewWidget

class ControllerMapOverview(QObject):

    play_signal = Signal()
    play_demo_signal = Signal()

    def __init__(self, app_model: AppModel, view: MapOverviewWidget):
        super().__init__()
        self.app_model = app_model
        self.view = view

        self.view.play_button.setEnabled(False)
        self.view.play_demo_button.setEnabled(False)

        self.view.play_button.clicked.connect(self._HandlePlay)
        self.view.demo_table.demo_selected.connect(self._HandleSelectDemo)
        self.view.play_demo_button.clicked.connect(self._HandlePlayDemo)

        self.app_model.selected_map_updated.connect(self.on_map_updated)

    def on_map_updated(self):

        if self.app_model.selected_map is not None:
            self.view.play_button.setEnabled(True)
            # self.view.demo_table.Update(self.app_model.selected_map)
        # TODO refresh
        # self.view._Update(self.app_model.GetLastMap())
        # self.view.play_button.setEnabled(True)
        # if map:
        #     self.play_button.setEnabled(True)
        #     self.demo_table.Update(map)
        # self.play_demo_button.setEnabled(False)
        # self._selected_demo = None


    def _HandlePlay(self):
        self._selected_demo = None
        self.play_signal.emit()

    def _HandleSelectDemo(self, index):
        if index == -1:
            self._selected_demo = None
            self.play_demo_button.setEnabled(False)
        else:
            self._selected_demo = index
            self.play_demo_button.setEnabled(True)

    def _HandlePlayDemo(self):
        if self._selected_demo is not None:
            self.play_demo_signal.emit()

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = MapOverviewWidget(None)
    view.resize(800, 600)
    
    controller = ControllerMapOverview(app_model, view)
    view.show()
    app.exec()
