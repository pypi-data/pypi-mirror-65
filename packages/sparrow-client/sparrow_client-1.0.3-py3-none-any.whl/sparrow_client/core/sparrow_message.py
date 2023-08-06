from enum import EnumMeta


class Color(EnumMeta):
    PRIMARY = "#2b7cf6"
    SECONDARY = "#6d757c"
    SUCCESS = "#53a451"
    DANGER = "#cc444a"
    WARNING = "#f7c244"


class SparrowData:
    # inapi python 버전이 낮아 dataclass를 사용하지 못 함
    """
    workspace: str = ""
    username: str = ""
    command: str = ""

    channel: str = ""
    title_text: str = ""

    color: str = Color.SECONDARY
    body_text: str = ""
    """
    def __init__(self, workspace="", username="", command="", channel="", title_text="", color=Color.SECONDARY, body_text=""):
        self.workspace = workspace
        self.username = username
        self.command = command
        self.channel = channel
        self.title_text = title_text
        self.color = color
        self.body_text = body_text


    def get_dict(self) -> dict:
        return self.__dict__
