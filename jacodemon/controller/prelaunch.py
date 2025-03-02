from PySide6.QtCore import QObject, Signal

from jacodemon.model.app import AppModel
from jacodemon.model.launch import LaunchMode
from jacodemon.view.prelaunch import ViewPreLaunch

class ControllerPreLaunch(QObject):

    accept_signal = Signal()
    reject_signal = Signal()

    def __init__(self, app_model: AppModel, view_pre_launch: ViewPreLaunch):
        super().__init__()
        self.app_model = app_model
        self.app_model.mode_changed.connect(self.refresh)

        self.view = view_pre_launch

        self.view.button_box.accepted.connect(self.on_accept)
        self.view.button_box.rejected.connect(self.reject_signal.emit)

        self.refresh()

    def on_accept(self):

        # we don't "save" the options until we launch
        self.app_model.options.auto_record = self.view.checkbox_auto_record.isChecked()
        self.app_model.options.record_demo = self.view.checkbox_record_demo.isChecked()
        self.app_model.options.obs = self.view.checkbox_obs.isChecked()
        self.app_model.options.mods = self.view.checkbox_mods.isChecked()
        self.app_model.options.music = self.view.checkbox_music.isChecked()
        self.app_model.options.fast = self.view.checkbox_fast.isChecked()

        self.accept_signal.emit()

    def refresh(self):

        # TODO: this sucks
        self.view.checkbox_record_demo.setChecked(self.app_model.IsRecordDemoEnabled())
        self.view.checkbox_record_demo.setEnabled(self.app_model.CanRecordDemo())

        self.view.checkbox_obs.setChecked(self.app_model.IsObsEnabled())
        self.view.checkbox_obs.setEnabled(self.app_model.CanControlObs())

        self.view.checkbox_auto_record.setChecked(self.app_model.IsAutoRecordEnabled())
        self.view.checkbox_auto_record.setEnabled(self.app_model.CanAutoRecord())

        self.view.checkbox_mods.setChecked(self.app_model.IsModsEnabled())
        self.view.checkbox_mods.setEnabled(self.app_model.GetMode() != LaunchMode.REPLAY_DEMO)

        self.view.checkbox_music.setChecked(self.app_model.IsMusicEnabled())
        self.view.checkbox_fast.setChecked(self.app_model.IsFastMonstersEnabled())

        # TODO: these have been removed or moved. commented for reference later
        # self.view.radio_normal.toggled.connect(self.set_mode)
        # self.view.radio_random.toggled.connect(self.set_mode)
        # self.view.radio_last.toggled.connect(self.set_mode)
        # self.view.radio_replay.toggled.connect(self.set_mode)

        # self.view.ll_debug.setChecked("DEBUG" in app_model.options.stdout_log_level)
        # self.view.ll_info.setChecked("INFO" in app_model.options.stdout_log_level)
        # self.view.ll_warning.setChecked("WARNING" in app_model.options.stdout_log_level or "WARN" in app_model.options.stdout_log_level)
        # self.view.ll_error.setChecked("ERROR" in app_model.options.stdout_log_level)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.arguments import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewPreLaunch()

    controller = ControllerPreLaunch(app_model, view)
    view.show()
    sys.exit(app.exec())
