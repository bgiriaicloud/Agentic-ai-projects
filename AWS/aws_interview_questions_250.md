# AWS Cloud Engineer - 250 Interview Questions and Answers

This document contains a comprehensive collection of 250 interview questions and answers categorized to help you prepare for Amazon Web Services (AWS) Cloud Engineer roles from junior to principal levels.

---

## Part 1: Fundamentals & General Cloud Concepts (Questions 1 - 50)

#### Q1: What is AWS, and what is its global infrastructure composed of?
**A**: AWS is a comprehensive, evolving cloud computing platform provided by Amazon. Its global infrastructure is composed of:
- **Regions**: Physical geographic locations around the world hosting clusters of datacenters.
- **Availability Zones (AZs)**: One or more discrete datacenters within a region with redundant power, cooling, and network.
- **Edge Locations**: Local cache endpoints used by Amazon CloudFront (CDN) to deliver low-latency content.

#### Q2: What is the difference between an Availability Zone (AZ) and a Region in AWS?
**A**: A **Region** is a separate geographic area (e.g., `us-east-1` in N. Virginia). An **Availability Zone (AZ)** is a physical location within that region (e.g., `us-east-1a`). One region contains multiple, isolated AZs connected through low-latency fiber-optic links to support high-availability designs.

#### Q3: What is the AWS Shared Responsibility Model?
**A**: A security framework dividing responsibilities:
- **Security OF the Cloud**: AWS is responsible for protecting the infrastructure (hardware, software, networking, physical datacenters) running AWS services.
- **Security IN the Cloud**: The customer is responsible for managing guest operating systems, application code, firewall settings (security groups), IAM identities, and data encryption.

#### Q4: Explain the difference between IaaS, PaaS, and SaaS in AWS.
**A**:
- **IaaS**: Infrastructure as a Service, providing direct VM, network, and storage control (e.g., Amazon EC2, Amazon VPC). The customer patches the OS.
- **PaaS**: Platform as a Service, managing host servers and runtimes so the customer only manages code (e.g., Elastic Beanstalk, AWS App Runner).
- **SaaS**: Software as a Service, where the application is fully hosted and managed (e.g., Amazon WorkDocs, Amazon Connect).

#### Q5: What is AWS IAM (Identity and Access Management)?
**A**: A service that controls authentication and authorization access to AWS resources. It manages IAM Users (human logins), Groups (collections of users), Roles (identities assumed by systems/applications), and Policies (JSON documents defining permissions).

#### Q6: What is an IAM Policy, and what are the two main types?
**A**: An IAM Policy is a JSON document defining permissions. Types:
- **Identity-based Policies**: Attached directly to a user, group, or role specifying what resources they can access.
- **Resource-based Policies**: Attached directly to a resource (e.g., an S3 Bucket Policy) defining who can access that specific resource.

#### Q7: Explain the structure of an IAM Policy JSON document.
**A**: An IAM Policy contains one or more Statements, which include:
- **Effect**: `Allow` or `Deny`.
- **Action**: The API operations (e.g., `s3:GetObject`).
- **Resource**: The AWS resource Amazon Resource Name (ARN) the actions apply to.
- **Condition** (Optional): Constraints under which the policy is valid (e.g., IP ranges or MFA requirement).

#### Q8: What is an ARN in AWS?
**A**: ARN stands for **Amazon Resource Name**. It is a standardized string format used to uniquely identify any resource across all of AWS (e.g., `arn:aws:s3:::my-bucket-name`).

#### Q9: What is the difference between an IAM User and an IAM Role?
**A**:
- **IAM User**: A persistent identity with long-term credentials (password, access keys) representing a single person or service login.
- **IAM Role**: An identity with no long-term credentials. It is assumed temporarily by trusted entities (users, EC2 instances, external services) using short-lived security tokens.

#### Q10: What is IAM Role Assumption (STS AssumeRole)?
**A**: A process where a user or application calls the AWS Security Token Service (STS) to temporarily assume an IAM Role. STS returns short-lived credentials (access key, secret key, session token) valid for a limited period (e.g., 1 hour).

#### Q11: Explain the Principle of Least Privilege in AWS IAM.
**A**: The security practice of granting users and applications only the absolute minimum permissions required to perform their tasks, preventing accidental or malicious access to unauthorized resources.

#### Q12: What is the root user account in AWS, and what are the best practices for securing it?
**A**: The root user is the email account used to create the AWS account, possessing unrestricted permissions. Best practices:
- Never use the root account for daily administrative tasks.
- Enable strong Multi-Factor Authentication (MFA).
- Delete root access keys (prevent API access).
- Create administrative IAM users instead.

#### Q13: What is the purpose of AWS Organizations?
**A**: A resource management service that enables consolidation of multiple AWS accounts under a single organization, enabling consolidated billing, centralized management, hierarchical project groupings (OUs), and governance via Service Control Policies (SCPs).

#### Q14: What is a Service Control Policy (SCP) in AWS Organizations?
**A**: A policy used to manage maximum permissions for all accounts in an organization or Organizational Unit (OU). It acts as a guardrail; if an SCP denies an action (e.g., `Deny region us-west-1`), no IAM user or role (even root) in the member account can perform that action.

#### Q15: Explain the difference between Consolidated Billing and standard billing in AWS.
**A**: Consolidated Billing bundles payment methods for multiple AWS accounts under a single paying organization account. This allows you to combine resource usage to qualify for bulk volume discounts (e.g., S3 tier discounts) and simplifies accounting.

#### Q16: What is AWS CloudTrail?
**A**: A governance, compliance, and auditing service that records all API activity in your AWS account. It logs who made the call, from what IP, at what time, and what parameters were passed.

#### Q17: What is the difference between CloudWatch and CloudTrail?
**A**:
- **CloudWatch**: Focuses on performance monitoring, logging system logs, metrics tracking, and triggering alarms (operational health).
- **CloudTrail**: Focuses on security auditing, tracking API calls and user actions across the account (who did what).

#### Q18: What is the AWS Pricing Calculator?
**A**: A web-based planning tool used to estimate the running costs of AWS configurations before provisioning them.

#### Q19: What is the AWS Budgets service?
**A**: A service allowing you to set custom budgets to track your AWS costs and usage, triggering email or SNS alerts when actual or forecasted expenditures cross your defined thresholds.

#### Q20: Explain the AWS Well-Architected Framework and its pillars.
**A**: A set of design tenets for cloud architecture. The six pillars are: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability.

#### Q21: What is the AWS Trusted Advisor?
**A**: An automated service that inspects your AWS infrastructure and recommends optimizations based on best practices across Cost Optimization, Security, Fault Tolerance, Performance, and Service Limits.

#### Q22: What is AWS Support and the different tiers available?
**A**: Customer service and technical support plans: Basic (Free, billing support only), Developer, Business (24/7 access to cloud engineers, recommended for production), and Enterprise (includes a Technical Account Manager - TAM).

#### Q23: What are AWS Service Quotas (Limits)?
**A**: Hard or soft limits on resources per region per account (e.g., max 5 VPCs per region). Soft limits can be increased by submitting a support request.

#### Q24: What is a Tag in AWS, and why is it important?
**A**: A key-value metadata label applied to resources. Tags are critical for cost allocation (Cost Allocation Tags), automated scripts, grouping resources, and attribute-based access control (ABAC).

#### Q25: Explain the difference between public IP, private IP, and Elastic IP in AWS.
**A**:
- **Public IP**: Dynamic IP address assigned automatically, lost when the instance is stopped/terminated.
- **Private IP**: Internal IP address allocated from the subnet CIDR block, persists for the life of the instance.
- **Elastic IP (EIP)**: A static, public IP address allocated to your account that you can associate and re-associate with instances dynamically.

#### Q26: What is the AWS Cost Explorer?
**A**: A financial reporting tool used to visualize, analyze, and forecast your AWS spending patterns over time, identifying cost-saving opportunities.

#### Q27: What is AWS Systems Manager (SSM) Parameter Store?
**A**: A secure, hierarchical storage service for configuration parameters and secrets (passwords, license keys) that integrates with IAM for encryption and access control.

#### Q28: What is AWS Secrets Manager, and how does it differ from Parameter Store?
**A**:
- **SSM Parameter Store**: General configuration storage, free for standard parameters, no built-in automatic rotation.
- **Secrets Manager**: Purpose-built for secrets; supports automatic credential rotation (e.g., database passwords via Lambda triggers), but incurs a per-secret monthly cost.

#### Q29: What is AWS Key Management Service (KMS)?
**A**: A managed service that makes it easy to create and control cryptographic keys (KMS keys) to encrypt data at rest across AWS services and custom applications.

#### Q30: What is Envelope Encryption in AWS?
**A**: The process of encrypting data with a Data Encryption Key (DEK), and then encrypting the DEK with a root Key Encryption Key (KEK) managed inside AWS KMS.

#### Q31: Explain the difference between symmetric and asymmetric KMS keys.
**A**:
- **Symmetric**: Uses the same single key to encrypt and decrypt data (default, used by most AWS services).
- **Asymmetric**: Uses a public-private key pair; public key encrypts, private key decrypts.

