from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, \
    QDialog, QWidget, QHBoxLayout, QLabel, QTableView, QCheckBox, \
    QDialogButtonBox, QHeaderView, QLineEdit

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel

from jacodemon.config import GetConfig
from jacodemon.model.maps import MapSet, MapSetPath
import jacodemon.controller.sets.edit as edit
from jacodemon.files import FindDoomFiles, FindIwad

# TODO use these constants instead of magic numbers
_COL_INDEX_ENABLED = 0
_COL_INDEX_PATH = 1
_COL_INDEX_MOVE_UP = 2
_COL_INDEX_MOVE_DOWN = 3
_COL_INDEX_LOCATE = 4
_COL_INDEX_REMOVE = 5

from PySide6.QtWidgets import QStyledItemDelegate, QPushButton, QStyleOptionButton, QStyle, QFileDialog
from PySide6.QtCore import Qt, QEvent

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # No editor is needed for buttons
        return None

    def paint(self, painter, option, index):
        # Determine button type
        if index.column() == _COL_INDEX_LOCATE:
            text = "Locate"
        elif index.column() == _COL_INDEX_MOVE_UP:
            text = "Move Up"
        elif index.column() == _COL_INDEX_MOVE_DOWN:
            text = "Move Down"
        elif index.column() == _COL_INDEX_REMOVE:
            text = "Remove"
        else:
            super().paint(painter, option, index)
            return

        button_style_option = QStyleOptionButton()
        button_style_option.rect = option.rect
        button_style_option.text = text
        if index.column() in (_COL_INDEX_MOVE_UP, _COL_INDEX_MOVE_DOWN):  # Disable 'Move Up' for the first row and 'Move Down' for the last row
            if (index.column() == _COL_INDEX_MOVE_UP and index.row() == 0) or (index.column() == _COL_INDEX_MOVE_DOWN and index.row() == index.model().rowCount() - 1):
                button_style_option.state |= QStyle.State_Enabled

        option.widget.style().drawControl(QStyle.CE_PushButton, button_style_option, painter)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease:
            if index.column() == _COL_INDEX_LOCATE:  # Locate button
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.ExistingFile)
                if file_dialog.exec():
                    selected_file = file_dialog.selectedFiles()[0]
                    model.setData(index.siblingAtColumn(1), selected_file, Qt.EditRole)
            elif index.column() == _COL_INDEX_MOVE_UP:  # Move Up button
                row = index.row()
                if row > 0:
                    model.moveItem(row, row - 1)
            elif index.column() == _COL_INDEX_MOVE_DOWN:  # Move Down button
                row = index.row()
                if row < model.rowCount() - 1:
                    model.moveItem(row, row + 1)
            elif index.column() == _COL_INDEX_REMOVE:  # Remove button
                model.removeItem(index.row())
            return True
        return False

