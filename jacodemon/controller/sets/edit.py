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
        dialog = EditSetDialog(parent, mapSet)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:

            model = dialog.tableView.model()
            row_count = model.rowCount()
            column_count = model.columnCount()

            for row in range(row_count):
                for column in range(column_count):
                    item = model.item(row, column)
                    print(item.text())

            mapSet.name = dialog.mapSet.name
            mapSet.paths = dialog.mapSet.paths

def GetEditSetController() -> EditSetController:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = EditSetController()
    return _SINGLETON