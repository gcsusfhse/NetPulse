# NetPulse — GitHub Repository Setup Guide

## 📦 Repository Description

> NetPulse is a Python-based network scanner and device monitoring tool that discovers active hosts on a LAN, retrieves IP/MAC/hostname info, performs port scanning, and exports results to CSV with security reports. Built as a team internship project.

---

## 🏷️ Suggested GitHub Topics

Add these topics to your repository (Settings → Topics):

```
network-scanner
python
cybersecurity
networking
arp-scan
ping-sweep
port-scanner
network-monitoring
network-security
python3
cli-tool
internship-project
device-discovery
lan-scanner
open-source
```

---

## 📝 Suggested Git Commit Messages (15+ Commits)

Use these commit messages to create a realistic, professional Git history.

```
Commit 1:
  git commit -m "Initial commit: project structure and README skeleton"

Commit 2:
  git commit -m "feat: add get_local_ip and get_hostname functions to scanner.py"

Commit 3:
  git commit -m "feat: implement cross-platform ping_host function using subprocess"

Commit 4:
  git commit -m "feat: add get_mac_from_arp_table with regex parsing for Linux/Windows"

Commit 5:
  git commit -m "feat: implement scan_with_ping for full /24 subnet ICMP sweep"

Commit 6:
  git commit -m "feat: add optional Scapy ARP scan with graceful fallback"

Commit 7:
  git commit -m "feat: add port_scanner.py with concurrent TCP scanning using ThreadPoolExecutor"

Commit 8:
  git commit -m "feat: implement save_to_csv with timestamped filenames in reporter.py"

Commit 9:
  git commit -m "feat: add generate_report function with security recommendations"

Commit 10:
  git commit -m "feat: implement color terminal output and ASCII banner in display.py"

Commit 11:
  git commit -m "feat: add main.py CLI with argparse — network, output, scapy flags"

Commit 12:
  git commit -m "feat: add network_info.sh bash helper script for Linux/macOS"

Commit 13:
  git commit -m "test: add unit tests for scanner and reporter modules using pytest"

Commit 14:
  git commit -m "docs: add comprehensive README with badges, architecture diagram, usage"

Commit 15:
  git commit -m "docs: add full project report in docs/PROJECT_REPORT.md"

Commit 16:
  git commit -m "chore: add requirements.txt, config.ini, .gitignore, and LICENSE"

Commit 17:
  git commit -m "feat: add sample scan CSV and report in outputs/sample_scans/"

Commit 18:
  git commit -m "fix: handle PermissionError gracefully when Scapy unavailable"

Commit 19:
  git commit -m "refactor: modularize display.py — separate print_error, print_info functions"

Commit 20:
  git commit -m "docs: update README with example terminal output and future scope table"
```

---

## 🚀 How to Push to GitHub

```bash
# 1. Initialize git in the project folder
cd NetPulse
git init

# 2. Add all files
git add .

# 3. Make initial commit
git commit -m "Initial commit: project structure and README skeleton"

# 4. Create repo on GitHub, then:
git remote add origin https://github.com/gcsusfhse/NetPulse.git
git branch -M main
git push -u origin main
```

---

## 🌿 Suggested Branch Strategy

```
main          ← stable, demo-ready code
dev           ← active development
feature/port-scanner   ← port scanner feature
feature/web-dashboard  ← future Flask UI
```

---

## 📌 GitHub Repository Settings

- **Visibility:** Public (for internship proof)
- **Description:** (use the description above)
- **Website:** (optional — can link to a demo video)
- **Include:** README, .gitignore (Python), MIT License