class MapSetPathItemTableModel(QAbstractTableModel):
    def __init__(self, mapSetPaths=None):
        super().__init__()
        self.items = mapSetPaths or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return 6  # Columns for 'enabled', 'path', 'move up', 'move down', 'locate button', 'remove button

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self.items[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == _COL_INDEX_PATH:
                return item.path

        if role == Qt.CheckStateRole and index.column() == _COL_INDEX_ENABLED:
            return Qt.Checked if item.enabled else Qt.Unchecked

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        item = self.items[index.row()]

        if role == Qt.EditRole and index.column() == _COL_INDEX_PATH:
            item.path = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True

        if role == Qt.CheckStateRole and index.column() == _COL_INDEX_ENABLED:
            item.enabled = (value == Qt.Checked.value)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == _COL_INDEX_ENABLED:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        elif index.column() == _COL_INDEX_PATH:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        elif index.column() in (_COL_INDEX_MOVE_UP, _COL_INDEX_MOVE_DOWN, _COL_INDEX_LOCATE, _COL_INDEX_REMOVE):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        return Qt.ItemIsEnabled

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(item)
        self.endInsertRows()

    def removeItem(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            self.items.pop(row)
            self.endRemoveRows()

    def moveItem(self, sourceRow, destinationRow):
        if sourceRow < 0 or sourceRow >= len(self.items):
            return
        if destinationRow < 0 or destinationRow >= len(self.items):
            return

        self.beginMoveRows(QModelIndex(), sourceRow, sourceRow, QModelIndex(), destinationRow + (1 if destinationRow > sourceRow else 0))
        self.items.insert(destinationRow, self.items.pop(sourceRow))
        self.endMoveRows()

class EditSetDialog(QDialog):

    def __init__(self, parent, mapSet: MapSet) -> None:
        # TODO: read COMPLVL from text lump if available
        super().__init__(parent)
        self.mapSet = mapSet
        self.setWindowTitle(f"Editing \"{self.mapSet.name}\"")

        # create the general mapset edit view
        summary_view = QVBoxLayout()
        row = QHBoxLayout()
        add_pwad_button = QPushButton("Add PWAD")
        add_pwad_button.clicked.connect(self.AddPwad)

        set_iwad_button = QPushButton("Set IWAD")
        set_iwad_button.clicked.connect(self.SetIwad)

        self.iwad_line_edit = QLineEdit(self.mapSet.iwad)
        self.iwad_line_edit.setReadOnly(True)

        # TODO dropdown for comp levels
        self.comp_level_label = QLabel("Comp Level:")
        self.comp_level_line_edit = QLineEdit(str(self.mapSet.compLevel))

        row.addWidget(add_pwad_button)
        row.addWidget(set_iwad_button)
        row.addWidget(self.iwad_line_edit)
        row.addWidget(self.comp_level_label)
        row.addWidget(self.comp_level_line_edit)

        summary_view.addLayout(row)


        # set up the model and table
        self.model = MapSetPathItemTableModel(self.mapSet.paths)

        self.tableView = QTableView()
        self.tableView.horizontalHeader().hide()
        self.tableView.verticalHeader().hide()
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setSelectionMode(QTableView.SingleSelection)

        # row controls delegate
        button_delegate = ButtonDelegate(self.tableView)
        for column in [_COL_INDEX_MOVE_UP, _COL_INDEX_MOVE_DOWN, _COL_INDEX_LOCATE, _COL_INDEX_REMOVE]:
            self.tableView.setItemDelegateForColumn(column, button_delegate)

        # confirm or close button box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # TODO: IWAD 
        # self.tableView.verticalHeader().setVisible(False)
        # self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(_COL_INDEX_PATH, 900)

        # set up layout
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.addLayout(summary_view)
        self.layout.addWidget(self.tableView)
        self.layout.addWidget(button_box)

        self.tableView.resizeColumnToContents(_COL_INDEX_PATH)
        table_width = self.tableView.verticalHeader().width() + self.tableView.horizontalHeader().length() + 8
        table_height = self.tableView.horizontalHeader().height() + self.tableView.verticalHeader().length() + 8
        self.tableView.setFixedSize(table_width, table_height)
        self.resize(self.tableView.sizeHint())

        self.setLayout(self.layout)

    def GetPaths(self):
        paths = []
        for row in range(self.model.rowCount()):
            path = self.model.data(self.model.index(row, 1), Qt.DisplayRole)
            enabled = self.model.data(self.model.index(row, 0), Qt.CheckStateRole) == Qt.Checked
            paths.append(MapSetPath(path, enabled))

        return paths

    def AddPwad(self):
        for file in FindDoomFiles(GetConfig().maps_dir):
            self.model.addItem(MapSetPath(enabled=True, path=file))

    def SetIwad(self):
        self.iwad_line_edit.setText(FindIwad())

def OpenEditDialog(mapSet: MapSet):
    dialog = EditSetDialog(parent=None, mapSet=mapSet)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.GetPaths()
    else:
        return []

if __name__ == "__main__":

    import sys
    app = QApplication([])
    result = OpenEditDialog(GetConfig(True).sets[0])
    sys.exit(0)
