from database import Database
from internals import ZoneUtils
from server import DNSServer
from config import RuntimeConfig
from logger import Logger
from watcher import FileWatcher

def main():
    RuntimeConfig.setup()
    Logger.setup(**RuntimeConfig.logger())
    fw = FileWatcher(RuntimeConfig.config())
    database = Database(RuntimeConfig.config())
    Database.in_memory_database = ZoneUtils.convert_zones_to_python_structure(database.get_all_zones())
    server = DNSServer()
    Logger.log.info("Starting DNS Server")
    fw.start()
    server.run_for_ever()


if __name__ == '__main__':
    main()
