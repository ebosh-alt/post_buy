from dataclasses import dataclass
from datetime import timezone, timedelta

tz = "6"
timezone_offset = 6.0  # Pacific Standard Time (UTC−08:00)
tzinfo = timezone(timedelta(hours=timezone_offset))
# datetime.now(tzinfo)

@dataclass
class Profile:
    name_organization: str = "Unknown"
    number_phone: str = "Unknown"
    inn: str = "Unknown"