#### Q32: What is AWS CloudHSM?
**A**: A cloud-based Hardware Security Module (HSM) dedicated entirely to a single customer, allowing you to generate and manage encryption keys on physical, FIPS 140-2 Level 3 validated devices inside AWS datacenters.

#### Q33: Explain AWS Shield Standard vs AWS Shield Advanced.
**A**:
- **Shield Standard**: Free DDoS protection enabled automatically for all AWS resources, mitigating common network/transport layer attacks.
- **Shield Advanced**: Paid subscription offering advanced DDoS protection, real-time alerts, integration with AWS WAF, and financial protection against billing spikes caused by attacks.

#### Q34: What is AWS WAF (Web Application Firewall)?
**A**: A web firewall protecting web applications against SQL injection, Cross-Site Scripting (XSS), and common OWASP Top 10 exploits by filtering HTTP traffic at ALB, CloudFront, or API Gateway.

#### Q35: What is Amazon GuardDuty?
**A**: A managed threat detection service that continuously monitors your AWS accounts, workloads, and data for malicious activity (like crypto-mining or unauthorized access) by analyzing CloudTrail, VPC Flow Logs, and DNS logs.

#### Q36: What is AWS Security Hub?
**A**: A security management service that aggregates security alerts (findings) from multiple AWS services (GuardDuty, Inspector, Macie) and checks infrastructure compliance against security standards (like CIS benchmarks).

#### Q37: What is Amazon Inspector?
**A**: An automated security assessment service that scans EC2 instances, ECR container images, and Lambda functions for software vulnerabilities and unintended network exposure.

#### Q38: What is Amazon Macie?
**A**: A data security and privacy service that uses machine learning and pattern matching to automatically discover, classify, and protect sensitive data (PII, credentials) stored in Amazon S3 buckets.

#### Q39: Explain the difference between AWS Directory Service Simple AD and AWS Managed Microsoft AD.
**A**:
- **Simple AD**: A Samba 4-compatible directory, supporting basic Active Directory features for small setups.
- **Managed Microsoft AD**: A real Windows Server Active Directory running natively on AWS hardware, supporting trusts, group policies, and schema extensions.

#### Q40: What is AWS IAM Access Analyzer?
**A**: A tool that analyzes resource policies (S3 bucket policies, KMS keys, IAM roles) to identify resources that are accessible from outside your AWS account, helping you eliminate security risks.

#### Q41: Explain IAM policy evaluation logic.
**A**:
1. Default: All requests are denied (`Default Deny`).
2. Evaluation checks all applicable policies.
3. An explicit deny in any policy overrides any allows (`Explicit Deny`).
4. An explicit allow is required to grant access.
5. If no explicit allow exists, the request remains denied.

#### Q42: What is the metadata service on an EC2 instance, and what is its URL?
**A**: A local web server providing VM configuration metadata and credentials. The URL is `http://169.254.169.254/latest/meta-data/`.

#### Q43: What is the difference between IMDSv1 and IMDSv2 in EC2 metadata?
**A**:
- **IMDSv1**: Uses a simple request/response model, vulnerable to SSRF (Server-Side Request Forgery) attacks.
- **IMDSv2**: Uses a session-oriented token request model, requiring a PUT request to fetch a token before making GET requests, significantly improving security.

#### Q44: What is an IAM Role trust policy?
**A**: A resource-based policy attached to an IAM Role that defines **which** trusted entities (e.g., an EC2 service, another AWS account, or an OIDC provider) are allowed to assume the role.

#### Q45: Explain what a Permission Boundary is in IAM.
**A**: An advanced policy assignment that sets the maximum permissions an identity-based policy can grant to an IAM user or role. It does not grant permissions on its own, but restricts existing permissions.

#### Q46: What is AWS Resource Access Manager (RAM)?
**A**: A service that allows you to securely share AWS resources (like subnets, Transit Gateways, or Route 53 resolver rules) across multiple AWS accounts within your AWS Organization.

#### Q47: What is the AWS Billing Conductor?
**A**: A billing customization service that allows enterprise customers to re-group billing data and compute custom pro-forma rates for subsidiary accounts or internal departments.

#### Q48: What is the purpose of the AWS Cost and Usage Report (CUR)?
**A**: The most comprehensive cost dataset available from AWS, exporting detailed hourly resource billing metadata to an S3 bucket for analysis via Athena or QuickSight.

#### Q49: What is Amazon Athena?
**A**: An interactive query service that allows you to analyze unstructured or semi-structured data directly in Amazon S3 using standard SQL, charging strictly per TB scanned.

#### Q50: Explain the AWS Service Catalog.
**A**: A governance tool allowing administrators to create, manage, and distribute catalogs of approved IT services (CloudFormation templates) to users, ensuring compliance while allowing self-service deployments.

---

## Part 2: Compute & Containers (Questions 51 - 100)

#### Q51: Explain the difference between Instance Store and Elastic Block Store (EBS) in EC2.
**A**:
- **Instance Store**: Physically attached to the host computer hosting the VM. It provides high IOPS and low latency, but is ephemeral—data is lost when the instance is stopped, rebooted on another host, or terminated.
- **EBS**: Network-attached storage that is independent of the VM. Data is durable, persists if the VM is stopped, and supports snapshots.

#### Q52: What is the difference between EBS Volume types: GP3, IO2, and ST1?
**A**:
- **GP3**: General-purpose SSD offering balanced price and performance (3,000 baseline IOPS up to 16,000, 125 MB/s throughput scaling).
- **IO2**: High-performance Provisioned IOPS SSD designed for business-critical, IO-intensive databases.
- **ST1**: Low-cost Throughput Optimized HDD designed for frequently accessed, throughput-intensive workloads (like MapReduce, log processing).

#### Q53: Explain the difference between EC2 Launch Configurations and Launch Templates.
**A**:
- **Launch Configuration**: The legacy model defining VM parameters (AMI, instance type, keys) for Auto Scaling. It is immutable and does not support versioning.
- **Launch Template**: The modern, active model. It supports configuration versioning, parameter parameter inheritance, mixing Spot/On-Demand instances in a single ASG, and is required for T3 unlimited and capacity reservations.

#### Q54: What are EC2 Placement Groups, and what are the three types?
**A**: Placement Groups influence the physical placement of instances on hardware. Types:
- **Cluster**: Packs instances close together inside a single AZ, enabling low latency and high network throughput (useful for HPC).
- **Spread**: Places instances on distinct physical racks, minimizing correlated failures (useful for critical VMs).
- **Partition**: Groups instances into logical segments (partitions) across physical racks to ensure no partitions share hardware.

#### Q55: How does Auto Scaling Group (ASG) scaling work, and what are the dynamic scaling policy types?
**A**: An ASG monitors traffic/resource demands and rescales instance pools. Policies:
- **Target Tracking**: Maintains a metric at a target value (e.g., keep average CPU at 60%).
- **Simple/Step Scaling**: Adds/removes a fixed number of instances based on alarm thresholds.
- **Scheduled Scaling**: Scales based on predictable dates/times.

#### Q56: What is a Lambda "Cold Start," and how can you mitigate it?
**A**: A cold start is the initialization latency observed when a Lambda function is invoked after being idle. The system must allocate compute container resources and load runtime dependencies. Mitigation: Use **Provisioned Concurrency** (pre-warms execution environments), optimize package sizing, and reduce initialization code complexity.

#### Q57: What is the difference between Reserved Instances (RIs) and Savings Plans in AWS?
**A**:
- **Reserved Instances**: Commit to a specific instance type family, OS, and region for 1 or 3 years.
- **Savings Plans**: Commit to a consistent hourly spend (e.g., $10/hour) for 1 or 3 years, offering greater flexibility across instance families, regions, and even Lambda/Fargate runtimes.

#### Q58: Explain the difference between ECS EC2 Launch Type and ECS Fargate Launch Type.
**A**:
- **EC2 Launch Type**: You must manage and pay for the underlying EC2 host servers, configuring container agents and scaling pools manually.
- **Fargate Launch Type**: Serverless container execution. You do not manage host servers; you define CPU/memory limits per container task, and AWS manages the infrastructure.

#### Q59: What is an Amazon ECR (Elastic Container Registry) Image Scan?
**A**: An automated security feature that scans your container images stored in ECR for software vulnerabilities using CVSS database records.

#### Q60: What are EKS Fargate Profiles?
**A**: Fargate Profiles allow EKS clusters to run Kubernetes pods directly on AWS Fargate serverless infrastructure, managing pod scheduling, network attachments, and resource allocations automatically.

#### Q61: What is the maximum execution execution timeout for an AWS Lambda function?
**A**: The maximum timeout limit is **15 minutes** (900 seconds) per invocation.

#### Q62: What is the difference between Lambda Reserved Concurrency and Provisioned Concurrency?
**A**:
- **Reserved Concurrency**: Sets the maximum number of concurrent executions allowed for a function, acting as a throttle and reserving that capacity from the regional pool.
- **Provisioned Concurrency**: Pre-allocates warm execution environments to instantly run requests, eliminating cold start latency.

