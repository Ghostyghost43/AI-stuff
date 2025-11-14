# WiFi Attack Automation Suite - Complete Edition

**AUTHORIZED USE ONLY** - For penetration testing, security research, and educational purposes.
Only use on networks you own or have explicit written permission to test.

## Overview

A comprehensive, fully-automated WiFi penetration testing toolkit that combines multiple attack vectors, OSINT capabilities, and intelligent wordlist generation to assess WiFi network security.

## Features

### 🎯 Multi-Vector Attack Capabilities

- **WPS Attacks**
  - Pixie Dust attack (fastest)
  - PIN bruteforce
  - WPS vulnerability detection

- **WPA/WPA2 Attacks**
  - PMKID attack (no clients needed)
  - WPA handshake capture with targeted deauth
  - Client tracking and enumeration

- **Automated Mode**
  - Tries all attack vectors automatically
  - Optimized attack order (fastest first)

### 📡 Comprehensive Information Gathering

- Full WiFi AP enumeration (BSSID, ESSID, channel, encryption)
- Client detection and tracking
- Signal strength monitoring
- Manufacturer identification (OUI lookup)
- WPS status and lock detection
- Channel utilization analysis

### 🔐 Advanced Password Cracking

- **Built-in Wordlist Generator**
  - Modern password patterns (2024)
  - WiFi-specific keywords
  - Year/season/month combinations
  - Common router defaults

- **OSINT-Based Wordlist Generation**
  - Interactive target profiling (Q&A)
  - Social media scraping (Facebook, Instagram, Twitter, LinkedIn)
  - Custom password mutations
  - Leet speak transformations
  - Name + year combinations
  - Location-based patterns

- **Hashcat Integration**
  - Automatic format conversion
  - Multi-wordlist support
  - GPU/CPU optimization

### 🌐 Network Connection

- Automatic connection after successful crack
- Uses NetworkManager (nmcli)
- Shows connection status and IP info

### 💻 User Interface

- Interactive menu system
- Verbose output mode
- Color-coded status messages
- Real-time progress updates
- Graceful Ctrl+C handling

## Requirements

### System Requirements
- **OS**: Linux (Kali Linux, Ubuntu, Debian, Arch)
- **Privileges**: Root/sudo access
- **Hardware**: WiFi adapter with monitor mode support

### Software Dependencies

```bash
# Essential (required)
sudo apt update
sudo apt install aircrack-ng

# Recommended (full functionality)
sudo apt install aircrack-ng hashcat wireless-tools reaver hcxtools network-manager

# Python dependencies
sudo apt install python3 python3-pip
pip3 install beautifulsoup4 requests
```

### Detailed Package List

- **aircrack-ng** - WiFi security auditing (airodump-ng, aireplay-ng, airmon-ng)
- **hashcat** - Password cracking engine
- **wireless-tools** - WiFi interface configuration (iwconfig)
- **reaver** - WPS attacks (reaver, wash)
- **hcxtools** - Packet capture and conversion (hcxdumptool, hcxpcapngtool)
- **network-manager** - Network connection (nmcli)
- **python3** - Runtime (3.6+)
- **beautifulsoup4** - HTML parsing for OSINT
- **requests** - HTTP requests for scraping

## Installation

```bash
# Clone or download the repository
cd ~/
git clone <repository-url>
cd wifi-autopwn

# Make scripts executable
chmod +x wifi_autopwn.py wordlist_generator.py

# Install dependencies
sudo apt update
sudo apt install aircrack-ng hashcat wireless-tools reaver hcxtools network-manager python3-pip
pip3 install beautifulsoup4 requests

# Download wordlist (optional but recommended)
cd ~
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

## Usage

### Quick Start (Interactive Mode)

```bash
# Basic usage
sudo python3 wifi_autopwn.py -i

