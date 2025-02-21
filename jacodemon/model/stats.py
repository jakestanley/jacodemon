_KEY_TIMESTAMP = 'Timestamp'
_KEY_COMP_LEVEL = 'CompLevel'
_KEY_SOURCE_PORT = 'SourcePort'
_KEY_ARGS = 'args'
_KEY_SKILL = 'Skill'
_KEY_KILLS = 'Kills'
_KEY_ITEMS = 'Items'
_KEY_SECRETS = 'Secrets'
_KEY_TIME = 'Time'

# deprecated
_KEY_LEVEL_STATS = 'levelStats'

class Statistics:

    def __init__(self, time=None, timestamp=None, comp_level=None, 
                 sourcePort=None, command=None, demo=None):

        self.time = time
        self.comp_level = comp_level
        self.sourcePort = sourcePort
        self.command = command
        self.timestamp = timestamp
        self.kills = None
        self.skill = None
        self.items = None
        self.secrets = None
        self.demo = demo
        
    def get_timestamp(self):
        return self.timestamp

    def get_time(self):
        return self.time
    
    def get_kills(self):
        return self.kills
    
    def get_items(self):
        return self.items
    
    def get_secrets(self):
        return self.secrets
    
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

    # TODO separate to_dict for saving and for the table
    def to_dict(self):
        dic = {}

        dic["Demo"] = "Yes" if self.demo else "No"
        dic[_KEY_SKILL] = self.skill
        dic[_KEY_SOURCE_PORT] = self.sourcePort
        dic[_KEY_TIME] = self.time
        dic[_KEY_KILLS] = self.kills
        dic[_KEY_ITEMS] = self.items
        dic[_KEY_SECRETS] = self.secrets
        dic[_KEY_TIMESTAMP] = self.timestamp
        dic[_KEY_COMP_LEVEL] = self.comp_level

        return dic

    # TODO make this work with multiple formats
    @classmethod
    def from_dict(cls, data):
        instance = cls()

        # fallbacks are old keys
        instance.timestamp = data.get(_KEY_TIMESTAMP, data.get("timestamp", None))
        instance.comp_level = data.get(_KEY_COMP_LEVEL, data.get("compLevel", None))
        instance.sourcePort = data.get(_KEY_SOURCE_PORT, data.get("sourcePort", None))
        instance.command = data.get(_KEY_ARGS, None)
        instance.skill = data.get(_KEY_SKILL, None)

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

        return instance
