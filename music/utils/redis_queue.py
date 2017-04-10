import redis


class RedisDb:
    def __init__(self, queue):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.rdb = redis.Redis(connection_pool=pool)
        self.queue = queue

    def push(self, element):
        self.rdb.rpush(self.queue, element)

    def pop(self):
        return self.rdb.lpop(self.queue)
