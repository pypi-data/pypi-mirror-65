from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation


class ProjectConfig:
    config = ConfigParser(interpolation=ExtendedInterpolation())
    CONFIG_DIR = Path(__file__).resolve().parent
    config.read(CONFIG_DIR.joinpath("env.cfg"))

    def __init__(self, env: str = "DEFAULT"):
        self.use_koverj = self.config.getboolean(env, "use_koverj")
        self.log_locators = self.config.getboolean(env, "log_locators")
        self.service_url = self.config.get(env, "service_url")