# With verbose output (see all commands)
sudo python3 wifi_autopwn.py -i -v
```

### Workflow

1. **Select WiFi Interface**
   - Tool detects available wireless adapters
   - Choose your adapter (e.g., wlan0)

2. **Enable Monitor Mode**
   - Automatically enables monitor mode
   - Kills interfering processes

3. **Scan for Networks**
   - Scans for 30 seconds (or until Ctrl+C)
   - Detects APs, clients, WPS status
   - Shows encryption types and attack vectors

4. **Select Target**
   - Choose network from list
   - View detailed information (clients, encryption, manufacturer)

5. **Select Attack Vector**
   - **Automated** - Tries all methods (recommended)
   - **WPS Pixie Dust** - Fast, if WPS enabled
   - **PMKID** - No clients needed
   - **WPA Handshake** - Traditional method

6. **Password Cracking**
   - Choose wordlist option:
     - Use existing (rockyou.txt)
     - Generate custom (target-specific)
     - Combine custom + rockyou
   - Hashcat automatically cracks the hash

7. **Connect to Network**
   - Option to connect after successful crack
   - Shows connection status and IP

### Advanced Features

#### Custom Wordlist Generation

The tool includes an advanced wordlist generator that creates targeted password lists:

**Target Profiling (Q&A Mode)**
```bash
# Standalone wordlist generator
python3 wordlist_generator.py -i
```

Questions include:
- Target's name, nickname
- Family member names
- Pet names
- Birth dates
- Address, city, ZIP
- Company/workplace
- Favorite sports team
- Hobbies and interests
- School/graduation year
- Phone numbers

**OSINT Mode**
- Scrape social media profiles
- Extract keywords, names, dates
- Parse hashtags and locations
- Automatic password mutation

**Built-in Patterns**
- Common passwords (2024)
- WiFi-specific keywords
- Router defaults
- Year combinations
- Leet speak variations

#### Attack Examples

**Automated Attack (Try Everything)**
```bash
sudo python3 wifi_autopwn.py -i
# Select target
# Choose "Automated (try all methods)"
# Tries WPS → PMKID → Handshake automatically
```

**WPS Pixie Dust (Fastest)**
```bash
sudo python3 wifi_autopwn.py -i
# Select WPS-enabled network
# Choose "WPS Pixie Dust Attack"
# Usually succeeds in <5 minutes if vulnerable
```

**PMKID Attack (No Clients Needed)**
```bash
sudo python3 wifi_autopwn.py -i
# Select WPA2 network
# Choose "PMKID Attack"
# Captures in 60 seconds, no deauth needed
```

**Handshake with Custom Wordlist**
```bash
sudo python3 wifi_autopwn.py -i -v
# Select target with clients
# Choose "WPA Handshake Capture"
# Choose "Generate custom wordlist"
# Answer profiling questions
# Automatically generates + cracks
```

## Attack Vector Details

### WPS Pixie Dust
- **Speed**: Very Fast (2-5 minutes)
- **Requirements**: WPS enabled, not locked
- **Success Rate**: High on vulnerable routers
- **How it works**: Exploits weak random number generation in WPS

### PMKID Attack
- **Speed**: Fast (1-2 minutes capture)
- **Requirements**: WPA/WPA2, any client state
- **Success Rate**: Medium (depends on router)
- **How it works**: Captures PMKID from RSN IE, no deauth needed

### WPA Handshake
- **Speed**: Medium (2-5 minutes capture)
- **Requirements**: WPA/WPA2, clients connected
- **Success Rate**: High for capture
- **How it works**: Forces client reconnection to capture 4-way handshake

## Output Files

All captures and wordlists are saved to:
```
~/wifi_captures/
├── <ESSID>_handshake_<timestamp>.cap    # Handshake captures
├── <ESSID>_pmkid_<timestamp>.pcapng     # PMKID captures
├── <ESSID>_<timestamp>.hash             # Converted hashcat format
├── hashcat.pot                          # Cracked passwords
└── wordlists/
    └── custom_wordlist_<timestamp>.txt  # Generated wordlists
```

## Troubleshooting

### Monitor Mode Issues
```bash
# Manually enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Check if enabled
iwconfig wlan0
# Should show "Mode:Monitor"
```

### No Networks Found
```bash
# Verify monitor mode is working
sudo airodump-ng wlan0mon

# Try different channels
sudo iwconfig wlan0mon channel 6

# Check adapter capabilities
iw list | grep -i monitor
```

### Handshake Capture Failed
- Wait longer (some clients reconnect slowly)
- Ensure clients are connected (check scan results)
- Try multiple deauth rounds
- Use targeted deauth for specific clients

### Hashcat Not Cracking
- Try larger wordlist
- Use custom wordlist generator with target info
- Try hashcat rules for mutations
- Consider mask attack for known patterns

### Dependencies Missing
```bash
# Check what's missing
which airmon-ng airodump-ng aireplay-ng hashcat reaver