#### Q63: Explain what AWS Systems Manager (SSM) Session Manager does.
**A**: A service that allows secure interactive command-line access to EC2 instances through a browser or AWS CLI, without opening RDP/SSH ports, exposing public IPs, or managing SSH key pairs.

#### Q64: What is AWS App Runner, and what hosting model does it use?
**A**: AWS App Runner is a serverless container hosting service. It abstracts away ECS/Fargate configurations, load balancers, and VPC setups, deploying containerized code directly from registries or GitHub repos.

#### Q65: What is the difference between AWS Elastic Beanstalk and AWS App Runner?
**A**:
- **Elastic Beanstalk**: An orchestration PaaS supporting web apps. It deploys resources (EC2, ELB, ASG, RDS) directly in the customer account, allowing full customization.
- **App Runner**: A serverless CD hosting platform. Infrastructure is managed in AWS-owned service projects, providing a zero-infrastructure configuration model.

#### Q66: Explain EC2 Instance Hibernation.
**A**: A state-saving feature that copies the VM's RAM memory contents to the root EBS volume before stopping the instance. When restarted, the VM loads the state back, resuming processes quickly.

#### Q67: What is an Amazon Machine Image (AMI)?
**A**: A master template containing the operating system, server configurations, pre-installed software, and block device mapping configuration used to launch EC2 instances.

#### Q68: What is the difference between EBS General Purpose GP2 and GP3 volumes?
**A**:
- **GP2**: Performance (IOPS) is bound to disk size (3 IOPS per GB, minimum 100). To get higher IOPS, you must buy a larger disk.
- **GP3**: Performance (IOPS and throughput) can be configured and scaled independently of disk size, offering cost savings and configuration flexibility.

#### Q69: Explain the difference between EBS snapshots and AMIs.
**A**:
- **EBS Snapshot**: A block-level backup of a single EBS volume.
- **AMI**: A bootable template containing a metadata manifest and snapshots of all attached disks needed to spawn a full virtual machine.

#### Q70: What is an EC2 Launch Template version?
**A**: A feature allowing templates to be versioned. You can make updates, create new versions, and set a default version for Auto Scaling Groups, facilitating rollbacks.

#### Q71: Explain EKS Managed Node Groups.
**A**: An EKS feature that automates node provisioning, lifecycle management, host patching, and cluster drain operations for your EC2 worker nodes.

#### Q72: What is Lambda Destination configuration?
**A**: A feature that routes execution results (success or failure payloads) of asynchronous Lambda invocations to other services (EventBridge, SQS, SNS, or another Lambda) without writing routing code.

#### Q73: What is the purpose of an ECS Task Definition?
**A**: A JSON configuration file defining the container parameters (image, port mappings, environment variables, IAM roles, CPU/memory) required to launch one or more Docker containers as a task.

#### Q74: Explain the difference between ECS Task Role and ECS Task Execution Role.
**A**:
- **Task Role**: The IAM role assumed by the container code itself to call AWS services (e.g., read an S3 bucket).
- **Task Execution Role**: The IAM role assumed by the ECS agent to pull images from ECR and send logs to CloudWatch.

#### Q75: What is Amazon Lightsail?
**A**: A simplified, low-cost virtual private server (VPS) hosting service tailored for developers, students, and small businesses needing simple VMs, databases, and DNS configurations with flat-rate monthly billing.

#### Q76: Explain what an EC2 Auto Scaling cooldown period is.
**A**: A safety timer that prevents an ASG from launching or terminating additional instances until the previous scaling action takes effect and the metrics stabilize, preventing over-scaling.

#### Q77: What are EBS Multi-Attach volumes?
**A**: An EBS feature allowing a single Provisioned IOPS (IO1/IO2) volume to be attached to multiple EC2 instances concurrently within the same AZ, supporting clustered, shared-disk applications.

#### Q78: Explain the difference between Spot Fleets and Spot Instances.
**A**:
- **Spot Instance**: A single request for low-cost, unused EC2 capacity.
- **Spot Fleet**: An advanced management interface that launches and manages a collection of Spot and On-Demand instances, optimizing capacity, instance types, and cost across multiple pools.

#### Q79: What is the purpose of the AWS Systems Manager (SSM) Agent?
**A**: A lightweight daemon installed on EC2 instances or on-premises servers that communicates with SSM endpoints, enabling patch management, execution of Run Commands, and Session Manager terminals.

#### Q80: How does EKS manage Kubernetes version upgrades?
**A**: EKS manages control plane upgrades. Worker node upgrades are managed by you (often using Managed Node Groups), which drains pods, updates the node AMI, and rolls out nodes sequentially to maintain availability.

#### Q81: What is a Lambda Layer?
**A**: A mechanism to share code, libraries, dependencies, or custom runtimes across multiple Lambda functions, reducing zip deployment sizes and separating code from dependencies.

#### Q82: What is the difference between Lambda Event Source Mapping and direct invocations?
**A**:
- **Event Source Mapping**: Lambda polls a stream or queue service (e.g., SQS) and invokes the function when items are found, managing retries and batches automatically.
- **Direct Invocation**: An external client calls the Lambda API directly (synchronously or asynchronously).

#### Q83: Explain the ECS "rolling update" deployment strategy.
**A**: A strategy that gradually replaces old tasks with new tasks. You define the `minimumHealthyPercent` (e.g., 100%) and `maximumPercent` (e.g., 200%) to control how many instances run during the upgrade.

#### Q84: What is the difference between AWS Lambda Function URL and API Gateway integration?
**A**:
- **Function URL**: A free, built-in HTTPS endpoint for a single Lambda function, best for simple webhooks.
- **API Gateway**: A managed API proxy offering request throttling, security policies, caching, validation, and multi-endpoint routing.

#### Q85: What is the purpose of Amazon Elastic Container Service (ECS) Service Connect?
**A**: A service mesh feature that simplifies service-to-service communication inside ECS, providing automated service discovery, health checks, traffic routing, and telemetry tracking.

#### Q86: What is a Spot Instance interruption notice, and how much warning is given?
**A**: A termination notification sent by AWS when it needs to reclaim capacity. The instance receives exactly a **2-minute warning** via metadata server hooks before being stopped or terminated.

#### Q87: Explain what an EBS volume snapshot lifecycle policy is (DLM).
**A**: Data Lifecycle Manager (DLM) is a built-in scheduler that automates the creation, retention, and deletion of EBS volume snapshots to enforce backup compliance rules.

#### Q88: How does Lambda execute inside a VPC?
**A**: When configured for VPC access, Lambda creates Hyperplane ENIs (Elastic Network Interfaces) in your subnets. The function is assigned private IPs, allowing it to communicate with internal resources (like RDS) over private networks.

#### Q89: What is EKS Karpenter, and how does it differ from Cluster Autoscaler?
**A**: Karpenter is a high-performance Kubernetes cluster autoscaler. Unlike standard autoscalers that scale fixed node pools, Karpenter bypasses node pools, provisioning the exact instance size and type required by pending pods directly from EC2 APIs, reducing resource waste.

#### Q90: What is an EC2 Instance Status Check?
**A**: Diagnostic checks run by AWS:
- **System Status Check**: Monitors the physical host hardware.
- **Instance Status Check**: Monitors the guest OS and software stack.

#### Q91: What is the default VPC subnet availability in terms of CIDR?
**A**: VPC subnets do not span multiple Availability Zones. Each subnet resides entirely within a single AZ.

#### Q92: Explain EBS volume initialization (Pre-warming).
**A**: New EBS volumes deliver maximum performance instantly. However, volumes restored from snapshots require blocks to be pulled from S3, causing initial read latency. "Pre-warming" reads all blocks on the volume once to initialize them.

#### Q93: Can you attach an EBS volume to an EC2 instance in a different Availability Zone?
**A**: No. EBS volumes are zonal resources and can only be attached to EC2 instances residing in the exact same Availability Zone.

#### Q94: What is the purpose of the AWS Lambda execution role?
**A**: An IAM role attached to the Lambda function that grants it permissions to write logs to CloudWatch and call other AWS APIs.

#### Q95: What is an ECS Task Placement Strategy, and what are the options?
**A**: Rules governing how tasks are distributed across instances in a cluster. Options:
- **Binpack**: Packs tasks into instances to minimize instance count and cost.
- **Spread**: Distributes tasks evenly across AZs or instances for high availability.
- **Random**: Places tasks randomly.

#### Q96: What is AWS App 2 Container?
**A**: A command-line tool that analyzes and containerizes Java and .NET applications running on IIS or application servers, generating Dockerfiles and ECS/EKS deployment templates.

#### Q97: What is Lambda Ephemeral Storage (`/tmp`), and what is its maximum limit?
**A**: A local storage directory available during function execution. The size limit can be configured from 512 MB up to **10 GB**.

#### Q98: Explain EKS Pod Identity.
**A**: The modern way to assign IAM roles to Kubernetes pods. It associates IAM roles directly with Kubernetes service accounts without requiring OIDC identity providers or trust policy configurations.

