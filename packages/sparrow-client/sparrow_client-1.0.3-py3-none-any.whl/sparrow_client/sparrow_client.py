import logging
from typing import Union

from .core.queue.sparrow_client_queue import SparrowClientQueue
from .core.slack_command import SlackCommandManager
from .core.sparrow_exception import CommandNotFound
from .core.sparrow_message import (
    Color,
    SparrowData,
)

logger = logging.getLogger(__name__)


def send_slack(channel: str, message: Union[str, list, dict], title: str = "", color: str = Color.SECONDARY):
    """
    Args:
        channel: 메시지를 전송할 channel의 이름
        message: 메시지의 본문
        title: 메시지의 타이틀
        color: slack 메시지의 quote 컬러
    """
    if isinstance(message, list):
        text_buffer = []
        for item in message:
            text_buffer += ">`"
            text_buffer += item
            text_buffer += "` \n"
        body = ''.join(text_buffer)

    elif isinstance(message, dict):
        text_buffer = []
        for key, value in message:
            text_buffer += ">`"
            text_buffer += key
            text_buffer += "`: *"
            text_buffer += value
            text_buffer += "*` \n"
        body = ''.join(text_buffer)
    else:
        body = message

    sparrow_data = SparrowData(channel=channel, title_text=title, color=color, body_text=body)
    SparrowClientQueue().push(sparrow_data)
    return


def execute_command(sparrow_data: SparrowData):
    """ 사용자가 입력한 명령어가 존재하는 명령어인지 확인 후, 해당 명령어에 대한 response의 결과를 슬랙으로 전송
    """
    cmd = SlackCommandManager.get_command(sparrow_data.command)

    if cmd is None:
        logging.exception("command not found")
        raise CommandNotFound(sparrow_data.command)

    message = cmd.response(
        user_command=sparrow_data.command,
        channel=sparrow_data.channel,
        username=sparrow_data.username
    )
    send_slack(channel=sparrow_data.channel, message=message, color=cmd.color)
    return
