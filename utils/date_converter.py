from datetime import datetime


def str_to_date(date: str) -> datetime:
    return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")


def date_to_str(date: datetime) -> str:
    return date.strftime("%d/%m/%Y %H:%M:%S")
