from jacodemon.view.components.config.config import ConfigWidget

from PySide6.QtCore import Signal

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QFileDialog

from jacodemon.model.mod import Mod
from jacodemon.model.app import AppModel

from jacodemon.model.config import JacodemonConfig, GetConfig
from jacodemon.misc.files import FindDoomFiles

class ModsTab(ConfigWidget):

    row_selected = Signal(int)
    row_toggled = Signal(int, bool)
    row_removed = Signal()

    def __init__(self, parent=None):
        super(ModsTab, self).__init__(parent)

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        hlayout = QHBoxLayout()

        self.mods = QListWidget(self)
        self.mods.setSelectionBehavior(QListWidget.SelectRows)
        self.mods.setSelectionMode(QListWidget.SingleSelection)
        self.mods.selectionModel().selectionChanged.connect(self.on_selection_changed)

        hlayout.addWidget(self.mods)
        hlayout.addLayout(self.create_side_layout())

        layout.addLayout(hlayout)

        self.AddButtons(layout)

    def on_selection_changed(self, selected, _):
        if selected.indexes():  # Ensure there's a selection
            row = selected.indexes()[0].row()  # Extract row index
            self.row_selected.emit(row)  # Emit the row index

    def create_side_layout(self):
        side_layout = QVBoxLayout()

        self.btn_add_mods = QPushButton("Add Mods")
        self.btn_remove_mods = QPushButton("Remove Mods")

        side_layout.addWidget(self.btn_add_mods)
        side_layout.addWidget(self.btn_remove_mods)

        side_layout.addStretch()

        return side_layout
    
    def AddMod(self, mod: Mod, index: int):
        item = QListWidgetItem(self.mods)
        checkbox = QCheckBox(mod.path)
        checkbox.setChecked(mod.enabled)
        checkbox.stateChanged.connect(lambda state, x=index: self.row_toggled.emit(x, state == 2))
        self.mods.setItemWidget(item, checkbox)

    def SetMods(self, mods: list[Mod]):
        self.mods.clear()
        for index, mod in enumerate(mods):
            self.AddMod(mod, index)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = ModsTab()
    widget.show()
    sys.exit(app.exec())
