import json

import redis

from config import config

pool = redis.ConnectionPool(host=config['redis_host'], port=config['redis_port'])


class Publisher:
    def __init__(self):
        self.db = redis.StrictRedis(connection_pool=pool)

    def do_publish(self, data: dict):
        _data = json.dumps(data)
        self.db.publish('main', _data)
