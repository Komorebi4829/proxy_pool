import redis
import ast


class RedisOperator(object):

    def __init__(self,
                 host='localhost',
                 port=6379,
                 decode_responses=True
                 ):
        self.r = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    def get(self, key):
        return self.r.get(key)

    def hget(self, key, filed):
        return self.r.hget(key, filed)

    def set(self, key, value):
        return self.r.set(key, value)

    def lpush(self, key, value):
        return self.r.lpush(key, value)

    def lrem(self, key, count, value):
        return self.r.lrem(key, count, value)

    def hset(self, key, filed, value):
        return self.r.hset(key, filed, value)

    def hsetall(self, key, kws):
        for k, v in kws.items():
            self.r.hset(key, k, v)
        return True

    def hgetall(self, key):
        return self.r.hgetall(key)

    def delete(self, key):
        return self.r.delete(key)

    def hincrby(self, key, field):
        return self.r.hincrby(key, field)

    def hexists(self, key, field):
        return self.r.hexists(key, field)

    def hkeys(self, key):
        return self.r.hkeys(key)

    def hdel(self, key, field):
        return self.r.hdel(key, field)

    def hlen(self, key):
        return self.r.hlen(key)
