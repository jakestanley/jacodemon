from typing import List
from functools import partial

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

    def __init__(self, mapset: MapSet):
        super().__init__()
        self.mapSetId = mapset.id
        
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

        # Edit
        self.editButton = QPushButton("Edit")
        self.editButton.setMaximumWidth(80)
        self.editButton.setEnabled(True)

        # Remove
        self.removeButton = QPushButton("Remove")
        self.removeButton.setMaximumWidth(80)
        self.removeButton.setEnabled(True)

        vLayout.addWidget(self.openButton)
        vLayout.addWidget(self.editButton)
        vLayout.addWidget(self.removeButton)

        layout.addLayout(vLayout)

        self.setLayout(layout)

class MapSetList(QListWidget):

    # let's just keep it simple and return map set IDs instead of indexes
    openItemRequested = Signal(str)
    editItemRequested = Signal(str)
    removeItemRequested = Signal(str)
    print("initialised signals")

    def __init__(self):
        super().__init__()

    def populate(self, mapsets: List[MapSet]):
        self.clear()

        self.stuff = []

        for mapset in mapsets:
            item = QListWidgetItem()
            widget = MapSetListItem(mapset)

            # ensure signals with indexes are emitted
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)

            mapset_id = mapset.id
            widget.openButton.clicked.connect(partial(self.on_open_item, mapset_id))
            widget.editButton.clicked.connect(partial(self.on_edit_item, mapset_id))
            widget.removeButton.clicked.connect(partial(self.on_remove_item, mapset_id))

            self.stuff.append(widget)
            self.stuff.append(item)

    def on_open_item(self, id):
        self.openItemRequested.emit(str(id))

    def on_edit_item(self, id):
        self.editItemRequested.emit(str(id))

    def on_remove_item(self, id):
        self.removeItemRequested.emit(str(id))
