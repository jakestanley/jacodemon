from jacodemon.model.app import AppModel

from jacodemon.view.components.config.obs import ObsTab

class ControllerObs:
    def __init__(self, app_model: AppModel, view: ObsTab):
        self.app_model = app_model
        self.view = view

        self.view.fields_updated.connect(self.changed)
        self.view.save_button.clicked.connect(self.save)
        self.view.revert_button.clicked.connect(self.update)

        self.update()

    def changed(self):
        self.view.save_button.setEnabled(True)
        self.view.revert_button.setEnabled(True)

    def save(self):
        self.app_model.config.play_scene = self.view.play_scene.text()
        self.app_model.config.wait_scene = self.view.wait_scene.text()
        self.app_model.config.browser_scene = self.view.browser_scene.text()
        self.app_model.config.title_source = self.view.title_source.text()
        self.app_model.config.Save()

        self.update()

    def update(self):
        self.view.play_scene.setText(self.app_model.config.play_scene)
        self.view.wait_scene.setText(self.app_model.config.wait_scene)
        self.view.browser_scene.setText(self.app_model.config.browser_scene)
        self.view.title_source.setText(self.app_model.config.title_source)

        self.view.save_button.setEnabled(False)
        self.view.revert_button.setEnabled(False)
