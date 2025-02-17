_KEY_TIMESTAMP = 'timestamp'
_KEY_COMP_LEVEL = 'compLevel'
_KEY_SOURCE_PORT = 'sourcePort'
_KEY_ARGS = 'args'

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

    # TODO statistics service should do this
    # def write_stats(self):
    #     stats_json_path = os.path.join(self._demo_dir, self._demo_name + "-STATS.json")
    #     with(open(stats_json_path, 'w')) as j:
    #         json.dump(self._stats, j)

    def to_dict(self):
        dic = {}

        dic["Demo"] = "Yes" if self.demo else "No"
        dic["Time"] = self.time
        dic["Kills"] = self.kills
        dic["Items"] = self.items
        dic["Secrets"] = self.secrets
        dic["Timestamp"] = self.timestamp

        return dic

    # TODO make this work with multiple formats
    @classmethod
    def from_dict(cls, data):
        instance = cls()

        instance.timestamp = data.get(_KEY_TIMESTAMP, None)
        instance.comp_level = data.get(_KEY_COMP_LEVEL, None)
        instance.sourcePort = data.get(_KEY_SOURCE_PORT, None)
        instance.command = data.get(_KEY_ARGS, None)

        # old style level stats
        levelStats = data.get(_KEY_LEVEL_STATS, None)
        if levelStats:
            instance.kills = levelStats.get('Kills', None)
            instance.items = levelStats.get('Items', None)
            instance.secrets = levelStats.get('Secrets', None)
            instance.time = levelStats.get('Time', None)
        else:
            instance.kills = data.get('Kills', None)
            instance.items = data.get('Items', None)
            instance.secrets = data.get('Secrets', None)
            instance.time = data.get('Time', None)

        return instance