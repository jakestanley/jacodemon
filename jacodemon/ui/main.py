from PySide6.QtWidgets import QMainWindow, QTabWidget

from jacodemon.ui.sets.select import SelectSetTab
from jacodemon.ui.config.general import GeneralTab
from jacodemon.ui.config.mods import ModsTab
from jacodemon.ui.config.obs import ObsTab
from jacodemon.ui.config.dsda import DsdaTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Jacodemon")
        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # create tabs
        self.tabWidget.addTab(SelectSetTab(self.tabWidget), "Sets")
        self.tabWidget.addTab(GeneralTab(self.tabWidget), "Config: General")
        self.tabWidget.addTab(ModsTab(self.tabWidget), "Config: Mods")
        self.tabWidget.addTab(ObsTab(self.tabWidget), "Config: OBS")
        self.tabWidget.addTab(DsdaTab(self.tabWidget), "Config: DSDA")
