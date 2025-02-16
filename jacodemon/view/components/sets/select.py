import copy
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QDialog

from jacodemon.model.maps import MapSet

class MapSetWidget(QWidget):

    change_signal = Signal()

    def __init__(self, mapset: MapSet, close_signal: Signal):
        super().__init__()
        self.close_signal = close_signal
        self.mapset: MapSet = mapset
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
        self.pathLabel = QLabel("\n".join([path.path for path in self.mapset.paths]))
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

    # TODO: open TXT file if it exists
    def open(self):
        # TODO SHOW RUNTIME OPTIONS BEFORE MAP LAUNCH (as well as in main dialog)
        if(GetMapsSelectController().Open(self.mapset.id)):
            self.close_signal.emit(QDialog.DialogCode.Accepted)

    def edit(self):
        GetEditSetController().NewEdit(self, self.mapset.id)
        self.change_signal.emit()

    def remove(self):
        GetSetController().Remove(self.mapset)
        self.change_signal.emit()


class SelectSetTab(QWidget):
    state_changed = Signal()

    def __init__(self, parent: QStackedWidget):
        super().__init__(parent)

        self.setWindowTitle("Select Set")

        self.layout = QVBoxLayout()

        self.add_button = QPushButton("New map set")
        self.add_button.clicked.connect(self.handle_add)
        self.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.listWidget)

    def handle_add(self):
        # GetSetController().Add(FindDoomFiles(GetConfig().maps_dir))
        self.populateList()

def OpenSetSelection():

    app = QApplication.instance()
    window = SelectSetTab(None, None)
    window.resize(800, 600)

    window.show()
    rt = app.exec()

    return

