#!/usr/bin/env python3
import threading
import queue
import time
import subprocess
import sys

from PySide6.QtWidgets import QApplication, QDialog
from jacodemon.arguments import GetArgs
from jacodemon.logs import GetLogManager
from jacodemon.view.config import ViewConfig
from jacodemon.signaling import Signaling, SWITCH_TO_BROWSER_SCENE
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.last import *
from jacodemon.launch import LaunchConfig
from jacodemon.service.obs.obs import ObsController, GetObsController
from jacodemon.options import Options, InitialiseOptions, GetOptions, MODE_LAST, MODE_REPLAY
from jacodemon.service.dsda.stats import Statistics, NewStatistics
from jacodemon.model.mapset import MapSet
from jacodemon.controller.maps.select import MapsSelectController, GetMapsSelectController
from jacodemon.ui.view.mapselect import OpenSelectMapDialog
from jacodemon.ui.view.prelaunch import OpenOptionsDialog
from jacodemon.model.demo import GetDemosForMap
from jacodemon.macros import Macros, GetMacros
from jacodemon.service.obs.scenes import SceneManager

from jacodemon.keys import *

def GetMap():

    if not GetMapsSelectController().mapSet:
        cd = ViewConfig()
        
        if cd.exec() == QDialog.DialogCode.Rejected:
            logger = GetLogManager().GetLogger(__name__)
            logger.debug("ConfigDialog was closed. Exiting normally")
            sys.exit(0)

        # if user clicked play last, override and set it to be sure
        if cd.last:
            GetOptions().mode = MODE_LAST

    demo_index = None
    if GetOptions().last():
        map = GetLastMap()
    else:
        map, demo_index = OpenSelectMapDialog()

    if demo_index is not None:
        GetOptions().mode = MODE_REPLAY

    return map, demo_index

def main():

    # signaling stuff
    ui_queue = queue.Queue()
    signaling = Signaling(ui_queue)

    # because of the different modes of operation, you must specify which 
    #   args. in this script's case, it's the default args
    InitialiseOptions(GetArgs())

    # set up logging now that we have options
    logger = GetLogManager().GetLogger(__name__)
    logger.debug("Starting application...")

    # prepare the QApplication context for its first (potential) usage
    QApplication([])

    # set up OBS on app launch, before any config in case we're streamin'
    obsController: ObsController = GetObsController()
    sceneManager = SceneManager(obsController)
    obsController.SetScene(GetConfig().wait_scene)
    
    # check if last option is provided and if so, select that map
    map = None
    if GetOptions().last():
        map = GetLastMap()

    while (True):

        # if last wasn't used, or it was and there was no last map selected, then 
        #   run the usual start window
        if not map:
            while(map is None):
                map, demo_index = GetMap()

        # allow player to view and edit provided options before launch
        OpenOptionsDialog()

        # if we're selecting the last map or replaying a demo, don't save
        if GetOptions().last() or GetOptions().replay():
            pass
        else:
            # for next time last is used, save the selected map
            logger.debug("Saving selected map for next time")
            SaveSelectedMap(map, GetMapsSelectController().mapSet.id)

        launch = LaunchConfig()
        if GetMapsSelectController().mapSet:
            launch.set_map_set(GetMapsSelectController().mapSet.id)
        else:
            # TODO: this triggers badges load, but on return after game close, badges are not reloaded
            GetMapsSelectController().Open(map.MapSetId)
        launch.set_map_set(GetMapsSelectController().mapSet)
        launch.set_map(map)

        if GetOptions().replay():
            demo = GetDemosForMap(map, GetConfig().demo_dir)[demo_index]
            demo_name = demo.name
            launch.set_replay(demo)
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

        map = None

if __name__ == "__main__":
    main()
