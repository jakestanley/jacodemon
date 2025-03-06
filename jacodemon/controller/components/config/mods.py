from typing import List

from PySide6.QtCore import QObject, Signal

from jacodemon.service.registry import Registry
from jacodemon.service.config_service import ConfigService

from jacodemon.misc.files import FindDoomFiles

from jacodemon.model.mod import Mod
from jacodemon.view.components.config.mods import ModsTab

class ControllerMods(QObject):

    def __init__(self, view: ModsTab):
        super().__init__()

        self.view: ModsTab = view

        # services
        self.config_service: ConfigService = Registry.get(ConfigService)

        # these rely on knowledge of the view*
        self.view.btn_add_mods.clicked.connect(self.on_add_pressed)
        self.view.btn_remove_mods.clicked.connect(self.on_remove_pressed)

        self.mods = []
        self.selected_mod = None

        # *but these subscribes to signals
        self.view.save_button.clicked.connect(self.save)
        self.view.revert_button.clicked.connect(self.update)

        self.view.row_selected.connect(self.on_mod_selected)
        self.view.row_toggled.connect(self.on_mod_toggled)

    def on_mod_selected(self, selected):
        self.selected_mod = selected

    def on_mod_toggled(self, index, checked):
        self.mods[index].enabled = checked

        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

    def on_add_pressed(self):
        files = FindDoomFiles(self.config_service.GetModsDir())
        for file in files:
            self.mods.append(Mod(file))

            # only update button states if there was at least one mod added
            self.view.save_button.setEnabled(True)
            self.view.revert_button.setEnabled(True)

        self.view.SetMods(self.mods)

    def on_remove_pressed(self):

        if self.selected_mod is None:
            return

        self.mods.pop(self.selected_mod)
        self.view.SetMods(self.mods)

        # TODO: if one was actually removed, like
        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

        self.selected_mod = None

    def save(self):
        self.config_service.SetMods(self.mods)
        self.update()
        
    def update(self):

        # TODO: make this respond to events. never trigger manually. same goes 
        #   for loads of other places
        self.mods: List[Mod] = self.config_service.GetMods()
        self.view.SetMods(self.mods)

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
    view = ModsTab()

    controller = ControllerMods(view)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec())
