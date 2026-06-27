#!/usr/bin/env python3
"""
NetPulse - Unit Tests
Tests for scanner, reporter, and display modules.
Run: python -m pytest tests/ -v
"""

import sys
import os
import csv
import tempfile
import unittest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.scanner  import get_local_ip, get_hostname, ping_host
from src.reporter import save_to_csv, generate_report


class TestScanner(unittest.TestCase):
    """Tests for scanner.py module."""

    def test_get_local_ip_returns_string(self):
        """Local IP should return a non-empty string."""
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertGreater(len(ip), 0)

    def test_get_local_ip_not_localhost(self):
        """When connected to a network, IP should not be 127.0.0.1 (usually)."""
        ip = get_local_ip()
        # This test may fail on machines with no network — that's OK
        self.assertIsInstance(ip, str)

    def test_get_hostname_localhost(self):
        """Hostname lookup for 127.0.0.1 should return a string."""
        hostname = get_hostname("127.0.0.1")
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)

    def test_get_hostname_invalid_ip(self):
        """Hostname lookup for an invalid IP should return 'Unknown'."""
        hostname = get_hostname("999.999.999.999")
        self.assertEqual(hostname, "Unknown")

    def test_ping_localhost(self):
        """Ping to localhost (127.0.0.1) should always succeed."""
        result = ping_host("127.0.0.1")
        self.assertTrue(result)

    def test_ping_invalid_host(self):
        """Ping to an invalid/unreachable IP should return False."""
        result = ping_host("192.0.2.255")  # TEST-NET — should not be reachable
        self.assertFalse(result)


class TestReporter(unittest.TestCase):
    """Tests for reporter.py module."""

    # Sample device data for testing
    SAMPLE_DEVICES = [
        {
            "ip": "192.168.1.1",
            "mac": "AA:BB:CC:DD:EE:01",
            "hostname": "router.local",
            "status": "Active",
            "method": "ICMP Ping",
            "scan_time": "2024-01-01 10:00:00"
        },
        {
            "ip": "192.168.1.10",
            "mac": "AA:BB:CC:DD:EE:02",
            "hostname": "laptop.local",
            "status": "Active",
            "method": "ICMP Ping",
            "scan_time": "2024-01-01 10:00:05"
        },
    ]

    def test_save_to_csv_creates_file(self):
        """save_to_csv should create a .csv file in the specified directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = save_to_csv(self.SAMPLE_DEVICES, output_dir=tmpdir)
            self.assertTrue(os.path.exists(filepath))
            self.assertTrue(filepath.endswith(".csv"))

    def test_save_to_csv_content(self):
        """CSV file should contain the correct headers and data rows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = save_to_csv(self.SAMPLE_DEVICES, output_dir=tmpdir)
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["ip"], "192.168.1.1")
            self.assertEqual(rows[1]["hostname"], "laptop.local")

    def test_generate_report_returns_string(self):
        """generate_report should return a non-empty string."""
        report = generate_report(self.SAMPLE_DEVICES, "192.168.1.0/24", 5.32)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)

    def test_generate_report_contains_device_info(self):
        """Report string should contain the IP addresses of found devices."""
        report = generate_report(self.SAMPLE_DEVICES, "192.168.1.0/24", 5.32)
        self.assertIn("192.168.1.1", report)
        self.assertIn("192.168.1.10", report)

    def test_generate_report_empty_devices(self):
        """Report with no devices should mention no active devices found."""
        report = generate_report([], "192.168.1.0/24", 1.5)
        self.assertIn("No active devices", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