# Install missing packages
sudo apt install <package-name>
```

## Best Practices

### Legal and Ethical
1. **Only test networks you own or have written permission to test**
2. **Unauthorized access is illegal in most jurisdictions**
3. **Use for education, authorized pentesting, or security research**

### Technical
1. **Use verbose mode (-v) for debugging**
2. **Start with automated mode to try all vectors**
3. **Generate custom wordlists when targeting specific networks**
4. **Document all findings for client reports**
5. **Clean up capture files regularly**

### Operational
1. **Ensure your WiFi adapter supports monitor mode**
2. **Position yourself close to target for better signal**
3. **Avoid congested channels for better capture**
4. **Be patient - some attacks take time**
5. **Use Ctrl+C to interrupt gracefully**

## Success Rates by Attack Type

Based on typical scenarios:

| Attack Type | Speed | Success Rate | Requirements |
|------------|-------|--------------|--------------|
| WPS Pixie Dust | ⚡⚡⚡ | 60-70% | WPS enabled, not locked |
| PMKID | ⚡⚡ | 40-60% | Modern router support |
| WPA Handshake + Weak Password | ⚡ | 30-50% | Weak/common password |
| WPA Handshake + Custom Wordlist | ⚡ | 50-70% | Good target intel |
| WPA Handshake + Large Wordlist | 🐌 | 70-80% | Time + compute power |

## Wordlist Generator Details

### Password Mutations

The generator creates variations including:
- Capitalization (password, Password, PASSWORD)
- Leet speak (p4ssw0rd, p@ssw0rd)
- Year suffixes (password2024, password2023)
- Symbol suffixes (password!, password#)
- Combinations (namebirthyear, name@year)
- Reversals (drowssap)

### OSINT Capabilities

**Supported Platforms**:
- Facebook (public profiles)
- Instagram (public profiles)
- Twitter/X (public profiles)
- LinkedIn (public profiles)
- Personal websites
- Any public webpage

**Extracted Information**:
- Names (capitalized words)
- Years (1900-2024)
- Hashtags
- Locations
- Keywords

### Generation Statistics

Typical wordlist sizes:
- Built-in patterns only: ~500-1,000 passwords
- Basic profiling (5-10 fields): ~2,000-5,000 passwords
- Full profiling (15-20 fields): ~10,000-30,000 passwords
- With OSINT data: +5,000-10,000 passwords

## Examples

### Example 1: Home Router Assessment
```bash
sudo python3 wifi_autopwn.py -i -v
# Scan detects "MyHomeWiFi" with WPS enabled
# Select "WPS Pixie Dust Attack"
# Router vulnerable - password found in 3 minutes
# Connect to network: Yes
# SUCCESS - Connected to MyHomeWiFi
```

### Example 2: Business Network Pentest
```bash
sudo python3 wifi_autopwn.py -i -v
# Scan detects "AcmeCorpGuest" (WPA2, no WPS)
# Select "PMKID Attack"
# PMKID captured successfully
# Choose "Generate custom wordlist"
# Enter: Company=Acme, City=Seattle, Year=2020
# Wordlist generated: 15,000 passwords
# Hashcat finds password: "AcmeSeattle2020!"
```

### Example 3: Client Engagement
```bash
sudo python3 wifi_autopwn.py -i
# Scan detects "ClientOffice" with 5 clients
# Select "Automated (try all methods)"
# WPS locked, PMKID fails
# Handshake captured from 5 clients
# Use rockyou.txt wordlist
# Password found: "CompanyName123"
```

## Advanced Tips

### Optimizing Captures
```bash
# Position yourself for best signal
# Aim for -30 to -70 dBm power levels

# For stubborn handshakes
# Target specific high-power clients
# Increase deauth packet count
# Wait for natural reconnections
```

### Wordlist Strategies
```bash
# For home routers
# Focus on: Names, addresses, phone numbers, pets

# For businesses
# Focus on: Company name, address, founding year, slogan

# For public WiFi
# Focus on: Business name, location, phone number
```

### Combining Wordlists
```bash
# Merge custom + rockyou
cat custom_wordlist.txt /usr/share/wordlists/rockyou.txt > combined.txt

# Remove duplicates
sort -u combined.txt > combined_unique.txt

# Use with hashcat
hashcat -m 22000 capture.hash combined_unique.txt
```

## Security Notes

This tool demonstrates common WiFi vulnerabilities:

1. **WPS is insecure** - Disable on all routers
2. **Weak passwords are easily cracked** - Use strong, random passwords
3. **Personal information makes bad passwords** - Avoid names, dates, addresses
4. **WPA2 is vulnerable to offline attacks** - Use WPA3 when available
5. **Default credentials are dangerous** - Always change from factory defaults

## License & Disclaimer

This tool is provided for educational and authorized security testing purposes only.

**DISCLAIMER**:
- Unauthorized access to computer networks is illegal
- The authors are not responsible for misuse or damage
- Always obtain proper authorization before testing
- Use responsibly and ethically

## Contributing

Found a bug? Have a feature request? Want to contribute?

- Report issues on GitHub
- Submit pull requests
- Share your experiences
- Suggest improvements

## Credits

Built using:
- aircrack-ng - WiFi security suite
- hashcat - Advanced password recovery
- reaver - WPS attack tool
- hcxtools - Packet capture tools
- Python - Automation and integration

## Support

For questions, issues, or discussions:
- Check the troubleshooting section
- Review example usage scenarios
- Consult tool documentation
- Seek community support

---

**Remember**: Always hack ethically and legally! 🔒🛡️

