# Cloud Engineer 250 Interview Questions & Answers - Part 2

This is Volume 2 of the Cloud Engineer Interview Guide, containing **Questions 91 to 170**. It covers Cloud Platform Services (VMs, disks, networking, load balancers) and Kubernetes Administration & Troubleshooting.

---

## 📋 Table of Contents (Part 2)
1.  [Cloud Platform Services (VMs, Networking, Load Balancers) (Q91 - Q130)](#1-cloud-platform-services-vms-networking-load-balancers-q91---q130)
2.  [Kubernetes Administration & Troubleshooting (Q131 - Q170)](#2-kubernetes-administration--troubleshooting-q131---q170)

---

## 1. Cloud Platform Services (VMs, Networking, Load Balancers) (Q91 - Q130)

#### Q91: What is a Google Cloud Compute Engine VM instance?
**Answer:** A fully managed virtual machine hosted on Google Cloud Platform's infrastructure, configurable with specific CPU architectures, memory footprints, operating systems, and disk mountings.

#### Q92: What is the difference between Local SSD and Persistent Disk in GCP?
**Answer:** 
*   **Local SSD**: Physically attached to the host machine running the VM, offering extremely high speed and low latency, but data is lost when the VM is stopped.
*   **Persistent Disk**: Network-attached storage that persists independently of the VM lifecycle, supporting snapshots and multi-reader mounts.

#### Q93: Explain what a Preemptible VM (or Spot VM) is.
**Answer:** Low-cost VM instances that Google can terminate at any time if they need the capacity back for other workloads. Spot VMs do not have a 24-hour runtime limit but have no uptime guarantees.

#### Q94: What is an Instance Template in GCP?
**Answer:** A resource definition template that defines machine type, boot image, subnets, labels, and startup scripts, used to create groups of identical VMs.

#### Q95: Explain Managed Instance Groups (MIGs).
**Answer:** A collection of identical VM instances created from an Instance Template, supporting auto-healing, auto-scaling, load balancing integration, and rolling updates.

#### Q96: What is a VPC (Virtual Private Cloud)?
**Answer:** A private, isolated network space within GCP where you can define IP address ranges, subnets, routers, firewalls, and route tables.

#### Q97: What is the difference between regional and global VPC resources?
**Answer:** 
*   **Regional**: Resources bound to a specific geographic region (e.g., subnets, static regional IP allocations).
*   **Global**: Available across all regions globally (e.g., VPC networks, global load balancers).

#### Q98: Explain VPC Network Peering.
**Answer:** A connection that links two VPCs privately, allowing VMs in both networks to communicate using internal IPs with low latency. (Non-transitive and cannot have overlapping subnets).

#### Q99: What is a Shared VPC?
**Answer:** A network architecture where a Host Project manages the core VPC network, subnets, and firewalls, and Service Projects deploy VM instances attached to those subnets.

#### Q100: Explain Private Google Access (PGA).
**Answer:** A subnet-level feature that allows virtual machines that only have private IP addresses to access Google Cloud APIs and services over their internal IPs.

#### Q101: What is Google Cloud NAT?
**Answer:** A regional network service that allows private VM instances without external public IPs to connect outbound to the internet for updates or API calls, while blocking incoming internet connections.

#### Q102: What is a Cloud Router?
**Answer:** A regional Google Cloud service that enables dynamic routing using BGP to advertise and learn IP prefixes between your GCP VPC and an on-premises network.

#### Q103: Explain High Availability (HA) VPN.
**Answer:** A cloud VPN service that provides a 99.99% service availability SLA. It uses a single gateway with two external interfaces, creating two independent IPsec tunnels using dynamic BGP routing.

#### Q104: What is Google Cloud Interconnect?
**Answer:** A high-bandwidth physical connection between on-premises networks and Google's network edge:
*   **Dedicated Interconnect**: Direct fiber connection at a Google colocation facility (10G/100G).
*   **Partner Interconnect**: Connection through a supported network service provider (50M to 50G).

#### Q105: What is Private Service Connect (PSC)?
**Answer:** A GCP feature that allows private, secure consumption of services (like managed databases or Google APIs) across different VPCs using internal IP addresses, without requiring VPC Peering.

#### Q106: What are the target options for GCP Firewall Rules?
**Answer:** Targets define which instances a firewall rule applies to. Options include applying to all instances in the VPC, instances matching specific Network Tags, or instances bound to a specific Service Account (recommended).

#### Q107: What is Google Cloud Armor?
**Answer:** Google's Web Application Firewall (WAF) and DDoS protection service that integrates with External HTTP(S) Load Balancers to inspect and filter web traffic.

#### Q108: What is a Global Load Balancer vs. Regional Load Balancer?
**Answer:** 
*   **Global**: Distribute traffic across backends in multiple regions worldwide using a single external IP address.
*   **Regional**: Distribute traffic within a single region, providing regional isolation.

#### Q109: Explain SSL Offloading (SSL Termination) on Load Balancers.
**Answer:** Decrypting incoming SSL/TLS encrypted traffic at the load balancer level before forwarding the unencrypted HTTP requests to backend servers, reducing processor load on the backend.

#### Q110: What is Session Affinity (Sticky Sessions) in load balancing?
**Answer:** A setting that routes all sequential requests from a specific user session to the same backend server, which is useful for stateful applications.

#### Q111: What is a Health Check in Load Balancers?
**Answer:** Periodic probes sent by the load balancer to backend servers to verify they are responsive; unresponsive servers are removed from the routing pool.

#### Q112: What is Google Cloud CDN?
**Answer:** A globally distributed network of edge cache nodes that caches static web assets close to users, reducing latency and load on origin servers.

#### Q113: What is an Edge Cache PoP (Point of Presence)?
**Answer:** A physical location where Google connects its network to the rest of the internet, hosting CDN caches and routing user traffic into the Google backbone.

#### Q114: What is a "ProxyOnly" subnet in GCP?
**Answer:** A dedicated subnet containing proxy IP addresses used by Google's Regional Internal HTTP(S) Load Balancers to communicate with backend instances.

#### Q115: What is dynamic routing in GCP VPC networks?
**Answer:** A configuration (regional or global) that enables Cloud Routers to automatically discover and propagate IP prefix changes across subnets and VPN tunnels.

#### Q116: What is the risk of overlapping IP subnets when planning hybrid cloud connections?
**Answer:** Overlapping subnets cause IP conflicts, preventing routers from determining the correct destination for traffic, resulting in dropped packets.

#### Q117: What is a "Static Route"?
**Answer:** A manual route rule defined in a VPC table that specifies the exact gateway or next-hop IP for a destination prefix.

#### Q118: What is VPC Flow Logs?
**Answer:** A monitoring feature that records network traffic telemetry (IP addresses, ports, protocols, packet counts) passing through subnet interfaces for audit and troubleshooting.

#### Q119: What is the difference between public and private DNS zones?
**Answer:** 
*   **Public**: DNS zones accessible from the internet.
*   **Private**: DNS zones accessible only to resources connected inside a specific VPC network.

#### Q120: What is a "Direct Peering" connection?
**Answer:** A private network peering connection established between Google's edge routers and an enterprise network without going through a public exchange or VPN.

#### Q121: What is the difference between standard and premium network tiers in GCP?
**Answer:** 
*   **Premium**: Routes user traffic over Google's global fiber backbone network, entering at the Edge PoP closest to the user.
*   **Standard**: Routes user traffic over the public internet, entering Google's network at the Edge PoP closest to the target GCP region.

#### Q122: What is Cloud SQL Auth Proxy?
**Answer:** A secure tunnel utility that runs locally on application servers, authenticating and encrypting connections to Cloud SQL databases using IAM credentials, eliminating the need for static database IP whitelists.

#### Q123: What is "Resource Hierarchy" in Google Cloud?
**Answer:** The logical structure used to organize GCP resources: Organization -> Folders -> Projects -> Resources. IAM permissions inherit downwards from the organization level.

#### Q124: What is an IAM Policy?
**Answer:** A JSON/YAML file attached to a resource that defines the bindings of members (identities) to roles, controlling access permissions.

#### Q125: What is the difference between a User Account and a Service Account in GCP?
**Answer:** 
*   **User Account**: Represents a human operator authenticated via username/password and MFA.
*   **Service Account**: Represents an application, service, or machine identity authenticated via keys or token federation (Workload Identity).

#### Q126: What is the Principle of Least Privilege (PoLP)?
**Answer:** A security practice where users, service accounts, and processes are granted only the minimum permissions necessary to perform their specific tasks, reducing the blast radius of a credential leak.

#### Q127: How does Google Cloud Secret Manager protect client credentials?
**Answer:** It stores sensitive strings (passwords, keys) encrypted at rest, integrates with IAM policies to restrict access, versions secrets automatically, and logs access events for audits.

#### Q128: What is the risk of hardcoding API keys in application source code?
**Answer:** Hardcoded keys are stored in plaintext and can easily be leaked to public repositories, compromised in build artifacts, or accessed by unauthorized developers. Use Secret Manager instead.

#### Q129: Explain "Confidential Computing" in Google Cloud.
**Answer:** An option that encrypts data in-memory while it is actively processed by the CPU, protecting workloads from node compromise.

#### Q130: What is a "Data Perimeter" in cloud security?
**Answer:** A security boundary that prevents unauthorized systems or networks from accessing data, even if they have valid IAM credentials.

---

## 2. Kubernetes Administration & Troubleshooting (Q131 - Q170)

#### Q131: What is a Pod in Kubernetes?
**Answer:** The smallest deployable unit in Kubernetes, which can host one or more containers sharing the same network namespace and storage volumes.

#### Q132: Explain the role of the Kubelet.
**Answer:** An agent running on each worker node that receives PodSpecs from the API server and ensures that the designated containers are running and healthy inside the node.

#### Q133: What is the difference between GKE Standard and GKE Autopilot?
**Answer:** 
*   **GKE Standard**: Gives the engineer full control over node provisioning, operating systems, and custom VM size selections.
*   **GKE Autopilot**: Automatically provisions and manages nodes, scales the cluster based on active pod demands, applies security hardening, and charges only for running pod CPU/Memory footprints.

#### Q134: What is Workload Identity, and how does it secure GKE workloads?
**Answer:** A feature that maps Kubernetes Service Accounts (KSA) inside a cluster directly to Google Cloud Service Accounts (GSA), allowing GKE pods to authenticate to GCP APIs (like Vertex AI or BigQuery) using temporary, automatically rotated tokens.

#### Q135: How do you configure resource requests and resource limits for agent pods?
**Answer:** Under the pod specs container section, configure:
*   `requests`: CPU and Memory guarantees used by the scheduler to place pods.
*   `limits`: Maximum resource bounds; if an agent pod exceeds its memory limits, the kernel kills it with an **OOMKilled** (Out of Memory) exception.

#### Q136: What is the difference between a Deployment and a StatefulSet?
**Answer:** 
*   **Deployment**: Manages stateless pods where instances are identical, exchangeable, and assigned random hostnames.
*   **StatefulSet**: Manages stateful pods where each instance gets a persistent, ordinal identifier (e.g. `agent-db-0`) and binds to its own dedicated persistent volume.

#### Q137: Explain the purpose of a DaemonSet.
**Answer:** It ensures that every single node in the cluster runs a copy of a designated pod (typically used for log forwarding, network routing, or node metrics monitoring).

#### Q138: What is a K8s Service, and what are its types?
**Answer:** An abstraction to expose an application running on a set of Pods as a network service. Types include ClusterIP (internal), NodePort (static port on nodes), LoadBalancer (cloud external load balancer), and ExternalName (DNS CNAME).

#### Q139: Explain the role of the Ingress resource and Ingress Controller.
**Answer:** The Ingress resource is a set of routing rules (HTTP/HTTPS) that exposes services to external traffic. The Ingress Controller (like NGINX or Google Cloud HTTP Load Balancer) acts as the reverse proxy that executes those routing rules.

#### Q140: What are Liveness and Readiness Probes in K8s?
**Answer:** 
*   **Liveness**: Determines if a container needs to be restarted. If it fails, Kubernetes kills the container and restarts it.
*   **Readiness**: Determines if a container is ready to accept network traffic. If it fails, the pod is removed from Service endpoint lists.

#### Q141: What is a Startup Probe, and why is it useful for heavy models?
**Answer:** A probe that checks if the application has completed its startup routine. It disables liveness and readiness checks until startup succeeds, preventing slow-starting containers (like those loading heavy weights) from getting killed during boot.

#### Q142: What is etcd?
**Answer:** A consistent, highly available distributed key-value store used as Kubernetes' storage backend for all cluster state and configuration data.

#### Q143: What is a ConfigMap vs a K8s Secret?
**Answer:** 
*   **ConfigMap**: Stores non-confidential configuration key-value blocks.
*   **Secret**: Stores sensitive data (keys, database passwords) encoded in base64, which can be encrypted at rest in etcd.

#### Q144: What is Horizontal Pod Autoscaler (HPA)?
**Answer:** A controller that automatically adjusts the replica count of a deployment or statefulset based on observed CPU utilization, memory thresholds, or custom metrics.

#### Q145: Explain Node Affinity.
**Answer:** A set of scheduling rules that constrains which nodes your Pod can schedule on, based on key-value labels defined on the nodes.

#### Q146: What are Taints and Tolerations?
**Answer:** 
*   **Taints**: Node configurations that repel sets of pods.
*   **Tolerations**: Pod configurations that allow (but do not force) pods to schedule on nodes with matching taints.

#### Q147: What is a Kubernetes Namespace?
**Answer:** A logical partition inside a single cluster used to organize resources, enforce scope boundaries, and isolate environments.

#### Q148: What is a Sidecar Container?
**Answer:** A utility container that runs alongside the main application container inside the same pod, handling helper tasks like logging, security proxying (mTLS), or configuration syncing.

#### Q149: What is Helm?
**Answer:** A package manager for Kubernetes that templates YAML manifests into structured packages called Charts, simplifying deployment, upgrades, and versioning.

#### Q150: What is a NetworkPolicy in Kubernetes?
**Answer:** A resource that acts as a Layer 3/4 firewall inside the cluster, defining rules that control traffic flow between pod groups.

#### Q151: What is a Service Mesh (e.g., Istio)?
**Answer:** An infrastructure layer that manages service-to-service communication, providing load balancing, traffic splitting, mutual TLS encryption (mTLS), and detailed observability.

#### Q152: Explain the CrashLoopBackOff error and how to debug it.
**Answer:** An error indicating a pod starts, crashes, and starts again repeatedly, forcing Kubernetes to delay restarts. Debug it by reviewing application logs (`kubectl logs pod_name -p`) and checking for configuration errors, missing environment variables, or database connection failures.

#### Q153: What causes an OOMKilled error?
**Answer:** The Linux kernel Out-Of-Memory killer terminates the container because it consumed more memory than the limit defined in its PodSpec configuration.

#### Q154: How do you check the event logs of a specific namespace?
**Answer:** Run the command: `kubectl get events -n namespace_name --sort-by='.metadata.creationTimestamp'`.

#### Q155: What does `kubectl describe pod pod_name` do?
**Answer:** Displays detailed metadata, active state, status events (scheduling, pulling images, container starts), IP addresses, and resource constraints of a specific pod.

#### Q156: How do you run a shell session inside a running pod container?
**Answer:** Run: `kubectl exec -it pod_name -c container_name -- /bin/sh`.

#### Q157: What is the purpose of `kubectl port-forward`?
**Answer:** It maps a local network port on your development machine directly to a target port on a pod or service inside the Kubernetes cluster, allowing private testing.

#### Q158: What is a PersistentVolume (PV) vs a PersistentVolumeClaim (PVC)?
**Answer:** 
*   **PV**: A storage resource in the cluster provisioned by an administrator or dynamically via StorageClasses.
*   **PVC**: A request for storage by a user/Pod. It defines size and access modes, and Kubernetes binds it to an available PV matching the criteria.

#### Q159: What does the `imagePullPolicy: Always` configuration enforce?
**Answer:** It tells the kubelet to always query the container registry to pull the image manifest before launching a container, ensuring it runs the latest image commit tag.

#### Q160: Explain kube-proxy.
**Answer:** A network agent running on each cluster node that manages IP tables or IPVS rules to load balance and route network traffic to Services.

#### Q161: What is an Init Container?
**Answer:** A specialized container that runs and completes its execution before the main application containers start, typically used to run database migrations or fetch configuration files.

#### Q162: What is the role of the Kube-Scheduler?
**Answer:** A control plane component that checks resource requests of unscheduled pods and assigns them to the node that best satisfies their CPU/Memory constraints.

#### Q163: How do you drain a node for maintenance?
**Answer:** First run `kubectl cordon node_name` to mark it as unschedulable, then run `kubectl drain node_name --ignore-daemonsets --delete-emptydir-data` to safely evict all running pods.

#### Q164: What is a Pod Disruption Budget (PDB)?
**Answer:** A configuration that limits the number of pods of a replicated application that can be down simultaneously during voluntary disruptions (like node upgrades), ensuring service availability.

#### Q165: What does the `kubectl logs --tail=100 -f pod_name` command do?
**Answer:** It displays the last 100 lines of stdout/stderr logs from the target pod and streams new log outputs in real-time.

#### Q166: What is a Kubernetes HPA metric source?
**Answer:** A source that feeds metrics to the Horizontal Pod Autoscaler, which can be standard resource metrics (CPU/Memory from Metrics Server) or custom external metrics (from Prometheus or GCP Monitoring).

#### Q167: Explain CNI (Container Network Interface).
**Answer:** A standard specification and library framework used by container runtimes to configure network interfaces, assign IPs, and manage routing tables for pods (e.g., Calico, Flannel).

#### Q168: How do you update a ConfigMap mounted as a volume without restarting the Pod?
**Answer:** Edit the ConfigMap (`kubectl edit configmap name`). Kubernetes updates the mounted files inside the container automatically in the background (usually within a few minutes). The application must support reloading configurations dynamically.

#### Q169: What does `kubectl get pods --all-namespaces` show?
**Answer:** Lists all pods running in the cluster across all namespaces, including system namespaces like `kube-system`.

#### Q170: Explain Pod Security Admission (PSA).
**Answer:** A built-in admission controller that evaluates PodSpecs against predefined security standards (Privileged, Baseline, Restricted) to restrict access to host namespaces and directories.
