import os
import re
import platform

from jacodemon.logs import GetLogManager

from jacodemon.model.options import Options
from jacodemon.model.launch import LaunchConfig, LaunchConfigMutables
from jacodemon.model.stats import Statistics
from jacodemon.model.config import JacodemonConfig
from jacodemon.service.launch.launch_service import LaunchService


_LEVELSTAT_TXT = "./levelstat.txt"

def _AddParsedLevelStats(rawLevelStats, stats: Statistics):

    regex_time = '(\d+:\d+\.\d+)'
    if re.search(regex_time, rawLevelStats):
        stats.time = re.search(regex_time, rawLevelStats).group(1)

    regex_kills = 'K: (\d+\/\d+)'
    if re.search(regex_kills, rawLevelStats):
        stats.kills = re.search(regex_kills, rawLevelStats).group(1)

    regex_secrets = 'S: (\d+\/\d+)'
    if re.search(regex_secrets, rawLevelStats):
        stats.secrets = re.search(regex_secrets, rawLevelStats).group(1)

    regex_items = 'I: (\d+\/\d+)'
    if re.search(regex_items, rawLevelStats):
        stats.items = re.search(regex_items, rawLevelStats).group(1)

class DsdaLaunchConfigMutables(LaunchConfigMutables):
    def __init__(self, options: Options):
        self.dsda_path = options.dsda_path
        self.dsda_cfg = options.dsda_cfg
        self.dsdadoom_hud_lump = options.dsdadoom_hud_lump

class DsdaService(LaunchService):

    def __init__(self):
        self._logger = GetLogManager().GetLogger(__name__)

    def _FormatCompLevel(self, comp_level):
        if comp_level == 'vanilla':
            return "4"
        elif comp_level == 'mbf21':
            return "21"
        else:
            return str(comp_level)

    def GetSourcePortName(self) -> str:
        return "dsdadoom"

    def PreLaunch(self):

        # remove any old levelstat.txt in case it wasn't removed by a previous execution
        if os.path.exists(_LEVELSTAT_TXT):
            os.remove(_LEVELSTAT_TXT)

    def GetLaunchCommand(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig, play_demo: bool = False, record_demo: bool = True):

        args = self.GetGenericDoomArgs(launch_config=launch_config, 
                                       iwad_dir=jacodemon_config.iwad_dir,
                                       demo_dir=jacodemon_config.demo_dir,
                                       play_demo=play_demo,
                                       record_demo=record_demo)

        args.extend(['-complevel', str(launch_config.comp_level)])

        if not play_demo:
            args.append('-levelstat')

        if platform.system() == "Darwin":
            args.extend(['-geom', '1920x1080f'])
        else:
            args.append('-window')

        if jacodemon_config.dsdadoom_hud_lump:
            args.extend(['-hud', jacodemon_config.dsdadoom_hud_lump])

        # TODO that this may break demo compatibility if it changes, but #
        #   i'm not about to start backing these up
        if jacodemon_config.dsda_cfg:
            args.extend(['-config', jacodemon_config.dsda_cfg])

        command = [jacodemon_config.dsda_path]
        command.extend(args)

        return command
    
    def EnhanceStatistics(self, launch_config: LaunchConfig, statistics: Statistics):
        if not os.path.exists("./tmp"):
            os.mkdir("./tmp")

        archived_levelstat_txt = f"./tmp/{launch_config.name}.txt"

        if os.path.exists(_LEVELSTAT_TXT):
            with(open(_LEVELSTAT_TXT)) as raw_level_stats:
                _AddParsedLevelStats(raw_level_stats.read(), statistics)
            raw_level_stats.close()
            os.rename(_LEVELSTAT_TXT, archived_levelstat_txt)
        else:
            self._logger.info("No levelstat.txt found. I assume you didn't finish the level or aren't using dsda-doom")
