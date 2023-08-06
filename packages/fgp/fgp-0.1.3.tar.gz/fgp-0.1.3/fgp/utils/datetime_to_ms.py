import datetime


def datetime_to_ms(dt: datetime.datetime) -> int:
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000
