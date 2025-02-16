from PySide6.QtWidgets import QApplication, QVBoxLayout, QTableView, QWidget, QStyle, QStyleOptionButton, QStyledItemDelegate
from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel, Signal

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.model.demo import GetDemosForMap

import jacodemon.model.demo_constants as DemoConstants

_COL_INDEX_TIME = 0
_COL_INDEX_KILLS = 1
_COL_INDEX_ITEMS = 2
_COL_INDEX_SECRETS = 3
_COL_INDEX_TIMESTAMP = 4

_COLUMN_NAMES = {
    _COL_INDEX_TIME: DemoConstants.KEY_TIME,
    _COL_INDEX_KILLS: DemoConstants.KEY_KILLS,
    _COL_INDEX_ITEMS: DemoConstants.KEY_ITEMS,
    _COL_INDEX_SECRETS: DemoConstants.KEY_SECRETS,
    _COL_INDEX_TIMESTAMP: DemoConstants.KEY_TIMESTAMP
}

class _DemoTableModel(QAbstractTableModel):
    def __init__(self, demos=[], parent=None):
        super().__init__(parent)
        self._data = demos or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(_COLUMN_NAMES.keys())
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._data[index.row()][_COLUMN_NAMES[index.column()]]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # Return the header label for the given section (column index)
                return _COLUMN_NAMES[section]
            
    def refreshData(self, new_data):
        # Begin model reset operation
        self.beginResetModel()
        # Update the internal data
        self._data = new_data
        # End model reset operation
        self.endResetModel()

class DemoTableView(QWidget):

    demo_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = _DemoTableModel()
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.selectionModel().selectionChanged.connect(self._HandleSelection)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

    def _HandleSelection(self, selected, deselected):
        if len(selected.indexes()) == 0:
            self.demo_selected.emit(-1)
            return
        for index in selected.indexes():
            # Only process the first column to avoid processing multiple columns per row click
            if index.column() == 0:
                row = index.row()
                self.demo_selected.emit(row)

    def Update(self, map):
        demos = GetDemosForMap(map, GetConfig().demo_dir)
        self.model.refreshData([demo.to_dict() for demo in demos])
        self.table_view.resizeColumnsToContents()
