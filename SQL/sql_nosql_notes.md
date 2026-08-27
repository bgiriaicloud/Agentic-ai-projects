# SQL & NoSQL Comprehensive Reference Notes

This document covers relational database management systems (RDBMS) and non-relational (NoSQL) database architectures, normalization rules, ACID vs. BASE properties, CAP theorem, indexing, and clustering.

---

## 📋 Table of Contents
*   [Relational Databases (SQL) Foundations](#relational-databases-sql-foundations)
*   [Non-Relational Databases (NoSQL) Foundations](#non-relational-databases-nosql-foundations)
*   [ACID vs. BASE Transactions](#acid-vs-base-transactions)
*   [The CAP Theorem](#the-cap-theorem)
*   [Indexing Strategies (B-Tree vs. Hash)](#indexing-strategies-b-tree-vs-hash)

---

## Relational Databases (SQL) Foundations

Relational databases store data in structured tables consisting of rows (tuples) and columns (attributes). They are based on set theory and relational algebra.

### Normalization Forms
Normalization is the process of organizing data to reduce redundancy and prevent update anomalies.
1.  **First Normal Form (1NF)**: All attributes must contain atomic (indivisible) values. There must be no repeating groups.
2.  **Second Normal Form (2NF)**: Must be in 1NF, and all non-key attributes must be fully functionally dependent on the entire primary key (removes partial dependencies in composite keys).
3.  **Third Normal Form (3NF)**: Must be in 2NF, and no non-key attribute can be transitively dependent on the primary key (removes transitive dependencies).
4.  **Boyce-Codd Normal Form (BCNF)**: A stronger version of 3NF where for every functional dependency $X \rightarrow Y$, $X$ must be a super key.

### Core SQL Joins
*   **INNER JOIN**: Returns records that have matching values in both tables.
*   **LEFT (OUTER) JOIN**: Returns all records from the left table and the matching records from the right table. If no match, returns NULL values for the right table.
*   **RIGHT (OUTER) JOIN**: Returns all records from the right table and the matching records from the left table.
*   **FULL (OUTER) JOIN**: Returns all records when there is a match in either left or right table.
*   **CROSS JOIN**: Returns the Cartesian product of the two tables (every row of the first table paired with every row of the second table).

---

## Non-Relational Databases (NoSQL) Foundations

NoSQL databases are non-tabular and support schema-less data structures, optimized for high write loads, horizontal scaling, and unstructured data.

### Main NoSQL Categories
1.  **Document Databases**: Store data as documents (JSON, BSON, XML). Examples: *MongoDB*, *CouchDB*. Optimized for nested data structures.
2.  **Key-Value Stores**: Store data as simple key-value pairings. Examples: *Redis*, *DynamoDB*, *Memcached*. Highly performant for caching and session management.
3.  **Column-Family (Wide-Column) Stores**: Store data in columns grouped into families, optimized for query performance on sparse datasets. Examples: *Cassandra*, *HBase*, *Bigtable*.
4.  **Graph Databases**: Store data as nodes (entities) and edges (relationships). Examples: *Neo4j*, *Amazon Neptune*. Optimized for path traversals and network analysis.

---

## ACID vs. BASE Transactions

### ACID Properties (Relational Databases)
ACID guarantees strict consistency and reliability in data transactions.
*   **Atomicity**: Transactions are executed as a single unit; either all operations succeed, or the entire transaction is rolled back.
*   **Consistency**: A transaction transitions the database from one valid state to another, maintaining all schema constraints and keys.
*   **Isolation**: Concurrent execution of transactions yields the same database state as if they were run sequentially.
*   **Durability**: Once a transaction is committed, its changes are permanently written to non-volatile storage and survive system crashes.

### BASE Properties (NoSQL Databases)
BASE relaxes strict consistency constraints to achieve high scalability and availability.
*   **Basically Available**: The system continues to function and respond to queries even during network partitions or node failures.
*   **Soft State**: The state of the data may change over time without user interaction due to background replication (consistency is not guaranteed immediately).
*   **Eventual Consistency**: The system guarantees that if no new updates are made, all replicas will eventually synchronize and display identical data.

---

## The CAP Theorem

Proposed by Eric Brewer, the CAP Theorem states that a distributed data system can simultaneously provide at most two of the following three guarantees:

```
                  Consistency
                     /   \
                    /     \
                   /  CAP  \
                  /         \
         Availability ---- Partition Tolerance
```

1.  **Consistency (C)**: Every read receives the most recent write or an error.
2.  **Availability (A)**: Every non-failing node returns a non-error response (without guarantee that it contains the most recent write).
3.  **Partition Tolerance (P)**: The system continues to operate despite arbitrary message loss or network partitions.

> [!IMPORTANT]
> Since network partitions (P) are inevitable in distributed systems, a NoSQL database must choose between **Consistency (CP)** (blocking writes/reads to prevent stale data) or **Availability (AP)** (returning stale data from partitioned nodes).

---

## Indexing Strategies (B-Tree vs. Hash)

Indexes are data structures used to speed up query retrieval times at the cost of slower write speeds and increased storage consumption.

### B-Tree Indexes
*   **Structure**: Self-balancing search trees where nodes contain sorted keys and child pointers.
*   **Usage**: The default index type in relational databases. Highly efficient for range queries (`WHERE age BETWEEN 20 AND 30`), sorting (`ORDER BY`), and exact match queries.
*   **Time Complexity**: $O(\log N)$ for search, insertion, and deletion.

### Hash Indexes
*   **Structure**: A key-value lookup table that maps keys to bucket addresses using a hash function.
*   **Usage**: Optimized for exact match equality comparisons (`WHERE id = 5`).
*   **Limits**: Cannot be used for range scans, partial key matches, or sorting operations.
*   **Time Complexity**: $O(1)$ constant time for exact match lookups.
