# Cloud Architect 250 Interview Questions & Answers - Part 2

This is Volume 2 of the Cloud Architect Interview Guide, containing **Questions 91 to 170**. It covers Cloud Networking, Hybrid Interconnectivity, Cloud Storage, Databases, and Enterprise Data Architectures.

---

## 📋 Table of Contents (Part 2)
1.  [Cloud Networking & Security Perimeters (Q91 - Q130)](#1-cloud-networking--security-perimeters-q91---q130)
2.  [Cloud Storage, Databases & Data Engineering (Q131 - Q170)](#2-cloud-storage-databases--data-engineering-q131---q170)

---

## 1. Cloud Networking & Security Perimeters (Q91 - Q130)

#### Q91: What is a Virtual Private Cloud (VPC) in Cloud Computing?
**Answer:** A VPC is a logically isolated virtual network patch within a public cloud provider's network, allowing you to define IP ranges, subnets, routers, firewalls, and route tables to connect compute resources securely.

#### Q92: Explain the difference between default and custom VPCs.
**Answer:** 
*   **Default VPC**: Pre-provisioned subnets in every region with permissive default firewall rules (e.g. allowing all internal traffic), which is unsuitable for production.
*   **Custom VPC**: You define subnets, IP allocations, routing rules, and strict firewall configurations from scratch.

#### Q93: What is a Subnet?
**Answer:** A subdivision of a VPC network's IP address range associated with a specific region, allowing you to group and isolate VMs or containers.

#### Q94: What is the difference between Public Subnets and Private Subnets?
**Answer:** 
*   **Public**: Resources in this subnet have external public IPs and routes to an Internet Gateway, allowing inbound and outbound internet access.
*   **Private**: Resources have only internal private IPs and no direct route to the internet, blocking incoming connections.

#### Q95: Explain what a CIDR block is.
**Answer:** Classless Inter-Domain Routing (CIDR) is a notation format (e.g., `10.0.0.0/16`) that defines an IP address range. The number after the slash indicates how many bits are allocated for the network routing prefix.

#### Q96: What is a Router, and what is its role in a VPC?
**Answer:** A logical networking component that routes traffic between subnetworks, across VPC peer connections, or through VPN tunnels to external networks.

#### Q97: Explain what a NAT Gateway (e.g., Cloud NAT) is.
**Answer:** Network Address Translation (NAT) allows private subnet VMs without public IPs to connect outbound to the internet for updates or API calls, while blocking incoming internet connections from initiating sessions.

#### Q98: What is the difference between static and dynamic IP addresses?
**Answer:** 
*   **Static**: A persistent IP address reserved for a resource that remains constant even if the resource restarts.
*   **Dynamic**: An IP assigned automatically from a pool that can change whenever the resource is power-cycled.

#### Q99: What is Google Cloud DNS?
**Answer:** A highly available, low-latency domain name system (DNS) service that translates domain names (e.g. `example.com`) into IP addresses.

#### Q100: Explain the difference between Split-Brain DNS and standard DNS.
**Answer:** Split-Brain DNS serves different DNS answers to queries depending on where the query originates (e.g. returning a private IP for queries inside the VPC and a public IP for internet queries).

#### Q101: What is VPC Network Peering?
**Answer:** A connection that links two VPCs privately, allowing resources in both networks to communicate using internal IPs with low latency. (Non-transitive and cannot have overlapping subnets).

#### Q102: What is a Shared VPC Host Project vs Service Project?
**Answer:** 
*   **Host Project**: Manages the core Shared VPC network, subnets, VPN connections, and firewalls.
*   **Service Projects**: Projects linked to the Host Project that deploy compute instances using the Shared VPC subnets without permissions to alter the network configuration.

#### Q103: Explain Private Google Access (PGA).
**Answer:** A subnet-level feature that allows virtual machines that only have private IP addresses to access Google Cloud APIs and services over their internal IPs.

#### Q104: What is Private Service Connect (PSC)?
**Answer:** A GCP feature that allows private, secure consumption of services (like managed SaaS or Google APIs) across different VPCs using internal IP addresses, without requiring VPC Peering.

#### Q105: What is Cloud Interconnect?
**Answer:** A high-bandwidth physical connection between on-premises networks and Google's network:
*   **Dedicated Interconnect**: Direct fiber connection at a Google colocation facility (10G/100G).
*   **Partner Interconnect**: Connection through a supported network service provider (50M to 50G).

#### Q106: Explain High Availability (HA) VPN.
**Answer:** High Availability (HA) VPN provides a 99.99% service availability SLA. It uses a single gateway with two external interfaces, creating two independent IPsec tunnels to peer gateways using dynamic routing with BGP.

#### Q107: What is BGP (Border Gateway Protocol)?
**Answer:** A routing protocol used to exchange routing information dynamically between routers in different autonomous networks (commonly used with Cloud VPN and Interconnect).

#### Q108: What are VPC Service Controls (VPC-SC)?
**Answer:** VPC-SC allows defining a security perimeter around multi-tenant Google APIs (Cloud Storage, BigQuery, Vertex AI) to prevent data exfiltration by blocking access requests from outside the perimeter.

#### Q109: Explain the difference between ingress and egress firewall rules.
**Answer:** 
*   **Ingress**: Rules that control incoming traffic to resources within the network.
*   **Egress**: Rules that control outgoing traffic from resources within the network.

#### Q110: What is a Global Load Balancer vs. Regional Load Balancer?
**Answer:** 
*   **Global**: Distributes traffic across backends globally using a single external IP address.
*   **Regional**: Distributes traffic within a single region, providing regional isolation.

#### Q111: Explain SSL Offloading (SSL Termination) on Load Balancers.
**Answer:** Decrypting incoming SSL/TLS encrypted traffic at the load balancer level before forwarding the unencrypted HTTP requests to backend servers, reducing processor load on the backend.

#### Q112: What is Session Affinity (Sticky Sessions) in load balancing?
**Answer:** A setting that routes all sequential requests from a specific user session to the same backend server, which is useful for stateful applications.

#### Q113: What is a Health Check in Load Balancers?
**Answer:** Periodic probes sent by the load balancer to backend servers to verify they are responsive; unresponsive servers are removed from the routing pool.

#### Q114: What is Google Cloud CDN?
**Answer:** A globally distributed network of edge cache nodes that caches static web assets close to users, reducing latency and load on origin servers.

#### Q115: What is an Edge Cache PoP (Point of Presence)?
**Answer:** A physical location where Google connects its network to the rest of the internet, hosting CDN caches and routing user traffic into the Google backbone.

#### Q116: Explain "BGP ASN" (Autonomous System Number).
**Answer:** A unique identifier assigned to an autonomous system of routers (like your corporate network or Google's network) to exchange routing paths using BGP.

#### Q117: What is a "ProxyOnly" subnet in GCP?
**Answer:** A dedicated subnet containing proxy IP addresses used by Google's Regional Internal HTTP(S) Load Balancers to communicate with backend instances.

#### Q118: What is dynamic routing in GCP VPC networks?
**Answer:** A configuration (regional or global) that enables Cloud Routers to automatically discover and propagate IP prefix changes across subnets and VPN tunnels.

#### Q119: What is the risk of overlapping IP subnets when planning hybrid cloud connections?
**Answer:** Overlapping subnets cause IP conflicts, preventing routers from determining the correct destination for traffic, resulting in dropped packets.

#### Q120: How does a "Service Directory" support cloud networking?
**Answer:** It provides a central, private registry to catalog, manage, and resolve internal service endpoints across different platforms and networks.

#### Q121: What is a Web Application Firewall (WAF)?
**Answer:** A security tool (like Cloud Armor) that monitors and filters HTTP/HTTPS traffic to defend web applications from OWASP Top 10 exploits, SQL injections, and DDoS attacks.

#### Q122: What is IP Masquerading?
**Answer:** A form of NAT that translates multiple internal IP addresses to a single public IP address to hide internal network topologies.

#### Q123: Explain what "Latency-Based Routing" is.
**Answer:** A DNS routing policy that resolves domain names to the IP address of the data center region that provides the lowest network latency for the querying user.

#### Q124: What is the difference between TCP and UDP protocols?
**Answer:** 
*   **TCP**: A connection-oriented protocol that guarantees delivery and packet ordering, which is ideal for web traffic.
*   **UDP**: A connectionless protocol that sends packets without verifying delivery, providing low latency for streaming and gaming.

#### Q125: What is MTU (Maximum Transmission Unit)?
**Answer:** The size of the largest packet (in bytes) that can be transmitted over a network interface without fragmentation (default VPC MTU is usually 1460 or 1500 bytes).

#### Q126: What is a "Static Route"?
**Answer:** A manual route rule defined in a VPC table that specifies the exact gateway or next-hop IP for a destination prefix.

#### Q127: Explain "Network Virtual Appliances" (NVAs).
**Answer:** Virtual machines running third-party firewall, routing, or load balancing software (e.g., F5, Palo Alto) deployed inside a VPC to handle custom traffic rules.

#### Q128: What is VPC Flow Logs?
**Answer:** A monitoring feature that records network traffic telemetry (IP addresses, ports, protocols, packet counts) passing through subnet interfaces for audit and troubleshooting.

#### Q129: Explain the difference between public and private DNS zones.
**Answer:** 
*   **Public**: DNS zones accessible from the internet.
*   **Private**: DNS zones accessible only to resources connected inside a specific VPC network.

#### Q130: What is a "Direct Peering" connection?
**Answer:** A private network peering connection established between Google's edge routers and an enterprise network without going through a public exchange or VPN.

---

## 2. Cloud Storage, Databases & Data Engineering (Q131 - Q170)

#### Q131: What is Object Storage, and what are its key characteristics?
**Answer:** A storage architecture that manages data as objects (combining data, metadata, and a globally unique identifier) in flat namespaces called buckets, offering virtually infinite scale.

#### Q132: Explain Google Cloud Storage (GCS) storage classes.
**Answer:** 
*   **Standard**: Highly active data accessed frequently.
*   **Nearline**: Infrequently accessed data (once a month).
*   **Coldline**: Rarely accessed data (once a quarter).
*   **Archive**: Long-term backup data (once a year) with high retrieval costs.

#### Q133: What is a GCS Lifecycle Policy?
**Answer:** A set of rules that automatically transitions files to cheaper storage classes or deletes them after a certain timeframe (e.g., moving files to Archive after 90 days).

#### Q134: Explain the difference between Relational (SQL) and Non-Relational (NoSQL) databases.
**Answer:** 
*   **Relational**: Structured schemas with tables, rows, and relationships, supporting ACID transactions.
*   **NoSQL**: Flexible schemas (key-value, document, column-family) designed for massive scale and horizontal partitioning.

#### Q135: What are ACID properties in database transactions?
**Answer:** **A**tomicity (all or nothing), **C**onsistency (valid states), **I**solation (concurrent isolation), and **D**urability (survives crashes).

#### Q136: Explain Cloud SQL.
**Answer:** A fully managed relational database service on Google Cloud that supports MySQL, PostgreSQL, and SQL Server databases.

#### Q137: What is Google Cloud Spanner?
**Answer:** A enterprise relational database service that scales horizontally across regions, providing strong consistency, schema management, and ACID transactions globally.

#### Q138: Explain how Cloud Spanner achieves global scale with consistency.
**Answer:** By using Google's network backbone and synchronized GPS atomic clocks (TrueTime API) to order transactions globally.

#### Q139: What is Google Cloud Firestore?
**Answer:** A fully managed, serverless, document-oriented NoSQL database designed for web and mobile application synchronization.

#### Q140: What is Google Cloud Bigtable?
**Answer:** A high-performance, wide-column NoSQL database service designed to handle massive analytical workloads with sub-millisecond latencies.

#### Q141: What is a Data Warehouse, and how does it differ from an OLTP database?
**Answer:** 
*   **Data Warehouse** (OLAP): Optimized for complex analytical queries across massive historical datasets, using columnar storage.
*   **OLTP Database**: Optimized for high-frequency, low-latency read/write transactional operations.

#### Q142: What is Google BigQuery?
**Answer:** A fully managed, serverless, multi-cloud enterprise data warehouse designed to run SQL queries across petabytes of data.

#### Q143: Explain Table Partitioning in BigQuery.
**Answer:** Segmenting a table into smaller partitions based on date, timestamp, or integer columns to optimize queries by scanning only relevant data, reducing costs.

#### Q144: Explain Table Clustering in BigQuery.
**Answer:** Sorting and organizing table rows based on specific columns to speed up query execution and reduce costs when filtering by those columns.

#### Q145: What is the difference between ETL and ELT?
**Answer:** 
*   **ETL (Extract, Transform, Load)**: Data is transformed on a staging server before being loaded into the warehouse.
*   **ELT (Extract, Load, Transform)**: Raw data is loaded directly into the warehouse, leveraging the warehouse's compute engine to run transformations.

#### Q146: What is a Data Lake?
**Answer:** A centralized repository that stores raw, unstructured, semi-structured, and structured data at any scale for machine learning and analytical pipelines.

#### Q147: Explain the concept of "Data Mesh."
**Answer:** An architectural framework that organizes data ownership by business domains, treating data as a product managed by individual teams.

#### Q148: What is Cloud Dataflow?
**Answer:** A fully managed runner service for unified batch and stream data processing pipelines based on the Apache Beam framework.

#### Q149: What is Cloud Dataproc?
**Answer:** A fully managed cloud service for running Apache Spark, Flink, and Hadoop clusters on-demand.

#### Q150: What is Cloud Composer?
**Answer:** A fully managed workflow orchestration service built on Apache Airflow used to schedule and monitor data pipeline stages.

#### Q151: Explain the difference between batch and streaming data processing.
**Answer:** 
*   **Batch**: Processing static data collections collected over a time window.
*   **Streaming**: Processing continuous, real-time data streams instantly as they arrive.

#### Q152: What is a "Write-Ahead Log" (WAL)?
**Answer:** A database log where changes are recorded before being written to the database files, ensuring durability and recovery after crashes.

#### Q153: What is Database Replication?
**Answer:** Copying database records dynamically to secondary replica servers to provide high availability and balance read traffic.

#### Q154: Explain the difference between synchronous and asynchronous database replication.
**Answer:** 
*   **Synchronous**: The primary database waits for confirmation from replicas before completing a write, guaranteeing consistency but increasing latency.
*   **Asynchronous**: The primary writes data instantly and pushes changes to replicas in the background, offering lower latency but introducing replication lag.

#### Q155: What is Database Sharding?
**Answer:** Horizontal partitioning of a database table across multiple independent database instances to scale write throughput.

#### Q156: Explain "Object Versioning" in GCS.
**Answer:** A configuration that retains older versions of objects when they are overwritten or deleted, protecting against accidental data loss.

#### Q157: What is a Signed URL in object storage?
**Answer:** A URL that provides temporary read or write permissions to a specific object without requiring GCP credentials or identity authentication.

#### Q158: Explain the difference between OLTP and OLAP workloads.
**Answer:** 
*   **OLTP (Online Transaction Processing)**: High volume of quick, row-level database transactions (e.g., shopping carts).
*   **OLAP (Online Analytical Processing)**: Complex query operations across columns and tables for business intelligence.

#### Q159: What is "Columnar Storage," and why do analytical databases use it?
**Answer:** Columnar storage saves table columns together on disk instead of rows, allowing queries to scan only the requested columns, reducing disk read overhead.

#### Q160: What is a database schema migration tool?
**Answer:** A utility (like Liquibase or Flyway) that manages, versions, and deploys incremental database schema changes using code scripts.

#### Q161: What is "Point-in-Time Recovery" (PITR) in databases?
**Answer:** A feature that allows you to restore a database to its exact state at any specific second in the past by restoring backup snapshots and applying transaction logs.

#### Q162: What is "Data Governance"?
**Answer:** A framework that defines the policies, access controls, compliance rules, and data quality standards within an organization.

#### Q163: Explain what a "Schema Registry" is in event-driven systems.
**Answer:** A service that manages schemas for event messages (e.g., using Avro or Protobuf), ensuring that publishers and subscribers agree on message formats.

#### Q164: What is "Cold Storage" retrieval latency?
**Answer:** The delay before data stored in archive classes can be read (which ranges from milliseconds in GCS to hours in traditional cloud archives).

#### Q165: What is database connection exhaustion, and how do you prevent it?
**Answer:** An error that occurs when a database run out of slots to accept new connections, preventing apps from querying data. Prevent it using connection pool managers.

#### Q166: What is a Read Replica?
**Answer:** A read-only copy of a primary database that handles read queries to offload traffic from the primary instance.

#### Q167: Explain "Write Amplification" in NoSQL databases.
**Answer:** An effect where a single logical database update triggers multiple physical writes to disk due to index updates or replication tasks.

#### Q168: What is a "Data Catalog"?
**Answer:** A fully managed metadata management service that helps users discover, classify, and manage data assets across cloud systems.

#### Q169: What is "Partition Pruning"?
**Answer:** A database query execution optimization where the engine skips scanning partitions that do not match the query filters, reducing scanned data.

#### Q170: Explain "Row-Level Security" (RLS).
**Answer:** A security configuration that restricts access to specific rows in a database table based on the identity of the querying user.
