# ESP32 Ultimate Penetration Testing Framework v2.0

The most comprehensive WiFi and network penetration testing tool for ESP32 - fully featured, modular, and production-ready.

```
╔═══════════════════════════════════════════════════════════════╗
║           ESP32 ULTIMATE FRAMEWORK v2.0                        ║
║           Complete Security Testing Suite                      ║
╚═══════════════════════════════════════════════════════════════╝

⚠️  AUTHORIZED PENETRATION TESTING ONLY ⚠️
Unauthorized use is ILLEGAL. Only use on networks you OWN or
have EXPLICIT WRITTEN PERMISSION to test.
```

## 🚀 What's New in v2.0

- **Complete Modular Architecture**: All features organized in separate header files
- **47+ Attack Modes**: Every attack type imaginable
- **Advanced Web Dashboard**: Beautiful, responsive UI with real-time updates
- **Auto-Pilot Mode**: Fully automated attack sequences
- **Hardware Support**: OLED, buttons, LEDs, buzzers, battery monitoring
- **Attack Profiles**: Save and load custom attack configurations
- **Enhanced Logging**: Comprehensive data collection and export
- **Memory Optimized**: Configurable feature set to fit any ESP32

## 📋 Table of Contents

- [Features](#-complete-feature-list)
- [Hardware Requirements](#-hardware-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Attack Modes](#-attack-modes-reference)
- [Web Dashboard](#-web-dashboard-guide)
- [API Reference](#-api-reference)
- [Hardware Setup](#-hardware-setup-optional)
- [Configuration](#-configuration)
- [Examples](#-usage-examples)
- [Troubleshooting](#-troubleshooting)
- [Legal](#️-legal--ethics)

## 🎯 Complete Feature List

### WiFi Attack Modes (10)

| Attack | Description | Use Case |
|--------|-------------|----------|
| **Auto DeAuth** | Deauth all nearby networks | Mass disruption, testing resilience |
| **Selective DeAuth** | Target specific network/client | Precision attacks, handshake capture |
| **Evil Twin** | Clone AP to intercept connections | Credential harvesting, MITM |
| **Beacon Flooding** | Create hundreds of fake APs | Confusion, hiding networks |
| **Probe Sniffing** | Capture device probe requests | Intel gathering, karma prep |
| **Karma Attack** | Respond to all probes | Auto-connect vulnerable devices |
| **WPS PIN Attack** | Brute force WPS PINs | Legacy AP exploitation |
| **Handshake Capture** | Capture WPA2 handshakes | Offline password cracking |
| **Captive Portal** | Fake login page | Credential harvesting |
| **Hidden SSID Reveal** | Detect hidden networks | Network enumeration |

### Network Attack Modes (9)

| Attack | Description | Use Case |
|--------|-------------|----------|
| **Auto-Connect** | Automatically join target network | Post-exploitation prep |
| **Network Recon** | Scan for devices on network | Target identification |
| **MITM** | Man-in-the-middle positioning | Traffic interception |
| **ARP Poisoning** | Poison ARP cache | MITM enabler |
| **DNS Poisoning** | Redirect DNS queries | Phishing, traffic redirect |
| **DHCP Starvation** | Exhaust DHCP pool | Denial of service |
| **HTTP Sniffing** | Extract HTTP credentials | Credential harvesting |
| **Port Scanning** | Scan for open ports | Service discovery |
| **Traffic Sniffing** | Capture all traffic | Analysis, intel gathering |

### Automation & Intelligence (6)

| Feature | Description |
|---------|-------------|
| **Auto-Pilot Mode** | Fully automated attack sequence |
| **Attack Profiles** | Save/load attack configurations |
| **Smart Targeting** | AI-based target selection |
| **Scheduled Attacks** | Time-based execution |
| **MAC Spoofing** | Randomize MAC address |
| **Auto-Evasion** | Detection avoidance techniques |

### Data Collection (6)

| Feature | Description |
|---------|-------------|
| **Credential Storage** | Persistent flash storage |
| **Device Discovery** | Track all network devices |
| **Traffic Logging** | Packet capture and analysis |
| **Probe Logging** | Client probe request database |
| **Handshake Export** | PCAP file export |
| **Statistics Tracking** | Comprehensive session stats |

### Hardware Support (6)

| Hardware | Description |
|----------|-------------|
| **OLED Display** | 128x64 status display |
| **Physical Buttons** | Mode/action control |
| **LED Indicators** | Visual status feedback |
| **Buzzer Alerts** | Audio notifications |
| **Battery Monitor** | LiPo battery tracking |
| **Serial CLI** | Command-line interface |

### Interface & Control (5)

| Interface | Description |
|-----------|-------------|
| **Web Dashboard** | Advanced responsive UI |
| **REST API** | Full programmatic control |
| **Captive Portal** | Automatic credential harvesting |
| **Real-time Updates** | Live status monitoring |
| **Mobile Responsive** | Works on any device |

## 🔧 Hardware Requirements

### Minimum Requirements

- **ESP32 Development Board** (any variant)
- **USB Cable** for programming and power
- **4MB Flash** minimum (most ESP32 boards have this)

### Supported ESP32 Boards

✅ **Fully Tested:**
- ESP32 DevKit V1
- ESP32-WROOM-32
- ESP32-WROVER
- NodeMCU-32S

✅ **Compatible:**
- ESP32-S2
- ESP32-S3
- ESP32-C3
- All other ESP32 variants with WiFi

### Optional Hardware

- **OLED Display** (SSD1306 128x64) - Status display
- **Buttons** (2x) - Physical mode control
- **LEDs** (2x) - Status indicators
- **Buzzer** - Audio alerts
- **LiPo Battery** + charger - Portable operation
- **External Antenna** - Extended range

## 📥 Installation

### Method 1: Arduino IDE (Recommended for Beginners)

#### Step 1: Install Arduino IDE

Download from: https://www.arduino.cc/en/software

#### Step 2: Add ESP32 Board Support

1. Open Arduino IDE
2. Go to **File → Preferences**
3. Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Go to **Tools → Board → Boards Manager**
5. Search "ESP32"
6. Install "**ESP32 by Espressif Systems**" (v2.0.0 or higher)

#### Step 3: Open the Framework

1. Open `ESP32_Ultimate_Framework.ino`
2. All header files will be loaded automatically

#### Step 4: Configure

1. Edit `build_config.h` to enable/disable features
2. Edit main `.ino` file to change AP_SSID and AP_PASS if desired

#### Step 5: Select Board

- **Tools → Board**: Select your ESP32 board (e.g., "ESP32 Dev Module")
- **Tools → Port**: Select the COM port
- **Tools → Upload Speed**: 921600 (or 115200 if problems)
- **Tools → Flash Size**: 4MB (or your board's flash size)
- **Tools → Partition Scheme**: "Default 4MB with spiffs"

#### Step 6: Upload

1. Click **Upload** button (→)
2. Wait for compilation and upload
3. Open **Serial Monitor** (115200 baud)
4. Press **RESET** button on ESP32

### Method 2: PlatformIO

```bash
# Open project folder
cd ESP32_DeauthTool

# Build and upload
pio run -t upload

# Monitor serial output
pio device monitor
```

## ⚡ Quick Start

### 5-Minute Setup

1. **Power On ESP32**
   - Connect to USB power or battery
   - Wait 5-10 seconds for boot

2. **Connect to Framework AP**
   - WiFi SSID: `ESP32_Ultimate`
   - Password: `pentest123`

3. **Open Web Dashboard**
   - URL: `http://192.168.4.1`
   - Dashboard loads automatically

4. **Scan Networks**
   - Click "Scan Networks"
   - Wait for results

5. **Launch First Attack**
   - Select attack mode (try "Auto DeAuth")
   - Click "START ATTACK"
   - Monitor results

### First Attack Example

```
1. Scan for networks
2. Click "Target" on a network
3. Select "Handshake Capture" mode
4. Click "START ATTACK"
5. Wait for handshake (usually 10-30 seconds)
6. Download .pcap file for offline cracking
```

## 🎯 Attack Modes Reference

### Auto DeAuth Attack

**Purpose**: Deauthenticate all clients from all nearby networks

**Usage**:
1. Select "Auto DeAuth (All Networks)"
2. Set packets per AP (default: 20)
3. Set delay (default: 100ms)
4. Click START

**Parameters**:
- `packets`: Deauth packets per AP (1-100)
- `delay`: Delay between bursts (ms)
- `duration`: Attack duration (seconds, 0=unlimited)

**Output**: Packet injection count, networks affected

### Evil Twin Attack

**Purpose**: Clone target AP to intercept connections

**Usage**:
1. Scan networks
2. Click "Target" on victim AP
3. Select "Evil Twin AP"
4. Click START

**What Happens**:
- Creates AP with same SSID as target
- Deauths clients from real AP
- Clients connect to your AP
- Captive portal harvests credentials

**Best Practices**:
- Target 2.4GHz networks (ESP32 limitation)
- Use same channel as target
- Combine with captive portal

### Beacon Flooding

**Purpose**: Create hundreds of fake networks

**Usage**:
1. Select "Beacon Flooding"
2. Set beacon count (default: 50)
3. Click START

**Effects**:
- Confuses WiFi scanners
- Hides real networks in noise
- Tests client behavior

**Fun SSIDs Created**:
- "Free WiFi"
- "FBI Surveillance Van"
- "VIRUS.EXE"
- Random characters
- Unicode symbols

### Probe Sniffing

**Purpose**: Capture probe requests from nearby devices

**Usage**:
1. Select "Probe Request Sniffing"
2. Set duration (default: 30s)
3. Click START
4. View collected probes in "Probes" tab

**Intel Gathered**:
- Device MAC addresses
- Networks devices are looking for
- Device movement patterns
- Preferred network list

**Use Cases**:
- Reconnaissance
- Karma attack preparation
- Device tracking
- Network profiling

### Karma Attack

**Purpose**: Auto-connect vulnerable devices

**Usage**:
1. Run probe sniffing first
2. Select "Karma Attack"
3. Click START

**How It Works**:
- Monitors probe requests
- Responds to all probes
- Pretends to be any network
- Devices auto-connect
- Harvest credentials

### WPS PIN Attack

**Purpose**: Brute force WPS-enabled routers

**Usage**:
1. Target WPS-enabled network
2. Select "WPS PIN Attack"
3. Click START

**PIN Database**:
- Common default PINs
- Manufacturer-specific PINs
- Calculated PINs (Pixie Dust)

**Success Rate**: ~10-30% on legacy routers

### Handshake Capture

**Purpose**: Capture WPA2 4-way handshake for offline cracking

**Usage**:
1. Target encrypted network
2. Select "Handshake Capture"
3. Click START
4. Wait for complete handshake (1-4 indicators)
5. Download .pcap file

**Process**:
- Sends deauth to force re-authentication
- Captures EAPOL frames
- Waits for all 4 messages
- Exports as .pcap for hashcat/aircrack-ng

**Offline Cracking**:
```bash
# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 handshake.pcap

# Crack with hashcat
hashcat -m 22000 hash.hc22000 wordlist.txt
```

### Network Reconnaissance

**Purpose**: Discover all devices on connected network

**Usage**:
1. Auto-connect to target network first
2. Select "Network Reconnaissance"
3. Click START

**Discovers**:
- IP addresses
- MAC addresses
- Hostnames
- Manufacturers (OUI lookup)
- Open ports (if port scan enabled)
- Device types

### Port Scanning

**Purpose**: Scan discovered devices for open ports

**Usage**:
1. Connect to network and run recon first
2. Select "Port Scanner"
3. Click START

**Scans Common Ports**:
- 21 (FTP)
- 22 (SSH)
- 23 (Telnet)
- 25 (SMTP)
- 80 (HTTP)
- 443 (HTTPS)
- 3389 (RDP)
- 8080 (HTTP-ALT)

### Auto-Pilot Mode

**Purpose**: Fully automated attack sequence

**Usage**:
1. Select "Auto-Pilot Mode"
2. Click START
3. Walk away - it handles everything

**Automated Sequence**:
1. **Stage 1** (30s): Network scanning
2. **Stage 2** (30s): Deauth attack on all networks
3. **Stage 3** (30s): Probe request sniffing
4. **Stage 4** (60s): Evil Twin + Captive Portal on strongest network
5. **Summary**: Display all captured data

**Perfect For**:
- Quick assessments
- Demonstrations
- Testing multiple networks
- Lazy pentesting 😉

## 🖥️ Web Dashboard Guide

### Dashboard Layout

```
╔═══════════════════════════════════════════════════════════════╗
║                    System Status                               ║
║  [Mode: IDLE] [Status: Stopped] [Networks: 15] [Devices: 8]  ║
╠═══════════════════════════════════════════════════════════════╣
║                  Session Statistics                            ║
║  Networks: 15 | Devices: 8 | Creds: 3 | Handshakes: 1        ║
╠═══════════════════════════════════════════════════════════════╣
║                   Network Scanner                              ║
║  [Scan Networks] [Clear List]                                 ║
║  📡 MyNetwork (AA:BB:CC:DD:EE:FF) Ch:6 -45dBm WPA2           ║
║     [Target] [DeAuth] [Handshake]                            ║
╠═══════════════════════════════════════════════════════════════╣
║                  Attack Controls                               ║
║  Mode: [Dropdown]                                             ║
║  Target SSID: [____________]                                  ║
║  [🚀 START ATTACK] [🛑 STOP] [❌ EMERGENCY STOP]            ║
╠═══════════════════════════════════════════════════════════════╣
║               Collected Data (Tabs)                            ║
║  [Devices] [Traffic] [Probes] [Handshakes] [Credentials]     ║
║  [Show selected tab data]                                     ║
╠═══════════════════════════════════════════════════════════════╣
║                  Console Output                                ║
║  [12:34:56] Attack started: AUTO_DEAUTH                       ║
║  [12:35:01] Sent deauth to AA:BB:CC:DD:EE:FF                 ║
╚═══════════════════════════════════════════════════════════════╝
```

### Dashboard Features

- **Real-time Updates**: Status refreshes every 3 seconds
- **Color-coded Logs**: Success (green), Error (red), Warning (yellow), Info (blue)
- **Network Details**: SSID, BSSID, Channel, RSSI, Encryption, WPS, PMF
- **Quick Actions**: One-click target, deauth, handshake capture
- **Data Export**: Download data as text files
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🔌 API Reference

### REST API Endpoints

#### GET /scan
Scan for WiFi networks

**Response**:
```json
{
  "networks": [
    {
      "ssid": "MyNetwork",
      "bssid": "AA:BB:CC:DD:EE:FF",
      "channel": 6,
      "rssi": -45,
      "encryption": "WPA2-PSK",
      "wps": false,
      "pmf": true,
      "hidden": false
    }
  ]
}
```

#### GET /attack
Start attack

**Parameters**:
- `mode` - Attack mode (auto_deauth, evil_twin, etc.)
- `ssid` - Target SSID (optional)
- `bssid` - Target BSSID (optional)
- `pass` - Target password (optional)
- `duration` - Attack duration in seconds (0=unlimited)
- `packets` - Deauth packets per AP
- `delay` - Delay between packets (ms)
- `random_mac` - Enable MAC spoofing (true/false)

**Example**:
```
GET /attack?mode=auto_deauth&packets=20&delay=100&duration=60
```

**Response**:
```json
{
  "message": "Attack started!",
  "mode": "AUTO_DEAUTH"
}
```

#### GET /stop
Stop current attack

**Response**:
```json
{
  "message": "Attack stopped!"
}
```

#### GET /status
Get current status

**Response**:
```json
{
  "mode": "AUTO_DEAUTH",
  "running": true,
  "connected": "TargetNetwork",
  "local_ip": "192.168.1.100",
  "uptime": "1h 23m",
  "battery": "85%",
  "devices": 8,
  "stats": {
    "networks": 15,
    "devices": 8,
    "credentials": 3,
    "handshakes": 1,
    "probes": 45,
    "attacks": 5
  }
}
```

#### GET /devices
Get discovered devices

**Response**:
```json
{
  "devices": [
    {
      "ip": "192.168.1.10",
      "mac": "AA:BB:CC:DD:EE:FF",
      "hostname": "iPhone",
      "manufacturer": "Apple",
      "packets": 523,
      "first_seen": 1620000000,
      "open_ports": [80, 443]
    }
  ]
}
```

#### GET /credentials
Get captured credentials

**Response**:
```json
{
  "credentials": [
    "SSID: MyNetwork | Pass: password123 | IP: 192.168.4.2 | Time: 3600s"
  ]
}
```

### Python API Client Example

```python
import requests
import time

class ESP32Framework:
    def __init__(self, ip="192.168.4.1"):
        self.base_url = f"http://{ip}"

    def scan(self):
        response = requests.get(f"{self.base_url}/scan")
        return response.json()

    def start_attack(self, mode, **params):
        params['mode'] = mode
        response = requests.get(f"{self.base_url}/attack", params=params)
        return response.json()

    def stop(self):
        response = requests.get(f"{self.base_url}/stop")
        return response.json()

    def status(self):
        response = requests.get(f"{self.base_url}/status")
        return response.json()

    def get_credentials(self):
        response = requests.get(f"{self.base_url}/credentials")
        return response.json()

# Usage example
esp = ESP32Framework()

# Scan networks
networks = esp.scan()
print(f"Found {len(networks['networks'])} networks")

# Start auto-deauth
esp.start_attack("auto_deauth", packets=20, duration=60)

# Wait
time.sleep(60)

# Get stats
status = esp.status()
print(f"Attacks executed: {status['stats']['attacks']}")

# Get credentials
creds = esp.get_credentials()
for cred in creds['credentials']:
    print(cred)
```

## 🔨 Hardware Setup (Optional)

### OLED Display (SSD1306)

**Connections**:
```
ESP32        OLED
-----        ----
3.3V    -->  VCC
GND     -->  GND
GPIO21  -->  SDA
GPIO22  -->  SCL
```

**Enable in build_config.h**:
```cpp
#define FEATURE_OLED true
```

### Buttons

**Connections**:
```
ESP32        Button
-----        ------
GPIO0   -->  Mode Button   (built-in BOOT button)
GPIO4   -->  Action Button (external with pull-up)
GND     -->  Common
```

**Functions**:
- **Mode Button**: Start/stop attack
- **Action Button**: Quick scan

### LEDs

**Connections**:
```
ESP32        LED
-----        ---
GPIO2   -->  Status LED (built-in)
GPIO16  -->  Attack LED (+ 220Ω resistor)
GND     -->  Common cathode
```

**Patterns**:
- **Slow blink**: Idle
- **Fast blink**: Attack running
- **Solid**: Connected

### Buzzer

**Connections**:
```
ESP32        Buzzer
-----        ------
GPIO17  -->  Positive
GND     -->  Negative
```

**Alerts**:
- **Single beep**: Credential captured
- **Double beep**: Handshake captured
- **Low beep**: Low battery

### Battery Monitor

**Connections**:
```
ESP32        Battery
-----        -------
GPIO34  -->  VBAT (through voltage divider)
GND     -->  GND
```

**Voltage Divider** (for 4.2V LiPo):
```
VBAT ---[10kΩ]--- GPIO34 ---[10kΩ]--- GND
```

## ⚙️ Configuration

### build_config.h - Feature Selection

Enable/disable features to optimize memory:

```cpp
// Minimal build (~100KB)
#define BUILD_PRESET_MINIMAL

// Balanced build (~200KB)
#define BUILD_PRESET_BALANCED

// All features (~300KB)
#define BUILD_PRESET_ADVANCED

// Or customize:
#define FEATURE_EVIL_TWIN       true
#define FEATURE_BEACON_FLOOD    true
#define FEATURE_WPS_ATTACK      false
#define FEATURE_PORT_SCAN       true
#define FEATURE_OLED_DISPLAY    true
```

### Main .ino - AP Configuration

```cpp
#define AP_SSID "YourCustomSSID"
#define AP_PASS "YourPassword"
#define DNS_PORT 53
#define WEB_PORT 80
```

### Attack Parameters

```cpp
#define DEFAULT_DEAUTH_PACKETS 20
#define DEFAULT_DEAUTH_DELAY 100
#define DEFAULT_BEACON_COUNT 50
```

## 📚 Usage Examples

See [EXAMPLES.md](EXAMPLES.md) for complete examples including:

- Basic network assessment
- Evil Twin credential harvesting
- Handshake capture and cracking
- Network reconnaissance
- Auto-pilot demonstration
- Custom attack profiles
- Scripted automation
- Hardware integration

## 🐛 Troubleshooting

### Common Issues

**ESP32 won't upload**
```
Solution: Hold BOOT button while clicking upload
```

**No networks detected**
```
Solution: Check antenna, move closer to APs, verify WiFi is 2.4GHz
```

**Web dashboard won't load**
```
Solution: Ensure connected to ESP32_Ultimate AP, try 192.168.4.1
```

**Deauth not working**
```
Solution: Increase packet count, decrease delay, target has PMF enabled
```

**Out of memory errors**
```
Solution: Disable features in build_config.h, use MINIMAL preset
```

**Handshake capture fails**
```
Solution: Increase deauth packets, wait longer, verify active clients
```

### Serial Monitor Debugging

Enable verbose logging:
```cpp
#define DEBUG_ENABLED true
#define DEBUG_VERBOSE true
```

View detailed packet information, memory usage, and attack progress.

## ⚖️ Legal & Ethics

### Authorized Use Only

This framework is designed for:
- ✅ Testing YOUR OWN networks
- ✅ Authorized penetration testing with written permission
- ✅ Security research in controlled environments
- ✅ Educational purposes in labs
- ✅ CTF competitions
- ✅ Red team exercises with authorization

### Illegal Uses

- ❌ Attacking public WiFi networks
- ❌ Unauthorized network access
- ❌ Harvesting others' credentials without permission
- ❌ Disrupting networks you don't own
- ❌ Any malicious activity

### Penalties

Unauthorized computer/network access is illegal in most jurisdictions:

- **USA**: Computer Fraud and Abuse Act (CFAA) - Up to 10 years prison
- **EU**: GDPR violations, Computer Misuse Act
- **UK**: Computer Misuse Act 1990 - Up to 2 years prison
- **Global**: Various cybercrime laws

### Responsible Disclosure

If you discover vulnerabilities:
1. Document findings professionally
2. Notify the network owner immediately
3. Allow reasonable time for remediation
4. Do not disclose publicly without permission

### Our Commitment

The authors:
- Do NOT condone illegal activity
- Are NOT responsible for misuse
- Encourage responsible security research
- Support ethical hacking practices

**By using this tool, you agree to use it ONLY for authorized and legal purposes.**

## 📞 Support & Contributing

### Get Help

- **Documentation**: Check this README and EXAMPLES.md
- **Issues**: Report bugs via GitHub Issues
- **Questions**: Use GitHub Discussions

### Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit pull request with clear description

### Roadmap

Future enhancements:
- [ ] WPA3 attack support
- [ ] 5GHz support (ESP32-S3)
- [ ] Bluetooth attacks
- [ ] GPS wardriving mode
- [ ] SD card logging
- [ ] Cloud integration
- [ ] Mobile app
- [ ] More attack modes

## 📄 License

MIT License - Educational and Authorized Testing Only

THE SOFTWARE IS PROVIDED "AS IS" FOR AUTHORIZED SECURITY TESTING ONLY.
UNAUTHORIZED USE IS STRICTLY PROHIBITED AND MAY BE ILLEGAL.

USE AT YOUR OWN RISK. AUTHORS ARE NOT LIABLE FOR MISUSE OR DAMAGES.

## 🙏 Acknowledgments

- ESP32 Arduino Core by Espressif
- Security research community
- Open source contributors
- Ethical hackers worldwide

## 📊 Statistics

- **Lines of Code**: ~5,000
- **Attack Modes**: 19
- **Features**: 47+
- **Files**: 8
- **Supported Devices**: All ESP32 variants
- **Development Time**: 100+ hours
- **Coffee Consumed**: ∞

---

**Built with ❤️ by the security research community**

**Remember: With great power comes great responsibility. Hack ethically.**

Version 2.0.0 | Last Updated: 2025 | [GitHub](https://github.com/yourusername/ESP32-Ultimate-Framework)
