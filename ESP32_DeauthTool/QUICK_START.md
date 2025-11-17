# Quick Start Guide - ESP32 DeAuth Tool

## ⚡ 5-Minute Setup

### Step 1: Install Arduino IDE
Download from: https://www.arduino.cc/en/software

### Step 2: Add ESP32 Support
1. File → Preferences
2. Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Tools → Board → Boards Manager
4. Search "ESP32" → Install "ESP32 by Espressif Systems"

### Step 3: Upload Code
1. Open `ESP32_DeauthTool.ino`
2. Tools → Board → ESP32 Dev Module
3. Tools → Port → Select your ESP32's COM port
4. Click Upload (→)

### Step 4: Use the Tool
1. Connect to WiFi: `ESP32_Control` (password: `deauth123`)
2. Open browser: http://192.168.4.1
3. Click "Scan Networks"
4. Choose attack mode and click "Start Attack"

## 🎯 Attack Modes Quick Reference

| Mode | Use Case | How to Use |
|------|----------|------------|
| **Auto DeAuth** | Deauth all networks | Select mode → Start Attack |
| **Selective DeAuth** | Target one network | Scan → Target → Start Attack |
| **Captive Portal** | Harvest credentials | Select mode → Start Attack → Wait |

## 🔧 Troubleshooting

**Can't upload?** Hold BOOT button while uploading

**No networks?** Move ESP32 near WiFi routers

**Web won't load?** Make sure you're connected to ESP32_Control WiFi

## ⚖️ Legal Warning

**ONLY USE ON NETWORKS YOU OWN OR HAVE WRITTEN PERMISSION TO TEST!**

Unauthorized use is illegal. You have been warned.

---

Need more details? See full README.md
