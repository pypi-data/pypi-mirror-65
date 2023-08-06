import datetime
import json
import threading
import time
import uuid
import redis

class RedisClient(object):

    def __init__(self, redis_setting):
        self.redis_client = redis.StrictRedis(host=redis_setting.host,
                                              port=redis_setting.port,
                                              db=redis_setting.db,
                                              password=redis_setting.password,
                                              decode_responses=True)

        self._is_connected = self.ping_redis()
        if not self.is_connected():
            raise RuntimeError('redis not connected')

        print('[redis] current connection status (conn){}'.format(self._is_connected))

    def is_connected(self):
        return self._is_connected

    def ping_redis(self):
        try:
            self.redis_client.ping()

        except redis.exceptions.ConnectionError as e:
            self._is_connected = False
            print('[ping] redis connection failed! (err){}'.format(e))
            return False

        else:
            self._is_connected = True
            return True

    def disconnect(self):
        self._is_connected = False


class WechatMessageRedisClient(RedisClient):

    def __init__(self, redis_setting):
        
        RedisClient.__init__(self, redis_setting)

        self.key = redis_setting.key

    def get_message(self):
        message = self.redis_client.lpop(self.key)
        return message
