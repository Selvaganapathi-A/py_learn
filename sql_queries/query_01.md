SQL (Structured Query Language) is used to interact with relational databases. Below are some basic, intermediate, and advanced SQL queries with examples.

### 1. **Basic SQL Queries**

#### **Select Query**

```sql
SELECT column1, column2
FROM table_name;
```

*Example:*

```sql
SELECT first_name, last_name
FROM employees;
```

#### **Select All Columns**

```sql
SELECT *
FROM table_name;
```

#### **Where Clause**

```sql
SELECT *
FROM employees
WHERE department = 'Sales';
```

#### **Order By**

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

#### **Distinct Values**

```sql
SELECT DISTINCT department
FROM employees;
```

#### **Limit the Number of Results**

```sql
SELECT *
FROM employees
LIMIT 5;
```

### 2. **Intermediate SQL Queries**

#### **Aggregate Functions**

* **COUNT, SUM, AVG, MIN, MAX**

```sql
SELECT COUNT(*), AVG(salary), MAX(salary)
FROM employees;
```

#### **GROUP BY**

```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department;
```

#### **HAVING Clause**

```sql
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

#### **JOINs**

* **INNER JOIN**

```sql
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;
```

* **LEFT JOIN**

```sql
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id;
```

#### **Subqueries**

```sql
SELECT first_name, last_name
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

#### **LIKE and Wildcards**

```sql
SELECT *
FROM employees
WHERE first_name LIKE 'J%';
```

### 3. **Advanced SQL Queries**

#### **CASE Statement**

```sql
SELECT first_name, last_name,
    CASE
        WHEN salary > 100000 THEN 'High'
        WHEN salary BETWEEN 50000 AND 100000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_category
FROM employees;
```

#### **Window Functions**

```sql
SELECT first_name, last_name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

#### **CTE (Common Table Expressions)**

```sql
WITH department_sales AS (
    SELECT department_id, SUM(salary) as total_salary
    FROM employees
    GROUP BY department_id
)
SELECT d.department_name, ds.total_salary
FROM departments d
JOIN department_sales ds ON d.department_id = ds.department_id;
```

#### **UNION and UNION ALL**

```sql
SELECT first_name, last_name
FROM employees WHERE department = 'HR'
UNION
SELECT first_name, last_name
FROM employees WHERE department = 'Finance';
```

#### **EXISTS Clause**

```sql
SELECT first_name, last_name
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM departments d
    WHERE d.department_id = e.department_id AND d.department_name = 'Sales'
);
```

### 4. **DDL and DML Queries**

#### **Create Table**

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10, 2)
);
```

#### **Insert Data**

```sql
INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (1, 'John', 'Doe', 101, 75000);
```

#### **Update Data**

```sql
UPDATE employees
SET salary = salary * 1.1
WHERE department_id = 101;
```

#### **Delete Data**

```sql
DELETE FROM employees
WHERE salary < 30000;
```

#### **Drop Table**

```sql
DROP TABLE employees;
```

### 5. **Complex Example Query**

Imagine you want to find the top 3 highest-paid employees from each department.

```sql
WITH ranked_salaries AS (
    SELECT
        employee_id,
        first_name,
        last_name,
        department_id,
        salary,
        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank
    FROM employees
)
SELECT *
FROM ranked_salaries
WHERE rank <= 3;
```

This query uses **window functions** and **CTE** to rank employees by salary within each department and fetch the top 3.

### 6. **Tips for Writing Efficient SQL Queries**

* **Use Indexes:** Indexes on columns used in WHERE, JOIN, and ORDER BY can significantly improve performance.
* **Avoid SELECT ***:** Specify the columns to fetch; it reduces data retrieval time.
* **Filter Early:** Use WHERE clauses to limit data as early as possible in your query.
* **Use EXISTS Instead of IN:** For subqueries, EXISTS can be more efficient than IN, especially with large datasets.

Let me know if you need any specific SQL queries or additional explanations!
