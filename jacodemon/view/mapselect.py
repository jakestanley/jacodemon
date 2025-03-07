from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout, QTableView, QTextEdit, QLineEdit

from PySide6.QtWidgets import QLabel, QGroupBox, QDialogButtonBox
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

    def populate(self, data, selectionIndex=-1):
        self.model.removeRows(0, self.model.rowCount())

        # TODO should replace, not append
        for row_dict in data:
            row_items = [QStandardItem(str(row_dict[key])) for key in _COLUMN_ORDER]
            for item in row_items:
                item.setEditable(False)  # Set the item as uneditable
            self.model.appendRow(row_items)
        self.resizeColumnsToContents()

        if selectionIndex < 0:
            return

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

        self.model = QStandardItemModel()
        self.setModel(self.model)
        
        if mapSet:
            paths = mapSet.paths
            mapSet.compLevel

        for path in paths:
            item = QStandardItem(path.path)
            item.setEditable(False)
            if not path.enabled:
                item.setForeground(QBrush(Qt.gray))
            self.model.appendRow(item)

        self.resizeColumnsToContents()
            
class SetOverviewWidget(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        
        paths = []
        compLevel = None

        self.wad_text = QTextEdit(self)
        monospace_font = QFont("Courier New")  # Use a standard monospace font
        monospace_font.setStyleHint(QFont.Monospace)

        self.wad_text.setFont(monospace_font)
        self.wad_text.setReadOnly(True)

        self.paths_table = PathsTableWidget(self)

        self.name_field = QLineEdit(self)
        layout.addWidget(QLabel(f"Name"))
        layout.addWidget(self.name_field)
        layout.addWidget(QLabel(f"Info"))
        layout.addWidget(self.wad_text)
        layout.addWidget(QLabel(f"Files"))
        layout.addWidget(self.paths_table)
        layout.addWidget(QLabel(f"CompLevel: {compLevel}"))
        layout.addStretch()
        self.setLayout(layout)

    def on_map_set_change(self, mapSet):

        if not mapSet:
            return
        
        self.name_field.setText(mapSet.name)

        if mapSet.text:
            self.wad_text.setText(mapSet.text)
        else:
            self.wad_text.setText("")

        if mapSet:
            self.paths_table.on_map_set_change(mapSet)

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

        # confirm or close
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)

    def on_map_set_change(self, mapSet):
        self.set_overview_widget.on_map_set_change(mapSet)

    def _CreateSetOverviewGroupBox(self) -> QGroupBox:
        gb_layout = QVBoxLayout()
        self.set_overview_widget = SetOverviewWidget(self)
        gb_layout.addWidget(self.set_overview_widget)

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

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = ViewMapSelect()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
