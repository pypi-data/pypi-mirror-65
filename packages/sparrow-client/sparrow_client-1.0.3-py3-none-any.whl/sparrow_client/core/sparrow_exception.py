from .sparrow_message import SparrowData


class InvalidDataPushException(Exception):
    def __init(self, sparrow_data: SparrowData):
        self.sparrow_data = sparrow_data

    def __str__(self):
        return str(self.sparrow_data.get_dict())


class CommandNotFound(Exception):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return "{}는 존재하지 않는 명령어입니다. ".format(self.command)
