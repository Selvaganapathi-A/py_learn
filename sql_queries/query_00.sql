CREATE TABLE IF NOT EXISTS
    Department (pk INTEGER PRIMARY KEY AUTOINCREMENT, department_name VARCHAR(256) UNIQUE);


INSERT INTO
    Department (pk, department_name)
VALUES
    (1, 'Accounts'),
    (2, 'Developer'),
    (3, 'Manager'),
    (4, 'CEO'),
    (5, 'Sales'),
    (6, 'Service');


CREATE TABLE IF NOT EXISTS
    Employee (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(256),
        last_name VARCHAR(256),
        salary INTEGER,
        department_id INTEGER,
        manager_id INTEGER,
        country VARCHAR(256),
        FOREIGN KEY (department_id) REFERENCES Department (pk) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (manager_id) REFERENCES Employee (pk) ON DELETE SET NULL ON UPDATE CASCADE
    );


INSERT INTO
    Employee (pk, first_name, last_name, salary, department_id, manager_id, country)
VALUES
    (1, 'Dominic', 'Gibbs', 12152, 1, 26, 'Mayotte'),
    (2, 'Manuel', 'Alvarado', 13319, 2, 7, 'Fiji'),
    (3, 'Pearl', 'Sullivan', 19648, 3, 19, 'New Caledonia'),
    (4, 'Scott', 'Hawkins', 15703, 5, 26, 'United Arab Emirates'),
    (5, 'Josie', 'Perkins', 19834, 1, 4, 'Diego Garcia'),
    (6, 'Herbert', 'Pittman', 20062, 3, 8, 'Kazakhstan'),
    (7, 'Norman', 'Medina', 18091, 6, 6, 'Colombia'),
    (8, 'Alvin', 'McGuire', 6487, 4, NULL, 'St. Kitts & Nevis'),
    (9, 'Dustin', 'McGuire', 7360, 1, 25, 'Tonga'),
    (10, 'Milton', 'Todd', 7340, 6, 15, 'Mauritania'),
    (11, 'Ophelia', 'Goodman', 5281, 3, 19, 'Comoros'),
    (12, 'Warren', 'Gibbs', 13136, 5, 25, 'Uruguay'),
    (13, 'Rosalie', 'Hogan', 15682, 1, 26, 'French Southern Territories'),
    (14, 'Adam', 'Gibson', 22882, 6, 28, 'Niger'),
    (15, 'Jackson', 'Castillo', 20833, 3, 8, 'Egypt'),
    (16, 'Zachary', 'Hicks', 18146, 6, 27, 'Armenia'),
    (17, 'Hulda', 'Dixon', 7806, 5, 13, 'Haiti'),
    (18, 'Leon', 'Tran', 8577, 1, 25, 'Armenia'),
    (19, 'Rhoda', 'Bowers', 9849, 3, 19, 'Guinea-Bissau'),
    (20, 'Lawrence', 'Roberts', 11997, 2, 7, 'St. Barthélemy'),
    (21, 'Marc', 'Elliott', 18538, 6, 19, 'Bolivia'),
    (22, 'Isabelle', 'Peterson', 5894, 5, 18, 'Guernsey'),
    (23, 'Cynthia', 'Diaz', 16684, 2, 21, 'Czech Republic'),
    (24, 'Verna', 'Vargas', 19367, 1, 5, 'Togo'),
    (25, 'Brandon', 'Wallace', 15958, 1, 5, 'Djibouti'),
    (26, 'Maggie', 'Nichols', 17002, 1, 5, 'Ecuador'),
    (27, 'Vincent', 'Allison', 16360, 3, 19, 'Tajikistan'),
    (28, 'Edgar', 'Swanson', 23542, 2, 21, 'St. Lucia'),
    (29, 'Lizzie', 'Shelton', 5359, 4, 8, 'Kiribati');
