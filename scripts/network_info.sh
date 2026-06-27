#!/bin/bash
# ============================================================
# NetPulse - Quick Network Info Script (Bash)
# Description: Gathers basic network information before running
#              the Python scanner. Useful for diagnostics.
# Authors: Team NetPulse
# Usage: bash scripts/network_info.sh
# ============================================================

echo ""
echo "======================================================"
echo "    NetPulse - Network Information Collector"
echo "======================================================"
echo ""

# ── Get local IP address ─────────────────────────────────────
echo "[1] Local IP Address:"
if command -v ip &>/dev/null; then
    # Modern Linux (iproute2)
    LOCAL_IP=$(ip route get 8.8.8.8 2>/dev/null | grep -oP 'src \K\S+')
elif command -v ifconfig &>/dev/null; then
    # macOS / older Linux
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
else
    LOCAL_IP="Could not detect"
fi
echo "    $LOCAL_IP"
echo ""

# ── Get default gateway ──────────────────────────────────────
echo "[2] Default Gateway:"
if command -v ip &>/dev/null; then
    GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
elif command -v netstat &>/dev/null; then
    GATEWAY=$(netstat -rn | grep default | awk '{print $2}' | head -1)
else
    GATEWAY="Could not detect"
fi
echo "    $GATEWAY"
echo ""

# ── Network interfaces ───────────────────────────────────────
echo "[3] Active Network Interfaces:"
if command -v ip &>/dev/null; then
    ip link show | grep "state UP" | awk '{print "    " $2}' | tr -d ':'
else
    ifconfig | grep "^[a-z]" | awk '{print "    " $1}'
fi
echo ""

# ── ARP Table ────────────────────────────────────────────────
echo "[4] Current ARP Table (known neighbors):"
arp -n 2>/dev/null | tail -n +2 | awk '{print "    IP: " $1 "  MAC: " $3}' | head -10
echo ""

# ── DNS Servers ──────────────────────────────────────────────
echo "[5] DNS Servers:"
if [ -f /etc/resolv.conf ]; then
    grep nameserver /etc/resolv.conf | awk '{print "    " $2}'
else
    echo "    /etc/resolv.conf not found"
fi
echo ""

# ── Derive network CIDR for scanner ─────────────────────────
if [ -n "$LOCAL_IP" ] && [ "$LOCAL_IP" != "Could not detect" ]; then
    NETWORK=$(echo $LOCAL_IP | cut -d. -f1-3).0/24
    echo "======================================================"
    echo "  Suggested scan target: $NETWORK"
    echo "  Run: python main.py -n $NETWORK"
    echo "======================================================"
fi

echo ""
