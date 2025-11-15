#!/bin/bash
#
# WiFiCrack Installer - Complete Package Setup
# Installs all required tools for modern WiFi security auditing
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╦ ╦╦╔═╗╦╔═╗┬─┐┌─┐┌─┐┬┌─
║║║║╠╣ ║║  ├┬┘├─┤│  ├┴┐
╚╩╝╩╚  ╩╚═╝┴└─┴ ┴└─┘┴ ┴
WiFiCrack Complete Package Installer
EOF
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should NOT be run as root${NC}"
   echo -e "${YELLOW}It will request sudo privileges when needed${NC}"
   exit 1
fi

echo -e "${CYAN}[*] Installing WiFiCrack and all dependencies...${NC}\n"

# Update package list
echo -e "${BLUE}[1/9] Updating package list...${NC}"
sudo apt update

# Install Python 3 and pip
echo -e "${BLUE}[2/9] Installing Python dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-dev

# Install aircrack-ng suite
echo -e "${BLUE}[3/9] Installing aircrack-ng suite...${NC}"
sudo apt install -y aircrack-ng

# Install hashcat
echo -e "${BLUE}[4/9] Installing hashcat...${NC}"
sudo apt install -y hashcat

# Install hcxtools (for modern hash formats)
echo -e "${BLUE}[5/9] Installing hcxtools...${NC}"
if ! command -v hcxpcapngtool &> /dev/null; then
    sudo apt install -y hcxtools || {
        echo -e "${YELLOW}Installing hcxtools from source...${NC}"
        cd /tmp
        sudo apt install -y git build-essential pkg-config libcurl4-openssl-dev libssl-dev zlib1g-dev
        git clone https://github.com/ZerBea/hcxtools.git
        cd hcxtools
        make
        sudo make install
        cd ..
        rm -rf hcxtools
        cd - > /dev/null
    }
else
    echo -e "${GREEN}hcxtools already installed${NC}"
fi

# Install hcxdumptool (for capturing PMKID)
echo -e "${BLUE}[6/9] Installing hcxdumptool...${NC}"
if ! command -v hcxdumptool &> /dev/null; then
    sudo apt install -y hcxdumptool || {
        echo -e "${YELLOW}Installing hcxdumptool from source...${NC}"
        cd /tmp
        sudo apt install -y git build-essential pkg-config libcurl4-openssl-dev libssl-dev
        git clone https://github.com/ZerBea/hcxdumptool.git
        cd hcxdumptool
        make
        sudo make install
        cd ..
        rm -rf hcxdumptool
        cd - > /dev/null
    }
else
    echo -e "${GREEN}hcxdumptool already installed${NC}"
fi

# Install additional wireless tools
echo -e "${BLUE}[7/9] Installing additional wireless tools...${NC}"
sudo apt install -y wireless-tools iw net-tools macchanger

# Install optional but useful tools
echo -e "${BLUE}[8/9] Installing optional tools...${NC}"
sudo apt install -y \
    reaver \
    pixiewps \
    bully \
    mdk4 \
    crunch \
    john \
    cowpatty 2>/dev/null || echo -e "${YELLOW}Some optional tools may not be available${NC}"

# Install Python packages
echo -e "${BLUE}[9/9] Installing Python packages...${NC}"
pip3 install --user scapy 2>/dev/null || echo -e "${YELLOW}Scapy installation optional${NC}"

# Make wificrack.py executable
echo -e "${CYAN}[*] Setting up WiFiCrack...${NC}"
chmod +x wificrack.py

# Create symlink for easy access (optional)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$SCRIPT_DIR/wificrack.py" "$HOME/.local/bin/wificrack" 2>/dev/null || true
    echo -e "${GREEN}Created symlink: ~/.local/bin/wificrack${NC}"
fi

# Download common wordlists
echo -e "${CYAN}[*] Setting up wordlists...${NC}"
mkdir -p wordlists

