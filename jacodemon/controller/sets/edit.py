from jacodemon.config import JacodemonConfig, GetConfig
import jacodemon.ui.sets.edit as edit
from jacodemon.model.maps import MapSet

from jacodemon.ui.sets.edit import EditSetDialog
from PySide6.QtWidgets import QDialog

_SINGLETON = None

class EditSetController:
    def __init__(self) -> None:
        if _SINGLETON is not None:
            raise Exception("EditSetController MUST only be instantiated once")
        super().__init__()

    def NewEdit(self, parent, mapSetId):
        mapSet: MapSet = GetConfig().GetMapSetById(mapSetId)
        mapSetCopy = mapSet.Copy()
        dialog = EditSetDialog(parent, mapSetCopy)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            mapSet.name = dialog.mapSet.name
            mapSet.paths = dialog.mapSet.paths

    # only modify the copy
    def Toggle(self, dialog, path, state):
        for p in dialog.mapSet.paths:
            if p.path == path:
                p.enabled = state
        return

def GetEditSetController() -> EditSetController:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = EditSetController()
    return _SINGLETON