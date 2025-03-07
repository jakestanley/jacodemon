from jacodemon.service.registry import Registry
from jacodemon.service.config_service import ConfigService

from jacodemon.view.components.config.obs import ObsTab

class ControllerObs:
    def __init__(self, view: ObsTab):
        self.view = view

        self.config_service: ConfigService = Registry.get(ConfigService)

        self.view.fields_updated.connect(self.changed)
        self.view.save_button.clicked.connect(self.save)
        self.view.revert_button.clicked.connect(self.update)

        self.update()

    def changed(self):
        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

    def save(self):
        self.config_service.config.play_scene = self.view.play_scene.text()
        self.config_service.config.wait_scene = self.view.wait_scene.text()
        self.config_service.config.browser_scene = self.view.browser_scene.text()
        self.config_service.config.title_source = self.view.title_source.text()
        self.config_service.Save()

        self.update()

    def update(self):
        self.view.play_scene.setText(self.config_service.config.play_scene)
        self.view.wait_scene.setText(self.config_service.config.wait_scene)
        self.view.browser_scene.setText(self.config_service.config.browser_scene)
        self.view.title_source.setText(self.config_service.config.title_source)

        self.view.save_button.setEnabled(False)
        self.view.revert_button.setEnabled(False)
