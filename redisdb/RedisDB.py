import redis


class RedisDB:
    _instance = None

    @staticmethod
    def get_instance() -> redis.Redis:
        if RedisDB._instance is None:
            raise Exception("Not Initialized yet!")
        return RedisDB._instance.get_redis()

    def get_redis(self) -> redis.Redis:
        return self.redis

    def __init__(self, config: dict):
        if RedisDB._instance is not None:
            raise Exception("RedisDB is a singleton")
        RedisDB._instance = self
        self.config = config
        self.redis = redis.Redis(**config)
