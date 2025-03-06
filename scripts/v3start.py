import sys

from PySide6.QtWidgets import QApplication

from jacodemon.arguments import GetArgs
from jacodemon.model.options import InitialiseOptions
from jacodemon.misc.logs import InitialiseLoggingConfig

from jacodemon.manager import UIManager, UIState

from jacodemon.service.registry import Registry, RegisterServices, RegisterObsService
from jacodemon.model.app import AppModel

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

def CreateViewsControllers(ui_manager: UIManager, app_model: AppModel):
    view_config     = ViewConfig()
    view_map_select = ViewMapSelect()
    view_pre_launch = ViewPreLaunch()

    controller_config = ControllerConfig(app_model, view_config)
    ui_manager.controllers.append(controller_config)
    controller_config.accept_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_MAP))
    controller_config.last_signal.connect(lambda: ui_manager.set_state(UIState.PRE_LAUNCH))

    controller_map_select = ControllerMapSelect(app_model, view_map_select)
    ui_manager.controllers.append(controller_map_select)
    controller_map_select.accept_signal.connect(lambda: ui_manager.set_state(UIState.PRE_LAUNCH))
    controller_map_select.reject_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_SET))

    controller_pre_launch = ControllerPreLaunch(app_model, view_pre_launch)
    ui_manager.controllers.append(controller_pre_launch)
    controller_pre_launch.accept_signal.connect(lambda: run(app_model, ui_manager))
    controller_pre_launch.reject_signal.connect(lambda: ui_manager.set_state(UIState.SELECT_MAP))

    ui_manager.register_view(UIState.SELECT_SET,    view_config)
    ui_manager.register_view(UIState.SELECT_MAP,    view_map_select)
    ui_manager.register_view(UIState.PRE_LAUNCH,    view_pre_launch)

def start():

    # get command line arguments and set up options and logging
    args = GetArgs()
    InitialiseOptions(args)
    InitialiseLoggingConfig(args.stdout_log_level.upper())

    # i guess create the QApplication now because from here on we'll be using QObject
    app = QApplication([])

    # instantiate and register the services but do not initialise them yet 
    #   as that will call listeners, and we want to rely on those for the 
    #   listeners are connected on the ui
    RegisterServices()
    if RegisterObsService() == False:
        sys.exit(1)

    # create the app model which doesn't really do much any more
    app_model: AppModel = AppModel()
    
    # create the ui manager and initialise views and controllers
    ui_manager = UIManager()
    CreateViewsControllers(ui_manager, app_model)

    # now we can initialise services which will trigger listeners and should 
    #   update the now instantiated UI elements
    Registry.InitialiseServices()

    # finally, let's show the UI and exec the app
    ui_manager.show()
    app.exec()

if __name__ == "__main__":
    start()
