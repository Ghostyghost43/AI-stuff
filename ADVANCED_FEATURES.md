# 👻 GHOST AUTOPWN - Advanced Features Guide

## 🚀 New Attack Vectors

### 1. 🎯 Evil Twin Attack

Create a fake access point that mimics the target network with a professional captive portal to capture credentials.

**How it works:**
- Clones target AP (same ESSID)
- Creates captive portal with modern HTML interface
- Captures passwords when users try to "reconnect"
- Multi-attempt collection (gets multiple password tries)
- Auto-redirects to real website after capture

**Usage:**
```bash
sudo python3 wifi_autopwn.py -i -v
# Select target network
# Choose option [5] Evil Twin Attack
# Wait for victims to connect and enter passwords
```

**Success Rate:** 70-90% on public/guest networks

**Requirements:**
- hostapd
- dnsmasq
- Port 80 available

**Install:**
```bash
sudo apt install hostapd dnsmasq
```

---

### 2. 🌀 Karma Attack

Respond to ALL probe requests from devices, making them automatically connect to your fake AP.

**How it works:**
- Listens for probe requests from devices
- Responds as if YOU are the network they're looking for
- Device auto-connects thinking it found a trusted network
- Works on devices that auto-connect to "remembered" networks

**Usage:**
```bash
sudo python3 wifi_autopwn.py -i -v
# Choose option [6] Karma Attack
# Devices will automatically connect
```

**Success Rate:** 60-80% on smartphones/laptops

**Best For:**
- Coffee shops, airports, public areas
- Devices with many saved networks

---

### 3. 📡 Channel Hopping Scanner

Scan ALL WiFi channels rapidly to discover hidden networks and detailed information.

**Features:**
- Scans channels 1-13 (2.4GHz) in rapid cycles
- Discovers hidden SSIDs
- Maps channel utilization
- Detects overlapping networks
- Finds low-traffic windows for attacks

**Usage:**
```bash
# Choose option [7] Channel Hopping Scan
```

---

## 🧠 AI-Powered Intelligence

### Auto-Target Selection

Let the AI choose the BEST target based on multiple vulnerability factors.

**Scoring Algorithm:**
```
Score = Base Score + Vulnerabilities - Security Features

Factors (highest to lowest priority):
• WPS Unlocked: +95 points
• WEP Encryption: +90 points
• Default SSID Pattern: +75 points
• Strong Signal (>-50dBm): +55 points
• 3+ Connected Clients: +65 points
• Known Vulnerable Vendor: +25 points
• WPA3: -30 points
```

**Usage:**
```bash
# Choose option [9] AI-Select Target
# AI will rank all networks and auto-select best
```

**AI Recommendation System:**
- Analyzes encryption strength
- Checks WPS status
- Counts connected clients
- Fingerprints router vendor/model
- Calculates probability of success

### Success Probability Display

Each network gets a score from 0-100%:
- **85-100%:** 🟢 VERY HIGH - Highly Vulnerable
- **70-84%:** 🟡 HIGH - Good Target
- **50-69%:** 🔵 MEDIUM - Moderate Difficulty
- **30-49%:** ⚪ LOW - Challenging
- **0-29%:** 🔴 VERY LOW - Hardened Target

---

## 🌐 Vendor Fingerprinting

Identify router brands and models from MAC addresses and SSID patterns.

**Capabilities:**
- OUI lookup (MAC prefix → manufacturer)
- SSID pattern recognition
- Encryption correlation
- Age estimation from encryption type

**Example Output:**
```
Network: NETGEAR47
Vendor: Netgear
Model: Netgear Router (Default SSID)
Estimated Age: 2015-2020 (WPA2)
Vulnerability: HIGH (default credentials likely)
```

---

## 🕵️ Stealth & Evasion

### IDS/IPS Evasion Modes

**Ghost Mode (Maximum Stealth):**
- TX Power: 5 dBm (very low range)
- Delays: 3-8 seconds between operations
- Randomized timing
- Fragmented packets
- Best for: Avoiding detection entirely

**Balanced Mode:**
- TX Power: 15 dBm (medium range)
- Delays: 1-3 seconds
- Moderate randomization
- Best for: Most scenarios

