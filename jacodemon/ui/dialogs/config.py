from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QTabWidget, QDialog, QVBoxLayout, QLabel

from jacodemon.ui.sets.select import SelectSetTab
from jacodemon.ui.config.general import GeneralTab
from jacodemon.ui.config.mods import ModsTab
from jacodemon.ui.config.obs import ObsTab
from jacodemon.ui.config.dsda import DsdaTab

class _ConfigTabWidget(QTabWidget):
    
    def __init__(self, parent, close_signal: Signal):
        super().__init__(parent)

        # create tabs
        self.addTab(SelectSetTab(self, close_signal), "Sets")
        self.addTab(GeneralTab(self), "Config: General")
        self.addTab(ModsTab(self), "Config: Mods")
        self.addTab(ObsTab(self), "Config: OBS")
        self.addTab(DsdaTab(self), "Config: DSDA")

class _ConfigDialog(QDialog):

    # define signal to be passed to child elements to signal closing
    #   the positioning implies it will be assigned to self. idk
    close_dialog = Signal(int)

    def __init__(self):
        super().__init__()

        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        layout = QVBoxLayout(self)

        # tab widget will use self.close_dialog to handle closing
        self.configTabWidget = _ConfigTabWidget(self, self.close_dialog)
        layout.addWidget(self.configTabWidget)
        self.setLayout(layout)

        self.close_dialog.connect(self._HandleClose)

    def _HandleClose(self, action):
        if action == QDialog.DialogCode.Accepted:
            self.accept()

def OpenConfigDialog():
    dialog = _ConfigDialog()
    return dialog.exec()
