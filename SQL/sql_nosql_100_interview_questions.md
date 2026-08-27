# SQL & NoSQL 100 Interview Questions & Answers

This document contains 100 essential interview questions and answers on SQL databases, NoSQL architectures, query optimizations, and database design.

---

## 📋 Table of Contents
*   [Relational Databases & SQL Syntax (Q1 - Q40)](#relational-databases--sql-syntax-q1---q40)
*   [Normalization, Indexing & Transactions (Q41 - Q70)](#normalization-indexing--transactions-q41---q70)
*   [NoSQL Architectures & distributed Systems (Q71 - Q100)](#nosql-architectures--distributed-systems-q71---q100)

---

## Relational Databases & SQL Syntax (Q1 - Q40)

#### Q1: What is a Relational Database Management System (RDBMS)?
**Answer:** A database management system based on the relational model introduced by E.F. Codd, where data is represented as tables (relations) with relationships defined between them.

#### Q2: What is SQL?
**Answer:** Structured Query Language. It is the standard programming language used to manage, query, and manipulate data stored in relational databases.

#### Q3: What is the difference between DDL, DML, DCL, and TCL?
**Answer:**
*   **DDL (Data Definition Language)**: Defines database structures (e.g., `CREATE`, `ALTER`, `DROP`).
*   **DML (Data Manipulation Language)**: Manipulates data values (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`).
*   **DCL (Data Control Language)**: Manages permissions and access controls (e.g., `GRANT`, `REVOKE`).
*   **TCL (Transaction Control Language)**: Manages transactions (e.g., `COMMIT`, `ROLLBACK`, `SAVEPOINT`).

#### Q4: What is a Primary Key?
**Answer:** A column (or set of columns) that uniquely identifies each row in a table. Primary keys must contain unique, non-null values.

#### Q5: What is a Foreign Key?
**Answer:** A column (or set of columns) in one table that references the primary key of another table, enforcing referential integrity between them.

#### Q6: What is the difference between `UNIQUE` and `PRIMARY KEY` constraints?
**Answer:** A table can have only one `PRIMARY KEY`, which cannot contain `NULL` values. A table can have multiple `UNIQUE` constraints, and they can accept `NULL` values.

#### Q7: Explain the difference between `WHERE` and `HAVING` clauses.
**Answer:** 
*   `WHERE`: Filters rows before grouping operations are applied.
*   `HAVING`: Filters grouped data returned by a `GROUP BY` clause.

#### Q8: What does the `GROUP BY` clause do?
**Answer:** Groups rows that have identical values in specified columns into summary rows, typically used with aggregate functions (like `COUNT`, `SUM`, `AVG`).

#### Q9: What is a SQL Join?
**Answer:** An operation used to combine rows from two or more tables based on a related column between them.

#### Q10: Explain the difference between `INNER JOIN` and `LEFT JOIN`.
**Answer:** 
*   `INNER JOIN`: Returns only the rows that have matching values in both tables.
*   `LEFT JOIN`: Returns all rows from the left table, plus any matching rows from the right table. If no match exists, it returns NULL values for the columns of the right table.

#### Q11: What is a `CROSS JOIN`?
**Answer:** A join that returns the Cartesian product of the two tables, pairing every row of the first table with every row of the second table.

#### Q12: What is a Self-Join?
**Answer:** A join operation where a table is joined with itself, typically used to query hierarchical relationships stored within a single table.

#### Q13: What is a subquery, and where can it be used?
**Answer:** A query nested inside another query (e.g., inside `SELECT`, `FROM`, `WHERE`, or `HAVING` clauses).

#### Q14: What is the difference between a correlated and an uncorrelated subquery?
**Answer:**
*   **Uncorrelated**: Can be executed independently of the outer query. It runs once and passes its results to the outer query.
*   **Correlated**: References columns from the outer query, meaning it must be executed repeatedly for each row evaluated by the outer query.

#### Q15: What is a Common Table Expression (CTE)?
**Answer:** A temporary named result set defined within the scope of a single query using the `WITH` clause, used to simplify complex nested subqueries.

#### Q16: What is a Recursive CTE?
**Answer:** A CTE that references itself, commonly used to traverse hierarchical or tree-structured datasets (e.g., organizational charts or file systems).

#### Q17: What are Window Functions?
**Answer:** Functions that perform calculations across a set of table rows related to the current row (using the `OVER` clause) without collapsing those rows into a single summary row.

#### Q18: Explain the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`.
**Answer:**
*   `ROW_NUMBER()`: Assigns a unique sequential integer starting at 1.
*   `RANK()`: Assigns sequential integers but leaves gaps if duplicate values exist (e.g., 1, 2, 2, 4).
*   `DENSE_RANK()`: Assigns sequential integers without leaving gaps for duplicates (e.g., 1, 2, 2, 3).

#### Q19: What do the `LEAD()` and `LAG()` window functions do?
**Answer:**
*   `LAG()`: Fetches the value of a column from a previous row in the partition.
*   `LEAD()`: Fetches the value of a column from a subsequent row in the partition.

#### Q20: What is the difference between `UNION` and `UNION ALL`?
**Answer:** 
*   `UNION`: Combines the result sets of two queries and removes duplicate rows.
*   `UNION ALL`: Combines result sets and retains duplicate rows, making it faster because it avoids sorting the data.

#### Q21: What is a View in SQL?
**Answer:** A virtual table whose contents are defined by a pre-saved query. It does not store data itself but displays data fetched from the underlying base tables.

#### Q22: What is a Materialized View?
**Answer:** A view that physically stores the results of its query on disk, improving read performance for complex queries. It must be refreshed periodically to capture updates to the base tables.

#### Q23: What are the differences between `DELETE`, `TRUNCATE`, and `DROP`?
**Answer:**
*   `DELETE` (DML): Removes specified rows from a table using a `WHERE` clause. It is logged, can be rolled back, and triggers database triggers.
*   `TRUNCATE` (DDL): Removes all rows from a table quickly by deallocating its storage pages. It cannot be filtered with a `WHERE` clause, is minimally logged, and cannot trigger triggers.
*   `DROP` (DDL): Deletes the entire table structure, indexes, and constraints from the database catalog.

#### Q24: What is a Database Cursor?
**Answer:** A control structure that allows you to traverse and process the rows of a query result set one by one, rather than all at once.

#### Q25: Why are cursor operations generally discouraged in high-performance applications?
**Answer:** Cursors process data sequentially (row-by-row), which is slow and memory-intensive. It is better to use set-based SQL operations, which can be optimized and parallelized by the query planner.

#### Q26: Explain the `COALESCE()` function.
**Answer:** Evaluates its arguments in order and returns the first non-null value it encounters.

#### Q27: What is the difference between `NULL` and an empty string or zero?
**Answer:** `NULL` represents the absence of a value or an unknown value, whereas an empty string `""` or zero `0` are defined, known values.

#### Q28: How do you handle pattern matching in SQL?
**Answer:** Using the `LIKE` operator with wildcard characters: `%` (matches any sequence of characters) and `_` (matches any single character).

#### Q29: What is referential integrity?
**Answer:** A database rule enforcing that relationships between tables remain consistent. It ensures that foreign key values must point to a valid, existing primary key in the referenced table.

#### Q30: What is the purpose of `ON DELETE CASCADE`?
**Answer:** A referential action that automatically deletes child rows in a table when their referenced parent row is deleted.

#### Q31: What is a Database Trigger?
**Answer:** A named block of code that automatically executes (fires) in response to a specific event (like `INSERT`, `UPDATE`, or `DELETE`) on a table.

#### Q32: What is a Stored Procedure?
**Answer:** A collection of pre-compiled SQL statements and control logic stored in the database catalog that can be executed on demand using arguments.

#### Q33: What is the difference between a Stored Procedure and a User-Defined Function (UDF)?
**Answer:** Procedures can modify database state, execute DDL, and return multiple output parameters (or none). Functions cannot modify database state, must return a single value or table, and can be used directly inside `SELECT` statements.

#### Q34: Explain the `EXISTS` operator.
**Answer:** A boolean operator used in a `WHERE` clause that returns `True` if a subquery returns one or more rows, stopping evaluation as soon as a match is found.

#### Q35: What is the difference between `IN` and `EXISTS`?
**Answer:** 
*   `IN`: Evaluates the entire subquery result set before filtering.
*   `EXISTS`: Evaluates rows one by one and exits early as soon as a match is found, making it faster for large datasets.

#### Q36: What is a composite key?
**Answer:** A primary key or candidate key composed of two or more columns combined to uniquely identify each row in a table.

#### Q37: What is a surrogate key?
**Answer:** An artificially generated unique identifier (e.g., an auto-incrementing integer or UUID) assigned to a table, serving no business meaning but acting as a primary key.

#### Q38: Explain the `CASE` statement in SQL.
**Answer:** A conditional control structure that evaluates conditions and returns a value when a condition is met (similar to if-else logic):
```sql
CASE WHEN salary > 100000 THEN 'High' ELSE 'Low' END
```

#### Q39: What is the difference between `CHAR` and `VARCHAR` data types?
**Answer:** 
*   `CHAR`: Fixed-length string. If the stored string is shorter than the defined limit, it is padded with spaces.
*   `VARCHAR`: Variable-length string. It consumes only the storage space needed for the characters actually stored, plus a length prefix.

#### Q40: What does the `MERGE` statement do?
**Answer:** Performs insert, update, or delete operations on a target table based on the results of a join with a source table (often called an "upsert").

---

## Normalization, Indexing & Transactions (Q41 - Q70)

#### Q41: What is Database Normalization?
**Answer:** The process of structuring a relational database schema to reduce data redundancy and eliminate update, insertion, and deletion anomalies.

#### Q42: What is Denormalization, and when would you use it?
**Answer:** The process of intentionally adding redundant data to a database schema to speed up complex query read times by avoiding resource-heavy joins.

#### Q43: What is a database anomaly?
**Answer:** A data inconsistency that can occur in poorly structured databases. Types include:
*   *Insertion Anomaly*: Inability to add data because some attributes are missing.
*   *Delete Anomaly*: Unintended loss of unrelated data when deleting a record.
*   *Update Anomaly*: Inconsistencies that occur when duplicate copies of the same data are not all updated simultaneously.

#### Q44: What is 1NF (First Normal Form)?
**Answer:** A table structure where all attribute columns contain only atomic (indivisible) values, and there are no repeating groups or nested arrays.

#### Q45: What is 2NF (Second Normal Form)?
**Answer:** A table in 1NF where every non-key column is fully functionally dependent on the primary key, removing partial dependencies (which can occur with composite keys).

#### Q46: What is 3NF (Third Normal Form)?
**Answer:** A table in 2NF where no non-key columns have transitive dependencies on the primary key (i.e., non-key attributes should only depend on key attributes).

#### Q47: What is Boyce-Codd Normal Form (BCNF)?
**Answer:** A stricter version of 3NF where for every functional dependency $X \rightarrow Y$, the determinant $X$ must be a super key of the table.

#### Q48: What is a Database Index?
**Answer:** A database search structure created to speed up data retrieval times at the cost of additional storage space and slower write operations.

#### Q49: Explain Clustered vs. Non-Clustered Indexes.
**Answer:**
*   **Clustered Index**: Determines the physical order of data rows on disk. A table can have only one clustered index (typically the Primary Key).
*   **Non-Clustered Index**: Stores index values alongside pointers to the physical data pages where the actual rows reside. A table can have multiple non-clustered indexes.

#### Q50: How does a B-Tree index work?
**Answer:** A self-balancing search tree structure that keeps data sorted and allows search, sequential access, insertion, and deletion operations in logarithmic time ($O(\log N)$).

#### Q51: How does a Hash index work?
**Answer:** Uses a hash function to map index keys to bucket pointers. It is highly performant ($O(1)$) for exact match equality comparisons but does not support range scans or sorting.

#### Q52: What is a composite index?
**Answer:** An index created on multiple columns of a table, useful for queries that filter on all those columns together.

#### Q53: Explain the "leftmost prefix rule" in composite indexes.
**Answer:** A composite index on columns `(A, B, C)` can speed up queries filtering on `(A)`, `(A, B)`, or `(A, B, C)`, but cannot be used for queries filtering only on `(B)` or `(C)` because search keys must match the index columns from left to right.

#### Q54: What is a covering index?
**Answer:** An index that contains all the columns referenced by a query, allowing the database to return the results directly from the index without having to look up the data rows.

#### Q55: What does the term "ACID" stand for?
**Answer:** Atomicity, Consistency, Isolation, and Durability. These properties guarantee that database transactions are executed reliably.

#### Q56: What is Atomicity in database transactions?
**Answer:** The guarantee that a transaction is treated as a single, indivisible unit of work: either all its modifications are committed, or the entire transaction is aborted and rolled back.

#### Q57: What is Consistency in database transactions?
**Answer:** The guarantee that a transaction will transition the database from one valid state to another, maintaining all schema rules, constraints, and triggers.

#### Q58: What is Isolation in database transactions?
**Answer:** The guarantee that concurrent execution of transactions results in the same database state as if they were run sequentially.

#### Q59: What is Durability in database transactions?
**Answer:** The guarantee that once a transaction is committed, its modifications are permanently recorded in non-volatile storage and will survive subsequent system failures.

#### Q60: What are the four default Transaction Isolation Levels?
**Answer:** In order of increasing isolation: `Read Uncommitted`, `Read Committed`, `Repeatable Read`, and `Serializable`.

#### Q61: What is a Dirty Read?
**Answer:** A concurrency issue where Transaction A reads data modified by Transaction B before Transaction B has committed those changes. If Transaction B rolls back, the data read by Transaction A becomes invalid.

#### Q62: What is a Non-Repeatable Read?
**Answer:** A concurrency issue where Transaction A reads a row value, Transaction B modifies or deletes that row and commits, and Transaction A reads the same row again to find a different value.

#### Q63: What is a Phantom Read?
**Answer:** A concurrency issue where Transaction A runs a query filtering rows, Transaction B inserts new rows matching that filter and commits, and Transaction A runs the query again to find new "phantom" rows.

#### Q64: Explain the `Read Committed` isolation level.
**Answer:** Prevents dirty reads. Transactions can only read committed changes, but non-repeatable and phantom reads can still occur.

#### Q65: Explain the `Repeatable Read` isolation level.
**Answer:** Prevents dirty and non-repeatable reads. Rows read by a transaction cannot be modified by other transactions until the transaction completes, but phantom reads can still occur.

#### Q66: Explain the `Serializable` isolation level.
**Answer:** The highest isolation level. It prevents all concurrency anomalies by enforcing strict locking or execution order, making transactions behave as if they were run sequentially, which can significantly reduce throughput.

#### Q67: What is Write-Ahead Logging (WAL)?
**Answer:** A transaction logging technique where changes are written to a secure log on disk before they are applied to the database pages, ensuring durability and recovery support.

#### Q68: Explain the difference between Shared (S) and Exclusive (X) locks.
**Answer:**
*   **Shared Lock (Read Lock)**: Allows multiple transactions to read a resource simultaneously but prevents them from modifying it.
*   **Exclusive Lock (Write Lock)**: Allows only a single transaction to read and modify a resource, blocking all other transactions.

#### Q69: What is a Deadlock in databases?
**Answer:** A concurrency block where Transaction A holds a lock on Resource 1 and waits for Resource 2, while Transaction B holds a lock on Resource 2 and waits for Resource 1. Neither can proceed.

#### Q70: How do databases resolve deadlocks?
**Answer:** The database engine's deadlock detector identifies lock wait cycles, aborts one of the blocking transactions (the victim), rolls back its changes, and allows the other transaction to complete.

---

## NoSQL Architectures & distributed Systems (Q71 - Q100)

#### Q71: What does "NoSQL" stand for?
**Answer:** "Not Only SQL". It represents a class of non-relational database management systems that support flexible schemas and scale horizontally.

#### Q72: What are the main limitations of traditional SQL databases at scale?
**Answer:** Scaling traditional relational databases horizontally (across multiple servers) is difficult because maintaining ACID compliance and joins across a network causes significant latency. They are typically scaled vertically (by adding more CPU/RAM to a single server).

#### Q73: What are Key-Value stores?
**Answer:** High-performance databases (like Redis or Memcached) that store data as simple key-value pairings, optimized for caching and session management.

#### Q74: What are Document Databases?
**Answer:** Databases (like MongoDB) that store data as self-contained documents (often JSON or BSON format), allowing for nested structures and flexible schemas.

#### Q75: What are Wide-Column (Column-Family) stores?
**Answer:** Databases (like Cassandra or HBase) that store data in column families rather than rows, allowing for fast queries on sparse datasets with billions of rows.

#### Q76: What are Graph Databases?
**Answer:** Databases (like Neo4j) that store data as nodes (entities) and edges (relationships), optimized for traversing complex networks.

#### Q77: Explain the BASE properties of NoSQL databases.
**Answer:** 
*   **Basically Available**: The system remains operational during failures.
*   **Soft State**: The database state can drift over time without user interaction due to background replication.
*   **Eventual Consistency**: Replicas will synchronize and become consistent over time if no new writes are made.

#### Q78: State the CAP Theorem.
**Answer:** A distributed systems principle stating that a system can simultaneously provide at most two of the following three guarantees: Consistency, Availability, and Partition Tolerance.

#### Q79: Why is Partition Tolerance (P) mandatory in distributed systems?
**Answer:** Physical networks will inevitably experience packet loss or disconnected nodes (partitions). Therefore, distributed databases must be designed to handle partitions.

#### Q80: What is the difference between a CP and an AP database under the CAP Theorem?
**Answer:**
*   **CP (Consistency/Partition Tolerance)**: During a partition, the database rejects writes or blocks reads to ensure data remains consistent across all nodes.
*   **AP (Availability/Partition Tolerance)**: During a partition, all nodes remain open to accept reads and writes, returning the local data version even if it is stale.

#### Q81: What is Eventual Consistency?
**Answer:** A consistency model where replicas can temporarily return stale data, but they will eventually synchronize and display identical data once updates stop.

#### Q82: What is Strong Consistency?
**Answer:** A consistency model guaranteeing that a read operation will always return the value of the most recent write, regardless of which node is queried.

#### Q83: Explain the concept of "Sharding".
**Answer:** A database partitioning technique that splits a dataset into smaller, independent parts (shards) and distributes them across multiple physical servers to scale horizontally.

#### Q84: What is a shard key?
**Answer:** The field used to determine which database shard stores a specific write or read operation (e.g., partitioning users by country code).

#### Q85: What is Consistent Hashing?
**Answer:** An algorithmic mapping technique used in distributed hash tables to minimize data re-distribution when storage nodes are added or removed.

#### Q86: Explain the difference between master-slave replication and master-master replication.
**Answer:**
*   **Master-Slave**: Writes are accepted by a single primary master node and replicated to read-only slave nodes.
*   **Master-Master**: Multiple nodes can accept read and write operations, requiring a conflict resolution strategy to merge concurrent changes.

#### Q87: What is split-brain scenario in clustered databases?
**Answer:** A failure state where a network partition splits a cluster into two disconnected halves, and each half elects a primary master node, leading to conflicting data modifications.

#### Q88: How do clusters prevent split-brain issues?
**Answer:** Quorum rules. A sub-cluster must contain a strict majority of nodes (e.g., more than 50% of the total nodes) to elect a master node and accept writes.

#### Q89: What is a Read/Write Split architecture?
**Answer:** Directing all write transactions to a primary master database node while routing read queries to secondary replica nodes to scale read throughput.

#### Q90: Explain replication lag.
**Answer:** The time delay between a write operation being committed on the primary master node and that change being applied on a secondary replica node.

#### Q91: What is a hot spot in database sharding?
**Answer:** An uneven distribution of read/write loads where a single shard receives the majority of traffic (e.g., sharding by date, causing the shard for the current date to get overloaded).

#### Q92: What are graph database edges and nodes?
**Answer:**
*   **Nodes**: Represent objects or entities (e.g., User, Product).
*   **Edges**: Represent relationships between nodes (e.g., "Follows", "Purchased"), containing direction and properties.

#### Q93: Explain the difference between SQL and NoSQL database scaling.
**Answer:** Relational databases scale **vertically** (adding CPU/RAM to a single server). NoSQL databases scale **horizontally** (distributing data across a cluster of low-cost commodity servers).

#### Q94: What is the purpose of Redis TTL (Time-To-Live)?
**Answer:** A key setting that defines an expiration time in seconds, after which Redis automatically deletes the key to free memory.

#### Q95: What is Cassandra's gossip protocol?
**Answer:** A peer-to-peer communication protocol where nodes in a cluster periodically share state and topology information to detect node failures.

#### Q96: What is a tombstone in NoSQL databases?
**Answer:** A temporary marker written to record a deletion operation in log-structured storage engines (like Cassandra), which is cleaned up later during database compaction.

#### Q97: Explain MongoDB's BSON format.
**Answer:** Binary JSON. A serialization format used to store documents in MongoDB, adding support for extra data types (like Date and Binary) not supported by standard JSON.

#### Q98: What is a columnar database (e.g., ClickHouse)?
**Answer:** A database optimized for analytics that stores data columns together on disk rather than row records, which significantly speeds up aggregation calculations.

#### Q99: What is Polyglot Persistence?
**Answer:** The architectural practice of using different database engines (e.g., using Postgres for orders, Redis for caching, and Elasticsearch for catalog search) in a single application stack to leverage their specific strengths.

#### Q100: How do you identify slow-running queries in a database?
**Answer:** By enabling the slow query log, analyzing execution plans using the `EXPLAIN` statement, and monitoring database metrics for long-running transactions.
