import csv
import os

REQUIRED_FIELDS = ["ModName", "Files"]
OPTIONAL_FIELDS = ["MapId", "MapName", "Author", "CompLevel", "Merge", "Port", "Notes"]

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
