import logging
import os
import sys
import time
from datetime import datetime
from jacodemon.io import IO
from jacodemon.logs import GetLogManager

import obsws_python as obs
from jacodemon.config import JacodemonConfig, GetConfig
from jacodemon.options import Options, GetOptions
from jacodemon.notifications import Notifications, GetNotifications
from jacodemon.io import IO, GetIo

class ObsController:
    def __init__(self,notifications: Notifications, io: IO):
        self.config: JacodemonConfig = GetConfig()
        self.notifications = notifications
        self.io = io
        self._logger = GetLogManager().GetLogger(__name__)

    def _GetReplayName(self):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        return f"{self._demo_name}-REPLAY-{timestamp}"

    def Setup(self):
        try:
            self.obs_client = obs.ReqClient(host='localhost', port=4455, password='')
        except ConnectionRefusedError:
            self._logger.fatal("Unable to connect to OBS. Is it running? Is the Websocket API enabled? Should you have passed the --no-obs argument?")
            sys.exit(1)
        self.obs_client.set_current_program_scene(self.config.wait_scene)
        if not self.obs_client.get_replay_buffer_status().output_active:
            self.notifications.notify("Replay buffer disabled", "That's it really.")

    def IsRecording(self):
        return self.obs_client.get_record_status().output_active

    def StartRecording(self):
        if self.IsRecording():
            self._logger.info("Stopping unrelated recording and waiting 2 seconds")
            self.obs_client.stop_record()
            time.sleep(2)
        self.obs_client.start_record()
        time.sleep(2)

    def CancelRecording(self):
        if self.IsRecording():
            path = self.obs_client.stop_record().output_path
            self.io.RemoveFile(path)
            self.notifications.notify("Cancelled recording", f"Deleted '{path}'")

    def MoveRecording(self, path, new_name):

        if not path:
            self._logger.error(f"Path argument was empty in call to MoveRecording")

        self._logger.debug(f"Moving {path} to {new_name}")
        parent = os.path.dirname(path)
        ext = os.path.splitext(path)[1]
        newpath = os.path.join(parent, f"{new_name}{ext}")
        try:
            self.io.RenameFile(path, newpath)
            self._logger.debug(f"Moved {path} to {newpath}\n")
        except Exception:
            self._logger.error("Failed to move recording")

        return newpath

    def SaveReplayBuffer(self):
        self.obs_client.save_replay_buffer()
        attempts = 0
        while attempts < 10:
            path = self.obs_client.get_last_replay_buffer_replay().saved_replay_path
            if path:
                self._logger.debug(f"Got saved replay path '{path}'")
                return path
            attempts += 1
            self._logger.debug(f"Saved replay path was empty on attempt {attempts}")
            time.sleep(0.2 * attempts)
        self._logger.error("Could not obtain saved replay path")
        return None

    def SaveReplay(self):
        replay_name = self._GetReplayName()
        
        if self.obs_client.get_replay_buffer_status().output_active:
            path = self.SaveReplayBuffer()
            try:
                newpath = self.MoveRecording(path, replay_name)
                self.notifications.notify("Replay saved", f"Saved to '{newpath}'")
            except Exception:
                self._logger.error("Could not save replay")
        else:
            self.notifications.notify("Replay buffer disabled", f"Not saving replay: '{replay_name}'")     

    def StopRecording(self):
        if self.IsRecording():
            path = self.obs_client.stop_record().output_path
        else:
            return

        # TODO toast notification that allows user to delete if they want
        if self._demo_name:
            newpath = self.MoveRecording(path, self._demo_name)
            self.notifications.notify("Recording stopped", f"Saved to '{newpath}'")

    def GetScene(self):
        return self.obs_client.get_current_program_scene().current_program_scene_name

    def SetScene(self, title):
        # TODO handle scene does not exist
        self.obs_client.set_current_program_scene(title)

    def UpdateMapTitle(self, title):
        settings = {'text': title}
        success = self.obs_client.set_input_settings(name=self.config.title_source, settings=settings, overlay=True)
        self._logger.debug(f"Set map title to {title}")

    def SetDemoName(self, name):
        self._demo_name = name

class MockObsController(ObsController):
    def __init__(self, notifications: Notifications):
        super().__init__(notifications=notifications, io=None)

    def Setup(self):
        return

    def IsRecording(self):
        return False

    def StartRecording(self):
        self._logger.warning(f"OBS is disabled. Cannot start recording")

    def CancelRecording(self):
        self._logger.warning(f"OBS is disabled. This CancelRecording call is redundant")

    def MoveRecording(self, path, new_name):
        self._logger.warning(f"OBS is disabled. This MoveRecording call is redundant")

    def SaveReplay(self):
        replay_name = self._GetReplayName()

        self.notifications.notify("OBS is disabled", f"Not saving replay: '{replay_name}'")

    def StopRecording(self):
        return

    def GetScene(self):
        return ""

    def SetScene(self, title):
        self._logger.warning(f"OBS is disabled. Scene requested: '{title}'")

    def UpdateMapTitle(self, title):
        self._logger.warning(f"OBS is disabled. Title provided: '{title}'")

def GetObsController() -> ObsController:
    # TODO if OBS is not running and no-obs flag is NOT 
    #   set, warn with pop up and continue

    options: Options = GetOptions()
    notifications: Notifications = GetNotifications()
    io: IO = GetIo()

    if options.obs:
        obsController = ObsController(notifications, io)
    else:
        obsController = MockObsController(notifications)

    obsController.Setup()

    return obsController
