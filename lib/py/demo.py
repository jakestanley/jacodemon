import glob

from lib.py.map import FlatMap

def GetDemosForMap(map: FlatMap, demo_dir):
    prefix = map.GetMapPrefix()
    files = glob.glob(demo_dir + f"/{prefix}*")
    
    return None