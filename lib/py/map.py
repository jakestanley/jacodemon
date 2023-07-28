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
    def ProcessFiles(self, PwadDir: str):
        print("Warning: ProcessFiles is not yet implemented!")
        pass

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
