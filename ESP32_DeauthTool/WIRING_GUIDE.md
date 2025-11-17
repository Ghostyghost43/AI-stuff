# ESP32 Wiring & Setup Guide

## Hardware Setup

### ESP32 DevKit V1 / NodeMCU-32S (Most Common)

```
┌─────────────────────────────────┐
│         ESP32 DevKit V1         │
│                                 │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │      WiFi Antenna         │  │
│  │         (Built-in)        │  │
│  │                           │  │
│  └───────────────────────────┘  │
│                                 │
│  [3V3] [GND] [D15] ... [EN] [VIN]│
└─────────────┬───────────────────┘
              │
         USB Cable
              │
    ┌─────────▼─────────┐
    │   Computer or     │
    │   Power Bank      │
    └───────────────────┘
```

### What You Need

#### Minimum Requirements:
- **ESP32 Development Board** (any variant)
- **USB Cable** (Micro-USB or USB-C depending on your board)
- **Computer** (for uploading code) OR **USB Power Bank** (for standalone use)

#### Optional:
- **External Antenna** (for better range)
- **Battery Pack** (for portable use)
- **Case** (for protection)

## Connection Steps

### 1. Basic USB Connection

**For Programming:**
```
ESP32 Board → USB Cable → Computer
```

1. Connect micro-USB cable to ESP32
2. Connect other end to computer USB port
3. ESP32 LED should light up (power indicator)

**For Standalone Operation:**
```
ESP32 Board → USB Cable → Power Bank
```

1. After uploading code, disconnect from computer
2. Connect to USB power bank
3. ESP32 will start automatically

### 2. External Antenna (Optional)

If your ESP32 has an antenna connector (U.FL/IPEX):

```
ESP32 Board → U.FL Connector → External Antenna
```

**Steps:**
1. Locate the small U.FL connector on ESP32 (near WiFi chip)
2. Gently press antenna connector straight down
3. You should feel/hear a small click
4. Do NOT force it - these connectors are fragile!

**Benefit:** Better WiFi range (up to 100m+)

### 3. Power Options

#### Option A: USB Power (Recommended)
- **Voltage:** 5V
- **Connection:** USB port
- **Power Draw:** ~500mA during attacks
- **Use Case:** Most common, safe, easy

#### Option B: Battery (Portable)
- **Voltage:** 3.7V LiPo or 5V USB power bank
- **Connection:**
  - LiPo → JST connector or GND/VIN pins
  - Power bank → USB port
- **Power Draw:** ~200-500mA
- **Use Case:** Portable pentesting

#### Option C: External Power Supply
- **Voltage:** 5V regulated
- **Connection:** VIN and GND pins
- **Current:** Minimum 500mA
- **⚠️ WARNING:** Do NOT exceed 5V on VIN or 3.3V on 3V3 pin!

### 4. Pin Reference

Most ESP32 boards have these important pins:

```
┌──────────────────────────────────┐
│ EN (Reset)    Used to reset ESP32│
│ VIN (5V)      5V power input     │
│ 3V3 (3.3V)    3.3V power output  │
│ GND           Ground (0V)        │
│ GPIO pins     General I/O        │
└──────────────────────────────────┘
```

**For this tool, you DON'T need to connect any GPIO pins!**
Just USB power is enough.

## Board Identification

### How to Identify Your ESP32 Board

Look for text on the board:

- **"ESP32-DevKitC"** → ESP32 DevKit (most common)
- **"NodeMCU-32S"** → NodeMCU ESP32
- **"ESP32-WROOM-32"** → WROOM module (also very common)
- **"ESP32-WROVER"** → WROVER module (has PSRAM)
- **"DOIT ESP32"** → DOIT DevKit

**All of these work with this tool!**

## USB Driver Installation

### Windows

If ESP32 is not detected:

1. Download **CP210x USB to UART Bridge Driver**
   - Link: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
2. Install the driver
3. Restart computer
4. Reconnect ESP32
5. Check Device Manager → Ports (COM & LPT)
6. You should see "Silicon Labs CP210x USB to UART Bridge (COM X)"

### macOS

Usually works out of the box. If not:

```bash
# Install driver
brew install --cask silicon-labs-vcp-driver
```

### Linux

Usually works out of the box. If permission errors:

```bash
# Add your user to dialout group
sudo usermod -a -G dialout $USER

# Logout and login again
```

## Troubleshooting Hardware Issues

