CREATE TABLE
    Customers (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(256),
        email VARCHAR(512) UNIQUE
    );


CREATE TABLE
    Orders (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date VARCHAR(32),
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES Customers (pk) ON DELETE CASCADE
    );


--
CREATE TABLE
    Users (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(256),
        last_name VARCHAR(256),
        email VARCHAR(256) UNIQUE,
        city VARCHAR(256),
    );


INSERT INTO
    Users (first_name, last_name, email, city)
VALUES
    (?, ?, ?, ?) ON CONFLICT (email) DO
UPDATE
SET
    first_name = excluded.first_name,
    last_name = excluded.last_name city = excluded.city;


-- ('John', 'Doe', 'john@example.com', 'New York'),
-- ('Todd', 'Baldwin', 'toddcokleg@hotpa.gr', 'Central African Republic'),
-- ('Amelia', 'Steele', 'ameliamoz@awoma.vc', 'Canary Islands'),
-- ('Owen', 'Dunn', 'dwenjokepek@ri.af', 'Liechtenstein'),
-- ('Jane', 'Smith', 'jane@example.com', 'New Mexico');
--
--
INSERT OR IGNORE INTO
    Users (first_name, last_name, email, city)
VALUES
    (?, ?, ?, ?);


--
SELECT
    pk
FROM
    Users
WHERE
    email = ?;
