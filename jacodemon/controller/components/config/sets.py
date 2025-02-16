from PySide6.QtCore import QObject, Signal

from jacodemon.model.app import AppModel

from jacodemon.view.components.config.sets import SetsTab

class ControllerSets(QObject):

    accept_signal = Signal()

    def __init__(self, app_model: AppModel, view: SetsTab):
        super().__init__()
        self.app_model: AppModel = app_model
        self.view: SetsTab = view

        # listen for changes to map sets
        self.app_model.mapsets_updated.connect(self.on_mapsets_updated)

        # do stuff if handle add is clicked, probably call the model, etc. 
        #   unsure about file dialog/ui in between yet
        self.view.add_button.clicked.connect(self.on_add_mapset)

        # do initial update
        self.on_mapsets_updated()

        # these are a fucking nightmare!!!
        self.view.mapSetList.openItemRequested.connect(self.on_open_mapset)
        self.view.mapSetList.editItemRequested.connect(self.on_edit_mapset)
        self.view.mapSetList.removeItemRequested.connect(self.on_remove_mapset)
    
        print("Right, I've definitely just set up those connections")

    def on_add_mapset(self):
        print( "Adding mapset")

    def on_open_mapset(self, mapSetId: str):
        print(f"Controller hit! Opening {mapSetId}")
        self.app_model.SetMapSet(mapSetId)
        self.accept_signal.emit()

    def on_edit_mapset(self, mapSetId: str):
        print(f"Controller hit! Editing {mapSetId}")

    def on_remove_mapset(self, mapSetId: str):
        print(f"Controller hit! Removing {mapSetId}")

    def on_mapsets_updated(self):

        # TODO: we always want to show the end of the list at the top cos 
        #   of how i do the crappy list thing i'm tired i should probbly slep
        self.view.mapSetList.populate(reversed(self.app_model.mapSets))
