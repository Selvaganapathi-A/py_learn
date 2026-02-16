def main():
    import pathlib
    import sqlite3

    from _init import register_adapter_and_converters
    from _sqlite_database import dict_factory

    register_adapter_and_converters()
    connection: sqlite3.Connection = sqlite3.connect(
        database=":memory:", detect_types=sqlite3.PARSE_DECLTYPES
    )
    connection.row_factory = dict_factory
    cursor: sqlite3.Cursor = connection.cursor()
    query: str = """
    create table datalake(
        pk integer primary key autoincrement,
        value WindowsPATH
    );
    """
    # * create
    cursor.execute(query)
    # * insert
    query: str = """
    insert into datalake(
        value
    ) values (?);
    """
    data: pathlib.Path = pathlib.Path().resolve()
    cursor.execute(query, (data,))
    data: pathlib.Path = pathlib.WindowsPath("./readme.md").resolve()
    cursor.execute(query, (data,))
    # * select
    query: str = """
    select * from datalake limit 10;
    """
    cursor.execute(query)
    result = cursor.fetchmany(10)
    print(result)
    # ! Close
    connection.close()


if __name__ == "__main__":
    main()