#### Q99: What is the difference between AWS Elastic Beanstalk Web Server Environment and Worker Environment?
**A**:
- **Web Server**: Hosts applications that listen for and handle HTTP requests (uses ALB).
- **Worker Server**: Pulls jobs from an SQS queue and processes background tasks.

#### Q100: How do you access an EC2 instance if you lost your SSH key pair?
**A**:
- Use **SSM Session Manager** (if the SSM Agent is installed and the instance has the correct role).
- Use **EC2 Instance Connect** (if configured).
- Detach the root EBS volume, mount it to a temporary instance, edit the `authorized_keys` file, and attach it back.

---

## Part 3: Networking & Hybrid Connectivity (Questions 101 - 150)

#### Q101: Explain the difference between Security Groups and Network Access Control Lists (NACLs) in AWS.
**A**:
- **Security Groups**: Stateful (inbound replies automatically allowed), applied at the instance/NIC level, support allow rules only, and evaluate all rules before taking action.
- **NACLs**: Stateless (return traffic must be explicitly allowed), applied at the subnet level, support allow and deny rules, and evaluate rules in numbered order.

#### Q102: Why do you need to open Ephemeral Ports in a NACL?
**A**: Because NACLs are stateless. When an EC2 instance establishes an outbound connection (e.g., calls an external API on port 80/443), the client chooses a temporary return port (ephemeral port range `1024-65535`). If the inbound NACL rules do not allow traffic back on these ephemeral ports, the response packets will be blocked.

#### Q103: Explain what a NAT Gateway is and the difference between public and private NAT Gateways.
**A**: A NAT Gateway enables instances in private subnets to connect to the internet while preventing external systems from initiating connections to them.
- **Public NAT Gateway**: Resides in a public subnet, requires an Elastic IP, and routes traffic to the Internet Gateway.
- **Private NAT Gateway**: Resides in a private subnet, uses private IPs, and routes traffic to other VPCs or on-premises networks without internet routing.

#### Q104: What is the difference between an Internet Gateway (IGW) and a Virtual Private Gateway (VGW)?
**A**:
- **IGW**: A horizontally scaled, redundant VPC component that enables communication between public subnet instances and the public internet.
- **VGW**: The VPN concentrator on the AWS side of a Site-to-Site VPN or Direct Connect connection, enabling private hybrid connectivity.

#### Q105: Is VPC Peering transitive? Explain with an example.
**A**: No. VPC Peering is **not transitive**. If VPC A is peered with VPC B, and VPC B is peered with VPC C, instances in VPC A cannot communicate with instances in VPC C unless you create a separate direct peering link between VPC A and VPC C, or route through a Transit Gateway.

#### Q106: What is AWS Transit Gateway, and what problem does it solve?
**A**: Transit Gateway is a centralized cloud router that connects multiple VPCs, VPNs, and Direct Connect links. It solves the complexity of managing a full-mesh network topology where every VPC must be peered with every other VPC, replacing it with a simple hub-and-spoke model.

#### Q107: Explain the difference between VPC Interface Endpoints and VPC Gateway Endpoints.
**A**:
- **Interface Endpoints (PrivateLink)**: Deploy an Elastic Network Interface (ENI) with a private IP from your subnet. Charges apply per hour/GB, and it supports most AWS services.
- **Gateway Endpoints**: A free routing target configured in your Route Table. It supports only **Amazon S3** and **DynamoDB** and does not use ENIs.

#### Q108: What are VPC Flow Logs?
**A**: A feature that captures IP traffic information flowing to and from network interfaces in your VPC. Flow logs can be published to CloudWatch Logs or Amazon S3 for security auditing and network troubleshooting.

#### Q109: Explain the difference between Application Load Balancers (ALB) and Network Load Balancers (NLB).
**A**:
- **ALB**: Layer 7 load balancer routing HTTP/HTTPS traffic based on request attributes (URL path, host headers, query parameters).
- **NLB**: Layer 4 load balancer routing TCP/UDP traffic at ultra-low latency, offering static Elastic IPs and handling sudden millions of requests per second.

#### Q110: What is a Gateway Load Balancer (GWLB)?
**A**: A specialized load balancer deployed to deploy, scale, and manage virtual network appliances (such as firewalls, intrusion detection systems, and deep packet inspection engines) from third-party vendors.

#### Q111: Explain Route 53 Routing Policies: Latency, Geolocation, and Geoproximity.
**A**:
- **Latency**: Routes users to the AWS region that provides the lowest round-trip latency.
- **Geolocation**: Routes traffic based on the physical geographic location of the user (country or state).
- **Geoproximity**: Routes traffic based on the physical distance between the user and resources, allowing you to shift traffic volumes using bias values.

#### Q112: What is the difference between Route 53 Alias Records and CNAME Records?
**A**:
- **CNAME**: Maps one domain name to another domain name. It cannot be created for the zone apex (root domain like `example.com`).
- **Alias Record**: An AWS-specific DNS record pointing directly to AWS resources (like an S3 bucket or ELB). It **can** be created for the zone apex and does not charge for DNS queries.

#### Q113: What is Route 53 Resolver (Active/Passive Endpoints)?
**A**: A hybrid DNS resolution service. It includes **Inbound Endpoints** (allows on-premises systems to resolve AWS private DNS records) and **Outbound Endpoints** (allows AWS resources to forward DNS queries to on-premises DNS servers).

#### Q114: What is AWS Direct Connect (DX), and what are its advantages over VPN?
**A**: A physical telecommunication connection linking your on-premises network directly to AWS locations. Advantages: Bypasses the public internet, delivers consistent network performance, offers high bandwidth (up to 100 Gbps), and reduces data egress costs.

#### Q115: What is AWS Global Accelerator, and how does it differ from Amazon CloudFront?
**A**:
- **Global Accelerator**: Optimizes the network path for any TCP/UDP traffic using static Anycast IPs to route users through AWS's global network edge (ideal for gaming, VoIP, non-HTTP).
- **CloudFront**: A CDN optimized specifically for caching and serving HTTP/HTTPS content (HTML, JS, media files) from edge locations.

#### Q116: How do you configure active-active and active-passive VPN failover in AWS?
**A**:
- **Active-Active**: Deploy a Virtual Private Gateway (VGW) which automatically provisions two public IP tunnels. Configure both tunnels to run dynamic routing (BGP) with your Customer Gateway.
- **Active-Passive**: Configure static routing. Set the route table weights or configure your on-premises router to prioritize one tunnel path, keeping the second as a backup.

#### Q117: What is an AWS Client VPN?
**A**: A managed client-to-site VPN service that allows remote employees to connect securely to resources inside your VPC or on-premises networks using OpenVPN client configurations.

#### Q118: How does Route 53 failover routing policy work?
**A**: It monitors the health of your primary endpoint using Route 53 health checks. If the primary health check fails, Route 53 automatically redirects DNS queries to a configured secondary (backup) endpoint.

#### Q119: Can you peer VPCs across different AWS accounts and regions?
**A**: Yes. VPC Peering supports inter-region peering (connecting VPCs in different regions) and inter-account peering (connecting VPCs belonging to different AWS accounts).

#### Q120: What is the maximum number of subnets you can create in a VPC?
**A**: The limit is governed by the VPC CIDR block. You can create up to **200 subnets** per VPC by default.

#### Q121: Which 5 IP addresses does AWS reserve in every subnet?
**A**: In a subnet range `10.0.0.0/24`:
- `10.0.0.0`: Network address.
- `10.0.0.1`: VPC router address.
- `10.0.0.2`: DNS mapping (AmazonProvidedDNS).
- `10.0.0.3`: Reserved for future AWS usage.
- `10.0.0.255`: Network broadcast address.

#### Q122: What is the Amazon Provided DNS (Route 53 Resolver) IP address?
**A**: It is always mapped to the base of the VPC network range plus two. For example, in a `10.0.0.0/16` network, the DNS resolver IP is `10.0.0.2`. It is also available at the link-local address `169.254.169.253`.

#### Q123: Explain the difference between public subnets and private subnets in AWS.
**A**:
- **Public Subnet**: The subnet route table has an explicit route pointing to an **Internet Gateway** (`0.0.0.0/0` -> `igw-xxxx`). Instances can have public IPs.
- **Private Subnet**: The route table does not route traffic to an Internet Gateway. Outbound internet traffic is routed through a NAT Gateway or virtual appliance.

#### Q124: What is an Elastic IP address allocation charge policy?
**A**: Elastic IPs are free if they are associated with a running EC2 instance and only one EIP is used per instance. If an EIP is unassociated, or associated with a stopped instance, AWS charges an hourly fee to prevent IP resource hoarding.

#### Q125: What is the VPC "Egress-Only Internet Gateway"?
**A**: A stateful VPC component that enables IPv6-based private instances to connect outbound to the internet, while blocking any inbound unsolicited connection attempts (analogous to NAT Gateway for IPv4).

#### Q126: Explain the difference between Route 53 Public Hosted Zones and Private Hosted Zones.
**A**:
- **Public Hosted Zone**: Holds DNS records accessible from the public internet (resolves public domains).
- **Private Hosted Zone**: Holds DNS records accessible only from within one or more VPCs linked to the zone.

