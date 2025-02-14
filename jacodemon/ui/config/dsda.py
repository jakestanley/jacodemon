from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QFileDialog

from jacodemon.ui.config.config import ConfigWidget
from jacodemon.config import JacodemonConfig, GetConfig
from PySide6.QtWidgets import QGroupBox

class DsdaTab(ConfigWidget):
    def __init__(self, parent=None):
        super(DsdaTab, self).__init__(parent)

        vlayout = QVBoxLayout(self)

        dsda = self.create_dsda_picker()
        vlayout.addWidget(dsda)

        dsda_config = self.create_dsda_cfg_picker()
        vlayout.addWidget(dsda_config)

        dsda_hud = self.create_dsda_hud_picker()
        vlayout.addWidget(dsda_hud)
        vlayout.addStretch()

        self.AddButtons(vlayout)
        self.LoadValuesFromConfig()

    def save(self):
        cfg: JacodemonConfig = GetConfig()

        cfg.dsda_path = self.dsda_path.text()
        cfg.dsda_cfg = self.dsda_cfg_path.text()
        cfg.dsdadoom_hud_lump = self.dsda_hud_path.text()
        cfg.Save()

    def revert(self):
        self.LoadValuesFromConfig()

    def LoadValuesFromConfig(self):
        cfg: JacodemonConfig = GetConfig()

        self.dsda_path.setText(cfg.dsda_path)
        self.dsda_cfg_path.setText(cfg.dsda_cfg)
        self.dsda_hud_path.setText(cfg.dsdadoom_hud_lump)
    
    def create_dsda_picker(self):
        groupbox: QGroupBox = QGroupBox("Executable")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_path = QLineEdit(self)
        self.dsda_path.setEnabled(True)
        # is self required for these?
        self.dsda_path_picker = QPushButton("Select dsda executable", self)
        self.dsda_path_picker.clicked.connect(lambda: self.OpenSingleFileDialog("All Files (*)", self.dsda_path))
        vlayout.addWidget(self.dsda_path)
        vlayout.addWidget(self.dsda_path_picker)
        groupbox.setLayout(vlayout)
        return groupbox
    
    def create_dsda_cfg_picker(self):
        groupbox: QGroupBox = QGroupBox("Config")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_cfg_path = QLineEdit(self)
        self.dsda_cfg_path.setEnabled(False)
        self.dsda_cfg_path_picker = QPushButton("Select dsda config file", self)
        self.dsda_cfg_path_picker.clicked.connect(lambda: self.OpenSingleFileDialog("All Files (*);;Text Files (*.cfg)", self.dsda_cfg_path))
        vlayout.addWidget(self.dsda_cfg_path)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.dsda_cfg_path_picker)
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(lambda: self.dsda_cfg_path.clear())
        hlayout.addWidget(clear_button)
        vlayout.addLayout(hlayout)
        groupbox.setLayout(vlayout)
        return groupbox
    
    def create_dsda_hud_picker(self):
        groupbox: QGroupBox = QGroupBox("HUD Lump")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_hud_path = QLineEdit(self)
        self.dsda_hud_path.setEnabled(False)
        self.dsda_hud_path_picker = QPushButton("Select dsda HUD lump file", self)
        self.dsda_hud_path_picker.clicked.connect(lambda: self.OpenSingleFileDialog("All Files (*);;LUMP Files (*.lmp)", self.dsda_hud_path))
        vlayout.addWidget(self.dsda_hud_path)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.dsda_hud_path_picker)
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(lambda: self.dsda_hud_path.clear())
        hlayout.addWidget(clear_button)
        vlayout.addLayout(hlayout)
        groupbox.setLayout(vlayout)
        return groupbox
    
    def OpenSingleFileDialog(self, types, line):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", types)

        if file:
            line.setText(file)
