from jacodemon.ui.components.config.config import ConfigWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QFileDialog

from jacodemon.model.mod import Mod
from jacodemon.model.app import AppModel

from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.misc.files import FindDoomFiles

class ModsTab(ConfigWidget):
    def __init__(self, parent=None):
        super(ModsTab, self).__init__(parent)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)

        self.mods = QListWidget(self)

        hlayout.addWidget(self.mods)

        button_layout: QVBoxLayout = QVBoxLayout()

        btn_add_mods: QPushButton = QPushButton("Add")
        
        button_layout.addWidget(btn_add_mods)        

        btn_remove_mods: QPushButton = QPushButton("Remove")
        
        button_layout.addWidget(btn_remove_mods)

        button_layout.addStretch()

        hlayout.addLayout(button_layout)
        self.layout.addLayout(hlayout)

        self.AddButtons(self.layout)

    # TODO port over to controller
    # def save(self):
    #     cfg: JacodemonConfig = GetConfig()
    #     cfg.mods = []
    #     for index in range(self.mods.count()):
    #         item = self.mods.item(index)
    #         checkbox = self.mods.itemWidget(item)
    #         path = checkbox.text()
    #         enabled = checkbox.isChecked()
    #         cfg.mods.append(Mod(path, enabled))
    #     cfg.Save()

    # def revert(self):
    #     self.LoadValuesFromConfig()

    # def AddMod(self, mod: Mod):
    #     item = QListWidgetItem(self.mods)
    #     checkbox = QCheckBox(mod.path)
    #     checkbox.setChecked(mod.enabled)
    #     self.mods.setItemWidget(item, checkbox)

    # def AddMods(self):

    #     files = FindDoomFiles(GetConfig().mods_dir)
    #     for file in files:
    #         self.AddMod(Mod(file))

    # def RemoveMods(self):

    #     for item in self.mods.selectedItems():
    #         self.mods.takeItem(self.mods.row(item))

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = ModsTab()
    widget.show()
    sys.exit(app.exec())
