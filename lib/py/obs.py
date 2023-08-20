import os
import sys
import time
from datetime import datetime
from lib.py.io import IO

import obsws_python as obs

from lib.py.config import Config
from lib.py.notifications import Notifications

class ObsController:
    def __init__(self, enabled, config: Config, notifications: Notifications, io: IO):
        self.enabled = enabled
        self.config = config
        self.notifications = notifications
        self.io = io

    def Setup(self):
        if self.enabled:
            try:
                self.obs_client = obs.ReqClient(host='localhost', port=4455, password='')
            except ConnectionRefusedError:
                print("""
    Unable to connect to OBS. Is it running? 
    Is the Websocket API enabled? 
    Should you have passed the --no-obs argument?
                    """)
                sys.exit(1)
            scenes = self.obs_client.get_scene_list()
            self.obs_client.set_current_program_scene(self.config.wait_scene)
            if not self.obs_client.get_replay_buffer_status().output_active:
                print("Replay buffer disabled")

    def IsRecording(self):
        return self.obs_client.get_record_status().output_active

    def StartRecording(self):
        if self.enabled:
            if self.IsRecording():
                print("Stopping unrelated recording and waiting 2 seconds")
                self.obs_client.stop_record()
                time.sleep(2)
            self.obs_client.start_record()
            time.sleep(2)

    def CancelRecording(self):
        if self.enabled and self.IsRecording():
            path = self.obs_client.stop_record().output_path
            self.io.RemoveFile(path)
            self.notifications.notify("Cancelled recording", f"Deleted '{path}'")

    def MoveRecording(self, path, new_name):

        parent = os.path.dirname(path)
        ext = os.path.splitext(path)[1]
        newpath = os.path.join(parent, f"{new_name}{ext}")
        self.io.RenameFile(path, newpath)

        return newpath

    def SaveReplay(self):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        replay_name = f"{self._demo_name}-REPLAY-{timestamp}"
        if self.enabled:
            if self.obs_client.get_replay_buffer_status().output_active:
                self.obs_client.save_replay_buffer()
                path = self.obs_client.get_last_replay_buffer_replay().saved_replay_path
                newpath = self.MoveRecording(path, replay_name)
                self.notifications.notify("Replay saved", f"Saved to '{newpath}'")
            else:
                self.notifications.notify("Replay buffer disabled", f"Not saving replay: '{replay_name}'")
        else:
            self.notifications.notify("OBS is disabled", f"Not saving replay: '{replay_name}'")

    def StopRecording(self):
        if self.enabled and self.IsRecording():
            path = self.obs_client.stop_record().output_path
        else:
            return

        # TODO toast notification that allows user to delete if they want
        if self._demo_name:
            newpath = self.MoveRecording(path, self._demo_name)
            self.notifications.notify("Recording stopped", f"Saved to '{newpath}'")

    def GetScene(self):
        # TODO consider dummy OBS class/interface so we don't have to keep doing this
        if self.enabled:
            return self.obs_client.get_current_program_scene()

    def SetScene(self, title):
        if self.enabled:
            self.obs_client.set_current_program_scene(title)
        else:
            print(f"OBS is disabled. Scene requested: '{title}'")

    def UpdateMapTitle(self, title):
        if self.enabled:
            settings = {'text': title}
            success = self.obs_client.set_input_settings(name=self.config.title_source, settings=settings, overlay=True)
            print(f"Set map title to {title}")
        else:
            print(f"OBS is disabled. Title provided: '{title}'")

    def SetDemoName(self, name):
        self._demo_name = name

class EnabledObsController(ObsController):
    def __init__(self) -> None:
        pass
