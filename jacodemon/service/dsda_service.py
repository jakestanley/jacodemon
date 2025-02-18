import os
import re
import platform

from jacodemon.logs import GetLogManager

from jacodemon.model.launch import LaunchConfig
from jacodemon.model.map import Map
from jacodemon.model.stats import Statistics

from jacodemon.service.launch_service import LaunchService
from jacodemon.config import JacodemonConfig


_LEVELSTAT_TXT = "./levelstat.txt"

def _ParseLevelStats(rawLevelStats):

    levelStats = {}
    levelStats['Time'] = "???"
    levelStats['Kills'] = "???"
    levelStats['Secrets'] = "???"
    levelStats['Items'] = "???"

    regex_time = '(\d+:\d+\.\d+)'
    mtch = re.search(regex_time, rawLevelStats)
    if re.search(regex_time, rawLevelStats):
        levelStats['Time'] = re.search(regex_time, rawLevelStats).group(1)

    regex_kills = 'K: (\d+\/\d+)'
    if re.search(regex_kills, rawLevelStats):
        levelStats["Kills"] = re.search(regex_kills, rawLevelStats).group(1)

    regex_secrets = 'S: (\d+\/\d+)'
    if re.search(regex_secrets, rawLevelStats):
        levelStats["Secrets"] = re.search(regex_secrets, rawLevelStats).group(1)

    regex_items = 'I: (\d+\/\d+)'
    if re.search(regex_items, rawLevelStats):
        levelStats["Items"] = re.search(regex_items, rawLevelStats).group(1)

    return levelStats

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

    def _GetLevelStats(self):

        stats = {}

        if os.path.exists(_LEVELSTAT_TXT):
            with(open(_LEVELSTAT_TXT)) as raw_level_stats:
                if not os.path.exists("./tmp"):
                    os.mkdir("./tmp")
                stats = _ParseLevelStats(raw_level_stats.read())
                archived_level_stat_txt = f"./tmp/levelstat_{self._demo_name}.txt"
            raw_level_stats.close()
            os.rename(_LEVELSTAT_TXT, archived_level_stat_txt)
        else:
            self._logger.info("No levelstat.txt found. I assume you didn't finish the level or aren't using dsda-doom")

        return stats

    def GetLaunchCommand(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig):

        args = self.GetGenericDoomArgs(launch_config, jacodemon_config)

        args.extend(['-complevel', str(launch_config.comp_level)])
        args.append('-levelstat')

        if platform.system() == "Darwin":
            args.extend(['-geom', '1920x1080f'])
        else:
            args.append('-window')

        if jacodemon_config.dsdadoom_hud_lump:
            args.extend(['-hud', jacodemon_config.dsdadoom_hud_lump])

        if jacodemon_config.dsda_cfg:
            args.extend(['-config', jacodemon_config.dsda_cfg])

        command = [jacodemon_config.dsda_path]
        command.extend(args)

        return command

    def PostLaunch(self, launch_config: LaunchConfig, jacodemon_config: JacodemonConfig) -> Statistics:
        # TODO capture stats
        pass
