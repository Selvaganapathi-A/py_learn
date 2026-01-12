import datetime
from pathlib import Path, WindowsPath


def sqlite_converter_date(value: bytes) -> datetime.date:
    return datetime.date.fromisoformat(value.decode(encoding='UTF-8'))


def sqlite_converter_time(value: bytes) -> datetime.time:
    return datetime.time.fromisoformat(value.decode(encoding='UTF-8'))


def sqlite_converter_datetime(value: bytes) -> datetime.datetime:
    return datetime.datetime.fromisoformat(value.decode(encoding='UTF-8'))


def sqlite_converter_FILE_TIMESTAMP(value: bytes) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(float(value))


def sqlite_converter_Path(value: bytes) -> Path:
    return Path(value.decode('utf-8'))


def sqlite_converter_WindowsPath(value: bytes) -> WindowsPath:
    return WindowsPath(value.decode('utf-8'))