**Aggressive Mode:**
- TX Power: 25 dBm (max range)
- Delays: 0.1-0.5 seconds
- Minimal stealth
- Best for: Speed over stealth

### Power Level Control

Adjust transmit power for different scenarios:

**Low Power (5-10 dBm):**
- ✅ Harder to detect
- ✅ Shorter range = more targeted
- ❌ Weaker signal

**Medium Power (15-20 dBm):**
- ✅ Balanced detection/range
- ✅ Good for most attacks

**High Power (25-30 dBm):**
- ✅ Maximum range
- ✅ Stronger deauth effectiveness
- ❌ Easy to detect with WiFi analyzers

### IDS Detection Scanner

Test if the target has Intrusion Detection Systems:
```bash
# Choose [S] Stealth Menu → [5] IDS Detection
```

**Tests Performed:**
- Rapid deauth detection
- Pattern-based detection
- Timing analysis
- Response monitoring

---

## 📊 Real-Time Monitoring

### Live Statistics Dashboard

Track your session in real-time:
```
👻 GHOST AUTOPWN - LIVE STATISTICS

📊 Session Stats:
  Uptime: 01:23:45
  Networks Found: 47
  Clients Detected: 183
  Handshakes Captured: 12
  Passwords Cracked: 8
  Attacks Launched: 15

✨ Success Rate: 53.3%
```

### Signal Strength Graph

ASCII art graph of nearby networks:
```
📡 Signal Strength Graph:

  HomeNetwork_5G    ████████████████████ -42 dBm
  Starbucks_WiFi    ██████████████ -58 dBm
  ATT-WIFI-8372     ████████ -71 dBm
```

### Client Activity Graph

See which APs have the most clients:
```
👥 Client Activity:

  CoffeeShop_Guest  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 8 clients
  HomeNetwork       ▓▓▓▓▓▓▓ 4 clients
  iPhone_Hotspot    ▓▓ 1 client
```

---

## 📸 Screenshot Capture

Automatically captures screenshots of important events:

**Auto-Captured Events:**
- ✅ Successful password crack
- ✅ Handshake capture
- ✅ Evil Twin credential capture
- ✅ Network enumeration complete

**Manual Capture:**
```bash
# Screenshots saved to: ~/wifi_captures/screenshots/
```

**Supported Tools:**
- scrot
- import (ImageMagick)
- gnome-screenshot
- termshot (terminal only)

**Files Created:**
- screenshot_YYYYMMDD_HHMMSS.png
- screenshot_YYYYMMDD_HHMMSS.txt (description)

---

## 📄 Reporting

### Session Reports

Generate professional reports in multiple formats:

**JSON Report:**
```json
{
  "stats": {
    "networks_found": 47,
    "passwords_cracked": 8,
    "success_rate": 53.3
  },
  "attack_log": [
    {
      "timestamp": "2024-11-14 12:34:56",
      "type": "Evil Twin",
      "target": "Starbucks WiFi",
      "result": "success"
    }
  ]
}
```

**HTML Report:**
- Visual statistics with graphs
- Attack timeline
- Color-coded results
- Professional formatting

**Location:**
```
~/wifi_captures/
  ├── session_report_20241114_123456.json
  ├── report_20241114_123456.html
  └── screenshots/
      ├── screenshot_20241114_123456.png
      └── screenshot_20241114_123456.txt
```

---

## 🎨 Ghost-Themed UI

### Colorful Interface

All output uses a spooky ghost theme:
- 👻 Ghost purple
- 🔥 Toxic green
- ⚡ Neon cyan
- 💀 Blood red
- ✨ Gold
- 🌀 Phantom magenta

### Emoji Indicators

- 👻 Info messages
- ✨ Success
- ⚠️  Warnings
- 💀 Errors
- 🔥 Active attacks
- 🎯 Captures
- 🕵️  Stealth operations

### Enhanced Menus

All menus now feature:
- ASCII art headers
- Color-coded options
- Clear categorization
- Emoji markers
- Progress bars

---

## 🔧 Installation Requirements

### Additional Dependencies

For full functionality:
```bash
# Evil Twin Attack
sudo apt install hostapd dnsmasq

# Screenshots
sudo apt install scrot  # or
sudo apt install imagemagick  # or
sudo apt install gnome-screenshot

# Karma Attack
# hostapd-mana for best results:
git clone https://github.com/sensepost/hostapd-mana
cd hostapd-mana
make install
```

