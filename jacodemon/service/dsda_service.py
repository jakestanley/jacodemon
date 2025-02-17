import os
import re

from jacodemon.logs import GetLogManager

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

class DsdaService:

    def __init__(self):
        self._logger = GetLogManager().GetLogger(__name__)

    def GetLevelStats(self):

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