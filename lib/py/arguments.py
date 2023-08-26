import argparse

from lib.py.options import Options, MODE_NORMAL, MODE_LAST, MODE_RANDOM, MODE_REPLAY

parser = argparse.ArgumentParser()

def ToOptions(args) -> Options:
    options = Options()
    options.playlist = args.playlist
    options.gui = not args.no_gui
    options.obs = not args.no_obs
    options.mods = not args.no_mods
    options.auto_record = not args.no_auto_record
    options.record_demo = not args.no_demo
    options.music = args.music
    options.crispy = args.crispy
    options.stdout_log_level = args.stdout_log_level.upper()

    if args.last:
        options.mode = MODE_LAST
    elif args.random:
        options.mode = MODE_RANDOM
    elif args.replay:
        options.mode = MODE_REPLAY
    else:
        options.mode = MODE_NORMAL

    return options

def _get_common_args():
    parser.add_argument("-p", "--playlist",     type=str,               help="Playlist")
    parser.add_argument("-g", "--no-gui",       action='store_true',    help="Command line operation only")

def get_args():
    _get_common_args()
    parser.add_argument("-no", "--no-obs",          action='store_true',    help="Disable OBS control")
    parser.add_argument("-nq", "--no-mods",         action='store_true',    help="Disable mods (use this if you are experiencing issues)")
    parser.add_argument("-ar", "--no-auto-record",  action='store_true',    help="Automatically record and stop when gameplay ends")
    parser.add_argument("-nd", "--no-demo",         action='store_true',    help="Demo recording will be disabled")

    parser.add_argument("-m",  "--music",       action='store_true',    help="Enable music")
    parser.add_argument("-sp", "--source-port", type=str,               help="Override source port (force)")
    parser.add_argument("-cr", "--crispy",      action='store_true',    help="Use Crispy Doom instead of Chocolate Doom")
    
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("-rp", "--replay",      action='store_true',    help="Replay a demo")
    modes.add_argument("-r",  "--random",      action='store_true',    help="Pick random map from playlist")
    modes.add_argument("-l",  "--last",        action='store_true',    help="If saved, play last map")

    parser.add_argument("-sll", "--stdout-log-level", type=str,        help="Log level that should also be printed to console", default='INFO')

    args = parser.parse_args()

    return ToOptions(args)

def get_analyse_args() -> Options:
    _get_common_args()
    args = parser.parse_args()

    return ToOptions(args)
