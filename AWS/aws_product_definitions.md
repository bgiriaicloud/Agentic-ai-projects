# Amazon Web Services (AWS) Product Definitions & Directory

This reference dictionary defines core Amazon Web Services (AWS) products, their key features, use cases, and deployment contexts.

---

## 1. Compute Services

AWS compute services support hosting virtual machines, running containers, and executing serverless scripts.

### Elastic Compute Cloud (EC2)
* **Definition**: Infrastructure-as-a-Service (IaaS) offering resizable virtualized servers (Instances) running on AWS physical infrastructure.
* **Key Features**: Customizable instance types (CPU, RAM, GPUs), AMI (Amazon Machine Image) templates, Auto Scaling Groups (ASG), and Spot/Reserved billing options.
* **Use Cases**: Legacy migration (lift-and-shift), custom databases, high-performance computing, and environments requiring full OS root access.

### Elastic Kubernetes Service (EKS)
* **Definition**: A managed Kubernetes service for deploying, scaling, and managing containerized applications on AWS.
* **Key Features**: Multi-AZ control plane scaling, integration with AWS IAM for authentication, support for Fargate serverless containers, and integration with AWS VPC.
* **Use Cases**: Microservices orchestration, cloud-native containerized applications, and multi-cloud container infrastructure.

### AWS Lambda
* **Definition**: Serverless Function-as-a-Service (FaaS) that executes code in response to system events without server provisioning.
* **Key Features**: Automated scaling, pay-per-millisecond billing, support for multiple runtimes (Node.js, Python, Java, Go), and event integration with S3, DynamoDB, and API Gateway.
* **Use Cases**: Image and file processing on upload, backend API integrations, real-time file parsing, and serverless background cron jobs.

### AWS App Runner
* **Definition**: A fully managed serverless hosting platform for containerized web applications and APIs.
* **Key Features**: Direct deployment from source control (GitHub) or container registry (ECR), automatic load balancing, auto-scaling, and managed SSL certificates.
* **Use Cases**: Hosting web applications, REST APIs, and microservices backends without managing VPCs, container orchestrators, or servers.

### Elastic Container Service (ECS) & AWS Fargate
* **Definition**:
  - **ECS**: A highly scalable, high-performance container orchestration service.
  - **Fargate**: A serverless compute engine for containers that works with both ECS and EKS.
* **Key Features**: Fargate eliminates VM node management; users only define CPU and memory limits per task. Integrates with ALB.
* **Use Cases**: Scaling microservice APIs, running containerized batch jobs, and running backend microservices.

---

## 2. Networking Services

Connect cloud resources securely, route traffic globally, and secure endpoints at AWS's edge.

### Virtual Private Cloud (VPC)
* **Definition**: A logically isolated virtual network dedicated to your AWS account, allowing you to launch AWS resources in a defined virtual network.
* **Key Features**: Custom subnets (public and private), Route Tables, Internet Gateways (IGW), NAT Gateways, VPC Peering, and VPC Flow Logs.
* **Use Cases**: Building secure private networks, hosting database servers, and creating hybrid enterprise connections.

### Elastic Load Balancing (ELB)
* **Definition**: A service that automatically distributes incoming application traffic across multiple targets (EC2 instances, containers, IP addresses).
* **Key Features**: 
  - **Application Load Balancer (ALB)**: Layer 7 load balancing (HTTP/HTTPS routing based on path/host).
  - **Network Load Balancer (NLB)**: Layer 4 load balancing (ultra-high performance, static IP, TCP/UDP).
* **Use Cases**: High-availability web applications, routing microservice endpoints, and handling high-performance TCP traffic.

### Route 53
* **Definition**: A highly available and scalable cloud Domain Name System (DNS) web service.
* **Key Features**: Domain registration, health checks, latency-based routing, Geo-Proximity routing, failover routing, and private DNS zones for VPCs.
* **Use Cases**: Public DNS management, routing internet traffic to ELB endpoints, and hosting internal private subnets hostnames.

