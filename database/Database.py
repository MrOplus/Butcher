from json import dumps
from queue import SimpleQueue
from pymongo import MongoClient


class Database:
    in_memory_database: list = None

    def __init__(self, connection_string, database):
        self.connection = MongoClient(connection_string)
        self.database = database

    def get_zone(self, zone):
        return self.connection[self.database]['records'].find_one({"zone": zone})

    def get_all_zones(self):
        return self.connection[self.database]['records'].find()

    @staticmethod
    def get_memory_zone(fld):
        return next((x for x in Database.in_memory_database if x["zone"] == fld), None)

    @staticmethod
    def get_primary_ns_record(zone):
        records = sorted(zone['NS'], key=lambda x: x['order'])
        for record in records:
            return record['value']
        return None

    @staticmethod
    def find_memory_record(zone, dns_type, subdomain):
        if subdomain == '':
            subdomain = '@'
        for record in zone['records'] :
            if record['name'] == subdomain :
                q = record['records'][dns_type] # type: SimpleQueue
                if q.qsize() > 0:
                    result = q.get()
                    q.put(result)
                    return result

        return None


