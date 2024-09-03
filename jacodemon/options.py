_SINGLETON = None

MODE_NORMAL: int = 1
MODE_RANDOM: int = 2
MODE_LAST: int = 3
MODE_REPLAY: int = 4

class Options:
    def __init__(self):
        self.playlist = None
        self.wad = None
        self.gui = None
        self.obs = None
        self.mods = None
        self.music = None
        self.auto_record = None
        self.record_demo = None
        self.crispy = None
        self.mode = MODE_NORMAL
        self.stdout_log_level = None

    def last(self):
        return self.mode == MODE_LAST

    def random(self):
        return self.mode == MODE_RANDOM

    def replay(self):
        return self.mode == MODE_REPLAY

def _ArgsToOptions(args) -> Options:
    options = Options()
    options.playlist            = args.playlist
    options.wad                 = args.wad
    options.gui                 = not args.no_gui
    options.stdout_log_level    = args.stdout_log_level.upper()

    # these are not common so we perform hasattr checks
    if hasattr(args, 'no_obs'):
        options.obs         = not args.no_obs
    if hasattr(args, 'no_mods'):
        options.mods        = not args.no_mods
    if hasattr(args, 'no_auto_record'):
        options.auto_record = not args.no_auto_record
    if hasattr(args, 'no_demo'):
        options.record_demo = not args.no_demo
    if hasattr(args, 'music'):
        options.music       = args.music
    if hasattr(args, 'crispy'):
        options.crispy      = args.crispy

    if hasattr(args, 'last') and args.last:
        options.mode = MODE_LAST
    elif hasattr(args, 'random') and args.random:
        options.mode = MODE_RANDOM
    elif hasattr(args, 'replay') and args.replay:
        options.mode = MODE_REPLAY
    else:
        options.mode = MODE_NORMAL

    return options

def InitialiseOptions(args):
    global _SINGLETON
    if _SINGLETON is not None:
        raise Exception("InitialiseOptions MUST only be called exactly once")
    _SINGLETON = _ArgsToOptions(args)

def GetOptions() -> Options:
    global _SINGLETON
    if _SINGLETON is None:
        raise Exception("GetOptions called when singleton was not initialised")
    return _SINGLETON