import sys
import os
import uuid
import argparse

from jacodemon.model.mapset import MapSet, MapSetPath
import jacodemon.model.config as config

def _DummyMapSet() -> MapSet:
    
    temp_folder = config.GetConfig().GetTemporaryFolder()
    os.makedirs(temp_folder, exist_ok=True)

    wad_file = os.path.join(temp_folder, "dummy.wad")
    deh_file = os.path.join(temp_folder, "dummy.deh")

    with(open(wad_file, "w+")) as f:
        f.write("some data")

    with(open(deh_file, "w+")) as f:
        f.write("some data")
    
    # paths: List[str], name = None, id=None
    return MapSet([MapSetPath(wad_file, True), MapSetPath(deh_file, False), MapSetPath("garbage/file/path", True)], "dummy set", uuid.uuid4())

class DummyConfig(config.JacodemonConfig):
    def __init__(self) -> None:
        self.sets = [_DummyMapSet()]
        self.iwad_dir = "D:\Dropbox\Games\Doom\WADs\IWADs"
        self.maps_dir = "D:\Dropbox\Games\Doom\WADs\Maps"

    def _PrepareSave(self):
        print("_PrepareSave called on inert DummyConfig")

    def Save(self):
        self._PrepareSave()
        print("Save called on inert DummyConfig")

    def GetMapSetById(self, mapSetId):
        return self.sets[0]

def DummyArgs():
    args = argparse.Namespace()
    args.no_gui = False
    args.stdout_log_level = 'DEBUG'
    args.playlist = None
    args.wad = None
    args.no_obs = False
    args.no_auto_record = False
    args.no_demo = False
    args.no_mods = False
    args.music = False
    args.replay = False
    args.random = False
    args.last = False
    return args

if __name__ == "__main__":
    cfg = config.GetConfig(True)
    sys.exit(0)
