from jacodemon.misc.files import ParseTimestampFromPath

from jacodemon.model.launch import LaunchSpec
from jacodemon.model.map import Map

def LegacyStatisticsArgsToLaunchSpec(args, demo, map: Map):

    parsed_args = {}

    # Iterate through the list, skipping the executable
    i = 1  # Start after the executable
    while i < len(args):
        # Check if the current item is a switch (i.e., it starts with '-')
        if args[i].startswith('-'):
            switch = args[i][1:]  # Remove the leading '-' from the switch name
            parsed_args[switch] = []

            # Check if the next item is a value (i.e., it's not another switch)
            i += 1
            while i < len(args) and not args[i].startswith('-'):
                parsed_args[switch].append(args[i])
                i += 1
        else:
            i += 1

    # we'll have to generate one based on what we have. it may be inaccurate
    # TODO: WARN log or in UI that as there is no launch config, demo may desync
    timestamp = ParseTimestampFromPath(demo)
    # wads must be a list
    name = f"{map.GetPrefix()}-{timestamp}"
    return LaunchSpec(
        name=name,
        map_id=map.MapId,
        timestamp=timestamp,
        iwad=parsed_args['iwad'][0],
        wads=[(file, "nohash") for file in parsed_args['file']],
        dehs=[],
        mods=[],
        fast_monsters="-fast" in parsed_args.keys(),
        skill=parsed_args['skill'][0],
        comp_level=parsed_args['complevel'][0]
    )