# Create a basic wordlist
echo -e "${BLUE}Creating basic wordlist...${NC}"
./wificrack.py wordlist -o wordlists/common-wifi.txt

# Download rockyou if available
if [ ! -f "wordlists/rockyou.txt" ]; then
    echo -e "${YELLOW}[*] Download rockyou.txt for better results:${NC}"
    echo -e "${YELLOW}    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O wordlists/rockyou.txt${NC}"
fi

# Create configuration file
echo -e "${CYAN}[*] Creating configuration...${NC}"
cat > wificrack.conf << 'EOL'
# WiFiCrack Configuration

# Default wordlist
DEFAULT_WORDLIST=wordlists/common-wifi.txt

# Default network interface (change this to your wireless interface)
DEFAULT_INTERFACE=wlan0

# Number of worker threads (0 = auto-detect)
WORKERS=0

# Capture timeout (seconds)
CAPTURE_TIMEOUT=60

# Hashcat options
HASHCAT_OPTS=--force

# Aircrack-ng options
AIRCRACK_OPTS=
EOL

echo -e "${GREEN}Configuration file created: wificrack.conf${NC}"

# Verify installations
echo -e "\n${CYAN}[*] Verifying installations...${NC}"

TOOLS=(
    "airmon-ng"
    "airodump-ng"
    "aireplay-ng"
    "aircrack-ng"
    "hashcat"
    "hcxpcapngtool"
    "hcxdumptool"
)

ALL_INSTALLED=true
for tool in "${TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        VERSION=$(command -v "$tool")
        echo -e "${GREEN}✓${NC} $tool: ${GREEN}installed${NC}"
    else
        echo -e "${RED}✗${NC} $tool: ${RED}not found${NC}"
        ALL_INSTALLED=false
    fi
done

# Final instructions
echo -e "\n${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║               Installation Complete!                         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}\n"

if [ "$ALL_INSTALLED" = true ]; then
    echo -e "${GREEN}All required tools installed successfully!${NC}\n"
else
    echo -e "${YELLOW}Some tools failed to install. Check errors above.${NC}\n"
fi

echo -e "${CYAN}Quick Start:${NC}"
echo -e "  1. Scan for networks:"
echo -e "     ${YELLOW}sudo ./wificrack.py capture -i wlan0 --scan${NC}\n"
echo -e "  2. Capture handshake:"
echo -e "     ${YELLOW}sudo ./wificrack.py capture -i wlan0 -b <BSSID> -c <CHANNEL>${NC}\n"
echo -e "  3. Crack password:"
echo -e "     ${YELLOW}./wificrack.py crack -f handshake.22000 -w wordlists/common-wifi.txt --hashcat${NC}\n"
echo -e "  4. Generate wordlist:"
echo -e "     ${YELLOW}./wificrack.py wordlist -o my-wordlist.txt -p password admin welcome${NC}\n"

echo -e "${CYAN}Advanced Features:${NC}"
echo -e "  • PMKID attacks (clientless):"
echo -e "    ${YELLOW}sudo hcxdumptool -i wlan0 -o capture.pcapng --enable_status=1${NC}"
echo -e "    ${YELLOW}hcxpcapngtool -o capture.22000 capture.pcapng${NC}"
echo -e "    ${YELLOW}hashcat -m 22000 capture.22000 wordlists/rockyou.txt${NC}\n"

echo -e "${CYAN}Documentation:${NC}"
echo -e "  Read WIFICRACK-README.md for detailed usage instructions\n"

echo -e "${RED}IMPORTANT:${NC}"
echo -e "  ${YELLOW}This tool is for CTF challenges and authorized testing ONLY!${NC}"
echo -e "  ${YELLOW}Unauthorized access to networks is illegal.${NC}\n"

echo -e "${CYAN}Recommended Downloads:${NC}"
echo -e "  • RockYou wordlist (134MB):"
echo -e "    ${YELLOW}wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O wordlists/rockyou.txt${NC}\n"

echo -e "${GREEN}Happy hacking! (legally!)${NC}\n"
