# Kubectl CLI Command Cheat Sheet

This document compiles the essential `kubectl` commands and syntax patterns used in daily Kubernetes cluster administration and troubleshooting.

---

## 📋 Table of Contents
1.  [Configuration, Context & Cluster Info](#1-configuration-context--cluster-info)
2.  [Creating, Appliying & Deleting Workloads](#2-creating-appliying--deleting-workloads)
3.  [Viewing & Querying Resources (`kubectl get`)](#3-viewing--querying-resources-kubectl-get)
4.  [Debugging, Logging & Diagnostics](#4-debugging-logging--diagnostics)
5.  [Scaling, Rollouts & Application Updates](#5-scaling-rollouts--application-updates)
6.  [Node Operations & Maintenance](#6-node-operations--maintenance)
7.  [Output Formatting & JSONPath Queries](#7-output-formatting--jsonpath-queries)

---

## 1. Configuration, Context & Cluster Info

Manage connections to multiple Kubernetes clusters (kubeconfig configurations).

```bash
# Display the active kubeconfig settings
kubectl config view

# List all available cluster contexts
kubectl config get-contexts

# Display the current active context name
kubectl config current-context

# Switch the active context to a different cluster
kubectl config use-context gke_my-project_us-central1_prod-cluster

# Temporarily switch execution to a specific namespace
kubectl config set-context --current --namespace=kube-system

# Display cluster master and CoreDNS endpoints info
kubectl cluster-info
```

---

## 2. Creating, Appliying & Deleting Workloads

```bash
# Apply or update resources declared in a YAML/JSON manifest
kubectl apply -f deployment.yaml

# Recursively apply all YAML manifests in a directory
kubectl apply -f ./manifests/

# Interactively edit a live resource configuration running in the cluster
kubectl edit deployment/web-server

# Delete a resource by its manifest definition
kubectl delete -f deployment.yaml

# Force delete a Pod immediately (bypasses grace period, useful for stuck pods)
kubectl delete pod stuck-pod-name --force --grace-period=0
```

---

## 3. Viewing & Querying Resources (`kubectl get`)

Query the state of resources in the active namespace.

```bash
# Get all Pods in the current namespace with extended IP and Node columns
kubectl get pods -o wide

# Get all Services across all namespaces
kubectl get svc --all-namespaces

# Get resource description manifest in YAML format
kubectl get deployment web-app -o yaml

# List Pods matching a specific label selector
kubectl get pods -l app=backend,env=prod

# List Pods showing their attached label key-value pairs
kubectl get pods --show-labels

# Sort Pods by restart count (troubleshooting crash loops)
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'
```

---

## 4. Debugging, Logging & Diagnostics

Core commands used to troubleshoot failing applications and pods.

```bash
# Print detailed lifecycle events, warnings, and configurations of a Pod
kubectl describe pod web-pod-name

# Stream container stdout logs in real-time
kubectl logs -f web-pod-name

# Stream logs of a specific container inside a multi-container Pod
kubectl logs -f web-pod-name -c helper-container

# Print logs from a previously crashed container instance (returns crash dump)
kubectl logs web-pod-name -p

# Open an interactive shell inside a running container
kubectl exec -it web-pod-name -- /bin/bash

# Forward local port 8080 to the target Pod's port 80 (debugging local network)
kubectl port-forward pod/web-pod-name 8080:80

# View real-time CPU and memory usage of all worker nodes
kubectl top nodes

# View CPU and memory usage of all Pods in the current namespace
kubectl top pods
```

---

## 5. Scaling, Rollouts & Application Updates

Manage application deployment scale, history, and rollout lifecycle.

```bash
# Scale a deployment to 5 active replicas immediately
kubectl scale deployment/web-app --replicas=5

# Monitor the active rollout status of a deployment upgrade
kubectl rollout status deployment/web-app

# View the revision history of rollouts for a deployment
kubectl rollout history deployment/web-app

# Roll back a deployment to the previous stable revision
kubectl rollout undo deployment/web-app

# Roll back a deployment to a specific historic revision number
kubectl rollout undo deployment/web-app --to-revision=3

# Trigger a rolling restart of all Pods in a deployment (pulls updated secrets/images)
kubectl rollout restart deployment/web-app
```

---

## 6. Node Operations & Maintenance

System administration commands to manage node schedules.

```bash
# Mark a Node as unschedulable (cordon) to prevent new Pod allocations
kubectl cordon node-name-1

# Cordon a Node and evict all running Pods safely (node maintenance)
kubectl drain node-name-1 --ignore-daemonsets --delete-emptydir-data

# Mark a cordoned Node as schedulable again (uncordon)
kubectl uncordon node-name-1

# Add a taint to a Node to repel Pods unless they tolerate it
kubectl taint nodes node-name-1 dedicated=experimental:NoSchedule

# Remove a taint from a Node
kubectl taint nodes node-name-1 dedicated:NoSchedule-
```

---

## 7. Output Formatting & JSONPath Queries

Extract specific fields from the Kubernetes API responses.

```bash
# Get the external IP address of all nodes using JSONPath
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'

# Extract the container image name of a specific deployment
kubectl get deployment/web-app -o jsonpath='{.spec.template.spec.containers[0].image}'

# Print all Pod names and their corresponding host node names as a list
kubectl get pods -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName
```
