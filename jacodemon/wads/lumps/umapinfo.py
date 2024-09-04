import re

def parse_umapinfo(data):
    # Prepare the data by removing \r\n and splitting lines
    
    lines = data.decode('utf-8').replace('\r\n', '\n').split('\n')

    # Token patterns
    doom2_map_pattern = re.compile(r'^MAP\s+(\S+)$')
    doom1_map_pattern = re.compile(r'^MAP\s+E(\S+)M(\S+)$')
    property_pattern = re.compile(r'^\s*(\w+)\s*=\s*(.*?)$')
    multi_line_pattern = re.compile(r'^\s*"([^"]+)"$')

    parsed_data = {}
    current_map = None
    current_multi_line_key = None
    current_multi_line_values = []

    for line in lines:
        # Remove leading and trailing whitespaces
        line = line.strip()
        if not line or line.startswith('#'):
            # Skip empty lines and comments
            continue
        
        # Check if the line starts a new MAP block
        map_match = doom2_map_pattern.match(line)
        if map_match:
            current_map = map_match.group(1)
            parsed_data[current_map] = {}
            continue

        map_match = doom1_map_pattern.match(line)
        if map_match:
            current_map = map_match.group(1)
            parsed_data[current_map] = {}
            continue

        # Check if we're in a multi-line property value
        if current_multi_line_key:
            if multi_line_pattern.match(line):
                current_multi_line_values.append(line.strip('"'))
                continue
            else:
                # Assign the collected multi-line values and reset
                parsed_data[current_map][current_multi_line_key] = "\n".join(current_multi_line_values)
                current_multi_line_key = None
                current_multi_line_values = []

        # Check for a property assignment
        property_match = property_pattern.match(line)
        if property_match:
            key = property_match.group(1)
            value = property_match.group(2).strip('"')
            parsed_data[current_map][key] = value
            continue
        
        # Check for multi-line string continuation
        if line.startswith('"') and line.endswith('"'):
            # Start a new multi-line property
            current_multi_line_key = list(parsed_data[current_map].keys())[-1]
            current_multi_line_values = [line.strip('"')]
            continue

    # Handle last multi-line property if still pending
    if current_multi_line_key:
        parsed_data[current_map][current_multi_line_key] = "\n".join(current_multi_line_values)
    
    return parsed_data

# Example usage
if __name__ == '__main__':
    data = b"""MAP E1M7\r\n{\r\n   levelname = "The Hidden Cave"\r\n   skytexture =  "sky2"\r\n   intertext = "You have beaten the shit",\r\n       "out of those big barons",\r\n       "and now must continue the fight."\r\n}"""
    parsed_umapinfo = parse_umapinfo(data)
    # TODO: the only keys we care about here really are:
    # - author
    # - partime
    # - levelname
    # - nextsecret (signifies the level has a secret exit)
    # - next (next map. this _might_ be useful but why would you use another order unless you're something weird like myhouse)
    print(parsed_umapinfo)
