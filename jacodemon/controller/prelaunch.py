from PySide6.QtCore import Qt, QObject, Signal

from jacodemon.model.app import AppModel
from jacodemon.view.prelaunch import ViewPreLaunch

from jacodemon.options import MODE_NORMAL, MODE_RANDOM, MODE_LAST, MODE_REPLAY

class ControllerPreLaunch(QObject):

    accept_signal = Signal()
    reject_signal = Signal()

    record_demo_enabled_changed = Signal(bool)
    record_demo_checkable_changed = Signal(bool)

    # TODO signal on prelaunch
    def __init__(self, app_model: AppModel, view_pre_launch: ViewPreLaunch):
        super().__init__()
        self.app_model = app_model
        self.view = view_pre_launch

        self.view.button_box.accepted.connect(self.accept_signal.emit)
        self.view.button_box.rejected.connect(self.reject_signal.emit)

        self.app_model.mode_changed.connect(self.refresh)

        # self.view.checkbox_record_demo.stateChanged.connect(self.on_checkbox_toggled)
        # self.view.checkbox_obs.stateChanged.connect(self.on_checkbox_toggled)
        # self.view.checkbox_auto_record.stateChanged.connect(self.on_checkbox_toggled)
        # self.view.checkbox_mods.stateChanged.connect(self.on_checkbox_toggled)
        # self.view.checkbox_music.stateChanged.connect(self.on_checkbox_toggled)

        self.refresh()

    def refresh(self):
        self.view.checkbox_record_demo.setChecked(self.app_model.IsRecordDemoEnabled())
        self.view.checkbox_record_demo.setEnabled(self.app_model.CanRecordDemo())

        self.view.checkbox_obs.setEnabled(self.app_model.CanControlObs())
        self.view.checkbox_obs.setChecked(self.app_model.IsObsEnabled())

        self.view.checkbox_auto_record.setChecked(self.app_model.IsAutoRecordEnabled())
        self.view.checkbox_auto_record.setEnabled(self.app_model.CanAutoRecord())

        self.view.checkbox_mods.setChecked(self.app_model.IsModsEnabled())

        self.view.checkbox_music.setChecked(self.app_model.IsMusicEnabled())

        # TODO: these have been removed or moved. commented for reference later
        # self.view.radio_normal.toggled.connect(self.set_mode)
        # self.view.radio_random.toggled.connect(self.set_mode)
        # self.view.radio_last.toggled.connect(self.set_mode)
        # self.view.radio_replay.toggled.connect(self.set_mode)

        # self.view.ll_debug.setChecked("DEBUG" in app_model.options.stdout_log_level)
        # self.view.ll_info.setChecked("INFO" in app_model.options.stdout_log_level)
        # self.view.ll_warning.setChecked("WARNING" in app_model.options.stdout_log_level or "WARN" in app_model.options.stdout_log_level)
        # self.view.ll_error.setChecked("ERROR" in app_model.options.stdout_log_level)

    def _SetObs(self, state):

        obs_checked = state == Qt.CheckState.Checked

        # enable or disable 
        self.view.checkbox_auto_record.setChecked(self.checkbox_auto_record.isChecked() and obs_checked)
        self.view.checkbox_auto_record.setEnabled(obs_checked)

    def _GetMode(self):
        if self.view.radio_last.isChecked():
            return MODE_LAST
        elif self.view.radio_random.isChecked():
            return MODE_RANDOM
        elif self.view.radio_replay.isChecked():
            return MODE_REPLAY
        else:
            return MODE_NORMAL
        
    def _SetMode(self):

        # TODO setters and getters on the view? consult the model?
        if self.view.radio_replay.isChecked() and self.view.checkbox_record_demo.isChecked():
            self.view.checkbox_record_demo.setChecked(False)

        self.view.checkbox_record_demo.setEnabled(not self.view.radio_replay.isChecked())

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.arguments import DummyArgs
    from jacodemon.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewPreLaunch()

    controller = ControllerPreLaunch(app_model, view)
    view.show()
    sys.exit(app.exec())
