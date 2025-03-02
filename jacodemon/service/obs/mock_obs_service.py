from jacodemon.service.obs_service import ObsService
from jacodemon.model.config import JacodemonConfig

class MockObsService(ObsService):

    def __init__(self, config: JacodemonConfig):
        super().__init__(config=config, fake=True)
        self._logger.warning("OBS is disabled. MockObsService is being used")
    # def __init__(self, notifications: Notifications):
        # super().__init__(notifications=notifications, io=None)

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
