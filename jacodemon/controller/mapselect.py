from jacodemon.model.app import AppModel
from jacodemon.ui.view.mapselect import ViewMapSelect

class ControllerMapSelect():

    # TODO: mapset change signal

    def __init__(self, app_model: AppModel, view_map_select: ViewMapSelect):
        self.app_model = app_model
        self.view = view_map_select

        # self.view.mapTableWidget.index_selected.connect(self._HandleSelection)

        # self.view.mapOverviewWidget.play_signal.connect(self._HandlePlay)
        # self.view.mapOverviewWidget.play_demo_signal.connect(self._HandlePlayDemo)

        self.app_model.selected_mapset_update.connect(self.update)

        # TODO on view accept (play)

        self.update()

    def update(self):
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
