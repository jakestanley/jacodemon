MODE_NORMAL: int = 0
MODE_RANDOM: int = 1
MODE_LAST: int = 2
MODE_REREC: int = 3

class Options:
    def __init__(self):
        self.playlist = None
        self.gui = None
        self.obs = None
        self.mods = None
        self.music = None
        self.auto_record = None
        self.record_demo = None
        self.crispy = None
        self.mode = MODE_NORMAL

    def last(self):
        return self.mode == MODE_LAST

    def random(self):
        return self.mode == MODE_RANDOM

    def rerecord(self):
        return self.mode == MODE_REREC
    
    def record(self):
        return self.rerecord() or self.auto_record
