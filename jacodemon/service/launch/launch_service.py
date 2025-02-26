import os
import subprocess
import threading
import time

from datetime import datetime
from abc import ABC, abstractmethod

from jacodemon.misc.map_utils import get_warp, get_inferred_iwad

from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL
from jacodemon.model.config import JacodemonConfig
from jacodemon.model.launch import LaunchSpec, LaunchSession, LaunchMode
from jacodemon.model.options import Options
from jacodemon.model.stats import Statistics

from jacodemon.model.map import Map
from jacodemon.model.mapset import MapSet
from jacodemon.misc.files import ToPathHashTupleList

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
    def GetLaunchCommand(self, launch_config: LaunchSpec, launch_session: LaunchSession):
        raise("Not implemented")

    @abstractmethod
    def EnhanceStatistics(self, spec: LaunchSpec, statistics: Statistics):
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

    def CreateLaunchSpec(self, jacodemon_config: JacodemonConfig, options: Options, map: Map) -> LaunchSpec:

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

        return LaunchSpec(
            name=name,
            map_id=map.MapId,
            timestamp=timestamp,
            iwad=map.MapSet.iwad,
            wads=ToPathHashTupleList(self.GetWadPatches(map.MapSet)),
            dehs=ToPathHashTupleList(self.GetDehackedPatches(map.MapSet)),
            mods=ToPathHashTupleList(mods),
            fast_monsters=options.fast,
            skill=skill,
            comp_level=comp_level
        )

    # TODO use/call OBS Service in this super class in/around Execute/PostLaunch
    def Launch(self, launch_spec: LaunchSpec, launch_session: LaunchSession) -> Statistics:

        self.PreLaunch()

        command = self.GetLaunchCommand(launch_spec, launch_session)

        subprocess_thread = threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        subprocess_thread.start()
        while subprocess_thread.is_alive():
            time.sleep(2)

        if launch_session.mode == LaunchMode.REPLAY_DEMO:
            return None

        statistics = Statistics()
        statistics.launch_spec = launch_spec
        self.EnhanceStatistics(launch_spec, statistics)

        return statistics

    def GetGenericDoomArgs(self, launch_spec: LaunchSpec, launch_session: LaunchSession):

        doom_args = []

        if len(launch_spec.dehs) > 0:
            doom_args.append("-deh")
            doom_args.extend(d[0] for d in launch_spec.dehs)

        files = []
        if len(launch_spec.wads) > 0:
            files.extend(w[0] for w in launch_spec.wads)

        if len(launch_spec.mods) > 0:
            files.extend([m[0] for m in launch_spec.mods])

        if len(files) > 0:
            doom_args.append("-file")
            doom_args.extend(files)

        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(launch_spec.map_id))

        iwad = launch_spec.iwad
        if not iwad:
            iwad = get_inferred_iwad(launch_spec.map_id)

        iwad_path = os.path.join(launch_session.iwad_dir, iwad)
        doom_args.extend(['-iwad', iwad_path])

        demo_path = os.path.join(launch_session.demo_dir, f"{launch_spec.name}.lmp")
        if launch_session.mode == LaunchMode.RECORD_DEMO:
            doom_args.append("-record")
            doom_args.append(demo_path)
        elif launch_session.mode == LaunchMode.REPLAY_DEMO:
            doom_args.append("-playdemo")
            doom_args.append(demo_path)

        if launch_spec.fast_monsters:
            doom_args.append('-fast')

        doom_args.extend(['-skill', f"{launch_spec.skill}"])

        return doom_args
