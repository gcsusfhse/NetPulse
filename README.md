<div align="center">

# 🌐 NetPulse

### Network Scanner & Device Monitoring Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()
[![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)]()

**A lightweight, cross-platform network scanning tool built with Python**  
*Internship Project — PSV College of Engineering & Technology, Krishnagiri*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Team](#-team-members) • [License](#-license)

</div>

---

## 📋 Project Overview

**NetPulse** is a Python-based network scanning and device monitoring tool developed as a team internship project by 2nd-year B.E. Computer Science / Cyber Security students. It enables users to discover all active devices on a local network, retrieve their IP addresses, MAC addresses, and hostnames, and export the results to CSV for analysis.

The tool uses **ICMP ping sweeps** (no root required) and optionally **ARP scanning via Scapy** for faster, more accurate results. A clean command-line interface with color-coded output makes it easy to use even for beginners.

---

## 🎯 Objectives

- 🔍 **Discover** all active hosts on a local IP network automatically
- 🖥️ **Identify** devices by IP address, MAC address, and hostname
- 📁 **Export** results to CSV for documentation and reporting
- 🔒 **Highlight** basic security recommendations for network administrators
- 🧰 **Demonstrate** real-world use of Python networking libraries (socket, subprocess, scapy)

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🚀 **Auto Network Detection** | Automatically detects your local /24 subnet |
| 📡 **ARP + Ping Scanning** | Supports both ICMP ping sweep and Scapy ARP scan |
| 🖥️ **Hostname Resolution** | Reverse DNS lookup for each discovered host |
| 🔌 **Port Scanner** | Scans 20 common TCP ports on any target host |
| 📊 **CSV Export** | Saves all scan results to timestamped CSV files |
| 📄 **Text Reports** | Generates human-readable summary reports |
| 🎨 **Color CLI** | ANSI color-coded terminal output for readability |
| 🏁 **Cross-Platform** | Works on Linux, macOS, and Windows |
| 🧪 **Unit Tests** | Includes `pytest` tests for core modules |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core programming language |
| **socket** | TCP/IP connections, hostname resolution |
| **subprocess** | Execute system ping commands |
| **ipaddress** | Parse and iterate over CIDR networks |
| **csv** | Export results to spreadsheet-compatible files |
| **concurrent.futures** | Multi-threaded port scanning |
| **scapy** *(optional)* | ARP packet crafting for fast network scans |
| **argparse** | Clean CLI argument parsing |
| **pytest** | Unit testing framework |
| **Bash** | System info helper script |

---

## 🗺️ Network Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    LOCAL NETWORK (192.168.1.0/24)            │
│                                                              │
│  ┌───────────┐     ARP/ICMP      ┌──────────────────────┐   │
│  │  NetPulse │ ◄─────────────── ► │  Target Devices      │   │
│  │ (Scanner) │                   │  192.168.1.1 - .254  │   │
│  └─────┬─────┘                   └──────────────────────┘   │
│        │                                                     │
│        ▼                                                     │
│  ┌───────────┐   ┌─────────────┐   ┌────────────────────┐   │
│  │ ARP Scan  │   │  Ping Sweep │   │  Port Scanner      │   │
│  │ (Scapy)   │   │  (socket)   │   │  (TCP Connect)     │   │
│  └─────┬─────┘   └──────┬──────┘   └────────┬───────────┘   │
│        └────────────────┼──────────────────-─┘               │
│                         ▼                                    │
│                  ┌─────────────┐                             │
│                  │  CSV + TXT  │                             │
│                  │  Reports    │                             │
│                  └─────────────┘                             │
└──────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Working Principle

1. **Network Detection** — The tool detects the local machine's IP using a UDP socket trick (no data sent), then assumes a `/24` subnet.
2. **Host Discovery** — Iterates over all 254 possible host IPs and sends ICMP ping packets using the OS `ping` command.
3. **MAC Resolution** — After a host responds to ping, its MAC address is read from the OS ARP cache using the `arp -n` command.
4. **Hostname Lookup** — Performs a reverse DNS (`socket.gethostbyaddr`) lookup for human-readable names.
5. **Port Scanning** — Optionally attempts TCP `connect()` on common ports to identify open services.
6. **Reporting** — Results are displayed in a color table, saved to CSV, and written to a text report.

---

## 📁 Project Structure

```
NetPulse/
│
├── main.py                     # Entry point — CLI argument parsing & orchestration
│
├── src/                        # Core source modules
│   ├── __init__.py
│   ├── scanner.py              # Network scanning (ping + ARP)
│   ├── port_scanner.py         # TCP port scanning
│   ├── reporter.py             # CSV saving & report generation
│   └── display.py              # Terminal UI, banner, color output
│
├── tests/                      # Unit tests
│   └── test_scanner.py
│
├── outputs/                    # Auto-created — scan results saved here
│   ├── sample_scans/
│   │   ├── scan_20241115_143201.csv
│   │   └── report_20241115_143220.txt
│   └── README.md
│
├── reports/                    # Auto-created — text reports saved here
│
├── config/
│   └── config.ini              # Tool configuration
│
├── scripts/
│   └── network_info.sh         # Bash script for quick network diagnostics
│
├── docs/
│   └── PROJECT_REPORT.md       # Full academic project report
│
├── requirements.txt            # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A local network connection

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-team/NetPulse.git
cd NetPulse
```

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `scapy` requires root/admin for ARP scanning. The tool works without it using ping scan.

### Step 4 — Verify Installation

```bash
python main.py --version
# Output: NetPulse v1.0.0
```

---

## 💻 Usage

### Basic Usage — Auto-detect and Scan Local Network

```bash
python main.py
```

### Scan a Specific Network

```bash
python main.py -n 192.168.1.0/24
```

### Use Scapy ARP Scan (Faster, Requires Root)

```bash
sudo python main.py -n 192.168.1.0/24 --scapy
```

### Save Results to a Custom Directory

```bash
python main.py -o /home/user/scan_results
```

### Skip CSV or Report Saving

```bash
python main.py --no-csv         # Don't save CSV
python main.py --no-report      # Don't save text report
```

### Get Network Info Before Scanning (Linux/macOS)

```bash
bash scripts/network_info.sh
```

### Run Unit Tests

```bash
python -m pytest tests/ -v
```

### All Available Options

```
usage: netpulse [-h] [-n CIDR] [--scapy] [-o DIR] [--no-report] [--no-csv] [-v]

options:
  -h, --help            show this help message and exit
  -n CIDR, --network CIDR
                        Target network in CIDR notation (default: auto-detect)
  --scapy               Use Scapy ARP scan (requires root/admin)
  -o DIR, --output DIR  Directory to save CSV results (default: outputs/)
  --no-report           Skip saving the text report file
  --no-csv              Skip saving results to CSV
  -v, --version         show version and exit
```

---

## 📤 Example Output

### Terminal Output

```
  ███╗   ██╗███████╗████████╗    ██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ████╗  ██║██╔════╝╚══██╔══╝    ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ...

  Network Scanner & Device Monitoring Tool
  Version 1.0.0 | Team NetPulse | 2024

  ──────────────────────────────────────────────────────────────

  [i] Local IP detected: 192.168.1.20
  [i] Target network   : 192.168.1.0/24

  [►] Starting scan on network: 192.168.1.0/24
  [►] Please wait...

  [✔] Scan complete in 18.45s — 8 device(s) found.

  ────────────────────────────────────────────────────────────────────────────
  #    IP Address         MAC Address          Hostname                   Status
  ─────────────────────────────────────────────────────────────────────────────
  1    192.168.1.1        A4:C3:F0:85:71:22    router.home                Active
  2    192.168.1.5        B8:27:EB:12:34:56    raspberrypi.local          Active
  3    192.168.1.10       D4:6E:5C:AB:CD:EF    DESKTOP-KARTHIK            Active
  4    192.168.1.15       3C:22:FB:12:AB:34    Priya-MacBook.local        Active
  ...

  Total: 8 active device(s) found
```

### CSV Output (`outputs/scan_20241115_143201.csv`)

```csv
ip,mac,hostname,status,method,scan_time
192.168.1.1,A4:C3:F0:85:71:22,router.home,Active,ICMP Ping,2024-11-15 14:32:01
192.168.1.5,B8:27:EB:12:34:56,raspberrypi.local,Active,ICMP Ping,2024-11-15 14:32:03
...
```

---

## 📚 Learning Outcomes

Through this project, the team gained hands-on experience with:

- 🔗 **Networking Fundamentals** — IP addressing, subnetting, ARP, ICMP, TCP
- 🐍 **Python Networking** — `socket`, `subprocess`, `ipaddress`, `scapy`
- 🔐 **Cybersecurity Concepts** — Network reconnaissance, MAC addressing, port scanning
- 💻 **Software Design** — Modular Python project structure, separation of concerns
- 🧪 **Testing** — Writing and running unit tests with `pytest`
- 📝 **Documentation** — Writing professional README, reports, and code comments
- 🔄 **Version Control** — Git workflow, branching, meaningful commit messages
- 🖥️ **CLI Development** — Argument parsing with `argparse`, color output with ANSI codes

---

## 🔮 Future Scope

- [ ] 📊 **HTML/PDF Reports** — Auto-generate styled visual reports using Jinja2
- [ ] 🌐 **Web Dashboard** — Flask-based web UI for scan results
- [ ] 📬 **Email Alerts** — Notify admin when unknown devices join the network
- [ ] 🔄 **Scheduled Scans** — Run scans at intervals and detect changes
- [ ] 🗄️ **Database Logging** — Store scan history in SQLite for trend analysis
- [ ] 🏷️ **OUI Lookup** — Identify device manufacturer from MAC address OUI prefix
- [ ] 🔌 **Service Fingerprinting** — Detect OS and service versions (like nmap)
- [ ] 📱 **Mobile App** — React Native app to view scan results on phone

---

## 👥 Team Members

| # | Name | Role | Contribution |
|---|------|------|-------------|
| 1 | **Arjun R.** | Team Lead & Backend Dev | `scanner.py`, `main.py`, CLI design, integration |
| 2 | **Priya K.** | Network Research & Testing | Network architecture, test cases, documentation |
| 3 | **Karthik S.** | Module Developer | `port_scanner.py`, `reporter.py`, CSV logic |
| 4 | **Sneha M.** | UI/UX & Documentation | `display.py`, README, project report, demo |

*Department of Computer Science & Engineering — Cyber Security*  
*PSV College of Engineering & Technology, Krishnagiri — 2024*

---

## 📖 References

1. Python `socket` module documentation — https://docs.python.org/3/library/socket.html
2. Scapy documentation — https://scapy.readthedocs.io/
3. IETF RFC 792 — Internet Control Message Protocol (ICMP)
4. IETF RFC 826 — An Ethernet Address Resolution Protocol (ARP)
5. Python `ipaddress` module — https://docs.python.org/3/library/ipaddress.html
6. Nmap Network Scanning Book — Gordon Lyon (reference for concepts)
7. Python `argparse` documentation — https://docs.python.org/3/library/argparse.html

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by **Team NetPulse** | PSV College of Engineering & Technology  
*B.E. Computer Science / Cyber Security — 2nd Year | 2024*

⭐ If this project helped you, give it a star!

</div>