#### Q127: What is an AWS PrivateLink service?
**A**: The underlying technology that maps endpoints privately. It allows service providers to share their services with consumers in other VPCs privately and securely over the AWS backbone using ENIs.

#### Q128: Explain what a Target Group is in Elastic Load Balancing.
**A**: A logical group of target resources (EC2 instances, lambda functions, container tasks, or IP addresses) that receive load-balanced traffic distributed by load balancer listener rules.

#### Q129: What is the purpose of the ALB "Slow Start" mode?
**A**: A configuration that allows newly added target instances to ramp up their traffic share gradually over a defined period (e.g., 30 seconds), preventing them from being overwhelmed by requests during startup.

#### Q130: What is connection draining (De-registration Delay) in ELB?
**A**: A configuration that keeps active connections open for a grace period (e.g., 300 seconds) when an instance is deregistered or becomes unhealthy, allowing it to complete in-flight requests before terminating.

#### Q131: What is a VPC DHCP Options Set?
**A**: A configuration set containing domain name settings, DNS servers, NTP servers, and NetBIOS settings assigned to instances when they lease IPs via DHCP in your VPC.

#### Q132: What is a VPC Peering MTU limitation?
**A**: VPC Peering supports MTU sizes up to `1500` bytes by default. However, inter-region peering does not support Jumbo frames (up to 9001 bytes); Jumbo frames are supported only for intra-region peering.

#### Q133: What is the purpose of Route 53 Resolver Rules?
**A**: Rules that define how DNS queries for specific domains should be routed. Useful for forwarding corporate domain queries (e.g., `*.corp.com`) to local enterprise DNS servers from cloud VPCs.

#### Q134: How do you secure an ALB to only accept traffic from CloudFront?
**A**:
- Configure CloudFront to add a custom HTTP header (e.g., `X-Origin-Secret`) to requests sent to the ALB origin.
- Configure ALB listener rules to block any incoming request that does not contain that specific custom header.
- Alternatively, restrict the ALB security group to allow inbound traffic only from CloudFront IP ranges.

#### Q135: What is AWS Global Accelerator static Anycast IP addresses advantage?
**A**: It provides two static public IP addresses. When configuring DNS records, you can point your domain root apex directly to these static IPs, eliminating the need to update DNS configurations if target ALB IPs change.

#### Q136: Explain the difference between Route 53 CNAME and ALIAS records for load balancer endpoints.
**A**:
- **CNAME**: Requires a lookup query that returns the load balancer DNS string, which then requires another lookup to find the IP. Cannot be used at the root domain (`example.com`).
- **ALIAS**: Instantly resolves to the target load balancer's IP addresses in one query, improving latency, and can be configured at the root domain.

#### Q137: What is the purpose of the AWS Network Firewall?
**A**: A managed, stateful firewall service that provides network-level traffic filtering and intrusion prevention (IPS) across all subnets in a VPC.

#### Q138: Explain the difference between ALB HTTP-to-HTTPS redirect rules.
**A**: You can configure ALB listeners to automatically redirect any HTTP request arriving on port 80 to port 443 (HTTPS) with a 301 (Moved Permanently) status code.

#### Q139: Can you assign multiple SSL/TLS certificates to a single ALB listener?
**A**: Yes. By using **Server Name Indication (SNI)**, an ALB can host multiple SSL certificates on a single listener, selecting the correct certificate dynamically based on the client request host header.

#### Q140: How does a NAT Instance differ from a managed NAT Gateway?
**A**:
- **NAT Instance**: A single EC2 VM configured to perform NAT routing. You must manage its scaling, HA, patching, and OS.
- **NAT Gateway**: A fully managed, highly available SaaS network appliance that scales bandwidth automatically up to 45 Gbps without admin maintenance.

#### Q141: What is a VPC Endpoint Policy?
**A**: An IAM resource policy attached to a VPC Endpoint (Interface or Gateway) that restricts which principals can call APIs through the endpoint and what resources they can access.

#### Q142: How do you inspect which security group rule is blocking traffic to an instance?
**A**: Security groups do not have block logs. To diagnose issues, enable **VPC Flow Logs** and search the log streams in CloudWatch. Look for the `REJECT` status to see the source/destination IPs and ports that were blocked.

#### Q143: Explain how the NLB health check protocol works.
**A**: NLB performs health checks at Layer 4 (TCP ping) or Layer 7 (HTTP request) against targets. If a target fails to respond, it is marked unhealthy, and NLB immediately stops routing TCP connections to it.

#### Q144: Can you peer a VPC with another VPC that has an overlapping CIDR block?
**A**: No. AWS blocks peering connections if the VPC networks have overlapping IP address spaces.

#### Q145: What is a VPC Virtual Private Cloud router?
**A**: The underlying software-defined router that manages routing tables inside the VPC to direct packets between subnets, network gateways, and endpoints.

#### Q146: What is a Route 53 DNS Query Logging feature?
**A**: An auditing feature that logs details of all public DNS queries received by Route 53 (domain queried, client IP, record type, timestamp), exporting logs to CloudWatch.

#### Q147: Explain what an AWS Direct Connect Hosted Connection is.
**A**: A Direct Connect connection provisioned by an AWS Partner network operator on physical circuits they own, allowing you to buy smaller bandwidth slices (50 Mbps up to 10 Gbps).

#### Q148: What is Route 53 DNSSEC?
**A**: DNS Security Extensions. A protocol that signs DNS records cryptographically, protecting clients against DNS spoofing and man-in-the-middle poisoning attacks.

#### Q149: What is the purpose of the VPC NAT Gateway "Elastic IP association"?
**A**: A public NAT Gateway requires a static public IP to perform source network address translation. AWS maps outbound private traffic onto this EIP before sending it to the internet.

#### Q150: What is a Transit Gateway Route Table?
**A**: A route table associated with a Transit Gateway attachment (VPC or VPN). It determines how packets arriving at the Transit Gateway from that attachment are routed to other attachments.

---

## Part 4: Identity, Security & Governance (Questions 151 - 200)

#### Q151: What is the difference between an IAM Role trust policy and an IAM Role permissions policy?
**A**:
- **Trust Policy**: A resource-based policy written in JSON that defines **who** (which accounts, users, or AWS services like EC2/Lambda) is allowed to assume the role.
- **Permissions Policy**: An identity-based JSON policy defining **what** actions the role can perform once assumed (e.g., read an S3 bucket).

#### Q152: What is an IAM Instance Profile?
**A**: An Instance Profile is a container for an IAM Role that allows you to pass the role's permissions to an EC2 instance. When you attach an Instance Profile to a VM, the EC2 agent automatically fetches temporary security credentials from the metadata server.

#### Q153: Explain the difference between AWS Secrets Manager and Systems Manager (SSM) Parameter Store.
**A**:
- **SSM Parameter Store**: Free for standard parameters (up to 10,000 parameters), supports basic secure strings, but does not support automatic secret rotation natively.
- **Secrets Manager**: Costs per secret per month, but supports automated key/password rotation using built-in AWS Lambda templates, cross-account access, and secret replication across regions.

#### Q154: Explain AWS Key Management Service (KMS) Key Policies. Can you access a key without one?
**A**: A Key Policy is a resource-based JSON policy attached to a KMS key that defines who can use and manage the key. **You cannot access a KMS key without a Key Policy.** Unlike S3 where identity policies can grant access, KMS access *must* be explicitly allowed by the Key Policy first.

#### Q155: What is a KMS Grant?
**A**: A KMS Grant is a delegating permission mechanism that allows a principal to use a KMS key temporarily or programmatically (e.g., allowing an autoscaling group to decrypt an EBS volume key during instance launches) without editing the main key policy.

#### Q156: Explain the difference between AWS-Managed Keys and Customer-Managed Keys (CMKs) in KMS.
**A**:
- **AWS-Managed Keys**: Created automatically by AWS services (e.g., `aws/s3`). You cannot view, edit, rotate, or delete these keys; they are rotated every 3 years.
- **Customer-Managed Keys**: Created by you. You have full control over key policies, description modifications, auditing, deletion schedules, and can configure automatic annual rotation.

#### Q157: What is the purpose of AWS Organizations Service Control Policies (SCPs)?
**A**: SCPs are organizational guardrails that define the maximum permissions allowed for member accounts under an AWS Organization. Even if an IAM user has full administrator permissions inside a member account, an SCP that denies an action will override those permissions.

#### Q158: Do Service Control Policies (SCPs) apply to the Master (Management) Account of an Organization?
**A**: No. SCPs apply to all member accounts and organizational units (OUs) but **do not apply** to the Master (Management) Account of the organization.

#### Q159: What is AWS Control Tower, and what are Guardrails?
**A**: Control Tower is a service that automates the setup of a secure, multi-account AWS environment (Landing Zone). **Guardrails** are pre-configured governance rules that enforce compliance (e.g., "Disallow public S3 buckets") using SCPs (preventative) or AWS Config rules (detective).

