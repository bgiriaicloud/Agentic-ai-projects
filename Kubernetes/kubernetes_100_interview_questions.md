# Kubernetes 100 Interview Questions & Answers

This document contains 100 essential interview questions and answers for Kubernetes administrators, cloud engineers, and DevOps architects.

---

## 📋 Table of Contents
1.  [Kubernetes Core Architecture & Concepts (Q1 - Q30)](#1-kubernetes-core-architecture--concepts-q1---q30)
2.  [Pod Scheduling, Workloads & Controllers (Q31 - Q60)](#2-pod-scheduling-workloads--controllers-q31---q60)
3.  [Kubernetes Networking & Services (Q61 - Q80)](#3-kubernetes-networking--services-q61---q80)
4.  [Storage, Config & Security Hardening (Q81 - Q100)](#4-storage-config--security-hardening-q81---q100)

---

## 1. Kubernetes Core Architecture & Concepts (Q1 - Q30)

#### Q1: What is Kubernetes?
**Answer:** An open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications.

#### Q2: What is the main purpose of the Kubernetes Control Plane?
**Answer:** It manages the global state of the cluster, makes scheduling decisions, detects and responds to cluster events, and maintains desired cluster configurations.

#### Q3: What is the API Server (`kube-apiserver`)?
**Answer:** The core front-end entry point of the control plane that exposes the Kubernetes API. It validates and configures data for state objects (Pods, Services, ReplicationControllers).

#### Q4: Explain the role of `etcd`.
**Answer:** A highly available, consistent distributed key-value store used as Kubernetes' backing database for all cluster state configurations and metadata.

#### Q5: What is the Kubernetes Scheduler (`kube-scheduler`)?
**Answer:** A control plane component that watches for newly created Pods with no assigned node, selects the optimal node for them to run on based on resource availability, constraints, and affinity rules.

#### Q6: What is the Controller Manager (`kube-controller-manager`)?
**Answer:** A daemon that runs core control loops (e.g., Node Controller, Job Controller, Endpoint Controller) to regulate the state of the cluster and bring the actual state closer to the desired state.

#### Q7: What is the Cloud Controller Manager?
**Answer:** A control plane component that embeds cloud-specific control logic, linking the cluster to the cloud provider's API (e.g., managing load balancers, route tables, and instances).

#### Q8: What runs on a Kubernetes Worker Node?
**Answer:** The Kubelet agent, Kube-Proxy network proxy, and the container runtime (e.g., containerd) that downloads and runs container images.

#### Q9: What is the Kubelet?
**Answer:** An agent running on each worker node that receives PodSpecs from the API Server and ensures that the designated containers are running and healthy inside their Pods.

#### Q10: What is Kube-Proxy?
**Answer:** A network agent running on each node that maintains network rules, allowing network communication to Pods from inside or outside the cluster.

#### Q11: What is a Container Runtime?
**Answer:** The software responsible for downloading container images and running the containers (e.g., containerd, CRI-O).

#### Q12: What is a Pod?
**Answer:** The smallest deployable computing unit in Kubernetes, hosting one or more containers that share storage, network IP address space, and port mappings.

#### Q13: What is a Sidecar Container?
**Answer:** A helper container that runs alongside the main application container within the same Pod to handle utility tasks (e.g., logging, proxying, metric aggregation).

#### Q14: Explain what Init Containers are.
**Answer:** Specialized containers that run and complete their execution sequentially before the main application containers start, typically used to run database setup scripts or fetch configs.

#### Q15: What is a Namespace?
**Answer:** A virtual partition within a physical Kubernetes cluster used to isolate resources, enforce scope limits, and divide cluster usage among multiple teams.

#### Q16: What is a Declarative Configuration?
**Answer:** Specifying the desired final state of resources in YAML/JSON manifests, leaving Kubernetes controllers to execute the necessary operations to achieve and maintain that state.

#### Q17: What is an Imperative Configuration?
**Answer:** Giving explicit step-by-step commands to the cluster (e.g., using `kubectl run` or `kubectl scale`) to modify the state immediately.

#### Q18: What does `kubectl` do?
**Answer:** The official command-line interface tool used to communicate with the Kubernetes API Server to manage and query cluster resources.

#### Q19: What is the difference between a node and a cluster?
**Answer:** A Node is a single physical or virtual worker machine, whereas a Cluster is the aggregated group of control planes and worker nodes working together.

#### Q20: Explain the Pod lifecycle phases.
**Answer:** The phases are: `Pending` (scheduling in progress), `Running` (at least one container is active), `Succeeded` (completed successfully), `Failed` (terminated with error), and `Unknown` (node status lost).

#### Q21: What is the role of the Container Runtime Interface (CRI)?
**Answer:** A standard plugin interface that allows the Kubelet to communicate with various container runtimes without needing to recompile cluster binaries.

#### Q22: What is the difference between `apiGroup` and `apiVersion` in Kubernetes manifests?
**Answer:** `apiVersion` defines the version of the API schema, while `apiGroup` organizes related resources into logical groupings (e.g., `apps`, `networking.k8s.io`).

#### Q23: What is a Custom Resource Definition (CRD)?
**Answer:** A powerful extension mechanism that allows engineers to define custom, user-made resource types in the Kubernetes API.

#### Q24: What is an Operator in Kubernetes?
**Answer:** A design pattern that combines Custom Resource Definitions (CRDs) with custom Controllers to automate the management of complex, stateful applications.

#### Q25: How does Kubernetes check node health?
**Answer:** The Kubelet sends periodic node status updates to the API Server. If updates stop, the Node Controller marks the node as `NotReady` or `Unknown`.

#### Q26: What is the "kube-system" namespace?
**Answer:** A default namespace reserved for core system components created by the Kubernetes control plane (e.g., DNS, proxies, CNI plug-ins).

#### Q27: What is a "Static Pod"?
**Answer:** A Pod managed directly by the Kubelet daemon on a specific node, bypassing the API Server and control plane scheduler. They are configured via files in a local directory.

#### Q28: How do you view cluster-wide resource utilization stats?
**Answer:** Run `kubectl top nodes` and `kubectl top pods` (requires the Metrics Server to be active).

#### Q29: What is "Garbage Collection" in Kubernetes?
**Answer:** An automatic cleanup mechanism that deletes orphaned resources, dead containers, unused container images, and resources whose owner reference is missing.

#### Q30: What is the purpose of the "kubectl config" command?
**Answer:** It manages access configurations, allowing users to switch between different Kubernetes clusters (contexts), namespaces, and user credentials.

---

## 2. Pod Scheduling, Workloads & Controllers (Q31 - Q60)

#### Q31: What is a ReplicaSet?
**Answer:** A controller that maintains a stable set of replica Pods running at any given time, ensuring application availability.

#### Q32: Explain the role of a Deployment.
**Answer:** A declarative object that manages ReplicaSets, providing rolling updates, rollbacks, and self-healing scaling for stateless applications.

#### Q33: What is a StatefulSet?
**Answer:** A controller used to manage stateful workloads, providing unique, persistent ordinal network identifiers (e.g., `db-0`, `db-1`) and dedicated persistent volumes.

#### Q34: What is a DaemonSet?
**Answer:** A controller that ensures all (or specific) nodes in the cluster run a single copy of a designated Pod (used for log forwarding, metric exporters, or proxy routing).

#### Q35: What is the difference between a Job and a CronJob?
**Answer:** A Job runs one or more Pods to completion (batch tasks), while a CronJob schedules Jobs to run at specific recurring times using cron syntax.

#### Q36: Explain the difference between Resource Requests and Resource Limits.
**Answer:** 
*   **Requests**: The minimum CPU and memory GKE/K8s guarantees and uses to schedule a Pod on a node.
*   **Limits**: The maximum bounds; if a Pod exceeds memory limits, the kernel kills it with an OOMKilled exception.

#### Q37: What is a NodeSelector?
**Answer:** A simple scheduling constraint that matches Pod label selectors to specific node key-value labels to assign Pod placement.

#### Q38: What is Node Affinity?
**Answer:** A flexible scheduling feature (hard or soft rules) that controls Pod node placement using logical selectors, operators (In, NotIn, Exists), and weight scores.

#### Q39: What is Pod Co-affinity (Affinity and Anti-affinity)?
**Answer:** Rules that determine if Pods should be scheduled close to each other (affinity) or kept apart (anti-affinity) on different nodes or availability zones.

#### Q40: What are Taints and Tolerations?
**Answer:** 
*   **Taints**: Node configurations that repel sets of Pods.
*   **Tolerations**: Pod configurations that allow (but do not force) Pods to schedule on nodes with matching taints.

#### Q41: Explain Pod Disruption Budgets (PDB).
**Answer:** A configuration that defines the minimum number of available Pod replicas that must remain healthy during voluntary disruptions (e.g., node drains, upgrades).

#### Q42: What happens when you run `kubectl drain <node-name>`?
**Answer:** The node is cordoned (marked unschedulable), and all active Pods are gracefully evicted and rescheduled onto other healthy nodes.

#### Q43: What is "Self-Healing" in Kubernetes?
**Answer:** The capability of controllers to detect failed Pods or nodes and automatically restart, reschedule, or recreate instances to match the desired state.

#### Q44: Explain "Rolling Updates" in Deployments.
**Answer:** A rollout strategy that updates Pod instances gradually, replacing old versions with new ones, ensuring zero-downtime service availability.

#### Q45: What does `kubectl rollout undo` do?
**Answer:** Reverts a deployment to its previous stable revision, undoing a failed application release.

#### Q46: What is a Pod's Quality of Service (QoS) class?
**Answer:** A class (`Guaranteed`, `Burstable`, `BestEffort`) assigned by Kubernetes based on request and limit configurations, determining eviction priority during node saturation.

#### Q47: What is Horizontal Pod Autoscaler (HPA)?
**Answer:** A controller that dynamically increases or decreases the number of Pod replicas in a deployment based on CPU utilization or custom metrics.

#### Q48: What is Vertical Pod Autoscaler (VPA)?
**Answer:** A controller that automatically sets CPU and memory requests/limits for container configurations based on historical usage analysis.

#### Q49: What is Cluster Autoscaler?
**Answer:** A component that automatically scales the physical node pool size up when Pods are unschedulable due to resource deficits, and scales nodes down when they are underutilized.

#### Q50: How do you force a Pod to restart without changing code?
**Answer:** Run `kubectl rollout restart deployment/deployment_name` to trigger a rolling update.

#### Q51: What is a Cordon operation?
**Answer:** Marking a node as unschedulable, preventing new Pods from being assigned to it while leaving existing running Pods unaffected.

#### Q52: What is the default update strategy for a StatefulSet?
**Answer:** `RollingUpdate`, which deletes and recreates Pods one at a time in reverse ordinal order (e.g., from `db-2` down to `db-0`).

#### Q53: Explain the difference between `Preemptible` nodes and standard nodes in GKE scheduling.
**Answer:** Preemptible nodes are short-lived, cheaper instances that can be reclaimed at any time, requiring Pods to handle quick terminations.

#### Q54: What does the error `ImagePullBackOff` mean?
**Answer:** The container runtime tried to pull an image but failed (due to wrong tag name, non-existent registry, or authorization failure), and Kubernetes is backing off retrying.

#### Q55: How do you troubleshoot a Pod stuck in the `Pending` state?
**Answer:** Run `kubectl describe pod <pod_name>` to inspect scheduler events. Common causes include insufficient CPU/memory on nodes or unmet node selectors/taints.

#### Q56: What is the purpose of the `terminationGracePeriodSeconds` field?
**Answer:** The time (default: 30s) Kubernetes grants to a Pod to shut down gracefully after receiving a `SIGTERM` signal, before sending a force-kill `SIGKILL` signal.

#### Q57: What is the difference between `recreate` and `rollingUpdate` deployment strategies?
**Answer:** `Recreate` terminates all existing Pods before starting new ones (causes downtime). `RollingUpdate` rolls out new Pods incrementally (zero downtime).

#### Q58: What is a Headless Service?
**Answer:** A Service with `clusterIP: None` that does not load-balance traffic, returning direct A-records of member Pod IPs, commonly used in stateful databases.

#### Q59: What is the role of the EndpointSlice resource?
**Answer:** A scalable resource that tracks network endpoints within a cluster, grouping Pod IPs and ports for backend routing efficiency.

#### Q60: Explain how a Pod's priority class affects scheduling.
**Answer:** High-priority Pods can preempt (evict) lower-priority Pods if node resource limits are reached, ensuring critical system agents run.

---

## 3. Kubernetes Networking & Services (Q61 - Q80)

#### Q61: What is a Kubernetes Service?
**Answer:** An abstraction that defines a logical set of Pods and a policy to access them, providing stable IP addresses and DNS entry points.

#### Q62: What is `ClusterIP`?
**Answer:** The default Service type that exposes the Service on an internal IP address inside the cluster, making it accessible only within the cluster.

#### Q63: Explain what a `NodePort` Service is.
**Answer:** Exposes the Service on a static port (between 30000 and 32767) on each node's IP, allowing external traffic to access it using `<NodeIP>:<NodePort>`.

#### Q64: What is a `LoadBalancer` Service?
**Answer:** Exposes the Service externally using a cloud provider's external load balancer, automatically routing traffic to NodePorts and Pods.

#### Q65: What is `ExternalName`?
**Answer:** A Service type that maps a Kubernetes service to an external DNS CNAME record (e.g., database endpoint) without routing traffic through proxies.

#### Q66: What is an Ingress resource?
**Answer:** A collection of rules (L7 HTTP/HTTPS routing configurations) that allows external traffic to access cluster Services based on hosts and paths.

#### Q67: Explain the role of an Ingress Controller.
**Answer:** The active daemon (e.g., NGINX, HAProxy, GCE) that runs inside the cluster to implement the rules defined in Ingress resources.

#### Q68: What is CoreDNS in Kubernetes?
**Answer:** The default cluster-level DNS server that resolves service names to their respective ClusterIP addresses automatically.

#### Q69: Explain the container-to-container network model.
**Answer:** Containers inside the same Pod share the same network namespace, loopback interface (`localhost`), and ports, allowing direct communication.

#### Q70: Explain the Pod-to-Pod network model.
**Answer:** Every Pod is assigned a unique IP address within the cluster, and Pods can communicate with all other Pods on other nodes directly without NAT translation.

#### Q71: What is a CNI (Container Network Interface) plugin?
**Answer:** A network plugin that sets up network interfaces, routing tables, and IP allocations for newly spawned Pods (e.g., Calico, Flannel, Cilium).

#### Q72: What is kube-proxy "iptables" mode?
**Answer:** Kube-proxy writes netfilter iptables rules on nodes to capture traffic bound for a Service IP and redirect it to a backend Pod IP.

#### Q73: What is kube-proxy "IPVS" mode?
**Answer:** An alternative routing mode that uses IP Virtual Server (L4 load balancing built into the Linux kernel), offering faster throughput and scale capabilities for large clusters.

#### Q74: What is a NetworkPolicy?
**Answer:** A resource that acts as an in-cluster firewall, defining ingress and egress rules to control traffic flow between Pod groups.

#### Q75: By default, are Pod networks isolated?
**Answer:** No. By default, Pod networking is non-isolated; all Pods can accept traffic from any source. Once a NetworkPolicy selects a Pod, it blocks unpermitted connections.

#### Q76: What does the `serviceName.namespace.svc.cluster.local` DNS structure mean?
**Answer:** The standard FQDN for a Service inside a cluster: `serviceName` is the resource name, `namespace` is its namespace, `svc` marks it as a service, and `cluster.local` is the domain.

#### Q77: What is Service Mesh?
**Answer:** An infrastructure layer (e.g., Istio) that manages service-to-service communication, handling mutual TLS (mTLS), load balancing, and tracing.

#### Q78: Explain "mTLS" (Mutual TLS) in a Service Mesh.
**Answer:** Encrypted tunnel communication between Pod sidecars where both client and server authenticate each other's certificates, securing data-in-transit.

#### Q79: What is the purpose of the `ports.targetPort` field in a Service manifest?
**Answer:** `targetPort` is the port number the container application listens on inside the Pod, whereas `port` is the port exposed by the Service.

#### Q80: How does an external load balancer verify GKE backend health?
**Answer:** It queries GKE NodePort health check paths; kube-proxy intercepts and responds based on active container endpoint health.

---

## 4. Storage, Config & Security Hardening (Q81 - Q100)

#### Q81: What is a PersistentVolume (PV)?
**Answer:** A storage resource in the cluster provisioned by an administrator or dynamically via StorageClasses. It is independent of the lifecycle of individual Pods.

#### Q82: What is a PersistentVolumeClaim (PVC)?
**Answer:** A user's request for storage. It defines size, access modes (ReadWriteOnce, ReadOnlyMany, ReadWriteMany), and binds to a matching PV.

#### Q83: Explain the role of a StorageClass.
**Answer:** A resource that defines different storage types (e.g., standard HDD, SSD) and enables dynamic provisioning of PersistentVolumes when a PVC is created.

#### Q84: What is a ConfigMap?
**Answer:** An API resource used to store non-confidential configuration data in key-value pairs, which can be injected into containers as env variables or files.

#### Q85: What is a Kubernetes Secret?
**Answer:** An API resource used to store sensitive data (keys, passwords) encoded in Base64, which can be mounted as volumes or variables.

#### Q86: Explain RBAC (Role-Based Access Control).
**Answer:** A security framework that regulates access to Kubernetes API resources based on the roles assigned to users, groups, or Service Accounts.

#### Q87: What is the difference between a Role and a ClusterRole?
**Answer:** 
*   **Role**: Defines API access permissions within a single Namespace.
*   **ClusterRole**: Defines API permissions across the entire cluster, including non-namespaced resources.

#### Q88: What is the difference between a RoleBinding and a ClusterRoleBinding?
**Answer:** 
*   **RoleBinding**: Assigns a Role/ClusterRole to users/Service Accounts within a specific Namespace.
*   **ClusterRoleBinding**: Assigns a ClusterRole cluster-wide, granting permissions across all Namespaces.

#### Q89: What is a Service Account?
**Answer:** An identity created in Kubernetes that allows Pod processes to authenticate and access the Kubernetes API Server.

#### Q90: What is Pod Security Admission (PSA)?
**Answer:** A built-in admission controller that evaluates PodSpecs against security standards (`Privileged`, `Baseline`, `Restricted`) to restrict root access.

#### Q91: What is the purpose of the `securityContext` field in a PodSpec?
**Answer:** It defines privilege and access control settings for a Pod or container (e.g., UID to run as, read-only root filesystems, Linux capabilities).

#### Q92: Explain what an Admission Controller is.
**Answer:** A plugin that intercepts requests to the Kubernetes API Server *after* authentication and authorization, but *before* object persistence, to mutate or validate resources.

#### Q93: What is dynamic volume provisioning?
**Answer:** The automatic creation of a physical storage volume (e.g., GCE Persistent Disk) and its matching PV resource when a user submits a PVC.

#### Q94: What does the reclaim policy `Delete` mean for a PV?
**Answer:** When the matching PVC is deleted, both the PV resource and the backing physical cloud storage disk are deleted automatically.

#### Q95: What does the reclaim policy `Retain` mean for a PV?
**Answer:** When the PVC is deleted, the PV remains intact, and the data is preserved for manual recovery by an administrator.

#### Q96: What is a Secret encryption at rest?
**Answer:** A security configuration that encrypts Secrets before writing them to the etcd database, typically using keys managed via Cloud KMS.

#### Q97: Explain the risk of mounting the host filesystem into a container.
**Answer:** It bypasses container isolation, allowing compromised containers to read or write sensitive files on the host node, potentially taking over the node.

#### Q98: What does the `readOnlyRootFilesystem: true` setting do?
**Answer:** It mounts the container's root directory as read-only, preventing attackers from writing malicious binaries or modifying system configurations at runtime.

#### Q99: What is GKE Workload Identity?
**Answer:** A GKE security feature that maps Kubernetes Service Accounts directly to IAM Service Accounts, eliminating the need to store static credentials inside GKE clusters.

#### Q100: How do you audit who made a specific API call in the cluster?
**Answer:** Check the API Server Audit Logs, which record every request made to the API Server, including identity, time, and modifications.
