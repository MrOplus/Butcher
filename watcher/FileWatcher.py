import time
from threading import Thread
import os

from config import RuntimeConfig
from database import Database
from internals import ZoneUtils
from logger import Logger


class FileWatcher:
    def __init__(self, conf_file) -> None:
        super().__init__()
        self.conf_file = conf_file
        self.watcherThread = Thread(target=self.fs_watcher)
        Logger.log.debug("Starting FS Watcher")

    def start(self):
        self.watcherThread.start()

    def stop(self):
        self.watcherThread.join(1)

    def fs_watcher(self):
        last_seen = os.stat(self.conf_file).st_mtime
        while True:
            time.sleep(5)
            current_time = os.stat(self.conf_file).st_mtime
            if current_time > last_seen:
                Logger.log.info("Config File has been changed")
                last_seen = current_time
                database = Database(RuntimeConfig.config())
                Database.in_memory_database = ZoneUtils.convert_zones_to_python_structure(database.get_all_zones())
                Logger.log.info("Update Finished")