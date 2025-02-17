from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout, QTableView, QPushButton

from PySide6.QtWidgets import QLabel, QGroupBox
from PySide6.QtGui import QBrush

from jacodemon.view.components.mapselect.map_overview import MapOverviewWidget

_COLUMN_ORDER = ['MapId','Badge','MapName','Author','ParTime','NextMapId','NextSecretMapId']

class MapTableWidget(QTableView):

    row_selected = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setModel(self.model)

        # Create table headers based on keys in the first dictionary
        self.model.setHorizontalHeaderLabels(_COLUMN_ORDER)

        self.selectionModel().selectionChanged.connect(self._HandleSelection)
        self.resizeColumnsToContents()

    def populate(self, data):
        # TODO should replace, not append
        for row_dict in data:
            row_items = [QStandardItem(str(row_dict[key])) for key in _COLUMN_ORDER]
            for item in row_items:
                item.setEditable(False)  # Set the item as uneditable
            self.model.appendRow(row_items)
        self.resizeColumnsToContents()

    def _HandleSelection(self, selected, deselected):
        if len(selected.indexes()) == 0:
            self.row_selected.emit(-1)
            return
        for index in selected.indexes():
            # Only process the first column to avoid processing multiple columns per row click
            if index.column() == 0:
                row = index.row()
                self.row_selected.emit(row)

class PathsTableWidget(QTableView):

    def __init__(self, parent):
        super().__init__(parent)

        self.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.resizeColumnsToContents()

    def on_map_set_change(self, mapSet):

        paths = []
        
        if mapSet:
            paths = mapSet.paths
            mapSet.compLevel

        for path in paths:
            item = QStandardItem(path.path)
            if not path.enabled:
                item.setForeground(QBrush(Qt.gray))
            self.model.appendRow(item)
            
class SetOverviewWidget(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        
        paths = []
        compLevel = None

        layout.addWidget(PathsTableWidget(self))
        layout.addWidget(QLabel(f"CompLevel: {compLevel}"))
        layout.addStretch()
        self.setLayout(layout)

    def on_map_set_change(mapSet):
        if mapSet:
            paths = mapSet.paths
            mapSet.compLevel

class ViewMapSelect(QDialog):

    # TODO on map select, update me
    def __init__(self):
        super().__init__()

        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        self.selectedIndex = None
        self.selectedDemo = None

        # self.setWindowTitle(f"Select a map from {mapSet.name}")

        layout = QVBoxLayout(self)
        set_groupbox = self._CreateSetOverviewGroupBox()
        maps_groupbox = self._CreateMapsGroupBox()
        
        layout.addWidget(maps_groupbox)
        layout.addWidget(set_groupbox)
        
        self.setLayout(layout)

    def _CreateSetOverviewGroupBox(self) -> QGroupBox:
        gb_layout = QVBoxLayout()
        gb_layout.addWidget(SetOverviewWidget(self))

        set_groupbox = QGroupBox("Set")
        set_groupbox.setLayout(gb_layout)
        return set_groupbox
    
    def _CreateMapsGroupBox(self):
        gb_layout = QHBoxLayout()
        self.mapTableWidget = MapTableWidget(self)

        gb_layout.addWidget(self.mapTableWidget)

        self.mapOverviewWidget = MapOverviewWidget(self)
        gb_layout.addWidget(self.mapOverviewWidget)

        maps_groupbox = QGroupBox("Maps")
        maps_groupbox.setLayout(gb_layout)
        return maps_groupbox

    def _HandleClose(self, action):
        if action == QDialog.DialogCode.Accepted:
            self.accept()

    def _HandlePlay(self):
        self.accept()

    def _HandlePlayDemo(self):
        self.selectedDemo = self.mapOverviewWidget._selected_demo
        self.accept()

    def _HandleSelection(self, index):
        self.selectedIndex = index
        self.mapOverviewWidget._Update(index)

# def OpenSelectMapDialog() -> str:
#     """Returns MapId of the selected map or None"""

#     # at this point a map set and its maps MUST have been loaded
#     table_rows = [map.to_dict() for map in GetMapsSelectController().maps]
#     dialog = ViewMapSelect(table_rows, GetMapsSelectController().mapSet)

#     if dialog.exec() == QDialog.DialogCode.Rejected:
#         # clear the selected map set
#         GetMapsSelectController().mapSet = None

#         return None, None

#     if dialog.selectedIndex is None:
#         return None, None
#     else:
#         map = GetMapsSelectController().maps[dialog.selectedIndex]
#         if dialog.selectedDemo is not None:
#             return map, dialog.selectedDemo
#         return map, None

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = ViewMapSelect()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
