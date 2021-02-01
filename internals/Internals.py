from queue import SimpleQueue
from config import RuntimeConfig
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
    def convert_zones_to_python_structure(zone_list):
        shallow = []
        for zone in zone_list:
            Logger.log.debug("Zone Name : {0}".format(zone['name']))
            for domain_record in zone['records']:
                Logger.log.debug("walking through {0}.{1}".format(domain_record['name'], zone['name']))
                for dns_type in domain_record['entries']:
                    Logger.log.debug("{0} Records : {1}".format(dns_type, len(domain_record['entries'][dns_type])))
                    if domain_record[dns_type] == "loadbalance":
                        q = ZoneUtils.__convert_list_to_queue(domain_record['entries'][dns_type])
                        domain_record['entries'][dns_type] = q
            shallow.append(zone)
        return shallow
