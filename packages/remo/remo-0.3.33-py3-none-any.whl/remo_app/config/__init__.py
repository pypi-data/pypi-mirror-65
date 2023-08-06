import os
import json
from pathlib import Path


class Config:
    __slots__ = ['port', 'server', 'user_name', 'user_email', 'user_password', 'conda_env', 'viewer', 'debug']

    def __init__(self, config: dict):
        for name in self.__slots__:
            setattr(self, name, config.get(name))

        if 'debug' not in config or not isinstance(self.debug, bool):
            self.debug = False

    def is_local_server(self):
        return self.server == 'http://localhost'

    def get_host_address(self):
        is_default_port = ((self.server.startswith('http://') and self.port == "80")
                           or (self.server.startswith('https://') and self.port == "443"))
        if is_default_port:
            return self.server
        else:
            return '{}:{}'.format(self.server, self.port)

    @staticmethod
    def get_path():
        REMO_HOME = os.getenv('REMO_HOME', str(Path.home().joinpath('.remo')))
        return str(os.path.join(REMO_HOME, 'remo.json'))

    @staticmethod
    def is_exists():
        return os.path.exists(Config.get_path())

    @staticmethod
    def load_config():
        cfg_path = Config.get_path()
        return Config.parse(cfg_path)

    @staticmethod
    def parse(config_path):
        if not os.path.exists(config_path):
            return None

        with open(config_path) as cfg_file:
            config = json.load(cfg_file)

        return Config(config)
