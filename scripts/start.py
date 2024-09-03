#!/usr/bin/env python3
import threading
import queue
import time
import subprocess

from PySide6.QtWidgets import QApplication
import jacodemon.arguments as args
import jacodemon.logs as logs
from jacodemon.ui.main import MainWindow
from jacodemon.signaling import Signaling, SWITCH_TO_BROWSER_SCENE
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.csv import load_raw_maps, load_raw_maps_from_wad
from jacodemon.last import *
from jacodemon.launch import LaunchConfig
from jacodemon.obs import *
from jacodemon.options import Options
from jacodemon.stats import Statistics, NewStatistics
from jacodemon.ui.demoselect import OpenDemoSelection
from jacodemon.ui.mapselect import OpenMapSelection
from jacodemon.demo import GetDemosForMap, AddBadgesToMap
from jacodemon.macros import Macros, GetMacros
from jacodemon.notifications import Notifications, GetNotifications
from jacodemon.io import IO, GetIo
from jacodemon.scenes import SceneManager
from jacodemon.keys import *
from jacodemon.map import EnrichMaps
from jacodemon.controller.sets.select import SelectSetController, GetSetController
from jacodemon.controller.maps.select import MapsSelectController, GetMapsSelectController

def main():

    ui_queue = queue.Queue()
    signaling = Signaling(ui_queue)
    options: Options = args.get_args()

    # set up logging now that we have arguments
    app = QApplication(sys.argv)
    logs.configure()
    logs.InitLogManager(options)
    logger = logs.GetLogManager().GetLogger(__name__)
    logger.info("Starting application...")

    config: JacodemonConfig = GetConfig()

    # TODO reimplement in new layout
    # if last selected, skip the gui
    # if not options.last():
        # OpenConfigDialog()
        # config.Save()
# 
        # OpenOptionsGui(options)

    # reset logging configuration after options
    logger = logs.GetLogManager().GetLogger(__name__)

    notifications: Notifications = GetNotifications()
    io: IO = GetIo()
    launch = LaunchConfig(options)

    # TODO if OBS is not running and no-obs flag is NOT 
    #   set, warn with pop up and continue
    if options.obs:
        obsController = ObsController(notifications, io)
    else:
        obsController = NoObsController(notifications)

    obsController.Setup()
    sceneManager = SceneManager(obsController)

    obsController.SetScene(config.wait_scene)

    map = None
    if options.last():
        map = GetLastMap()

    mainWindow = MainWindow(options)
    GetSetController().SetMainWindow(mainWindow)
    mainWindow.show()
    rt = app.exec()

    OpenMapSelection(GetMapsSelectController().maps)

    # TODO this is all trash now
    if not map:

        if options.wad:
            raw_maps = load_raw_maps_from_wad(options.wad)
        else:
            raw_maps = load_raw_maps(options.playlist)

        maps = EnrichMaps(config, raw_maps)

        for map in maps:
            AddBadgesToMap(map, config.demo_dir)

        if options.random():
            import random
            map = random.choice(maps)
        else:
            map = OpenMapSelection(maps)

    if not map:
        logger.info("A map was not selected. Exiting normally")
        sys.exit(0)

    if options.replay():
        demos = GetDemosForMap(map, config.demo_dir)
        demo = OpenDemoSelection(demos)
        if not demo:
            logger.info("A demo was not selected. Exiting normally")
            sys.exit(0)
    elif not options.random():
        SaveSelectedMap(map)

    launch.set_map(map)

    if options.replay():
        demo_name = demo.name
        launch.set_replay(demo.path)
    else:
        demo_name = launch.get_demo_name()

    command = launch.get_command()

    obsController.SetScene(config.play_scene)
    obsController.UpdateMapTitle(f"{map.ModName}: {map.GetTitle()}")
    obsController.SetDemoName(demo_name)

    macros: Macros = GetMacros()
    # TODO move this to configuration somehow
    macros.add_hotkey_callback(KEY_NUMPAD_0, callback=obsController.SaveReplay)
    macros.add_hotkey_callback(KEY_DOT, callback=obsController.CancelRecording)
    macros.add_hotkey_callback(KEY_DEL, callback=obsController.CancelRecording)
    macros.add_hotkey_callback(KEY_NUMPAD_3, callback=signaling.SwitchToBrowserScene)
    macros.listen()

    if options.auto_record:
        obsController.StartRecording()

    if not options.replay():
        statistics: Statistics = NewStatistics(launch, config.demo_dir)

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
    if not options.replay():
        statistics.set_level_stats()
        statistics.write_stats()

    if options.auto_record:
        obsController.StopRecording()

    obsController.SetScene(config.wait_scene)

if __name__ == "__main__":
    main()
