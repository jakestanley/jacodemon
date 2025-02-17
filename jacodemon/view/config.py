from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from jacodemon.view.components.config.sets import SetsTab
from jacodemon.view.components.config.general import GeneralTab
from jacodemon.view.components.config.mods import ModsTab
from jacodemon.view.components.config.obs import ObsTab
from jacodemon.view.components.config.dsda import DsdaTab

class _LastWidget(QWidget):

    last_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        button = QPushButton("Play last", self)
        button.clicked.connect(self.last_signal.emit)
        layout.addWidget(button)

        vlayout = QVBoxLayout()
        self.last_map_mod_name = QLabel(f"Mod: None")
        vlayout.addWidget(self.last_map_mod_name)
        self.last_map_map_id = QLabel(f"Map: None")
        vlayout.addWidget(self.last_map_map_id)
        layout.addLayout(vlayout)

        self.setLayout(layout)

class ViewConfig(QWidget):

    # define signal to be passed to child elements to signal closing
    #   the positioning implies it will be assigned to self. idk
    # NOTE: this may be removed with the Presenter design pattern
    close_dialog = Signal(int)

    def __init__(self):
        super().__init__()

        self.last = False
        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        layout = QVBoxLayout(self)

        # tab widget will use self.close_dialog to handle closing
        self.lastWidget = _LastWidget(self)

        self.configTabWidget = QTabWidget(self)

        self.selectSetTab = SetsTab()
        self.generalTab = GeneralTab()
        self.modsTab = ModsTab()
        self.obsTab = ObsTab()
        self.dsdaTab = DsdaTab()

        self.configTabWidget.addTab(self.selectSetTab, "Sets")
        self.configTabWidget.addTab(self.generalTab, "Config: General")
        self.configTabWidget.addTab(self.modsTab, "Config: Mods")
        self.configTabWidget.addTab(self.obsTab, "Config: OBS")
        self.configTabWidget.addTab(self.dsdaTab, "Config: DSDA")

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

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ViewConfig()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
