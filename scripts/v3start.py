import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from jacodemon.arguments import GetArgs
from jacodemon.model.options import InitialiseOptions
from jacodemon.misc.logs import InitialiseLoggingConfig

from jacodemon.manager import UIManager, UIState

from jacodemon.wiring.context import Context, InitialiseContext
from jacodemon.model.app import AppModel, InitialiseAppModel

from jacodemon.service.obs_service import ObsServiceException

from jacodemon.controller.config import ControllerConfig
from jacodemon.controller.mapselect import ControllerMapSelect
from jacodemon.controller.prelaunch import ControllerPreLaunch

from jacodemon.view.config import ViewConfig
from jacodemon.view.mapselect import ViewMapSelect
from jacodemon.view.prelaunch import ViewPreLaunch

def run(app_model: AppModel, ui_manager: UIManager):
    app_model.Launch()
    # TODO ensure demos, badges and stats are refreshed
    ui_manager.set_state(UIState.SELECT_MAP)

def start():

    args = GetArgs()
    InitialiseOptions(args)
    InitialiseLoggingConfig(args.stdout_log_level.upper())

    app = QApplication([])
    InitialiseContext()

    try:
        app_model: AppModel = InitialiseAppModel()
    except ObsServiceException as e:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(e.cause)
        msg_box.setWindowTitle("Error")
        msg_box.exec()
        sys.exit(1)
    
    ui_manager = UIManager()

    view_config     = ViewConfig()
    view_map_select = ViewMapSelect()
    view_pre_launch = ViewPreLaunch()

    controller_config = ControllerConfig(app_model, view_config)
    controller_config.accept_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_MAP))
    controller_config.last_signal.connect(lambda: ui_manager.set_state(UIState.PRE_LAUNCH))

    controller_map_select = ControllerMapSelect(app_model, view_map_select)
    controller_map_select.accept_signal.connect(lambda: ui_manager.set_state(UIState.PRE_LAUNCH))
    controller_map_select.reject_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_SET))

    controller_pre_launch = ControllerPreLaunch(app_model, view_pre_launch)
    controller_pre_launch.accept_signal.connect(lambda: run(app_model, ui_manager))
    controller_pre_launch.reject_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_MAP))

    ui_manager.register_view(UIState.SELECT_SET,    view_config)
    ui_manager.register_view(UIState.SELECT_MAP,    view_map_select)
    ui_manager.register_view(UIState.PRE_LAUNCH,    view_pre_launch)

    # force all appmodel signals to emit, which should refresh all UIs
    app_model.update()

    ui_manager.show()
    app.exec()

if __name__ == "__main__":
    start()
