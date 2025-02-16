from jacodemon.config import JacodemonConfig, GetConfig
import jacodemon.ui.sets.edit as edit
from jacodemon.model.maps import MapSet

from jacodemon.ui.sets.edit import EditSetDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt


class EditSetController:
    def __init__(self) -> None:
        super().__init__()

    def NewEdit(self, parent, mapSetId):
        mapSet: MapSet = GetConfig().GetMapSetById(mapSetId)
        dialog = EditSetDialog(parent, mapSet)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:

            # TODO reload button, in case you messed up the complevel and want to re-import it or summat
            mapSet.compLevel = dialog.comp_level_line_edit.text()
            mapSet.iwad = dialog.iwad_line_edit.text()
            mapSet.paths = dialog.GetPaths()
            # TODO check saved
