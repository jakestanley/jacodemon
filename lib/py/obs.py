import os
import sys
import time

import obsws_python as obs

from lib.py.config import Config

class ObsController:
    def __init__(self, enabled, config: Config):
        self.enabled = enabled
        self.config = config

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

    def IsRecording(self):
        return self.obs_client.get_record_status().output_active

    def StartRecording(self):
        if self.enabled:
            if self.IsRecording():
                self.StopRecording()
            self.obs_client.start_record()
            time.sleep(2)

    def SaveReplay(self, name=None):
        saved = self.obs_client.save_replay_buffer()
        pass

    def StopRecording(self, name=None):
        if self.enabled:
            path = self.obs_client.stop_record().output_path
        else:
            return
        
        parent = os.path.dirname(path)
        ext = os.path.splitext(path)[1]
        newpath = os.path.join(parent, f"{name}{ext}")

        if not name == None:
            print(f"""
    Recording stopped
    Renaming '{path}' to 
    '{newpath}'
            """)

        # Pausing renaming for 5 seconds to allow OBS to release the handle
        time.sleep(5)
        
        os.rename(path, newpath)

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
