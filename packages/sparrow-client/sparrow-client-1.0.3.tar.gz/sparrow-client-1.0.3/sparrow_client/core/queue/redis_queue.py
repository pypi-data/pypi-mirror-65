from typing import Optional

import redis


class RedisQueue:
    def __init__(self, host: str, port: int, db: int, **kwargs):
        pool = redis.ConnectionPool(
            host=host, port=port, db=db, max_connections=10, **kwargs
        )
        self._redis = redis.StrictRedis(charset="utf-8", decode_responses=True, connection_pool=pool)

    def get_connection(self) -> redis.StrictRedis:
        return self._redis

    def get_list(self, key) -> list:
        return self._redis.lrange(key, 0, -1)

    def count(self, key, value):
        """ 특정 키 내의 동일한 value의 개수를 반환합니다. """
        return self.get_list(key).count(value)

    def enqueue(self, key, value):
        self._redis.rpush(key, value)

    def dequeue(self, key) -> Optional[str]:
        """ 키에 value가 존재하지 않는 경우 None """
        return self._redis.lpop(key)

    def remove(self, key, value) -> int:
        """ key의 list에서 동일한 value를 모두 지우고 그 개수를 반환 """
        return self._redis.lrem(key, 0, value)

    def _clear_queue(self, key) -> int:
        return self._redis.delete(key)

    def size(self, key) -> int:
        return self._redis.llen(key)

    def get_keys(self) -> list:
        return self._redis.keys()
