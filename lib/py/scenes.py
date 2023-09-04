from lib.py.obs import ObsController
from lib.py.ui.web import OpenDoomWiki
from lib.py.config import Config

"""For when you want to do a bit more complex stuff with an OBS scene"""
class SceneManager():

    def __init__(self, obs: ObsController, config: Config) -> None:
        self._obs = obs
        self._config = config
        self._previous_scene = None

    def SwitchToBrowserScene(self):
        # TODO: consider a stack for this, but may be overkill for my needs
        self._previous_scene = self._obs.GetScene()
        self._obs.SetScene(self._config.browser_scene)
        OpenDoomWiki()
        self._obs.SetScene(self._previous_scene)
        self._previous_scene = None
        