from PySide6.QtWidgets import QApplication

from jacodemon.arguments import GetArgs
from jacodemon.options import InitialiseOptions

from jacodemon.service.config_service import ConfigService
from jacodemon.service.map_set_service import MapSetService

from jacodemon.config import GetConfig
from jacodemon.ui.manager import UIManager, UIState

from jacodemon.model.app import AppModel, InitialiseAppModel

from jacodemon.ui.controller.config import ControllerConfig
from jacodemon.ui.controller.mapselect import ControllerMapSelect
from jacodemon.ui.controller.prelaunch import ControllerPreLaunch

from jacodemon.ui.view.config import ViewConfig
from jacodemon.ui.view.mapselect import ViewMapSelect
from jacodemon.ui.view.prelaunch import ViewPreLaunch

from jacodemon.app import AppController

def start():

    InitialiseOptions(GetArgs())

    app_model: AppModel = InitialiseAppModel()

    app = QApplication([])
    ui_manager = UIManager()

    view_config     = ViewConfig()
    view_map_select = ViewMapSelect()
    view_pre_launch = ViewPreLaunch()

    presenter_config = ControllerConfig(app_model, view_config)
    presenter_map_select = ControllerMapSelect(app_model, view_map_select)
    presenter_pre_launch = ControllerPreLaunch(app_model, view_pre_launch)

    # NOTE: can subscribe to any app_model event emissions in the dialog constructors
    ui_manager.register_view(UIState.CONFIG,        view_config)
    # ui_manager.register_view(UIState.SELECT_MAP,    ) # TODO don't use this, make it public instead of "OpenMapDialog"
    # ui_manager.register_view(UIState.PRE_LAUNCH,    )

    # force all appmodel signals to emit, which should refresh all UIs
    app_model.update()

    controller = AppController()

    ui_manager.show()
    app.exec()

if __name__ == "__main__":
    start()