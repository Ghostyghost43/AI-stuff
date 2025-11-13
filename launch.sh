#!/bin/bash

# Franken-Pentest v2.0 ULTIMATE Launcher
# Simple launcher script

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Franken-Pentest requires root privileges${NC}"
    echo -e "${CYAN}[*] Restarting with sudo...${NC}"
    exec sudo bash "$0" "$@"
fi

# Change to script directory
cd "$(dirname "$0")"

# Check if modules exist
if [ -d "modules" ]; then
    echo -e "${GREEN}[+] Launching Franken-Pentest v2.0 ULTIMATE...${NC}\n"
    python3 franken_ultimate.py "$@"
else
    echo -e "${CYAN}[*] Launching Franken-Pentest v1.0 (basic)...${NC}\n"
    python3 franken_pentest.py "$@"
fi
