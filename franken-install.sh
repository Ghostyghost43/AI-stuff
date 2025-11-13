#!/bin/bash

# Franken-Pentest Framework Installation Script
# Installs all required tools: Metasploit, SET, Bettercap, mdk4, Aircrack-ng, Wireshark
# For authorized security testing only

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ███████╗██████╗  █████╗ ███╗   ██╗██╗  ██╗███████╗███╗   ██╗     ║
║    ██╔════╝██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔════╝████╗  ██║     ║
║    █████╗  ██████╔╝███████║██╔██╗ ██║█████╔╝ █████╗  ██╔██╗ ██║     ║
║    ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║╚██╗██║     ║
║    ██║     ██║  ██║██║  ██║██║ ╚████║██║  ██╗███████╗██║ ╚████║     ║
║    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝     ║
║                                                                       ║
║               PENTEST FRAMEWORK INSTALLER                            ║
╚═══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Starting Franken-Pentest installation...${NC}\n"

# Update system
echo -e "${YELLOW}[*] Updating system packages...${NC}"
apt-get update -y

# Install essential dependencies
echo -e "${YELLOW}[*] Installing essential dependencies...${NC}"
apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    net-tools \
    vim \
    tmux \
    screen \
    htop

# ===== METASPLOIT INSTALLATION =====
echo -e "\n${CYAN}[*] Installing Metasploit Framework...${NC}"
if ! command -v msfconsole &> /dev/null; then
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
    chmod 755 msfinstall
    ./msfinstall
    rm msfinstall

    # Initialize database
    systemctl start postgresql
    systemctl enable postgresql
    msfdb init

    echo -e "${GREEN}[+] Metasploit installed successfully${NC}"
else
    echo -e "${GREEN}[+] Metasploit already installed${NC}"
fi

# ===== SOCIAL ENGINEERING TOOLKIT (SET) =====
echo -e "\n${CYAN}[*] Installing Social Engineering Toolkit (SET)...${NC}"
if ! command -v setoolkit &> /dev/null; then
    apt-get install -y set

    # Or install from source
    if ! command -v setoolkit &> /dev/null; then
        cd /opt
        git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit/
        cd setoolkit
        pip3 install -r requirements.txt
        python3 setup.py install
        ln -s /opt/setoolkit/setoolkit /usr/local/bin/setoolkit
    fi

    echo -e "${GREEN}[+] SET installed successfully${NC}"
else
    echo -e "${GREEN}[+] SET already installed${NC}"
fi

# ===== BETTERCAP =====
echo -e "\n${CYAN}[*] Installing Bettercap...${NC}"
if ! command -v bettercap &> /dev/null; then
    # Install from apt
    apt-get install -y bettercap

    # If not available, install from source
    if ! command -v bettercap &> /dev/null; then
        # Install Go if needed
        if ! command -v go &> /dev/null; then
            wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
            tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
            export PATH=$PATH:/usr/local/go/bin
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
            rm go1.21.0.linux-amd64.tar.gz
        fi

        # Install bettercap
        go install github.com/bettercap/bettercap@latest
        cp ~/go/bin/bettercap /usr/local/bin/
    fi

    # Install UI
    bettercap -eval "caplets.update; ui.update; q"

    echo -e "${GREEN}[+] Bettercap installed successfully${NC}"
else
    echo -e "${GREEN}[+] Bettercap already installed${NC}"
fi

# ===== AIRCRACK-NG SUITE =====
echo -e "\n${CYAN}[*] Installing Aircrack-ng Suite...${NC}"
apt-get install -y \
    aircrack-ng \
    airmon-ng \
    airodump-ng \
    aireplay-ng \
    airbase-ng

# Install wireless tools
apt-get install -y \
    wireless-tools \
    net-tools \
    iw \
    ethtool \
    usbutils \
    pciutils

echo -e "${GREEN}[+] Aircrack-ng installed successfully${NC}"

# ===== MDK4 =====
echo -e "\n${CYAN}[*] Installing mdk4...${NC}"
if ! command -v mdk4 &> /dev/null; then
    # Try apt first
    apt-get install -y mdk4 || {
        # Build from source if not in repos
        cd /tmp
        git clone https://github.com/aircrack-ng/mdk4.git
        cd mdk4
        make
        make install
        cd ..
        rm -rf mdk4
    }
    echo -e "${GREEN}[+] mdk4 installed successfully${NC}"
else
    echo -e "${GREEN}[+] mdk4 already installed${NC}"
fi

# ===== WIRESHARK / TSHARK =====
echo -e "\n${CYAN}[*] Installing Wireshark/tshark...${NC}"
DEBIAN_FRONTEND=noninteractive apt-get install -y wireshark tshark tcpdump

# Allow non-root users to capture packets
dpkg-reconfigure -p high wireshark-common 2>/dev/null || true
usermod -a -G wireshark $(who am i | awk '{print $1}') 2>/dev/null || true

