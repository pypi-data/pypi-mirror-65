import json
import os

from ..queue.redis_queue import RedisQueue
from ..sparrow_exception import InvalidDataPushException
from ..sparrow_message import SparrowData


class Singleton(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class SparrowClientQueue(RedisQueue, metaclass=Singleton):

    def __init__(self, **kwargs):
        host = os.getenv("SPARROW_REDIS_HOST")
        port = int(os.getenv("SPARROW_REDIS_PORT"))
        db = int(os.getenv("SPARROW_REDIS_DB"))

        super().__init__(host, port, db, **kwargs)

    def push(self, sparrow_data: SparrowData):
        sp_dict = sparrow_data.get_dict()

        if not _is_valid_sparrow_data(sp_dict):
            raise InvalidDataPushException(sparrow_data)

        sp_data = json.dumps(sp_dict)

        if isinstance(sp_data, bytes):
            sp_data = sp_data.decode('utf-8')

        self.enqueue(sparrow_data.channel, sp_data)
        return


def _is_valid_sparrow_data(sp_dict: dict) -> bool:
    """
    redis에서 push 직전, pop 직후의 dict 데이터를 통한 유효성 검증
    """
    if not (isinstance(sp_dict, dict)
            and isinstance(sp_dict.get("username"), str)
            and isinstance(sp_dict.get("command"), str)

            and isinstance(sp_dict.get("channel"), str)
            and isinstance(sp_dict.get("title_text"), str)

            and isinstance(sp_dict.get("color"), str)
            and isinstance(sp_dict.get("body_text"), str)):
        return False
    return True
