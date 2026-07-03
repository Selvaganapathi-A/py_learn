import datetime
import sqlite3
from pathlib import Path, WindowsPath

import _sqlite_adapters
import _sqlite_converters


def _register_adapter():
    # ! Adapter for Date
    sqlite3.register_adapter(
        datetime.date,
        _sqlite_adapters.sqlite_adapter_date,
    )
    # ! Adapter for DateTime
    sqlite3.register_adapter(
        datetime.datetime,
        _sqlite_adapters.sqlite_adapter_datetime,
    )
    # ! Adapter for Time
    sqlite3.register_adapter(
        datetime.time,
        _sqlite_adapters.sqlite_adapter_time,
    )
    # ! Adapter for pathlib.Path
    sqlite3.register_adapter(
        Path,
        _sqlite_adapters.sqlite_adapter_Path,
    )
    # ! Adapter for pathlib.WindowsPath
    sqlite3.register_adapter(
        WindowsPath,
        _sqlite_adapters.sqlite_adapter_WindowsPath,
    )


def _register_converter():
    # ! Converter for Date
    sqlite3.register_converter(
        'DATE',
        _sqlite_converters.sqlite_converter_date,
    )
    # ! Converter for Time
    sqlite3.register_converter(
        'TIME',
        _sqlite_converters.sqlite_converter_time,
    )
    # ! Converter for DateTime and Timestamp
    sqlite3.register_converter(
        'DATETIME',
        _sqlite_converters.sqlite_converter_datetime,
    )
    # ! Converter for pathlib.Path
    sqlite3.register_converter(
        'PATH',
        _sqlite_converters.sqlite_converter_Path,
    )
    # ! Converter for pathlib.Path
    sqlite3.register_converter(
        'WindowsPATH',
        _sqlite_converters.sqlite_converter_WindowsPath,
    )


def register_adapter_and_converters():
    _register_adapter()
    _register_converter()


if __name__ == '__main__':
    register_adapter_and_converters()
