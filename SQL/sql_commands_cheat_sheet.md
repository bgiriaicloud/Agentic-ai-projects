# Master SQL Commands Cheat Sheet & Complete Reference Guide

A comprehensive, publication-grade SQL reference guide covering **all major SQL commands**, definitions, syntax specifications, and working code examples across ANSI SQL, PostgreSQL, MySQL, Snowflake, and BigQuery.

---

## 📋 Table of Contents
* [1. Data Query Language (DQL)](#1-data-query-language-dql)
* [2. Data Manipulation Language (DML)](#2-data-manipulation-language-dml)
* [3. Data Definition Language (DDL)](#3-data-definition-language-ddl)
* [4. Data Control Language (DCL)](#4-data-control-language-dcl)
* [5. Transaction Control Language (TCL)](#5-transaction-control-language-tcl)
* [6. JOIN Types & Operations](#6-join-types--operations)
* [7. Set Operations](#7-set-operations)
* [8. Advanced Window Functions & CTEs](#8-advanced-window-functions--ctes)
* [9. Conditional & Built-in Functions](#9-conditional--built-in-functions)
* [10. Database Constraints & Schema Rules](#10-database-constraints--schema-rules)

---

## 1. Data Query Language (DQL)

DQL commands are used to query data from database tables.

### 1.1 `SELECT`
*   **Definition**: Retrieves rows and columns from one or more tables.
*   **Syntax**: `SELECT column1, column2 FROM table_name;`
*   **Example**:
```sql
SELECT employee_id, first_name, salary 
FROM employees;
```

### 1.2 `DISTINCT`
*   **Definition**: Filters out duplicate values from the output query results.
*   **Syntax**: `SELECT DISTINCT column1 FROM table_name;`
*   **Example**:
```sql
SELECT DISTINCT department_id 
FROM employees;
```

### 1.3 `WHERE`
*   **Definition**: Filters records before aggregation based on specified conditions.
*   **Syntax**: `SELECT columns FROM table_name WHERE condition;`
*   **Example**:
```sql
SELECT first_name, salary 
FROM employees 
WHERE salary >= 75000 AND status = 'ACTIVE';
```

### 1.4 `GROUP BY`
*   **Definition**: Groups rows sharing the same values into summary rows.
*   **Syntax**: `SELECT column1, COUNT(*) FROM table_name GROUP BY column1;`
*   **Example**:
```sql
SELECT department_id, AVG(salary) AS avg_salary 
FROM employees 
GROUP BY department_id;
```

### 1.5 `HAVING`
*   **Definition**: Filters summary groups *after* `GROUP BY` aggregation has been computed.
*   **Syntax**: `SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > n;`
*   **Example**:
```sql
SELECT department_id, COUNT(*) AS emp_count 
FROM employees 
GROUP BY department_id 
HAVING COUNT(*) > 10;
```

### 1.6 `ORDER BY`
*   **Definition**: Sorts result sets in ascending (`ASC`) or descending (`DESC`) order.
*   **Syntax**: `SELECT columns FROM table ORDER BY column1 ASC|DESC;`
*   **Example**:
```sql
SELECT first_name, salary 
FROM employees 
ORDER BY salary DESC, first_name ASC;
```

### 1.7 `LIMIT` / `OFFSET` / `FETCH FIRST`
*   **Definition**: Restricts the maximum number of rows returned by a query (for pagination).
*   **Syntax (PostgreSQL/MySQL)**: `SELECT columns FROM table LIMIT n OFFSET m;`
*   **Syntax (ANSI SQL)**: `SELECT columns FROM table FETCH FIRST n ROWS ONLY;`
*   **Example**:
```sql
SELECT employee_id, salary 
FROM employees 
ORDER BY salary DESC 
LIMIT 10 OFFSET 20;
```

### 1.8 `AS` (Aliasing)
*   **Definition**: Assigns a temporary column or table alias name for readability.
*   **Syntax**: `SELECT column_name AS alias_name FROM table_name AS t_alias;`
*   **Example**:
```sql
SELECT first_name AS fname, total_amount AS total 
FROM orders AS o;
```

---

## 2. Data Manipulation Language (DML)

DML commands insert, update, delete, and merge data records within tables.

### 2.1 `INSERT INTO`
*   **Definition**: Inserts new rows into a specified table.
*   **Syntax**: `INSERT INTO table_name (col1, col2) VALUES (val1, val2);`
*   **Example**:
```sql
INSERT INTO employees (employee_id, first_name, salary, department_id) 
VALUES (101, 'Jane', 95000, 4);
```

### 2.2 `INSERT INTO ... SELECT`
*   **Definition**: Copies rows from one query result directly into a target table.
*   **Syntax**: `INSERT INTO target_table (cols) SELECT cols FROM source_table;`
*   **Example**:
```sql
INSERT INTO archived_employees (employee_id, first_name, salary)
SELECT employee_id, first_name, salary 
FROM employees 
WHERE status = 'TERMINATED';
```

### 2.3 `UPDATE`
*   **Definition**: Modifies existing row values in a table.
*   **Syntax**: `UPDATE table_name SET col1 = val1 WHERE condition;`
*   **Example**:
```sql
UPDATE employees 
SET salary = salary * 1.10, updated_at = CURRENT_TIMESTAMP 
WHERE department_id = 2;
```

### 2.4 `DELETE FROM`
*   **Definition**: Removes specified rows from a table based on a condition.
*   **Syntax**: `DELETE FROM table_name WHERE condition;`
*   **Example**:
```sql
DELETE FROM sessions 
WHERE last_active_date < '2025-01-01';
```

### 2.5 `MERGE` / `UPSERT`
*   **Definition**: Performs an atomic conditional update, insert, or delete operation in a single statement.
*   **Syntax (ANSI SQL / Snowflake)**:
```sql
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id
WHEN MATCHED THEN
  UPDATE SET t.name = s.name, t.price = s.price
WHEN NOT MATCHED THEN
  INSERT (id, name, price) VALUES (s.id, s.name, s.price);
```
*   **Syntax (PostgreSQL UPSERT)**:
```sql
INSERT INTO users (id, name, email)
VALUES (1, 'Alice', 'alice@example.com')
ON CONFLICT (id) 
DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email;
```

---

## 3. Data Definition Language (DDL)

DDL commands create, modify, and drop database schemas and structures.

### 3.1 `CREATE DATABASE` / `DROP DATABASE`
*   **Definition**: Creates a new logical database instance or deletes an existing database.
*   **Example**:
```sql
CREATE DATABASE analytics_db;
DROP DATABASE test_db;
```

### 3.2 `CREATE TABLE`
*   **Definition**: Defines a new physical table with column names, data types, and constraints.
*   **Example**:
```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    salary NUMERIC(10, 2) CHECK (salary > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 `ALTER TABLE`
*   **Definition**: Modifies existing table structures (add, drop, rename, or modify columns/constraints).
*   **Example**:
```sql
-- Add column
ALTER TABLE employees ADD COLUMN phone_number VARCHAR(20);

-- Drop column
ALTER TABLE employees DROP COLUMN phone_number;

-- Modify column type
ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12, 2);

-- Rename column
ALTER TABLE employees RENAME COLUMN first_name TO given_name;
```

### 3.4 `DROP TABLE`
*   **Definition**: Permanently deletes a table structure and all of its data from storage.
*   **Syntax**: `DROP TABLE table_name;`
*   **Example**:
```sql
DROP TABLE IF EXISTS legacy_logs;
```

### 3.5 `TRUNCATE TABLE`
*   **Definition**: Quickly deletes ALL rows from a table without logging individual row deletions (faster than `DELETE FROM` without conditions). Cannot be rolled back in some engines.
*   **Example**:
```sql
TRUNCATE TABLE staging_events;
```

### 3.6 `CREATE VIEW` / `CREATE MATERIALIZED VIEW`
*   **Definition**:
    *   `VIEW`: A saved, virtual query template.
    *   `MATERIALIZED VIEW`: Stores actual pre-computed physical query results on disk.
*   **Example**:
```sql
-- Virtual View
CREATE VIEW high_earners_vw AS
SELECT employee_id, first_name, salary 
FROM employees WHERE salary > 100000;

-- Materialized View
CREATE MATERIALIZED VIEW monthly_sales_summary_mv AS
SELECT DATE_TRUNC('month', order_date) AS mth, SUM(amount) AS total_sales
FROM orders
GROUP BY 1;
```

### 3.7 `CREATE INDEX` / `DROP INDEX`
*   **Definition**: Creates a B-Tree or Bitmap lookup index over table columns to accelerate query search speed.
*   **Example**:
```sql
CREATE INDEX idx_emp_dept_salary ON employees (department_id, salary);
DROP INDEX idx_emp_dept_salary;
```

---

## 4. Data Control Language (DCL)

DCL commands manage user access, privileges, and database security roles.

### 4.1 `GRANT`
*   **Definition**: Bestows database permissions (SELECT, INSERT, UPDATE, DELETE, ALL) to users or roles.
*   **Syntax**: `GRANT privilege ON object TO user_or_role;`
*   **Example**:
```sql
GRANT SELECT, INSERT ON employees TO analyst_role;
GRANT ALL PRIVILEGES ON DATABASE analytics_db TO admin_user;
```

### 4.2 `REVOKE`
*   **Definition**: Removes previously assigned permissions from users or roles.
*   **Syntax**: `REVOKE privilege ON object FROM user_or_role;`
*   **Example**:
```sql
REVOKE INSERT ON employees FROM analyst_role;
```

---

## 5. Transaction Control Language (TCL)

TCL commands manage transactional integrity and ACID guarantees.

### 5.1 `COMMIT`
*   **Definition**: Permanently saves all changes made during the current transaction session to disk.
*   **Example**:
```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;
```

### 5.2 `ROLLBACK`
*   **Definition**: Undoes and reverts all uncommitted changes made in the current transaction.
*   **Example**:
```sql
BEGIN TRANSACTION;
DELETE FROM accounts WHERE account_id = 1;
-- Realize mistake, abort transaction:
ROLLBACK;
```

### 5.3 `SAVEPOINT` / `RELEASE SAVEPOINT`
*   **Definition**: Creates a checkpoint within a transaction allowing selective partial rollbacks.
*   **Example**:
```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
SAVEPOINT sp1;

UPDATE accounts SET balance = balance - 50000 WHERE account_id = 1; -- Error!
ROLLBACK TO SAVEPOINT sp1; -- Rollbacks only back to sp1

COMMIT; -- Commits the first -100 update
```

---

## 6. JOIN Types & Operations

JOINs combine columns from two or more tables based on matching key relationships.

```
       INNER JOIN                  LEFT JOIN                   RIGHT JOIN
    ┌───┐     ┌───┐             ┌───┬───┐                     ┌───┬───┐
    │   │ █ █ │   │             │ █ │ █ │   │                 │   │ █ │ █ │
    └───┘     └───┘             └───┴───┘                     └───┴───┘
```

### 6.1 `INNER JOIN`
*   **Definition**: Returns rows when matching keys exist in **both** tables.
*   **Example**:
```sql
SELECT e.first_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;
```

### 6.2 `LEFT (OUTER) JOIN`
*   **Definition**: Returns **all** rows from the left table, plus matched values from the right table (unmatched right columns return `NULL`).
*   **Example**:
```sql
SELECT e.first_name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id;
```

### 6.3 `RIGHT (OUTER) JOIN`
*   **Definition**: Returns **all** rows from the right table, plus matched values from the left table.
*   **Example**:
```sql
SELECT e.first_name, d.department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.department_id;
```

### 6.4 `FULL (OUTER) JOIN`
*   **Definition**: Returns all rows when there is a match in **either** left or right table.
*   **Example**:
```sql
SELECT e.first_name, d.department_name
FROM employees e
FULL JOIN departments d ON e.department_id = d.department_id;
```

### 6.5 `CROSS JOIN`
*   **Definition**: Computes Cartesian product of two tables (combines every row of Left table with every row of Right table).
*   **Example**:
```sql
SELECT p.product_name, s.store_name
FROM products p
CROSS JOIN stores s;
```

### 6.6 `SELF JOIN`
*   **Definition**: Joins a table to itself (used for hierarchical data).
*   **Example**:
```sql
SELECT e.first_name AS employee, m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

---

## 7. Set Operations

Set operations combine row results from two query statements.

### 7.1 `UNION` vs `UNION ALL`
*   **`UNION`**: Combines query result rows and removes duplicates (performs distinct sort).
*   **`UNION ALL`**: Combines query result rows keeping all duplicate entries (faster execution).
*   **Example**:
```sql
SELECT email FROM customer_contacts
UNION ALL
SELECT email FROM lead_contacts;
```

### 7.2 `INTERSECT`
*   **Definition**: Returns only rows present in **both** query result sets.
*   **Example**:
```sql
SELECT user_id FROM web_visitors
INTERSECT
SELECT user_id FROM mobile_app_users;
```

### 7.3 `EXCEPT` / `MINUS`
*   **Definition**: Returns rows from the first query that are **not** present in the second query.
*   **Example**:
```sql
SELECT customer_id FROM active_subscribers
EXCEPT
SELECT customer_id FROM churned_users;
```

---

## 8. Advanced Window Functions & CTEs

Window functions perform calculations across a subset of table rows related to the current row without collapsing rows into a single summary output.

### 8.1 Common Table Expressions (CTEs - `WITH`)
*   **Definition**: Defines a temporary named result set for query modularity.
*   **Example**:
```sql
WITH HighSalaryDepts AS (
    SELECT department_id, AVG(salary) as avg_sal
    FROM employees
    GROUP BY department_id
    HAVING AVG(salary) > 80000
)
SELECT e.first_name, e.salary, h.avg_sal
FROM employees e
JOIN HighSalaryDepts h ON e.department_id = h.department_id;
```

### 8.2 `WITH RECURSIVE`
*   **Definition**: Iteratively evaluates hierarchical datasets (e.g., organizational charts).
*   **Example**:
```sql
WITH RECURSIVE OrgChart AS (
    SELECT employee_id, manager_id, first_name, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.first_name, o.level + 1
    FROM employees e
    JOIN OrgChart o ON e.manager_id = o.employee_id
)
SELECT * FROM OrgChart;
```

### 8.3 Ranking Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`)
*   **Example**:
```sql
SELECT 
    employee_id, department_id, salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as row_num,
    RANK()       OVER (PARTITION BY department_id ORDER BY salary DESC) as rnk,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as dense_rnk
FROM employees;
```

### 8.4 Value Window Functions (`LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`)
*   **Example**:
```sql
SELECT 
    order_date, amount,
    LAG(amount, 1)  OVER (ORDER BY order_date) as prev_day_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) as next_day_amount,
    FIRST_VALUE(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as initial_amount
FROM sales;
```

### 8.5 `QUALIFY`
*   **Definition**: Filters the results of Window Functions directly without wrapping inside subqueries.
*   **Example (Snowflake / BigQuery)**:
```sql
SELECT employee_id, department_id, salary
FROM employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) = 1;
```

### 8.6 Multi-Level Aggregations (`GROUPING SETS`, `ROLLUP`, `CUBE`)
*   **Example**:
```sql
SELECT year, region, SUM(sales) AS total_sales
FROM annual_sales
GROUP BY ROLLUP(year, region);
```

---

## 9. Conditional & Built-in Functions

### 9.1 `CASE WHEN`
*   **Definition**: Evaluates conditional logic and returns scalar values.
*   **Example**:
```sql
SELECT first_name, salary,
       CASE 
           WHEN salary >= 100000 THEN 'Executive'
           WHEN salary >= 60000 THEN 'Mid-Level'
           ELSE 'Entry-Level'
       END AS salary_tier
FROM employees;
```

### 9.2 `COALESCE()` and `NULLIF()`
*   **`COALESCE(v1, v2, ...)`**: Returns first non-NULL argument.
*   **`NULLIF(v1, v2)`**: Returns NULL if $v1 = v2$.
*   **Example**:
```sql
SELECT 
    COALESCE(phone, mobile, 'N/A') AS primary_contact,
    total_sales / NULLIF(total_orders, 0) AS avg_order_value
FROM store_stats;
```

### 9.3 String Functions
```sql
SELECT 
    CONCAT(first_name, ' ', last_name) AS full_name,
    SUBSTRING(email FROM 1 FOR 5) AS email_prefix,
    LENGTH(first_name) AS name_len,
    UPPER(first_name) AS upper_name,
    LOWER(email) AS lower_email,
    TRIM(both ' ' FROM comment) AS clean_comment,
    REPLACE(phone, '-', '') AS clean_phone
FROM customers;
```

### 9.4 Date Functions
```sql
SELECT 
    CURRENT_DATE AS today,
    CURRENT_TIMESTAMP AS now_ts,
    DATE_TRUNC('month', order_date) AS month_start,
    EXTRACT(YEAR FROM order_date) AS order_year,
    DATEDIFF('day', order_date, delivery_date) AS shipping_days
FROM orders;
```

---

## 10. Database Constraints & Schema Rules

Constraints enforce data validity and referential integrity rules.

### 10.1 Primary Key & Foreign Key
*   **Primary Key**: Uniquely identifies each row; cannot contain NULLs.
*   **Foreign Key**: Enforces referential integrity between tables (`ON DELETE CASCADE`).
*   **Example**:
```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    CONSTRAINT fk_customer 
      FOREIGN KEY (customer_id) 
      REFERENCES customers(customer_id) 
      ON DELETE CASCADE
);
```

### 10.2 `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`
*   **Example**:
```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    price NUMERIC(10,2) CHECK (price >= 0),
    status VARCHAR(20) DEFAULT 'ACTIVE'
);
```
