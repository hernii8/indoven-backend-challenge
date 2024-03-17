from datetime import datetime


class InvalidDateError(Exception):
    pass


def str_to_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        raise InvalidDateError


def date_to_str(date: datetime) -> str:
    try:
        return date.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        raise InvalidDateError
