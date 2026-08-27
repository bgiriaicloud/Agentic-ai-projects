# Google Cloud Networking Exam Preparation Guide

This guide is designed to prepare candidates for the **Google Cloud Professional Cloud Network Engineer** certification. It covers core networking concepts, implementation workflows, best practices, troubleshooting, and AI-powered networking features on Google Cloud Platform (GCP).

---

## 📋 Table of Contents
*   [Chapter 1: Introduction to GCP and Networking Fundamentals](#chapter-1-introduction-to-gcp-and-networking-fundamentals)
*   [Chapter 2: Designing and Planning a Google Cloud Network](#chapter-2-designing-and-planning-a-google-cloud-network)
*   [Chapter 3: Implementing Virtual Private Cloud (VPC) Networks](#chapter-3-implementing-virtual-private-cloud-vpc-networks)
*   [Chapter 4: Configuring Managed Network Services](#chapter-4-configuring-managed-network-services)
*   [Chapter 5: Implementing Hybrid Network Interconnectivity](#chapter-5-implementing-hybrid-network-interconnectivity)
*   [Chapter 6: Google Cloud Networking Security](#chapter-6-google-cloud-networking-security)
*   [Chapter 7: Network Operations, Monitoring, and Troubleshooting](#chapter-7-network-operations-monitoring-and-troubleshooting)
*   [Chapter 8: AI-Powered Google Cloud Networking](#chapter-8-ai-powered-google-cloud-networking)

---

## Chapter 1: Introduction to Google Cloud Platform and Networking Fundamentals

This chapter lays the foundation of Google's global infrastructure and the core components of software-defined networking (SDN) in GCP.

### 1. Google's Global Infrastructure
*   **Regions**: Global geographic locations containing cluster data centers (e.g., `us-central1`, `europe-west3`).
*   **Zones**: Isolated locations within a region. Connectivity within a region is low-latency but zones have separate power, cooling, and network physical setups.
*   **Edge Points of Presence (PoPs)**: Locations where Google connects its network to the rest of the internet. Google has over 100 Edge PoPs globally.
*   **Global Fiber Network**: Google operates a privately owned global fiber optic network, which transports traffic between regions without routing over the public internet.

### 2. Software-Defined Networking (Andromeda)
*   **Andromeda**: Google Cloud's SDN virtualization stack. It controls the routing and packet processing on Google's physical network controllers.
*   *Key benefit*: Bypasses traditional virtual router bottlenecks, allowing linear scale of network throughput directly tied to VM compute size.

### 3. Core IP Addressing Concepts
*   **RFC 1918 Private Ranges**: Private IP ranges reserved for local networks:
    *   `10.0.0.0/8`
    *   `172.16.0.0/12`
    *   `192.168.0.0/16`
*   **External IP Addresses**: Can be ephemeral (dynamic) or static (reserved).
    *   *Premium Tier*: Traffic enters Google's network at an Edge PoP closest to the user and travels over Google's backbone.
    *   *Standard Tier*: Traffic travels over the public internet and enters Google's network at the Edge PoP closest to the destination region.

---

## Chapter 2: Designing and Planning a Google Cloud Network

Designing a production-grade GCP network requires configuring IP spaces, organizational hierarchies, and routing tiers.

### 1. Organizational Hierarchy Design
```
   ┌──────────────────────────────────┐
   │        GCP Organization          │
   └────────────────┬─────────────────┘
                    ▼
   ┌──────────────────────────────────┐
   │        Folders (optional)        │
   └────────────────┬─────────────────┘
                    ▼
   ┌──────────────────────────────────┐
   │             Projects             │
   └────────────────┬─────────────────┘
                    ▼
   ┌──────────────────────────────────┐
   │      VPC Networks & Subnets      │
   └──────────────────────────────────┘
```

*   **Projects**: Organize isolated resource environments. Network resources (firewalls, load balancers, interconnects) are bound to a project.
*   **Shared VPC**: Allows an organization to connect resources from multiple projects (Service Projects) to a common VPC network managed in a central project (Host Project).

### 2. Subnet Planning & Sizing
*   Subnets are regional resources in GCP.
*   **IP Allocation**: Avoid overlapping IP subnets across on-premises networks and other VPCs to prevent routing failures in hybrid setups.
*   *Reserved IP Addresses*: Google reserves **5 IP addresses** in every subnet:
    *   `.0`: Network address.
    *   `.1`: Default gateway.
    *   `.2`: Google DNS server.
    *   `.3`: Reserved for future Google use.
    *   `._`: Broadcast address (the last IP of the subnet range).

### 3. Routing Design Tiers
*   **Dynamic Routing**: Configured via Cloud Router using Border Gateway Protocol (BGP).
    *   *Regional*: Routes are only advertised and visible within the same region.
    *   *Global*: Routes are dynamically advertised across all regions in the VPC.

---

## Chapter 3: Implementing Virtual Private Cloud (VPC) Networks

Implementing VPCs involves managing subnets, configuring routing, and linking projects.

### 1. VPC Creation Modes
*   **Auto Mode**: Automatically creates a subnet in every Google Cloud region with a predefined `/20` range (from the `10.128.0.0/9` block).
    *   *Drawback*: Predefined subnets might overlap with corporate networks, making them unsuitable for hybrid configurations.
*   **Custom Mode**: You manually define regional subnets, IP ranges, and allocation settings. This is the **standard recommendation** for enterprise environments.

### 2. Private Google Access (PGA)
*   Allows VMs without public external IP addresses in a subnet to access Google APIs and services (e.g., Cloud Storage, BigQuery) over their private IPs.
*   *Configuration requirement*: Enable `privateIpGoogleAccess` on the subnet settings.

### 3. VPC Network Peering
*   Connects two VPC networks dynamically, allowing VM-to-VM communication over private IPs with low latency.
*   *Key characteristics*:
    *   Non-transitive: If VPC A peers with VPC B, and VPC B peers with VPC C, VPC A **cannot** communicate with VPC C unless explicitly peered.
    *   Allows cross-project connectivity.
    *   Peered networks cannot have overlapping IP ranges.

---

## Chapter 4: Configuring Managed Network Services

Managed services handle external access, name resolution, and load distribution.

### 1. Google Cloud Load Balancing (GCLB)
GCP offers various load balancers categorized by traffic scope (global vs. regional) and layer (Layer 4 vs. Layer 7).

| Load Balancer Type | Layer | Scope | Key Features |
| :--- | :--- | :--- | :--- |
| **Global External HTTP(S)** | L7 | Global | HTTP/HTTPS routing, SSL offloading, Cloud CDN & Cloud Armor integration, path-based routing. |
| **Regional External HTTP(S)** | L7 | Regional | Regional isolation, compliance bounds. |
| **Internal HTTP(S)** | L7 | Regional | Private application load balancing within a VPC. |
| **External SSL/TCP Proxy** | L4 | Global | Non-HTTP TCP traffic with SSL offloading. |
| **Internal TCP/UDP (Network)** | L4 | Regional | Private, high-throughput, low-latency, pass-through routing. |

### 2. Cloud DNS
*   **Private Zones**: Resolve internal domain names (e.g., `app.internal`) within designated VPCs.
*   **DNS Forwarding**: Connects local on-premises DNS servers with Cloud DNS to resolve hybrid domain names.
*   **DNS Peering**: Shares name-resolution configurations from one VPC with another.

### 3. Cloud NAT (Network Address Translation)
*   Allows VMs without external IP addresses to access the internet (for software updates, external API calls) securely.
*   *Operational structure*: Outbound connections are translated, but external internet clients cannot initiate inbound sessions to private VMs.

---

## Chapter 5: Implementing Hybrid Network Interconnectivity

Hybrid connectivity bridges on-premises data centers or other clouds with Google Cloud.

```
                  ┌──────────────────────────────┐
                  │         Google Cloud         │
                  │                              │
                  │   ┌──────────────────────┐   │
                  │   │     VPC Network      │   │
                  │   └──────────▲───────────┘   │
                  │              │               │
                  └──────────────┼───────────────┘
                                 │
                   Hybrid Connection Options:
                   1. Cloud VPN (IPsec)
                   2. Partner Interconnect
                   3. Dedicated Interconnect (10G/100G)
                                 │
                  ┌──────────────▼───────────────┐
                  │      On-Premises Network     │
                  └──────────────────────────────┘
```

### 1. Cloud VPN
*   **Classic VPN**: Legacy, single-tunnel setups.
*   **HA VPN (High Availability)**: Offers a 99.99% service availability SLA.
    *   Uses **two active tunnels** from GCP to the peer gateway.
    *   Requires dynamic routing via BGP using Cloud Router.

### 2. Cloud Interconnect
*   **Dedicated Interconnect**: Direct physical connection between your on-premises network and Google's network edge. Available in sizes of **10 Gbps** or **100 Gbps** circuits.
*   **Partner Interconnect**: Connection via a third-party service provider. Useful if your data center is not in a Google colocation facility. Available in sizes from **50 Mbps** up to **50 Gbps**.

### 3. Cloud Router & BGP
*   Cloud Router manages dynamic routing by exchanging routes using BGP. It establishes a BGP session over VPN or VlanAttachments to dynamically learn and advertise route prefixes.

---

## Chapter 6: Google Cloud Networking Security

Securing the network requires applying firewalls, encryption, perimeters, and threat defense.

### 1. VPC Firewall Rules
*   Firewall rules control traffic to and from VMs.
*   **Implied Rules**:
    *   *Implied Egress Allow*: All outbound traffic is permitted by default.
    *   *Implied Ingress Deny*: All incoming traffic is blocked by default.
*   **Target Selection**: Apply rules using network tags, service accounts, or target all instances.
    *   *Best Practice*: Use **Service Accounts** instead of Network Tags for production firewalls to prevent non-privileged users from bypassing security by changing VM tags.

### 2. Cloud Armor
*   Google's DDoS defense and Web Application Firewall (WAF) service.
*   *Key capabilities*: Protects against OWASP Top 10 vulnerabilities (SQL injection, cross-site scripting) and filters traffic based on geographic IP location.

### 3. VPC Service Controls (VPC-SC)
*   Mitigates data exfiltration risks by defining a security perimeter around multi-tenant Google APIs (e.g., Cloud Storage, BigQuery). PGA VMs can talk to APIs inside the perimeter, but cannot copy data to projects outside the perimeter.

---

## Chapter 7: Network Operations, Monitoring, and Troubleshooting

Maintaining network health requires logging, network path visualization, and monitoring key metrics.

### 1. VPC Flow Logs
*   Record network telemetry flows sent from or received by VM instances.
*   Used for: Network auditing, security forensics, and analyzing bandwidth usage.

### 2. Network Intelligence Center (NIC)
*   **Connectivity Tests**: Simulates path packet routes between source and destination endpoints to identify firewall configuration blocks or incorrect routing rules.
*   **Network Topology**: Visually graphs active VPC architectures and regional throughput paths.
*   **Performance Dashboard**: Displays packet loss and latency metrics aggregated across regions.

### 3. Troubleshooting Common Issues
*   *Issue*: VMs cannot ping each other across peered VPCs.
    *   *Fix*: Ensure no overlapping subnets exist and verify that both VPCs have the dynamic routes configuration enabled.
*   *Issue*: Outbound traffic from private VMs to public APIs fails.
    *   *Fix*: Ensure Private Google Access (PGA) is enabled on the subnet, or confirm Cloud NAT is deployed and active in the region.

---

## Chapter 8: AI-Powered Google Cloud Networking

Google Cloud integrates generative AI to simplify cloud operations, optimize performance, and accelerate network troubleshooting.

### 1. Gemini in Network Intelligence Center
*   **AI-Assisted Troubleshooting**: Gemini analyzes VPC Flow Logs, routing policies, and firewall configurations to diagnose connectivity issues.
    *   *Example*: Instead of manually tracing BGP state transitions, you can ask Gemini: *"Why is my HA VPN tunnel failing to establish BGP peering?"* Gemini evaluates the configuration and suggests mismatched ASN values or IP configs.
*   **Natural Language Queries**: Allows operators to query their global topology using plain English:
    *   *"Show me all paths with latency spikes over 50ms between us-east1 and europe-west1."*
    *   *"Which firewall rules are currently blocking SSH traffic to service-project-A?"*

### 2. Network Optimization & Smart Routing
*   **Predictive Traffic Engineering**: AI engines analyze traffic histories across Google's global fiber backbone to dynamically reroute traffic, avoiding congestion before packet drop events occur.
*   **Automated Policy Generation**: Security models analyze system traffic patterns to automatically recommend optimal, least-privilege firewall rules and Cloud Armor policies.
