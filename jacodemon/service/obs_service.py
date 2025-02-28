import logging

import os
import sys
import time
from datetime import datetime
from jacodemon.misc.io import IO

import obsws_python as obs
from jacodemon.model.options import Options, GetOptions
from jacodemon.model.config import JacodemonConfig
from jacodemon.notifications import Notifications, GetNotifications
from jacodemon.misc.io import IO, GetIo
from jacodemon.exceptions import ObsServiceException

from PySide6.QtWidgets import QMessageBox

class ObsService:
    # TODO: v3 -> notifications re-write
    # def __init__(self,notifications: Notifications, io: IO):
    def __init__(self, config: JacodemonConfig, fake=False):
        self.config: JacodemonConfig = config
        # self.notifications = notifications
        # self.io = io
        self._logger = logging.getLogger(self.__class__.__name__)
        if fake:
            return
        try:
            self.obs_client = obs.ReqClient(host='localhost', port=4455, password='')
            # if not self.obs_client.get_replay_buffer_status().output_active:
                # self.notifications.notify("OBS replay buffer is not active")
        except ConnectionRefusedError as cause:
            self._logger.error("Connection to OBS refused. Is it running? Is the Websocket API enabled?")
            raise ObsServiceException("Connection to OBS refused. Is it running? Is the Websocket API enabled? If it is desired to run without OBS, please use the --no-obs flag")
        # catch all other exceptions
        except Exception as cause:
            raise ObsServiceException(cause)

    def _GetReplayName(self):
        # TODO use the one from the launch spec
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        return f"{self._demo_name}-REPLAY-{timestamp}"

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

def PromptUserContinueExit():
    message_box = QMessageBox()

    message_box.setWindowTitle("OBS is unavailable")
    message_box.setText("OBS is not running and the --no-obs flag was not set. Would you like to continue anyway?")

    continue_button = message_box.addButton("Continue", QMessageBox.AcceptRole)
    exit_button = message_box.addButton("Exit", QMessageBox.RejectRole)
    
    # Execute the dialog and get the user's response
    message_box.exec()

    if message_box.clickedButton() == continue_button:
        return True
    elif message_box.clickedButton() == exit_button:
        return False

def GetObsController() -> ObsService:

    options: Options = GetOptions()
    notifications: Notifications = GetNotifications()
    io: IO = GetIo()

    if options.obs:
        try:
            obsController = ObsService(notifications, io)
            obsController.Setup()
        except ObsServiceException:
            # TODO reuse this
            if PromptUserContinueExit():
                obsController = MockObsService(notifications)
            else:
                sys.exit(0)
    else:
        obsController = MockObsService(notifications)

    return obsController