echo -e "${GREEN}[+] Wireshark installed successfully${NC}"

# ===== ADDITIONAL PENTESTING TOOLS =====
echo -e "\n${CYAN}[*] Installing additional pentesting tools...${NC}"

# Network tools
apt-get install -y \
    nmap \
    masscan \
    netcat \
    socat \
    netdiscover \
    arp-scan

# Web tools
apt-get install -y \
    nikto \
    sqlmap \
    wfuzz \
    gobuster \
    dirb \
    whatweb \
    wafw00f

# Password tools
apt-get install -y \
    john \
    hashcat \
    hydra \
    medusa \
    crunch \
    wordlists

# Extraction and analysis
apt-get install -y \
    binwalk \
    foremost \
    exiftool \
    strings \
    hexedit

# Python libraries
echo -e "${YELLOW}[*] Installing Python libraries...${NC}"
pip3 install --upgrade pip
pip3 install \
    scapy \
    pwntools \
    impacket \
    requests \
    beautifulsoup4 \
    paramiko \
    python-nmap \
    pyshark \
    netaddr \
    netifaces \
    colorama \
    tabulate

# ===== WORDLISTS =====
echo -e "\n${CYAN}[*] Setting up wordlists...${NC}"
if [ -f /usr/share/wordlists/rockyou.txt.gz ]; then
    gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || true
fi

# Download SecLists if not present
if [ ! -d /usr/share/wordlists/SecLists ]; then
    git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/SecLists
fi

# ===== FRAMEWORK SETUP =====
echo -e "\n${CYAN}[*] Setting up Franken-Pentest Framework...${NC}"

# Make main script executable
chmod +x franken_pentest.py

# Create symbolic link
ln -sf "$(pwd)/franken_pentest.py" /usr/local/bin/franken-pentest

# Create work directory
mkdir -p ~/franken-work/{logs,reports,captures,loot}

# ===== SYSTEM CONFIGURATION =====
echo -e "\n${CYAN}[*] Configuring system...${NC}"

# Disable network manager interference with wireless tools
if systemctl is-active --quiet NetworkManager; then
    cat > /etc/NetworkManager/conf.d/unmanaged.conf << EOF
[keyfile]
unmanaged-devices=interface-name:wlan*;interface-name:*mon
EOF
    systemctl restart NetworkManager
fi

# ===== KERNEL MODULES FOR WIRELESS =====
echo -e "${YELLOW}[*] Loading wireless kernel modules...${NC}"
modprobe mac80211 2>/dev/null || true

# ===== VERIFICATION =====
echo -e "\n${CYAN}[*] Verifying installation...${NC}"

tools_check() {
    local tool=$1
    if command -v "$tool" &> /dev/null; then
        echo -e "${GREEN}  ✓ $tool${NC}"
        return 0
    else
        echo -e "${RED}  ✗ $tool${NC}"
        return 1
    fi
}

echo -e "\n${YELLOW}Core Tools:${NC}"
tools_check "msfconsole"
tools_check "msfvenom"
tools_check "setoolkit" || tools_check "set"
tools_check "bettercap"
tools_check "aircrack-ng"
tools_check "airodump-ng"
tools_check "aireplay-ng"
tools_check "mdk4"
tools_check "wireshark"
tools_check "tshark"

echo -e "\n${YELLOW}Additional Tools:${NC}"
tools_check "nmap"
tools_check "sqlmap"
tools_check "hydra"
tools_check "john"
tools_check "hashcat"

# ===== CREATE QUICK LAUNCH SCRIPT =====
cat > /usr/local/bin/franken << 'LAUNCHER'
#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "Franken-Pentest requires root privileges"
    exec sudo python3 /usr/local/bin/franken-pentest "$@"
else
    exec python3 /usr/local/bin/franken-pentest "$@"
fi
LAUNCHER

chmod +x /usr/local/bin/franken

# ===== COMPLETION =====
echo -e "\n${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════╗
║                     INSTALLATION COMPLETE!                            ║
╚═══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}To launch the framework, run:${NC}"
echo -e "${YELLOW}  sudo franken${NC}"
echo -e "${YELLOW}  OR${NC}"
echo -e "${YELLOW}  sudo python3 franken_pentest.py${NC}\n"

echo -e "${CYAN}Work directory:${NC} ~/franken-work/"
echo -e "${CYAN}Wordlists:${NC} /usr/share/wordlists/\n"

echo -e "${RED}[!] IMPORTANT REMINDERS:${NC}"
echo -e "${RED}  • Only use for authorized testing!${NC}"
echo -e "${RED}  • Unauthorized access is illegal!${NC}"
echo -e "${RED}  • Reboot may be required for wireless tools${NC}\n"

echo -e "${YELLOW}[*] You may need to log out and back in for group changes to take effect${NC}"
echo -e "${YELLOW}[*] Run 'sudo franken' to start the framework${NC}\n"
