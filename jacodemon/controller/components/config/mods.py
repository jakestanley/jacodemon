from PySide6.QtWidgets import QListWidgetItem, QCheckBox

from jacodemon.model.app import AppModel
from jacodemon.model.mod import Mod
from jacodemon.view.components.config.mods import ModsTab

class ControllerMods:
    def __init__(self, app_model: AppModel, view: ModsTab):
        self.app_model: AppModel = app_model
        self.view: ModsTab = view

        # self.view.btn_add_mods.clicked.connect(self.AddMods)
        # self.view.btn_remove_mods.clicked.connect(self.RemoveMods)

        self.on_mods_updated()

    def on_mods_updated(self):

        self.view.mods.clear()
        for mod in self.app_model.GetMods():
            self.AddMod(mod)

    def AddMod(self, mod: Mod):
        item = QListWidgetItem(self.view.mods)
        checkbox = QCheckBox(mod.path)
        checkbox.setChecked(mod.enabled)
        self.view.mods.setItemWidget(item, checkbox)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ModsTab()

    controller = ControllerMods(app_model, view)
    view.show()
    sys.exit(app.exec())
