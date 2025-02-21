from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QFileDialog

from PySide6.QtCore import Signal

from jacodemon.view.components.config.config import ConfigWidget
from PySide6.QtWidgets import QGroupBox

class DsdaTab(ConfigWidget):

    fields_updated = Signal()

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

        self.dsda_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.dsda_cfg_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.dsda_hud_path.textChanged.connect(lambda: self.fields_updated.emit())

        self.AddButtons(vlayout)
    
    def create_dsda_picker(self):
        groupbox: QGroupBox = QGroupBox("Executable")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_path = QLineEdit(self)
        self.dsda_path.setEnabled(True)
        self.dsda_path_picker = QPushButton("Select dsda executable", self)
        vlayout.addWidget(self.dsda_path)
        vlayout.addWidget(self.dsda_path_picker)
        groupbox.setLayout(vlayout)
        return groupbox
    
    def create_dsda_cfg_picker(self):
        groupbox: QGroupBox = QGroupBox("Config")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_cfg_path = QLineEdit(self)
        self.dsda_cfg_path.setEnabled(True)
        self.dsda_cfg_path_picker = QPushButton("Select dsda config file", self)
        vlayout.addWidget(self.dsda_cfg_path)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.dsda_cfg_path_picker)
        self.clear_dsda_cfg_btn = QPushButton("Clear", self)
        hlayout.addWidget(self.clear_dsda_cfg_btn)
        vlayout.addLayout(hlayout)
        groupbox.setLayout(vlayout)
        return groupbox
    
    def create_dsda_hud_picker(self):
        groupbox: QGroupBox = QGroupBox("HUD Lump")
        vlayout: QVBoxLayout = QVBoxLayout()
        self.dsda_hud_path = QLineEdit(self)
        self.dsda_hud_path.setEnabled(True)
        self.dsda_hud_path_picker = QPushButton("Select dsda HUD lump file", self)
        vlayout.addWidget(self.dsda_hud_path)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.dsda_hud_path_picker)
        self.clear_dsda_hud_btn = QPushButton("Clear", self)
        hlayout.addWidget(self.clear_dsda_hud_btn)
        vlayout.addLayout(hlayout)
        groupbox.setLayout(vlayout)
        return groupbox
