from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.map_service import MapService
from jacodemon.service.map_set_service import MapSetService
from jacodemon.service.options_service import OptionsService

from jacodemon.view.config import ViewConfig
from jacodemon.model.map import Map

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
        self.map_set_service: MapSetService = Registry.get(MapSetService)
        self.options_service: OptionsService = Registry.get(OptionsService)

        # event listeners
        Registry.get(EventService).connect(Event.LAST_MAP_UPDATED, self.update_last_map)

        # create views and controllers for tabs
        self.cSets = ControllerSets(self.view.selectSetTab)
        self.cGeneral = ControllerGeneral(self.view.generalTab)
        self.cMods = ControllerMods(self.view.modsTab)
        self.cObs = ControllerObs(self.view.obsTab)
        self.cDsda = ControllerDsda(self.view.dsdaTab)

        self.cSets.accept_signal.connect(self.accept_signal.emit)
        self.view.lastWidget.last_signal.connect(self.on_play_last)

        # initial last map load
        self.view.configTabWidget.currentChanged.connect(self.update)

    def update_last_map(self, map: Map):

        if map is not None:
            self.view.lastWidget.last_map_set_name.setText(f"Mod: {map.MapSet.name}")
            self.view.lastWidget.last_map_map_id.setText(f"Map: {map.MapId}")
            self.view.lastWidget.play_last_button.setEnabled(True)
        else:
            self.view.lastWidget.play_last_button.setEnabled(False)

    def update(self):
        self.cGeneral.update()
        self.cMods.update()
        self.cObs.update()
        self.cDsda.update()

    def on_play_last(self):
        # TODO needs updating post event/remove app model gubbins
        map = self.map_service.last_map
        self.map_set_service.SetMapSet(map.MapSet.id)
        self.map_service.SetMapByMapId(map.MapId)
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
    
    controller = ControllerConfig(view)
    view.show()
    sys.exit(app.exec())
