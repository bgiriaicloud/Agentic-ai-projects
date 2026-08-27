# Data Engineer 250 Interview Questions & Answers - Part 1

This is Volume 1 of the Data Engineer Interview Guide, containing **Questions 1 to 90**. It covers Data Warehousing, Data Modeling (Star Schema, Snowflake Schema, Data Vault 2.0), Apache Spark Architecture, PySpark DataFrame Optimizations, and Data Ingestion & Event Streaming (Apache Kafka, Flink).

---

## 📋 Table of Contents (Part 1)
1. [Data Warehousing & Data Modeling (Q1 - Q30)](#1-data-warehousing--data-modeling-q1---q30)
2. [Distributed Computing & Apache Spark Fundamentals (Q31 - Q60)](#2-distributed-computing--apache-spark-fundamentals-q31---q60)
3. [Data Ingestion & Event Streaming Pipelines (Q61 - Q90)](#3-data-ingestion--event-streaming-pipelines-q61---q90)

---

## 1. Data Warehousing & Data Modeling (Q1 - Q30)

#### Q1: What is the primary difference between OLTP and OLAP systems?
**Answer:**
*   **OLTP (Online Transaction Processing)**: Optimized for fast, frequent transactional write/update operations (row-oriented, normalized 3NF schemas, low latency, high concurrency, e.g., PostgreSQL, MySQL).
*   **OLAP (Online Analytical Processing)**: Optimized for complex analytical read queries over massive historical volumes (columnar storage, denormalized star/snowflake schemas, batch operations, e.g., Snowflake, BigQuery).

#### Q2: Explain the Kimball Dimensional Modeling methodology.
**Answer:** A bottom-up data warehousing approach centered around business processes. It organizes data into **Fact Tables** (containing numeric metrics/measures) connected to **Dimension Tables** (containing descriptive context attributes for slicing and dicing data).

#### Q3: What is a Fact Table? Explain the three main types of Fact Tables.
**Answer:** A central table in a dimensional model containing quantitative metrics (e.g., revenue, quantity sold) and foreign keys referencing dimension tables.
1.  **Transaction Fact Table**: Records an entry for a discrete event at a specific point in time (e.g., individual store purchase receipt).
2.  **Periodic Snapshot Fact Table**: Summarizes metrics over a defined recurring interval (e.g., monthly bank account balance summary).
3.  **Accumulating Snapshot Fact Table**: Tracks a workflow or lifecycle process that has a clear start and end with milestones (e.g., order fulfillment pipeline from order date to delivery date).

#### Q4: What is a Dimension Table?
**Answer:** A table that contains context, attributes, and descriptive textual background surrounding a business event (e.g., `DimCustomer` with name, address, gender; `DimProduct` with brand, category, price).

#### Q5: Compare Star Schema vs. Snowflake Schema.
**Answer:**
*   **Star Schema**: Dimension tables are fully denormalized and directly connected to a single central Fact Table. Offers faster query read performance (fewer `JOIN` operations) at the cost of data redundancy.
*   **Snowflake Schema**: Dimension tables are normalized into sub-dimension tables (e.g., `DimProduct` references `DimCategory`). Reduces data redundancy but increases query complexity and `JOIN` execution latency.

#### Q6: Explain Slowly Changing Dimensions (SCD) Types 0, 1, 2, and 3.
**Answer:**
*   **SCD Type 0**: Fixed attribute (never changes, e.g., original birth date).
*   **SCD Type 1**: Overwrite old data with new data. Historical changes are lost.
*   **SCD Type 2**: Track historical changes by creating a new record row with effective start/end timestamps and an `is_current` boolean flag.
*   **SCD Type 3**: Add a new column to store the previous attribute value (tracks current vs immediate previous value only).

#### Q7: What are SCD Type 4 and Type 6?
**Answer:**
*   **SCD Type 4**: Uses a separate historical history table to archive past records while maintaining only current values in the main dimension table.
*   **SCD Type 6 (Hybrid 1 + 2 + 3)**: Combines Type 1, Type 2, and Type 3 attributes by embedding effective dates and active flags while also overwriting current columns across historical rows.

#### Q8: What is a Conformed Dimension?
**Answer:** A standardized, shared dimension table that is consistently defined and reused across multiple business data marts (e.g., a shared `DimDate` or `DimCustomer` table used across Sales, Marketing, and Support data marts).

#### Q9: What is a Junk Dimension?
**Answer:** A single combined dimension table created to group miscellaneous, low-cardinality flags and indicators (e.g., payment status `IsCash`, tax status `IsTaxable`, delivery flag `IsExpress`) into a single table to avoid cluttering fact tables with foreign keys.

#### Q10: What is a Degenerate Dimension?
**Answer:** A dimension attribute that resides directly inside a Fact Table without referencing a separate dimension table (e.g., invoice numbers, order numbers, transaction hash IDs).

#### Q11: Explain Data Vault 2.0 architecture and its 3 core entity types.
**Answer:** An agile, highly scalable enterprise data warehouse modeling technique designed for multi-source integration.
1.  **Hubs**: Represent core business concepts (e.g., `Hub_Customer`) containing a unique immutable business key, hash key, and load timestamp.
2.  **Links**: Represent relationships or transactions between Hubs (e.g., `Link_Customer_Store_Order`).
3.  **Satellites**: Store context and descriptive attributes over time, capturing change history for Hubs or Links.

#### Q12: What is surrogate key vs business key?
**Answer:**
*   **Business Key (Natural Key)**: A unique identifier assigned by operational source systems (e.g., Customer Social Security Number, Account ID `CUST-1092`).
*   **Surrogate Key**: An internally generated integer ID or cryptographic hash (MD5/SHA256) created by the data warehouse to serve as a primary key, decoupling warehouse data from operational system changes.

#### Q13: What is Data Normalization (1NF, 2NF, 3NF)?
**Answer:**
*   **1NF**: Atomic values (no repeating groups or comma-separated lists in a cell).
*   **2NF**: In 1NF and all non-key columns depend fully on the primary key (no partial dependencies).
*   **3NF**: In 2NF and no transitive dependencies (non-key attributes depend only on the primary key, reducing write anomalies).

#### Q14: When should you deliberately denormalize a data schema?
**Answer:** In analytical data warehouses (OLAP) and big data storage engines where read performance, aggregate speed, and minimal table `JOIN` costs outweigh storage efficiency and update speed requirements.

#### Q15: What is a Factless Fact Table?
**Answer:** A fact table that contains no numeric measures/metrics, only foreign keys. Used to track event occurrences (e.g., student class attendance) or coverage relationships (e.g., products on promotion during a specific week).

#### Q16: Explain the concept of Data Lineage.
**Answer:** The end-to-end tracking of data's origin, transformation lifecycle, dependency paths, and final consumption targets across pipelines, from operational ingestion to downstream dashboards.

#### Q17: What is Data Governance?
**Answer:** The holistic framework of policies, processes, access controls (RBAC/ABAC), data quality standards, and compliance rules (GDPR, HIPAA, CCPA) governing enterprise data assets.

#### Q18: What is Data Mesh architecture?
**Answer:** A decentralized, domain-driven architectural framework that treats data as a product. Domain teams (e.g., Marketing, Supply Chain) own, build, and serve their data products independently using self-serve data infrastructure platforms and federated governance.

#### Q19: Compare Data Warehouse vs. Data Lake vs. Data Lakehouse.
**Answer:**
*   **Data Warehouse**: Structured storage, high-speed SQL, proprietary formats, compute coupled or decoupled from storage (e.g., Snowflake).
*   **Data Lake**: Low-cost blob storage (S3, GCS) holding raw, unstructured, semi-structured, and structured data (e.g., Parquet/ORC files).
*   **Data Lakehouse**: Combines low-cost object storage of Data Lakes with ACID transactions, schema enforcement, and SQL performance of Data Warehouses using open table formats (Delta Lake, Iceberg).

#### Q20: Explain the Data Vault hash key strategy.
**Answer:** Instead of auto-incrementing integers, Data Vault 2.0 uses cryptographic hashes (e.g., SHA-256 of business keys) as primary/foreign keys. This enables multi-threaded parallel loading across distributed systems without waiting for sequence generators.

#### Q21: What is a Bridge Table in dimensional modeling?
**Answer:** A table placed between a dimension and a fact table to resolve many-to-many relationships (e.g., an account shared by multiple joint bank account owners).

#### Q22: What is Grain in dimensional modeling?
**Answer:** The exact level of detail or atomic measurement represented by a single row in a Fact Table (e.g., "one row per line-item on an individual store transaction receipt"). Defining grain is the critical second step in Kimball design.

#### Q23: What is Late-Arriving Data / Late-Arriving Dimensions?
**Answer:** A scenario where fact events arrive in the pipeline before the corresponding dimension record exists in the warehouse. Handled by creating a placeholder/stub dimension record that is updated when the real dimension record arrives.

#### Q24: Explain the difference between Push vs Pull Data Pipelines.
**Answer:**
*   **Push**: Source systems push data events to downstream receivers as soon as they occur (e.g., webhooks, Kafka event streams). Low latency.
*   **Pull**: Data pipelines query or fetch data from source systems on a scheduled batch timer (e.g., scheduled SQL query against transactional DB every midnight).

#### Q25: What is Schema Evolution?
**Answer:** The ability of data storage frameworks (Delta Lake, Iceberg, BigQuery) to gracefully handle schema alterations (adding new columns, renaming, dropping columns) over time without breaking existing pipelines or historical data queries.

#### Q26: What is Data Mart?
**Answer:** A sub-set or focused section of an enterprise data warehouse tailored to the analytical needs of a specific business department or domain (e.g., Sales Data Mart, Finance Data Mart).

#### Q27: What is Lambda Architecture?
**Answer:** A data processing architecture that splits ingestion into two parallel layers:
1.  **Batch Layer**: Processes historical batch data with high latency and maximum accuracy.
2.  **Speed Layer**: Processes streaming real-time data with low latency.
3.  **Serving Layer**: Merges query results from both layers.

#### Q28: What is Kappa Architecture?
**Answer:** An architectural alternative to Lambda that removes the batch layer entirely. All data processing (both real-time and historical backfills) is handled through a single stream-processing engine (e.g., Apache Flink or Kafka Streams) by replaying historical log retention streams.

#### Q29: What is Change Data Capture (CDC)?
**Answer:** A technique that monitors operational database transaction logs (e.g., Postgres WAL, MySQL binlog) to detect and extract `INSERT`, `UPDATE`, and `DELETE` events in real-time without querying source tables directly (e.g., using Debezium).

#### Q30: What is Data Idempotency?
**Answer:** A property of a data pipeline step or task ensuring that executing it multiple times with the same input produces the exact same output state without creating duplicate records or side effects.

---

## 2. Distributed Computing & Apache Spark Fundamentals (Q31 - Q60)

#### Q31: What is Apache Spark?
**Answer:** An open-source, distributed cluster-computing framework designed for fast, in-memory data processing, ETL pipelines, machine learning (MLlib), and stream processing.

#### Q32: Explain the Apache Spark Master/Slave Architecture.
**Answer:**
*   **Driver Node**: Runs the `SparkContext`/`SparkSession`, converts code into a DAG (Directed Acyclic Graph) of execution stages, coordinates task execution, and communicates with the Cluster Manager.
*   **Cluster Manager**: Allocates cluster resources (YARN, Kubernetes, Standalone).
*   **Worker Nodes / Executors**: Distributed JVM processes running tasks in parallel, storing cached data blocks, and reporting status back to Driver.

#### Q33: What is RDD (Resilient Distributed Dataset)?
**Answer:** Spark's core fundamental abstraction: an immutable, fault-tolerant, partitioned collection of records distributed across cluster nodes that can be operated on in parallel.

#### Q34: Differentiate Spark Transformations vs. Actions.
**Answer:**
*   **Transformations**: Lazy operations that transform an RDD/DataFrame into another (e.g., `map()`, `filter()`, `groupBy()`, `select()`). They build an execution DAG and return immediately without running computation.
*   **Actions**: Operations that trigger computation execution of the DAG and return results to Driver or write output to storage (e.g., `count()`, `collect()`, `saveAsParquet()`, `show()`).

#### Q35: What is Lazy Evaluation in Apache Spark?
**Answer:** Spark delays computing transformation steps until an Action is explicitly triggered. This allows the Catalyst Optimizer to analyze the full DAG plan, apply predicate pushdowns, project pruning, and optimize execution before executing physical tasks.

#### Q36: Explain Narrow vs. Wide Transformations in Spark.
**Answer:**
*   **Narrow Transformation**: Each input partition contributes to at most one output partition (no data shuffling across network nodes, e.g., `map()`, `filter()`).
*   **Wide Transformation**: Data from multiple input partitions must be shuffled across network nodes to compute output partitions (causes network I/O, e.g., `groupByKey()`, `reduceByKey()`, `join()`).

#### Q37: What is Data Shuffling in Spark, and why is it expensive?
**Answer:** Shuffling is the process of redistributing and writing data partitions across cluster network nodes during Wide Transformations. It involves disk serialization, network transfer I/O, and deserialization overhead, making it the primary performance bottleneck in Spark jobs.

#### Q38: What is the Spark Catalyst Optimizer?
**Answer:** The internal query optimization engine for Spark SQL and DataFrames. It converts DataFrame code into an optimized Physical Execution Plan through 4 phases:
1.  Analysis (Unresolved Logical Plan -> Resolved Logical Plan)
2.  Logical Optimization (Predicate pushdown, constant folding, column pruning)
3.  Physical Planning (Selecting join strategies)
4.  Code Generation (Tungsten bytecode generation).

#### Q39: What is Project Tungsten in Spark?
**Answer:** Spark's physical execution engine optimization component focused on hardware efficiency. It uses off-heap memory management (bypassing JVM GC), cache-aware algorithms, and explicit code generation (`whole-stage code generation`) to maximize CPU speed.

#### Q40: What is a Broadcast Join in Spark?
**Answer:** A join strategy used when joining a large DataFrame with a small DataFrame (typically < 10 MB default). Spark broadcasts (copies) the small DataFrame to all executor nodes, eliminating data shuffling of the large DataFrame across the network.

#### Q41: How do you manually force a Broadcast Join in PySpark?
**Answer:**
```python
from pyspark.sql.functions import broadcast

result_df = large_df.join(broadcast(small_df), "user_id")
```

#### Q42: What is Data Skew in Spark, and how do you handle it?
**Answer:** Data skew occurs when data is unevenly distributed across partitions (e.g., 90% of rows have `country_code = 'US'`), causing a single executor task to run significantly longer than others.
*   **Fixes**:
    1.  **Salting**: Append random integer suffixes (`0-N`) to skew keys before joins/aggregations.
    2.  **Broadcast Join**: Convert shuffle join to broadcast join.
    3.  **Adaptive Query Execution (AQE)**: Enable `spark.sql.adaptive.enabled=true` (automatically splits skewed partitions).

#### Q43: What is Adaptive Query Execution (AQE) in Spark 3.x?
**Answer:** A feature that dynamically re-optimizes physical execution plans at runtime based on actual stage metrics. Capabilities include:
1.  Dynamically coalescing shuffle partitions.
2.  Dynamically converting Sort-Merge Joins to Broadcast Hash Joins.
3.  Dynamically optimizing skewed joins.

#### Q44: Differentiate `repartition()` vs `coalesce()` in PySpark.
**Answer:**
*   `repartition(n)`: Increases or decreases the number of partitions. Performs a full shuffle across network nodes to balance partition sizes evenly.
*   `coalesce(n)`: Decreases the number of partitions by combining adjacent existing partitions on local executors without triggering a full network data shuffle.

#### Q45: Explain Spark Out-Of-Memory (OOM) errors and common solutions.
**Answer:**
*   **Driver OOM**: Occurs when calling `.collect()` on massive DataFrames or broadcasting overly large DataFrames. *Fix*: Increase driver memory or write output to disk directly instead of collecting to Driver memory.
*   **Executor OOM**: Occurs due to high data skew, large partition sizes, or excessive JVM GC pressure. *Fix*: Increase executor memory (`spark.executor.memoryOverhead`), increase partition count (`repartition`), apply salting to skewed keys.

#### Q46: What is Cache vs Persist in PySpark?
**Answer:**
*   `cache()`: Shorthand method for `persist(StorageLevel.MEMORY_AND_DISK)` in DataFrames (stores partitions in memory; spills to disk if memory is full).
*   `persist(StorageLevel)`: Allows specifying custom storage levels (e.g., `MEMORY_ONLY`, `MEMORY_ONLY_SER`, `DISK_ONLY`, `MEMORY_AND_DISK_2` for replication).

#### Q47: What is PySpark DataFrame Schema Enforcement?
**Answer:** Ensuring that ingested files match predefined column data types strictly. When reading structured formats, explicitly defining schemas (`StructType`) improves performance by avoiding extra file scanning for schema inference.

#### Q48: Write a PySpark code snippet to read Parquet data, filter rows, and write partitioned Parquet output.
**Answer:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("DataEngineeringDemo").getOrCreate()

df = spark.read.parquet("s3://my-bucket/raw-data/")

filtered_df = df.filter(col("status") == "COMPLETED") \
                .withColumn("year", col("event_date").substr(1, 4))

filtered_df.write \
    .mode("overwrite") \
    .partitionBy("year", "country") \
    .parquet("s3://my-bucket/processed-data/")
```

#### Q49: What is Spark Accumulator?
**Answer:** Shared write-only variables used to aggregate metrics/counters across executor tasks back to the Driver process (e.g., counting corrupt records encountered during processing).

#### Q50: What is Spark Broadcast Variable?
**Answer:** A read-only variable cached on each worker executor machine once, rather than transmitting a copy with every task submission, reducing network overhead for lookup tables.

#### Q51: Explain Spark Execution Memory vs Storage Memory.
**Answer:** Spark 2.x unified memory management divides memory into:
*   **Execution Memory**: Used for computation in shuffles, joins, sorts, and aggregations.
*   **Storage Memory**: Used for caching, persisting DataFrames, and internal broadcast data.
*   *Dynamic Borrowing*: When execution memory is idle, storage memory can borrow it, and vice versa.

#### Q52: What is Lineage Graph in Spark?
**Answer:** A dependency tree tracked internally for each RDD/DataFrame recording the exact sequence of transformations applied to raw data. It enables fault tolerance: if an executor node crashes and loses a partition, Spark uses the Lineage Graph to recompute only the lost partition on another node.

#### Q53: Differentiate `groupByKey()` vs `reduceByKey()` in Spark RDDs.
**Answer:**
*   `groupByKey()`: Shuffles ALL key-value pairs across the network before performing aggregation (high network I/O, prone to OOM).
*   `reduceByKey()`: Performs map-side local aggregation (combiner) on each executor node BEFORE shuffling data across the network (significantly reduces network traffic).

#### Q54: What is Whole-Stage Code Generation in Spark?
**Answer:** A Tungsten feature that collapses multiple physical operators (like filter, project, aggregate) into a single optimized Java bytecode function loop, eliminating virtual function calls and leveraging CPU registers efficiently.

#### Q55: What is UDF (User Defined Function) in PySpark, and what is its performance drawback?
**Answer:** Custom Python logic wrapped using `udf()` to transform DataFrame columns.
*   *Drawback*: PySpark UDFs force data serialization between JVM (Spark engine) and Python worker processes, bypassing Catalyst Optimizer optimizations and running significantly slower than native PySpark SQL functions (`pyspark.sql.functions`).

#### Q56: What are Vectorized UDFs (Pandas UDFs) in PySpark?
**Answer:** PySpark UDFs built using Apache Arrow to transfer data efficiently between JVM and Python workers in columnar format, using Pandas and NumPy for vectorization and running up to 100x faster than standard Python UDFs.

#### Q57: How do you read streaming data in PySpark Structured Streaming?
**Answer:**
```python
streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders-topic") \
    .load()
```

#### Q58: What is Watermarking in Spark Structured Streaming?
**Answer:** A mechanism to handle late-arriving event data in windowed streaming operations. It sets a threshold limit for how late an event can arrive relative to event time before it is dropped by the streaming engine.

#### Q59: What is Speculative Execution in Apache Spark?
**Answer:** A configuration setting (`spark.speculation=true`) where if Spark detects a task running significantly slower than the median task completion speed on a straggling node, it launches a duplicate copy of the task on another executor and accepts whichever task finishes first.

#### Q60: Explain Spark Deployment Modes: Client Mode vs Cluster Mode.
**Answer:**
*   **Client Mode**: Driver process runs locally on the host machine submitting the job (e.g., developer laptop/Jupyter notebook). If host client disconnects, job fails.
*   **Cluster Mode**: Driver process is submitted to and executes inside a worker node executor process within the cluster (production standard).

---

## 3. Data Ingestion & Event Streaming Pipelines (Q61 - Q90)

#### Q61: What is Apache Kafka?
**Answer:** An open-source distributed event streaming platform capable of handling high-throughput, real-time data feeds through a publish-subscribe durable commit log architecture.

#### Q62: Explain the core components of Apache Kafka Architecture.
**Answer:**
*   **Producer**: Application that publishes (writes) event records to Kafka topics.
*   **Broker**: Kafka cluster server node storing partitions and serving client reads/writes.
*   **Topic**: Logical category or stream name where records are published.
*   **Partition**: Ordered, immutable sequence of records stored append-only on broker disk.
*   **Consumer**: Application that subscribes to topics and processes record feeds.
*   **Consumer Group**: Group of consumers sharing topic partition processing workloads in parallel.

#### Q63: Why are Kafka Topics divided into Partitions?
**Answer:**
1.  **Scalability**: Allows a single topic's log data to scale beyond storage limits of a single broker server across multiple machines.
2.  **Parallelism**: Enables multiple consumers in a Consumer Group to read partitions concurrently.

#### Q64: How does Kafka guarantee message ordering?
**Answer:** Kafka guarantees strict message ordering **only within a single partition**, NOT across an entire multi-partition topic. Messages written with the same Partition Key (e.g., `user_id`) are routed to the exact same partition in append-only sequential order.

#### Q65: What is Consumer Group Rebalancing in Kafka?
**Answer:** The process where Kafka redistributes partition assignments among consumers in a group when a consumer joins, leaves, or crashes, ensuring all partitions remain assigned to active consumers.

#### Q66: Explain Kafka Message Delivery Guarantees.
**Answer:**
1.  **At-Most-Once**: Messages may be lost but are never re-delivered/processed twice (offsets committed before processing).
2.  **At-Least-Once**: Messages are guaranteed to be delivered, but duplicates may occur (offsets committed after processing succeeds).
3.  **Exactly-Once Processing (EOP)**: Messages are processed exactly once using transactional producers and consumer read-committed isolation levels.

#### Q67: What is the role of KRaft (Kafka Raft Metadata Mode) replacing ZooKeeper?
**Answer:** KRaft removes Kafka's external dependency on Apache ZooKeeper by managing cluster metadata consensus natively within Kafka brokers using the Raft consensus algorithm, simplifying cluster operation and scaling to millions of partitions.

#### Q68: What is In-Sync Replicas (ISR) in Kafka?
**Answer:** The subset of partition replica brokers that are actively caught up and synchronized with the leader partition broker node.

#### Q69: Explain Producer Acks (`acks=0`, `acks=1`, `acks=all` / `-1`).
**Answer:**
*   `acks=0`: Producer does not wait for broker response (highest speed, risk of data loss).
*   `acks=1`: Producer waits for Leader partition to write record to its local log.
*   `acks=all` / `-1`: Producer waits for Leader AND all In-Sync Replicas (ISR) to acknowledge record write (highest durability).

#### Q70: What is Schema Registry in Kafka ecosystem?
**Answer:** A central service that stores and serves schemas (Avro, Protobuf, JSON Schema) for Kafka topics, enabling producers and consumers to validate message compatibility and evolve schemas without breaking data pipelines.

#### Q71: Why is Apache Avro preferred for Kafka message serialization?
**Answer:** Avro is a compact, binary serialization format that enforces strict schema evolution rules and does not include field names in every message payload (uses Schema IDs), resulting in minimal network payload size.

#### Q72: What is Kafka Connect?
**Answer:** A pluggable, scalable framework for streaming data between Apache Kafka and external datastores (e.g., Kafka Connect Source to pull from PostgreSQL; Kafka Connect Sink to push into Snowflake/S3).

#### Q73: Explain Dead Letter Queue (DLQ) in streaming pipelines.
**Answer:** A designated quarantine queue/topic where unparseable, malformed, or corrupt message payloads are routed automatically so processing of valid messages can continue without crashing the pipeline.

#### Q74: Differentiate Batch Processing vs. Stream Processing.
**Answer:**
*   **Batch Processing**: High-throughput processing of static, bounded datasets at scheduled intervals (e.g., daily PySpark job).
*   **Stream Processing**: Low-latency, real-time continuous processing of unbounded event streams as data arrives (e.g., Apache Flink, Kafka Streams).

#### Q75: What is Apache Flink?
**Answer:** An open-source, stateful stream-processing framework designed for low-latency, event-driven stream analytics, featuring native event-time processing and exact-once state consistency.

#### Q76: Explain Event Time vs Processing Time vs Ingestion Time in streaming.
**Answer:**
*   **Event Time**: Timestamp when the event actually occurred on the client device (embedded in message payload).
*   **Ingestion Time**: Timestamp when Kafka broker received the event.
*   **Processing Time**: Timestamp when stream processing engine machine executes the computation step.

#### Q77: What is a Streaming Window? Explain Tumbling, Sliding, and Session Windows.
**Answer:**
*   **Tumbling Window**: Fixed-size, non-overlapping time windows (e.g., 5-minute non-overlapping blocks: 10:00-10:05, 10:05-10:10).
*   **Sliding Window**: Fixed-size, overlapping time windows evaluated at regular slide intervals (e.g., 5-minute window sliding every 1 minute).
*   **Session Window**: Dynamic time windows configured by periods of activity separated by gaps of inactivity (e.g., user activity session ending after 10 minutes of idle gap).

#### Q78: What is Backpressure in streaming systems?
**Answer:** A condition where a downstream processing stage cannot keep up with the data rate emitted by an upstream producer, causing queues to fill up. Handled by slowing down upstream producers or rate-limiting ingestion.

#### Q79: What is Log Compaction in Kafka?
**Answer:** A topic retention mechanism where Kafka retains at least the last known value for each record key within a partition, purging older updates for that same key. Useful for maintaining state snapshots (e.g., current user account balances).

#### Q80: How does Kafka achieve high-throughput IO performance?
**Answer:**
1.  **Sequential I/O**: Writes events sequentially to append-only log files on disk (avoids random disk seek overhead).
2.  **Page Cache**: Utilizes OS page cache aggressively in RAM.
3.  **Zero-Copy Memory Access**: Uses system call `sendfile` to transfer data from OS page cache directly to network socket buffer without copying to application memory space.

#### Q81: What is a Partition Key in Kafka, and how does default partitioning work?
**Answer:** A key passed with a message payload. Kafka hashes the partition key (e.g., `murmur2(key) % num_partitions`) to assign the message to a specific partition. If no key is provided, newer versions use sticky partitioning to batch records efficiently across partitions.

#### Q82: What happens if a consumer in a Consumer Group fails?
**Answer:** The Kafka Group Coordinator broker detects the missing heartbeat, marks the consumer dead, and triggers a **Group Rebalance** to reassign the dead consumer's partitions to the remaining healthy group members.

#### Q83: What is Out-of-Order Data in stream processing?
**Answer:** Streaming events that arrive at the processing engine out of chronological event-time sequence (e.g., mobile device connection delays). Handled using Watermarking and event-time window buffers.

#### Q84: Explain Change Data Capture (CDC) with Debezium and Kafka.
**Answer:** Debezium reads low-level transaction logs of databases (e.g., Postgres WAL) and converts every row mutation into structured JSON/Avro events directly streamed to Kafka topics, maintaining real-time database mirrors with zero impact on operational database performance.

#### Q85: What is Compaction vs Retention Policy in Kafka?
**Answer:**
*   **Time/Size Retention Policy**: Deletes log segments older than `retention.ms` (e.g., 7 days) or exceeding `retention.bytes`.
*   **Log Compaction Policy**: Retains the latest value per message key indefinitely, purging superseded key entries.

#### Q86: Differentiate Push-based vs Pull-based Consumers.
**Answer:**
*   **Push Consumers**: Server pushes messages to client as soon as available (e.g., RabbitMQ). Can overwhelm clients if intake rate spikes.
*   **Pull Consumers**: Client explicitly queries broker for available messages at its own pace (e.g., Kafka). Allows consumers to self-regulate processing throughput and batch requests.

#### Q87: What is Apache StreamPark / Flink CDC?
**Answer:** Integrations allowing Apache Flink to read CDC streams directly from database transaction logs without requiring intermediate Kafka broker staging, creating low-latency real-time lakehouse tables.

#### Q88: What is Idempotent Producer in Kafka?
**Answer:** Enabled via `enable.idempotence=true`. The producer sends a unique Sequence ID and Producer ID with every message, allowing the broker to detect and reject duplicate retried network requests.

#### Q89: How do you handle schema breaking changes in Schema Registry?
**Answer:** Enforce compatibility modes (e.g., `BACKWARD`, `FORWARD`, `FULL`). For breaking schema changes (like removing a mandatory field without fallback defaults), register a new topic version rather than modifying an existing incompatible topic.

#### Q90: What is KSQL / ksqlDB?
**Answer:** An event streaming database built on top of Kafka Streams that allows developers to write real-time stream processing operations (filtering, aggregations, joins) using familiar SQL syntax.
