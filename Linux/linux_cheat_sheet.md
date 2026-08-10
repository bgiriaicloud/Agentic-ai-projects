# Linux CLI Command Cheat Sheet

This document compiles essential Linux commands and utilities used in daily systems administration, diagnostic analysis, and SRE operations.

---

## 📋 Table of Contents
1.  [File & Directory Operations](#1-file--directory-operations)
2.  [Text Search, Filtering & Processing](#2-text-search-filtering--processing)
3.  [System Status, Hardware & Disk Audits](#3-system-status-hardware--disk-audits)
4.  [Process Diagnostics & Memory Control](#4-process-diagnostics--memory-control)
5.  [Network Connections & Troubleshooting](#5-network-connections--troubleshooting)
6.  [Permissions, Ownership & Security](#6-permissions-ownership--security)
7.  [File Archiving & Compression](#7-file-archiving--compression)

---

## 1. File & Directory Operations

```bash
# List directory contents with detailed permissions, sizes, and hidden files
ls -la

# Print the absolute path of the current working directory
pwd

# Create nested directories recursively
mkdir -p /var/log/app/archive/

# Copy a directory and all of its contents recursively
cp -r /src/folder/ /dest/folder/

# Move or rename files/directories
mv old_name.txt new_name.txt

# Create an empty file or update timestamps of an existing file
touch index.js

# Create a symbolic link pointing to a target file
ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

# Remove a file
rm file.txt

# Force remove a directory and all its contents recursively
rm -rf /tmp/temporary-data/
```

---

## 2. Text Search, Filtering & Processing

```bash
# Search for a pattern recursively inside files, showing line numbers
grep -rn "error_pattern" /var/log/

# Case-insensitive search, showing 3 lines of context after each match
grep -i -A 3 "critical" application.log

# Find files matching a name pattern in a directory
find /var/log/ -name "*.log"

# Find files larger than 100MB and list them
find /var/log/ -type f -size +100M -exec ls -lh {} \;

# Run a command (e.g., delete) on all files returned by a find search
find . -name "*.tmp" | xargs rm -f

# Search and replace text in a file in-place
sed -i 's/old-value/new-value/g' config.env

# Print the second column of a space-separated log file
awk '{print $2}' access.log

# Stream and print the last 100 lines of a file in real-time
tail -n 100 -f auth.log
```

---

## 3. System Status, Hardware & Disk Audits

```bash
# Display general system kernel and OS information
uname -a

# Show system uptime and CPU load averages
uptime

# View free and used physical memory (RAM) and swap in megabytes
free -m

# Show total disk space usage on all mounted file systems in human-readable format
df -h

# Calculate disk usage of files and folders inside a specific directory
du -sh /var/log/*

# List all block storage devices (disks and partitions)
lsblk
```

---

## 4. Process Diagnostics & Memory Control

```bash
# List all running processes with their CPU/Memory usage and commands
ps aux

# Find process IDs (PIDs) matching a specific process name
pgrep -fl "nginx"

# Open an interactive task manager showing system resources and threads
top

# Terminate a process gracefully by its process ID (sends SIGTERM)
kill 1234

# Force terminate a process immediately (sends SIGKILL)
kill -9 1234

# Terminate all processes matching a specific name
killall node

# List all open files and network sockets opened by processes
lsof -i :8080
```

---

## 5. Network Connections & Troubleshooting

```bash
# Send ICMP echo requests to verify network connectivity to a host
ping -c 4 google.com

# Fetch headers and print the response body of an HTTP request
curl -i https://api.github.com/status

# Download a file in the background, saving it to a specific filename
wget -O package.tar.gz https://example.com/file.tar.gz

# Display all active listening TCP and UDP sockets with process names (ss)
ss -tulnp

# Display active network interfaces and their assigned IP addresses
ip addr show

# Query DNS records for a specific domain name
dig google.com MX

# Perform a traceroute to identify the network path to a destination host
traceroute 8.8.8.8

# Test if a TCP port is open on a remote host (using netcat)
nc -zv 192.168.1.100 22
```

---

## 6. Permissions, Ownership & Security

```bash
# Grant execution permissions to a script file
chmod +x script.sh

# Change file permissions explicitly (e.g., Read/Write/Execute for owner only)
chmod 700 keys.pem

# Change the user and group owner of a folder recursively
chown -R www-data:www-data /var/www/html/

# Run a command with administrative root privileges
sudo systemctl restart nginx
```

---

## 7. File Archiving & Compression

```bash
# Create a gzipped tar archive from a directory
tar -czvf backup.tar.gz /var/www/html/

# Extract a gzipped tar archive to the current directory
tar -xzvf backup.tar.gz

# Compress a file using gzip
gzip large-file.log

# Decompress a .gz file
gunzip large-file.log.gz
```
