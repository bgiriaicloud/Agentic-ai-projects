# Linux Command Registry for Technical Interviews

This registry consolidates the essential Linux commands frequently discussed in technical interviews for DevOps, SRE, and Cloud Systems Engineering roles.

---

## 📋 Table of Contents
1.  [File & Directory Operations](#1-file--directory-operations)
2.  [Search, Find & File Viewing](#2-search-find--file-viewing)
3.  [Permissions, Ownership & Security](#3-permissions-ownership--security)
4.  [Process Management & System Resource Monitoring](#4-process-management--system-resource-monitoring)
5.  [Network Troubleshooting & Diagnostics](#5-network-troubleshooting--diagnostics)
6.  [Text Processing, Filtering & Stream Editing](#6-text-processing-filtering--stream-editing)
7.  [Storage Management & Disk I/O](#7-storage-management--disk-io)
8.  [Archiving, Compression & Package Management](#8-archiving-compression--package-management)

---

## 1. File & Directory Operations

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`ls`** | Lists directory contents. | `ls -la` (list all files, including hidden ones, in long-listing format). |
| **`cd`** | Changes the current working directory. | `cd -` (toggles back to the previous directory). |
| **`pwd`** | Prints absolute path of current working directory. | Used in shell scripts to log execution roots. |
| **`mkdir`** | Creates new directories. | `mkdir -p parent/child` (creates parent directory nested structures if they don't exist). |
| **`rm`** | Deletes files or directories. | `rm -rf <path>` (recursively forces deletion of files and folders; high danger). |
| **`cp`** | Copies files and directories. | `cp -r <src> <dest>` (recursively copies folders). |
| **`mv`** | Moves or renames files/folders. | Atomic action on local storage devices. |
| **`touch`** | Creates empty files or updates file timestamps. | `touch -a` or `touch -m` (modify access/modification timestamps). |
| **`ln`** | Creates hard or soft symbolic links. | `ln -s <target> <link_name>` (creates a symbolic soft link). |

---

## 2. Search, Find & File Viewing

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`cat`** | Concatenates and displays file content. | `cat -n file.txt` (shows content with line numbers). |
| **`less`** | Renders file content page-by-page. | Memory efficient because it doesn't load the entire file into RAM at startup. |
| **`head`** | Outputs the beginning lines of a file. | `head -n 15 file.log` (shows the first 15 lines). |
| **`tail`** | Outputs the trailing lines of a file. | `tail -f -n 100 app.log` (actively streams the last 100 lines in real-time). |
| **`find`** | Searches filesystem files matching selectors. | `find /var/log -type f -name "*.log" -mtime +7` (finds log files older than 7 days). |
| **`grep`** | Performs pattern matching using regex. | `grep -ri "error" /var/log/` (recursively searches case-insensitive matching entries). |
| **`diff`** | Compares file contents line-by-line. | `diff -u file1 file2` (outputs a unified diff block layout). |
| **`wc`** | Prints newline, word, and byte counts. | `ls -l | wc -l` (counts the number of files in a folder). |

---

## 3. Permissions, Ownership & Security

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`chmod`** | Modifies file access permissions. | `chmod 755 script.sh` (Read/Write/Execute for Owner; Read/Execute for Group/Others). |
| **`chown`** | Modifies file owner and group. | `chown -R nginx:nginx /var/www/html` (recursively changes owner). |
| **`umask`** | Defines default permissions for new files. | A umask of `022` yields default file permissions of `644` (666-022) and directories `755`. |
| **`sudo`** | Executes command as superuser (root). | `sudo -u user_name command` (executes command as a specific user). |
| **`passwd`** | Updates user authentication credentials. | `passwd -l user` (locks a user's password access). |

---

## 4. Process Management & System Resource Monitoring

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`ps`** | Reports active process snapshots. | `ps aux` or `ps -ef` (displays every active process running on the system). |
| **`top`** | Dynamic real-time system process list. | Used to inspect active CPU, memory load, and system swap stats. |
| **`htop`** | Interactive, colorful process viewer. | Modern, user-friendly alternative to `top`. |
| **`kill`** | Transmits termination signals to processes. | `kill -15 <PID>` (graceful `SIGTERM`), `kill -9 <PID>` (unpreventable force-kill `SIGKILL`). |
| **`pkill`** | Kills processes based on name matching. | `pkill -u apache` (terminates all processes run by the user 'apache'). |
| **`free`** | Displays RAM and Swap utilization stats. | `free -h` (outputs numbers in human-readable GB/MB format). |
| **`uptime`** | Shows how long the OS has been running. | Displays load averages for 1, 5, and 15 minutes. |
| **`lsof`** | Lists open files and network descriptors. | `lsof -i :8080` (finds the active process binding to port 8080). |

---

## 5. Network Troubleshooting & Diagnostics

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`ping`** | Sends ICMP Echo requests to verify hosts. | Tests basic network reachability. |
| **`curl`** | Downloads/Transmits data from/to URLs. | `curl -Iv https://example.com` (fetches HTTP headers with verbose debug logs). |
| **`wget`** | Non-interactive network downloader. | `wget -c <url>` (resumes an interrupted download). |
| **`ss`** | Dumps socket and connection statistics. | `ss -tulpn` (lists all listening TCP/UDP sockets with process PIDs). |
| **`ip`** | Manages routing, network devices, and tunnels. | `ip addr show` (replaces deprecated `ifconfig`), `ip route show`. |
| **`dig`** | Queries DNS details (A, CNAME, MX records). | `dig @8.8.8.8 example.com A +trace` (performs recursive query trace). |
| **`nslookup`**| Basic interactive query tool for DNS servers. | Used for quick hostname resolution. |
| **`nc` / `netcat`**| Arbitrary TCP/UDP connections and listeners. | `nc -zv 10.0.0.5 22` (scans port 22 on host to verify firewall rules). |
| **`traceroute`**| Dumps packet hops traversing network routes. | Tracks packet latency paths to the target host. |

---

## 6. Text Processing, Filtering & Stream Editing

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`awk`** | Pattern scanning and processing language. | `awk '{print $1}' access.log` (extracts and prints the first column/field of a log). |
| **`sed`** | Stream editor for filtering and transforming text. | `sed -i 's/foo/bar/g' config.txt` (performs in-place replacement of 'foo' with 'bar'). |
| **`cut`** | Extracts specific fields or characters. | `cut -d':' -f1 /etc/passwd` (isolates the username list split by delimiter ':'). |
| **`sort`** | Arranges lines of text files. | `sort -n` (sorts numerically), `sort -r` (sorts in reverse order). |
| **`uniq`** | Filters adjacent duplicate lines. | `uniq -c` (counts occurrences; input must be sorted first, e.g., `sort | uniq -c`). |
| **`xargs`** | Translates inputs into command parameters. | `find . -name "*.tmp" | xargs rm` (finds and deletes temp files in bulk). |

---

## 7. Storage Management & Disk I/O

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`df`** | Reports disk space utilization. | `df -h` (displays free storage levels across mounted disk partitions). |
| **`du`** | Estimates directory space usage. | `du -sh *` (calculates human-readable disk consumption size for directories). |
| **`mount`** | Mounts a filesystem. | `mount -o ro /dev/sdb1 /mnt` (mounts partition read-only). |
| **`lsblk`** | Lists information about block devices. | Visualizes physical partition tables, SSDs, and disk sizing. |
| **`iostat`** | Displays CPU and disk input/output stats. | Used to diagnose storage IOPS performance saturation bottlenecks. |

---

## 8. Archiving, Compression & Package Management

| Command | Description | Common Interview Usage / Flag |
| :--- | :--- | :--- |
| **`tar`** | Creates or extracts tape archive packages. | `tar -xzvf archive.tar.gz` (extracts a gzipped tar archive). |
| **`gzip`** | Compresses files using Lempel-Ziv coding. | `gzip -d file.gz` (decompresses a file). |
| **`apt` / `yum`**| Debian/RedHat system package managers. | Used to install, upgrade, and resolve package dependencies automatically. |

---

## 💡 Practical Interview Exercises

### 1. Find the Top 5 IP Addresses Hitting an Nginx Log
**Scenario**: You are asked to parse an Nginx access log file to count and isolate the most frequent client IP addresses.
*   **Command Pipeline**:
    ```bash
    cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 5
    ```
*   **How it works**:
    1.  `awk '{print $1}'` extracts the first column (the client IP address).
    2.  `sort` aligns the IP lines alphabetically so duplicate IPs are adjacent.
    3.  `uniq -c` counts adjacent duplicate IP occurrences.
    4.  `sort -nr` sorts the output numerically (`-n`) in reverse (`-r`) order.
    5.  `head -n 5` selects the top 5 highest IP occurrences.

### 2. Search for configuration flags and update them
**Scenario**: Replace port configurations from `8080` to `9090` across multiple configuration files in a folder.
*   **Command Pipeline**:
    ```bash
    grep -rl "8080" ./configs/ | xargs sed -i 's/8080/9090/g'
    ```
*   **How it works**:
    1.  `grep -rl "8080"` lists (`-l`) all filenames containing the string "8080".
    2.  `xargs` passes the list of filenames to the next command as arguments.
    3.  `sed -i` performs an in-place search-and-replace of "8080" with "9090".
