from jacodemon.model.app import AppModel

class ControllerGeneral:
    def __init__(self, app_model: AppModel, view):
        self.app_model = app_model
        self.view = view

        self.view.demo_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("demos", self.demo_path))
        self.view.iwad_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("IWAD", self.iwad_path))
        self.view.maps_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("maps", self.maps_path))
        self.view.mods_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("mods", self.mods_path))

        self.update()

    def update(self):

        # general settings
        self.view.demo_path.setText(self.app_model.GetDemoDir())
        self.view.iwad_path.setText(self.app_model.GetIwadDir())
        self.view.maps_path.setText(self.app_model.GetMapsDir())
        self.view.mods_path.setText(self.app_model.GetModsDir())
        self.view.default_complevel.setText(self.app_model.GetDefaultCompLevel())
