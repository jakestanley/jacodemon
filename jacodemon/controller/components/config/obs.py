from jacodemon.model.app import AppModel

class ControllerObs:
    def __init__(self, app_model: AppModel, view):
        self.app_model = app_model
        self.view = view

        self.update()

    def update(self):
        self.view.play_scene.setText(self.app_model.config.play_scene)
        self.view.wait_scene.setText(self.app_model.config.wait_scene)
        self.view.browser_scene.setText(self.app_model.config.browser_scene)
        self.view.title_source.setText(self.app_model.config.title_source)