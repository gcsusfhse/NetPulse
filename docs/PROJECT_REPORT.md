# Project Report

## NetPulse — Network Scanner and Device Monitoring Tool

---

| Field | Details |
|-------|---------|
| **Project Title** | NetPulse — Network Scanner & Device Monitoring Tool |
| **Team Name** | Team NetPulse |
| **Institution** | PSV College of Engineering & Technology, Krishnagiri |
| **Department** | Computer Science & Engineering (Cyber Security) |
| **Academic Year** | 2024–2025 |
| **Year / Semester** | 2nd Year / 3rd Semester |
| **Guide** | [Faculty Name] |
| **Version** | 1.0.0 |
| **Date** | November 2024 |

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Scope](#5-scope)
6. [Literature Survey](#6-literature-survey)
7. [System Requirements](#7-system-requirements)
8. [System Design](#8-system-design)
9. [Modules Description](#9-modules-description)
10. [Implementation](#10-implementation)
11. [Testing](#11-testing)
12. [Results & Output](#12-results--output)
13. [Security Considerations](#13-security-considerations)
14. [Learning Outcomes](#14-learning-outcomes)
15. [Future Enhancements](#15-future-enhancements)
16. [Team Contributions](#16-team-contributions)
17. [Conclusion](#17-conclusion)
18. [References](#18-references)

---

## 1. Abstract

Network management and security monitoring are critical aspects of modern IT infrastructure. NetPulse is a Python-based network scanning and device monitoring tool designed to help network administrators and security professionals quickly identify all active devices on a local area network (LAN). The tool performs host discovery using ICMP echo requests (ping sweep) and optionally uses ARP scanning via the Scapy library for higher accuracy and speed. For each discovered device, NetPulse resolves the hostname using reverse DNS lookups and retrieves the MAC address from the OS ARP cache. Results are displayed in a color-coded terminal table, exported to CSV, and compiled into a human-readable text report with security recommendations.

---

## 2. Introduction

### 2.1 Background

In any network environment — from home networks to enterprise LANs — a network administrator needs to know which devices are connected at any given time. Unauthorized or unknown devices can pose serious security risks including data interception, bandwidth theft, and network intrusion.

Traditional network monitoring tools like Nmap are powerful but complex and require deep networking knowledge. NetPulse aims to bridge the gap — providing a lightweight, easy-to-use alternative suitable for students, home users, and junior IT professionals.

### 2.2 Motivation

This project was motivated by real-world internship scenarios where IT teams need to quickly audit network devices. Building this tool allowed our team to apply theoretical networking concepts (IP addressing, ARP, DNS, TCP) in a hands-on programming project using Python.

### 2.3 Project Type

This is a **tool/utility project** with practical cybersecurity applications. It falls under the domain of **network security and reconnaissance tools** — the ethical and authorized side of network scanning.

---

## 3. Problem Statement

> *"Network administrators often lack a simple, free tool to quickly discover all connected devices on a local network with their IP, MAC address, and hostname in an easy-to-export format."*

Commercial tools are expensive. Nmap is powerful but has a steep learning curve. Simple ping commands show one host at a time. NetPulse solves this by combining host discovery, MAC resolution, hostname lookup, and reporting into a single Python script with a clean CLI.

---

## 4. Objectives

1. Develop a Python tool that discovers all active devices on a `/24` local subnet.
2. Retrieve IP address, MAC address, and hostname for each device.
3. Display results in a formatted, color-coded terminal table.
4. Export results to a CSV file for further analysis.
5. Generate a text-based summary report with security recommendations.
6. Include an optional TCP port scanner for service identification.
7. Provide cross-platform compatibility (Linux, macOS, Windows).
8. Write modular, well-commented, and testable code.

---

## 5. Scope

**In Scope:**
- IPv4 host discovery on local networks (Class A, B, C private subnets)
- ICMP ping-based scanning (no root required)
- ARP scanning via Scapy (root/admin required)
- MAC address resolution via OS ARP cache
- Reverse DNS hostname resolution
- TCP port scanning for common ports (21 ports)
- CSV and text file export
- Command-line interface

**Out of Scope:**
- IPv6 scanning
- Remote network scanning (only local LAN)
- OS fingerprinting
- Vulnerability detection
- GUI interface (planned for v2.0)

---

## 6. Literature Survey

### 6.1 Existing Tools

| Tool | Type | Pros | Cons |
|------|------|------|------|
| **Nmap** | CLI Scanner | Feature-rich, scriptable | Complex, steep learning curve |
| **Angry IP Scanner** | GUI Tool | Easy to use | Closed source, Java dependency |
| **Advanced IP Scanner** | GUI Tool | Windows-friendly | Windows only, freeware |
| **arp-scan** | CLI (Linux) | Fast ARP scanning | Linux only |
| **Fing** | Mobile App | User-friendly | Paid features, closed source |

### 6.2 Why NetPulse?

NetPulse fills the gap between simplicity and functionality. It is:
- **Open source** and free
- **Cross-platform** (Linux, macOS, Windows)
- **Educational** — well-commented code for learning
- **Lightweight** — minimal dependencies (works without Scapy)
- **Exportable** — built-in CSV and report generation

---

## 7. System Requirements

### 7.1 Hardware Requirements

| Component | Minimum |
|-----------|---------|
| Processor | Intel Core i3 / ARM Cortex-A53 |
| RAM | 512 MB |
| Storage | 50 MB |
| Network | Ethernet or Wi-Fi (connected to LAN) |

### 7.2 Software Requirements

| Component | Version |
|-----------|---------|
| Operating System | Ubuntu 20.04+ / macOS 12+ / Windows 10+ |
| Python | 3.8 or higher |
| pip | 20.0+ |
| scapy | 2.5.0 (optional) |
| pytest | 7.4.3 (for testing) |

---

## 8. System Design

### 8.1 Architecture Overview

NetPulse follows a **modular architecture** with 4 core modules:

```
main.py (Orchestrator)
    │
    ├── src/scanner.py       — Network scanning logic
    ├── src/port_scanner.py  — TCP port scanning
    ├── src/reporter.py      — CSV and report generation
    └── src/display.py       — Terminal UI and colors
```

### 8.2 Data Flow Diagram

```
User Input (CLI args)
        │
        ▼
   main.py parses args
        │
        ▼
scanner.py: Determine target network
        │
        ├─── ICMP Ping Sweep (subprocess)
        │         └─── ARP cache lookup for MAC
        │
        └─── ARP Scan via Scapy (optional)
                  └─── MAC from ARP response
        │
        ▼
   Hostname Resolution (socket.gethostbyaddr)
        │
        ▼
   Results List (dicts)
        │
        ├─── display.py → Print color table to terminal
        ├─── reporter.py → Save CSV to outputs/
        └─── reporter.py → Save report to reports/
```

### 8.3 Module Interaction

- `main.py` imports and calls functions from all modules
- `scanner.py` returns a `list[dict]` of device records
- `reporter.py` consumes device records to produce files
- `display.py` consumes device records to produce terminal output
- Modules are **loosely coupled** — each can be tested independently

---

## 9. Modules Description

### 9.1 `scanner.py`

**Purpose:** Core network scanning logic.

**Key Functions:**
- `get_local_ip()` — Detects the machine's local IP using a UDP socket trick
- `get_hostname(ip)` — Reverse DNS lookup using `socket.gethostbyaddr()`
- `ping_host(ip)` — Pings a single host using OS ping command (cross-platform)
- `get_mac_from_arp_table(ip)` — Reads ARP cache to get MAC address
- `scan_with_ping(network)` — Full subnet ping sweep (no root needed)
- `scan_with_scapy(network)` — ARP broadcast scan using Scapy (root needed)
- `scan_network(network, use_scapy)` — Main entry point, chooses method

**Technologies:** `socket`, `subprocess`, `ipaddress`, `scapy`

### 9.2 `port_scanner.py`

**Purpose:** Concurrent TCP port scanning for a single host.

**Key Functions:**
- `scan_port(ip, port)` — Attempts TCP connect() to a single port
- `scan_ports(ip, ports)` — Scans multiple ports concurrently using ThreadPoolExecutor
- `print_port_results(ip, ports)` — Displays open ports in a table

**Technologies:** `socket`, `concurrent.futures`

### 9.3 `reporter.py`

**Purpose:** Saves results to CSV and generates text reports.

**Key Functions:**
- `save_to_csv(devices, output_dir)` — Writes device list to timestamped CSV
- `generate_report(devices, network, duration)` — Builds text report string
- `save_report(content, output_dir)` — Writes report to file
- `print_report(content)` — Prints report to terminal

**Technologies:** `csv`, `os`, `datetime`

### 9.4 `display.py`

**Purpose:** All terminal UI: banner, tables, colors, messages.

**Key Functions:**
- `print_banner()` — ASCII art banner at startup
- `print_device_table(devices)` — Formatted color table of results
- `print_scan_start/complete()` — Status messages
- `colorize(text, color)` — Wraps text in ANSI codes safely

**Technologies:** `platform` (for Windows ANSI support), ANSI escape codes

---

## 10. Implementation

### 10.1 Network Detection Algorithm

```python
# UDP trick — no data sent, just establishes default route
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]  # e.g., "192.168.1.20"
s.close()
network = ".".join(local_ip.split(".")[:3]) + ".0/24"  # "192.168.1.0/24"
```

### 10.2 Ping Sweep Algorithm

```python
for host in ipaddress.ip_network(network, strict=False).hosts():
    if ping_host(str(host)):         # ICMP ping
        mac = get_mac_from_arp_table(str(host))  # ARP cache
        hostname = get_hostname(str(host))        # Reverse DNS
        results.append({...})
```

### 10.3 Concurrent Port Scanning

```python
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(scan_port, ip, port): port for port in ports}
    for future in as_completed(futures):
        result = future.result()
        if result["state"] == "Open":
            open_ports.append(result)
```

---

## 11. Testing

### 11.1 Test Strategy

We used **unit testing** with `pytest` to test individual module functions in isolation.

### 11.2 Test Cases

| Test | Module | Expected Result | Status |
|------|--------|----------------|--------|
| `test_get_local_ip_returns_string` | scanner | Returns non-empty string | ✅ Pass |
| `test_get_hostname_localhost` | scanner | Returns string for 127.0.0.1 | ✅ Pass |
| `test_get_hostname_invalid_ip` | scanner | Returns "Unknown" | ✅ Pass |
| `test_ping_localhost` | scanner | Returns True for 127.0.0.1 | ✅ Pass |
| `test_ping_invalid_host` | scanner | Returns False for 192.0.2.255 | ✅ Pass |
| `test_save_to_csv_creates_file` | reporter | Creates .csv file | ✅ Pass |
| `test_save_to_csv_content` | reporter | CSV has correct rows | ✅ Pass |
| `test_generate_report_returns_string` | reporter | Returns non-empty string | ✅ Pass |
| `test_generate_report_contains_device_info` | reporter | Contains IP addresses | ✅ Pass |
| `test_generate_report_empty_devices` | reporter | Mentions no devices found | ✅ Pass |

### 11.3 Running Tests

```bash
python -m pytest tests/ -v --tb=short
```

---

## 12. Results & Output

### 12.1 Sample Scan Result

Scanning `192.168.1.0/24` on a college lab network:

| # | IP Address | MAC Address | Hostname | Status |
|---|-----------|------------|---------|--------|
| 1 | 192.168.1.1 | A4:C3:F0:85:71:22 | router.home | Active |
| 2 | 192.168.1.5 | B8:27:EB:12:34:56 | raspberrypi.local | Active |
| 3 | 192.168.1.10 | D4:6E:5C:AB:CD:EF | DESKTOP-KARTHIK | Active |
| 4 | 192.168.1.15 | 3C:22:FB:12:AB:34 | Priya-MacBook.local | Active |

**Scan duration:** ~18 seconds for /24 subnet  
**With Scapy ARP:** ~2 seconds for /24 subnet

### 12.2 CSV Export

Results are saved to `outputs/scan_YYYYMMDD_HHMMSS.csv` after every scan.

### 12.3 Port Scan Sample

```
  Port     Service         State
  ─────    ───────         ─────
  22       SSH             Open
  80       HTTP            Open
  443      HTTPS           Open
  3306     MySQL           Open
```

---

## 13. Security Considerations

- **Authorized use only** — This tool must only be used on networks you own or have written permission to scan.
- **Ping scan is noisy** — ICMP pings can appear in firewall/IDS logs.
- **MAC spoofing** — MAC addresses can be spoofed; do not solely rely on MACs for device identification.
- **ARP poisoning** — ARP cache may contain spoofed entries in compromised networks.
- **Legal compliance** — Unauthorized network scanning may violate the IT Act 2000 (India) and similar laws in other countries.

> ⚠️ **Disclaimer:** This tool is developed for educational purposes only. Always obtain proper authorization before scanning any network.

---

## 14. Learning Outcomes

1. **TCP/IP Networking** — Deep understanding of IP addressing, subnetting, ARP protocol, and ICMP
2. **Python Socket Programming** — `socket` module for TCP connections and DNS lookup
3. **System Programming** — Using `subprocess` to invoke OS commands cross-platform
4. **Concurrency** — `concurrent.futures.ThreadPoolExecutor` for parallel port scanning
5. **Software Architecture** — Modular design, separation of concerns, single responsibility principle
6. **Testing** — Writing meaningful unit tests with `pytest`
7. **CLI Development** — `argparse` for professional CLI design
8. **Version Control** — Git branching, commit discipline, collaborative development
9. **Documentation** — Technical writing: README, project report, code comments
10. **Cybersecurity Awareness** — Ethical hacking concepts, reconnaissance, risk assessment

---

## 15. Future Enhancements

| Priority | Feature | Description |
|----------|---------|-------------|
| High | **OUI Database Lookup** | Identify device manufacturer from MAC address prefix |
| High | **Scheduled Monitoring** | Run scans periodically and alert on new/removed devices |
| Medium | **HTML Report** | Generate styled visual reports using Jinja2 |
| Medium | **SQLite History** | Store all scan results for trend analysis |
| Medium | **Web Dashboard** | Flask-based web UI for results browsing |
| Low | **OS Fingerprinting** | Detect OS type (like Nmap's -O flag) |
| Low | **Packet Capture** | Live traffic monitoring mode |
| Low | **Mobile App** | React Native companion app |

---

## 16. Team Contributions

### Arjun R. — Team Lead & Backend Developer
- Designed overall system architecture
- Implemented `scanner.py` (ping sweep, ARP, hostname resolution)
- Implemented `main.py` (CLI, argument parsing, application flow)
- Integrated all modules and resolved cross-platform issues
- Conducted final code review

### Priya K. — Network Research & QA
- Researched networking protocols (ARP, ICMP, DNS, TCP)
- Designed the Network Architecture diagram
- Wrote all unit tests in `tests/test_scanner.py`
- Performed manual testing on Linux and Windows
- Compiled the Literature Survey section of this report

### Karthik S. — Module Developer
- Implemented `port_scanner.py` (concurrent TCP port scanning)
- Implemented `reporter.py` (CSV export, report generation)
- Set up the project folder structure and `config/config.ini`
- Created Bash helper script `scripts/network_info.sh`
- Maintained `requirements.txt` and environment setup

### Sneha M. — UI/UX & Documentation
- Implemented `display.py` (ASCII banner, color tables, ANSI output)
- Wrote the professional `README.md` with badges and emojis
- Created sample CSV and report output files
- Compiled and formatted this Project Report
- Created GitHub repository, topics, and description

---

## 17. Conclusion

NetPulse successfully achieves its goal of providing a simple, lightweight, cross-platform tool for local network discovery. By combining Python's built-in `socket` and `subprocess` modules with optional Scapy support, the tool offers flexibility for users with or without elevated privileges.

The project gave our team valuable hands-on experience with networking protocols, Python programming, software design, testing, and documentation — skills directly applicable to careers in network administration, cybersecurity, and software development.

The modular architecture ensures the codebase can be easily extended with planned features like HTML reports, scheduled monitoring, and a web dashboard in future iterations.

---

## 18. References

1. Python Software Foundation. *socket — Low-level networking interface*. https://docs.python.org/3/library/socket.html
2. Python Software Foundation. *ipaddress — IPv4/IPv6 manipulation library*. https://docs.python.org/3/library/ipaddress.html
3. The Scapy Project. *Scapy Documentation*. https://scapy.readthedocs.io/en/latest/
4. Postel, J. (1981). *RFC 792: Internet Control Message Protocol*. IETF.
5. Plummer, D. (1982). *RFC 826: An Ethernet Address Resolution Protocol*. IETF.
6. Python Software Foundation. *concurrent.futures — Launching parallel tasks*. https://docs.python.org/3/library/concurrent.futures.html
7. Lyon, G. (2009). *Nmap Network Scanning*. Insecure.com LLC.
8. Python Software Foundation. *argparse — Parser for command-line options*. https://docs.python.org/3/library/argparse.html
9. Forouzan, B. A. (2012). *Data Communications and Networking* (5th ed.). McGraw-Hill.
10. Information Technology Act, 2000 — Government of India.

---

*Report prepared by Team NetPulse | PSV College of Engineering & Technology, Krishnagiri*  
*November 2024*
