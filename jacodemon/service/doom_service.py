# Standard library imports
import logging
import os
import platform
import re
import subprocess
import threading
import time

from datetime import datetime

# Local application/utility imports
from jacodemon.misc.constants import DEFAULT_COMP_LEVEL, DEFAULT_SKILL
from jacodemon.misc.map_utils import get_warp, get_inferred_iwad
from jacodemon.misc.files import ToPathHashTupleList, FindAndVerify

# Model imports
from jacodemon.model.config import JacodemonConfig
from jacodemon.model.launch import LaunchSpec, LaunchSession, LaunchMode
from jacodemon.model.options import Options
from jacodemon.model.stats import Statistics
from jacodemon.model.map import Map
from jacodemon.model.mapset import MapSet

_LEVELSTAT_TXT = "./levelstat.txt"

def _AddParsedLevelStats(rawLevelStats, stats: Statistics):

    regex_time = r'(\d+:\d+\.\d+)'
    if re.search(regex_time, rawLevelStats):
        stats.time = re.search(regex_time, rawLevelStats).group(1)

    regex_kills = r'K: (\d+\/\d+)'
    if re.search(regex_kills, rawLevelStats):
        stats.kills = re.search(regex_kills, rawLevelStats).group(1)

    regex_secrets = r'S: (\d+\/\d+)'
    if re.search(regex_secrets, rawLevelStats):
        stats.secrets = re.search(regex_secrets, rawLevelStats).group(1)

    regex_items = r'I: (\d+\/\d+)'
    if re.search(regex_items, rawLevelStats):
        stats.items = re.search(regex_items, rawLevelStats).group(1)

class DoomService:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def initialise(self):
        pass

    def _FormatCompLevel(self, comp_level):
        if comp_level == 'vanilla':
            return "4"
        elif comp_level == 'mbf21':
            return "21"
        else:
            return str(comp_level)


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
            doom_args.extend(d[0] for d in FindAndVerify(launch_spec.dehs, [launch_session.maps_dir]))

        files = []
        if len(launch_spec.wads) > 0:
            files.extend(w[0] for w in FindAndVerify(launch_spec.wads, [launch_session.maps_dir]))

        if len(launch_spec.mods) > 0:
            files.extend(m[0] for m in FindAndVerify(launch_spec.mods, [launch_session.mods_dir]))

        if len(files) > 0:
            doom_args.append("-file")
            doom_args.extend(files)

        doom_args.extend(['-warp'])
        doom_args.extend(get_warp(launch_spec.map_id))

        iwad = launch_spec.iwad
        if not iwad:
            iwad = get_inferred_iwad(launch_spec.map_id)

        if os.path.exists(iwad):
            iwad_path = iwad
        else:
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

        if launch_session.music:
            pass
        else:
            doom_args.append("-nomusic")

        doom_args.extend(['-skill', f"{launch_spec.skill}"])

        return doom_args


    def GetSourcePortName(self) -> str:
        return "dsdadoom"

    def PreLaunch(self):

        # remove any old levelstat.txt in case it wasn't removed by a previous execution
        if os.path.exists(_LEVELSTAT_TXT):
            os.remove(_LEVELSTAT_TXT)

    def GetLaunchCommand(self, launch_config: LaunchSpec, launch_session: LaunchSession):

        args = self.GetGenericDoomArgs(launch_spec=launch_config, 
                                       launch_session=launch_session)

        args.extend(['-complevel', self._FormatCompLevel(str(launch_config.comp_level))])

        if launch_session is not LaunchMode.REPLAY_DEMO:
            args.append('-levelstat')

        if platform.system() == "Darwin":
            args.extend(['-geom', '1920x1080f'])
        else:
            args.append('-window')

        # TODO that this may break demo compatibility if it changes, but
        #   i'm not about to start hashing/backing these up
        if launch_session.cfg_path:
            args.extend(['-config', launch_session.cfg_path])

        command = [launch_session.executable]
        command.extend(args)

        return command
    
    def EnhanceStatistics(self, launch_spec: LaunchSpec, statistics: Statistics):
        if not os.path.exists("./tmp"):
            os.mkdir("./tmp")

        archived_levelstat_txt = f"./tmp/{launch_spec.name}.txt"

        if os.path.exists(_LEVELSTAT_TXT):
            with(open(_LEVELSTAT_TXT)) as raw_level_stats:
                _AddParsedLevelStats(raw_level_stats.read(), statistics)
            raw_level_stats.close()
            os.rename(_LEVELSTAT_TXT, archived_levelstat_txt)
        else:
            self._logger.debug("No levelstat.txt found. I assume you didn't finish the level or aren't using dsda-doom")
