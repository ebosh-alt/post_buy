from dataclasses import dataclass, field


@dataclass
class Post:
    id_user: int = 0
    text: str = ""
    date: str = ""
    fixing: bool = False
    photo: str = ""
    video: str = ""
    category_channel: str = ""
    name_channels: tuple[str] | None = field(default_factory=tuple)
    message_id: int = 0
    price: int = 0
