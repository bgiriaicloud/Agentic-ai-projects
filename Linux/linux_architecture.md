# Linux Operating System Architecture

The Linux operating system is divided into two primary execution spaces to ensure security, stability, and resource protection: **User Space** and **Kernel Space**.

---

## 🗺️ Architectural Layer Diagram

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          USER SPACE (Restricted)                       │
│                                                                        │
│   ┌──────────────────────┐  ┌──────────────────┐  ┌────────────────┐   │
│   │   User Applications  │  │ System Utilities │  │ Shells / CLI   │   │
│   │   (Nginx, Python)    │  │   (tar, grep)    │  │ (bash, zsh)    │   │
│   └──────────┬───────────┘  └────────┬─────────┘  └────────┬───────┘   │
│              │                       │                     │           │
│              ▼                       ▼                     ▼           │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │               Standard C Library (glibc / musl)                │   │
│   └──────────────────────────────┬─────────────────────────────────┘   │
└──────────────────────────────────┼─────────────────────────────────────┘
                                   │
                    [ System Call Interface (SCI) ]
             (Boundary - transition via trap instruction)
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│                          KERNEL SPACE (Privileged)                     │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     System Call Interface (SCI)                  │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     │                                  │
│  ┌──────────────────────────────────▼───────────────────────────────┐  │
│  │                    Core Kernel Subsystems                        │  │
│  │                                                                  │  │
│  │  ┌────────────────────┐ ┌────────────────────┐ ┌──────────────┐  │  │
│  │  │ Process Management │ │ Memory Management  │ │ Network Stack│  │  │
│  │  │ (Scheduler, Fork)  │ │ (Virtual Memory)   │ │ (TCP/IP, Socket) │  │
│  │  └────────────────────┘ └────────────────────┘ └──────────────┘  │  │
│  │  ┌────────────────────┐ ┌────────────────────┐                   │  │
│  │  │Virtual File System │ │   IPC Subsystem    │                   │  │
│  │  │ (VFS: ext4, xfs)   │ │ (Semaphores, Pipes)│                   │  │
│  │  └────────────────────┘ └────────────────────┘                   │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     │                                  │
│  ┌──────────────────────────────────▼───────────────────────────────┐  │
│  │                           Device Drivers                         │  │
│  │                (USB, SATA Disk, Network Interface)               │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
└─────────────────────────────────────┼──────────────────────────────────┘
                                      │
┌─────────────────────────────────────▼──────────────────────────────────┐
│                             HARDWARE SPACE                             │
│                                                                        │
│         ┌───────────┐         ┌───────────┐         ┌───────────┐      │
│         │    CPU    │         │    RAM    │         │ Disk / NIC│      │
│         └───────────┘         └───────────┘         └───────────┘      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Subsystems & Layers Detailed

### 1. User Space
User Space is the sandboxed environment where all user-run programs, daemon services, and applications run. 
*   **Protection**: Applications running here have restricted access to system resources. They cannot communicate directly with the CPU or physical memory pages.
*   **Safety**: If an application in User Space crashes (e.g., a segmentation fault in an Nginx worker process), it does not crash the entire operating system.

### 2. Standard C Library (`glibc`)
Exposes the APIs that map high-level programming instructions to low-level Kernel entry functions. When a program needs to write to a file, it calls standard function declarations (like `printf()` or `fopen()`), which `glibc` translates into the corresponding Kernel system calls (like `write()` or `open()`).

### 3. System Call Interface (SCI)
The secure boundary layer that controls transitions from User Space to Kernel Space. 
*   When a program makes a system call, it triggers a CPU software interrupt (trap instruction), shifting the processor execution privilege level from Ring 3 (User) to Ring 0 (Kernel).
*   Examples of system calls include `fork()` (create process), `execve()` (run binary), `kill()` (send signal), and `socket()` (open network socket).

### 4. Kernel Space (Ring 0)
The heart of the operating system. The Kernel runs with complete, unrestricted access to CPU registers and hardware resources. It contains several modules:
*   **Process Management**: Coordinates CPU time allocation among processes using scheduling algorithms (e.g., the Completely Fair Scheduler - CFS), handles context switching, and manages process trees.
*   **Memory Management**: Manages physical and virtual memory spacing. It maps process virtual memory to hardware RAM pages, handles swap storage when RAM is saturated, and prevents processes from accessing other processes' memory spaces.
*   **Virtual File System (VFS)**: An abstraction layer that exposes uniform file operations (open, read, write) to user applications, regardless of the underlying filesystem format (e.g., ext4, XFS, FAT32, NFS).
*   **Network Stack**: Handles packets passing through network interfaces, implementing protocols like IP, TCP, UDP, and Netfilter firewall filters.
*   **Device Drivers**: Software components compiled into or dynamically loaded by the kernel to communicate directly with hardware (controllers, disk interfaces, input devices).

### 5. Hardware Space
The physical hardware layer containing the Central Processing Unit (CPU), Random Access Memory (RAM), hard drives/SSDs, and Network Interface Cards (NIC).
