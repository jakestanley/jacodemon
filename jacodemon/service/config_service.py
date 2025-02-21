from jacodemon.model.config import Config, GetConfig

class ConfigService:

    def __init__(self) -> Config:
        self.config = GetConfig()

