# Set up bridge
from lib.py.macros import Macros
from hammerspoon_bridge import LuaBridge

# from http://www.hammerspoon.org/docs/hs.keycodes.html#map
_KEY_NUMPAD_0='pad0'


hs = LuaBridge().proxy().hs

def balls():
    print("balls")

# hs.hotkey.bind(mods, key, [message,] pressedfn, releasedfn, repeatfn)
hs.hotkey.bind([], _KEY_NUMPAD_0, balls)

class MacMacros(Macros):
    def __init__(self, obs):
        super().__init__(obs)