import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QGroupBox, QDialogButtonBox, QLabel

from lib.py.options import Options

class OptionsDialog(QDialog):
    def __init__(self, parent=None, options=None):
        super(OptionsDialog, self).__init__(parent)
        self.options = options
        self.setWindowTitle("Options")

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        # options: demo
        checkbox_record_demo = QCheckBox("Record demo")
        checkbox_record_demo.setChecked(self.options.record_demo)
        checkbox_record_demo.stateChanged.connect(lambda state: self.set_demo(state == Qt.Checked))
        layout.addWidget(checkbox_record_demo)

        # options: obs
        checkbox_obs = QCheckBox("Control OBS")
        layout.addWidget(checkbox_obs)

        checkbox_obs_label = QLabel("If unchecked, recording and scene control will be unavailable")
        layout.addWidget(checkbox_obs_label)

        # options: auto-record 
        checkbox_auto_record = QCheckBox("Enable auto record")
        checkbox_auto_record.setChecked(self.options.auto_record)
        checkbox_auto_record.stateChanged.connect(lambda state: self.set_auto_record(state == Qt.Checked))
        layout.addWidget(checkbox_auto_record)

        checkbox_auto_record_label = QLabel("If checked, video recording be started, ended automatically \nand the outputted recording will be renamed")
        layout.addWidget(checkbox_auto_record_label)

        # options: re-record (currently not implemented)
        # checkbox_re_record = QCheckBox("re_record")
        # layout.addWidget(checkbox_re_record)

        # options: mods
        checkbox_mods = QCheckBox("Enable mods")
        checkbox_mods.setChecked(self.options.mods)
        checkbox_mods.stateChanged.connect(lambda state: self.set_mods(state == Qt.Checked))
        layout.addWidget(checkbox_mods)

        checkbox_mods_label = QLabel("If unchecked, any configured 'Quality of Life' mods \nwill not be included in the launch configuration")
        layout.addWidget(checkbox_mods_label)

        # options: Source port override TODO implement
        #groupbox_ports = QGroupBox("Source port")
        #checkbox_source_port = QCheckBox("Port")
        #layout.addWidget(checkbox_source_port)

        # options: crispy doom
        checkbox_crispy = QCheckBox("Prefer Crispy Doom")
        checkbox_crispy.setChecked(self.options.crispy)
        checkbox_crispy.stateChanged.connect(lambda state: self.set_crispy(state == Qt.Checked))
        layout.addWidget(checkbox_crispy)

        # options: music
        checkbox_music = QCheckBox("Enable music")
        checkbox_music.setChecked(self.options.music)
        checkbox_music.stateChanged.connect(lambda state: self.set_music(state == Qt.Checked))
        layout.addWidget(checkbox_music)

        checkbox_crispy_label = QLabel("If playing a Chocolate Doom mod, force it to launch with Crispy Doom")
        layout.addWidget(checkbox_crispy_label)

        # options: last
        checkbox_last = QCheckBox("Last")
        checkbox_last.setChecked(self.options.last)
        checkbox_last.stateChanged.connect(lambda state: self.set_last(state == Qt.Checked))
        layout.addWidget(checkbox_last)

        checkbox_last_label = QLabel("Play the previously selected map")
        layout.addWidget(checkbox_last_label)

        # options: random
        checkbox_random = QCheckBox("Random")
        checkbox_random.setChecked(self.options.random)
        checkbox_random.stateChanged.connect(lambda state: self.set_random(state == Qt.Checked))
        layout.addWidget(checkbox_random)

        checkbox_random_label = QLabel("Play a random map from the provided mod list")
        layout.addWidget(checkbox_random_label)

        checkbox_demo_label = QLabel("If unchecked, no demo lump will be created for this session")
        layout.addWidget(checkbox_demo_label)

        # special controls
        checkbox_obs.setChecked(self.options.obs)
        checkbox_obs.stateChanged.connect(lambda state: self.set_obs(state == Qt.Checked, [checkbox_auto_record]))
        if (self.options.obs):
            checkbox_auto_record.setEnabled(True)

        # confirm or close
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


    def set_last(self, value):
        self.options.last = value

    def set_obs(self, value, disables):
        self.options.obs = value
        for disable in disables:
            disable.setEnabled(value)

    def set_crispy(self, value):
        self.options.crispy = value

    def set_music(self, value):
        self.options.music = value

    def set_auto_record(self, value):
        self.options.auto_record = value

    def set_mods(self, value):
        self.options.mods = value

    def set_random(self, value):
        self.options.random = value

    def set_demo(self, value):
        self.options.record_demo = value


def OpenOptionsGui(options: Options):
    app = QApplication([])

    dialog = OptionsDialog(options=options)

    if dialog.exec_() == QDialog.Accepted:
        pass
    else:
        sys.exit(0)