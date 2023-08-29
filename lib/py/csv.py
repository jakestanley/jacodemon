import os
from typing import List

import sys
import csv
from lib.py.map import FlatMap
from lib.py.logs import LogManager, GetLogManager

# private constants
_KEY_MOD_NAME = "ModName"
_KEY_FILES = "Files"
_KEY_MAP_ID = "MapId"
_KEY_MAP_NAME = "MapName"
_KEY_AUTHOR = "Author"
_KEY_COMP_LEVEL = "CompLevel"
_KEY_MERGE = "Merge"
_KEY_PORT = "Port"
_KEY_NOTES = "Notes"

REQUIRED_FIELDS = [_KEY_MOD_NAME, _KEY_FILES]

OPTIONAL_FIELDS = [_KEY_MAP_ID, _KEY_MAP_NAME, _KEY_AUTHOR, _KEY_COMP_LEVEL, 
                   _KEY_MERGE, _KEY_PORT, _KEY_NOTES]

def has_valid_extension(file_path):
    valid_extensions = [".pk3", ".wad", ".deh"]
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in valid_extensions

def csv_is_valid(csv_path):
    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        rows = list(reader)

    # Check if all required fields are present in the CSV header
    missing_required_fields = [field for field in REQUIRED_FIELDS if field not in headers]
    if missing_required_fields:
        print("Error: The following required fields are missing in the CSV header:")
        print(", ".join(missing_required_fields))
        return False
    
    # Check if all optional fields are valid and not duplicated
    optional_fields = [field for field in headers if field in OPTIONAL_FIELDS]
    invalid_optional_fields = [field for field in optional_fields if field not in OPTIONAL_FIELDS]
    if invalid_optional_fields:
        print("Error: The following fields are not valid:")
        print(", ".join(invalid_optional_fields))
        print("Only the following OPTIONAL fields are supported:")
        print(", ".join(OPTIONAL_FIELDS))
        return False

    unique_combinations = set()

    for row_num, row in enumerate(rows, start=1):
        mod_name = row["ModName"]
        map_id = row.get("MapId")

        # Rule: mod_name must be present in every row
        if not mod_name:
            print(f"Error in row {row_num}: mod_name is missing")
            return False
        
        # Rule: mod name and map ID MUST be unique
        combination = (mod_name, map_id)
        if combination in unique_combinations:
            print(f"Error in row {row_num}: Duplicate combination of ModName '{mod_name}' and MapId '{map_id}' found in the CSV.")
            return False
        
        # Rule: files and merges must be separated by a pipe character and have valid extensions
        if row["Files"]:
            files = row["Files"].split("|")
            for file_path in files:
                if not has_valid_extension(file_path):
                    print(f"Error in row {row_num}: Invalid file extension in '{file_path}'. Only pk3, wad, and deh extensions are allowed.")
                    return False
        else:
            print(f"Error in row {row_num}: No files were present")
            return False
            
        unique_combinations.add(combination)


    return True

"""
Load raw map data from a dict. It is possible that a map has no map ID and 
has to be enriched with this data
"""
def load_raw_map(dic) -> FlatMap:

    map = FlatMap(dic[_KEY_MOD_NAME], dic[_KEY_FILES], 
                  dic.get(_KEY_MAP_ID), dic.get(_KEY_MAP_NAME), 
                  dic.get(_KEY_AUTHOR), dic.get(_KEY_COMP_LEVEL),
                  dic.get(_KEY_MERGE), dic.get(_KEY_PORT), 
                  dic.get(_KEY_NOTES))

    return map

"""
Load raw map data from a CSV. It is possible that a map has no map ID and 
has to be enriched with this data
"""
def load_raw_maps(csv_path) -> List[FlatMap]:

    logger = GetLogManager().GetLogger(__name__)

    if not os.path.exists(csv_path):
        logger.critical(f"Could not find playlist file: {csv_path}")
        sys.exit(1)

    if not csv_is_valid(csv_path):
        logger.critical("CSV header is invalid. See output")
        sys.exit(1)

    raw_maps = []

    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        map = load_raw_map(row)
        raw_maps.append(map)
    
    return raw_maps