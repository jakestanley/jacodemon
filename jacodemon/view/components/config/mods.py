from jacodemon.view.components.config.config import ConfigWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QFileDialog

from jacodemon.model.mod import Mod
from jacodemon.model.app import AppModel

from jacodemon.model.config import JacodemonConfig, GetConfig
from jacodemon.misc.files import FindDoomFiles

class ModsTab(ConfigWidget):
    def __init__(self, parent=None):
        super(ModsTab, self).__init__(parent)

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        hlayout = QHBoxLayout()

        self.mods = QListWidget(self)

        hlayout.addWidget(self.mods)
        hlayout.addLayout(self.create_side_layout())

        layout.addLayout(hlayout)

        self.AddButtons(layout)

    def create_side_layout(self):
        side_layout = QVBoxLayout()

        self.btn_add_mods = QPushButton("Add Mods")
        self.btn_remove_mods = QPushButton("Remove Mods")

        side_layout.addWidget(self.btn_add_mods)
        side_layout.addWidget(self.btn_remove_mods)

        side_layout.addStretch()

        return side_layout

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
