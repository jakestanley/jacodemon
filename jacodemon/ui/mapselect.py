from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout, QTableView


from jacodemon.controller.maps.select import MapsSelectController, GetMapsSelectController
from jacodemon.model.maps import MapSet, MapSetPath
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QBrush


_COLUMN_ORDER = ['MapId', 'Badge', 'MapName', 'Author', 'Notes']

class MapTableWidget(QTableView):
    index_selected = Signal(int)

    def __init__(self, data, parent):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.setModel(self.model)

        # Create table headers based on keys in the first dictionary
        self.model.setHorizontalHeaderLabels(_COLUMN_ORDER)

        for row_dict in data:
            row_items = [QStandardItem(str(row_dict[key])) for key in _COLUMN_ORDER]
            for item in row_items:
                item.setEditable(False)  # Set the item as uneditable
            self.model.appendRow(row_items)

        self.doubleClicked.connect(self.handle_double_click)
        self.resizeColumnsToContents()

    def handle_double_click(self, index):
        self.index_selected.emit(index.row())
        self.close()  # Close the window

class PathsTableWidget(QTableView):

    def __init__(self, paths: list[MapSetPath], parent):
        super().__init__(parent)

        self.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        self.model = QStandardItemModel()
        self.setModel(self.model)

        for path in paths:
            item = QStandardItem(path.path)
            if not path.enabled:
                item.setForeground(QBrush(Qt.gray))
            self.model.appendRow(item)

        self.resizeColumnsToContents()


class MapOverviewWidget(QWidget):
    
    def __init__(self, mapSet: MapSet, parent):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel(f"Map Set: {mapSet.name}"))
        layout.addWidget(PathsTableWidget(mapSet.paths, self))
        layout.addWidget(QLabel(f"Port: {mapSet.port}"))
        layout.addWidget(QLabel(f"CompLevel: {mapSet.compLevel}"))
        layout.addStretch()
        self.setLayout(layout)

class _SelectMapDialog(QDialog):

    close_dialog = Signal(int)

    def __init__(self, maps: dict, mapSet: MapSet):
        super().__init__()

        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        layout = QHBoxLayout(self)

        layout.addWidget(MapOverviewWidget(mapSet, self))

        self.mapTableWidget = MapTableWidget(maps, self)
        layout.addWidget(self.mapTableWidget)
        self.setLayout(layout)

        self.close_dialog.connect(self._HandleClose)

    def _HandleClose(self, action):
        if action == QDialog.DialogCode.Accepted:
            self.accept()

def OpenMapSelection():

    # at this point a map set and its maps MUST have been loaded
    table_rows = [map.Dictify() for map in GetMapsSelectController().maps]
    dialog = _SelectMapDialog(table_rows, GetMapsSelectController().mapSet)

    rs = dialog.exec()
    # TODO return to previous window on reject
    return rs
