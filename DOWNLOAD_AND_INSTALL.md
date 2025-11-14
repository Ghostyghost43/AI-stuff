# 🚀 QUICK START - Download & Install Guide

## 📥 HOW TO GET THE FILES

### Option 1: Clone the Repository (Recommended)

```bash
# Clone the entire repository
git clone https://github.com/Ghostyghost43/AI-stuff.git

# Navigate to the directory
cd AI-stuff

# Switch to the pentest platform branch
git checkout claude/gui-automation-pentest-platform-01CdXk8kDv6o5dyj5Sa2tqLX
```

### Option 2: Download ZIP from GitHub

1. Go to: **https://github.com/Ghostyghost43/AI-stuff**
2. Click the **"Code"** button (green button)
3. Select **"Download ZIP"**
4. Extract the ZIP file
5. Open terminal in the extracted folder

---

## 🔧 INSTALLATION (3 Steps)

### Step 1: Make the install script executable

```bash
chmod +x install-pentest-platform.sh
```

### Step 2: Run the installation script

```bash
sudo ./install-pentest-platform.sh
```

This will install:
- Python dependencies (PyQt5, scapy, matplotlib, etc.)
- Network tools (nmap, masscan, netcat)
- Wireless tools (aircrack-ng, reaver, hcxtools)
- Password crackers (hashcat, john)
- Web tools (nikto, sqlmap, gobuster)
- And 50+ more pentesting tools

**Installation takes 5-15 minutes depending on your internet speed.**

### Step 3: Run the platform

```bash
# Quick start script (with safety checks)
sudo ./run-pentest-platform.sh

# Or run directly
sudo python3 pentest_platform.py
```

---

## 📁 WHAT FILES YOU GET

```
AI-stuff/
├── pentest_platform.py          ← Main GUI application
├── modules/                     ← Attack modules
│   ├── network_scanner.py       ← Network scanning
│   ├── mitm_attacks.py          ← MITM attacks
│   ├── wireless_attacks.py      ← WiFi/EAPOL attacks
│   ├── hash_cracker.py          ← Hash cracking
│   ├── visualizer.py            ← Real-time graphs
│   └── automation.py            ← Automation engine
├── install-pentest-platform.sh  ← Installation script
├── run-pentest-platform.sh      ← Quick launcher
├── requirements.txt             ← Python dependencies
├── PENTEST_PLATFORM_README.md   ← Full user guide
└── ATTACKS_AND_FEATURES.md      ← 250+ features list
```

---

## ⚡ SUPER QUICK START (One-Liner)

```bash
git clone https://github.com/Ghostyghost43/AI-stuff.git && cd AI-stuff && git checkout claude/gui-automation-pentest-platform-01CdXk8kDv6o5dyj5Sa2tqLX && sudo ./install-pentest-platform.sh && sudo ./run-pentest-platform.sh
```

---

## 🎯 FIRST TIME USAGE

After installation, when you run the platform:

1. **The GUI window opens** with dark theme
2. **Select a tab** on the left:
   - 🌐 Network Scan
   - 🎯 MITM Attacks
   - 📡 Wireless/EAPOL
   - 🔓 Hash Cracking
   - ⚡ Automation
3. **Configure your attack** (enter targets, options)
4. **Click "Start Attack"**
5. **Watch real-time results** in console and graphs
6. **Save results** when done

---

## 📋 SYSTEM REQUIREMENTS

**Operating System:**
- ✅ Kali Linux (best choice)
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ Parrot OS
- ❌ Windows (not supported)
- ❌ macOS (limited support)

**Hardware:**
- **RAM:** 4GB minimum, 8GB+ recommended
- **CPU:** Any modern multi-core processor
- **Storage:** 10GB free space
- **Wireless:** Adapter with monitor mode (for WiFi attacks)
- **GPU:** Optional (for faster hash cracking with hashcat)

**Wireless Adapters (Recommended):**
- Alfa AWUS036ACH
- Alfa AWUS036NH
- TP-Link TL-WN722N (v1 only)
- Panda PAU09

---

## 🔥 QUICK EXAMPLES

### Example 1: Scan Your Network
```bash
sudo python3 pentest_platform.py
# Go to "Network Scan" tab
# Enter: 192.168.1.0/24
# Select: Quick Scan
# Click: Start Attack
```

### Example 2: Capture WiFi Handshake
```bash
sudo python3 pentest_platform.py
# Go to "Wireless/EAPOL" tab
# Click: Enable Monitor Mode
# Click: Scan for Access Points
# Enter target BSSID and channel
# Click: Capture EAPOL Handshake
```

### Example 3: Crack Password
```bash
sudo python3 pentest_platform.py
# Go to "Hash Cracking" tab
# Load your .22000 file
# Select: WPA/WPA2
# Browse to: /usr/share/wordlists/rockyou.txt
# Click: Start Cracking
```

---

## 🆘 TROUBLESHOOTING

### "Command not found: git"
```bash
sudo apt-get install git
```

### "Permission denied"
```bash
# Always run with sudo
sudo python3 pentest_platform.py
```

### "No module named 'PyQt5'"
```bash
# Re-run installation
sudo ./install-pentest-platform.sh
```

### "Wireless adapter not found"
```bash
# Check adapters
iwconfig
sudo airmon-ng
```

### Installation fails
```bash
# Update system first
sudo apt-get update
sudo apt-get upgrade
# Then retry installation
```

---

## 📞 NEED HELP?

- **Full Documentation:** Read `PENTEST_PLATFORM_README.md`
- **Feature List:** Check `ATTACKS_AND_FEATURES.md`
- **GitHub Issues:** Report problems on GitHub
- **Kali Forums:** Ask the security community

---

## ⚠️ LEGAL WARNING

**ONLY USE ON NETWORKS YOU OWN OR HAVE WRITTEN PERMISSION TO TEST**

Unauthorized use is **ILLEGAL** and can result in:
- ⚖️ Criminal prosecution
- 🚔 Imprisonment
- 💰 Heavy fines
- 📜 Permanent criminal record

**YOU ARE RESPONSIBLE FOR YOUR ACTIONS.**

---

## 🎓 LEARNING PATH

**New to pentesting?**

1. **Start with Network Scan** - Learn reconnaissance
2. **Try local testing only** - Test on your own network
3. **Read documentation** - Understand each attack
4. **Practice legally** - Use HackTheBox, TryHackMe
5. **Get certified** - Consider OSCP, CEH, or PNPT

---

## ✅ CHECKLIST FOR FIRST RUN

- [ ] Linux system (Kali/Ubuntu)
- [ ] Downloaded/cloned repository
- [ ] Ran installation script
- [ ] Have sudo/root access
- [ ] Read legal disclaimer
- [ ] Have authorization for testing
- [ ] Wireless adapter (for WiFi attacks)
- [ ] Wordlist file (rockyou.txt)

---

## 🚀 YOU'RE READY!

```bash
cd AI-stuff
sudo ./run-pentest-platform.sh
```

**Happy (legal & authorized) hacking!** 🔒

---

**Repository:** https://github.com/Ghostyghost43/AI-stuff
**Branch:** claude/gui-automation-pentest-platform-01CdXk8kDv6o5dyj5Sa2tqLX
