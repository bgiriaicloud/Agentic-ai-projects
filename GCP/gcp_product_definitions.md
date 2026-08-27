# Google Cloud Platform (GCP) Product Definitions & Directory

This reference dictionary defines core Google Cloud Platform (GCP) products, their key features, use cases, and deployment contexts.

---

## 1. Compute Services

Google Cloud compute services support hosting virtual machines, running containers, and executing event-driven serverless workloads.

### Compute Engine (GCE)
* **Definition**: Infrastructure-as-a-Service (IaaS) offering virtualized server instances (VMs) running on Google’s infrastructure.
* **Key Features**: Custom machine sizing, live migration (prevents hardware maintenance downtime), preemptible/spot instances, and automatic sustained use discounts.
* **Use Cases**: Migrating legacy on-premises applications, hosting custom server clusters, and running databases that require deep OS configuration.

### Google Kubernetes Engine (GKE)
* **Definition**: A managed Kubernetes service for deploying, scaling, and managing containerized applications at scale.
* **Key Features**: Autopilot mode (fully managed cluster nodes and security baselines), node auto-repair/auto-upgrade, multi-cluster management, and integration with Cloud Logging/Monitoring.
* **Use Cases**: Cloud-native microservices architectures, orchestration of distributed container workloads, and auto-scaling APIs.

### Cloud Run
* **Definition**: A serverless compute platform that enables you to run containerized applications without managing server hosts or Kubernetes clusters.
* **Key Features**: Scales dynamically from zero to thousands of containers, pay-per-use billing (per 100ms), and custom domain bindings with automatic SSL.
* **Use Cases**: Hosting web applications, REST APIs, microservices, and background queue workers using any programming language.

### Cloud Functions
* **Definition**: Serverless Function-as-a-Service (FaaS) that executes code in response to system events without server management.
* **Key Features**: Event-driven execution (Pub/Sub triggers, Cloud Storage uploads, HTTP requests), support for multiple runtimes (Node.js, Python, Go, Java), and automated scaling.
* **Use Cases**: Processing image uploads, executing webhooks, light IoT telemetry parsing, and serverless cron jobs.

### App Engine (GAE)
* **Definition**: Platform-as-a-Service (PaaS) to deploy and scale web applications and APIs quickly in standard or flexible sandboxed runtime environments.
* **Key Features**: Automatic scaling, application versioning, split-traffic testing (canary deployments), and zero-configuration setups.
* **Use Cases**: Rapid deployment of standard web applications, mobile backends, and Python/Java/Node.js apps without managing runtime containers.

---

## 2. Networking Services

Connect cloud resources securely, route traffic globally, and secure endpoints at Google's edge.

### Virtual Private Cloud (VPC)
* **Definition**: A managed virtual network environment offering global, logically isolated networks for GCP resources.
* **Key Features**: Global scope (a single VPC can span multiple regions without external gateways), custom routing, Shared VPC (sharing networks across projects), and VPC Peering.
* **Use Cases**: Building isolated server environments, configuring cross-region server communication, and managing corporate hybrid connections.

### Cloud Load Balancing
* **Definition**: Fully managed, software-defined global and regional load balancing service that routes internet and internal traffic across computing nodes.
* **Key Features**: Single global Anycast IP address, instant scaling, autoscaling integration, and HTTPS SSL offloading.
* **Use Cases**: High-availability web applications, global website traffic distribution, and backend internal API routing.

### Cloud DNS
* **Definition**: High-performance, resilient, managed Domain Name System (DNS) service running on Google’s infrastructure.
* **Key Features**: Low latency, public and private DNS zones, integration with VPC split-horizon DNS, and scaling to millions of domains.
* **Use Cases**: Resolving internal VM hostnames privately, hosting public website domains, and routing DNS traffic.

### Cloud VPN
* **Definition**: A secure, encrypted connection linking your on-premises network to your Google Cloud VPC via IPsec VPN tunnels.
* **Key Features**: Supports classic and High-Availability (HA) VPN (99.99% SLA), static and dynamic routing using Border Gateway Protocol (BGP).
* **Use Cases**: Linking branch offices to Google Cloud networks, developer testing of hybrid setups over the internet.

### Cloud Interconnect
* **Definition**: Dedicated, high-speed physical connection linking on-premises network systems directly to Google's physical network edge.
* **Key Features**: High bandwidth (10 Gbps or 100 Gbps circuits), lower network latency, and bypassed public internet routing.
* **Use Cases**: Large-scale data ingestion, high-speed real-time databases synchronization, and large enterprise hybrid clouds.

