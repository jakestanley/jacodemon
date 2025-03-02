from jacodemon.misc.files import OpenDirectoryDialog

from jacodemon.model.app import AppModel
from jacodemon.view.components.config.general import GeneralTab

class ControllerGeneral:
    def __init__(self, app_model: AppModel, view: GeneralTab):
        self.app_model = app_model
        self.view = view

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
        self.app_model.SetDemoDir(self.view.demo_path.text())
        self.app_model.SetIwadDir(self.view.iwad_path.text())
        self.app_model.SetMapsDir(self.view.maps_path.text())
        self.app_model.SetModsDir(self.view.mods_path.text())
        self.app_model.SetDefaultCompLevel(self.view.default_complevel.text())

        index = self.view.default_skill.currentIndex() + 1
        self.app_model.SetDefaultSkillLevel(index)
        self.update()

    def update(self):

        # general settings
        skill = self.app_model.GetDefaultSkillLevel()-1
        self.view.default_skill.setCurrentIndex(skill)
        self.view.demo_path.setText(self.app_model.GetDemoDir())
        self.view.iwad_path.setText(self.app_model.GetIwadDir())
        self.view.maps_path.setText(self.app_model.GetMapsDir())
        self.view.mods_path.setText(self.app_model.GetModsDir())
        self.view.default_complevel.setText(self.app_model.GetDefaultCompLevel())

        self.view.save_button.setEnabled(False)
        self.view.revert_button.setEnabled(False)