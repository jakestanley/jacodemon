from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget

from jacodemon.view.components.sets.select import MapSetList

class SetsTab(QWidget):
    state_changed = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Set")

        self.layout = QVBoxLayout()

        self.add_button = QPushButton("New map set")
        self.setLayout(self.layout)

        self.mapSetList = MapSetList()
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.mapSetList)
