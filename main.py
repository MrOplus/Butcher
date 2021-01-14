from database import Database
from internals import ZoneUtils
from server import DNSServer
from config import RuntimeConfig
from logger import Logger


def main():
    RuntimeConfig.setup()
    Logger.setup(**RuntimeConfig.logger())
    database = Database(RuntimeConfig.database()['connection_string'],
                        RuntimeConfig.database()['database_name'])

    zones = database.get_all_zones()
    Database.in_memory_database = ZoneUtils.convert_zones_to_python_structure(zones)
    server = DNSServer()
    Logger.log.info("Starting DNS Server")
    server.run_for_ever()


if __name__ == '__main__':
    main()
