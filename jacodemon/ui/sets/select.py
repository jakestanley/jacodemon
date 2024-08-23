from typing import List

from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QFileDialog

from jacodemon.wad import IsValidWadPath
from jacodemon.model.maps import MapSet
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.controller.set_controller import SetController, GetSetController

class MapSetWidget(QWidget):
    def __init__(self, mapset: MapSet):
        super().__init__()
        self.mapset = mapset
        self.initUI()

    def initUI(self):
        
        invalid = self.mapset.HasInvalidConfiguration()

        layout = QHBoxLayout()
        layout.setContentsMargins(8,8,8,8)

        # mapset name label
        vLayout = QVBoxLayout()
        nameLabel = QLabel(self.mapset.name if self.mapset.name else "UNNAMED")

        nameLabel.setStyleSheet("font-size: 14px")
        if invalid:
            nameLabel = QLabel(f"⚠️ {self.mapset.name if self.mapset.name else "UNNAMED"}")
            nameLabel.setStyleSheet("font-size: 14px; color: red;")

        # mapset path label
        self.pathLabel = QLabel("\n".join(self.mapset.paths))
        self.pathLabel.setStyleSheet("font-size: 12px; color: grey;")

        # setup layouts
        vLayout.addWidget(nameLabel)
        vLayout.addWidget(self.pathLabel)

        layout.addLayout(vLayout)

        # TODO: if any files are not valid, warn and disable Open button

        # Open button
        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        self.openButton = QPushButton("Open")
        self.openButton.setMaximumWidth(80)
        self.openButton.clicked.connect(self.open)
        self.openButton.setEnabled(invalid == False)

        # Edit
        self.editButton = QPushButton("Edit")
        self.editButton.setMaximumWidth(80)
        self.editButton.clicked.connect(self.edit)
        self.editButton.setEnabled(True)

        # Remove
        self.removeButton = QPushButton("Remove")
        self.removeButton.setMaximumWidth(80)
        self.removeButton.clicked.connect(self.remove)
        self.removeButton.setEnabled(True)

        vLayout.addWidget(self.openButton)
        vLayout.addWidget(self.editButton)
        vLayout.addWidget(self.removeButton)

        layout.addLayout(vLayout)

        self.setLayout(layout)

    def open(self):
        pass

    def edit(self):
        pass

    def remove(self):
        pass

class SetWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Select Set")
        self.layout = QVBoxLayout()

        self.add_button = QPushButton("New map set")
        self.add_button.clicked.connect(self.handle_add)
        self.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.listWidget)

        self.populateList()

    def handle_add(self):
        GetSetController().Add(FindDoomFiles())

    def populateList(self):
        self.listWidget.clear()

        for mapset in GetConfig().sets:
            listItem = QListWidgetItem(self.listWidget)
            mapsetWidget = MapSetWidget(mapset)
            listItem.setSizeHint(mapsetWidget.sizeHint())
            self.listWidget.addItem(listItem)
            self.listWidget.setItemWidget(listItem, mapsetWidget)

def FindDoomFiles() -> str:
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    title = "Select a map set"

    fileName, _ = dialog.getOpenFileNames(None, title, "",
        "Doom mod files (*.pk3 *.wad *.deh);;Other (*)")

    return fileName

def OpenSetSelection():
    
    # rows = []
    # for map in maps:
    #     rows.append(map.Dictify())
    # to reuse this instance later, use QApplication.instance()

    app = QApplication.instance()
    window = SetWindow(None)
    window.resize(800, 600)
    # selected = None

    # def handle_index_selected(index):
    #     nonlocal selected
    #     selected = maps[index]

    # window.index_selected.connect(handle_index_selected)

    window.show()
    app.exec()

    # return selected

if __name__ == "__main__":
    app = QApplication()
    # TODO mock config
    OpenSetSelection()