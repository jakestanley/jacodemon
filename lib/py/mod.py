class Map:
    def __init__(self):
        self._map_id = None
        self._map_name = None

    def get_map_name(self):
        if self._map_name:
            return self._map_name
        return self._map_id


class Mod:
    def __init__(self, csv):
        self._iwad      = ""
        self._pwads     = []
        self._dehs      = []
        self._mwads     = []
        self._maps      = []
        
