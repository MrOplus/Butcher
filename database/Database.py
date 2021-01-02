from pymongo import MongoClient


class Database:
    def __init__(self, connection_string, database):
        self.connection = MongoClient(connection_string)
        self.database = database

    def get_zone(self, zone):
        return self.connection[self.database]['records'].find_one({"zone": zone})

    @staticmethod
    def get_records(zone: dict, rtype: str):
        records = zone['records']
        result = []
        for r in records:
            if r['type'] == rtype:
                result.append(r)
        return result

    @staticmethod
    def get_prior_record(zone: dict, rtype: str):
        records = zone['records']
        result = []
        for r in records:
            if r['type'] == rtype:
                result.append(r)
        lst = sorted(result, key=lambda x: x['priority'])
        if len(lst) > 0:
            return lst[0]
        else:
            return None
