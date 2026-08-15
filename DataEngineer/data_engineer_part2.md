# Data Engineer 250 Interview Questions & Answers - Part 2

This is Volume 2 of the Data Engineer Interview Guide, containing **Questions 91 to 170**. It covers Modern Data Lakehouses (Delta Lake, Apache Iceberg, Apache Hudi), File Formats (Parquet, ORC, Avro), Pipeline Orchestration (Apache Airflow, dbt), and Cloud Data Warehouses (Snowflake, Google Cloud BigQuery, AWS Redshift, Databricks).

---

## 📋 Table of Contents (Part 2)
4. [Modern Data Lakehouses & Storage File Formats (Q91 - Q120)](#4-modern-data-lakehouses--storage-file-formats-q91---q120)
5. [ETL/ELT Pipeline Orchestration & Transformations (Q121 - Q145)](#5-etlelt-pipeline-orchestration--transformations-q121---q145)
6. [Cloud Data Warehouses & Analytics Services (Q146 - Q170)](#6-cloud-data-warehouses--analytics-services-q146---q170)

---

## 4. Modern Data Lakehouses & Storage File Formats (Q91 - Q120)

#### Q91: Compare Row-Oriented vs Column-Oriented Data Storage formats.
**Answer:**
*   **Row-Oriented (CSV, JSON, Avro)**: Stores entire record rows consecutively on disk. Excellent for OLTP write-heavy applications and fetching full record rows by key. Slow for analytics queries aggregating specific subset columns across millions of rows.
*   **Column-Oriented (Parquet, ORC)**: Stores column values sequentially on disk. Highly efficient for OLAP analytical queries (scans only requested columns, eliminates unused disk reads) and enables superior compression ratios.

#### Q92: What is Apache Parquet, and how is it structured internally?
**Answer:** An open-source, columnar storage file format optimized for big data query engines.
*   *Internal Structure*: Organized into **Row Groups** (typically 128 MB–1 GB). Each Row Group contains **Column Chunks** for every column. Column Chunks are divided into **Pages** (containing data values, dictionary encodings, and min/max statistics).

#### Q93: How do Parquet files use Predicate Pushdown and Projection Pushdown?
**Answer:**
*   **Projection Pushdown**: Read engines scan only the specific byte offsets of requested columns in the SELECT clause, completely skipping unreferenced columns.
*   **Predicate Pushdown**: Read engines evaluate `WHERE` clause filters against page/row-group metadata statistics (min/max values) to skip reading entire row groups without uncompressing file data blocks.

#### Q94: Compare Apache Parquet, ORC, and Avro.
**Answer:**
*   **Avro**: Row-based, binary format with inline schema definition. Best for data serialization in streaming ingestion pipelines (Kafka).
*   **Parquet**: Columnar format optimized for Spark and general big data analytics engines.
*   **ORC (Optimized Row Columnar)**: Columnar format optimized primarily for Hive and Presto/Trino engines, offering lightweight indexing (indexes every 10,000 rows).

#### Q95: What is Data Compaction in Big Data storage?
**Answer:** The process of merging thousands of small files (created by streaming ingestion or micro-batch writes) into larger contiguous files (e.g., 128 MB–512 MB). Solves the "Small File Problem" which causes driver memory overload and high object storage list-call latency.

#### Q96: What is Open Table Format in Data Lakehouses?
**Answer:** A metadata management layer built on top of cloud object storage (S3, GCS) that provides ACID database transactions, time travel, schema evolution, and concurrent writer isolation over raw parquet files (e.g., Delta Lake, Apache Iceberg, Apache Hudi).

#### Q97: Explain Delta Lake architecture and its Transaction Log (`_delta_log`).
**Answer:** Delta Lake stores data as Parquet files alongside an append-only JSON transaction log folder (`_delta_log`).
*   Every commit creates a new JSON commit file (e.g., `000001.json`). Periodic checkpoint files (Parquet) summarize transaction history to accelerate metadata loading.

#### Q98: What is Apache Iceberg, and how does it differ from Delta Lake?
**Answer:** Apache Iceberg is a high-performance open table format designed for huge analytical tables.
*   *Difference*: Iceberg abstracts table layout at the individual **file level** rather than partition directories, using a 3-tier metadata architecture (Catalog -> Metadata File -> Manifest List -> Manifest Files -> Data Files). This enables hidden partitioning and partition evolution without rewriting tables.

#### Q99: What is Apache Hudi, and what are its table types?
**Answer:** An open table format designed for low-latency streaming ingest and CDC updates into data lakes.
1.  **Copy-on-Write (CoW)**: Rewrites existing Parquet data files during updates (higher write latency, fast read latency).
2.  **Merge-on-Read (MoR)**: Appends updates to delta log files (Avro) and merges them with base Parquet files at read/query time (fast write ingestion, slightly higher read latency).

#### Q100: Explain Time Travel in Delta Lake and Iceberg.
**Answer:** The ability to query an analytical table as it existed at a specific timestamp or historical version number by utilizing transaction log commit histories and manifest files.
*   *Example (Delta Lake SQL)*:
```sql
SELECT * FROM sales_table VERSION AS OF 42;
SELECT * FROM sales_table TIMESTAMP AS OF '2026-01-15 00:00:00';
```

#### Q101: What is the `VACUUM` command in Delta Lake?
**Answer:** A command that permanently deletes unreferenced data files older than a specified retention period (default 7 days) to reclaim cloud storage space. *Note*: Executing `VACUUM` prevents time-travel queries to versions prior to the retention threshold.

#### Q102: What is Z-Ordering (Multidimensional Clustering) in Delta Lake?
**Answer:** A technique that maps multi-column dimensional data into space-filling Z-values, clustering related information into the same set of files. Dramatically increases the effectiveness of data skipping for multi-column `WHERE` filters.

#### Q103: Explain Partition Evolution in Apache Iceberg.
**Answer:** The ability to change a table's partitioning strategy (e.g., changing from partitioning by `YYYY-MM` to `YYYY-MM-DD`) without rewriting existing historical data files. Iceberg handles queries across old and new partition specs seamlessly.

#### Q104: Explain Hidden Partitioning in Apache Iceberg.
**Answer:** Users do not need to supply explicit partition transform columns in queries (e.g., `WHERE year = 2026 AND month = 5`). Iceberg automatically derives partition filters directly from timestamp queries (`WHERE event_timestamp >= '2026-05-01'`), preventing incorrect full-table scans.

#### Q105: What is Schema Enforcement (Schema Validation)?
**Answer:** A feature in Lakehouse formats that rejects DataFrame write operations if the incoming schema contains extra or mismatched data type columns not present in the target table schema, preventing silent table corruption.

#### Q106: What is Schema Evolution via `mergeSchema` in PySpark Delta Lake?
**Answer:** Explicitly allowing new columns in incoming DataFrames to be appended to the target Delta table schema automatically during write operations:
```python
df.write.option("mergeSchema", "true").mode("append").save(delta_path)
```

#### Q107: Differentiate Copy-on-Write vs Merge-on-Read.
**Answer:**
*   **Copy-on-Write (CoW)**: During an UPDATE/DELETE, entire data files containing modified rows are re-written. Fast reads, slow writes.
*   **Merge-on-Read (MoR)**: Modifications are written to separate log files/deletion vectors. Reads must reconcile base files + log files. Fast ingestion, trade-off on read speed.

#### Q108: What are Deletion Vectors in Delta Lake 3.0?
**Answer:** A optimization for Copy-on-Write tables where row deletions are written to a small sidecar bit-vector file marking deleted rows. Bypasses the expensive step of rewriting entire Parquet data files during simple `DELETE` or `UPDATE` statements.

#### Q109: Explain Snappy, GZIP, and ZSTD Compression Formats.
**Answer:**
*   **Snappy**: Moderate compression ratio, extremely high encoding/decoding speed, CPU friendly. Standard default for Parquet/Spark.
*   **GZIP**: High compression ratio, higher CPU cost, lower throughput.
*   **ZSTD (Zstandard)**: Next-gen compression offering high compression ratios comparable to GZIP with decoding speeds matching Snappy.

#### Q110: What makes a file format "Splittable" in distributed computing?
**Answer:** The ability of a file to be processed by multiple parallel workers across arbitrary byte-offset boundaries without reading from the beginning. Parquet and BZip2 are splittable; standard uncompressed GZIP files are non-splittable.

#### Q111: Explain the Medallion Architecture (Bronze -> Silver -> Gold).
**Answer:** A data design pattern used in Lakehouses to structure data cleanliness logically:
*   **Bronze (Raw)**: Raw, un-validated append-only historical ingestion landing zone.
*   **Silver (Cleansed/Enriched)**: Filtered, cleaned, deduplicated, and normalized data joined with reference tables.
*   **Gold (Curated Business Insights)**: Aggregated, domain-specific data marts optimized for executive reporting, BI dashboards, and ML features.

#### Q112: What is the Small File Problem in HDFS and Cloud Object Storage?
**Answer:** Having millions of files significantly smaller than the block size (e.g., < 10 MB). In HDFS, it overwhelms NameNode RAM storing file metadata. In Cloud Object Storage (S3/GCS), it causes massive HTTP LIST/GET call latency and overhead during Spark directory listing.

#### Q113: How do you compact small files in Delta Lake?
**Answer:** Run the `OPTIMIZE` command:
```sql
OPTIMIZE sales_delta_table;
-- Or with Z-Ordering:
OPTIMIZE sales_delta_table ZORDER BY (customer_id, region);
```

#### Q114: What is Unity Catalog in Databricks?
**Answer:** A unified governance solution for Data Lakes providing centralized access control (RBAC/ABAC), data auditing, lineage tracking, and data discovery across multiple workspaces and cloud regions.

#### Q115: What is AWS Glue Data Catalog?
**Answer:** A persistent, managed Apache Hive-compatible metadata metastore on AWS that stores table definitions, schemas, and partition locations for Athena, EMR, Redshift Spectrum, and Spark jobs.

#### Q116: Explain Data Sanitization and Data Anonymization.
**Answer:**
*   **Sanitization**: Removing or modifying sensitive data (PII) before storage (e.g., truncating IP addresses).
*   **Anonymization**: Irreversibly transforming PII attributes (e.g., cryptographic hashing with salt) so individuals cannot be re-identified.

#### Q117: What is File Pruning (Partition Pruning & Min/Max Pruning)?
**Answer:** The capability of query engines to evaluate SQL `WHERE` clauses against directory partition structures or file-level footer statistics (min/max column values) to bypass downloading unneeded files from object storage.

#### Q118: How do you handle schema drifts in semi-structured JSON ingestion?
**Answer:** Ingest raw JSON payloads into a variant/json column type (e.g., Snowflake `VARIANT`, BigQuery `JSON`, Databricks `VARIANT`), then use schema-on-read transformation tools (dbt, PySpark) to extract structured fields dynamically.

#### Q119: What is Apache Hive Metastore (HMS)?
**Answer:** The historical standard metadata catalog storing table schemas, data types, physical file paths, and partition details in a relational database (e.g., MySQL) for Hadoop/Spark execution engines.

#### Q120: Differentiate Structured Streaming sink modes: Append, Complete, Update.
**Answer:**
*   **Append**: Only new rows added to the stream since the last trigger are written to the sink.
*   **Complete**: The entire updated result table (including historical aggregations) is rewritten to the sink.
*   **Update**: Only rows that were updated or modified since the last trigger are written to the sink.

---

## 5. ETL/ELT Pipeline Orchestration & Transformations (Q121 - Q145)

#### Q121: Compare ETL (Extract, Transform, Load) vs. ELT (Extract, Load, Transform).
**Answer:**
*   **ETL**: Data is transformed on a dedicated processing engine (Spark, Informatica) *before* loading into the target warehouse. Used for legacy on-prem storage where compute inside warehouse was expensive.
*   **ELT**: Raw data is extracted and loaded directly into a cloud data warehouse (BigQuery, Snowflake) *first*, leveraging the warehouse's massive, scalable compute engine to execute transformations in SQL (dbt).

#### Q122: What is Apache Airflow, and what are its core components?
**Answer:** An open-source workflow orchestration platform for programmatically authoring, scheduling, and monitoring data pipelines as DAGs (Directed Acyclic Graphs).
*   **Components**:
    1.  **Webserver**: UI to monitor execution, logs, and DAG states.
    2.  **Scheduler**: Evaluates DAG triggers and submits tasks to executor queue.
    3.  **Executor**: Manages task allocation (LocalExecutor, CeleryExecutor, KubernetesExecutor).
    4.  **Worker**: Executes task code.
    5.  **Metadata Database**: Stores task states, DAG configs, variables, and history (Postgres/MySQL).

#### Q123: What is a DAG in Apache Airflow?
**Answer:** A Directed Acyclic Graph: a collection of tasks organized with explicit directional dependencies (e.g., `Task A >> [Task B, Task C] >> Task D`) ensuring tasks execute in sequence without cyclical loops.

#### Q124: Differentiate Airflow Operators, Tasks, and Task Instances.
**Answer:**
*   **Operator**: The template/class definition of a unit of work (e.g., `PythonOperator`, `BashOperator`, `BigQueryExecuteQueryOperator`).
*   **Task**: A specific instantiation of an Operator within a DAG definition.
*   **Task Instance**: A single specific run execution of a Task for a particular logical execution date/timestamp.

#### Q125: What is Airflow XCom (Cross-Communication)?
**Answer:** A mechanism allowing small metadata payloads (typically < 48 KB JSON serializable parameters, task status, execution IDs) to be passed between tasks within the same DAG run via the Airflow metadata database. *Note*: XCom should not be used to pass large dataframes.

#### Q126: Explain Airflow Execution Date / Logical Date (`ds`).
**Answer:** The logical timestamp for which a DAG run is processing data (representing the beginning of the data interval), NOT the wall-clock time when the task actually runs. Essential for writing deterministic, backfillable pipelines.

#### Q127: What is Airflow Backfilling?
**Answer:** The process of running a historical DAG across a past date range (e.g., running a newly deployed daily pipeline for the past 6 months) using historical `logical_date` parameters.

#### Q128: Explain Airflow Executors: CeleryExecutor vs KubernetesExecutor.
**Answer:**
*   **CeleryExecutor**: Assigns tasks to a fixed, pre-allocated pool of worker virtual machines running Celery worker daemons.
*   **KubernetesExecutor**: Dynamically spawns an isolated Kubernetes Pod for every individual task instance run, providing dynamic resource allocation and clean environment isolation, terminating the Pod upon completion.

#### Q129: What is dbt (Data Build Tool)?
**Answer:** An open-source ELT transformation tool that allows data engineers to write SQL `SELECT` statements (Models) with Jinja templating, version control them, and compile them into DDL/DML executed inside cloud data warehouses.

#### Q130: What are dbt Models and Materializations?
**Answer:**
*   **Model**: A `.sql` file containing a single SELECT statement defining a data transformation.
*   **Materialization Types**:
    1.  `view`: Compiles model into a standard database VIEW.
    2.  `table`: Rebuilds the entire table from scratch on every run.
    3.  `incremental`: Inserts/updates only new or changed records since the last dbt run.
    4.  `ephemeral`: Interpolated as a Common Table Expression (CTE) inside dependent models without creating a warehouse object.

#### Q131: How do dbt Incremental Models work?
**Answer:** Uses Jinja conditionals (`is_incremental()`) to filter source data based on timestamps, appending or updating target table rows:
```sql
{{ config(materialized='incremental', unique_key='order_id') }}

select * from {{ ref('raw_orders') }}
{% if is_incremental() %}
  where order_timestamp > (select max(order_timestamp) from {{ this }})
{% endif %}
```

#### Q132: What is dbt `ref()` and `source()` functions?
**Answer:**
*   `source('schema', 'table')`: References raw ingestion tables, creating lineage links to upstream sources.
*   `ref('model_name')`: References another dbt model, building automatic DAG dependency graphs and ensuring dependent models execute in correct topological order.

#### Q133: What are dbt Tests?
**Answer:** Automated data quality assertions executed against model tables in the cloud warehouse.
*   *Generic Tests*: Out-of-the-box validations: `unique`, `not_null`, `accepted_values`, `relationships` (foreign key referential integrity).
*   *Singular Tests*: Custom SQL queries returning failing rows (if query returns > 0 rows, test fails).

#### Q134: What is dbt Snapshot?
**Answer:** A mechanism in dbt to implement Type 2 Slowly Changing Dimensions (SCD Type 2) over source tables that overwrite data, automatically tracking row modification histories via timestamp or check columns.

#### Q135: What is Task Idempotency in Data Pipelines?
**Answer:** Designing pipeline tasks so re-running a task for date `2026-05-15` produces identical table states without creating duplicate rows (e.g., using `DELETE WHERE partition_date = '2026-05-15'` followed by `INSERT`, or using `MERGE`/`UPSERT` logic).

#### Q136: What is Apache Airflow Sensor?
**Answer:** A special type of operator that continuously polls or waits for an external event or state to become true (e.g., `S3KeySensor` waiting for a file to land in S3; `ExternalTaskSensor` waiting for a dependent DAG task to complete) before allowing downstream tasks to proceed.

#### Q137: Explain Sensor Mode: `poke` vs `reschedule` in Airflow.
**Answer:**
*   `poke` (default): Sensor holds onto worker execution slot while sleeping between polls (wastes worker resources during long waits).
*   `reschedule`: Sensor frees up worker execution slot between polling intervals, re-queueing itself when the next check interval occurs (resource efficient).

#### Q138: Compare Prefect vs Apache Airflow.
**Answer:**
*   **Airflow**: Static DAG-based structure defined at parse time, centralized scheduler, heavy reliance on execution dates.
*   **Prefect**: Dynamic execution DAGs resolved at runtime, "code-as-workflows" paradigm (uses standard Python decorators `@flow` and `@task`), native parameterized invocations, data-flow centric.

#### Q139: Compare Dagster vs Apache Airflow.
**Answer:**
*   **Dagster**: Asset-based orchestration model ("Software-Defined Assets"), treating data products as primary abstractions rather than tasks. Strong focus on local testing, type checking, and data observability.

#### Q140: What is Data Pipeline Backpressure and how is it managed in Airflow?
**Answer:** Prevented using Airflow concurrency controls:
*   `max_active_runs`: Limits concurrent DAG runs.
*   `concurrency` / `max_active_tasks_per_dag`: Limits active task instances per DAG.
*   `pools`: Restricts concurrent task execution accessing specific external resources (e.g., limiting concurrent connections to a operational database).

#### Q141: What is a dbt Semantic Layer?
**Answer:** A centralized metric definition layer in dbt (`metrics`) allowing organizations to define business metrics (e.g., `monthly_recurring_revenue`) once in code, exposing consistent definitions to BI tools (Tableau, Lightdash, Hex).

#### Q142: How do you handle secrets and credentials in Apache Airflow?
**Answer:** Store credentials securely in Airflow **Connections** or integrate with enterprise Secret Managers (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault) using Airflow Secret Backends, avoiding hardcoded plaintext keys in code repository DAGs.

#### Q143: Explain Dynamic DAG Generation in Apache Airflow.
**Answer:** Writing Python code loops that dynamically parse external configurations (YAML/JSON files) or database tables to instantiate multiple DAG objects dynamically within a single DAG file.

#### Q144: What is dbt Slim CI?
**Answer:** A CI/CD optimization technique where dbt compiles and runs tests only on models that were modified in a pull request (and their immediate downstream dependents), identified using `state:modified+` comparison against production manifest state files.

#### Q145: What is SLA (Service Level Agreement) in Data Engineering pipelines?
**Answer:** The guaranteed maximum timeframe by which a data pipeline must finish processing and deliver output tables to business stakeholders (e.g., "Executive sales dashboard must be fully updated by 06:00 AM EST every morning").

---

## 6. Cloud Data Warehouses & Analytics Services (Q146 - Q170)

#### Q146: Explain Snowflake's Multi-Cluster Shared Data Architecture.
**Answer:** Separates compute and storage into 3 decoupled layers:
1.  **Database Storage Layer**: Centralized cloud object storage (S3/GCS/Azure Blob) storing data in proprietary encrypted micro-partitions.
2.  **Query Processing Layer**: Independent virtual warehouses (MPP compute clusters) that execute queries without resource contention.
3.  **Cloud Services Layer**: Manages authentication, metadata, query parsing, optimization, access control, and transaction security.

#### Q147: What are Snowflake Micro-partitions?
**Answer:** Immutable, contiguous 50 MB–150 MB uncompressed storage blocks automatically created when data is loaded into Snowflake. Contains detailed metadata footers (min/max values, distinct counts) enabling aggressive partition pruning without manual index management.

#### Q148: What is Zero-Copy Cloning in Snowflake?
**Answer:** A feature that creates an instant duplicate copy of a database, schema, or table without duplicating underlying storage files. The cloned object references the existing micro-partitions until new write updates create modified micro-partitions (Copy-on-Write).

#### Q149: What is Snowflake Virtual Warehouse Auto-suspend and Auto-resume?
**Answer:** Settings that automatically shut down virtual compute warehouses when idle for a specified duration (e.g., 5 minutes) to eliminate compute charges, and automatically resume compute instantly when a new query is submitted.

#### Q150: Explain Google Cloud BigQuery Architecture (Dremel & Colossus).
**Answer:**
*   **Compute (Dremel)**: Multi-tenant serverless execution engine that compiles SQL queries into execution trees distributed across thousands of slots (workers).
*   **Storage (Colossus)**: Google's global distributed file system storing data in columnar Capacitor format, connected to Dremel via ultra-fast Jupiter network fabric (100 Gbps+).

#### Q151: What are BigQuery Slots?
**Answer:** A virtual CPU unit used by BigQuery to execute SQL queries. BigQuery dynamically scales slots based on query complexity (On-Demand billing model) or allocates dedicated capacity reservations (Flat-Rate / Edition pricing model).

#### Q152: Compare BigQuery Table Partitioning vs. Table Clustering.
**Answer:**
*   **Partitioning**: Segregates table data into distinct physical storage segments based on a date, timestamp, or integer range column (scans only matching partitions).
*   **Clustering**: Sorts and organizes data within partitions based on up to 4 specified columns, improving query efficiency for specific `WHERE` and `JOIN` filters.

#### Q153: Write a BigQuery SQL DDL statement to create a partitioned and clustered table.
**Answer:**
```sql
CREATE TABLE `my_project.analytics.orders`
(
  order_id STRING,
  customer_id STRING,
  order_date DATE,
  total_amount NUMERIC
)
PARTITION BY order_date
CLUSTER BY customer_id
OPTIONS(
  require_partition_filter = true
);
```

#### Q154: Explain AWS Redshift Architecture.
**Answer:** A managed Massively Parallel Processing (MPP) columnar data warehouse consisting of:
*   **Leader Node**: Receives client connections, compiles queries into execution code, and coordinates task distribution.
*   **Compute Nodes**: Execute compiled code on local columnar storage (RA3 nodes decouple storage using Redshift Managed Storage).

#### Q155: What is AWS Redshift Spectrum?
**Answer:** A feature allowing Redshift queries to directly scan and join unstructured or semi-structured data files (Parquet, ORC, CSV) stored in AWS S3 buckets without loading data into native Redshift tables, leveraging the AWS Glue Data Catalog.

#### Q156: Differentiate On-Demand Billing vs Capacity/Editions Pricing in Cloud Warehouses.
**Answer:**
*   **On-Demand**: Billed per-query based on the volume of data scanned (e.g., $5 per TB scanned in BigQuery). Can result in unpredictable costs if unoptimized full-table queries run frequently.
*   **Capacity / Editions (Reserved Slots / Warehouses)**: Billed for dedicated, allocated compute infrastructure per hour (e.g., Snowflake Virtual Warehouse sizes XS-6XL; BigQuery Enterprise Slots), providing cost predictability.

#### Q157: What is Federated Query in Cloud Warehouses?
**Answer:** The capability of a cloud warehouse engine to execute SQL queries directly against external transactional databases (e.g., querying Cloud SQL Postgres or AWS RDS MySQL directly from BigQuery/Redshift) without ETL extraction.

#### Q158: Explain Snowflake Streams and Tasks.
**Answer:**
*   **Stream**: Tracks Change Data Capture (CDC) modifications (inserts, updates, deletes) made to a Snowflake table.
*   **Task**: Executes a specified SQL statement on a schedule or when triggered by a Stream, automating internal ELT transformations inside Snowflake.

#### Q159: What is Databricks Lakehouse Platform?
**Answer:** A unified analytics platform built around Apache Spark, Delta Lake, and MLflow that integrates data engineering, data science, and business intelligence on a single storage layer.

#### Q160: What is Serverless Compute in Databricks / Snowflake / BigQuery?
**Answer:** Compute infrastructure managed entirely by the cloud provider that auto-scales instantaneously to meet query demand without requiring manual cluster size provisioning, VM configuration, or cluster spin-up wait times.

#### Q161: How does Snowflake handle Time Travel storage retention?
**Answer:** Standard Edition provides 1-day retention; Enterprise Edition allows configuring Time Travel retention up to 90 days (`DATA_RETENTION_TIME_IN_DAYS = 90`). Beyond Time Travel, **Fail-safe** provides an additional 7-day non-queryable disaster recovery window managed by Snowflake support.

#### Q162: What is BigQuery Materialized View?
**Answer:** Pre-computed views that periodically background-refresh query aggregate results. BigQuery automatically routes queries matching the view logic to the pre-computed materialized results without modifying original SQL code.

#### Q163: Explain AWS Redshift Distribution Keys (DISTKEY).
**Answer:** Determines how table rows are distributed across compute node slices in a Redshift cluster:
*   `EVEN`: Rows distributed round-robin (good for un-joined tables).
*   `KEY`: Rows with the same key value are stored on the same compute node (eliminates network shuffle during joins).
*   `ALL`: A full copy of the entire table is duplicated to every compute node (ideal for small dimension tables).

#### Q164: Explain AWS Redshift Sort Keys (SORTKEY).
**Answer:** Determines the physical order in which data rows are stored within columnar blocks on disk slices (similar to indexes). B-tree block metadata stores min/max values allowing Redshift to skip unneeded blocks during query filtering.

#### Q165: What is Azure Synapse Analytics?
**Answer:** Microsoft's enterprise analytics service combining SQL data warehousing (Dedicated SQL Pools MPP), Spark big data processing, and Azure Data Factory integration in a single workspace.

#### Q166: What is a Secure Data Sharing in Snowflake / BigQuery?
**Answer:** Sharing live analytical tables directly with external organizations/accounts without copying or transferring physical data files across object storage. Consumers query the provider's data live with read-only access.

#### Q167: What is Search Optimization Service in Snowflake?
**Answer:** A background maintenance service that creates and updates persistent search access paths (lookup indexes) over high-cardinality table columns, speeding up point lookup queries returning small row counts.

#### Q168: How do you prevent cost overruns in Google Cloud BigQuery?
**Answer:**
1.  Enforce `require_partition_filter = true` on large tables.
2.  Set maximum bytes billed limits per query (`maximum_bytes_billed`).
3.  Set project-level and user-level daily quota caps.
4.  Utilize Partitioning and Clustering to minimize data scan volumes.

#### Q169: What is Delta Live Tables (DLT) in Databricks?
**Answer:** A declarative framework for building reliable ETL data pipelines in PySpark/SQL. DLT manages DAG dependencies, automatic error handling, data quality testing (`EXPECTATIONS`), and infrastructure scaling automatically.

#### Q170: Explain Data Caching in Cloud Warehouses.
**Answer:** Warehouses cache query metadata and results at multiple levels:
*   **Result Set Cache**: Returns pre-computed query results instantly if the exact same SQL query is submitted again and underlying table data has not changed (cost = $0).
*   **Local Disk/SSD Cache**: Caches downloaded micro-partitions/blocks on compute node local SSDs to avoid downloading from remote object storage repeatedly.
