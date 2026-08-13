# Google Cloud CLI (`gcloud`) Cheat Sheet

This cheat sheet provides a comprehensive reference for the most commonly used Google Cloud CLI (`gcloud`), Cloud Storage (`gsutil`/`gcloud storage`), and BigQuery (`bq`) commands.

---

## 1. Authentication & Configuration

Manage your GCP CLI environment, active accounts, and project configurations.

| Command | Description |
| :--- | :--- |
| `gcloud init` | Initialize the SDK, authorize access, and set default project/zone. |
| `gcloud auth login` | Authorize gcloud to access GCP using Google user credentials. |
| `gcloud auth application-default login` | Generate credentials for local application development. |
| `gcloud auth revoke` | Revoke credentials for an active account. |
| `gcloud config list` | View active configuration properties (project, account, zone). |
| `gcloud config set project <project-id>` | Set the default project for subsequent commands. |
| `gcloud config set compute/zone <zone>` | Set the default Compute Engine zone (e.g., `us-central1-a`). |
| `gcloud config set compute/region <region>` | Set the default Compute Engine region (e.g., `us-central1`). |
| `gcloud config configurations list` | List all user-defined gcloud configurations. |
| `gcloud version` | Show the installed components and version info. |

---

## 2. Project & Account Management

Manage Google Cloud projects and billing associations.

```bash
# List all projects accessible to the logged-in user
gcloud projects list

# Create a new project
gcloud projects create my-gcp-project-12345 --name="My Enterprise Project"

# Describe project details
gcloud projects describe my-gcp-project-12345

# Delete a project (schedules it for teardown)
gcloud projects delete my-gcp-project-12345

# List active billing accounts
gcloud billing accounts list

# Link a project to a billing account
gcloud billing projects link my-gcp-project-12345 --billing-account=012345-67890A-BCDEF0
```

---

## 3. Compute Engine (`gcloud compute`)

Manage Virtual Machine instances, disk volumes, and machine configurations.

```bash
# Create a standard Debian Linux VM
gcloud compute instances create my-vm-instance \
  --machine-type=e2-medium \
  --zone=us-central1-a \
  --image-family=debian-11 \
  --image-project=debian-cloud

# List VMs in the active project
gcloud compute instances list --format="table(name,zone,machineType,status,networkInterfaces[0].accessConfigs[0].natIP:label=EXTERNAL_IP)"

# SSH into a VM instance
gcloud compute ssh my-vm-instance --zone=us-central1-a

# Stop, Start, and Reset (reboot) a VM
gcloud compute instances stop my-vm-instance --zone=us-central1-a
gcloud compute instances start my-vm-instance --zone=us-central1-a
gcloud compute instances reset my-vm-instance --zone=us-central1-a

# Resize a VM's machine type (requires VM to be stopped first)
gcloud compute instances set-machine-type my-vm-instance --machine-type=e2-standard-4 --zone=us-central1-a

# Create a disk snapshot
gcloud compute disks snapshot my-vm-disk \
  --snapshot-names=my-disk-snapshot-v1 \
  --zone=us-central1-a
```

---

## 4. Virtual Private Cloud (VPC) Networking

Manage subnets, firewall rules, and cloud routers.

```bash
# Create a custom-mode VPC network
gcloud compute networks create my-custom-vpc --subnet-mode=custom

# Create a subnet inside the custom VPC
gcloud compute networks subnets create my-subnet \
  --network=my-custom-vpc \
  --region=us-central1 \
  --range=10.0.1.0/24

# Create a firewall rule to allow inbound SSH (port 22)
gcloud compute firewall-rules create allow-ssh-ingress \
  --network=my-custom-vpc \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=ssh-server

# Create a Cloud NAT Gateway (requires Cloud Router first)
gcloud compute routers create my-router --network=my-custom-vpc --region=us-central1
gcloud compute routers nats create my-nat-gateway \
  --router=my-router \
  --region=us-central1 \
  --auto-allocate-nat-external-ips \
  --nat-custom-subnet-ip-ranges=my-subnet
```

