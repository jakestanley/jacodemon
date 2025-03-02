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

        # disable buttons that aren't allowed during demo replay
        self.view.checkbox_record_demo.setEnabled(self.app_model.GetMode() != LaunchMode.REPLAY_DEMO)
        self.view.checkbox_mods.setEnabled(self.app_model.GetMode() != LaunchMode.REPLAY_DEMO)
        self.view.checkbox_fast.setEnabled(self.app_model.GetMode() != LaunchMode.REPLAY_DEMO)

        # disable buttons OBS conditional buttons
        self.view.checkbox_obs.setEnabled(self.app_model.IsObsAvailable())
        self.view.checkbox_auto_record.setEnabled(self.app_model.IsObsAvailable())

        self.view.checkbox_record_demo.setChecked(self.app_model.IsRecordDemoEnabled())
        self.view.checkbox_obs.setChecked(self.app_model.IsObsEnabled())
        self.view.checkbox_auto_record.setChecked(self.app_model.IsAutoRecordEnabled())
        self.view.checkbox_mods.setChecked(self.app_model.IsModsEnabled())
        self.view.checkbox_music.setChecked(self.app_model.IsMusicEnabled())
        self.view.checkbox_fast.setChecked(self.app_model.IsFastMonstersEnabled())

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    from jacodemon.misc.dummy import DummyArgs
    from jacodemon.model.options import InitialiseOptions
    from jacodemon.model.app import InitialiseAppModel

    app = QApplication([])

    InitialiseOptions(DummyArgs())
    app_model = InitialiseAppModel()
    view = ViewPreLaunch()

    controller = ControllerPreLaunch(app_model, view)
    view.show()
    sys.exit(app.exec())
