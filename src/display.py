#!/usr/bin/env python3
"""
NetPulse - Network Scanner and Device Monitoring Tool
======================================================
Module: display.py
Description: Terminal UI helpers — banner, tables, colors, progress display.
Authors: Team NetPulse (Arjun, Priya, Karthik, Sneha)
Version: 1.0.0
"""

import platform

# ANSI color codes for terminal output
# These are supported on Linux/macOS terminals and Windows 10+ (with VT enabled)
class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


def supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    if platform.system().lower() == "windows":
        # Windows 10+ supports ANSI in newer terminals
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable VIRTUAL_TERMINAL_PROCESSING (0x0004)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True  # Unix terminals generally support colors


def colorize(text: str, color: str) -> str:
    """
    Wraps text with ANSI color if terminal supports it.
    Falls back to plain text if not supported.
    """
    if supports_color():
        return f"{color}{text}{Colors.RESET}"
    return text


def print_banner() -> None:
    """
    Prints the NetPulse ASCII art banner with version info.
    Called once at application startup.
    """
    banner = r"""
  ███╗   ██╗███████╗████████╗    ██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ████╗  ██║██╔════╝╚══██╔══╝    ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██╔██╗ ██║█████╗     ██║       ██████╔╝██║   ██║██║     ███████╗█████╗
  ██║╚██╗██║██╔══╝     ██║       ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
  ██║ ╚████║███████╗   ██║       ██║     ╚██████╔╝███████╗███████║███████╗
  ╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
    """
    print(colorize(banner, Colors.CYAN))
    print(colorize("  Network Scanner & Device Monitoring Tool", Colors.BOLD))
    print(colorize("  Version 1.0.0 | Team NetPulse | 2024", Colors.YELLOW))
    print(colorize("  PSV College of Engineering & Technology", Colors.WHITE))
    print(colorize("  " + "─" * 60, Colors.BLUE))
    print()


def print_device_table(devices: list) -> None:
    """
    Prints a formatted table of discovered devices to the terminal.

    Args:
        devices: List of device dicts from scanner.py
    """
    if not devices:
        print(colorize("\n  [!] No active devices found.", Colors.RED))
        return

    # Table header
    header = (
        f"\n  {'#':<4} "
        f"{'IP Address':<18} "
        f"{'MAC Address':<20} "
        f"{'Hostname':<28} "
        f"{'Status':<10} "
        f"{'Method'}"
    )
    separator = "  " + "─" * 100

    print(colorize(separator, Colors.BLUE))
    print(colorize(header, Colors.BOLD + Colors.WHITE))
    print(colorize(separator, Colors.BLUE))

    # Device rows with alternating subtle coloring for readability
    for i, device in enumerate(devices, start=1):
        ip       = device.get("ip", "N/A")
        mac      = device.get("mac", "N/A")
        hostname = device.get("hostname", "Unknown")
        status   = device.get("status", "Unknown")
        method   = device.get("method", "N/A")

        # Truncate long hostnames
        if len(hostname) > 26:
            hostname = hostname[:23] + "..."

        # Color status based on value
        status_colored = colorize(status, Colors.GREEN) if status == "Active" else colorize(status, Colors.RED)
        ip_colored     = colorize(ip, Colors.CYAN)
        mac_colored    = colorize(mac, Colors.YELLOW) if mac != "N/A" else colorize(mac, Colors.RED)

        row = (
            f"  {i:<4} "
            f"{ip_colored:<27} "   # extra chars for ANSI codes
            f"{mac_colored:<29} "
            f"{hostname:<28} "
            f"{status_colored:<19} "
            f"{method}"
        )
        print(row)

    print(colorize(separator, Colors.BLUE))
    print(colorize(f"\n  Total: {len(devices)} active device(s) found\n", Colors.GREEN + Colors.BOLD))


def print_scan_start(network: str) -> None:
    """Prints a formatted scan start message."""
    print(colorize(f"\n  [►] Starting scan on network: {network}", Colors.CYAN))
    print(colorize(f"  [►] Please wait...\n", Colors.CYAN))


def print_scan_complete(duration: float, count: int) -> None:
    """Prints a formatted scan complete message."""
    print(colorize(
        f"\n  [✔] Scan complete in {duration:.2f}s — {count} device(s) found.",
        Colors.GREEN + Colors.BOLD
    ))


def print_error(message: str) -> None:
    """Prints a formatted error message."""
    print(colorize(f"\n  [✘] Error: {message}", Colors.RED + Colors.BOLD))


def print_info(message: str) -> None:
    """Prints a formatted informational message."""
    print(colorize(f"  [i] {message}", Colors.BLUE))
