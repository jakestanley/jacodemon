import logging

from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.service.event_service import EventService, Event
from jacodemon.service.map_set_service import MapSetService

from jacodemon.model.map import MapSet

from jacodemon.view.components.config.sets import SetsTab

class ControllerSets(QObject):

    accept_signal = Signal()

    def __init__(self, view: SetsTab):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self.view: SetsTab = view

        self.map_set_service: MapSetService = Registry.get(MapSetService)

        # connect to signals
        Registry.get(EventService).connect(Event.MAPSETS_UPDATED, self.on_mapsets_updated)

        # do stuff if handle add is clicked, probably call the model, etc. 
        #   unsure about file dialog/ui in between yet
        self.view.new_button.clicked.connect(self.on_new_mapset)

        self.view.mapSetList.openItemRequested.connect(self.on_open_mapset)
        self.view.mapSetList.editItemRequested.connect(self.on_edit_mapset)
        self.view.mapSetList.removeItemRequested.connect(self.on_remove_mapset)

    def on_new_mapset(self):
        self.map_set_service.CreateMapSet()

    def on_open_mapset(self, mapSetId: str):
        self._logger.debug(f"Controller hit! Opening {mapSetId}")
        self.map_set_service.SetMapSet(mapSetId)
        self.accept_signal.emit()

    def on_edit_mapset(self, mapSetId: str):
        self._logger.debug(f"Controller hit! Editing {mapSetId}")

    def on_remove_mapset(self, mapSetId: str):
        self.map_set_service.RemoveMapSetById(mapSetId)

    def on_mapsets_updated(self):
        self.view.mapSetList.populate(reversed(self.map_set_service.mapSets))
