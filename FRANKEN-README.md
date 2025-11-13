# 🔥 FRANKEN-PENTEST FRAMEWORK

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ███████╗██████╗  █████╗ ███╗   ██╗██╗  ██╗███████╗███╗   ██╗     ║
║    ██╔════╝██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔════╝████╗  ██║     ║
║    █████╗  ██████╔╝███████║██╔██╗ ██║█████╔╝ █████╗  ██╔██╗ ██║     ║
║    ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║╚██╗██║     ║
║    ██║     ██║  ██║██║  ██║██║ ╚████║██║  ██╗███████╗██║ ╚████║     ║
║    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝     ║
║                                                                       ║
║               THE ULTIMATE ALL-IN-ONE PENTEST FRAMEWORK              ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## 🎯 What is Franken-Pentest?

**Franken-Pentest** is a comprehensive, all-in-one penetration testing framework that combines the power of the industry's most effective security tools into a single, unified interface. Born from the need for a streamlined pentesting workflow, this "Frankenstein" of security tools brings together:

- **Metasploit Framework** - Exploitation and post-exploitation
- **Social Engineering Toolkit (SET)** - Social engineering attacks
- **Bettercap** - Network attacks and MITM
- **mdk4** - Advanced WiFi attacks
- **Aircrack-ng Suite** - Wireless security testing
- **Wireshark/tshark** - Network traffic analysis

### ⚡ Why Franken-Pentest?

- **Unified Interface**: One tool, all capabilities
- **Automated Attack Chains**: Pre-built attack workflows
- **Session Management**: Track all your activities
- **Comprehensive Logging**: Never lose track of findings
- **Auto-Reporting**: Generate professional reports automatically
- **Modular Design**: Use what you need, when you need it

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/franken-pentest.git
cd franken-pentest

# Run the installer (requires root)
sudo bash franken-install.sh

# Launch the framework
sudo franken
```

### First Run

```bash
# Simple launch
sudo python3 franken_pentest.py

# Or use the shortcut
sudo franken
```

## 📋 Features

### 🎯 Core Modules

#### 1. **Metasploit Integration**
- Launch Metasploit console
- Quick exploit search
- Database management
- Payload generation (Windows, Linux, Android, PHP, Python, PowerShell)
- Multi/Handler setup
- Port scanning
- Automated exploitation workflows

#### 2. **Social Engineering Toolkit**
- Interactive SET launcher
- Credential harvester
- Mass mailer campaigns
- Phishing page cloning
- PowerShell attack vectors

#### 3. **Bettercap Network Attacks**
- ARP spoofing
- DNS spoofing
- Network traffic sniffing
- Credential capture
- WiFi reconnaissance
- Man-in-the-Middle attacks
- SSL stripping

#### 4. **Wireless Attacks**
- Monitor mode setup
- WiFi network scanning
- Deauth attacks
- WPA/WPA2 cracking
- WEP cracking
- Evil twin attacks
- Fake access points
- mdk4 attack suite (beacon flood, auth DoS, etc.)
- Handshake capture

#### 5. **Network Sniffing**
- Wireshark GUI launcher
- tshark capture
- PCAP analysis
- Credential extraction from captures
- HTTP traffic analysis
- DNS query analysis
- TCP stream following
- SSL/TLS analysis

#### 6. **Automated Attack Chains**
- Full network compromise workflow
- WiFi attack chain
- Web application attack chain
- Credential harvesting chain
- Post-exploitation chain
- Custom attack chain builder

#### 7. **Session Management**
- Track all sessions
- View logs in real-time
- Manage captured files
- Organize loot
- Clean up old sessions

#### 8. **Report Generation**
- Automated report creation
- Markdown format
- HTML export
- Evidence inclusion
- Session log attachment

## 🛠️ Installation Details

### Supported Systems

- Kali Linux (recommended)
- Ubuntu 20.04+
- Debian 11+
- ParrotOS
- Any Debian-based Linux distribution

### What Gets Installed

**Core Tools:**
- Metasploit Framework
- Social Engineering Toolkit
- Bettercap
- Aircrack-ng suite
- mdk4
- Wireshark/tshark

**Additional Tools:**
- nmap, masscan
- sqlmap, nikto
- hydra, john, hashcat
- gobuster, dirb
- tcpdump, netcat
- binwalk, foremost

**Python Libraries:**
- scapy
- impacket
- pwntools
- requests
- pyshark

**Wordlists:**
- rockyou.txt
- SecLists collection

## 📖 Usage Examples

### Example 1: Quick Network Scan

```bash
# Launch framework
sudo franken

