import queue

SWITCH_TO_BROWSER_SCENE="STBS"

class Signaling:
    def __init__(self, ui_queue: queue) -> None:
        self._signal_queue = ui_queue

    def SwitchToBrowserScene(self):
        self._signal_queue.put(SWITCH_TO_BROWSER_SCENE)