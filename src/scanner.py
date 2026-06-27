#!/usr/bin/env python3
"""
NetPulse - Network Scanner and Device Monitoring Tool
======================================================
Module: scanner.py
Description: Core network scanning module using ARP and ICMP protocols.
Authors: Team NetPulse (Arjun, Priya, Karthik, Sneha)
Version: 1.0.0
"""

import subprocess
import socket
import ipaddress
import platform
import re
from datetime import datetime
from typing import Optional

# Try to import scapy (optional - falls back to ping-based scan)
try:
    from scapy.all import ARP, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


def get_local_ip() -> str:
    """
    Returns the local machine's IP address by connecting to an external host.
    Uses a UDP trick (no actual data sent) to find the default interface IP.
    """
    try:
        # Connect to a public DNS server (no data is actually sent)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def get_hostname(ip: str) -> str:
    """
    Performs a reverse DNS lookup to resolve IP address to hostname.
    Returns 'Unknown' if resolution fails.
    """
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.gaierror):
        return "Unknown"


def ping_host(ip: str) -> bool:
    """
    Pings a single host to check if it is alive/reachable.
    Works on both Windows and Linux/macOS.

    Args:
        ip: Target IP address string

    Returns:
        True if host responded, False otherwise
    """
    os_name = platform.system().lower()

    # Adjust ping command flags based on OS
    if os_name == "windows":
        # -n 1 = send 1 packet, -w 500 = timeout 500ms
        cmd = ["ping", "-n", "1", "-w", "500", ip]
    else:
        # -c 1 = send 1 packet, -W 1 = timeout 1 second
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def get_mac_from_arp_table(ip: str) -> str:
    """
    Reads the OS ARP cache to retrieve the MAC address of a known IP.
    This avoids needing root/admin privileges for MAC resolution.

    Args:
        ip: Target IP address string

    Returns:
        MAC address string or 'N/A' if not found
    """
    try:
        os_name = platform.system().lower()

        if os_name == "windows":
            output = subprocess.check_output(["arp", "-a", ip], stderr=subprocess.DEVNULL).decode()
            # Windows ARP output uses dashes: aa-bb-cc-dd-ee-ff
            match = re.search(r"(([0-9a-f]{2}[:-]){5}([0-9a-f]{2}))", output, re.IGNORECASE)
        else:
            output = subprocess.check_output(["arp", "-n", ip], stderr=subprocess.DEVNULL).decode()
            # Linux ARP output: aa:bb:cc:dd:ee:ff
            match = re.search(r"(([0-9a-f]{2}[:-]){5}([0-9a-f]{2}))", output, re.IGNORECASE)

        if match:
            return match.group(0).upper()
    except Exception:
        pass

    return "N/A"


def scan_with_scapy(network: str) -> list:
    """
    Performs a fast ARP scan using Scapy (requires root/admin privileges).
    This is the preferred method for accurate MAC address discovery.

    Args:
        network: Network in CIDR notation (e.g., '192.168.1.0/24')

    Returns:
        List of dicts with 'ip', 'mac', 'hostname', 'status' keys
    """
    results = []
    print(f"  [*] Using Scapy ARP scan on {network}...")

    # Craft an ARP request broadcast packet
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send packet and collect responses (timeout=2s, verbose=0 to suppress output)
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=0)[0]

    for sent, received in answered_list:
        hostname = get_hostname(received.psrc)
        results.append({
            "ip": received.psrc,
            "mac": received.hwsrc.upper(),
            "hostname": hostname,
            "status": "Active",
            "method": "ARP (Scapy)",
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return results


def scan_with_ping(network: str) -> list:
    """
    Performs a ping-based host discovery scan (no root privileges needed).
    MAC addresses are read from the OS ARP cache after pinging.

    Args:
        network: Network in CIDR notation (e.g., '192.168.1.0/24')

    Returns:
        List of dicts with device info for active hosts
    """
    results = []
    net = ipaddress.ip_network(network, strict=False)
    hosts = list(net.hosts())
    total = len(hosts)

    print(f"  [*] Ping scanning {total} hosts in {network}...")
    print(f"  [*] This may take a while for large networks...\n")

    for i, host in enumerate(hosts):
        ip = str(host)
        # Show progress every 10 hosts
        if (i + 1) % 10 == 0 or (i + 1) == total:
            print(f"  Progress: {i+1}/{total} hosts scanned...", end="\r")

        if ping_host(ip):
            hostname = get_hostname(ip)
            mac = get_mac_from_arp_table(ip)
            results.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "status": "Active",
                "method": "ICMP Ping",
                "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    print()  # New line after progress
    return results


def scan_network(network: Optional[str] = None, use_scapy: bool = False) -> list:
    """
    Main entry point for network scanning.
    Auto-detects the local network if none provided.
    Chooses Scapy ARP scan or ping scan based on availability and preference.

    Args:
        network: Optional CIDR network string. If None, auto-detects local network.
        use_scapy: Force use of Scapy if available.

    Returns:
        List of discovered device dictionaries
    """
    # Auto-detect local network if not provided
    if network is None:
        local_ip = get_local_ip()
        # Assume /24 subnet (most common home/office network)
        network = ".".join(local_ip.split(".")[:3]) + ".0/24"
        print(f"  [*] Auto-detected local network: {network}")

    # Validate network format
    try:
        ipaddress.ip_network(network, strict=False)
    except ValueError:
        print(f"  [!] Invalid network format: {network}")
        print(f"  [!] Use CIDR notation (e.g., 192.168.1.0/24)")
        return []

    # Choose scanning method
    if use_scapy and SCAPY_AVAILABLE:
        return scan_with_scapy(network)
    else:
        if use_scapy and not SCAPY_AVAILABLE:
            print("  [!] Scapy not available. Falling back to ping scan.")
        return scan_with_ping(network)


# ── Quick test when run directly ────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing scanner module...")
    devices = scan_network()
    for d in devices:
        print(d)