#### Q160: Explain how cross-account IAM access is configured in AWS.
**A**:
1. In Account B (Target), create an IAM Role with a trust policy that permits Account A (Source) to assume it.
2. In Account A, assign an IAM policy to the user/group that allows them to call `sts:AssumeRole` on Account B's role ARN.
3. The user in Account A calls STS to assume the role, receives temporary credentials, and accesses resources in Account B.

#### Q161: What is AWS Config, and how does it differ from CloudTrail?
**A**:
- **AWS Config**: Records configuration changes of resources over time, evaluates compliance against rules (e.g., "Is EBS volume encrypted?"), and supports automated remediation.
- **CloudTrail**: Records user API actions and account activity (who did it).

#### Q162: What is Amazon GuardDuty, and what data sources does it analyze?
**A**: GuardDuty is an intelligent threat detection service. It analyzes:
- VPC Flow Logs (network patterns).
- CloudTrail Management and Data Events (user APIs).
- DNS Logs (query queries from EC2).
- EKS Audit Logs.

#### Q163: Explain what AWS Systems Manager (SSM) Patch Manager does.
**A**: An automated patching tool that scans and installs security patches, OS updates, and package updates across fleets of EC2 instances or on-premises servers based on patch baseline rules.

#### Q164: What is the AWS Security Hub, and what compliance frameworks does it support?
**A**: Security Hub aggregates security alerts and findings from GuardDuty, Inspector, and third-party tools. It checks compliance against standards such as CIS AWS Foundations Benchmark, PCI-DSS, and AWS Foundational Security Best Practices.

#### Q165: What is AWS Artifact?
**A**: A self-service portal providing on-demand access to AWS security and compliance reports (such as SOC, ISO, PCI, FedRAMP certificates) and agreements (like Business Associate Addendums - BAA for HIPAA).

#### Q166: Explain the difference between Amazon Inspector network scans and host scans.
**A**:
- **Network Scan**: Evaluates the network configuration of EC2 instances to identify reachable open ports and external exposures.
- **Host Scan**: Installs an agent on the instance OS to scan for installed software vulnerabilities, software patches, and compliance issues.

#### Q167: What is an IAM Permission Boundary?
**A**: A policy boundary assigned to an IAM user or role that defines the maximum permissions they can possess. Even if an identity policy allows administrator access (`*:*`), the user can only perform actions that are explicitly allowed in both the identity policy and the permission boundary.

#### Q168: What is the purpose of the AWS Key Management Service (KMS) Multi-Region Keys?
**A**: Specialized KMS keys created in one region that can be replicated to other regions with the same key ID and key material. This allows data encrypted in one region to be decrypted in another region without making cross-region KMS API calls.

#### Q169: Explain the difference between IAM inline policies and customer-managed policies.
**A**:
- **Customer-Managed Policy**: A standalone policy in your account that can be attached to multiple users, groups, or roles, supporting versioning.
- **Inline Policy**: A policy embedded directly within a single user, group, or role. It maintains a strict 1-to-1 relationship and does not exist independently.

#### Q170: What is AWS IAM Identity Center (successor to AWS Single Sign-On)?
**A**: A centralized service that manages single sign-on access to all your AWS accounts and cloud business applications (like Microsoft 365 or Salesforce), integrating with external identity providers like Okta or Azure AD.

#### Q171: What is the purpose of an IAM Service-Linked Role?
**A**: A predefined IAM role linked directly to an AWS service (e.g., Auto Scaling). The service assumes this role automatically to perform tasks in your account (like launching EC2 instances) without requiring you to configure credentials.

#### Q172: How does AWS Organizations manage billing consolidated payment accounts?
**A**: The management account consolidates all member account costs into a single monthly invoice, allowing resource usage (like S3 storage or EC2 hours) to be aggregated to meet higher tier discount thresholds.

#### Q173: Explain what an AWS CloudTrail Organization Trail is.
**A**: A trail configured in the master account of an AWS Organization that automatically records and centralizes all API logs for all member accounts into a single secure S3 bucket, preventing member accounts from disabling the logging.

#### Q174: What is the purpose of the AWS Directory Service Active Directory Connector (AD Connector)?
**A**: A directory gateway that redirects directory requests (authentication, searches) from AWS services to your on-premises Microsoft Active Directory without caching or storing user credentials in the cloud.

#### Q175: What is AWS Network Manager?
**A**: A management service that provides a single global dashboard to monitor and manage the quality and performance of your global network attachments (Transit Gateways, Site-to-Site VPNs, and Direct Connect).

#### Q176: What is AWS WAF Web ACL (Access Control List)?
**A**: A collection of security rules containing filter conditions (IP ranges, header contents, geo-filters, rate limits) applied to protect resources (ALB, CloudFront, API Gateway) against malicious payloads.

#### Q177: Explain the AWS KMS Key Policy "Enable Key Rotation" feature.
**A**: A setting that configures KMS to automatically rotate the cryptographic key material once a year. Older key versions are retained to decrypt existing data, and new data is encrypted using the new key version.

#### Q178: What is AWS CloudTrail Insights?
**A**: An anomaly detection feature in CloudTrail that analyzes management logs to identify unusual API patterns (such as a sudden spike in resource creations or permission modifications) and fires alerts.

#### Q179: Can a member account leave an AWS Organization?
**A**: Yes, a member account can leave an organization if it has been configured with its own payment method and billing details, and if the organization policies permit removal.

#### Q180: What is AWS Systems Manager Run Command?
**A**: A management tool that allows administrators to execute shell/PowerShell scripts securely inside a fleet of EC2 instances or on-premises servers using the SSM Agent without requiring SSH/RDP connections.

#### Q181: How do you configure AWS Config to automatically remediate non-compliant resources?
**A**: Link an AWS Config rule to an **SSM Automation Document**. When a resource (e.g., an unencrypted S3 bucket) is marked non-compliant, AWS Config triggers the automation document to execute remediation steps (e.g., enabling S3 bucket encryption).

#### Q182: What is the difference between AWS Shield and AWS WAF?
**A**:
- **AWS Shield**: Protects against Layer 3 and Layer 4 volumetric network DDoS attacks (pings, syn floods).
- **AWS WAF**: Protects against Layer 7 application exploits (SQL injection, XSS, bad bot scraping).

#### Q183: What is the role of an IAM Role trust policy statement Principal?
**A**: The parameter in the trust policy JSON that specifies **which** entity (e.g., `ec2.amazonaws.com` or an account ARN) is authorized to assume the role.

#### Q184: What is an AWS KMS Key Alias?
**A**: A friendly, display name assigned to a KMS key ID (e.g., `alias/my-db-key`). Using an alias allows applications to refer to the key by name, allowing you to swap out the underlying key ID without changing application code.

#### Q185: Explain the purpose of Amazon GuardDuty "Delegated Administrator".
**A**: A feature in AWS Organizations that allows the master account to designate a specific security account to manage GuardDuty configurations and consolidate alerts for all member accounts.

#### Q186: What is AWS Network Firewall rule groups?
**A**: Reusable collections of stateless or stateful traffic-filtering rules (using Suricata syntax) that define how network packets traversing your subnets are audited or blocked.

#### Q187: Explain what an IAM Service Role is.
**A**: An IAM role that an AWS service assumes to perform actions in your account on your behalf (e.g., allowing Lambda to write logs to CloudWatch).

#### Q188: What is the difference between AWS IAM user credentials: Access Keys and Console Passwords?
**A**:
- **Console Password**: Used for interactive login to the AWS web console.
- **Access Keys**: A pair of strings (Access Key ID and Secret Access Key) used for programmatic authentication via the CLI, SDKs, or APIs.

#### Q189: What is the purpose of the AWS Systems Manager State Manager?
**A**: A configuration management service that automates the process of keeping your EC2 instances or on-premises servers in a defined target state (e.g., ensuring specific software is installed or antivirus is running).

#### Q190: What is AWS Security Hub compliance checking frequency?
**A**: Security Hub runs automated security checks against your resources daily to assess compliance with CIS and industry security standards.

#### Q191: How does AWS Secrets Manager handle automatic database credentials rotation?
**A**: It uses an **AWS Lambda function** that it runs at configured intervals. The Lambda function logs into the database, updates the password, saves the new password in Secrets Manager, and updates the application credentials.

#### Q192: What is AWS CloudTrail Data Events?
**A**: High-volume operations performed *on* or *within* a resource (e.g., S3 `GetObject` calls, Lambda `Invoke` API calls). These are disabled by default in CloudTrail to avoid log costs.

#### Q193: Explain what the AWS Billing Conductor does.
**A**: A billing customization service that allows enterprise customers to re-group billing data and compute custom pro-forma rates for subsidiary accounts or internal departments.

#### Q194: What is the purpose of the AWS Cost and Usage Report (CUR)?
**A**: The most comprehensive cost dataset available from AWS, exporting detailed hourly resource billing metadata to an S3 bucket for analysis via Athena or QuickSight.

#### Q195: What is Amazon Athena?
**A**: An interactive query service that allows you to analyze unstructured or semi-structured data directly in Amazon S3 using standard SQL, charging strictly per TB scanned.

