import json
import os
from typing import Optional

import jsonpickle

from lib.py.map import FlatMap

# constants
LAST_JSON = "./last.json"


def GetLastMap() -> Optional[FlatMap]:
    if os.path.exists(LAST_JSON):
        with(open(LAST_JSON)) as f:
            return jsonpickle.decode(json.load(f))
    else:
        print("""
Cannot select last map as '{LAST_JSON}' was not found
        """)
        return None


def SaveSelectedMap(map: FlatMap):
    # saves selected map for last
    with open(LAST_JSON, 'w') as f:
        json.dump(jsonpickle.encode(map), f)
