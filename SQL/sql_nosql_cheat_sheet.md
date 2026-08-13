# SQL & NoSQL Command Cheat Sheet

This document compiles essential SQL queries, advanced window functions, common CTE structures, MongoDB document query syntax, and Redis key-value store commands.

---

## 📋 Table of Contents
1.  [Relational SQL Queries (DML/DDL)](#1-relational-sql-queries-dmlddl)
2.  [Advanced SQL (Window Functions & CTEs)](#2-advanced-sql-window-functions--ctes)
3.  [MongoDB Document Query Syntax](#3-mongodb-document-query-syntax)
4.  [Redis Key-Value Commands](#4-redis-key-value-commands)

---

## 1. Relational SQL Queries (DML/DDL)

### Standard Selection & Aggregation
```sql
SELECT department_id, COUNT(*) AS employee_count, AVG(salary) AS avg_salary
FROM employees
WHERE hire_date >= '2023-01-01'
GROUP BY department_id
HAVING AVG(salary) > 60000
ORDER BY avg_salary DESC;
```

### Table Definitions & Indexing
```sql
-- Create a new relational table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a B-Tree index for performance optimizations
CREATE INDEX idx_users_email ON users(email);
```

---

## 2. Advanced SQL (Window Functions & CTEs)

### Common Table Expressions (CTEs)
CTEs improve the readability of complex queries by defining temporary result sets:
```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > 1000000
)
SELECT * FROM orders
WHERE region IN (SELECT region FROM top_regions);
```

### Window Functions
Perform calculations across a set of table rows related to the current row, without collapsing them into a single summary row.

#### ROW_NUMBER, RANK, and DENSE_RANK
*   `ROW_NUMBER()`: Assigns a unique sequential integer starting at 1.
*   `RANK()`: Assigns sequential integers but leaves gaps if duplicates exist.
*   `DENSE_RANK()`: Assigns sequential integers without gaps for duplicates.
```sql
SELECT employee_id, department_id, salary,
       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank_num,
       DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank_num
FROM employees;
```

#### LEAD and LAG
Access data from a subsequent or previous row without using a self-join:
```sql
SELECT employee_id, salary,
       LAG(salary, 1, 0) OVER (ORDER BY salary) AS prev_lower_salary,
       LEAD(salary, 1, 0) OVER (ORDER BY salary) AS next_higher_salary
FROM employees;
```

---

## 3. MongoDB Document Query Syntax

MongoDB stores records as BSON documents.

### CRUD Operations
```javascript
// Insert a document
db.users.insertOne({
  name: "Alice",
  age: 30,
  skills: ["Python", "SQL"],
  status: "active"
});

// Find documents with filters (equivalent to WHERE age > 25)
db.users.find({ age: { $gt: 25 }, status: "active" });

// Update documents (increment age, add skill)
db.users.updateOne(
  { name: "Alice" },
  { 
    $set: { status: "pending" },
    $inc: { age: 1 },
    $push: { skills: "Docker" }
  }
);

// Delete documents
db.users.deleteOne({ name: "Alice" });
```

### Aggregation Pipeline
MongoDB uses multi-stage aggregation pipelines to transform data:
```javascript
db.users.aggregate([
  // Stage 1: Filter active users
  { $match: { status: "active" } },
  // Stage 2: Group by status and calculate average age
  { 
    $group: { 
      _id: "$status", 
      avgAge: { $avg: "$age" },
      totalUsers: { $sum: 1 }
    } 
  },
  // Stage 3: Sort by average age descending
  { $sort: { avgAge: -1 } }
]);
```

---

## 4. Redis Key-Value Commands

Redis is an in-memory key-value data structure store used for caching and sessions.

### String Operations (Basic Key-Value)
```bash
# Set a key value
SET user:100:token "abc123xyz"

# Set a key with an expiration time in seconds (TTL)
SETEX user:100:session 3600 "active_session_data"

# Get a key value
GET user:100:token

# Increment an integer key atomically
INCR page:views
```

### Hash Operations (Object Mappings)
```bash
# Set multiple fields on a hash key
HSET user:100 name "Alice" email "alice@example.com" role "admin"

# Retrieve all fields and values from a hash key
HGETALL user:100

# Get a single field value from a hash key
HGET user:100 email
```

### List Operations (Queues / Stacks)
```bash
# Push elements to the left (head) of a list
LPUSH tasks "task_1"
LPUSH tasks "task_2"

# Pop elements from the right (tail) of a list (FIFO Queue behavior)
RPOP tasks
```
