from dataclasses import dataclass

tz = 3


@dataclass
class Profile:
    name_organization: str = "Unknown"
    number_phone: str = "Unknown"
    inn: str = "Unknown"

