import logging
import sys


class Logger:
    __instance__ = None  # type: Logger
    log = None  # type: logging

    def __init__(self):
        if Logger.__instance__ is None:
            Logger.__instance__ = self
            Logger.log = logging

    def configure(self, **config):
        if config['stream'] == True:
            logging.basicConfig(stream=sys.stdout,level=config['level'])
        else:
            logging.basicConfig(**config)


    @staticmethod
    def get_instance():
        if Logger.__instance__ is None:
            return Logger()
        return Logger.__instance__

    @staticmethod
    def setup(**config):
        logger = Logger.get_instance()
        logger.configure(**config)
