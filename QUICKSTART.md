# 🚀 FRANKEN-PENTEST QUICK START GUIDE

## ⚡ Installation (5 Minutes)

### Step 1: Get the Code
```bash
git clone <your-repo-url>
cd franken-pentest
```

### Step 2: Run the Installer
```bash
sudo bash franken-install.sh
```

**What this does:**
- Installs Metasploit, SET, Bettercap, mdk4, Aircrack-ng, Wireshark
- Sets up Python dependencies
- Downloads wordlists
- Configures the system
- Creates work directories

**Time:** ~15-30 minutes depending on internet speed

### Step 3: Launch
```bash
sudo franken
```

## 🎯 Common Scenarios

### Scenario 1: "I want to test a WiFi network"

```bash
sudo franken

# Main Menu → [4] Wireless Attacks

# Enable monitor mode
→ [1] Put Interface in Monitor Mode
→ Enter interface: wlan0

# Scan for networks
→ [2] WiFi Network Scan
→ Enter monitor interface: wlan0mon
→ Press Ctrl+C after seeing your target

# Capture handshake
→ [8] Capture WPA Handshake
→ Enter monitor interface: wlan0mon
→ Enter target BSSID: [from scan]
→ Enter channel: [from scan]

# In another terminal, deauth
sudo aireplay-ng --deauth 10 -a [BSSID] wlan0mon

# Once handshake captured, crack it
→ [4] WPA/WPA2 Cracking
→ Enter capture file path
→ Enter BSSID
→ Uses rockyou.txt automatically
```

### Scenario 2: "I want to perform a network pentest"

```bash
sudo franken

# Automated approach
→ [6] Automated Attack Chains
→ [1] Full Network Compromise
→ Enter target: 192.168.1.0/24

# Manual approach
→ [1] Metasploit Integration
→ [6] Port Scan with Metasploit
→ Enter target: 192.168.1.100
→ [7] Automated Exploitation
```

### Scenario 3: "I want to do a Man-in-the-Middle attack"

```bash
sudo franken

→ [3] Bettercap Network Attacks
→ [7] Man-in-the-Middle Attack
→ Enter interface: eth0
→ Enter target IP: 192.168.1.50 (or leave blank for entire subnet)

# This automatically:
# - Enables ARP spoofing
# - Starts packet capture
# - Enables SSL stripping
# - Captures credentials
```

### Scenario 4: "I want to clone a website for phishing"

```bash
sudo franken

→ [2] Social Engineering Toolkit (SET)
→ [4] Create Phishing Page
→ Enter URL to clone: https://targetsite.com
→ Follow prompts in SET interface
```

### Scenario 5: "I want to generate a payload"

```bash
sudo franken

→ [1] Metasploit Integration
→ [4] Generate Payload

# Choose your payload type:
→ [1] Windows Reverse TCP
→ Enter LHOST: [your IP]
→ Enter LPORT: 4444

# Payload saved to ~/franken-work/loot/

# Then setup listener:
→ [5] Start Multi/Handler
→ Enter payload: windows/meterpreter/reverse_tcp
→ Enter LHOST: [your IP]
→ Enter LPORT: 4444
```

### Scenario 6: "I want to capture and analyze network traffic"

```bash
sudo franken

→ [5] Network Sniffing (Wireshark/tshark)
→ [2] Capture with tshark
→ Enter interface: eth0
→ Enter filter: [leave blank or specify]

# Let it capture for a while, then Ctrl+C

→ [3] Analyze Existing Capture
→ Enter PCAP file path
→ [6] Credentials (to extract passwords)
```

## 🔧 Pro Tips

### Tip 1: Use Attack Chains
The automated attack chains save you time by running multiple tools in sequence:
- `[6] Automated Attack Chains` → `[1] Full Network Compromise`

### Tip 2: Check Tool Status First
Before starting, verify all tools are installed:
- `[9] Tool Status Check`

### Tip 3: Generate Reports
After your pentest, generate a professional report:
- `[8] Generate Report`
- Includes all logs, captures, and loot
- Exports to Markdown and HTML

