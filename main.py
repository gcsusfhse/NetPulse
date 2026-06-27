#!/usr/bin/env python3
"""
NetPulse - Network Scanner and Device Monitoring Tool
======================================================
Module: main.py  (Entry Point)
Description: CLI argument parsing and main application flow.
Authors: Team NetPulse (Arjun, Priya, Karthik, Sneha)
Version: 1.0.0
Usage:
    python main.py                         # Auto-scan local /24 network
    python main.py -n 192.168.1.0/24      # Scan specific network
    python main.py -n 10.0.0.0/24 --scapy # Use Scapy ARP scan
    python main.py --output /tmp/results   # Custom output directory
    python main.py --no-report             # Skip saving report
"""

import argparse
import time
import sys
import os

# Ensure src/ directory is in Python path when run from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.scanner  import scan_network, get_local_ip
from src.reporter import save_to_csv, generate_report, save_report, print_report
from src.display  import (
    print_banner, print_device_table,
    print_scan_start, print_scan_complete,
    print_error, print_info
)


def parse_arguments() -> argparse.Namespace:
    """
    Defines and parses command-line arguments.
    Returns the parsed Namespace object.
    """
    parser = argparse.ArgumentParser(
        prog="netpulse",
        description="NetPulse — Network Scanner & Device Monitoring Tool",
        epilog="Example: python main.py -n 192.168.1.0/24 --scapy"
    )

    parser.add_argument(
        "-n", "--network",
        type=str,
        default=None,
        metavar="CIDR",
        help="Target network in CIDR notation (default: auto-detect local /24)"
    )

    parser.add_argument(
        "--scapy",
        action="store_true",
        help="Use Scapy ARP scan instead of ping (requires root/admin)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="outputs",
        metavar="DIR",
        help="Directory to save CSV results (default: outputs/)"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip saving the text report file"
    )

    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Skip saving results to CSV"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="NetPulse v1.0.0"
    )

    return parser.parse_args()


def main() -> None:
    """
    Main application entry point.
    Orchestrates scanning, display, CSV saving, and report generation.
    """
    # Step 1: Print banner
    print_banner()

    # Step 2: Parse CLI arguments
    args = parse_arguments()

    # Step 3: Determine target network
    network = args.network
    if network is None:
        local_ip = get_local_ip()
        network = ".".join(local_ip.split(".")[:3]) + ".0/24"
        print_info(f"Local IP detected: {local_ip}")
        print_info(f"Target network   : {network}")

    # Step 4: Start scan
    print_scan_start(network)
    start_time = time.time()

    try:
        devices = scan_network(network=network, use_scapy=args.scapy)
    except PermissionError:
        print_error("Permission denied. Try running with sudo/admin for full MAC resolution.")
        sys.exit(1)
    except KeyboardInterrupt:
        print_error("Scan interrupted by user (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error during scan: {e}")
        sys.exit(1)

    end_time = time.time()
    scan_duration = end_time - start_time

    # Step 5: Display results in terminal
    print_scan_complete(scan_duration, len(devices))
    print_device_table(devices)

    # Step 6: Save to CSV (unless --no-csv flag)
    if not args.no_csv and devices:
        save_to_csv(devices, output_dir=args.output)

    # Step 7: Generate and print report
    report_content = generate_report(devices, network, scan_duration)
    print_report(report_content)

    # Step 8: Save report file (unless --no-report flag)
    if not args.no_report:
        save_report(report_content, output_dir="reports")

    print_info("Thank you for using NetPulse!")


# ── Script entry guard ───────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
