from jacodemon.model.config import Config, GetConfig

class ConfigService:

    def __init__(self) -> Config:
        self.config = GetConfig()

    def GetExecutableForSourcePort(self, source_port_name: str) -> str:
        if source_port_name == "dsdadoom":
            return self.config.dsda_path
        
    def GetCfgPathForSourcePort(self, source_port_name: str) -> str:
        if source_port_name == "dsdadoom":
            return self.config.dsda_cfg
