from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, \
    QDialog, QWidget, QHBoxLayout, QLabel, QTableView, QCheckBox, \
    QDialogButtonBox

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from jacodemon.config import GetConfig
from jacodemon.model.maps import MapSet
from jacodemon.wad import IsValidWadPath
import jacodemon.controller.sets.edit as edit

_COL_INDEX_WAD = 0
_COL_INDEX_ENABLED = 1
_COL_INDEX_ACTION = 2

class EnabledCell(QWidget):
    def __init__(self, parent=None, path=None, enabled=True):
        super().__init__(parent)

        self.path = path
        self.enabled = enabled

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 0, 2, 0)
        self.checkbox = QCheckBox();
        self.checkbox.setChecked(self.enabled)
        self.checkbox.stateChanged.connect(self.Toggle)
        self.layout.addWidget(self.checkbox)

    def Toggle(self, state):
        edit.GetEditSetController().Toggle(self.path, state)
        print(f"Toggle {self.id} to {state}")
        pass

class ActionPanel(QWidget):
    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.path = path
        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(2, 0, 2, 0)
        self.layout.setSpacing(2)
        self.locateButton = QPushButton("Locate")
        self.removeButton = QPushButton("Remove")
        self.upButton = QPushButton("⬆️")
        self.downButton = QPushButton("⬇️")
        self.upButton.setFixedWidth(40)
        self.downButton.setFixedWidth(40)

        if IsValidWadPath(path):
            self.locateButton.setEnabled(False)
        
        self.layout.addWidget(self.locateButton)
        self.layout.addWidget(self.removeButton)
        
        # TODO: functionality
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.upButton.setToolTip("Coming soon!")
        self.downButton.setToolTip("Coming soon!")
        self.layout.addWidget(self.upButton)
        self.layout.addWidget(self.downButton)

        self.locateButton.clicked.connect(self.locate)
        self.removeButton.clicked.connect(self.remove)
        self.upButton.clicked.connect(self.up)
        self.downButton.clicked.connect(self.down)

        # TODO table re-ordering
        self.setLayout(self.layout)

    def locate(self):
        edit.GetEditSetController().Locate(self.path)
        print(f"Locating (unimplemented)")

    def remove(self):
        edit.GetEditSetController().Remove(self.path)

    def up(self):
        print(f"Moving up (unimplemented)")

    def down(self):
        print(f"Moving down (unimplemented)")

class EditSetDialog(QDialog):

    def __init__(self, parent, mapSet: MapSet) -> None:
        super().__init__(parent)

        self.setWindowTitle(f"Editing \"{mapSet.name}\"")
        self.resize(920, 600)

        self.model = None
        self.resetModel()
        self.mapSet = mapSet

        self.layout: QVBoxLayout = QVBoxLayout()

        headingLayout = self.create_heading_layout()
        self.layout.addLayout(headingLayout)

        self.tableView = QTableView()
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setModel(self.model)
        # self.tableView.setColumnWidth(_COL_INDEX_WAD, 400)
        self.tableView.setColumnWidth(_COL_INDEX_ENABLED, 24)
        # self.tableView.setColumnWidth(_COL_INDEX_ACTION, 300)

        self.layout.addWidget(self.tableView)

        # confirm or close
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        # TODO: on reject, don't save, on accept, DO save
        self.layout.addWidget(button_box)

        self.setLayout(self.layout)

        # TODO set IWAD to use for this set
        self.populateTable()
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()

    def create_heading_layout(self):
        hlayout = QHBoxLayout()
        
        button_addWad = QPushButton("Add WAD")
        button_addWad.clicked.connect(self.AddWad)
        hlayout.addWidget(button_addWad)

        button_setIwad = QPushButton("Set IWAD");
        button_setIwad.clicked.connect(self.SetIwad)
        hlayout.addWidget(button_setIwad)

        return hlayout

    def AddWad(self):
        pass

    def SetIwad(self):
        pass

    def resetModel(self):
        if self.model:
            self.model.clear()
        
        self.model = QStandardItemModel(0, 3)  # 2 columns
        self.model.setHeaderData(_COL_INDEX_WAD, Qt.Horizontal, "Path")
        self.model.setHeaderData(_COL_INDEX_ENABLED, Qt.Horizontal, "")
        self.model.setHeaderData(_COL_INDEX_ACTION, Qt.Horizontal, "Actions")

    def populateTable(self):

        if self.mapSet is None:
            return

        for path in self.mapSet.paths:
            item = QStandardItem(path.path)
            if not IsValidWadPath(path.path):
                item = QStandardItem(f"⚠️ {path.path}")
            enabled = QStandardItem()
            actions = QStandardItem()
            self.model.appendRow([item, enabled, actions])
            current_row = self.model.rowCount() - 1
            wadpath = path.path
            actionPanel = ActionPanel(path=wadpath) # TODO id, mapset, etc
            enabledCell = EnabledCell(self, path=path, enabled=path.enabled)
            self.tableView.setIndexWidget(self.model.index(current_row, _COL_INDEX_ENABLED), enabledCell)
            self.tableView.setIndexWidget(self.model.index(current_row, _COL_INDEX_ACTION), actionPanel)

def OpenEditDialog(mapset: MapSet):
    # window = EditSetDialog(mapset)
    # window.resize(800, 600)
    # window.show()
    pass

if __name__ == "__main__":

    app = QApplication([])
    OpenEditDialog(GetConfig(True).sets[0])
