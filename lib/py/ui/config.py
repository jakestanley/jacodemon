import sys

from lib.py.config import Config, Mod
from lib.py.macros import KeyNames

from PyQt5.QtWidgets import QApplication, \
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QDialogButtonBox, QGroupBox, QLabel, QListWidget, QListWidgetItem, QCheckBox

class ConfigDialog(QDialog):
    def __init__(self, cfg: Config, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowTitle("Configure")
        self.setGeometry(100, 100, 800, 200)

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        general_group = self.create_general_group(cfg)
        directories_group = self.create_directories_group(cfg)
        dsda_group = self.create_dsda_group(cfg)
        obs_group = self.create_obs_group(cfg)
        macros_group = QGroupBox("Macros", self)
        macros_layout = QHBoxLayout()
        macros_layout.addWidget(self.create_keys_group(cfg))
        macros_layout.addWidget(self.create_bindings_group(cfg))
        macros_group.setLayout(macros_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(general_group)
        layout.addWidget(directories_group)
        layout.addWidget(dsda_group)
        layout.addWidget(obs_group)
        layout.addWidget(macros_group)
        layout.addWidget(button_box)

    def FixedQPushButton(self, text: str) -> QPushButton:
        button = QPushButton(text, self)
        button.setFixedWidth(64)
        return button

    def create_directories_group(self, cfg):
        group_box = QGroupBox("Directories", self)
        vlayout = QVBoxLayout()

        iwad_hlayout = self.create_iwad_picker(cfg)
        maps_hlayout = self.create_maps_picker(cfg)
        demo_hlayout = self.create_demo_picker(cfg)
        qol_layout = self.create_qol_layout(cfg)

        vlayout.addLayout(iwad_hlayout)
        vlayout.addLayout(maps_hlayout)
        vlayout.addLayout(demo_hlayout)

        vlayout.addWidget(QLabel("Mods"))
        vlayout.addLayout(qol_layout)

        group_box.setLayout(vlayout)
        return group_box

    def create_demo_picker(self, cfg):
        demo_hlayout: QHBoxLayout = QHBoxLayout()
        self.demo_path = QLineEdit(self)
        self.demo_path.setText(cfg.demo_dir)
        self.demo_path.setEnabled(False)
        self.demo_path_picker = QPushButton("Select demos directory", self)
        demo_hlayout.addWidget(self.demo_path)
        demo_hlayout.addWidget(self.demo_path_picker)
        self.demo_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("demos", self.demo_path))
        return demo_hlayout

    def create_iwad_picker(self, cfg):
        iwad_hlayout: QHBoxLayout = QHBoxLayout()
        self.iwad_path = QLineEdit(self)
        self.iwad_path.setText(cfg.iwad_dir)
        self.iwad_path.setEnabled(False)
        self.iwad_path_picker = QPushButton("Select IWAD directory", self)
        iwad_hlayout.addWidget(self.iwad_path)
        iwad_hlayout.addWidget(self.iwad_path_picker)
        self.iwad_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("IWAD", self.iwad_path))
        return iwad_hlayout

    def create_maps_picker(self, cfg):
        maps_hlayout: QHBoxLayout = QHBoxLayout()
        self.maps_path = QLineEdit(self)
        self.maps_path.setText(cfg.maps_dir)
        self.maps_path.setEnabled(False)
        self.maps_path_picker = QPushButton("Select maps directory", self)
        maps_hlayout.addWidget(self.maps_path)
        maps_hlayout.addWidget(self.maps_path_picker)
        self.maps_path_picker.clicked.connect(lambda: self.OpenDirectoryDialog("maps", self.maps_path))
        return maps_hlayout
    
    def create_qol_layout(self, cfg: Config):
        layout: QHBoxLayout = QHBoxLayout()

        self.mods = QListWidget(self)

        for mod in cfg.mods:
            self.AddMod(mod)

        layout.addWidget(self.mods)

        button_layout: QVBoxLayout = QVBoxLayout()

        btn_add_mods: QPushButton = QPushButton("Add")
        btn_add_mods.clicked.connect(self.AddMods)
        button_layout.addWidget(btn_add_mods)        

        btn_remove_mods: QPushButton = QPushButton("Remove")
        btn_remove_mods.clicked.connect(self.RemoveMods)
        button_layout.addWidget(btn_remove_mods)

        layout.addLayout(button_layout)
        return layout
    
    def create_dsda_picker(self, cfg):
        hlayout: QHBoxLayout = QHBoxLayout()
        self.dsda_path = QLineEdit(self)
        self.dsda_path.setText(cfg.dsda_path)
        self.dsda_path.setEnabled(False)
        # is self required for these?
        self.dsda_path_picker = QPushButton("Select dsda executable", self)
        self.dsda_path_picker.clicked.connect(lambda: self.OpenSingleFileDialog("All Files (*)", self.dsda_path))
        hlayout.addWidget(self.dsda_path)
        hlayout.addWidget(self.dsda_path_picker)
        return hlayout
    
    def create_dsda_cfg_picker(self, cfg):
        hlayout: QHBoxLayout = QHBoxLayout()
        self.dsda_cfg_path = QLineEdit(self)
        self.dsda_cfg_path.setText(cfg.dsda_cfg)
        self.dsda_cfg_path.setEnabled(False)
        self.dsda_cfg_path_picker = QPushButton("Select dsda config file", self)
        self.dsda_cfg_path_picker.clicked.connect(lambda: self.OpenSingleFileDialog("All Files (*);;Text Files (*.cfg)", self.dsda_cfg_path))
        hlayout.addWidget(self.dsda_cfg_path)
        hlayout.addWidget(self.dsda_cfg_path_picker)
        return hlayout
    
    def create_general_group(self, cfg):
        group_box = QGroupBox("General", self)
        vlayout = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Default compatibility level"))
        self.default_complevel = QLineEdit(self)
        self.default_complevel.setText(cfg.default_complevel)
        hbox.addWidget(self.default_complevel)

        vlayout.addLayout(hbox)
        group_box.setLayout(vlayout)
        return group_box
    
    def create_dsda_group(self, cfg):
        group_box = QGroupBox("DSDA Doom", self)
        vlayout = QVBoxLayout()

        dsda = self.create_dsda_picker(cfg)
        vlayout.addLayout(dsda)

        dsda_config = self.create_dsda_cfg_picker(cfg)
        vlayout.addLayout(dsda_config)

        group_box.setLayout(vlayout)
        return group_box
    
    def create_obs_group(self, cfg: Config):
        # TODO complete test button functionality
        group_box = QGroupBox("OBS", self)
        vlayout = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("play_scene"))
        self.play_scene = QLineEdit(self)
        self.play_scene.setText(cfg.play_scene)
        hbox.addWidget(self.play_scene)
        self.btn_test_play_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_play_scene)

        vlayout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("wait_scene"))
        self.wait_scene = QLineEdit(self)
        self.wait_scene.setText(cfg.wait_scene)
        hbox.addWidget(self.wait_scene)
        self.btn_test_wait_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_wait_scene)
        vlayout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("browser_scene"))
        self.browser_scene = QLineEdit(self)
        self.browser_scene.setText(cfg.browser_scene)
        hbox.addWidget(self.browser_scene)
        self.btn_test_browser_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_browser_scene)
        vlayout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("title_source"))
        self.title_source = QLineEdit(self)
        self.title_source.setText(cfg.title_source)
        hbox.addWidget(self.title_source)
        self.btn_test_title_source = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_title_source)
        vlayout.addLayout(hbox)

        group_box.setLayout(vlayout)
        return group_box

    def clicked_macro_key(self, key):
        print(key.name)

    def create_keys_group(self, cfg: Config):

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
    
    def create_bindings_group(self, cfg: Config):
        group_box = QGroupBox("Bindings", self)
        vlayout = QVBoxLayout()

        group_box.setLayout(vlayout)
        return group_box

    def AddMod(self, mod: Mod):
        item = QListWidgetItem(self.mods)
        checkbox = QCheckBox(mod.path)
        checkbox.setChecked(mod.enabled)
        self.mods.setItemWidget(item, checkbox)

    def AddMods(self):

        files = self.OpenManyFilesDialog()
        for file in files:
            self.AddMod(Mod(file))

    def RemoveMods(self):

        for item in self.mods.selectedItems():
            self.mods.takeItem(self.mods.row(item))

    def OpenManyFilesDialog(self):
        options = QFileDialog.Option()
        files, _ = QFileDialog.getOpenFileNames(self, "Add Files", "", options=options)

        return files

    def OpenSingleFileDialog(self, types, line):
        options = QFileDialog.Option()
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", types, options=options)

        if file:
            line.setText(file)

    def OpenDirectoryDialog(self, what, line):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly

        directory = QFileDialog.getExistingDirectory(self, f"Select {what} directory", "", options=options)

        if directory:
            line.setText(directory)

def OpenConfigDialog(cfg: Config):
    app = QApplication([])

    dialog = ConfigDialog(cfg)

    if dialog.exec_() == QDialog.Accepted:
        cfg.iwad_dir = dialog.iwad_path.text()
        cfg.maps_dir = dialog.maps_path.text()
        cfg.demo_dir = dialog.demo_path.text()
        cfg.mods = []
        for index in range(dialog.mods.count()):
            item = dialog.mods.item(index)
            checkbox = dialog.mods.itemWidget(item)
            path = checkbox.text()
            enabled = checkbox.isChecked()
            cfg.mods.append(Mod(path, enabled))
        cfg.default_complevel = dialog.default_complevel.text()
        cfg.set_dsda_path(dialog.dsda_path.text())
        cfg.dsda_cfg = dialog.dsda_cfg_path.text()
        cfg.play_scene = dialog.play_scene.text()
        cfg.wait_scene = dialog.wait_scene.text()
        cfg.browser_scene = dialog.browser_scene.text()
        cfg.title_source = dialog.title_source.text()
        # TODO chocolate/crispy inputs
    else:
        sys.exit(0)