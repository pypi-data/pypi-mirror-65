from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Optional,
    Union,
)

from .sparrow_message import Color


class SlackCommand(metaclass=ABCMeta):
    """
    Base Class of User's Command.
    """

    @property
    def color(self) -> str:
        return Color.SUCCESS

    @property
    @abstractmethod
    def execution_words(self) -> Union[list, tuple]:
        """ 특정 명령을 실행할 수 있는 명령어를 반환

        Returns:
            이 명령을 실행할 수 있는 단어의 튜플로 부합하는 명령이 들어오면, `response` 함수를 실행
        """

    @abstractmethod
    def response(self, user_command: str, channel: str, username: str) -> str:
        """ 명령이 실행되는 함수

        Returns:
            slack으로 보내야하는 response 메시지.

        """


class SlackCommandManager:
    commands = []

    @classmethod
    def register(cls, command: SlackCommand):
        cls.commands.append(command)

    @classmethod
    def get_command(cls, command: str) -> Optional[SlackCommand]:
        for cmd in cls.commands:
            if command in cmd.execution_words:
                return cmd
        return None
