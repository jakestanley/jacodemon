import argparse

parser = argparse.ArgumentParser()

def _get_common_args():
    parser.add_argument("-g", "--no-gui",       action='store_true',    help="Command line operation only")
    parser.add_argument("-sll", "--stdout-log-level", type=str,        help="Log level that should also be printed to console", default='INFO')
    # mutually exclusive
    parser.add_argument("-p", "--playlist",     type=str,               help="Playlist")
    parser.add_argument("-w", "--wad",          type=str,               help="WAD")

def GetArgs():
    _get_common_args()
    parser.add_argument("-no", "--no-obs",          action='store_true',    help="Disable OBS control")
    parser.add_argument("-nq", "--no-mods",         action='store_true',    help="Disable mods (use this if you are experiencing issues)")
    parser.add_argument("-ar", "--no-auto-record",  action='store_true',    help="Automatically record and stop when gameplay ends")
    parser.add_argument("-nd", "--no-demo",         action='store_true',    help="Demo recording will be disabled")

    parser.add_argument("-m",  "--music",       action='store_true',    help="Enable music")
    
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("-rp", "--replay",      action='store_true',    help="Replay a demo")
    modes.add_argument("-r",  "--random",      action='store_true',    help="Pick random map from playlist")
    modes.add_argument("-l",  "--last",        action='store_true',    help="If saved, play last map")

    return parser.parse_args()

def get_analyse_args():
    _get_common_args()
    return parser.parse_args()

