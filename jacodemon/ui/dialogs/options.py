import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton, QGroupBox, QDialogButtonBox, QLabel, QDialog

from jacodemon.options import Options, GetOptions, MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create an instance of your custom widget
        self.options_widget = OptionsWidget(self)
        layout.addWidget(self.options_widget)
        
        # confirm or close
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class OptionsWidget(QWidget):
    def __init__(self, parent=None):
        super(OptionsWidget, self).__init__(parent)

        self.setWindowTitle("Options")

        # build layout
        layout: QVBoxLayout = QVBoxLayout(self)

        # options: demo
        self.checkbox_record_demo = QCheckBox("Record demo lump")
        self.checkbox_record_demo.setChecked(GetOptions().record_demo and not GetOptions().mode == MODE_REPLAY)
        self.checkbox_record_demo.setEnabled(GetOptions().mode != MODE_REPLAY)
        layout.addWidget(self.checkbox_record_demo)

        # options: obs
        self.checkbox_obs = QCheckBox("Control OBS")
        self.checkbox_obs.setChecked(GetOptions().obs)
        self.checkbox_obs.setToolTip("If unchecked, OBS will not be controlled")
        layout.addWidget(self.checkbox_obs)

        # options: auto-record 
        self.checkbox_auto_record = QCheckBox("Enable auto record")
        self.checkbox_auto_record.setChecked(GetOptions().auto_record and GetOptions().obs)
        self.checkbox_auto_record.setToolTip("If unchecked, video recording will not be started automatically")
        layout.addWidget(self.checkbox_auto_record)

        # options: mods
        self.checkbox_mods = QCheckBox("Enable mods")
        self.checkbox_mods.setToolTip("If unchecked, any configured 'Quality of Life' mods \nwill not be included in the launch configuration")
        self.checkbox_mods.setChecked(GetOptions().mods)
        layout.addWidget(self.checkbox_mods)

        # options: music
        self.checkbox_music = QCheckBox("Enable music")
        self.checkbox_music.setChecked(GetOptions().music)
        layout.addWidget(self.checkbox_music)

        # special controls
        self.checkbox_obs.stateChanged.connect(self.set_obs)
        self.checkbox_auto_record.setEnabled(GetOptions().obs)

    def create_modes_group(self):
        groupbox_modes = QGroupBox("Modes")
        vlayout = QVBoxLayout()

        self.radio_normal = QRadioButton("Select", self)
        vlayout.addWidget(self.radio_normal)

        self.radio_random = QRadioButton("Random", self)
        vlayout.addWidget(self.radio_random)

        self.radio_last = QRadioButton("Last", self)
        vlayout.addWidget(self.radio_last)

        self.radio_replay = QRadioButton("Replay", self)
        self.radio_replay.setToolTip("Prompts to select a demo to replay")
        vlayout.addWidget(self.radio_replay)

        self.radio_normal.setChecked(GetOptions().mode is MODE_NORMAL)
        self.radio_random.setChecked(GetOptions().mode is MODE_RANDOM)
        self.radio_last.setChecked(GetOptions().mode is MODE_LAST)
        self.radio_replay.setChecked(GetOptions().mode is MODE_REPLAY)

        self.radio_normal.toggled.connect(self.set_mode)
        self.radio_random.toggled.connect(self.set_mode)
        self.radio_last.toggled.connect(self.set_mode)
        self.radio_replay.toggled.connect(self.set_mode)

        groupbox_modes.setLayout(vlayout)
        return groupbox_modes

    def create_logging_levels_group(self):
        groupbox = QGroupBox("Logging")
        vlayout = QVBoxLayout()

        self.ll_debug = QRadioButton("DEBUG")
        self.ll_debug.setChecked("DEBUG" in GetOptions().stdout_log_level)
        vlayout.addWidget(self.ll_debug)

        self.ll_info = QRadioButton("INFO")
        self.ll_info.setChecked("INFO" in GetOptions().stdout_log_level)
        vlayout.addWidget(self.ll_info)

        self.ll_warning = QRadioButton("WARN")
        self.ll_warning.setChecked("WARNING" in GetOptions().stdout_log_level or "WARN" in GetOptions().stdout_log_level)
        vlayout.addWidget(self.ll_warning)

        self.ll_error = QRadioButton("ERROR")
        self.ll_error.setChecked("ERROR" in GetOptions().stdout_log_level)
        vlayout.addWidget(self.ll_error)

        groupbox.setLayout(vlayout)
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


def OpenOptionsDialog():

    dialog = OptionsDialog()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        ow = dialog.options_widget
        GetOptions().obs                 = ow.checkbox_obs.isChecked()
        GetOptions().mods                = ow.checkbox_mods.isChecked()
        GetOptions().music               = ow.checkbox_music.isChecked()
        GetOptions().auto_record         = ow.checkbox_auto_record.isChecked()
        GetOptions().record_demo         = ow.checkbox_record_demo.isChecked()
    else:
        sys.exit(0)