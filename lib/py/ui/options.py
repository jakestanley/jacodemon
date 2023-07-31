import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QRadioButton, QGroupBox, QDialogButtonBox, QLabel

from lib.py.options import Options, MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

class OptionsDialog(QDialog):
    def __init__(self, parent=None, options: Options = None):
        super(OptionsDialog, self).__init__(parent)

        if not options:
            print("Error: `options` was not provided")
            sys.exit(2)

        self.options = options
        self.setWindowTitle("Options")

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        # options: demo
        self.checkbox_record_demo = QCheckBox("Record demo lump")
        self.checkbox_record_demo.setChecked(self.options.record_demo)
        layout.addWidget(self.checkbox_record_demo)

        # options: obs
        self.checkbox_obs = QCheckBox("Control OBS")
        self.checkbox_obs.setChecked(self.options.obs)
        layout.addWidget(self.checkbox_obs)

        checkbox_obs_label = QLabel("If unchecked, recording and scene control will be unavailable")
        layout.addWidget(checkbox_obs_label)

        # options: auto-record 
        self.checkbox_auto_record = QCheckBox("Enable auto record")
        self.checkbox_auto_record.setChecked(self.options.auto_record)
        layout.addWidget(self.checkbox_auto_record)

        checkbox_auto_record_label = QLabel("If checked, video recording be started, ended automatically \nand the outputted recording will be renamed")
        layout.addWidget(checkbox_auto_record_label)

        # options: mods
        self.checkbox_mods = QCheckBox("Enable mods")
        self.checkbox_mods.setChecked(self.options.mods)
        layout.addWidget(self.checkbox_mods)

        checkbox_mods_label = QLabel("If unchecked, any configured 'Quality of Life' mods \nwill not be included in the launch configuration")
        layout.addWidget(checkbox_mods_label)

        # options: Source port override TODO implement
        #groupbox_ports = QGroupBox("Source port")
        #checkbox_source_port = QCheckBox("Port")
        #layout.addWidget(checkbox_source_port)

        # options: crispy doom
        self.checkbox_crispy = QCheckBox("Prefer Crispy Doom")
        self.checkbox_crispy.setChecked(self.options.crispy)
        layout.addWidget(self.checkbox_crispy)

        checkbox_crispy_label = QLabel("If playing a Chocolate Doom mod, force it to launch with Crispy Doom")
        layout.addWidget(checkbox_crispy_label)

        # options: music
        self.checkbox_music = QCheckBox("Enable music")
        self.checkbox_music.setChecked(self.options.music)
        layout.addWidget(self.checkbox_music)

        # options: operation modes
        groupbox_modes = self.create_modes_group(options)
        layout.addWidget(groupbox_modes)

        # special controls
        self.checkbox_obs.stateChanged.connect(self.set_obs)
        if (self.options.obs):
            self.checkbox_auto_record.setEnabled(True)

        # confirm or close
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def create_modes_group(self, options: Options):
        groupbox_modes = QGroupBox("Modes")
        vlayout = QVBoxLayout()

        self.radio_normal = QRadioButton("Select", self)
        vlayout.addWidget(self.radio_normal)

        self.radio_random = QRadioButton("Random", self)
        vlayout.addWidget(self.radio_random)

        self.radio_last = QRadioButton("Last", self)
        vlayout.addWidget(self.radio_last)

        self.radio_replay = QRadioButton("Replay", self)
        vlayout.addWidget(self.radio_replay)

        checkbox_replay_label = QLabel("Prompts to select a demo to replay")
        vlayout.addWidget(checkbox_replay_label)

        self.radio_normal.setChecked(options.mode is MODE_NORMAL or (not options.obs and options.mode is MODE_REPLAY))
        self.radio_random.setChecked(options.mode is MODE_RANDOM)
        self.radio_last.setChecked(options.mode is MODE_LAST)
        self.radio_replay.setChecked(options.mode is MODE_REPLAY and options.obs)
        self.radio_replay.setEnabled(options.obs)

        groupbox_modes.setLayout(vlayout)
        return groupbox_modes

    # only use state change methods when other fields are dependent on this value
    def set_obs(self, state):

        value = state == Qt.Checked

        # enable or disable 
        self.checkbox_auto_record.setChecked(self.checkbox_auto_record.isChecked() and value)
        self.checkbox_auto_record.setEnabled(value)
        
        if self.radio_replay.isChecked() and not value:
            self.radio_replay.setChecked(False)
            self.radio_normal.setChecked(True)

        self.radio_replay.setEnabled(value)

    def get_mode(self):
        if self.radio_last.isChecked():
            return MODE_LAST
        elif self.radio_random.isChecked():
            return MODE_RANDOM
        elif self.radio_replay.isChecked():
            return MODE_REPLAY
        else:
            return MODE_NORMAL


def OpenOptionsGui(options: Options):
    app = QApplication([])

    dialog = OptionsDialog(options=options)

    if dialog.exec_() == QDialog.Accepted:
        options.obs = dialog.checkbox_obs.isChecked()
        options.mods = dialog.checkbox_mods.isChecked()
        options.music = dialog.checkbox_music.isChecked()
        options.auto_record = dialog.checkbox_auto_record.isChecked()
        options.record_demo = dialog.checkbox_record_demo.isChecked()
        options.crispy = dialog.checkbox_crispy.isChecked()
        options.mode = dialog.get_mode()
    else:
        sys.exit(0)