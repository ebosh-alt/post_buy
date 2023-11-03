from dataclasses import dataclass

tz = 6


@dataclass
class Profile:
    name_organization: str = "Unknown"
    number_phone: str = "Unknown"
    inn: str = "Unknown"

