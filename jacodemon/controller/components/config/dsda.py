from jacodemon.model.app import AppModel

class ControllerDsda:
    def __init__(self, app_model: AppModel, view):
        self.app_model = app_model
        self.view = view