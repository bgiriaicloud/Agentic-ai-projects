# Azure Service Definitions & Directory

A comprehensive reference dictionary defining core Microsoft Azure services, their key features, use cases, and architectural contexts.

---

## 1. Compute Services

Compute services provide virtualized hosting environments for running applications, background jobs, and container workloads.

### Azure Virtual Machines (VM)
* **Definition**: Infrastructure-as-a-Service (IaaS) offering providing on-demand, customizable virtualized computing resources (Windows or Linux).
* **Key Features**: Supports custom OS images, scale-up capability, extension management (monitoring, scripting), and integration with virtual networks.
* **Use Cases**: Legacy application migrations (lift-and-shift), dev/test environments, and hosting custom server software.

### Azure App Service
* **Definition**: Platform-as-a-Service (PaaS) for hosting web applications, RESTful APIs, and mobile backends.
* **Key Features**: Built-in support for multiple stacks (.NET, Java, Node.js, Python, PHP), auto-scaling, deployment slots, custom domains, and SSL bindings.
* **Use Cases**: Hosting high-availability web applications and microservice backends without managing the underlying OS.

### Azure Functions
* **Definition**: Serverless Compute-as-a-Service (FaaS) that executes code on-demand in response to events.
* **Key Features**: Pay-per-execution billing (Consumption Plan), automatic event-driven scaling, and bindings to integrate with other Azure services.
* **Use Cases**: Scheduled cron jobs, image processing on file uploads, webhooks, and lightweight API endpoints.

### Azure Kubernetes Service (AKS)
* **Definition**: A fully managed Kubernetes service for deploying, scaling, and managing containerized applications.
* **Key Features**: Automated Kubernetes patches, control-plane managed by Azure free of charge, tight integration with Entra ID, and integration with Azure Container Registry (ACR).
* **Use Cases**: Hosting microservices architectures, cloud-native containerized applications, and DevOps CI/CD pipelines.

### Azure Container Apps (ACA)
* **Definition**: A managed serverless platform for containerized applications and microservices built on top of Kubernetes (without managing Kubernetes).
* **Key Features**: Scaling to zero, integration with Dapr (Distributed Application Runtime) and KEDA (Kubernetes Event-driven Autoscaling).
* **Use Cases**: Building microservices, serverless API backends, and background event processors.

### Azure Virtual Machine Scale Sets (VMSS)
* **Definition**: A group of load-balanced, identical virtual machines that scale automatically up or down.
* **Key Features**: Integrated with Azure Load Balancer or Application Gateway, supports spot instances, and offers auto-scaling rules.
* **Use Cases**: Big compute, large scale workloads, and container platforms.

---

## 2. Networking Services

Networking services connect cloud resources securely to each other, to hybrid sites, and to the public internet.

### Azure Virtual Network (VNet)
* **Definition**: The fundamental building block for private networks in Azure, allowing secure communication between resources, the internet, and on-premises systems.
* **Key Features**: Customizable IP address spaces, subnet segmentation, custom Route Tables (UDRs), and VNet Peering.
* **Use Cases**: Creating isolated network environments, hosting VMs, and establishing hybrid clouds.

### Azure Load Balancer
* **Definition**: Layer 4 (TCP/UDP) load balancer that distributes incoming traffic across backend VM instances.
* **Key Features**: High availability, health probes, inbound NAT rules, and supports public or internal traffic routing.
* **Use Cases**: Distributing traffic to VM pools, high-availability web architectures.

### Azure Application Gateway
* **Definition**: Layer 7 web traffic load balancer and reverse proxy that includes Web Application Firewall (WAF) capabilities.
* **Key Features**: URL path-based routing, SSL termination, cookie-based affinity, and multi-site hosting.
* **Use Cases**: Managing traffic to web apps, securing public-facing web servers with WAF.

### Azure Front Door
* **Definition**: A global, scalable entry-point that uses the Microsoft global edge network to deliver secure, high-performance web applications.
* **Key Features**: Global HTTP load balancing, SSL offloading, global WAF, and edge caching (CDN).
* **Use Cases**: Multi-region web applications, latency-sensitive global sites, and API routing.

### Azure VPN Gateway
* **Definition**: A virtual network gateway used to send encrypted traffic between an Azure VNet and an on-premises location.
* **Key Features**: Supports Site-to-Site (IPsec), Point-to-Site (client VPN), and VNet-to-VNet connectivity.
* **Use Cases**: Secure branch office connections to the cloud, developer remote access.

### Azure ExpressRoute
* **Definition**: Dedicated, private, high-speed physical network connections between on-premises datacenters and Azure.
* **Key Features**: Bypasses the public internet, offers bandwidth up to 100 Gbps, and provides lower latency and higher security.
* **Use Cases**: Large-scale data migration, real-time data sync, and high-security hybrid enterprise connections.

### Azure Bastion
* **Definition**: A fully managed PaaS service that provides secure, seamless RDP and SSH access to VMs directly through the Azure portal over SSL.
* **Key Features**: No public IP required on target VMs, browser-based console access, and eliminates the need for exposed jumpboxes.
* **Use Cases**: Administrative access to private subnet VMs without internet exposure.

