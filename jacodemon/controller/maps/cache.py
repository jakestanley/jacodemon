import os
import pickle

from jacodemon.config import JacodemonConfig, GetConfig

def LoadMapsFromCache(mapSetId):
    temp_folder = GetConfig().GetTemporaryFolder()
    cache_file = os.path.join(temp_folder, f"{mapSetId}.pkl")
    if os.path.exists(cache_file):
        with(open(cache_file, "rb")) as f:
            return pickle.load(f)
    return None

def AddMapsToCache(mapSetId, maps):
    temp_folder = GetConfig().GetTemporaryFolder()
    cache_file = os.path.join(temp_folder, f"{mapSetId}.pkl")
    with open(cache_file, 'wb') as f:
        pickle.dump(maps, f)
