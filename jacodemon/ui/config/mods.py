from jacodemon.ui.config.config import ConfigWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QFileDialog

from jacodemon.config import JacodemonConfig, GetConfig, Mod
from jacodemon.files import FindDoomFiles

class ModsDialog(ConfigWidget):
    def __init__(self, parent=None):
        super(ModsDialog, self).__init__(parent)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)

        self.mods = QListWidget(self)

        hlayout.addWidget(self.mods)

        button_layout: QVBoxLayout = QVBoxLayout()

        btn_add_mods: QPushButton = QPushButton("Add")
        btn_add_mods.clicked.connect(self.AddMods)
        button_layout.addWidget(btn_add_mods)        

        btn_remove_mods: QPushButton = QPushButton("Remove")
        btn_remove_mods.clicked.connect(self.RemoveMods)
        button_layout.addWidget(btn_remove_mods)

        button_layout.addStretch()

        hlayout.addLayout(button_layout)
        self.layout.addLayout(hlayout)

        self.AddButtons(self.layout)
        self.LoadValuesFromConfig()

    def LoadValuesFromConfig(self):

        cfg: JacodemonConfig = GetConfig()

        self.mods.clear()
        for mod in cfg.mods:
            self.AddMod(mod)

    def save(self):
        cfg: JacodemonConfig = GetConfig()
        cfg.mods = []
        for index in range(self.mods.count()):
            item = self.mods.item(index)
            checkbox = self.mods.itemWidget(item)
            path = checkbox.text()
            enabled = checkbox.isChecked()
            cfg.mods.append(Mod(path, enabled))
        cfg.Save()

    def revert(self):
        self.LoadValuesFromConfig()

    def AddMod(self, mod: Mod):
        item = QListWidgetItem(self.mods)
        checkbox = QCheckBox(mod.path)
        checkbox.setChecked(mod.enabled)
        self.mods.setItemWidget(item, checkbox)

    def AddMods(self):

        files = FindDoomFiles(GetConfig().mods_dir)
        for file in files:
            self.AddMod(Mod(file))

    def RemoveMods(self):

        for item in self.mods.selectedItems():
            self.mods.takeItem(self.mods.row(item))