---

## 3. Storage Services

Azure Storage provides secure, durable, scalable, and highly available cloud storage.

### Azure Blob Storage
* **Definition**: Object storage optimized for storing massive amounts of unstructured data (files, images, backups).
* **Key Features**: Hot, Cool, Cold, and Archive storage tiers, life-cycle management rules, and immutability settings.
* **Use Cases**: Storing images, documents, static website assets, log files, and database backups.

### Azure Files
* **Definition**: Fully managed cloud file shares accessible via the industry-standard SMB or NFS protocols.
* **Key Features**: Simultaneous mount access, Azure File Sync to cache shares on on-premises Windows Servers.
* **Use Cases**: Migrating legacy on-premises file shares to the cloud, sharing configuration files across VMs.

### Azure Disk Storage
* **Definition**: Managed block-level storage volumes for Azure Virtual Machines.
* **Key Features**: Available in Standard HDD, Standard SSD, Premium SSD (v1/v2), and Ultra Disk SKUs.
* **Use Cases**: Operating system disks, database storage, and high-IOPS transactional applications.

---

## 4. Database Services

Managed databases minimize the operational overhead of setting up, maintaining, and scaling engines.

### Azure SQL Database
* **Definition**: Fully managed relational database engine based on Microsoft SQL Server.
* **Key Features**: Automatic tuning, serverless scaling, active geo-replication, point-in-time restores, and built-in HA.
* **Use Cases**: Enterprise SaaS databases, transaction-heavy web applications.

### Azure Cosmos DB
* **Definition**: Globally distributed, multi-model NoSQL database service designed for low-latency applications at any scale.
* **Key Features**: Supports SQL (Core), MongoDB, Cassandra, Gremlin, and Table APIs, guaranteed single-digit millisecond latency, and multi-region replication.
* **Use Cases**: IoT telemetry ingestion, gaming leaderboards, real-time personalization, and e-commerce shopping carts.

### Azure Cache for Redis
* **Definition**: In-memory data store service based on open-source Redis software.
* **Key Features**: Sub-millisecond latency, data clustering, active-passive geodistribution, and high throughput.
* **Use Cases**: Web application session caching, database query caching, and message broker backends.

---

## 5. Identity & Security Services

These services manage access permissions, protect resources, and detect advanced threats.

### Microsoft Entra ID (Formerly Azure Active Directory)
* **Definition**: Cloud-based identity and access management service.
* **Key Features**: Single Sign-On (SSO), Multi-Factor Authentication (MFA), Conditional Access policies, and guest access lifecycle.
* **Use Cases**: User identity control, integration with external SaaS apps, and resource authorization.

### Azure Key Vault
* **Definition**: A secure, centralized cloud service for safeguarding cryptographic keys, secrets (passwords/API keys), and SSL certificates.
* **Key Features**: Hardware Security Module (HSM) backing, role-based access control, and seamless integration with Azure services for auto-rotation.
* **Use Cases**: Storing database connection strings, managing SSL certificates, and application secret injection.

### Microsoft Defender for Cloud
* **Definition**: Cloud Security Posture Management (CSPM) and Cloud Workload Protection Platform (CWPP) for multi-cloud security assessment.
* **Key Features**: Secure score calculation, regulatory compliance audits, and real-time threat alerts for VMs and containers.
* **Use Cases**: Hardening security baselines and monitoring runtime threats.

---

## 6. Management & Monitoring Services

Tools to govern subscriptions, automate deployments, and track service health.

### Azure Monitor
* **Definition**: Comprehensive platform for collecting, analyzing, and acting on telemetry from cloud and on-premises environments.
* **Key Features**: Metrics explorer, log querying (Kusto Query Language - KQL), and alerting mechanisms.
* **Use Cases**: End-to-end performance visibility and operational alerting.

### Log Analytics Workspace
* **Definition**: A logical storage container where log telemetry data is aggregated, indexed, and queried.
* **Key Features**: High-performance log searching using KQL, integration with Microsoft Sentinel.
* **Use Cases**: Centralizing logs from firewalls, VMs, and Kubernetes clusters.

### Application Insights
* **Definition**: Application Performance Management (APM) tool for developers to monitor live applications.
* **Key Features**: Request tracking, dependency maps, exception logging, and user analytics.
* **Use Cases**: Diagnosing application errors, identifying execution bottlenecks.

### Azure Bicep / ARM Templates
* **Definition**: Infrastructure as Code (IaC) solutions for declarative resource provisioning.
* **Key Features**: Declarative syntax, idempotent deployments, and zero-day resource support.
* **Use Cases**: Automated CI/CD platform provisioning.

### Azure Policy
* **Definition**: Governance service used to enforce organizational standards and assess compliance at scale.
* **Key Features**: Evaluation of resource configurations, "Audit" or "Deny" policy effects, and automatic remediation.
* **Use Cases**: Enforcing tags on resources, blocking deployment of expensive VM SKUs.
