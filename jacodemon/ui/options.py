import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton, QGroupBox, QDialogButtonBox, QLabel

from jacodemon.options import Options, MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

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
        self.checkbox_record_demo.setChecked(self.options.record_demo and not self.options.mode == MODE_REPLAY)
        self.checkbox_record_demo.setEnabled(self.options.mode != MODE_REPLAY)
        layout.addWidget(self.checkbox_record_demo)

        # options: obs
        self.checkbox_obs = QCheckBox("Control OBS")
        self.checkbox_obs.setChecked(self.options.obs)
        layout.addWidget(self.checkbox_obs)

        checkbox_obs_label = QLabel("If unchecked, recording and scene control will be unavailable")
        layout.addWidget(checkbox_obs_label)

        # options: auto-record 
        self.checkbox_auto_record = QCheckBox("Enable auto record")
        self.checkbox_auto_record.setChecked(self.options.auto_record and self.options.obs)
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

        # options: logging levels
        groupbox_logging_levels = self.create_logging_levels_group(options)
        layout.addWidget(groupbox_logging_levels)

        # special controls
        self.checkbox_obs.stateChanged.connect(self.set_obs)
        self.checkbox_auto_record.setEnabled(self.options.obs)

        # confirm or close
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
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

        self.radio_normal.setChecked(options.mode is MODE_NORMAL)
        self.radio_random.setChecked(options.mode is MODE_RANDOM)
        self.radio_last.setChecked(options.mode is MODE_LAST)
        self.radio_replay.setChecked(options.mode is MODE_REPLAY)

        self.radio_normal.toggled.connect(self.set_mode)
        self.radio_random.toggled.connect(self.set_mode)
        self.radio_last.toggled.connect(self.set_mode)
        self.radio_replay.toggled.connect(self.set_mode)

        groupbox_modes.setLayout(vlayout)
        return groupbox_modes

    def create_logging_levels_group(self, options: Options):
        groupbox = QGroupBox("Logging")
        hlayout = QHBoxLayout()

        self.ll_debug = QRadioButton("DEBUG")
        self.ll_debug.setChecked("DEBUG" in options.stdout_log_level)
        hlayout.addWidget(self.ll_debug)

        self.ll_info = QRadioButton("INFO")
        self.ll_info.setChecked("INFO" in options.stdout_log_level)
        hlayout.addWidget(self.ll_info)

        self.ll_warning = QRadioButton("WARN")
        self.ll_warning.setChecked("WARNING" in options.stdout_log_level or "WARN" in options.stdout_log_level)
        hlayout.addWidget(self.ll_warning)

        self.ll_error = QRadioButton("ERROR")
        self.ll_error.setChecked("ERROR" in options.stdout_log_level)
        hlayout.addWidget(self.ll_error)

        groupbox.setLayout(hlayout)
        return groupbox

    # only use state change methods when other fields are dependent on this value
    def set_obs(self, state):

        obs_checked = state == Qt.CheckState.Checked

        # enable or disable 
        self.checkbox_auto_record.setChecked(self.checkbox_auto_record.isChecked() and obs_checked)
        self.checkbox_auto_record.setEnabled(obs_checked)

    def set_mode(self):

        if self.radio_replay.isChecked() and self.checkbox_record_demo.isChecked():
            self.checkbox_record_demo.setChecked(False)

        self.checkbox_record_demo.setEnabled(not self.radio_replay.isChecked())

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

    dialog = OptionsDialog(options=options)

    if dialog.exec() == QDialog.DialogCode.Accepted:
        options.obs = dialog.checkbox_obs.isChecked()
        options.mods = dialog.checkbox_mods.isChecked()
        options.music = dialog.checkbox_music.isChecked()
        options.auto_record = dialog.checkbox_auto_record.isChecked()
        options.record_demo = dialog.checkbox_record_demo.isChecked()
        options.crispy = dialog.checkbox_crispy.isChecked()
        options.mode = dialog.get_mode()
        options.stdout_log_level = next(radio.text() for radio in [dialog.ll_info, dialog.ll_warning, dialog.ll_debug, dialog.ll_error] if radio.isChecked())
    else:
        sys.exit(0)