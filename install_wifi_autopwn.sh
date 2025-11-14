#!/bin/bash
#
# WiFi AutoPwn Installation Script
# Automated installation of all dependencies
#

echo "========================================="
echo "WiFi AutoPwn - Installation Script"
echo "========================================="
echo ""
echo "This will install all required dependencies."
echo "Requires: sudo/root privileges"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "[!] This script must be run as root (sudo)"
    exit 1
fi

echo "[+] Updating package lists..."
apt update

echo ""
echo "[+] Installing essential packages..."
apt install -y \
    aircrack-ng \
    hashcat \
    wireless-tools \
    reaver \
    hcxtools \
    network-manager \
    python3 \
    python3-pip \
    macchanger

echo ""
echo "[+] Installing Python dependencies..."
pip3 install beautifulsoup4 requests

echo ""
echo "[+] Making scripts executable..."
chmod +x wifi_autopwn.py wordlist_generator.py

echo ""
echo "[+] Creating wordlist directory..."
mkdir -p ~/wifi_captures/wordlists

echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Optional: Download rockyou.txt wordlist"
echo "  cd ~"
echo "  wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"
echo ""
echo "Usage:"
echo "  sudo python3 wifi_autopwn.py -i -v"
echo ""
echo "For help:"
echo "  python3 wifi_autopwn.py --help"
echo ""
echo "Read the documentation:"
echo "  less WIFI_AUTOPWN_README.md"
echo ""
