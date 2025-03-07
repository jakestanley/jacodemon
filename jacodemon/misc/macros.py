import logging
import platform

from jacodemon.service.obs_service import ObsService
from jacodemon.keys import *

class Key:
    def __init__(self, id=str, name=str, enabled=True):
        self.id = id
        self.name = name
        self.enabled = True

# ordered as per Jelly Comb keyboard
KeyNames = [
    Key(KEY_NUM, "Num"),
    Key(KEY_DIV, "/"),
    Key(KEY_MUL, "*"),
    Key(KEY_BCK, "<-", False),
    Key(KEY_NUMPAD_7, "7"),
    Key(KEY_NUMPAD_8, "8"),
    Key(KEY_NUMPAD_9, "9"),
    Key(KEY_MIN, "-"),
    Key(KEY_NUMPAD_4, '4'),
    Key(KEY_NUMPAD_5, '5'),
    Key(KEY_NUMPAD_6, '6'),
    Key(KEY_PLUS, '+'),
    Key(KEY_NUMPAD_1, '1'),
    Key(KEY_NUMPAD_2, '2'),
    Key(KEY_NUMPAD_3, '3'),
    Key(KEY_ENTER, 'Enter'),
    Key(KEY_NUMPAD_0, '0'),
    Key(KEY_DEL, 'Del')
]

class Macros:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        return

    def add_hotkey_callback(self, key: str, callback):
        self._logger.warning("add_hotkey_callback not implemented")

    def listen(self):
        pass


def GetMacros() -> Macros:
    system = platform.system()
    if system == "Darwin":
        from jacodemon.platform.macos.macros import MacMacros
        return MacMacros()
    else:
        from jacodemon.platform.windows.macros import WinMacros
        return WinMacros()

