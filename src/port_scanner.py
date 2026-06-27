#!/usr/bin/env python3
"""
NetPulse - Network Scanner and Device Monitoring Tool
======================================================
Module: port_scanner.py
Description: Scans common TCP ports on a given host to identify open services.
Authors: Team NetPulse (Arjun, Priya, Karthik, Sneha)
Version: 1.0.0
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

# Common ports and their associated services for display
COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017:"MongoDB",
}


def scan_port(ip: str, port: int, timeout: float = 0.5) -> Dict:
    """
    Attempts a TCP connection to a single port on the target IP.
    Uses socket with a configurable timeout to avoid hanging.

    Args:
        ip: Target IP address
        port: TCP port number to scan
        timeout: Socket connection timeout in seconds

    Returns:
        Dict with port info: {port, state, service}
    """
    service = COMMON_PORTS.get(port, "Unknown")

    try:
        # Create TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))  # Returns 0 if connection succeeded
        sock.close()

        state = "Open" if result == 0 else "Closed"
    except socket.error:
        state = "Filtered"

    return {"port": port, "state": state, "service": service}


def scan_ports(ip: str, ports: List[int] = None, max_workers: int = 50) -> List[Dict]:
    """
    Scans multiple ports concurrently using ThreadPoolExecutor.
    Concurrent scanning dramatically reduces scan time.

    Args:
        ip: Target IP address
        ports: List of port numbers to scan (defaults to COMMON_PORTS)
        max_workers: Number of concurrent threads (default: 50)

    Returns:
        List of open port dicts sorted by port number
    """
    if ports is None:
        ports = list(COMMON_PORTS.keys())

    open_ports = []
    print(f"\n  [*] Port scanning {ip} ({len(ports)} ports)...")

    # Use thread pool for concurrent port scanning
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all port scan tasks
        futures = {executor.submit(scan_port, ip, port): port for port in ports}

        # Collect results as they complete
        for future in as_completed(futures):
            result = future.result()
            if result["state"] == "Open":
                open_ports.append(result)

    # Sort by port number for clean output
    open_ports.sort(key=lambda x: x["port"])
    return open_ports


def print_port_results(ip: str, open_ports: List[Dict]) -> None:
    """Prints open port results in a formatted table."""
    print(f"\n  Open ports on {ip}:")

    if not open_ports:
        print("  No open ports found.")
        return

    print(f"  {'Port':<8} {'Service':<15} {'State'}")
    print(f"  {'─'*8} {'─'*15} {'─'*8}")

    for p in open_ports:
        print(f"  {p['port']:<8} {p['service']:<15} {p['state']}")


# ── Quick test when run directly ────────────────────────────────────────────
if __name__ == "__main__":
    target = input("Enter IP to port scan: ").strip()
    results = scan_ports(target)
    print_port_results(target, results)
