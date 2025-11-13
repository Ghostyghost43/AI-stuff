# 🔥 Franken-Pentest v2.0 ULTIMATE - Update Guide

## ⚡ Quick Launch (FIXED!)

```bash
# Simple method - use the launcher
sudo bash launch.sh

# OR direct method
sudo python3 franken_ultimate.py
```

## 🆕 What's New in v2.0

### NEW MENU OPTIONS (7-14):

- **[7] Advanced Exploit Automation** - Smart auto-exploitation
- **[8] Anonymous Scanning** - Tor/Proxychains integration
- **[9] Post-Exploitation Suite** - Full automation
- **[10] Enhanced Bettercap** - Advanced MITM attacks
- **[11] Physical Attack Module** - Beacon spam, DoS, USB attacks
- **[12] Hashcat Automation** - Automated hash cracking
- **[13] MSF Database Manager** - Auto-setup & management
- **[14] Framework Updater** - Self-updating system

## 📋 Installation

If you just pulled the update:

```bash
# Make sure you're in the repo directory
cd AI-stuff

# Make launcher executable
chmod +x launch.sh franken_ultimate.py

# Launch!
sudo bash launch.sh
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the right directory
ls -la modules/

# Should see:
# - exploit_automation.py
# - anonymous_scanning.py
# - post_exploitation.py
# - etc...
```

### Still not launching?
```bash
# Try the basic version first
sudo python3 franken_pentest.py

# Then try ultimate
sudo python3 franken_ultimate.py
```

### Python path issues?
```bash
# Install in development mode
sudo pip3 install -e .
```

## 🎯 New Features Quick Guide

### 1. Anonymous Scanning Through Tor
```
Menu → [8] → [1] Start Tor
       [8] → [4] Scan Through Tor
```

### 2. WiFi Beacon Spam
```
Menu → [11] → [1] WiFi Beacon Spam
```

### 3. Auto Hash Cracking
```
Menu → [12] → [1] Auto-Crack Hashes
```

### 4. MSF Database Setup
```
Menu → [13] → [1] Auto-Setup Database
```

### 5. Post-Exploitation Automation
```
Menu → [9] → [1] Full Post-Exploitation
```

## 🔧 Advanced Usage

### Run specific module directly:
```python
from modules.physical_attacks import PhysicalAttacks
attacks = PhysicalAttacks("/root/franken-work")
attacks.wifi_beacon_spam("wlan0mon", 100)
```

### Chain multiple attacks:
```python
from modules.anonymous_scanning import AnonymousScanner
from modules.exploit_automation import ExploitAutomation

# Scan anonymously
scanner = AnonymousScanner("/root/franken-work")
scanner.start_tor()
results = scanner.tor_nmap("target.com")

# Then exploit
exploiter = ExploitAutomation("/root/franken-work")
exploiter.smart_exploit("target.com", results)
```

## 📦 Module Overview

| Module | Lines | Features |
|--------|-------|----------|
| exploit_automation | 600+ | Smart exploitation, pivoting, payload generation |
| anonymous_scanning | 500+ | Tor, proxychains, IP rotation |
| post_exploitation | 700+ | Privilege escalation, persistence, mimikatz |
| better_bettercap | 800+ | Advanced MITM, SSL stripping, credential capture |
| physical_attacks | 900+ | Beacon spam, DoS, USB attacks, bluetooth |
| hashcat_automation | 600+ | Auto hash cracking, wordlist management |
| msf_database | 300+ | PostgreSQL setup, database management |
| framework_updater | 200+ | Auto-updates, dependency checking |

**Total: 4,600+ lines of new code!**

## 🚀 Performance Tips

1. **For stealth**: Use Anonymous Scanning (option 8)
2. **For speed**: Use Advanced Exploit Automation (option 7)
3. **For persistence**: Use Post-Exploitation Suite (option 9)
4. **For physical access**: Use Physical Attacks (option 11)

## 📝 Notes

- All features require root access
- Some modules need specific tools installed (run option 17 to check)
- For authorized testing only!

## 🆘 Still Having Issues?

1. Check you have the latest code:
   ```bash
   git pull origin claude/penetest-framework-linux-011CV5a451TdDEf5XvZqQpEa
   ```

2. Reinstall dependencies:
   ```bash
   sudo bash franken-install.sh
   ```

3. Check Python version:
   ```bash
   python3 --version  # Should be 3.6+
   ```

4. Verify modules loaded:
   ```bash
   python3 -c "from modules import *; print('OK')"
   ```

---

**Version: 2.0.0-ULTIMATE**
**Date: 2024**
**For authorized security testing only!**
