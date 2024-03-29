import json
from queue import SimpleQueue
import random
from venv import logger

from config import RuntimeConfig
from logger import Logger
from redisdb import RedisDB


class Database:
    in_memory_database: list = None

    def __init__(self, config_path):
        with open(config_path,mode='r',encoding='utf8') as f :
            self.config = json.loads(f.read())

    def get_all_zones(self):
        return self.config

    @staticmethod
    def get_memory_zone(fld):
        return next((x for x in Database.in_memory_database if x["name"] == fld), None)

    @staticmethod
    def find_memory_record(zone, dns_type, subdomain,request_address):
        if subdomain == '':
            subdomain = '@'
        for record in zone['records']:
            if record['name'] == subdomain:
                if not dns_type in record['entries']:
                    return None
                if record[dns_type] == "loadbalance":
                    q = record['entries'][dns_type]  # type: SimpleQueue
                    key = "{}.{}:{}".format(subdomain, zone['name'], request_address)
                    redis_value = RedisDB.get_instance().get(key)
                    if redis_value is not None:
                        Logger.log.debug("Cache hit for {}".format(key))
                        return json.loads(redis_value)
                    if q.qsize() > 0:
                        result = q.get()
                        q.put(result)
                        RedisDB.get_instance().setex(key,RuntimeConfig.get_instance().cache_duration(), json.dumps(result))
                        Logger.log.debug("Cache miss for {}".format(key))
                        return result
                elif record[dns_type] == "random":
                    return random.choice(record['entries'][dns_type])
                elif record[dns_type] == "all":
                    return sorted(record['entries'][dns_type],key=lambda x: x['order'])
        return None
