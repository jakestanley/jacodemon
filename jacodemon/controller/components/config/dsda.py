from jacodemon.service.registry import Registry
from jacodemon.service.config_service import ConfigService

from jacodemon.misc.files import OpenSingleFileDialog

from jacodemon.view.components.config.dsda import DsdaTab

class ControllerDsda:
    def __init__(self, view: DsdaTab):
        self.config_service: ConfigService = Registry.get(ConfigService)
        self.view = view

        self.view.dsda_path_picker.clicked.connect(lambda: OpenSingleFileDialog(self.view, "All Files (*);;Exe Files (*.exe)", self.view.dsda_path))
        self.view.dsda_cfg_path_picker.clicked.connect(lambda: OpenSingleFileDialog(self.view, "All Files (*);;Text Files (*.cfg)", self.view.dsda_cfg_path))
        self.view.dsda_hud_path_picker.clicked.connect(lambda: OpenSingleFileDialog(self.view, "All Files (*);;LUMP Files (*.lmp)", self.view.dsda_hud_path))

        self.view.fields_updated.connect(self.changed)
        self.view.save_button.clicked.connect(self.save)
        self.view.revert_button.clicked.connect(self.update)

        self.view.clear_dsda_cfg_btn.clicked.connect(lambda: self.view.dsda_cfg_path.setText(""))
        self.view.clear_dsda_hud_btn.clicked.connect(lambda: self.view.dsda_hud_path.setText(""))

        self.update()

    def changed(self):
        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

    def save(self):
        self.config_service.SetDsdaPath(self.view.dsda_path.text())
        self.config_service.SetDsdaCfgPath(self.view.dsda_cfg_path.text())
        self.config_service.SetDsdaHudLump(self.view.dsda_hud_path.text())
        self.update()

    def update(self):
        self.view.dsda_path.setText(self.config_service.GetDsdaPath())
        self.view.dsda_cfg_path.setText(self.config_service.GetDsdaCfgPath())
        self.view.dsda_hud_path.setText(self.config_service.GetDsdaHudLump())

        self.view.save_button.setEnabled(False)
        self.view.revert_button.setEnabled(False)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = DsdaTab()
    view.resize(800,600)
    
    controller = ControllerDsda(app_model, view)
    view.show()
    sys.exit(app.exec())
