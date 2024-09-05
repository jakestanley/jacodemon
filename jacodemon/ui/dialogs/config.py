from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from jacodemon.ui.sets.select import SelectSetTab
from jacodemon.ui.config.general import GeneralTab
from jacodemon.ui.config.mods import ModsTab
from jacodemon.ui.config.obs import ObsTab
from jacodemon.ui.config.dsda import DsdaTab

from jacodemon.last import GetLastMap

class _LastWidget(QWidget):

    last_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        
        last_map = GetLastMap()
        if not last_map: 
            return

        layout = QHBoxLayout(self)
        button = QPushButton("Play last", self)
        button.clicked.connect(self.last_signal.emit)
        layout.addWidget(button)

        vlayout = QVBoxLayout()
        label = QLabel(f"Mod: {last_map.ModName}")
        vlayout.addWidget(label)
        label = QLabel(f"Map: {last_map.MapId}")
        vlayout.addWidget(label)
        layout.addLayout(vlayout)

        self.setLayout(layout)

class _ConfigTabWidget(QTabWidget):
    
    def __init__(self, parent, close_signal: Signal):
        super().__init__(parent)

        # create tabs
        self.addTab(SelectSetTab(self, close_signal), "Sets")
        self.addTab(GeneralTab(self), "Config: General")
        self.addTab(ModsTab(self), "Config: Mods")
        self.addTab(ObsTab(self), "Config: OBS")
        self.addTab(DsdaTab(self), "Config: DSDA")

class ConfigDialog(QDialog):

    # define signal to be passed to child elements to signal closing
    #   the positioning implies it will be assigned to self. idk
    close_dialog = Signal(int)

    def __init__(self):
        super().__init__()

        self.last = False
        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        layout = QVBoxLayout(self)

        # tab widget will use self.close_dialog to handle closing
        self.lastWidget = _LastWidget(self)
        self.configTabWidget = _ConfigTabWidget(self, self.close_dialog)
        layout.addWidget(self.configTabWidget)
        layout.addWidget(self.lastWidget)
        self.setLayout(layout)

        self.close_dialog.connect(self._HandleClose)
        self.lastWidget.last_signal.connect(self._HandleLast)

    def _HandleClose(self, action):
        if action == QDialog.DialogCode.Accepted:
            self.accept()

    def _HandleLast(self):
        self.last = True
        self.accept()

