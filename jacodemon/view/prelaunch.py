from PySide6.QtWidgets import QVBoxLayout, QCheckBox, QRadioButton, QGroupBox, QDialogButtonBox, QGroupBox, QDialog

class ViewPreLaunch(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prelaunch Options")

        layout = QVBoxLayout(self)
        
        groupbox = QGroupBox("Game")
        groupbox.setLayout(QVBoxLayout())

        self.checkbox_record_demo = QCheckBox("Record demo lump")

        self.checkbox_mods = QCheckBox("Enable mods")
        self.checkbox_mods.setToolTip("If unchecked, any configured 'Quality of Life' mods \nwill not be included in the launch configuration")
        self.checkbox_fast = QCheckBox("Enable fast monsters")

        groupbox.layout().addWidget(self.checkbox_record_demo)
        groupbox.layout().addWidget(self.checkbox_mods)
        groupbox.layout().addWidget(self.checkbox_fast)
        
        layout.addWidget(groupbox)

        # options: obs
        groupbox = QGroupBox("Recording && Streaming")
        groupbox.setLayout(QVBoxLayout())

        self.checkbox_obs = QCheckBox("Control OBS")
        self.checkbox_obs.setToolTip("If unchecked, OBS will not be controlled")

        # options: auto-record 
        self.checkbox_auto_record = QCheckBox("Enable auto record")
        self.checkbox_auto_record.setToolTip("If unchecked, video recording will not be started automatically")

        # options: music
        self.checkbox_music = QCheckBox("Enable music")
        self.checkbox_music.setToolTip("Game music will be disabled if unchecked")
        
        groupbox.layout().addWidget(self.checkbox_obs)
        groupbox.layout().addWidget(self.checkbox_auto_record)
        groupbox.layout().addWidget(self.checkbox_music)

        layout.addWidget(groupbox)

        layout.addStretch()

        # confirm or close
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

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

        groupbox_modes.setLayout(vlayout)
        return groupbox_modes

    def create_logging_levels_group(self):
        groupbox = QGroupBox("Logging")
        vlayout = QVBoxLayout()

        self.ll_debug = QRadioButton("DEBUG")
        vlayout.addWidget(self.ll_debug)

        self.ll_info = QRadioButton("INFO")
        vlayout.addWidget(self.ll_info)

        self.ll_warning = QRadioButton("WARN")
        vlayout.addWidget(self.ll_warning)

        self.ll_error = QRadioButton("ERROR")
        vlayout.addWidget(self.ll_error)

        groupbox.setLayout(vlayout)
        return groupbox

# for testing the view layout only
if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])
    dialog = ViewPreLaunch()
    sys.exit(dialog.exec())
