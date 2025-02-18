import os
import subprocess
import threading
import time

from datetime import datetime
from abc import ABC, abstractmethod

from jacodemon.misc.map_utils import get_warp, get_inferred_iwad

from jacodemon.config import JacodemonConfig
from jacodemon.model.launch import LaunchConfig
from jacodemon.model.stats import Statistics

from jacodemon.model.mapset import MapSet

class LaunchService(ABC):
    """
    Service for launching DSDA doom, may be extended later to support other ports
    """

    def __init__(self):
        super().__init__()

    # TODO use/call OBS Service in this super class in/around Execute/PostLaunch
    def Launch(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig):
        
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        launch_config.timestamp = timestamp

        command = self.GetLaunchCommand(launch_config, jacodemon_config)
        subprocess_thread = threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        subprocess_thread.start()
        while subprocess_thread.is_alive():
            time.sleep(2)

        self.PostLaunch(launch_config, jacodemon_config)

    @abstractmethod
    def GetLaunchCommand(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig):
        raise("Not implemented")

    @abstractmethod
    def PostLaunch(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig) -> Statistics:
        raise("Not implemented")

    def GetDehackedPatches(self, mapSet: MapSet):
        patches = []
        for map in mapSet.paths:
            if map.enabled and map.path.lower().endswith(".deh"):
                patches.append(map.path)

        return patches
    
    def GetWadPatches(self, mapSet: MapSet):
        patches = []
        for map in mapSet.paths:
            if map.enabled and map.path.lower().endswith(".wad"):
                patches.append(map.path)

        return patches
    
    def GetDemoFileName(self, launch_config: LaunchConfig):
        return f"{launch_config.map.GetPrefix()}-{launch_config.timestamp}.lmp"

    def GetGenericDoomArgs(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig):
        wads = self.GetWadPatches(launch_config.map.MapSet)
        dehs = self.GetDehackedPatches(launch_config.map.MapSet)

        doom_args = []

        if len(dehs) > 0:
            doom_args.append("-deh")
            doom_args.extend(dehs)

        if len(wads) > 0:
            doom_args.append("-wad")
            doom_args.extend(wads)

        if launch_config.mods:
            enabled_mods = [mod for mod in jacodemon_config.mods if mod['enabled']]
            if len(enabled_mods) > 0:
                doom_args.append("-file")
                doom_args.extend(mod['path'] for mod in enabled_mods)

        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(launch_config.map.MapId))

        iwad = launch_config.map.MapSet.iwad
        if not iwad:
            iwad = get_inferred_iwad(launch_config.map.MapId)

        doom_args.extend(['-iwad', os.path.join(jacodemon_config.iwad_dir, launch_config.map.MapSet.iwad)])

        if False: # TODO this should be fixed to play demos back
            doom_args.append("-playdemo")
            doom_args.append(self._demo_path)
        elif launch_config.record_demo:
            doom_args.append("-record")
            doom_args.append(os.path.join(jacodemon_config.demo_dir, self.GetDemoFileName(launch_config)))

        if not launch_config.music:
            doom_args.append('-nomusic')

        doom_args.extend(['-skill', f"{launch_config.skill}"])

        return doom_args
