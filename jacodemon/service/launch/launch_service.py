import os
import subprocess
import threading
import time

from datetime import datetime
from abc import ABC, abstractmethod

from jacodemon.misc.map_utils import get_warp, get_inferred_iwad

from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL
from jacodemon.model.config import JacodemonConfig
from jacodemon.model.launch import LaunchConfig
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

    @abstractmethod
    def GetSourcePortName(self) -> str:
        raise("Not implemented")

    @abstractmethod
    def PreLaunch(self):
        print("PreLaunch is not implemented by this LaunchService instance")

    @abstractmethod
    def GetLaunchCommand(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig, play_demo: bool):
        raise("Not implemented")

    @abstractmethod
    def EnhanceStatistics(self, launch_config: LaunchConfig, statistics: Statistics):
        print("EnhanceStatistics is not implemented by this LaunchService instance")

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

    def CreateLaunchConfig(self, jacodemon_config: JacodemonConfig, options: Options, map: Map) -> LaunchConfig:

        skill = DEFAULT_SKILL
        if jacodemon_config.skill:
            skill = jacodemon_config.skill

        comp_level = DEFAULT_COMP_LEVEL
        if map.MapSet.compLevel:
            comp_level = map.MapSet.compLevel
        elif jacodemon_config.default_complevel:
            comp_level = jacodemon_config.default_complevel

        mods = []
        if options.mods:
            mods = [mod['path'] for mod in jacodemon_config.mods if mod['enabled']]

        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        name = f"{map.GetPrefix()}-{timestamp}"

        return LaunchConfig(
            name=name,
            map_id=map.MapId,
            iwad=map.MapSet.iwad,
            wads=self.GetWadPatches(map.MapSet),
            dehs=self.GetDehackedPatches(map.MapSet),
            mods=mods,
            fast_monsters=options.fast,
            skill=skill,
            comp_level=comp_level
        )

    # TODO use/call OBS Service in this super class in/around Execute/PostLaunch
    def Launch(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig, play_demo: bool=False, record_demo: bool=True) -> Statistics:

        self.PreLaunch()

        command = self.GetLaunchCommand(launch_config, jacodemon_config, play_demo=play_demo, record_demo=record_demo)

        subprocess_thread = threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        subprocess_thread.start()
        while subprocess_thread.is_alive():
            time.sleep(2)

        statistics = Statistics()
        statistics.timestamp = launch_config.timestamp
        statistics.launch_config = launch_config
        statistics.sourcePort = self.GetSourcePortName()

        self.EnhanceStatistics(launch_config, statistics)

        return statistics

    def GetGenericDoomArgs(self, launch_config: LaunchConfig, iwad_dir: str, demo_dir: str, play_demo: bool=True, record_demo: bool=False):

        if play_demo and record_demo:
            raise Exception("You can't play and record a demo at the same time")

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
        doom_args.extend(get_warp(launch_config.map_id))

        iwad = launch_config.iwad
        if not iwad:
            iwad = get_inferred_iwad(launch_config.map_id)

        iwad_path = os.path.join(iwad_dir, iwad)
        doom_args.extend(['-iwad', iwad_path])

        demo_path = os.path.join(demo_dir, f"{launch_config.name}.lmp")
        if play_demo:
            doom_args.append("-playdemo")
            doom_args.append(demo_path)
        elif record_demo:
            doom_args.append("-record")
            doom_args.append(demo_path)

        if launch_config.fast_monsters:
            doom_args.append('-fast')

        doom_args.extend(['-skill', f"{launch_config.skill}"])

        return doom_args
