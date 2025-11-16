# Bettercap Complete Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Network Interface Setup](#network-interface-setup)
5. [Core Concepts](#core-concepts)
6. [Common Commands](#common-commands)

---

## Introduction

**Bettercap** is a powerful, flexible, and portable network attack and monitoring framework. It's designed for WiFi, Bluetooth Low Energy, wireless HID hijacking, and Ethernet networks reconnaissance and MITM attacks.

### Key Features
- Network reconnaissance and monitoring
- Man-in-the-Middle (MITM) attacks
- WiFi attacks (deauth, handshake capture, evil twin)
- ARP spoofing
- DNS spoofing
- HTTP/HTTPS proxy and manipulation
- Network sniffing and packet capture
- Credential harvesting
- Caplet scripting for automation

### Legal Warning
⚠️ **IMPORTANT**: Bettercap is a penetration testing tool. Only use it on networks you own or have explicit written permission to test. Unauthorized network attacks are illegal and punishable by law.

---

## Installation

### Prerequisites
- Linux (Kali, Ubuntu, Debian, etc.) or macOS
- Root/sudo privileges
- Network adapter that supports monitor mode (for WiFi attacks)

### Method 1: Package Manager (Recommended)

#### Debian/Ubuntu/Kali Linux
```bash
sudo apt update
sudo apt install bettercap
```

#### Arch Linux
```bash
sudo pacman -S bettercap
```

#### macOS (Homebrew)
```bash
brew install bettercap
```

### Method 2: Pre-compiled Binaries
Download from: https://github.com/bettercap/bettercap/releases

```bash
# Download latest release
wget https://github.com/bettercap/bettercap/releases/download/v2.32.0/bettercap_linux_amd64_v2.32.0.zip

# Unzip
unzip bettercap_linux_amd64_v2.32.0.zip

# Move to /usr/local/bin
sudo mv bettercap /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/bettercap
```

### Method 3: Build from Source
```bash
# Install Go (if not installed)
sudo apt install golang

# Install dependencies
sudo apt install build-essential libpcap-dev libusb-1.0-0-dev libnetfilter-queue-dev

# Clone repository
git clone https://github.com/bettercap/bettercap.git
cd bettercap

# Build
make build

# Install
sudo make install
```

### Verify Installation
```bash
bettercap -version
```

### Install UI (Web Interface)
```bash
# Install caplets
sudo bettercap -eval "caplets.update; ui.update; quit"
```

---

## Basic Usage

### Starting Bettercap

#### Interactive Mode
```bash
sudo bettercap
```

#### Specify Interface
```bash
sudo bettercap -iface eth0
```

#### Start with Caplet
```bash
sudo bettercap -caplet http-ui
```

#### Non-interactive (Run Commands)
```bash
sudo bettercap -eval "net.probe on; net.show"
```

### Basic Commands

Once in the interactive shell:

```bash
# Show help
help

# List available modules
help modules

# Get help for specific module
help net.probe

# Show network hosts
net.show

# Enable network discovery
net.probe on

# Exit bettercap
quit
```

---

## Network Interface Setup

### List Available Interfaces
```bash
# In bettercap
get iface

# Or from system
ip link show
ifconfig
```

### Monitor Mode (WiFi)

Enable monitor mode for WiFi attacks:

```bash
# Stop network manager
sudo systemctl stop NetworkManager

# Kill interfering processes
sudo airmon-ng check kill

# Enable monitor mode
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Or use airmon-ng
sudo airmon-ng start wlan0
```

Disable monitor mode:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---

## Core Concepts

### Caplets
Caplets are scripts that automate bettercap operations. They use simple command syntax.

**Location**: `/usr/local/share/bettercap/caplets/`

**Create custom caplet** (`my-script.cap`):
```bash
# Enable network probing
net.probe on

# Start ARP spoofing
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# Enable sniffer
net.sniff on
```

**Run caplet**:
```bash
sudo bettercap -caplet my-script.cap
```

### Modules
Bettercap is modular. Key modules include:

- **net.probe** - Network discovery
- **net.recon** - Active network reconnaissance
- **arp.spoof** - ARP spoofing for MITM
- **dhcp6.spoof** - DHCPv6 spoofing
- **dns.spoof** - DNS spoofing
- **http.proxy** - HTTP transparent proxy
- **https.proxy** - HTTPS transparent proxy
- **net.sniff** - Packet sniffer
- **wifi.recon** - WiFi reconnaissance
- **wifi.deauth** - WiFi deauthentication
- **ble.recon** - Bluetooth LE scanning

---

## Common Commands

### Network Discovery
```bash
# Start network probing
net.probe on

# Show discovered hosts
net.show

# Active reconnaissance with ARP
net.recon on

# Show specific host details
net.show 192.168.1.10
```

### Setting Variables
```bash
# Set ARP spoof targets
set arp.spoof.targets 192.168.1.0/24

# Set gateway to spoof
set arp.spoof.fullduplex true

# Set DNS spoof domain
set dns.spoof.domains example.com

# View all settings
get *

# View specific setting
get arp.spoof.targets
```

### Logging
```bash
# Enable logging to file
set events.stream.output /root/bettercap.log
events.stream on

# Log HTTP requests
set http.proxy.sslstrip true
http.proxy on
```

### Web UI
```bash
# Start web UI (default: http://127.0.0.1:80)
sudo bettercap -caplet http-ui

# Access UI
# Username: user
# Password: pass

# Change credentials
set api.rest.username admin
set api.rest.password newpassword
```

---

## Tips and Best Practices

### Performance
- Use targeted spoofing instead of whole network
- Disable unnecessary modules
- Use caplets for repeated tasks

### Stealth
- Avoid deauth floods (use controlled bursts)
- Use passive reconnaissance when possible
- Monitor for detection systems

### Troubleshooting
```bash
# Check network connectivity
ping 8.8.8.8

# Verify IP forwarding
cat /proc/sys/net/ipv4/ip_forward
# Should be 1, if not:
sudo sysctl -w net.ipv4.ip_forward=1

# Check iptables rules
sudo iptables -L -t nat

# Clear iptables (if needed)
sudo iptables -F
sudo iptables -t nat -F
```

### Session Management
```bash
# Save session to file
bettercap> events.stream.output /tmp/session.log

# Load previous caplet on startup
sudo bettercap -caplet /path/to/script.cap
```

---

## Advanced Features

### REST API
Bettercap includes a REST API for programmatic control:

```bash
# Start API server
api.rest on

# Example API call (from another terminal)
curl -k https://localhost:8083/api/session -u user:pass
```

### GPS Integration
```bash
# If you have GPS device
set gps.device /dev/ttyUSB0
set gps.baudrate 9600
gps on
```

### Custom Scripts
Bettercap supports JavaScript for custom packet manipulation:

```javascript
// proxy-script.js
function onRequest(req, res) {
    if(req.Hostname.indexOf('example.com') != -1) {
        log("Request to example.com detected");
    }
}
```

Load script:
```bash
set https.proxy.script /path/to/proxy-script.js
```

---

## Next Steps

- [MITM Attack Guide](BETTERCAP-MITM-GUIDE.md) - Complete Man-in-the-Middle attack tutorials
- [WiFi Pentesting Guide](BETTERCAP-WIFI-GUIDE.md) - WiFi attacks and monitoring
- [Quick Reference](BETTERCAP-CHEATSHEET.md) - Command cheat sheet

---

## Resources

- Official Website: https://www.bettercap.org/
- Documentation: https://www.bettercap.org/usage/
- GitHub: https://github.com/bettercap/bettercap
- Community: https://community.bettercap.org/

---

**Last Updated**: November 2025
**Version**: 2.32.0+