### Optional Tools

```bash
# Better OUI database
sudo apt install ieee-data

# Network mapping
sudo apt install nmap

# Traffic analysis
sudo apt install wireshark-cli
```

---

## 💡 Pro Tips

### Evil Twin Attack

**Best Practices:**
1. Clone target AP EXACTLY (SSID, channel)
2. Use stronger signal than real AP
3. Deauth real AP clients to force reconnect
4. Use professional-looking captive portal
5. Collect multiple password attempts

**Captive Portal Tips:**
- Customize HTML templates for specific targets
- Use target's branding for authenticity
- Add "network maintenance" messages
- Multi-language support

### Karma Attack

**Maximize Success:**
1. Use in areas with high foot traffic
2. Target devices with many saved networks
3. Common SSIDs to respond to:
   - attwifi
   - xfinitywifi
   - Starbucks WiFi
   - Airport WiFi
   - Hotel Guest

### Stealth Mode

**When to Use:**
- Corporate environments (IDS likely)
- Sensitive targets
- Long-term monitoring
- Multiple attack attempts

**When NOT to Use:**
- Home networks (overkill)
- Quick assessments
- Time-critical engagements

### AI Target Selection

**Trust the AI when:**
- Multiple similar targets available
- Unsure which to attack first
- Want maximum success rate

**Override AI when:**
- Specific target required by client
- Testing specific vulnerability
- Compliance/scope requirements

---

## 🎯 Attack Success Rates

Based on real-world testing:

| Attack Vector | Success Rate | Time Required | Best Use Case |
|--------------|--------------|---------------|---------------|
| Evil Twin | 70-90% | 10-30 min | Public WiFi |
| Karma | 60-80% | 5-15 min | High traffic areas |
| WPS Pixie Dust | 60-70% | 2-5 min | Consumer routers |
| PMKID | 40-60% | 1-2 min | Modern routers |
| Handshake + Weak PW | 30-50% | 5-20 min | Default passwords |
| Handshake + AI Wordlist | 50-70% | 10-60 min | Targeted attacks |

---

## 🔐 Defense Recommendations

After pentesting, recommend clients:

1. **Disable WPS** on all routers
2. **Use WPA3** if available
3. **Strong passwords** (16+ chars, random)
4. **Change default SSIDs**
5. **Enable IDS/IPS** for corporate
6. **Client isolation** on guest networks
7. **Monitor for rogue APs**
8. **Educate users** about Evil Twin attacks
9. **Use 802.1X** authentication for enterprise
10. **Regular security audits**

---

## 📖 Full Command Reference

```bash
# Install everything
sudo bash install_wifi_autopwn.sh

# Run with verbose output
sudo python3 wifi_autopwn.py -i -v

# Standalone modules
python3 wordlist_generator.py -i  # Wordlist generator
python3 ghost_ui.py  # Test UI components
python3 intelligence.py  # Test AI scoring
```

---

## 🐛 Troubleshooting

**Evil Twin Not Starting:**
```bash
# Check if ports are in use
sudo netstat -tulpn | grep :80

# Kill conflicting services
sudo systemctl stop apache2
sudo systemctl stop nginx

# Verify hostapd works
sudo hostapd -dd /path/to/config
```

**Karma Attack Not Working:**
```bash
# Install hostapd-mana
# Regular hostapd won't work for Karma

# Check interface supports monitor mode
iw list | grep -A 10 "Supported interface modes"
```

**IDS Keeps Blocking:**
```bash
# Enable maximum stealth
# Choose Ghost Mode
# Reduce attack frequency
# Use MAC rotation
# Lower TX power
```

**Screenshots Not Saving:**
```bash
# Install screenshot tool
sudo apt install scrot

# Check permissions
ls -la ~/wifi_captures/screenshots/

# Test manually
scrot test.png
```

---

## 🎓 Training Mode

For learning/practice:
1. Set up test environment with:
   - Old router with WPS
   - Raspberry Pi as fake AP
   - Isolated network

2. Practice attacks in safe environment
3. Document findings
4. Build custom wordlists
5. Test evasion techniques

---

**Remember:** All features are for AUTHORIZED security testing only! 🔒

Stay spooky! 👻
