from PySide6.QtWidgets import QFileDialog, QListWidgetItem

from jacodemon.model.app import AppModel
from jacodemon.ui.view.config import ViewConfig

from jacodemon.ui.view.components.sets.select import SelectSetTab
from jacodemon.ui.view.components.config.general import GeneralTab
from jacodemon.ui.view.components.config.mods import ModsTab
from jacodemon.ui.view.components.config.obs import ObsTab
from jacodemon.ui.view.components.config.dsda import DsdaTab

from jacodemon.ui.view.components.sets.select import MapSetWidget

class ControllerConfig():
    def __init__(self, app_model: AppModel, view_config: ViewConfig):

        self.app_model = app_model
        self.view = view_config

        

        self.app_model.mapsets_updated.connect(self.on_mapsets_updated)

        # general settings, more controllers for tabs might be a good idea :D
        self.view.generalTab.demo_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("demos", self.demo_path))
        self.view.generalTab.iwad_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("IWAD", self.iwad_path))
        self.view.generalTab.maps_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("maps", self.maps_path))
        self.view.generalTab.mods_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("mods", self.mods_path))

        # mod settings
        self.view.modsTab.btn_add_mods.clicked.connect(self.AddMods)
        self.view.modsTab.btn_remove_mods.clicked.connect(self.RemoveMods)

        # TODO: this order ok?
        self.on_mapsets_updated()
        self.update()

    def update(self):

        # general settings
        self.view.generalTab.demo_path.setText(self.app_model.GetDemoDir())
        self.view.generalTab.iwad_path.setText(self.app_model.GetIwadDir())
        self.view.generalTab.maps_path.setText(self.app_model.GetMapsDir())
        self.view.generalTab.mods_path.setText(self.app_model.GetModsDir())
        self.view.generalTab.default_complevel.setText(self.app_model.GetDefaultCompLevel())

        # mods settings
        

        # obs settings
        self.view.obsTab.play_scene.setText(self.app_model.config.play_scene)
        self.view.obsTab.wait_scene.setText(self.app_model.config.wait_scene)
        self.view.obsTab.browser_scene.setText(self.app_model.config.browser_scene)
        self.view.obsTab.title_source.setText(self.app_model.config.title_source)

    def on_mapsets_updated(self):

        self.view.selectSetTab.listWidget.clear()

        # TODO: make this less shit tbh
        for mapset in reversed(self.app_model.mapSets):
            listItem = QListWidgetItem(self.view.selectSetTab.listWidget)
            mapsetWidget = MapSetWidget(mapset, None)
            # TODO: rearchecting means we don't need this signal iirc
            # mapsetWidget.change_signal.connect(self.populateList)
            listItem.setSizeHint(mapsetWidget.sizeHint())
            self.view.selectSetTab.listWidget.addItem(listItem)
            self.view.selectSetTab.listWidget.setItemWidget(listItem, mapsetWidget)

    def on_mods_updated(self):

        self.view.modsTab.mods.clear()
        for mod in self.app_model.GetMods():
            self.AddMod(mod)

    # TODO: move this
    def OpenSingleFileDialog(self, types, line):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", types)

        if file:
            line.setText(file)

    def OpenDirectoryDialog(self, what, line):
        options = QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, f"Select {what} directory", "", options=options)

        if directory:
            line.setText(directory)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewConfig()
    
    controller = ControllerConfig(app_model, view)
    view.show()
    sys.exit(app.exec())
