# https://pypi.org/project/ahk/
from ahk import AHK

# from https://www.autohotkey.com/docs/v1/KeyList.htm
# I use the Jellycomb external numpad
_KEY_NUMPAD_0='Numpad0'
_KEY_NUMPAD_1='Numpad1'
_KEY_NUMPAD_2='Numpad2'
_KEY_NUMPAD_3='Numpad3'
_KEY_NUMPAD_4='Numpad4'
_KEY_NUMPAD_5='Numpad5'
_KEY_NUMPAD_6='Numpad6'
_KEY_NUMPAD_7='Numpad7'
_KEY_NUMPAD_8='Numpad8'
_KEY_NUMPAD_9='Numpad9'
_KEY_DEL='NumpadDel'

def pressed(key):
    print("detected hotkey")

ahk = AHK()

def focus_game():
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

ahk.add_hotkey(_KEY_NUMPAD_0, callback=None)
ahk.add_hotkey(_KEY_NUMPAD_1, callback=None)
ahk.add_hotkey(_KEY_NUMPAD_2, callback=None)
ahk.add_hotkey(_KEY_NUMPAD_3, callback=focus_browser)
ahk.add_hotkey(_KEY_NUMPAD_4, callback=pressed(_KEY_NUMPAD_4))
ahk.add_hotkey(_KEY_NUMPAD_5, callback=pressed(_KEY_NUMPAD_5))
ahk.add_hotkey(_KEY_NUMPAD_6, callback=pressed(_KEY_NUMPAD_6))
ahk.add_hotkey(_KEY_NUMPAD_7, callback=pressed(_KEY_NUMPAD_7))
ahk.add_hotkey(_KEY_NUMPAD_8, callback=pressed(_KEY_NUMPAD_8))
ahk.add_hotkey(_KEY_NUMPAD_9, callback=pressed(_KEY_NUMPAD_9))
ahk.add_hotkey(_KEY_DEL, callback=pressed(_KEY_DEL))


ahk.start_hotkeys()
if __name__ == "__main__":
    ahk.block_forever()

# TODO: return hotkeys and continue execution
