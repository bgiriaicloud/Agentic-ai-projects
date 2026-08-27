# Data Engineer 250 Interview Questions & Answers - Part 3

This is Volume 3 of the Data Engineer Interview Guide, containing **Questions 171 to 250**. It covers Advanced SQL Query Optimization, Execution Plans, Window Functions, Data Governance, Security, Data Quality Frameworks, Feature Stores, Vector Databases, and Data FinOps.

---

## 📋 Table of Contents (Part 3)
7. [SQL Optimization, Indexing & Advanced Analytical Queries (Q171 - Q200)](#7-sql-optimization-indexing--advanced-analytical-queries-q171---q200)
8. [Data Governance, Data Quality & Security (Q201 - Q225)](#8-data-governance-data-quality--security-q201---q225)
9. [Advanced Data Engineering & Real-Time MLOps Pipelines (Q226 - Q250)](#9-advanced-data-engineering--real-time-mlops-pipelines-q226---q250)

---

## 7. SQL Optimization, Indexing & Advanced Analytical Queries (Q171 - Q200)

#### Q171: Explain SQL Window Functions and their core clause syntax (`OVER()`).
**Answer:** Functions that perform calculations across a set of table rows related to the current row without collapsing rows into a single summary output row (unlike `GROUP BY`).
```sql
FUNCTION_NAME() OVER (
    PARTITION BY column1 
    ORDER BY column2 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

#### Q172: Compare `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`.
**Answer:** For tied values (e.g., test scores 90, 90, 85):
*   `ROW_NUMBER()`: Assigns unique sequential integers regardless of ties (1, 2, 3).
*   `RANK()`: Assigns same rank to ties, skipping subsequent ranks (1, 1, 3).
*   `DENSE_RANK()`: Assigns same rank to ties without skipping subsequent ranks (1, 1, 2).

#### Q173: Explain `LEAD()` and `LAG()` Window Functions.
**Answer:**
*   `LAG(col, offset)`: Fetches a value from a row prior to the current row within the partition (e.g., calculating month-over-month sales growth).
*   `LEAD(col, offset)`: Fetches a value from a row subsequent to the current row within the partition.

#### Q174: Write a SQL query using Window Functions to find the Top 2 highest-earning employees per department.
**Answer:**
```sql
WITH RankedEmployees AS (
    SELECT 
        employee_id,
        department_id,
        salary,
        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank
    FROM employees
)
SELECT employee_id, department_id, salary
FROM RankedEmployees
WHERE rank <= 2;
```

#### Q175: What is a Common Table Expression (CTE), and when should you use it over subqueries?
**Answer:** A temporary named result set defined using the `WITH` clause that exists only within the execution scope of a single SQL statement. Improves query readability, modularity, and allows recursive self-referencing operations.

#### Q176: What is a Recursive CTE? Give an example use case.
**Answer:** A CTE that references itself to iteratively process hierarchical or graph data structures (e.g., organizational chart reporting hierarchies, bill of materials, category trees).
```sql
WITH RECURSIVE OrgChart AS (
    SELECT employee_id, manager_id, name, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, e.name, o.level + 1
    FROM employees e
    INNER JOIN OrgChart o ON e.manager_id = o.employee_id
)
SELECT * FROM OrgChart;
```

#### Q177: How do you analyze a SQL Query Execution Plan (`EXPLAIN ANALYZE`)?
**Answer:**
1.  Run `EXPLAIN ANALYZE <SQL_QUERY>`.
2.  Inspect operator tree from bottom to top.
3.  Look for expensive operators: Full Table Scans (`Seq Scan`), high-cost Nested Loop joins on unindexed large tables, heavy Disk Sorts, and disparity between estimated rows vs actual rows.

#### Q178: Compare Hash Join vs Nested Loop Join vs Sort-Merge Join.
**Answer:**
*   **Nested Loop Join**: Compares every row of table A against every row of table B. Fast for small tables; terrible $O(M \times N)$ performance for large tables without indexes.
*   **Hash Join**: Builds an in-memory hash table for the smaller table and probes it with the larger table. Fast for equi-joins ($O(M+N)$), but fails if hash table exceeds RAM.
*   **Sort-Merge Join**: Sorts both tables by join key first, then merges matching rows. Efficient for huge tables, especially when keys are already sorted on disk.

#### Q179: Explain B-Tree Index vs. Bitmap Index.
**Answer:**
*   **B-Tree Index**: Balanced tree index ideal for high-cardinality columns (e.g., primary keys, UUIDs, timestamps). Excellent for fast range searches and point lookups.
*   **Bitmap Index**: Stores bit arrays for distinct values. Highly efficient for low-cardinality columns (e.g., `gender`, `marital_status`) in read-heavy data warehouses, allowing fast boolean bitwise AND/OR filter execution.

#### Q180: What is a Composite Index, and what is the "Leftmost Prefix" rule?
**Answer:** An index created over multiple columns (e.g., `CREATE INDEX idx ON orders (country, order_date)`).
*   *Leftmost Prefix Rule*: The database query optimizer can use the composite index only if the query `WHERE` clause includes the leftmost column (`country`). Querying only by `order_date` bypasses the composite index.

#### Q181: Why can functions in `WHERE` clauses degrade query performance (Non-SARGable Queries)?
**Answer:** Applying functions to columns in a filter (e.g., `WHERE YEAR(order_date) = 2026` or `WHERE UPPER(email) = 'USER@MAIL.COM'`) prevents the database optimizer from using indexes (SARGable = Search Argument Able), forcing a full table scan.
*   *Fix*: Rewrite filter without column wrapping: `WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'`.

#### Q182: Write a SQL query to deduplicate data keeping only the latest record based on a timestamp.
**Answer:**
```sql
WITH Deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY updated_at DESC
        ) as rn
    FROM raw_users
)
SELECT * EXCEPT(rn)
FROM Deduplicated
WHERE rn = 1;
```

#### Q183: What is the difference between `UNION` and `UNION ALL`?
**Answer:**
*   `UNION`: Combines result sets from multiple queries and performs a distinct sort operation to eliminate duplicate rows (slower due to sorting overhead).
*   `UNION ALL`: Combines result sets keeping all duplicate rows without sorting (faster execution).

#### Q184: What is a Correlated Subquery, and why should it be avoided in large analytical queries?
**Answer:** A subquery that depends on values from the outer query for each row processed. It executes once for EVERY row in the outer query table, resulting in $O(N^2)$ execution latency. Convert correlated subqueries to explicit `JOIN`s or window functions instead.

#### Q185: Explain the `COALESCE()` and `NULLIF()` SQL functions.
**Answer:**
*   `COALESCE(val1, val2, ...)`: Returns the first non-NULL value in the argument list.
*   `NULLIF(val1, val2)`: Returns NULL if `val1 == val2`; otherwise returns `val1`. Useful for preventing division-by-zero errors (`total / NULLIF(count, 0)`).

#### Q186: Explain `GROUPING SETS`, `ROLLUP`, and `CUBE` in SQL aggregations.
**Answer:** Extensions to `GROUP BY` that compute multiple aggregate levels in a single query pass:
*   `GROUPING SETS`: Computes aggregations only for explicitly listed column combinations.
*   `ROLLUP(year, month, day)`: Computes hierarchical subtotals and grand totals (year+month+day, year+month, year, grand total).
*   `CUBE(a, b, c)`: Computes all possible $2^N$ permutation subtotals across specified columns.

#### Q187: Write a SQL query using `LAG()` to calculate Month-over-Month (MoM) revenue growth percentage.
**Answer:**
```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS sales_month,
        SUM(amount) AS current_month_revenue
    FROM sales
    GROUP BY 1
),
RevenueWithLag AS (
    SELECT 
        sales_month,
        current_month_revenue,
        LAG(current_month_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue
    FROM MonthlyRevenue
)
SELECT 
    sales_month,
    current_month_revenue,
    prev_month_revenue,
    ROUND(((current_month_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100, 2) AS mom_growth_pct
FROM RevenueWithLag;
```

#### Q188: What is Partition Pruning in database query engines?
**Answer:** An optimization technique where the query engine inspects table partition metadata and completely skips reading physical directories/files that fall outside the query's `WHERE` date/key boundaries.

#### Q189: Differentiate `HAVING` vs. `WHERE` clauses in SQL.
**Answer:**
*   `WHERE`: Filters individual raw data rows *before* aggregation takes place (cannot contain aggregate functions).
*   `HAVING`: Filters aggregated summary groups *after* `GROUP BY` execution (e.g., `HAVING SUM(amount) > 10000`).

#### Q190: What is Data Sharding?
**Answer:** Horizontally partitioning a massive database table across multiple independent physical database server nodes (shards), where each shard holds a subset of the total rows based on a shard key (e.g., `user_id % 10`).

#### Q191: Explain Database Deadlocks and how to prevent them.
**Answer:** A deadlock occurs when two concurrent transactions hold locks on resources that the other transaction needs to proceed, causing both transactions to block indefinitely.
*   *Prevention*: Access tables in the exact same sequential order across all transaction workflows, keep transaction execution times short, and use proper lock timeouts.

#### Q192: What is the `EXISTS` clause, and how does it compare to `IN`?
**Answer:**
*   `EXISTS`: Evaluates whether a subquery returns any rows. It short-circuits (stops scanning) as soon as the first matching row is found. Highly efficient for large subquery lookup tables.
*   `IN`: Evaluates the full subquery result list before filtering. Can perform poorly if subquery returns large datasets or contains NULL values.

#### Q193: What are Covering Indexes?
**Answer:** An index that includes all columns referenced in a SQL query (both SELECT, WHERE, and JOIN columns). Allows the database optimizer to satisfy the entire query directly from the index (Index-Only Scan) without accessing table data heap pages.

#### Q194: Write a SQL query using `COUNT(CASE WHEN ...)` to pivot categorical data.
**Answer:**
```sql
SELECT 
    department_id,
    COUNT(CASE WHEN status = 'ACTIVE' THEN 1 END) AS active_count,
    COUNT(CASE WHEN status = 'PENDING' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN status = 'TERMINATED' THEN 1 END) AS terminated_count
FROM employees
GROUP BY department_id;
```

#### Q195: Explain `QUALIFY` clause in modern cloud data warehouses.
**Answer:** A clause available in Snowflake, BigQuery, and Databricks that filters the results of Window Functions directly without wrapping the query inside a CTE or subquery:
```sql
SELECT employee_id, department_id, salary
FROM employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) = 1;
```

#### Q196: What is a Materialized View vs Standard View?
**Answer:**
*   **Standard View**: A saved SQL query template that executes from scratch every time it is referenced. Consumes compute resources on every run.
*   **Materialized View**: Stores the actual pre-computed physical query results on disk and periodically updates them, delivering near-instant query performance at the cost of storage space.

#### Q197: Explain Database Isolation Levels (ACID).
**Answer:** Controls transaction read phenomenon visibility (Dirty Reads, Non-repeatable Reads, Phantom Reads):
1.  **Read Uncommitted**: Lowest isolation, allows dirty reads.
2.  **Read Committed**: Prevents dirty reads; default in Postgres/SQL Server.
3.  **Repeatable Read**: Prevents dirty and non-repeatable reads.
4.  **Serializable**: Highest isolation; transactions execute strictly in sequence.

#### Q198: What is Optimistic Concurrency Control (OCC)?
**Answer:** A concurrency method used in Data Lakehouses (Delta Lake, Iceberg) that assumes multiple transactions can complete without affecting each other. Transactions record state changes without locking tables; at commit time, if a conflict is detected, the transaction retries automatically.

#### Q199: Write a SQL query to calculate running total of sales by date.
**Answer:**
```sql
SELECT 
    order_date,
    daily_amount,
    SUM(daily_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_sales
FROM daily_sales;
```

#### Q200: What is Query Spill to Disk in Analytical Engine execution?
**Answer:** Occurs when an intermediate execution operation (large hash join, sorting, aggregation) exceeds assigned executor RAM, forcing Spark or Snowflake to write temporary intermediate spill blocks to local disk SSDs, causing significant query performance degradation.

---

## 8. Data Governance, Data Quality & Security (Q201 - Q225)

#### Q201: What is Data Quality, and what are its 6 core dimensions?
**Answer:** The measure of data fitness for business decisions.
1.  **Accuracy**: Data correctly reflects real-world entities.
2.  **Completeness**: No missing or unexpected null fields.
3.  **Consistency**: Uniform data values across systems.
4.  **Timeliness**: Data is available when expected (SLA).
5.  **Uniqueness**: No duplicate records.
6.  **Validity**: Data conforms to syntax, format, and domain rules.

#### Q202: What is Great Expectations (GX)?
**Answer:** An open-source Python framework for asserting, documenting, and auditing data quality in pipelines through declarative test assertions called **Expectations** (e.g., `expect_column_values_to_not_be_null()`).

#### Q203: Explain Data Lineage and why it is critical for enterprise governance.
**Answer:** The visual tracking of data flow from origin ingestion sources to downstream tables and dashboards. Crucial for impact analysis (evaluating upstream changes before deployment), root-cause debugging, and regulatory compliance auditing.

#### Q204: What is OpenLineage?
**Answer:** An open standard for data lineage collection that defines a unified specification to collect metadata events from orchestrators (Airflow), processing engines (Spark), and transformation tools (dbt) into metadata engines (Marquez, Atlan).

#### Q205: Explain PII (Personally Identifiable Information) and PHI (Protected Health Information).
**Answer:**
*   **PII**: Information that can directly or indirectly identify an individual (e.g., SSN, email, phone number, physical address).
*   **PHI**: Identifiable health data created or received by healthcare providers subject to HIPAA enforcement.

#### Q206: How do you implement Data Masking / Dynamic Data Masking?
**Answer:** A security feature in cloud databases (Snowflake, BigQuery) that obfuscates sensitive column values at query runtime based on the user's role:
*   *Example*: Admins see real SSN `123-45-6789`; analysts see masked string `XXX-XX-6789`.

#### Q207: Compare Role-Based Access Control (RBAC) vs Attribute-Based Access Control (ABAC).
**Answer:**
*   **RBAC**: Grants database permissions based on defined user roles (e.g., `ROLE_FINANCE_ANALYST` has access to `schema_finance`).
*   **ABAC**: Grants access dynamically based on attributes of the user, resource, and context (e.g., "Allow access if user department == resource tag AND region == US").

#### Q208: What is Row-Level Security (RLS)?
**Answer:** A security policy configured on a database table that restricts which rows a user can query based on their authorization credentials (e.g., a regional sales manager querying `orders` table can view only rows where `region = 'EMEA'`).

#### Q209: What is Column-Level Security (CLS)?
**Answer:** Restricting access to specific table columns based on security tags (e.g., non-HR users receive access denied when attempting to include `salary` or `ssn` columns in SELECT queries).

#### Q210: Explain Encryption at Rest vs Encryption in Transit.
**Answer:**
*   **At Rest**: Encrypting static files stored on disk/cloud object storage using symmetric algorithms (AES-256) with managed keys (KMS).
*   **In Transit**: Encrypting data streams traversing network connections between clients, servers, and services using TLS/SSL protocols.

#### Q211: What is Data Observability, and what are its 5 pillars?
**Answer:** The ability to understand, diagnose, and manage the health of data systems.
1.  **Freshness**: Is data up-to-date?
2.  **Distribution**: Are numerical distributions within expected bounds?
3.  **Volume**: Are row counts complete?
4.  **Schema**: Have table structure changes broken downstream consumers?
5.  **Lineage**: Who and what is impacted by data outages?

#### Q212: What is Data Anomaly Detection in Data Quality monitoring?
**Answer:** Using machine learning models to track pipeline telemetry metrics over time, automatically firing alerts when metric metrics deviate from historical baselines (e.g., daily row ingestion count drops by 60%).

#### Q213: What is Data Catalog (e.g., Apache Atlas, Amundsen, Atlan)?
**Answer:** An enterprise metadata repository that indexes data assets across databases, data lakes, and BI tools, enabling search, data discovery, documentation tagging, and lineage visualization.

#### Q214: What is GDPR "Right to be Forgotten" (Data Erasure), and how is it implemented in Data Lakes?
**Answer:** A regulatory requirement requiring organizations to delete all personal data belonging to an individual upon request.
*   *Implementation*: In traditional object storage, deleting rows required expensive full-file rewrites. In Data Lakehouses (Delta Lake/Iceberg), it is handled efficiently via `DELETE FROM table WHERE user_id = X` executing deletion vectors or ACID partition updates.

#### Q215: Explain SOC 2 and HIPAA Compliance in Data Architecture.
**Answer:**
*   **SOC 2**: Audit framework certifying that a cloud data platform manages data securely based on 5 trust service criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy).
*   **HIPAA**: US regulation requiring administrative, physical, and technical safeguards for PHI data (auditing, encryption, access logs).

#### Q216: What is a Data Contract?
**Answer:** An explicit agreement between software engineering producers (who own application services emitting events) and data engineering consumers defining the schema, SLA, semantics, quality expectations, and change notifications for data APIs.

#### Q217: What is Differential Privacy?
**Answer:** A mathematical technique that adds controlled random statistical noise to analytical query outputs, allowing business intelligence reporting across dataset populations while preventing attackers from discovering individual participant identities.

#### Q218: What is Data Quarantine / Data Sanitization Pipeline pattern?
**Answer:** Ingesting incoming data into a sandbox stage where data quality rules are executed. Valid records are passed to core warehouse tables; invalid records are isolated in a quarantine store for engineering inspection.

#### Q219: Explain KMS (Key Management Service) Envelop Encryption.
**Answer:** Encrypting data with a local Data Encryption Key (DEK), and then encrypting the DEK with a master Key Encryption Key (KEK) managed inside a secure cloud KMS hardware module.

#### Q220: What is Zero-Trust Security in Data Architecture?
**Answer:** A security model operating under the principle "never trust, always verify". Every client request, service connection, and data access call must be authenticated, authorized, encrypted, and logged regardless of network location.

#### Q221: How do you handle Data Retention Policies?
**Answer:** Defining lifecycle rules that automatically archive data to lower-cost cold storage (e.g., Moving S3 Standard to S3 Glacier after 90 days) and permanently purging data after legal retention periods expire.

#### Q222: What is Data Drift vs Model Drift?
**Answer:**
*   **Data Drift**: Unintended statistical shift in input data distribution entering a pipeline over time (e.g., user demographics changing after a marketing campaign).
*   **Model Drift**: Degradation in machine learning model prediction accuracy due to real-world behavioral changes over time.

#### Q223: How do you implement Column Tagging for Governance?
**Answer:** Tagging table columns with metadata labels (e.g., `TAG PII = 'CONFIDENTIAL'`). Access control policies automatically enforce masking rules across all columns carrying the `PII` tag without manual policy creation per table.

#### Q224: What is Audit Logging in Cloud Data Warehouses?
**Answer:** System logs recording every access event, authentication attempt, DDL execution, and query statement run in the warehouse (e.g., Snowflake `QUERY_HISTORY()`, GCP Cloud Audit Logs).

#### Q225: What is Soda Core / Soda SQL?
**Answer:** An open-source command-line tool and Python library that allows data engineers to write data quality checks in declarative YAML files (`sodacl`) and execute them during pipeline execution.

---

## 9. Advanced Data Engineering & Real-Time MLOps Pipelines (Q226 - Q250)

#### Q226: What is a Feature Store in MLOps Data Architecture?
**Answer:** A centralized data platform that manages ML feature pipelines, serving consistent feature data for both offline batch model training and low-latency (< 10ms) online real-time inference (e.g., Feast, Hopsworks).

#### Q227: Compare Offline Feature Store vs. Online Feature Store.
**Answer:**
*   **Offline Feature Store**: High-capacity historical storage (S3, Parquet, Snowflake, BigQuery) used to generate training datasets across long time windows for batch ML training.
*   **Online Feature Store**: Low-latency key-value cache (Redis, Cassandra, DynamoDB) serving pre-computed current feature vectors to online ML model microservices.

#### Q228: What is Point-in-Time Correctness (Time-Travel Join) in Feature Stores?
**Answer:** A join technique that prevents data leakage during ML training dataset creation. It joins entity events with feature values as they existed strictly *at the exact time the historical event occurred*, ignoring feature updates that happened after the event timestamp.

#### Q229: What is a Vector Database, and why is it used in GenAI Data Engineering?
**Answer:** A database optimized for indexing, storing, and querying high-dimensional mathematical vector embeddings generated by machine learning models (e.g., Pinecone, Milvus, Qdrant, pgvector). Enables fast vector similarity search (k-NN/ANN) for Retrieval-Augmented Generation (RAG) pipelines.

#### Q230: Explain Similarity Search Algorithms: Cosine Similarity vs. Euclidean Distance vs. Dot Product.
**Answer:**
*   **Cosine Similarity**: Measures the cosine of the angle between two vectors (evaluates semantic direction regardless of vector magnitude). Range: -1 to 1.
*   **Euclidean Distance (L2)**: Measures straight-line distance between vector endpoints in multi-dimensional space.
*   **Dot Product**: Measures vector direction and magnitude (fastest computation when vectors are normalized).

#### Q231: What is Approximate Nearest Neighbors (ANN) Indexing (HNSW, IVF)?
**Answer:** Algorithms that speed up vector similarity searches over millions of high-dimensional vectors by sacrificing a tiny fraction of accuracy for orders-of-magnitude speed improvements:
*   **HNSW (Hierarchical Navigable Small World)**: Graph-based vector index delivering ultra-fast search speed.
*   **IVF (Inverted File Index)**: Clustering-based vector index that partitions space into Voronoi cells to narrow search scope.

#### Q232: What is Retrieval-Augmented Generation (RAG) Architecture?
**Answer:** An AI architecture where incoming user prompts are converted into vector embeddings, used to retrieve relevant enterprise document chunks from a Vector Database, and appended to the LLM prompt context window to generate grounded answers without fine-tuning models.

#### Q233: What is Data Engineering FinOps (Financial Operations)?
**Answer:** The practice of bringing financial accountability to cloud data engineering, continuously monitoring, managing, and optimizing infrastructure spend across compute clusters, storage tiers, and query engines.

#### Q234: Explain key strategies for reducing Spark infrastructure costs.
**Answer:**
1.  Use AWS Spot Instances / GCP Preemptible VMs for stateless worker executors (saves 60-80%).
2.  Enable Dynamic Allocation (`spark.dynamicAllocation.enabled=true`) to scale executor worker count up/down based on workload queue.
3.  Tune JVM memory settings to avoid OOM retries.
4.  Compact small files to eliminate unnecessary object storage list calls.

#### Q235: Explain key strategies for reducing Snowflake / BigQuery query costs.
**Answer:**
1.  Enforce Partitioning & Clustering to limit data byte scanning.
2.  Set Query Execution Timeouts and Maximum Bytes Billed limits.
3.  Configure Auto-Suspend on Snowflake Virtual Warehouses to 1-2 minutes.
4.  Avoid `SELECT *` queries in analytical workloads; select only explicit columns required.

#### Q236: What is Chunking in GenAI RAG Data Pipelines?
**Answer:** The process of breaking large raw text documents (PDFs, Markdown, Web pages) into smaller, semantically coherent text passages (e.g., 512 tokens with 50-token overlap) before generating vector embeddings for storage in a Vector DB.

#### Q237: What is Embedding Model in Data Pipelines?
**Answer:** A deep learning model (e.g., OpenAI `text-embedding-3-small`, HuggingFace `bge-large-en`) that converts raw text, images, or audio into fixed-length floating-point vector arrays (e.g., 1536-dimensional array) capturing semantic meaning.

#### Q238: What is Semantic Caching in AI Data Pipelines?
**Answer:** Caching past LLM prompt queries and generated responses in a Vector Database. When a new user query arrives, if its vector embedding has high cosine similarity (e.g., > 0.95) to a cached query, the cached answer is returned instantly without incurring LLM API costs.

#### Q239: Explain Real-Time Feature Ingestion Pipeline Architecture.
**Answer:**
```
[Event Source] -> [Kafka/Flink Stream] -> [Real-Time Feature Transformation]
                                                 |
                       ┌─────────────────────────┴─────────────────────────┐
                       ▼                                                   ▼
         [Online Store: Redis Cache]                        [Offline Store: Delta Lake/S3]
         (Serves Real-Time Inference < 5ms)                 (Serves Historical ML Training)
```

#### Q240: What is Data Leakage in Machine Learning Pipelines?
**Answer:** Occurs when information from the target prediction label or future dataset leaks into the feature training set during feature engineering, resulting in artificially high model validation accuracy that fails completely in production.

#### Q241: What is Reverse ETL?
**Answer:** The process of moving transformed, aggregated data out of cloud data warehouses back into operational business applications (Salesforce, HubSpot, Zendesk, Stripe) to empower front-line business teams (e.g., Hightouch, Census).

#### Q242: Explain Data Fabric vs Data Mesh.
**Answer:**
*   **Data Fabric**: An architectural approach leveraging automated metadata discovery, AI/ML graphs, and integrated pipelines to dynamically connect distributed data sources into a unified virtualization layer.
*   **Data Mesh**: An organizational and architectural approach emphasizing domain ownership, data-as-a-product, and federated self-serve governance.

#### Q243: What is Unstructured Data Processing in Modern Data Engineering?
**Answer:** Extracting structured tabular features from raw video, audio, logs, and PDF documents using OCR tools (Tesseract), NLP parsers, and Multimodal LLMs, storing output in Lakehouse parquet tables.

#### Q244: How do you handle Data Pipeline Disaster Recovery (DR)?
**Answer:**
1.  **Multi-Region Object Storage**: Enable Cross-Region Replication (CRR) on S3/GCS buckets.
2.  **Metadata Backups**: Automate daily exports of Hive metastore/Postgres catalogs and Git version control for all Airflow/dbt/Terraform code.
3.  **RPO (Recovery Point Objective)** & **RTO (Recovery Time Objective)**: Maintain disaster recovery runbooks to redeploy infrastructure using IaC (Terraform).

#### Q245: What is Zero-Copy Integration (e.g., Salesforce + BigQuery/Snowflake)?
**Answer:** Direct live data sharing integrations between SaaS applications and cloud data warehouses without running traditional ETL ingestion pipelines, allowing querying of live SaaS records in-place.

#### Q246: Explain Data Pipeline Monitoring and Alerting Best Practices.
**Answer:**
*   Integrate Airflow/Dagster notification hooks with Slack/PagerDuty for task failures.
*   Track core SLIs: Pipeline completion SLA timestamp, record volume changes, failure rates, and infrastructure cost anomalies.

#### Q247: What is Hybrid Search in Vector Databases?
**Answer:** Combining traditional BM25 keyword text search with dense vector similarity search (k-NN) using Reciprocal Rank Fusion (RRF) to deliver superior retrieval accuracy for complex user queries in RAG systems.

#### Q248: Explain Graph Databases in Data Engineering (Neo4j, AWS Neptune).
**Answer:** Databases designed to store and query nodes (entities) and edges (relationships) natively. Ideal for fraud detection, network topology, recommendation engines, and knowledge graph construction.

#### Q249: What is Columnar Storage Partition Skew in BigQuery / Snowflake?
**Answer:** Occurs when partitioning a table on a high-cardinality key resulting in millions of tiny partitions, or on a biased key resulting in a single massive partition, causing uneven query slot distribution. *Fix*: Use Partitioning on low-cardinality keys (dates) combined with Clustering on high-cardinality keys.

#### Q250: Summary: What are the key traits of a Senior Data Engineer?
**Answer:**
1.  **Architectural Mastery**: Ability to design scalable, cost-effective Data Warehouses, Lakes, Lakehouses, and Streaming architectures tailored to business workloads.
2.  **Code Excellence**: Mastery of SQL, Python/PySpark, software engineering principles (clean code, modular design, CI/CD, unit testing).
3.  **Data Reliability & Governance**: Designing idempotent, self-healing pipelines with automated data quality checks, observability, and strict security compliance.
4.  **FinOps & Business Alignment**: Continuously optimizing cloud infrastructure spend while delivering reliable, low-latency data products that drive business value.
