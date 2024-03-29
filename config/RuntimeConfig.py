from typing import Any
from pathlib import Path
import yaml
import os


class RuntimeConfig:
    __instance__ = None # type: RuntimeConfig

    def __init__(self, config: dict):
        if self.__instance__ is None:
            RuntimeConfig.__instance__ = self
            self.config = config

    def __getitem__(self, item):
        print(item)

    @staticmethod
    def setup():
        p = Path(__file__)
        conf_path = os.path.join(p.parent.parent,"config.yaml")
        config_file = open(conf_path, mode='r')
        config = yaml.load(config_file, yaml.FullLoader)
        RuntimeConfig(config)

    @staticmethod
    def get_instance():
        return RuntimeConfig.__instance__

    @staticmethod
    def config():
        return RuntimeConfig.__instance__.config['config']['path']

    @staticmethod
    def verbose():
        return RuntimeConfig.__instance__.config['verbose']

    @staticmethod
    def logger():
        return RuntimeConfig.__instance__.config['logger']

    @staticmethod
    def network():
        return RuntimeConfig.__instance__.config['network']

    @staticmethod
    def redis() -> dict:
        return RuntimeConfig.__instance__.config['redis']

    @staticmethod
    def cache_duration() -> int:
        return RuntimeConfig.__instance__.config['cache_duration']
