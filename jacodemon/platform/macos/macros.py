# Set up bridge
from jacodemon.macros import Macros
from hammerspoon_bridge import LuaBridge

# from http://www.hammerspoon.org/docs/hs.keycodes.html#map
_KEY_NUMPAD_0='pad0'

class MacMacros(Macros):
    
    def balls():
        print("balls")

    def __init__(self):
        super().__init__()
        self.macros_enabled: bool = True
        try:
            self.hs = LuaBridge().proxy().hs
            # self.hs.hotkey.bind(mods, key, [message,] pressedfn, releasedfn, repeatfn)
            self.hs.hotkey.bind([], _KEY_NUMPAD_0, self.balls)
        except:
            self.macros_enabled = False
            print("unable to initialise macro bridge")

