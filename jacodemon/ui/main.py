import sys

from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from jacodemon.options import Options
from jacodemon.ui.config.general import GeneralDialog
from jacodemon.ui.config.obs import ObsDialog
from jacodemon.ui.options import OptionsDialog
from jacodemon.ui.config.mods import ModsDialog
from jacodemon.ui.sets.select import SelectSetWindow
from jacodemon.ui.config.dsda import DsdaDialog
from PySide6.QtWidgets import QTabWidget

class MainWindow(QMainWindow):
    def __init__(self, options: Options):
        super().__init__()
        
        self.setWindowTitle("Jacodemon")
        self.setContentsMargins(8,8,8,8)
        self.setMinimumWidth(768)

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        
        # create tabs
        self.tabWidget.addTab(SelectSetWindow(self.tabWidget), "Sets")
        self.tabWidget.addTab(OptionsDialog(self.tabWidget, options), "Options")
        self.tabWidget.addTab(GeneralDialog(self.tabWidget), "Config: General")
        self.tabWidget.addTab(ModsDialog(self.tabWidget), "Config: Mods")
        self.tabWidget.addTab(ObsDialog(self.tabWidget), "Config: OBS")
        self.tabWidget.addTab(DsdaDialog(self.tabWidget), "Config: DSDA")

