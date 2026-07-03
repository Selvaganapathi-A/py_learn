import sqlite3
from collections.abc import Generator
from pathlib import Path
from typing import Any, Self


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict[str, Any]:
    result_dictionary: dict[str, Any] = {}
    for column_id, column_name in enumerate(cursor.description):
        result_dictionary[column_name[0]] = row[column_id]
    return result_dictionary


class Database:
    __slots__: tuple[str, ...] = (
        '__connection__',
        '__cursor__',
        '__initialized__',
    )
    __instance__: Self | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
            cls.__instance__.__initialized__ = False
        return cls.__instance__

    def __init__(self, /, database: str | Path, register_row_factory: bool = False) -> None:
        if self.__initialized__:
            return
        if not Path(database).exists():
            FileNotFoundError(database)
        self.__connection__: sqlite3.Connection = sqlite3.connect(
            database=database,
            check_same_thread=True,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        if register_row_factory:
            self.__connection__.row_factory = dict_factory
        self.__cursor__: sqlite3.Cursor = self.__connection__.cursor()
        self.__initialized__ = True

    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection__

    @connection.setter
    def connection(self, value: Any):
        raise ValueError('Cannot assign value.')

    @connection.getter
    def connection(self) -> sqlite3.Connection:
        return self.__connection__

    @connection.deleter
    def connection(self):
        raise NotImplementedError('Action Not Implemented')

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor__

    @cursor.setter
    def cursor(self, value: Any):
        raise ValueError('Cannot assign value.')

    @cursor.getter
    def cursor(self):
        return self.__cursor__

    @cursor.deleter
    def cursor(self):
        raise NotImplementedError('Action Not Implemented')

    def save(self) -> None:
        self.__connection__.commit()

    def save_and_close(self) -> None:
        self.vacuum()
        self.destroy()

    def close(self) -> None:
        self.destroy()

    def destroy(self):
        self.__connection__.close()
        self.__initialized__ = False
        Database.__instance__ = None

    def vacuum(self):
        self.__connection__.commit()
        self.__cursor__.execute('VACUUM;')
        self.__connection__.commit()

    def get_tables(self) -> Generator[Any]:
        self.__cursor__.execute('select name from sqlite_master where type="table";')
        return (x[0] for x in self.__cursor__.fetchall())

    def get_fields(self, table_name: str) -> Generator[str]:
        if self.table_exists(table_name):
            self.__cursor__.execute(
                f'select * from {table_name} limit 1;',
            )
            return (x[0] for x in self.__cursor__.description)
        raise sqlite3.DatabaseError('Table not present in this database.', table_name)

    def get_schema(self, table_name: str) -> str:
        if self.table_exists(table_name):
            self.__cursor__.execute(
                ('select sql from sqlite_master where type="table" and name = ?;'),
                (table_name,),
            )
            return self.__cursor__.fetchone()[0]
        raise sqlite3.DatabaseError('Table not present in this database.', table_name)

    def table_exists(self, table_name: str) -> bool:
        self.__cursor__.execute(
            'select name from sqlite_master where type="table" and name = ?;',
            (table_name,),
        )
        return (table_name,) in self.__cursor__.fetchall()