# Select: [1] Metasploit Integration
# Select: [6] Port Scan with Metasploit
# Enter target: 192.168.1.0/24
```

### Example 2: WiFi Attack

```bash
# Select: [4] Wireless Attacks
# Select: [1] Put Interface in Monitor Mode
# Select: [8] Capture WPA Handshake
# Follow prompts...
```

### Example 3: MITM Attack

```bash
# Select: [3] Bettercap Network Attacks
# Select: [7] Man-in-the-Middle Attack
# Enter interface: eth0
# Enter target: 192.168.1.100
```

### Example 4: Automated Network Compromise

```bash
# Select: [6] Automated Attack Chains
# Select: [1] Full Network Compromise
# Enter target: 192.168.1.0/24
# Sit back and watch!
```

## 🎓 Attack Chain Examples

### Full Network Compromise Chain

1. **Reconnaissance** - Port and service scanning
2. **Vulnerability Scanning** - Identify weaknesses
3. **Automated Exploitation** - Exploit vulnerable services
4. **Network Sniffing** - Capture traffic

### WiFi Attack Chain

1. **Enable Monitor Mode** - Prepare wireless interface
2. **Network Scan** - Discover nearby networks
3. **Target Selection** - Choose victim network
4. **Handshake Capture** - Deauth and capture
5. **Password Cracking** - Crack WPA password

### Credential Harvesting Chain

1. **MITM Setup** - Position in the middle
2. **ARP Spoofing** - Redirect traffic
3. **SSL Stripping** - Downgrade HTTPS
4. **Credential Capture** - Extract passwords
5. **Analysis** - Parse captured data

## 📁 Directory Structure

```
~/franken-work/
├── logs/              # Session logs
├── reports/           # Generated reports
├── captures/          # PCAP files and captures
└── loot/             # Extracted credentials and data
```

## 🔒 Security & Legal Notice

⚠️ **CRITICAL WARNING** ⚠️

This framework is designed for:
- **Authorized penetration testing**
- **Security research**
- **Educational purposes**
- **CTF competitions**
- **Red team exercises**

### Legal Requirements

- ✅ Always obtain written authorization
- ✅ Stay within defined scope
- ✅ Follow rules of engagement
- ✅ Report findings responsibly

### Illegal Uses

- ❌ Unauthorized network access
- ❌ Attacking systems without permission
- ❌ Stealing data
- ❌ Causing damage
- ❌ Disrupting services

**Unauthorized computer access is illegal in most jurisdictions and may result in criminal prosecution.**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Your OS and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## 📝 Changelog

### v1.0.0 (2024)
- Initial release
- Metasploit integration
- SET integration
- Bettercap integration
- Wireless attack suite
- Network sniffing capabilities
- Automated attack chains
- Report generation

## 🎯 Roadmap

- [ ] API for external integrations
- [ ] Web-based GUI
- [ ] Docker containerization
- [ ] Plugin system
- [ ] Cloud deployment support
- [ ] Enhanced reporting templates
- [ ] Integration with vulnerability scanners
- [ ] Custom payload obfuscation
- [ ] Traffic analysis ML models

## 📚 Resources

### Documentation
- [Metasploit Unleashed](https://www.offensive-security.com/metasploit-unleashed/)
- [Bettercap Documentation](https://www.bettercap.org/)
- [Aircrack-ng Tutorial](https://www.aircrack-ng.org/doku.php?id=tutorial)

### Training
- [Offensive Security Certifications](https://www.offensive-security.com/)
- [HackTheBox](https://www.hackthebox.eu/)
- [TryHackMe](https://tryhackme.com/)

## 👥 Credits

Created by combining the best tools in cybersecurity:
- Metasploit by Rapid7
- SET by TrustedSec
- Bettercap by evilsocket
- Aircrack-ng team
- mdk4 developers
- Wireshark team

## 📜 License

This tool is released for educational and authorized testing purposes only.

**Use responsibly. Happy (legal) hacking!** 🔐

---

## 🆘 Support

Need help?
- Check the documentation
- Open an issue on GitHub
- Join our community discussions

## ⭐ Show Your Support

If you find this tool useful:
- Give it a star ⭐
- Share with others
- Contribute improvements
- Report bugs

---

**Remember: With great power comes great responsibility. Use ethically!**
