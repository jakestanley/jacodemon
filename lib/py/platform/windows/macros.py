# https://pypi.org/project/ahk/
from lib.py.keys import *
from lib.py.macros import Macros
from ahk import AHK

# from https://www.autohotkey.com/docs/v1/KeyList.htm
# I use the Jellycomb external numpad
KeyAhkMappings={
    KEY_DEL:      'NumpadDel',
    KEY_DOT:      'NumpadDot',
    KEY_DIV:      'NumpadDiv',
    KEY_ENTER:    'NumpadEnter',
    KEY_MIN:      'NumpadSub',
    KEY_MUL:      'NumpadMult',
    KEY_NUM:      'NumLock',
    KEY_NUMPAD_0: 'Numpad0',
    KEY_NUMPAD_1: 'Numpad1',
    KEY_NUMPAD_2: 'Numpad2',
    KEY_NUMPAD_3: 'Numpad3',
    KEY_NUMPAD_4: 'Numpad4',
    KEY_NUMPAD_5: 'Numpad5',
    KEY_NUMPAD_6: 'Numpad6',
    KEY_NUMPAD_7: 'Numpad7',
    KEY_NUMPAD_8: 'Numpad8',
    KEY_NUMPAD_9: 'Numpad9',
    KEY_PLUS:     'NumpadAdd'
}

def pressed(key):
    print("detected hotkey")

ahk = AHK()

def focus_play():
    print("going back to game")
    # TODO switch scene

def focus_browser():
    
    print("focusing browser")
    # use configuration to get browser
    all_windows = ahk.list_windows()

    browser = "firefox.exe"
    ahk.run_script(f"Run {browser} -private https://doomwiki.org")
    # TODO close and run or raise
    # or use embedded python browser idk
    # TODO store this and re-use it later
    win = ahk.win_wait(title='The Doom Wiki', timeout=50)
    # TODO maths
    win.move(x=0,y=0,width=1024,height=768)
    

    # TODO switch scene

    pass

class WinMacros(Macros):
    def __init__(self, obs):
        super().__init__(obs=obs)
        self.ahk = AHK()
        self.ahk.add_hotkey(KeyAhkMappings[KEY_NUMPAD_0], callback=self._obs.SaveReplay)
        self.ahk.add_hotkey(KeyAhkMappings[KEY_DOT], callback=self._obs.CancelRecording)
        self.ahk.add_hotkey(KeyAhkMappings[KEY_DEL], callback=self._obs.CancelRecording)
        self.ahk.start_hotkeys()