---

## 5. Cloud Storage (`gcloud storage` & `gsutil`)

Manage buckets and upload/download objects. Note: `gcloud storage` is the modern replacement for `gsutil`.

```bash
# Create a storage bucket
gcloud storage buckets create gs://my-unique-bucket-name --location=us-central1

# Upload a local file to a bucket
gcloud storage cp /path/to/local/file.txt gs://my-unique-bucket-name/uploads/

# List objects inside a bucket
gcloud storage ls gs://my-unique-bucket-name --recursive

# Download an object from a bucket
gcloud storage cp gs://my-unique-bucket-name/uploads/file.txt /path/to/downloaded/

# Synchronize a local directory with a bucket
gcloud storage rsync -r /my/local/folder gs://my-unique-bucket-name/backup/

# Share a file publicly (make read access public)
gsutil acl ch -u AllUsers:R gs://my-unique-bucket-name/uploads/file.txt
```

---

## 6. IAM & Resource Management

Create service accounts, assign IAM roles, and manage permissions.

```bash
# Create a Service Account
gcloud iam service-accounts create my-deployer-sa \
  --description="Service account used for CI/CD deployments" \
  --display-name="CI-Deployer"

# Assign "Storage Admin" role to the service account
gcloud projects add-iam-policy-binding my-gcp-project-12345 \
  --member="serviceAccount:my-deployer-sa@my-gcp-project-12345.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Generate and download a JSON private key for the service account (sensitive!)
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=my-deployer-sa@my-gcp-project-12345.iam.gserviceaccount.com

# Authorize gcloud CLI session using a Service Account Key
gcloud auth activate-service-account --key-file=sa-key.json
```

---

## 7. Cloud Run & App Engine

Deploy serverless container workloads and Web Apps.

```bash
# Deploy a container to Cloud Run (fully managed)
gcloud run deploy my-web-service \
  --image=gcr.io/my-gcp-project-12345/my-app:v1 \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated

# List all Cloud Run services
gcloud run services list --platform=managed --region=us-central1

# Deploy an App Engine Application
gcloud app deploy app.yaml

# View App Engine log tail
gcloud app logs read
```

---

## 8. Google Kubernetes Engine (GKE)

Deploy and manage managed Kubernetes clusters.

```bash
# Create a GKE Standard Cluster
gcloud container clusters create my-gke-cluster \
  --num-nodes=3 \
  --zone=us-central1-a \
  --machine-type=e2-standard-2

# Retrieve cluster credentials (updates local ~/.kube/config for kubectl)
gcloud container clusters get-credentials my-gke-cluster --zone=us-central1-a

# Resize a GKE node pool
gcloud container clusters resize my-gke-cluster \
  --node-pool=default-pool \
  --num-nodes=5 \
  --zone=us-central1-a
```

---

## 9. Databases & Analytics (`bq`)

Manage Cloud SQL databases and perform BigQuery analysis.

```bash
# Create a Cloud SQL (PostgreSQL) Instance
gcloud sql instances create my-pg-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-7680 \
  --region=us-central1 \
  --root-password="SecurePassword123!"

# List Cloud SQL database instances
gcloud sql instances list

# Create a BigQuery Dataset
bq mk --location=US my_dataset

# Run a SQL Query on BigQuery public data
bq query --use_legacy_sql=false \
  'SELECT name, gender, count FROM `bigquery-public-data.usa_names.usa_1910_current` LIMIT 10'
```

---

## 10. Operations & Logs (`gcloud logging`)

Monitor resources and read operations logs.

```bash
# Read the last 5 logs from a Compute Engine instance
gcloud logging read "resource.type=gce_instance AND resource.labels.instance_id=my-vm-instance" --limit=5

# Create a metric-based log alert
gcloud logging sinks create my-error-sink \
  pubsub.googleapis.com/projects/my-gcp-project-12345/topics/my-errors-topic \
  --log-filter="severity>=ERROR"
```
