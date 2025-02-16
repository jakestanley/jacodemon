from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from jacodemon.model.maps import MapSet

class MapSetListItem(QWidget):

    openClicked: Signal = Signal(int)
    editClicked: Signal = Signal(int)
    removeClicked: Signal = Signal(int)

    def __init__(self, mapset: MapSet, index: int):
        super().__init__()
        self.index = index
        
        invalid = mapset.HasInvalidConfiguration()

        layout = QHBoxLayout()
        layout.setContentsMargins(8,8,8,8)

        # mapset name label
        vLayout = QVBoxLayout()

        # TODO: I am not happy with all this logic in MapSetListItem
        nameLabel = QLabel(mapset.name if mapset.name else "UNNAMED")

        nameLabel.setStyleSheet("font-size: 14px")
        if invalid:
            nameLabel = QLabel(f"⚠️ {mapset.name if mapset.name else "UNNAMED"}")
            nameLabel.setStyleSheet("font-size: 14px; color: red;")

        # mapset path label
        self.pathLabel = QLabel("\n".join([path.path for path in mapset.paths]))
        self.pathLabel.setStyleSheet("font-size: 12px; color: grey;")

        # setup layouts
        vLayout.addWidget(nameLabel)
        vLayout.addWidget(self.pathLabel)

        layout.addLayout(vLayout)

        # Open button
        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        self.openButton = QPushButton("Open")
        self.openButton.setMaximumWidth(80)
        self.openButton.setEnabled(invalid == False)
        self.openButton.clicked.connect(self.on_open_clicked)

        # Edit
        self.editButton = QPushButton("Edit")
        self.editButton.setMaximumWidth(80)
        self.editButton.setEnabled(True)
        self.editButton.clicked.connect(self.on_edit_clicked)

        # Remove
        self.removeButton = QPushButton("Remove")
        self.removeButton.setMaximumWidth(80)
        self.removeButton.setEnabled(True)
        self.removeButton.clicked.connect(self.on_remove_clicked)

        vLayout.addWidget(self.openButton)
        vLayout.addWidget(self.editButton)
        vLayout.addWidget(self.removeButton)

        layout.addLayout(vLayout)

        self.setLayout(layout)

    def on_open_clicked(self):
        self.openClicked.emit(self.index)

    def on_edit_clicked(self):
        self.editClicked.emit(self.index)

    def on_remove_clicked(self):
        self.removeClicked.emit(self.index)

class MapSetList(QListWidget):

    openItemRequested = Signal(int)
    editItemRequested = Signal(int)
    removeItemRequested = Signal(int)

    def __init__(self):
        super().__init__()

    def populate(self, mapsets: List[MapSet]):
        self.clear()
        for index, mapset in enumerate(mapsets):
            item = QListWidgetItem()
            widget = MapSetListItem(mapset, index)

            # ensure signals with indexes are emitted
            widget.openClicked.connect(self.openItemRequested.emit)
            widget.editClicked.connect(self.editItemRequested.emit)
            widget.removeClicked.connect(self.removeItemRequested.emit)

            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)
