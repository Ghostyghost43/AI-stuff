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

    def check_deps(self):
        """Check dependencies"""
        self.log("Checking dependencies...", "INFO")

        required = ['airmon-ng', 'airodump-ng', 'aireplay-ng']
        optional = ['hashcat', 'reaver', 'wash', 'hostapd', 'dnsmasq']

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
            print(f"\n{C.BL}Install: sudo apt install aircrack-ng{C.R}\n")
            return False

        if missing_opt:
            self.log(f"Missing optional: {', '.join(missing_opt)}", "WARNING")
            print(f"{C.GO}Some features unavailable. Run: sudo bash install_wifi_autopwn.sh{C.R}\n")

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
                print(f"  [1] PMKID")
                print(f"  [2] Handshake")
                print(f"  [3] WPS")
                print(f"  [4] Evil Twin")
                print(f"  [5] Skip\n")

                attack = input(f"{C.NE}Choose attack: {C.R}").strip()

                if attack == '1':
                    ghost_print("PMKID attack selected", C.TX, "🎯")
                elif attack == '2':
                    ghost_print("Handshake attack selected", C.TX, "🤝")
                elif attack == '3':
                    ghost_print("WPS attack selected", C.TX, "🔓")
                elif attack == '4':
                    ghost_print("Evil Twin selected", C.TX, "👤")
                else:
                    continue

                # Placeholder - attacks will be implemented
                print(f"\n{C.GO}Attack functionality will be implemented next...{C.R}\n")

                another = input(f"{C.NE}Attack another target? (y/n): {C.R}").strip()
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
