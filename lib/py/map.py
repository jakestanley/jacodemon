import os

class FlatMap:
    def __init__(self, ModName, Files, MapId=None, MapName=None, Author=None, 
                 CompLevel=None, Merge=[], Port=None, 
                 Notes=None):

        # public
        self.MapId = MapId

        # private, required
        self._ModName = ModName
        self._Files = Files

        # private, optional
        self._MapName = MapName
        self._Author = Author
        self._CompLevel = CompLevel
        self._Merge = Merge
        self._Port = Port
        self._Notes = Notes

        # set files
        self._dehs = None
        self._patches = None
        self._merges = None

    def SetMapId(self, MapId: str):
        if self._MapId:
            print(f"Warning: setting MapId: '{MapId}' on a map that already has a MapId ('{self._MapId}')")

        self._MapId = MapId

    """
    Happily returns None if MapId has not been set. You may wish to use None 
    to decide to find some MapIds!
    """
    def GetMapId(self):
        return self._MapId

    def SetMapName(self, MapName: str):
        self._MapName = MapName

    def SetAuthor(self, Author: str):
        self._Author = Author

    """
    Populate DEHs, patches and merges based on the patch directory
    Jury's still out on whether or not this should be done in the constructor
    """
    def ProcessFiles(self, pwad_dir: str):

        # build lists of map specific files we need to pass in
        patches = [patch for patch in self._Files.split('|') if patch]
        for patch in patches:
            ext = os.path.splitext(patch)[1]
            path = os.path.join(pwad_dir, patch)
            if ext.lower() == ".deh":
                self._dehs.append(path)
            elif ext.lower() == ".wad":
                self._patches.append(path)
            else:
                print(f"Ignoring unsupported file "'{patch}'"with extension '{ext}'")

        # for chocolate doom/vanilla wad merge emulation
        merges = [merge for merge in self._Merge.split('|') if merge]
        for merge in merges:
            self._merges.append(os.path.join(pwad_dir, merge))

    """
    Get map prefix (used for naming demos and recordings) based on Files or 
    Merges, and MapId
    """
    def GetMapPrefix(self) -> str:

        if len(self._patches) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self._patches[0]))[0]
        elif len(self._merges) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self._merges[0]))[0]
        elif len(self._dehs) > 0:
            mod_prefix = os.path.splitext(os.path.basename(self._dehs[0]))[0]
        else:
            print("Error: Could not get a prefix as there were no files!")
            exit(1)

        if self._MapId:
            return f"{mod_prefix}-{self._MapId}"
        else:
            print("Error: Could not get a prefix as there was no MapId set")
            exit(1)

    def GetFiles(self):
        return self._Files
    
    def Dictify(self):
        dic = {}

        dic['ModName'] = self._ModName
        dic['MapId'] = self._MapId
        dic['MapName'] = self._MapName
        dic['Author'] = self._Author
        dic['CompLevel'] = self._CompLevel
        dic['Files'] = self._Files
        dic['Merge'] = self._Merge
        dic['Port'] = self._Port
        dic['Notes'] = self._Notes

        return dic