#### Q196: Explain the AWS Service Catalog.
**A**: A governance tool allowing administrators to create, manage, and distribute catalogs of approved IT services (CloudFormation templates) to users, ensuring compliance while allowing self-service deployments.

#### Q197: How does AWS Organizations handle Service Control Policy (SCP) permissions inheritance?
**A**: SCPs use a filtering inheritance model. If a permission is denied at a parent OU level, it is blocked for all child OUs and member accounts underneath, even if a lower-level policy explicitly attempts to allow it.

#### Q198: Explain the difference between AWS KMS Key Administrator permissions and Key User permissions.
**A**:
- **Key Administrators**: Can manage the key (enable/disable, rotate, update policies, delete), but cannot encrypt or decrypt data.
- **Key Users**: Can use the key to encrypt, decrypt, and generate data keys, but cannot manage the key properties.

#### Q199: What is the purpose of the AWS Control Tower Landing Zone?
**A**: A pre-configured, secure multi-account environment built on AWS best practices, organizing accounts, federated access, and governance guardrails automatically.

#### Q200: Can you attach multiple permission boundaries to a single IAM role?
**A**: No. You can only assign a **single** permission boundary policy to an IAM user or role at any given time.

---

## Part 5: DevOps, Monitoring & Architectural Scenarios / Troubleshooting (Questions 201 - 250)

#### Q201: Describe the primary components of AWS CodePipeline.
**A**:
- **Source**: The starting stage that fetches source code changes (from GitHub, S3, or CodeCommit).
- **Build**: Compiles code, runs tests, and packages artifacts (typically using AWS CodeBuild).
- **Deploy**: Publishes the package package built to target infrastructure (typically using AWS CodeDeploy, CloudFormation, or ECS).
- **Stages**: Logical phases of the pipeline containing one or more actions.
- **Artifacts**: File archives passed between pipeline stages, stored in an S3 artifact bucket.

#### Q202: What is the difference between AWS CodeDeploy deployment configurations: Canary, Linear, and AllAtOnce?
**A**:
- **Canary**: Traffic is shifted in two increments. A small percentage (e.g., 10%) is shifted first, and the remaining 90% is shifted after a soak period (e.g., 10 minutes) if no alarms trigger.
- **Linear**: Traffic is shifted gradually in equal increments at equal time intervals (e.g., 10% every 3 minutes).
- **AllAtOnce**: All traffic is shifted to the new version instantly, maximizing deployment speed but offering no safety rollback window.

#### Q203: How do you configure a Terraform backend to manage state locks on AWS?
**A**:
1. Create a DynamoDB Table with a primary key named `LockID` (string).
2. Create an S3 bucket with versioning enabled.
3. Reference both in your Terraform backend block:
   ```hcl
   terraform {
     backend "s3" {
       bucket         = "my-tfstate-bucket"
       key            = "state/terraform.tfstate"
       region         = "us-east-1"
       dynamodb_table = "my-lock-table"
     }
   }
   ```
During execution, Terraform writes a lock record to DynamoDB, preventing concurrent runs.

#### Q204: What is AWS CloudFormation Drift Detection?
**A**: A feature that detects whether resources managed by a CloudFormation stack have been modified or deleted outside of CloudFormation control (e.g., manual edits in the Console), listing the specific parameters that have drifted.

#### Q205: Explain the difference between AWS CloudFormation StackSets and standard Stacks.
**A**:
- **Standard Stack**: Manages a set of resources within a single AWS account and region.
- **StackSets**: Allows you to deploy a single CloudFormation template to create resources across multiple AWS accounts and multiple regions concurrently, managed from a central account.

#### Q206: How do you write a CloudWatch Metric Filter to count specific error occurrences?
**A**: Define a Metric Filter on a CloudWatch Log Group using a filter pattern (e.g., `{ $.level = "ERROR" }` or `[ip, user, status_code=500, ...]`). The filter matches incoming log lines and increments a custom CloudWatch metric, which can trigger alarm notifications.

#### Q207: What is the difference between AWS System Manager Parameter Store and AWS AppConfig?
**A**:
- **Parameter Store**: A database key-value store for static environment variables and database keys.
- **AppConfig**: Designed for dynamic feature flagging and runtime configuration updates, supporting validators, gradual rollout strategies, and automatic rollback triggers.

#### Q208: Explain the four Disaster Recovery (DR) strategies in AWS, ordered by cost and RTO.
**A**:
1. **Backup & Restore**: High RTO (hours/days). Backups are stored in S3/Glacier and restored when needed. Low cost.
2. **Pilot Light**: Medium RTO (minutes/hours). Critical databases replicate continuously, but compute nodes (web servers) are only spun up (from AMIs) during disaster.
3. **Warm Standby**: Low RTO (minutes). A scaled-down version of the fully functional environment runs continuously, scaling up immediately during failover.
4. **Multi-Site (Active-Active)**: Near-zero RTO (seconds). Full replicas run concurrently in multiple regions, load balancing users globally. High cost.

#### Q209: What is AWS Application Migration Service (MGN), and how does it execute server migration?
**A**: MGN is the primary migration service. It installs an agent on source servers (on-premises or other clouds) that continuously replicates blocks to lightweight staging EC2 instances in AWS. When ready, it launches fully functional replica EC2 instances in your target VPC.

#### Q210: What is AWS Database Migration Service (DMS)?
**A**: A service that helps migrate databases to AWS quickly and securely, supporting homogenous migrations (e.g., Oracle to Oracle) and heterogeneous migrations (e.g., Oracle to Aurora PostgreSQL) using continuous data replication.

#### Q211: Troubleshooting: An EC2 instance shows high CPU load. How do you analyze the root cause from the terminal?
**A**:
1. SSH into the instance using Systems Manager Session Manager.
2. Run `top` or `htop` to identify the command processes consuming the most CPU.
3. Run `lsof -i :<port>` or `netstat -tulpn` to check network listeners.
4. Review the system and application logs inside `/var/log` (e.g., `/var/log/messages` or `/var/log/nginx/error.log`).

#### Q212: Troubleshooting: You deploy a new server, but HTTP requests from the internet timeout. What are your diagnostic steps?
**A**:
1. Check if the instance has a public IP address.
2. Verify the **Security Group** allows inbound traffic on port 80/443 from source `0.0.0.0/0`.
3. Check the subnet **NACL** rules to ensure they allow both inbound port 80/443 traffic and outbound ephemeral port return traffic.
4. Check the subnet **Route Table** to ensure it routes outbound traffic to an Internet Gateway (`0.0.0.0/0` -> `igw-xxxx`).

#### Q213: If an ALB returns a "502 Bad Gateway" error, what does this indicate, and how do you troubleshoot?
**A**: It indicates that the ALB was able to connect to the backend instances, but received an invalid or unparseable HTTP response. Troubleshooting:
1. Check the ALB **Target Group health status** metrics.
2. Confirm the backend application server is running and listening on the correct port.
3. Verify if web server headers are configured correctly (e.g., Nginx upstream parameters).
4. Inspect application logs on the target instances.

#### Q214: If an ALB returns a "504 Gateway Timeout" error, what does this indicate?
**A**: It indicates that the backend instance did not respond within the ALB's idle timeout period (default 60 seconds). This typically occurs when a database query or backend calculation takes too long to complete.

#### Q215: Troubleshooting: An ECS Fargate task immediately terminates after starting. What are your diagnostic steps?
**A**:
1. Go to the ECS console, select the cluster, open the **Tasks** tab, and set the status filter to **Stopped**.
2. Click on the stopped task and inspect the **Stopped Reason** field (e.g., "Essential container in task exited").
3. Check the container exit code (e.g., exit code 137 indicates out of memory; exit code 1 indicates application syntax error).
4. Review the log streams in CloudWatch Logs for the container tasks.

#### Q216: Scenario: Design a highly available web application across two AWS regions.
**A**:
- Deploy application instances on EC2 Auto Scaling Groups (or ECS Fargate) behind **ALBs** in both regions (e.g., `us-east-1` and `eu-west-1`).
- Configure a **Route 53 latency routing policy** pointing to both ALB endpoints.
- Store database records on a **DynamoDB Global Table** (active-active multi-region replication).
- Store media assets in **S3 buckets with cross-region replication** enabled.

#### Q217: Scenario: Secure database passwords for an app running on ECS Fargate.
**A**:
1. Save the database password inside **AWS Secrets Manager**.
2. Grant the ECS Task Execution Role read permissions on the secret in Secrets Manager.
3. In the ECS Task Definition JSON, reference the secrets manager ARN under the container `secrets` block, mapping it to a local environment variable. ECS will fetch and decrypt the secret at startup, keeping it secure.

#### Q218: Scenario: An application needs to scale up dynamically during a temporary Black Friday traffic surge. How do you implement this?
**A**: Configure target tracking scaling policies on your **EC2 Auto Scaling Groups** based on average CPU or ALB request counts. Set up **Aurora Auto Scaling** on your database cluster to automatically add read replicas if query loads surge. Enable CloudFront caching to offload static requests.

