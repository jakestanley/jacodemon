from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout, QTableView, QPushButton

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.controller.maps.select import MapsSelectController, GetMapsSelectController
from jacodemon.model.maps import MapSet, MapSetPath
from jacodemon.ui.maps.demo import DemoTableView
from PySide6.QtWidgets import QLabel, QGroupBox
from PySide6.QtGui import QBrush

import sys


_COLUMN_ORDER = ['MapId', 'Badge', 'MapName', 'Author', 'Notes']

class MapTableWidget(QTableView):

    index_selected = Signal(int)

    def __init__(self, data, parent):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setModel(self.model)

        # Create table headers based on keys in the first dictionary
        self.model.setHorizontalHeaderLabels(_COLUMN_ORDER)

        for row_dict in data:
            row_items = [QStandardItem(str(row_dict[key])) for key in _COLUMN_ORDER]
            for item in row_items:
                item.setEditable(False)  # Set the item as uneditable
            self.model.appendRow(row_items)

        self.selectionModel().selectionChanged.connect(self._HandleSelection)
        self.resizeColumnsToContents()

    def _HandleSelection(self, selected, deselected):
        if len(selected.indexes()) == 0:
            self.index_selected.emit(-1)
            return
        for index in selected.indexes():
            # Only process the first column to avoid processing multiple columns per row click
            if index.column() == 0:
                row = index.row()
                self.index_selected.emit(row)

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

    play_signal = Signal()
    play_demo_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self._selected_demo = None
        layout = QVBoxLayout(self)

        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self._HandlePlay)

        self.demo_table = DemoTableView(self)
        self.demo_table.demo_selected.connect(self._HandleSelectDemo)
        self.play_demo_button = QPushButton("Play Demo")
        self.play_demo_button.clicked.connect(self._HandlePlayDemo)
        self.play_demo_button.setEnabled(False)

        layout.addWidget(self.play_button)
        layout.addWidget(self.demo_table)
        layout.addWidget(self.play_demo_button)

        layout.addStretch()
        self.setLayout(layout)

    def _Update(self, index):
        map = GetMapsSelectController().maps[index]
        if map:
            self.play_button.setEnabled(True)
            self.demo_table.Update(map)
        self.play_demo_button.setEnabled(False)
        self._selected_demo = None
    
    def _HandlePlay(self):
        self._selected_demo = None
        self.play_signal.emit()

    def _HandleSelectDemo(self, index):
        if index == -1:
            self._selected_demo = None
            self.play_demo_button.setEnabled(False)
        else:
            self._selected_demo = index
            self.play_demo_button.setEnabled(True)

    def _HandlePlayDemo(self):
        if self._selected_demo is not None:
            self.play_demo_signal.emit()
            

class SetOverviewWidget(QWidget):
    
    def __init__(self, mapSet: MapSet, parent):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        
        layout.addWidget(PathsTableWidget(mapSet.paths, self))
        layout.addWidget(QLabel(f"Port: {mapSet.port}"))
        layout.addWidget(QLabel(f"CompLevel: {mapSet.compLevel}"))
        layout.addStretch()
        self.setLayout(layout)

class _SelectMapDialog(QDialog):

    def __init__(self, maps: dict, mapSet: MapSet):
        super().__init__()

        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        self.selectedIndex = None
        self.selectedDemo = None

        self.setWindowTitle(f"Select a map from {mapSet.name}")

        layout = QVBoxLayout(self)
        set_groupbox = self._CreateSetOverviewGroupBox(mapSet)
        maps_groupbox = self._CreateMapsGroupBox(maps)
        
        layout.addWidget(maps_groupbox)
        layout.addWidget(set_groupbox)
        
        self.setLayout(layout)

    def _CreateSetOverviewGroupBox(self, mapSet) -> QGroupBox:
        gb_layout = QVBoxLayout()
        gb_layout.addWidget(SetOverviewWidget(mapSet, self))

        set_groupbox = QGroupBox("Set")
        set_groupbox.setLayout(gb_layout)
        return set_groupbox
    
    def _CreateMapsGroupBox(self, maps):
        gb_layout = QHBoxLayout()
        self.mapTableWidget = MapTableWidget(maps, self)
        self.mapTableWidget.index_selected.connect(self._HandleSelection)

        gb_layout.addWidget(self.mapTableWidget)

        self.mapOverviewWidget = MapOverviewWidget(self)
        self.mapOverviewWidget.play_signal.connect(self._HandlePlay)
        self.mapOverviewWidget.play_demo_signal.connect(self._HandlePlayDemo)
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

def OpenSelectMapDialog() -> str:
    """Returns MapId of the selected map or None"""

    # at this point a map set and its maps MUST have been loaded
    table_rows = [map.Dictify() for map in GetMapsSelectController().maps]
    dialog = _SelectMapDialog(table_rows, GetMapsSelectController().mapSet)

    if dialog.exec() == QDialog.DialogCode.Rejected:
        sys.exit(0)

    if dialog.selectedIndex is None:
        return None
    else:
        map = GetMapsSelectController().maps[dialog.selectedIndex]
        if dialog.selectedDemo is not None:
            return map, dialog.selectedDemo
        return map, None

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    rs = OpenSelectMapDialog()