### Transit Gateway
* **Definition**: A central hub that connects VPCs and on-premises networks, simplifying network topologies by replacing mesh VPC peering arrangements.
* **Key Features**: Centralized route management, transitive routing, and simplified VPN/Direct Connect attachments across multiple AWS accounts.
* **Use Cases**: Large-scale enterprise multi-account networking, hub-and-spoke configurations.

### Amazon CloudFront
* **Definition**: A fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency.
* **Key Features**: Global edge locations, dynamic and static caching, SSL/TLS acceleration, and integration with AWS WAF and AWS Shield.
* **Use Cases**: Caching static web assets, accelerating API endpoints, and streaming video contents.

---

## 3. Storage Services

Scalable block, object, and file storage systems.

### Simple Storage Service (S3)
* **Definition**: An object storage service offering industry-leading scalability, data availability, security, and performance.
* **Key Features**: S3 Standard, Intelligent-Tiering, Glacier Flexible, and Glacier Deep Archive tiers, lifecycle policies, versioning, object locks, and replication.
* **Use Cases**: Backup and restore, media hosting, data lakes, and static website hosting.

### Elastic Block Store (EBS)
* **Definition**: High-performance block storage volumes designed for use with EC2 instances.
* **Key Features**: GP2/GP3 (General Purpose SSD), IO1/IO2 (Provisioned IOPS), snapshots (stored in S3), and online capacity modifications.
* **Use Cases**: VM boot volumes, database storage volumes, and transactional block-level storage.

### Elastic File System (EFS)
* **Definition**: Fully managed, serverless, elastic NFS file system that can be shared across thousands of EC2 instances and containers.
* **Key Features**: Standard and Infrequent Access storage classes, POSIX-compliant file system permissions, and dynamic scaling.
* **Use Cases**: Enterprise file shares, active web server directories (CMS assets), and container persistent storage.

---

## 4. Database Services

Managed relational, key-value, and in-memory databases.

### Relational Database Service (RDS) & Aurora
* **Definition**:
  - **RDS**: Managed relational databases supporting PostgreSQL, MySQL, MariaDB, Oracle, and SQL Server.
  - **Aurora**: A cloud-native relational database engine (MySQL/PostgreSQL compatible) designed for the cloud.
* **Key Features**: Automated backups, multi-AZ deployment (high availability), read-replicas, and automatic storage scaling. Aurora offers 5x speed of standard MySQL.
* **Use Cases**: Transactional e-commerce backends, enterprise apps, and standard SQL query workloads.

### DynamoDB
* **Definition**: A fully managed, serverless, multi-region key-value and document NoSQL database.
* **Key Features**: Single-digit millisecond response times at any scale, automatic partitioning, global tables (multi-region active-active replication), and on-demand capacity scaling.
* **Use Cases**: Shopping carts, user profile stores, mobile backends, and high-frequency real-time web configurations.

---

## 5. Security & Operations Services

Manage access control, audit activity logs, monitor resource metrics, and encrypt data.

### AWS IAM (Identity & Access Management)
* **Definition**: Securely manage access to AWS services and resources by creating users, groups, and roles with fine-grained permissions.
* **Key Features**: Policy-based access controls, IAM roles for EC2/service authorization, multi-factor authentication (MFA), and Access Analyzer.
* **Use Cases**: Restricting console access, managing service credentials, and configuring resource-level permissions.

### Secrets Manager
* **Definition**: Helps you protect secrets needed to access applications, services, and IT resources.
* **Key Features**: Centralized database credentials rotation, API keys storage, fine-grained access policies, and integration with AWS CloudFormation and ECS.
* **Use Cases**: Automatic rotation of database passwords, secure API keys retrieval at runtime.

### CloudWatch & CloudTrail
* **Definition**:
  - **CloudWatch**: Monitoring and management service providing operational data (metrics, logs, alarms).
  - **CloudTrail**: Governance and compliance tool that records API actions and user activity across your AWS account.
* **Use Cases**: Monitoring server CPU usage, aggregating application log streams, configuring alarms, and auditing API deletions for security.