#### Q219: Scenario: A compliance audit requires you to store server activity logs for 7 years. How do you implement this?
**A**: Create an **S3 Lifecycle Policy** on your central logging bucket that automatically transitions log objects to the **Glacier Deep Archive** storage class after 30 days to optimize cost. Configure an **S3 Object Lock** in **Compliance Mode** with a retention period of 7 years to prevent anyone, including root, from deleting the log files.

#### Q220: Scenario: How would you isolate database instances from receiving direct internet traffic?
**A**: Place the database instances in a private subnet. Do not assign public IP addresses. Configure a security group on the database instances that allows inbound traffic *only* from the security group of the web servers on port 5432/3306.

#### Q221: Troubleshooting: A server inside a private subnet cannot resolve internal DNS names. What do you check?
**A**:
1. Check the VPC settings. Ensure **DNS resolution** (`enableDnsSupport`) and **DNS hostnames** (`enableDnsHostnames`) options are set to `true`.
2. Check if a private hosted zone in Route 53 is associated with that specific VPC.

#### Q222: Troubleshooting: You encounter an RDS PostgreSQL database connection timeout. What are your diagnostic steps?
**A**:
1. Verify if the database is in the same VPC.
2. Check the **RDS Security Group** to ensure it allows inbound traffic on port 5432 from the client server's security group or IP range.
3. Review the subnet NACL rules.
4. Ensure you are routing traffic to the correct RDS endpoint string.

#### Q223: What is the purpose of AWS App2Container?
**A**: A migration tool that scans and containerizes existing Java and .NET web applications running on servers, producing Dockerfiles, ECR repositories, and ECS/EKS deployment templates.

#### Q224: Explain what the AWS Lambda concurrency limit is.
**A**: The default regional concurrency limit for Lambda is **1,000 concurrent executions** across all functions in an account. This limit can be increased by submitting a support ticket.

#### Q225: What is the purpose of AWS Systems Manager State Manager?
**A**: A secure configuration management service that automates the process of keeping your virtual machines or on-premises servers in a defined target configuration state.

#### Q226: Troubleshooting: A Terraform plan fails with a "BucketAlreadyExists" error. How do you resolve this?
**A**: S3 bucket names are globally unique. You must edit your Terraform configuration file to change the bucket name parameter to a unique string, or import the existing bucket if it already belongs to your account.

#### Q227: Explain what AWS CloudTrail Insights does.
**A**: An automated threat intelligence tool that analyzes CloudTrail logs to identify anomalies (e.g., unusual API calls spikes) and flags them as insights in the console.

#### Q228: Scenario: You need to migrate 100 TB of files from an on-premises network to S3. What is the most efficient tool?
**A**: Use **AWS DataSync** over the network if high-speed bandwidth is available. If bandwidth is limited, request an **AWS Snowball Edge** physical storage device, copy the data locally, and ship it back to AWS to load directly into S3.

#### Q229: What is EKS Karpenter scaling advantage?
**A**: Karpenter rescales clusters much faster than standard autoscalers by skipping node groups. It queries the EC2 APIs directly to spin up custom instance sizes that fit the pending pods exactly, optimizing cost.

#### Q230: Troubleshooting: A developer reports they cannot view logs in CloudWatch. What IAM permission do they need?
**A**: They need the `logs:DescribeLogGroups`, `logs:DescribeLogStreams`, and `logs:GetLogEvents` permissions, or the managed role **CloudWatchReadOnlyAccess**.

#### Q231: Explain the purpose of Route 53 Resolver Rules.
**A**: They configure conditional DNS forwarding rules, allowing you to route DNS queries for local domains (e.g., `*.internal.company.com`) from your VPC to on-premises DNS servers.

#### Q232: Troubleshooting: A Lambda function terminates with a "Task timed out after 3.00 seconds" error. How do you fix it?
**A**: The default timeout for Lambda is 3 seconds. If your code needs more time (e.g., to fetch data from an external API), go to the function configuration settings and increase the timeout limit (up to 15 minutes).

#### Q233: What is the purpose of the CloudWatch Agent?
**A**: A software agent installed inside VM guest operating systems that collects system-level metrics (such as memory usage, disk swap space, and processes) that are not visible to the hypervisor, sending them to CloudWatch.

#### Q234: What is Amazon Simple Queue Service (SQS) FIFO queue?
**A**: A queue configuration that guarantees First-In-First-Out (FIFO) delivery ordering and strictly once-only processing, preventing duplicate messages from being processed.

#### Q235: Explain the difference between SQS and Amazon SNS.
**A**:
- **SQS**: A pull-based message queue service. Workers poll the queue to retrieve and process messages.
- **SNS**: A push-based pub/sub messaging service. It broadcasts messages instantly to all subscribed endpoints (HTTP, Email, Lambda, SQS).

#### Q236: Explain the difference between S3 Object Lock Governance Mode and Compliance Mode.
**A**:
- **Governance Mode**: Prevents most users from deleting or modifying objects, but users with specific permissions (like `s3:BypassGovernanceRetention`) can override the lock.
- **Compliance Mode**: Completely locks the object. No user, including the root account or AWS support, can bypass the retention period or delete the files.

#### Q237: What is AWS Network Firewall stateless vs stateful rules evaluation?
**A**:
- **Stateless Rules**: Evaluate packets individually in priority order, looking only at source/destination IPs and ports, similar to NACLs.
- **Stateful Rules**: Inspect packets in context of the connection flow (evaluating payloads, HTTP headers, URLs) using Suricata engines.

#### Q238: Troubleshooting: An Aurora MySQL database queries run slowly. What native AWS tool do you use to diagnose the bottleneck?
**A**: Enable **Performance Insights** on the database instance. It provides an easy-to-read dashboard showing database load by CPU wait times, SQL statements, and host clients, highlighting slow queries.

#### Q239: Scenario: A corporate policy requires all S3 objects to be encrypted with keys controlled by the security team. How do you implement this?
**A**: Create a customer-managed key (CMK) in KMS. Configure a bucket policy on S3 that denies any PUT upload request (`s3:PutObject`) that does not specify server-side encryption with KMS (`aws:kms`) and your specific KMS key ARN.

#### Q240: Explain the purpose of the AWS Transit Gateway route propagation.
**A**: A setting that allows attachments (VPCs, VPNs) to dynamically advertise their subnets and routing paths to the Transit Gateway route table over BGP, automating routing mesh configurations.

#### Q241: Troubleshooting: An administrator cannot delete an S3 bucket. What is the most likely cause?
**A**: The bucket is not empty. S3 blocks bucket deletions if it contains objects or older file versions (if versioning is enabled). You must empty the bucket first.

#### Q242: What is the purpose of the AWS CloudFormation template "Mappings" section?
**A**: It defines a lookup table of key-value pairs (e.g., mapping AMI IDs to different regions) allowing the template to dynamically select parameters based on variables.

#### Q243: Scenario: An application needs to run short-lived Docker containers that run for 5 minutes and shutdown. What is the most cost-effective hosting model?
**A**: **AWS Fargate** (running under ECS or EKS). Since Fargate charges strictly per-second for the vCPU and memory allocated during task execution, it eliminates idle VM server costs.

#### Q244: Explain what the Systems Manager Session Manager port forwarding feature does.
**A**: It allows you to establish a secure tunnel to forward local ports (e.g., local port 8080) to a port inside your private EC2 instances (e.g., database port 5432) over HTTPS without exposing public endpoints.

#### Q245: Troubleshooting: A Lambda function fails with an "OutOfMemory" exception. How do you resolve it?
**A**: Go to the function settings and increase the allocated memory (up to 10 GB). Note: Increasing memory also scales the virtual CPU allocation proportionally, which can improve execution times.

#### Q246: Explain what AWS Compute Optimizer does.
**A**: An AI-driven service that analyzes your resource metrics and recommends optimizations (e.g., suggesting smaller EC2 instance sizes, EBS changes, or Lambda settings) to reduce costs and improve performance.

#### Q247: Scenario: Design for zero data loss (RPO = 0) for a critical PostgreSQL database in AWS.
**A**: Deploy **Amazon Aurora PostgreSQL** with Multi-AZ replication. Aurora replicates data synchronously across three availability zones in the region before committing writes, ensuring zero data loss if an AZ fails.

#### Q248: Troubleshooting: How do you resolve a VPC Peering routing conflict?
**A**: You cannot peer VPCs with overlapping CIDRs. You must delete the overlapping subnet configuration and assign a new, non-overlapping IP address block to one of the VPCs, or route traffic through a NAT virtual appliance.

#### Q249: What is AWS Systems Manager Patch Baseline?
**A**: A set of rules defining which patches (security, critical updates) are approved for installation on your target EC2 instances, categorized by OS and severity.

#### Q250: Scenario: A company needs to deploy a private web application that can only be accessed from an on-premises network. How do you architect this?
**A**:
- Deploy the web application on **ECS Fargate** or **EC2**.
- Place the instances in private subnets and configure an **Internal ALB**.
- Connect the on-premises network to the VPC using a **Site-to-Site VPN** or **Direct Connect**.
- Configure private Route 53 DNS zones to resolve the application domain to the private ALB IP.