### Issue: Computer doesn't detect ESP32

**Check:**
- ✓ USB cable is data cable (not power-only)
- ✓ USB cable is properly connected
- ✓ Try different USB port
- ✓ Try different USB cable
- ✓ Install USB drivers (see above)

### Issue: ESP32 won't enter upload mode

**Solution:**
1. Hold **BOOT** button
2. Press and release **EN** (reset) button
3. Release **BOOT** button
4. Try uploading again

### Issue: ESP32 restarts randomly

**Possible causes:**
- Insufficient power supply
- Faulty USB cable
- Code error (infinite loop, memory overflow)

**Solution:**
- Use good quality USB cable
- Connect to powered USB hub
- Check Serial Monitor for error messages

### Issue: WiFi range is poor

**Solutions:**
- Use external antenna
- Position ESP32 vertically (antenna upright)
- Move away from metal objects
- Reduce obstacles between ESP32 and targets
- Increase TX power in config.h

## Portable Setup Ideas

### 1. Stealth Setup
```
┌──────────────────────┐
│   Small USB Battery  │
│        (2000mAh)     │
└──────────┬───────────┘
           │ Short USB cable
    ┌──────▼──────┐
    │    ESP32    │
    │   (hidden)  │
    └─────────────┘
```
- Small form factor
- Can fit in pocket
- 4-6 hours runtime

### 2. Extended Runtime Setup
```
┌──────────────────────┐
│  Large Power Bank    │
│     (20000mAh)       │
└──────────┬───────────┘
           │
    ┌──────▼──────┐
    │    ESP32    │
    │ + Antenna   │
    └─────────────┘
```
- Extended runtime (40+ hours)
- Better range with antenna
- Good for long-term monitoring

### 3. Professional Setup
```
┌──────────────────────┐
│  Project Box/Case    │
│  ┌────────────────┐  │
│  │ ESP32 + Screen │  │
│  └────────────────┘  │
│  ┌────────────────┐  │
│  │ Battery 18650  │  │
│  └────────────────┘  │
│  [Power Switch]      │
└──────────────────────┘
```
- Professional appearance
- Integrated power switch
- Protected components

## Safety & Best Practices

### ⚠️ Safety Guidelines

1. **Never exceed voltage limits**
   - VIN max: 5.5V
   - GPIO max: 3.3V
   - Over-voltage will DESTROY your ESP32!

2. **Don't short circuit pins**
   - Keep pins from touching each other
   - Don't connect VIN directly to GND

3. **Use proper power supply**
   - Minimum 500mA current capability
   - Regulated 5V for VIN or 3.3V for 3V3

4. **Heat management**
   - ESP32 can get warm during heavy use
   - Ensure ventilation if in enclosure
   - Don't cover WiFi antenna

5. **ESD protection**
   - Touch grounded metal before handling ESP32
   - Store in anti-static bag when not in use

### 🔋 Battery Safety

If using LiPo batteries:

- ✓ Use protected batteries
- ✓ Don't over-discharge (min 3.0V)
- ✓ Don't over-charge (max 4.2V)
- ✓ Don't puncture or damage
- ✓ Store in LiPo safe bag
- ✗ Never leave charging unattended

## Physical Installation Tips

### Antenna Positioning

For best WiFi performance:

```
GOOD:                    BAD:
  │ Vertical              ── Horizontal
  │                       (on metal surface)
  │

  │ Clear space           │ Behind metal
  │                       ║ (shielded)
  │
```

### Placement Guidelines

**DO:**
- Mount vertically when possible
- Keep antenna clear of obstructions
- Position in central location
- Use external antenna for >50m range

**DON'T:**
- Place on metal surfaces
- Cover antenna with hand
- Block antenna with case
- Mount near motors/EMI sources

## Pre-Flight Checklist

Before deploying your ESP32 DeAuth Tool:

- [ ] Code uploaded successfully
- [ ] Serial Monitor shows "Setup Complete"
- [ ] Can connect to ESP32_Control AP
- [ ] Web interface loads at 192.168.4.1
- [ ] Network scan works
- [ ] Attack modes function correctly
- [ ] Adequate power supply for duration needed
- [ ] **Legal authorization obtained**

## Next Steps

Once hardware is set up:

1. See **QUICK_START.md** for software setup
2. See **README.md** for complete documentation
3. Configure settings in **config.h** if needed
4. Upload code and test!

---

**Need help?** Check the troubleshooting section in README.md