### Tip 4: Session Management
Track your work across multiple sessions:
- `[7] Session Management`
- View logs: `~/franken-work/logs/`
- View captures: `~/franken-work/captures/`
- View loot: `~/franken-work/loot/`

### Tip 5: Combine Tools
Use Bettercap for MITM while capturing in Wireshark:
1. Start Wireshark capture
2. Launch Bettercap MITM
3. Analyze captured traffic after

## 📝 Cheat Sheet

### Quick Commands
```bash
# Launch framework
sudo franken

# Check installation
franken --version

# View help
franken --help
```

### File Locations
```
Main script:     /usr/local/bin/franken-pentest
Work directory:  ~/franken-work/
Logs:            ~/franken-work/logs/
Reports:         ~/franken-work/reports/
Captures:        ~/franken-work/captures/
Loot:            ~/franken-work/loot/
Wordlists:       /usr/share/wordlists/
```

### WiFi Interfaces
```bash
# Check wireless interfaces
iwconfig

# Check if monitor mode is active
iwconfig | grep Monitor

# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0
```

### Metasploit Quick Commands
```bash
# From within msfconsole
search <term>           # Search for exploits
use <exploit>           # Select exploit
show options            # Show required options
set <option> <value>    # Set option
exploit                 # Run exploit
sessions -l             # List sessions
sessions -i <id>        # Interact with session
```

## ⚠️ Common Issues

### Issue: "Permission denied"
**Solution:** Run with sudo
```bash
sudo franken
```

### Issue: "Tool not found"
**Solution:** Re-run installer
```bash
sudo bash franken-install.sh
```

### Issue: "Monitor mode won't enable"
**Solution:** Kill network manager interference
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### Issue: "Bettercap won't start"
**Solution:** Check network interface
```bash
# List interfaces
ip a

# Use correct interface name
sudo bettercap -iface eth0
```

### Issue: "Database connection failed" (Metasploit)
**Solution:** Initialize database
```bash
sudo msfdb init
```

## 🎓 Learning Path

### Beginner → Intermediate → Advanced

**Beginner:**
1. Start with Tool Status Check
2. Try WiFi scanning (read-only)
3. Run network scans with nmap
4. Practice with HackTheBox or TryHackMe

**Intermediate:**
5. Capture handshakes
6. Crack simple passwords
7. Perform MITM attacks on test network
8. Generate and test payloads

**Advanced:**
9. Build custom attack chains
10. Perform full network pentests
11. Combine multiple techniques
12. Write professional reports

## 📚 Next Steps

After mastering the basics:

1. **Read the full documentation:** `FRANKEN-README.md`
2. **Study the attack chains:** Understand how they work
3. **Practice legally:** Use labs like:
   - HackTheBox
   - TryHackMe
   - PentesterLab
   - VulnHub VMs

4. **Get certified:**
   - OSCP (Offensive Security Certified Professional)
   - CEH (Certified Ethical Hacker)
   - GPEN (GIAC Penetration Tester)

## 🆘 Getting Help

Stuck? Here's what to do:

1. Check the session logs: `~/franken-work/logs/session_*.log`
2. Verify tools are installed: Menu option `[9]`
3. Read error messages carefully
4. Check if running as root: `sudo`
5. Open an issue on GitHub

## ✅ Pre-Flight Checklist

Before starting a pentest:

- [ ] Written authorization obtained
- [ ] Scope clearly defined
- [ ] Tools verified installed
- [ ] Network connectivity confirmed
- [ ] Backup plan ready
- [ ] Legal considerations reviewed
- [ ] Time window understood

## 🎯 Success Indicators

You're doing it right when:

✅ Tools launch without errors
✅ Captures are being saved
✅ Logs are being written
✅ You're staying in scope
✅ You're documenting findings
✅ You have authorization

## 🚫 Red Flags

Stop immediately if:

❌ You don't have written permission
❌ You're not sure if target is in scope
❌ System owners aren't aware
❌ You're causing damage
❌ Legal status is unclear

---

**Remember: Always get authorization before testing!**

Ready to start? Run: `sudo franken` 🚀
