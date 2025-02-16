class DemoService:
    def __init__(self, demo_dir):
        self.demo_dir = demo_dir

    def GetDemosForMap(self, map: FlatMap):

        demos = []

        prefix = map.GetMapPrefix()
        files = glob.glob(demo_dir + f"/{prefix}*")

        # Sort the filenames list to group similar combinations together
        files.sort(key=extract_prefix)

        # Group filenames by the common part before the suffixes
        groups = {key: list(group) for key, group 
                in groupby(files, key=extract_prefix)}
        
        for _, group in groups.items():
            demo_files = sorted(group, key=lambda x: x.endswith("-STATS.json"))
            if len(demo_files) > 1:
                demos.append(Demo(demo_files[0], demo_files[1]))
            elif len(demo_files) > 0:
                if demo_files[0].endswith(".lmp"):
                    demos.append(Demo(demo_files[0]))

        # TODO: treat incomplete demos as zero
        return sorted(demos, key=lambda d: d.stats.get_timestamp() or 0, reverse=True)
