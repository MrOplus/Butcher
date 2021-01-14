from queue import SimpleQueue
from config import RuntimeConfig
import pymongo
from logger import Logger

class ZoneUtils:
    @staticmethod
    def __convert_list_to_queue(records: list) -> SimpleQueue:
        records = sorted(records, key=lambda x: x['order'])
        queue = SimpleQueue()
        for i in records:
            for j in range(0, i['weight']):
                queue.put(i)
        return queue

    @staticmethod
    def convert_zones_to_python_structure(zone_list: pymongo.cursor):
        shallow = []
        for zone in zone_list:
            Logger.log.debug("Zone Name : {0}".format(zone['zone']))
            for domain_record in zone['records']:
                Logger.log.debug("walking through {0}.{1}".format(domain_record['name'], zone['zone']))
                settings = domain_record['settings']
                for dns_type in domain_record['records']:
                    Logger.log.debug("{0} Records : {1}".format(dns_type, len(domain_record['records'][dns_type])))
                    if settings[dns_type] == "loadbalance":
                        q = ZoneUtils.__convert_list_to_queue(domain_record['records'][dns_type])
                        domain_record['records'][dns_type] = q
            shallow.append(zone)
        return shallow
