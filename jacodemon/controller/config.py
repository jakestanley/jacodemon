from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog

from jacodemon.model.app import AppModel
from jacodemon.view.config import ViewConfig

from jacodemon.controller.components.config.sets import ControllerSets
from jacodemon.controller.components.config.general import ControllerGeneral
from jacodemon.controller.components.config.mods import ControllerMods
from jacodemon.controller.components.config.obs import ControllerObs
from jacodemon.controller.components.config.dsda import ControllerDsda

class ControllerConfig(QObject):

    accept_signal = Signal()
    reject_signal = Signal()

    def __init__(self, app_model: AppModel, view_config: ViewConfig):
        super().__init__()

        self.app_model = app_model
        self.view = view_config

        # create views and controllers for tabs
        self.cSets = ControllerSets(app_model, self.view.selectSetTab)
        self.cGeneral = ControllerGeneral(app_model, self.view.generalTab)
        self.cMods = ControllerMods(app_model, self.view.modsTab)
        self.cObs = ControllerObs(app_model, self.view.obsTab)
        self.cDsda = ControllerDsda(app_model, self.view.dsdaTab)

        self.cSets.accept_signal.connect(self.accept_signal.emit)

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

    import gc
    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    gc.disable()

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewConfig()
    
    controller = ControllerConfig(app_model, view)
    view.show()
    sys.exit(app.exec())
