# Linux File System Hierarchy

The Linux directory structure is organized as a single unified hierarchical tree, starting from the root directory `/`. Unlike Windows, which uses separate drive letters (e.g., `C:`, `D:`), Linux mounts all physical storage devices, virtual partitions, and network drives as subdirectories under the single root `/`.

---

## 📂 Visual Directory Tree Schema

```text
/ (Root Directory)
├── 📁 bin/         # Essential user command binaries (e.g., ls, cp, bash, grep)
├── 📁 sbin/        # Essential system administration binaries (e.g., iptables, fdisk, reboot)
├── 📁 etc/         # Host-specific system-wide configuration files (e.g., passwd, hosts, fstab)
├── 📁 dev/         # Device files representing hardware components (e.g., sda1, tty, random)
├── 📁 proc/        # Virtual filesystem providing process and kernel information (e.g., /proc/cpuinfo)
├── 📁 sys/         # Virtual filesystem representing device drivers and hardware stats
├── 📁 var/         # Variable data files (e.g., logs, caches, spool files, lock markers)
│   ├── 📁 log/     # System log files (e.g., syslog, auth.log)
│   └── 📁 cache/   # Temporary application cache data
├── 📁 tmp/         # Temporary files (often cleared automatically on reboot)
├── 📁 home/        # User home directories (e.g., /home/alice, /home/bob)
├── 📁 root/        # Home directory for the root superuser account
├── 📁 usr/         # Read-only user data, binaries, libraries, and documentation
│   ├── 📁 bin/     # Non-essential user binaries (e.g., python3, git, curl)
│   ├── 📁 sbin/    # Non-essential system admin binaries
│   ├── 📁 lib/     # Shared libraries for /usr/bin and /usr/sbin
│   └── 📁 share/   # Architecture-independent shared data (e.g., manual pages)
├── 📁 boot/        # Static files required to boot the system (e.g., vmlinuz kernel, initramfs)
├── 📁 lib/         # Shared libraries required by binaries in /bin and /sbin
├── 📁 lib64/       # 64-bit shared library alternatives
├── 📁 mnt/         # Temporary mount points for administrators to mount filesystems
├── 📁 media/       # Mount points for removable media devices (e.g., USB drives, CD-ROMs)
└── 📁 opt/         # Optional add-on application software packages (third-party tools)
```

---

## 🔍 Core Directories Explained

### 1. Root `/`
The top-level parent directory of the entire filesystem. Every single file, folder, and mounted device resides under this directory.

### 2. `/bin` (User Binaries)
Contains essential, single-user command binaries that must be available to boot, repair, or run the system (e.g., `cat`, `ls`, `cp`, `mkdir`, `ping`).

### 3. `/sbin` (System Binaries)
Similar to `/bin`, but contains essential binaries used by system administrators for boot maintenance and root-level commands (e.g., `iptables`, `fdisk`, `ifconfig`, `init`).

### 4. `/etc` (System Configuration)
Houses system-wide configuration files and startup scripts for services. These are static text files that control how the operating system and installed services behave. Examples:
*   `/etc/passwd`: User account database.
*   `/etc/hosts`: Local hostname-to-IP mappings.
*   `/etc/fstab`: Filesystem mount configurations.

### 5. `/dev` (Device Files)
Linux treats everything as a file, including hardware. This folder contains special device nodes that represent input/output devices (e.g., `/dev/sda` represents the first hard drive, `/dev/urandom` generates random bytes, `/dev/null` acts as the trash blackhole).

### 6. `/proc` & `/sys` (Process & System Kernel Virtual Filesystems)
These are not real physical directories on disk, but virtual filesystems generated dynamically by the Linux kernel in RAM:
*   **`/proc`**: Contains process information and kernel state stats. Reading `/proc/meminfo` displays RAM specs; reading `/proc/cpuinfo` displays CPU specifications.
*   **`/sys`**: Exposes kernel-level configuration settings and hardware controller nodes.

### 7. `/var` (Variable Data)
Stores files that constantly change in size while the system is running (e.g., system logs at `/var/log`, mail spools, database files, printer queues, lock files).

### 8. `/tmp` (Temporary Files)
A directory where applications and users can write temporary session files. Most Linux distributions automatically wipe the contents of this folder upon reboot or at scheduled intervals.

### 9. `/home` & `/root` (User Environments)
*   **`/home`**: Holds personal workspace folders and profiles for regular users.
*   **`/root`**: The dedicated home directory for the superuser (root) administrator, kept separate from standard users for security isolation.

### 10. `/usr` (User System Resources)
The largest directory in the filesystem, housing non-essential user binaries, libraries, header files, and shared documentations (often referred to as the secondary hierarchy).
