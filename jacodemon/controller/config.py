from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog

from jacodemon.model.app import AppModel
from jacodemon.view.config import ViewConfig

from jacodemon.controller.components.config.sets import ControllerSets
from jacodemon.controller.components.config.general import ControllerGeneral
from jacodemon.controller.components.config.mods import ControllerMods
from jacodemon.controller.components.config.obs import ControllerObs
from jacodemon.controller.components.config.dsda import ControllerDsda

class ControllerConfig(QObject):

    accept_signal = Signal()
    reject_signal = Signal()
    last_signal = Signal()

    def __init__(self, app_model: AppModel, view_config: ViewConfig):
        super().__init__()

        self.app_model = app_model
        self.view = view_config

        # create views and controllers for tabs
        self.cSets = ControllerSets(app_model, self.view.selectSetTab)
        self.cGeneral = ControllerGeneral(app_model, self.view.generalTab)
        self.cMods = ControllerMods(app_model, self.view.modsTab)
        self.cObs = ControllerObs(app_model, self.view.obsTab)
        self.cDsda = ControllerDsda(app_model, self.view.dsdaTab)

        self.cSets.accept_signal.connect(self.accept_signal.emit)
        self.view.lastWidget.last_signal.connect(self.on_play_last)

        if self.app_model.last_map is not None:
            self.view.lastWidget.last_map_set_name.setText(f"Mod: {self.app_model.last_map.MapSet.name}")
            self.view.lastWidget.last_map_map_id.setText(f"Map: {self.app_model.last_map.MapId}")
            self.view.lastWidget.play_last_button.setEnabled(True)
        else:
            self.view.lastWidget.play_last_button.setEnabled(False)

        self.view.configTabWidget.currentChanged.connect(self.update)

    def update(self):
        self.cGeneral.update()
        self.cMods.update()
        self.cObs.update()
        self.cDsda.update()

    def on_play_last(self):
        self.app_model.SetMapSet(self.app_model.last_map.MapSet.id)
        self.app_model.SetMapByMapId(self.app_model.last_map.MapId)
        self.app_model.SetPlayMode()
        self.last_signal.emit()

if __name__ == "__main__":

    import gc
    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    gc.disable()

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewConfig()
    
    controller = ControllerConfig(app_model, view)
    view.show()
    sys.exit(app.exec())
