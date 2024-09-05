#!/usr/bin/env python3
import threading
import queue
import time
import subprocess
import sys

from PySide6.QtWidgets import QApplication, QDialog
from jacodemon.arguments import GetArgs
from jacodemon.logs import GetLogManager
from jacodemon.ui.dialogs.config import OpenConfigDialog
from jacodemon.signaling import Signaling, SWITCH_TO_BROWSER_SCENE
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.last import *
from jacodemon.launch import LaunchConfig
from jacodemon.obs import ObsController, GetObsController
from jacodemon.options import Options, InitialiseOptions, GetOptions
from jacodemon.stats import Statistics, NewStatistics
from jacodemon.model.maps import MapSet
from jacodemon.controller.maps.select import MapsSelectController, GetMapsSelectController
from jacodemon.ui.demoselect import OpenDemoSelection
from jacodemon.ui.mapselect import OpenMapSelection
from jacodemon.ui.options import OpenOptionsDialog
from jacodemon.demo import GetDemosForMap
from jacodemon.macros import Macros, GetMacros
from jacodemon.scenes import SceneManager

from jacodemon.keys import *

def main():

    # signaling stuff
    ui_queue = queue.Queue()
    signaling = Signaling(ui_queue)

    # because of the different modes of operation, you must specify which 
    #   args. in this script's case, it's the default args
    InitialiseOptions(GetArgs())

    # set up logging now that we have options
    logger = GetLogManager().GetLogger(__name__)
    logger.info("Starting application...")

    # set up OBS on app launch, before any config in case we're streamin'
    obsController: ObsController = GetObsController()
    sceneManager = SceneManager(obsController)
    obsController.SetScene(GetConfig().wait_scene)
    
    # check if last option is provided and if so, select that map
    map = None
    if GetOptions().last():
        map = GetLastMap()

    # prepare the QApplication context for its first (potential) usage
    app = QApplication([])

    # if last wasn't used, or it was and there was no last map selected, then 
    #   run the usual start window
    if not map:

        # TODO wrap this in a function, like OpenMapSelection below
        if OpenConfigDialog() == QDialog.DialogCode.Rejected:
            logger.info("ConfigDialog was closed. Exiting normally")
            sys.exit(0)

        # GetSetController().SetMainWindow(mainWindow)
        # if mainWindow.exec() != QDialog.DialogCode.Accepted:
        #     sys.exit(0)

        map = OpenMapSelection()

    if not map:
        logger.info("A map was not selected. Exiting normally")
        sys.exit(0)

    # allow player to view and edit provided options before launch
    OpenOptionsDialog()

    # if replay is enabled, we need to select a demo for the map
    # TODO: this is probably massively broken with the rewrite. FIXME
    if GetOptions().replay():
        demos = GetDemosForMap(map, GetConfig().demo_dir)
        demo = OpenDemoSelection(demos)
        if not demo:
            logger.info("A demo was not selected. Exiting normally")
            sys.exit(0)
    else:
        # for next time last is used, save the selected map
        logger.debug("Saving selected map for next time")
        SaveSelectedMap(map)

    launch = LaunchConfig()
    launch.set_map_set(GetMapsSelectController().mapSet)
    launch.set_map(map)

    if GetOptions().replay():
        demo_name = demo.name
        launch.set_replay(demo.path)
    else:
        demo_name = launch.get_demo_name()

    command = launch.get_command()

    # prepare OBS, the game is about to start
    obsController.SetScene(GetConfig().play_scene)
    obsController.UpdateMapTitle(f"{map.ModName}: {map.GetTitle()}")
    obsController.SetDemoName(demo_name)

    macros: Macros = GetMacros()
    # TODO move this to configuration somehow
    macros.add_hotkey_callback(KEY_NUMPAD_0, callback=obsController.SaveReplay)
    macros.add_hotkey_callback(KEY_DOT, callback=obsController.CancelRecording)
    macros.add_hotkey_callback(KEY_DEL, callback=obsController.CancelRecording)
    macros.add_hotkey_callback(KEY_NUMPAD_3, callback=signaling.SwitchToBrowserScene)
    macros.listen()

    if GetOptions().auto_record:
        obsController.StartRecording()

    if not GetOptions().replay():
        statistics: Statistics = NewStatistics(launch, GetConfig().demo_dir)

    logger.debug(f"Running command: {' '.join(command)}")
    subprocess_thread = threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    subprocess_thread.start()

    # process events that require main thread, i.e UI stuff
    # TODO could this be in the signaling class?
    while subprocess_thread.is_alive():
        if ui_queue.empty():
            time.sleep(1)
        else:
            signal = ui_queue.get()
            if signal == SWITCH_TO_BROWSER_SCENE:
                sceneManager.SwitchToBrowserScene() # blocking

    # update stats and save
    if not GetOptions().replay():
        statistics.set_level_stats()
        statistics.write_stats()

    if GetOptions().auto_record:
        # TODO: handle recording already stopped, maybe manually or by error
        obsController.StopRecording()

    obsController.SetScene(GetConfig().wait_scene)

if __name__ == "__main__":
    main()
