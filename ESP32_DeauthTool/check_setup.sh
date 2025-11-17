#!/bin/bash

###############################################################################
# ESP32 DeAuth Tool - Setup Checker
#
# This script checks if you have everything needed to compile and upload
# the ESP32 DeAuth Tool
###############################################################################

echo "======================================"
echo "ESP32 DeAuth Tool - Setup Checker"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
passed=0
failed=0

# Function to check command
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $2 found: $(command -v $1)"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $2 not found"
        ((failed++))
        return 1
    fi
}

# Function to check Python package
check_python_package() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python package '$1' installed"
        ((passed++))
        return 0
    else
        echo -e "${YELLOW}○${NC} Python package '$1' not found (optional for API control)"
        return 1
    fi
}

echo "Checking system requirements..."
echo ""

# Check for Python (optional)
if check_command "python3" "Python 3"; then
    python_version=$(python3 --version)
    echo "  Version: $python_version"
    echo ""

    # Check for requests library (optional, for API scripts)
    echo "Checking Python packages (optional)..."
    check_python_package "requests"
    echo ""
fi

# Check for Arduino CLI (if available)
echo "Checking for Arduino CLI (optional)..."
if check_command "arduino-cli" "Arduino CLI"; then
    arduino_version=$(arduino-cli version)
    echo "  Version: $arduino_version"

    # Check if ESP32 platform is installed
    echo ""
    echo "Checking ESP32 platform installation..."
    if arduino-cli core list | grep -q "esp32"; then
        echo -e "${GREEN}✓${NC} ESP32 platform is installed"
        ((passed++))
        esp32_version=$(arduino-cli core list | grep esp32 | awk '{print $2}')
        echo "  Version: $esp32_version"
    else
        echo -e "${RED}✗${NC} ESP32 platform not installed"
        echo ""
        echo "To install ESP32 platform:"
        echo "  arduino-cli core update-index"
        echo "  arduino-cli core install esp32:esp32"
        ((failed++))
    fi
else
    echo -e "${YELLOW}○${NC} Arduino CLI not found (you can use Arduino IDE instead)"
    echo ""
    echo "Install Arduino CLI (optional):"
    echo "  curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh"
fi

echo ""
echo "Checking for PlatformIO (optional)..."
check_command "pio" "PlatformIO CLI"

echo ""
echo "======================================"
echo "Summary"
echo "======================================"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ Your system is ready!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Open ESP32_DeauthTool.ino in Arduino IDE or PlatformIO"
    echo "2. Select your ESP32 board"
    echo "3. Select the correct COM port"
    echo "4. Click Upload"
    echo ""
else
    echo -e "${YELLOW}! Some dependencies are missing${NC}"
    echo ""
    echo "You need either:"
    echo "  1. Arduino IDE with ESP32 support, OR"
    echo "  2. PlatformIO IDE"
    echo ""
    echo "Installation guides:"
    echo ""
    echo "Arduino IDE:"
    echo "  1. Download from: https://www.arduino.cc/en/software"
    echo "  2. File → Preferences"
    echo "  3. Add Board Manager URL:"
    echo "     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json"
    echo "  4. Tools → Board → Boards Manager"
    echo "  5. Search 'ESP32' and install 'ESP32 by Espressif Systems'"
    echo ""
    echo "PlatformIO:"
    echo "  1. Install VS Code"
    echo "  2. Install PlatformIO IDE extension"
    echo "  3. Open this folder in PlatformIO"
    echo "  4. Click Upload"
    echo ""
fi

echo "======================================"
echo ""
echo "For detailed instructions, see README.md"
echo ""
