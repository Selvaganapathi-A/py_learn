-- get all table names from sqlite database
SELECT
    name
FROM
    sqlite_master
WHERE
    type = 'table';
