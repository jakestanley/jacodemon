from jacodemon.misc.files import OpenDirectoryDialog

from jacodemon.service.registry import Registry
from jacodemon.service.config_service import ConfigService

from jacodemon.view.components.config.general import GeneralTab

class ControllerGeneral:
    def __init__(self, view: GeneralTab):
        self.view = view
        self.config_service: ConfigService = Registry.get(ConfigService)

        self.view.demo_path_picker.clicked.connect(lambda: OpenDirectoryDialog(self.view, "demos",   self.view.demo_path))
        self.view.iwad_path_picker.clicked.connect(lambda: OpenDirectoryDialog(self.view, "IWAD",    self.view.iwad_path))
        self.view.maps_path_picker.clicked.connect(lambda: OpenDirectoryDialog(self.view, "maps",    self.view.maps_path))
        self.view.mods_path_picker.clicked.connect(lambda: OpenDirectoryDialog(self.view, "mods",    self.view.mods_path))

        self.view.fields_updated.connect(self.changed)
        self.view.save_button.clicked.connect(self.save)
        self.view.revert_button.clicked.connect(self.update)

        self.update()

    def changed(self):
        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

    def save(self):
        self.config_service.SetDemoDir(self.view.demo_path.text())
        self.config_service.SetIwadDir(self.view.iwad_path.text())
        self.config_service.SetMapsDir(self.view.maps_path.text())
        self.config_service.SetModsDir(self.view.mods_path.text())
        self.config_service.SetDefaultCompLevel(self.view.default_complevel.text())

        index = self.view.default_skill.currentIndex() + 1
        self.config_service.SetDefaultSkillLevel(index)
        self.update()

    def update(self):

        # general settings
        skill = self.config_service.GetDefaultSkillLevel()-1
        self.view.default_skill.setCurrentIndex(skill)
        self.view.demo_path.setText(self.config_service.GetDemoDir())
        self.view.iwad_path.setText(self.config_service.GetIwadDir())
        self.view.maps_path.setText(self.config_service.GetMapsDir())
        self.view.mods_path.setText(self.config_service.GetModsDir())
        self.view.default_complevel.setText(self.config_service.GetDefaultCompLevel())

        self.view.save_button.setEnabled(False)
        self.view.revert_button.setEnabled(False)
