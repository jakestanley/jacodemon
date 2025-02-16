from PySide6.QtWidgets import QFileDialog, QListWidgetItem

from jacodemon.model.app import AppModel
from jacodemon.view.config import ViewConfig

from jacodemon.view.components.config.sets import SetsTab
from jacodemon.view.components.config.general import GeneralTab
from jacodemon.view.components.config.mods import ModsTab
from jacodemon.view.components.config.obs import ObsTab
from jacodemon.view.components.config.dsda import DsdaTab

from jacodemon.controller.components.config.sets import ControllerSets
from jacodemon.controller.components.config.general import ControllerGeneral
from jacodemon.controller.components.config.mods import ControllerMods
from jacodemon.controller.components.config.obs import ControllerObs
from jacodemon.controller.components.config.dsda import ControllerDsda

class ControllerConfig():
    def __init__(self, app_model: AppModel, view_config: ViewConfig):

        self.app_model = app_model
        self.view = view_config

        # create views and controllers for tabs
        selectSetTab = SetsTab()
        generalTab = GeneralTab()
        modsTab = ModsTab()
        obsTab = ObsTab()
        dsdaTab = DsdaTab()

        ControllerSets(app_model, selectSetTab)
        ControllerGeneral(app_model, generalTab)
        ControllerMods(app_model, modsTab)
        ControllerObs(app_model, obsTab)
        ControllerDsda(app_model, dsdaTab)

        self.view.configTabWidget.addTab(selectSetTab, "Sets")
        self.view.configTabWidget.addTab(generalTab, "Config: General")
        self.view.configTabWidget.addTab(modsTab, "Config: Mods")
        self.view.configTabWidget.addTab(obsTab, "Config: OBS")
        self.view.configTabWidget.addTab(dsdaTab, "Config: DSDA")

    # TODO: move this
    def OpenSingleFileDialog(self, types, line):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", types)

        if file:
            line.setText(file)

    # TODO: move this also
    def OpenDirectoryDialog(self, what, line):
        options = QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, f"Select {what} directory", "", options=options)

        if directory:
            line.setText(directory)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewConfig()
    
    controller = ControllerConfig(app_model, view)
    view.show()
    sys.exit(app.exec())
