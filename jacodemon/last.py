import json
import os
from typing import Optional

import jsonpickle

from jacodemon.model.map import Map
from jacodemon.model.mapset import MapSet

# constants
_LAST_JSON = "./last.json"


def GetLastMap() -> Optional[Map]:
    if os.path.exists(_LAST_JSON):
        with(open(_LAST_JSON)) as f:
            return jsonpickle.decode(json.load(f))
    else:
        print("""
Cannot select last map as '{LAST_JSON}' was not found
        """)
        return None


def SaveSelectedMap(map: Map, mapSetId: str):
    # saves selected map for last
    map.MapSetId = mapSetId
    with open(_LAST_JSON, 'w') as f:
        json.dump(jsonpickle.encode(map), f)
