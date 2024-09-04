import sys

from jacodemon.config import JacodemonConfig, Mod, GetConfig
from jacodemon.macros import KeyNames
from jacodemon.ui.config.config import ConfigWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QFileDialog, QDialogButtonBox, QGroupBox, QLabel, \
    QListWidget, QListWidgetItem, QCheckBox, QDialog

class GeneralTab(ConfigWidget):
    def __init__(self, parent=None):
        super(GeneralTab, self).__init__(parent)
        self.setWindowTitle("Configure")

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        general_group = self.create_general_group()
        directories_group = self.create_directories_group()

        layout.addWidget(general_group)
        layout.addWidget(directories_group)
        layout.addStretch()

        self.AddButtons(layout)
        self.LoadValuesFromConfig()

    def LoadValuesFromConfig(self):

        cfg: JacodemonConfig = GetConfig()

        self.demo_path.setText(cfg.demo_dir)
        self.iwad_path.setText(cfg.iwad_dir)
        self.maps_path.setText(cfg.maps_dir)
        self.mods_path.setText(cfg.mods_dir)
        self.default_complevel.setText(cfg.default_complevel)

    def save(self):
        cfg = GetConfig()
        cfg.demo_dir = self.demo_path.text()
        cfg.iwad_dir = self.iwad_path.text()
        cfg.maps_dir = self.maps_path.text()
        cfg.mods_dir = self.mods_path.text()
        cfg.default_complevel = self.default_complevel.text()
        cfg.Save()

    def revert(self):
        self.LoadValuesFromConfig()

    def create_directories_group(self):
        group_box = QGroupBox("Directories", self)
        vlayout = QVBoxLayout()

        iwad_hlayout = self.create_iwad_picker()
        maps_hlayout = self.create_maps_picker()
        demo_hlayout = self.create_demo_picker()
        mods_hlayout = self.create_mods_picker()

        vlayout.addLayout(iwad_hlayout)
        vlayout.addLayout(maps_hlayout)
        vlayout.addLayout(demo_hlayout)
        vlayout.addLayout(mods_hlayout)

        group_box.setLayout(vlayout)
        return group_box

    def create_demo_picker(self):
        demo_hlayout: QHBoxLayout = QHBoxLayout()
        self.demo_path = QLineEdit(self)
        
        self.demo_path.setEnabled(False)
        self.demo_path_picker = QPushButton("Select demos directory", self)
        demo_hlayout.addWidget(self.demo_path)
        demo_hlayout.addWidget(self.demo_path_picker)
        self.demo_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("demos", self.demo_path))
        return demo_hlayout

    def create_iwad_picker(self):
        iwad_hlayout: QHBoxLayout = QHBoxLayout()
        self.iwad_path = QLineEdit(self)
        
        self.iwad_path.setEnabled(False)
        self.iwad_path_picker = QPushButton("Select IWAD directory", self)
        iwad_hlayout.addWidget(self.iwad_path)
        iwad_hlayout.addWidget(self.iwad_path_picker)
        self.iwad_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("IWAD", self.iwad_path))
        return iwad_hlayout

    # TODO: this should move, possibly into Sets?
    def create_maps_picker(self):
        maps_hlayout: QHBoxLayout = QHBoxLayout()
        self.maps_path = QLineEdit(self)
        self.maps_path.setEnabled(False)
        self.maps_path_picker = QPushButton("Select maps directory", self)
        maps_hlayout.addWidget(self.maps_path)
        maps_hlayout.addWidget(self.maps_path_picker)
        self.maps_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("maps", self.maps_path))
        return maps_hlayout
    
    def create_mods_picker(self):
        mods_hlayout: QHBoxLayout = QHBoxLayout()
        self.mods_path = QLineEdit(self)
        self.mods_path.setEnabled(False)
        self.mods_path_picker = QPushButton("Select mods directory", self)
        mods_hlayout.addWidget(self.mods_path)
        mods_hlayout.addWidget(self.mods_path_picker)
        self.mods_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("mods", self.mods_path))
        return mods_hlayout
    
    def create_general_group(self):
        group_box = QGroupBox("General", self)
        vlayout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Default compatibility level"))
        self.default_complevel = QLineEdit(self)
        hbox.addWidget(self.default_complevel)
        vlayout.addLayout(hbox)
        group_box.setLayout(vlayout)
        return group_box


    def clicked_macro_key(self, key):
        print(key.name)

    def create_keys_group(self, cfg: JacodemonConfig):

        group_box = QGroupBox("Keys", self)
        group_box.setFixedWidth(300)
        
        vbox = QVBoxLayout()

        hbox = None
        for idx, obj in enumerate(KeyNames):
            if idx % 4 == 0:
                if hbox is not None:
                    vbox.addLayout(hbox)
                hbox = QHBoxLayout()
            button = QPushButton(obj.name)
            button.setEnabled(obj.enabled)
            button.clicked.connect(lambda checked, obj=obj: self.clicked_macro_key(obj))
            hbox.addWidget(button)

        if hbox is not None:
            vbox.addLayout(hbox)

        group_box.setLayout(vbox)
        return group_box
    
    def create_bindings_group(self, cfg: JacodemonConfig):
        group_box = QGroupBox("Bindings", self)
        vlayout = QVBoxLayout()

        group_box.setLayout(vlayout)
        return group_box

    def OpenDirectoryDialog(self, what, line):
        options = QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, f"Select {what} directory", "", options=options)

        if directory:
            line.setText(directory)

# def OpenConfigDialog():

#     dialog = GeneralTab()
#     cfg: JacodemonConfig = GetConfig()

#     if dialog.exec() == QDialog.DialogCode.Accepted:
#         cfg.iwad_dir = dialog.iwad_path.text()
#         cfg.maps_dir = dialog.maps_path.text()
#         cfg.demo_dir = dialog.demo_path.text()
#         cfg.mods_dir = dialog.mods_path.text()

#         cfg.default_complevel = dialog.default_complevel.text()
#         cfg.set_dsda_path(dialog.dsda_path.text())
#         cfg.dsda_cfg = dialog.dsda_cfg_path.text()
#         cfg.dsdadoom_hud_lump = dialog.dsda_hud_path.text()
#         cfg.play_scene = dialog.play_scene.text()
#         cfg.wait_scene = dialog.wait_scene.text()
#         cfg.browser_scene = dialog.browser_scene.text()
#         cfg.title_source = dialog.title_source.text()
#         # TODO chocolate/crispy inputs
#     else:
#         sys.exit(0)