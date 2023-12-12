import datetime


def parse(publication_time: str, fix_day: int = 0) -> str:
    day, month = publication_time.split(' ')[0].split('/')
    hour, minute = publication_time.split(' ')[1].split(":")
    publication_time = ((datetime.datetime(year=datetime.datetime.now().year, month=int(month), day=int(day),
                                           hour=int(hour), minute=int(minute)) + + datetime.timedelta(days=fix_day)).
                        strftime("%Y/%m/%d %H:%M"))
    return publication_time
