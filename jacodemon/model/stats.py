from typing import List

from jacodemon.misc.legacy import LegacyStatisticsArgsToLaunchSpec

from jacodemon.model.launch import LaunchSpec
from jacodemon.model.map import Map

_KEY_TIMESTAMP = 'Timestamp'
_KEY_COMP_LEVEL = 'CompLevel'
_KEY_SOURCE_PORT = 'SourcePort'
_KEY_SKILL = 'Skill'
_KEY_KILLS = 'Kills'
_KEY_ITEMS = 'Items'
_KEY_SECRETS = 'Secrets'
_KEY_TIME = 'Time'
_KEY_LAUNCH_CONFIG = 'LaunchConfig'

# deprecated
_KEY_LEVEL_STATS = 'levelStats'

class Statistics:

    def __init__(self, demo=None):

        self.time = None
        self.kills = None
        self.sourcePort = None
        self.items = None
        self.secrets = None
        self.launch_spec: LaunchSpec = None

        # deprecated
        self.skill = None
        self.comp_level = None
        self.args: List[str] = None

        # transient
        self.demo = demo

    def get_time(self):
        return self.time
    
    def get_kills(self):
        return self.kills
    
    def get_items(self):
        return self.items
    
    def get_secrets(self):
        return self.secrets
    
    def get_comp_level(self):
        if self.launch_spec:
            return self.launch_spec.comp_level or self.comp_level
        return self.comp_level
    
    def get_skill(self):
        if self.launch_spec:
            return self.launch_spec.skill or self.skill
        return self.skill
    
    def get_badge(self) -> int:

        if None in [self.kills, self.items, self.secrets]:
            return 0

        badge = 1
        kills = self.kills.split('/')
        items = self.items.split('/')
        secrets = self.secrets.split('/')

        if kills[0] == kills[1]:
            badge += 1
        if secrets[0] == secrets[1] and items[0] == items[1]:
            badge += 1

        return badge

    def set_level_stats(self):        
        self.dsda_service.GetLevelStats() # or something

    def to_view(self):
        """
        Get UI representation as dict
        """
        dic = {}

        dic["Demo"] = "Yes" if self.demo else "No"
        dic[_KEY_TIMESTAMP] = self.demo
        dic[_KEY_COMP_LEVEL] = self.get_comp_level()
        dic[_KEY_SOURCE_PORT] = self.sourcePort
        dic[_KEY_SKILL] = self.get_skill()
        dic[_KEY_KILLS] = self.kills
        dic[_KEY_ITEMS] = self.items
        dic[_KEY_SECRETS] = self.secrets
        dic[_KEY_TIME] = self.time

        return dic

    def to_dict(self):
        """
        Convert to dict for persistence only
        """
        dic = {}
        
        dic[_KEY_SOURCE_PORT] = self.sourcePort
        dic[_KEY_TIME] = self.time
        dic[_KEY_KILLS] = self.kills
        dic[_KEY_ITEMS] = self.items
        dic[_KEY_SECRETS] = self.secrets
        dic[_KEY_LAUNCH_CONFIG] = self.launch_spec.to_dict()

        return dic

    def GetLaunchSpec(self, map: Map):
        """
        Get launch spec for a pre-recorded demo. Map argument is only used if 
        launch config is to be inferred when launch config data is unavailable
        """
        if self.launch_spec:
            return self.launch_spec
        else:
            return LegacyStatisticsArgsToLaunchSpec(self.args, self.demo, map)

    @classmethod
    def from_dict(cls, data):
        instance = cls()

        launch_config: LaunchSpec = None
        launch_config_data = data.get(_KEY_LAUNCH_CONFIG, None)

        try:
            launch_config = LaunchSpec.from_dict(launch_config_data)
            if launch_config:
                instance.comp_level = launch_config.comp_level or data.get(_KEY_COMP_LEVEL, data.get("compLevel", None))
                instance.skill = launch_config.skill or data.get(_KEY_SKILL, None)
        except TypeError:
            instance.comp_level = data.get(_KEY_COMP_LEVEL, data.get("compLevel", None))
            instance.skill = data.get(_KEY_SKILL, None)

        # fallbacks are old keys
        instance.timestamp = data.get(_KEY_TIMESTAMP, data.get("timestamp", None))
        instance.sourcePort = data.get(_KEY_SOURCE_PORT, data.get("sourcePort", None))
        instance.launch_spec = launch_config

        # old style level stats
        levelStats = data.get(_KEY_LEVEL_STATS, None)
        if levelStats:
            instance.kills = levelStats.get(_KEY_KILLS, None)
            instance.items = levelStats.get(_KEY_ITEMS, None)
            instance.secrets = levelStats.get(_KEY_SECRETS, None)
            instance.time = levelStats.get(_KEY_TIME, None)
        else:
            # new style level stats
            instance.kills = data.get(_KEY_KILLS, None)
            instance.items = data.get(_KEY_ITEMS, None)
            instance.secrets = data.get(_KEY_SECRETS, None)
            instance.time = data.get(_KEY_TIME, None)

        # deprecated
        instance.args = data.get("args", None)

        return instance
