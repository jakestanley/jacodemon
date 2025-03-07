from jacodemon.model.launch import LaunchMode

_SINGLETON = None

class Options:
    def __init__(self):
        self.obs = None
        self.mods = None
        self.music = None
        self.auto_record = None
        self.fast = None
        self.mode: LaunchMode = None
        self.stdout_log_level = None
        self.skill = None

def _ArgsToOptions(args) -> Options:
    options = Options()
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
    if hasattr(args, 'fast'):
        options.fast       = args.fast

    # these two are currently disabled while i work out other stuff
    if hasattr(args, 'last') and args.last:
        options.mode = None
    elif hasattr(args, 'random') and args.random:
        options.mode = None
    elif hasattr(args, 'replay') and args.replay:
        options.mode = LaunchMode.REPLAY_DEMO
    else:
        options.mode = LaunchMode.RECORD_DEMO

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