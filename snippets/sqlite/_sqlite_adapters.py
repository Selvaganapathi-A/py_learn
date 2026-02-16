import datetime
from pathlib import Path, WindowsPath

import pytz


def sqlite_adapter_date(value: datetime.date) -> bytes:
    return value.isoformat().encode(encoding="UTF-8")


def sqlite_adapter_time(value: datetime.time) -> bytes:
    return value.isoformat(timespec="microseconds").encode(encoding="UTF-8")


def sqlite_adapter_FILE_TIMESTAMP(value: float) -> bytes:
    return str(value).encode()


def sqlite_adapter_datetime(value: datetime.datetime) -> bytes:
    if value.tzinfo is None:
        value = pytz.timezone(zone="Asia/Calcutta").localize(dt=value)
    return value.isoformat(timespec="microseconds").encode(encoding="UTF-8")


def sqlite_adapter_Path(value: Path) -> bytes:
    return str(value).encode("utf-8")


def sqlite_adapter_WindowsPath(value: WindowsPath) -> bytes:
    return str(value).encode("utf-8")
