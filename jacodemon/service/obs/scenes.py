from jacodemon.service.obs.obs import ObsController
from jacodemon.ui.components.web import OpenDoomWiki
from jacodemon.model.config import JacodemonConfig, GetConfig

"""For when you want to do a bit more complex stuff with an OBS scene"""
class SceneManager():

    def __init__(self, obs: ObsController) -> None:
        self._obs = obs
        self._config: JacodemonConfig = GetConfig()
        self._previous_scene = None

    # TODO use signals for this
    def SwitchToBrowserScene(self):
        # TODO: consider a stack for this, but may be overkill for my needs
        self._previous_scene = self._obs.GetScene()
        self._obs.SetScene(self._config.browser_scene)
        OpenDoomWiki()
        self._obs.SetScene(self._previous_scene)
        self._previous_scene = None
        