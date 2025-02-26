import os
import subprocess
import threading
import time

from datetime import datetime
from abc import ABC, abstractmethod

from jacodemon.misc.map_utils import get_warp, get_inferred_iwad

from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL
from jacodemon.model.config import JacodemonConfig
from jacodemon.model.launch import LaunchConfig, LaunchConfigMutables
from jacodemon.model.options import Options
from jacodemon.model.stats import Statistics

from jacodemon.model.map import Map
from jacodemon.model.mapset import MapSet

class LaunchService(ABC):
    """
    Service for launching DSDA doom, may be extended later to support other ports
    """

    def __init__(self):
        super().__init__()

    def CreateLaunchConfig(self, config: JacodemonConfig, options: Options, map: Map) -> LaunchConfig:

        skill = DEFAULT_SKILL
        if config.skill:
            skill = config.skill

        comp_level = DEFAULT_COMP_LEVEL
        if map.MapSet.compLevel:
            comp_level = map.MapSet.compLevel
        elif config.default_complevel:
            comp_level = config.default_complevel

        mods = []
        if options.mods:
            mods = [mod['path'] for mod in config.mods if mod['enabled']]

        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        name = f"{map.GetPrefix()}-{timestamp}"

        return LaunchConfig(
            name=name,
            timestamp=timestamp,
            map_id=map.MapId,
            iwad=map.MapSet.iwad,
            wads=self.GetWadPatches(map),
            dehs=self.GetDehackedPatches(map),
            mods=mods,
            fast_monsters=options.fast,
            skill=skill,
            comp_level=comp_level
        )

    # TODO use/call OBS Service in this super class in/around Execute/PostLaunch
    def Launch(self, launch_config: LaunchConfig, launch_config_extras: LaunchConfigMutables, jacodemon_config: JacodemonConfig) -> Statistics:

        self.PreLaunch()

        command = self.GetLaunchCommand(launch_config, jacodemon_config)

        subprocess_thread = threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        subprocess_thread.start()
        while subprocess_thread.is_alive():
            time.sleep(2)

        statistics = Statistics()
        statistics.sourcePort = self.GetSourcePortName()

        self.EnhanceStatistics(launch_config, jacodemon_config, statistics)
        self.PostLaunch(launch_config, jacodemon_config)

        return statistics

    @abstractmethod
    def GetSourcePortName(self) -> str:
        raise("Not implemented")

    @abstractmethod
    def PreLaunch(self):
        print("PreLaunch is not implemented by this LaunchService instance")

    @abstractmethod
    def GetLaunchCommand(self, launch_config: LaunchConfig, launch_config_extras: LaunchConfigMutables):
        raise("Not implemented")

    @abstractmethod
    def EnhanceStatistics(self, launch_config: LaunchConfig, statistics: Statistics):
        print("EnhanceStatistics is not implemented by this LaunchService instance")

    @abstractmethod
    def PostLaunch(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig):
        print("PostLaunch is not implemented by this LaunchService instance")

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

    def GetGenericDoomArgs(self, launch_config: LaunchConfig, demo_dir: str, iwad_dir: str, play_demo: bool):

        doom_args = []

        if len(launch_config.dehs) > 0:
            doom_args.append("-deh")
            doom_args.extend(launch_config.dehs)

        files = []
        if len(launch_config.wads) > 0:
            files.extend(launch_config.wads)

        if len(launch_config.mods) > 0:
            files.extend([mod for mod in launch_config.mods])

        if len(files) > 0:
            doom_args.append("-file")
            doom_args.extend(files)

        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(launch_config.mapId))

        iwad = launch_config.map.MapSet.iwad
        if not iwad:
            iwad = get_inferred_iwad(launch_config.map.MapId)

        iwad_path = os.path.join(iwad_dir, iwad)
        doom_args.extend(['-iwad', iwad_path])

        demo_path = os.path.join(demo_dir, f"{launch_config.name}.lmp")
        if play_demo:
            doom_args.append("-playdemo")
            doom_args.append(demo_path)
        elif launch_config.record_demo:
            doom_args.append("-record")
            doom_args.append(demo_path)

        if launch_config.fast:
            doom_args.append('-fast')

        doom_args.extend(['-skill', f"{launch_config.skill}"])

        return doom_args
