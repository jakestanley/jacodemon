class Mod:
    def __init__(self, path: str, enabled: bool = True):
        self.path = path
        self.enabled = enabled

    def to_dict(self):
        dic = {}
        dic['path'] = self.path
        dic['enabled'] = self.enabled
        return dic
    
    @classmethod
    def from_dict(cls, dic: dict):
        return cls(dic['path'], dic['enabled'])
