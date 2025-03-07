from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog

from jacodemon.service.registry import Registry
from jacodemon.service.map_service import MapService
from jacodemon.service.options_service import OptionsService

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

    def __init__(self, view_config: ViewConfig):
        super().__init__()
        self.view = view_config

        # services
        self.map_service: MapService = Registry.get(MapService)
        self.options_service: OptionsService = Registry.get(OptionsService)

        # create views and controllers for tabs
        self.cSets = ControllerSets(self.view.selectSetTab)
        self.cGeneral = ControllerGeneral(self.view.generalTab)
        self.cMods = ControllerMods(self.view.modsTab)
        self.cObs = ControllerObs(self.view.obsTab)
        self.cDsda = ControllerDsda(self.view.dsdaTab)

        self.cSets.accept_signal.connect(self.accept_signal.emit)
        self.view.lastWidget.last_signal.connect(self.on_play_last)

        # TODO use an event for this? do an initial load and then an event listener
        if self.map_service.last_map is not None:
            self.view.lastWidget.last_map_set_name.setText(f"Mod: {self.map_service.last_map.MapSet.name}")
            self.view.lastWidget.last_map_map_id.setText(f"Map: {self.map_service.last_map.MapId}")
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
        # TODO needs updating post event/remove app model gubbins
        self.app_model.SetMapSet(self.app_model.last_map.MapSet.id)
        self.app_model.SetMapByMapId(self.app_model.last_map.MapId)
        self.options_service.SetPlayMode()
        self.last_signal.emit()

if __name__ == "__main__":

    import gc
    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.model.options import InitialiseOptions


    gc.disable()

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    view = ViewConfig()
    
    controller = ControllerConfig(app_model, view)
    view.show()
    sys.exit(app.exec())
