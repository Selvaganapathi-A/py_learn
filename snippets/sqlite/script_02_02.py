def main():
    import datetime
    import sqlite3

    from _init import register_adapter_and_converters
    from _sqlite_database import dict_factory

    #
    register_adapter_and_converters()
    connection: sqlite3.Connection = sqlite3.connect(
        database=':memory:', detect_types=sqlite3.PARSE_DECLTYPES
    )
    #
    connection.row_factory = dict_factory
    #
    cursor: sqlite3.Cursor = connection.cursor()
    #
    query: str = """
    create table datalake(
        pk integer primary key autoincrement,
        value DATE
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
    data: datetime.date = datetime.date(year=1990, month=12, day=5)
    cursor.execute(query, (data,))
    # * select
    query: str = """
    select * from datalake limit 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)
    # ! Close
    connection.close()


if __name__ == '__main__':
    main()