### Cloud Armor
* **Definition**: Security service offering Web Application Firewall (WAF) and distributed denial-of-service (DDoS) protection at Google's network edge.
* **Key Features**: IP whitelist/blacklist, SQL injection and Cross-Site Scripting (XSS) pre-configured rules, and deep integration with HTTP(S) Load Balancer.
* **Use Cases**: Protecting public-facing web applications from OWASP Top 10 vulnerabilities and mitigating massive volumetric DDoS attacks.

---

## 3. Storage Services

Scalable block, object, and file storage systems for virtual machines and databases.

### Cloud Storage (GCS)
* **Definition**: High-performance, globally distributed object storage service for unstructured data.
* **Key Features**: Standard, Nearline, Coldline, and Archive storage tiers, lifecycle policies for automated tiering, object versioning, and unified APIs.
* **Use Cases**: Storing media assets, backups, log repositories, and loading datasets for big data analytics.

### Persistent Disk
* **Definition**: Reliable, high-performance block storage volumes attached to Compute Engine and GKE container instances.
* **Key Features**: Standard HDD, balanced SSD, and extreme performance SSD SKUs, multi-writer mode, and online resizing without downtime.
* **Use Cases**: VM boot drives, transactional database storage, and shared read-only disk volumes.

### Filestore
* **Definition**: Managed Network Attached Storage (NAS) file share service supporting the standard Network File System (NFS) protocol.
* **Key Features**: Low latency, high IOPS, support for shared read-write access from thousands of client VMs.
* **Use Cases**: Hosting legacy enterprise applications, sharing media files, and active CMS directories (WordPress/Drupal).

---

## 4. Database Services

Managed SQL and NoSQL engines designed for scale and low administrative overhead.

### Cloud SQL
* **Definition**: Fully managed relational database service supporting MySQL, PostgreSQL, and SQL Server.
* **Key Features**: Automated backups, read-replicas, automatic failover (HA setups), and integration with Cloud IAM for authentication.
* **Use Cases**: E-commerce transactional backends, standard CRM/ERP systems, and standard relational applications.

### Cloud Spanner
* **Definition**: Enterprise-grade, globally distributed relational database offering high scalability with strong transactional consistency.
* **Key Features**: Unlimited horizontal scaling (shares data across nodes), multi-region replication, SQL querying, and 99.999% SLA availability.
* **Use Cases**: Global financial transaction systems, inventory supply chain management, and high-volume billing platforms.

### Cloud Bigtable
* **Definition**: Scalable, fully managed wide-column NoSQL database engine designed for massive write/read throughput at sub-millisecond latencies.
* **Key Features**: Seamless scalability to petabytes of data, single-digit millisecond latency, and integration with open-source HBase APIs.
* **Use Cases**: IoT telemetry ingestion, ad-tech clickstream analytics, financial market data streaming, and fraud detection.

### Firestore
* **Definition**: Serverless document-based NoSQL database designed for building web, mobile, and IoT applications.
* **Key Features**: Real-time data synchronization, offline database support, auto-scaling, and hierarchical document data modeling.
* **Use Cases**: Mobile user profile storage, real-time gaming leaderboards, and collaborative document apps.

---

## 5. Security & Operations Services

Manage access control, audit activity logs, monitor resource metrics, and encrypt data.

### Cloud IAM (Identity & Access Management)
* **Definition**: Access control service defining permissions and access rights on GCP resource scopes for service accounts and users.
* **Key Features**: Role-based access control (Basic, Predefined, and Custom roles), IAM policy evaluation, and audit logs.
* **Use Cases**: Delegating administrative control, securing cloud API access, and organizing project permissions.

### Secret Manager
* **Definition**: Centralized secure storage service for safeguarding credentials, API keys, passwords, and database connection strings.
* **Key Features**: Automatic versioning, access policy controls, audit logs, and integration with Cloud Build and Cloud Run.
* **Use Cases**: Application credentials rotation, API token injection in pipelines, and database password lifecycle management.

### Cloud Monitoring & Logging (GCP Operations Suite)
* **Definition**: Operations dashboard providing diagnostic logging, performance metrics tracking, and alerting across resources.
* **Key Features**: Log query search engine, metric dashboard builder, alert rules routing to email/webhooks, and trace analytics.
* **Use Cases**: Centralizing VM syslog logs, diagnosing backend response times, and firing alerts when systems fail.
