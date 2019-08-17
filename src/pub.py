import json

import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)


class Publisher:
    def __init__(self):
        self.db = redis.StrictRedis(connection_pool=pool)

    def do_publish(self, data: dict):
        _data = json.dumps(data)
        self.db.publish('main', _data)
