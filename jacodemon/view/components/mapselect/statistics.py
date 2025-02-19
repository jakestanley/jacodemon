
from typing import List

from PySide6.QtWidgets import QVBoxLayout, QTableView, QWidget
from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel, Signal

from jacodemon.model.stats import Statistics

_COL_INDEX_DEMO = 0
_COL_INDEX_SKILL = 1
_COL_INDEX_TIME = 2
_COL_INDEX_KILLS = 3
_COL_INDEX_ITEMS = 4
_COL_INDEX_SECRETS = 5
_COL_INDEX_TIMESTAMP = 6

KEY_LUMP="Demo"
KEY_SKILL="Skill"
KEY_TIME="Time"
KEY_KILLS="Kills"
KEY_ITEMS="Items"
KEY_SECRETS="Secrets"
KEY_TIMESTAMP="Timestamp"

_COLUMN_NAMES = {
    _COL_INDEX_DEMO: KEY_LUMP,
    _COL_INDEX_SKILL: KEY_SKILL,
    _COL_INDEX_TIME: KEY_TIME,
    _COL_INDEX_KILLS: KEY_KILLS,
    _COL_INDEX_ITEMS: KEY_ITEMS,
    _COL_INDEX_SECRETS: KEY_SECRETS,
    _COL_INDEX_TIMESTAMP: KEY_TIMESTAMP
}

class _StatisticsTableModel(QAbstractTableModel):
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

class StatisticsTableView(QWidget):

    statistics_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = _StatisticsTableModel()
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
            self.statistics_selected.emit(-1)
            return
        for index in selected.indexes():
            # Only process the first column to avoid processing multiple columns per row click
            if index.column() == 0:
                row = index.row()
                self.statistics_selected.emit(row)

    def Update(self, statisticses: List[Statistics]):
        self.model.refreshData([statistics.to_dict() for statistics in statisticses])
        self.table_view.resizeColumnsToContents()
