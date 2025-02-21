from jacodemon.view.components.config.config import ConfigWidget

from PySide6.QtCore import Signal

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QGroupBox, QLabel

class GeneralTab(ConfigWidget):

    fields_updated = Signal()

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

        self.demo_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.iwad_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.maps_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.mods_path.textChanged.connect(lambda: self.fields_updated.emit())
        self.default_complevel.textChanged.connect(lambda: self.fields_updated.emit())

        self.AddButtons(layout)

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
        
        self.demo_path_picker = QPushButton("Select demos directory", self)
        demo_hlayout.addWidget(self.demo_path)
        demo_hlayout.addWidget(self.demo_path_picker)
        
        return demo_hlayout

    def create_iwad_picker(self):
        iwad_hlayout: QHBoxLayout = QHBoxLayout()
        self.iwad_path = QLineEdit(self)
        
        self.iwad_path_picker = QPushButton("Select IWAD directory", self)
        iwad_hlayout.addWidget(self.iwad_path)
        iwad_hlayout.addWidget(self.iwad_path_picker)
        
        return iwad_hlayout

    def create_maps_picker(self):
        maps_hlayout: QHBoxLayout = QHBoxLayout()
        self.maps_path = QLineEdit(self)
        self.maps_path_picker = QPushButton("Select maps directory", self)
        maps_hlayout.addWidget(self.maps_path)
        maps_hlayout.addWidget(self.maps_path_picker)
        
        return maps_hlayout
    
    def create_mods_picker(self):
        mods_hlayout: QHBoxLayout = QHBoxLayout()
        self.mods_path = QLineEdit(self)
        self.mods_path_picker = QPushButton("Select mods directory", self)
        mods_hlayout.addWidget(self.mods_path)
        mods_hlayout.addWidget(self.mods_path_picker)
        
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
    
    def create_bindings_group(self):
        group_box = QGroupBox("Bindings", self)
        vlayout = QVBoxLayout()

        group_box.setLayout(vlayout)
        return group_box

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = GeneralTab()
    widget.show()
    sys.exit(app.exec())
