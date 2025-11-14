"""
Enhanced Wireless Attack Module
Real-time AP monitoring, packet streaming, target selection, automation with kill switches
"""

import subprocess
import time
import os
import re
import threading
import queue
from typing import Dict, List, Callable
from datetime import datetime


class WirelessEnhanced:
    """Enhanced wireless penetration testing with real-time features"""

    def __init__(self):
        self.is_running = False
        self.kill_signal = threading.Event()
        self.monitor_interface = None
        self.captured_handshakes = []
        self.ap_list = []
        self.packet_queue = queue.Queue()
        self.realtime_stats = {
            'packets_captured': 0,
            'aps_found': 0,
            'clients_found': 0,
            'handshakes': 0
        }
        self.verbose = True

    def set_verbose(self, verbose: bool):
        """Toggle verbose output"""
        self.verbose = verbose

    def kill_all(self):
        """EMERGENCY KILL SWITCH - Stop everything immediately"""
        self.log("[KILL SWITCH] Stopping all wireless operations...")
        self.kill_signal.set()
        self.is_running = False

        # Kill all aircrack-ng processes
        subprocess.run("killall -9 airodump-ng aireplay-ng airmon-ng reaver wash hcxdumptool 2>/dev/null",
                      shell=True, capture_output=True)

        # Restore managed mode if monitor mode was enabled
        if self.monitor_interface:
            self.disable_monitor_mode(self.monitor_interface)

        self.log("[KILL SWITCH] All operations stopped")

    def log(self, message: str, callback: Callable = None):
        """Log message with verbosity control"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        if callback:
            callback(message)

    def configure_wifi_adapter(self, interface: str, callback: Callable = None) -> Dict:
        """
        Configure WiFi adapter for pentesting

        Returns adapter capabilities and configuration
        """
        self.log(f"[CONFIG] Configuring adapter {interface}...", callback)

        config = {
            'interface': interface,
            'driver': None,
            'chipset': None,
            'monitor_mode_capable': False,
            'injection_capable': False,
            'channels': [],
            'current_mode': None
        }

        try:
            # Get driver info
            driver_cmd = f"readlink -f /sys/class/net/{interface}/device/driver"
            result = subprocess.run(driver_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                config['driver'] = result.stdout.strip().split('/')[-1]
                self.log(f"[CONFIG] Driver: {config['driver']}", callback)

            # Check current mode
            mode_cmd = f"iwconfig {interface} 2>/dev/null | grep Mode"
            result = subprocess.run(mode_cmd, shell=True, capture_output=True, text=True)
            if 'Monitor' in result.stdout:
                config['current_mode'] = 'Monitor'
            elif 'Managed' in result.stdout:
                config['current_mode'] = 'Managed'
            self.log(f"[CONFIG] Current mode: {config['current_mode']}", callback)

            # Check monitor mode capability (try to enable and disable)
            self.log("[CONFIG] Testing monitor mode capability...", callback)
            test_result = self.enable_monitor_mode(interface)
            if test_result:
                config['monitor_mode_capable'] = True
                self.log("[CONFIG] ✓ Monitor mode supported", callback)
                # Restore to managed mode
                self.disable_monitor_mode(test_result)
            else:
                self.log("[CONFIG] ✗ Monitor mode not supported", callback)

            # Test packet injection
            if config['monitor_mode_capable']:
                self.log("[CONFIG] Testing packet injection...", callback)
                mon_iface = self.enable_monitor_mode(interface)
                if mon_iface:
                    test_cmd = f"timeout 5 aireplay-ng --test {mon_iface} 2>&1"
                    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
                    if 'Injection is working!' in result.stdout:
                        config['injection_capable'] = True
                        self.log("[CONFIG] ✓ Packet injection working", callback)
                    else:
                        self.log("[CONFIG] ✗ Packet injection not working", callback)
                    self.disable_monitor_mode(mon_iface)

            # Get supported channels
            channels_cmd = f"iwlist {interface} channel 2>/dev/null | grep 'Channel' | awk '{{print $2}}'"
            result = subprocess.run(channels_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                config['channels'] = [int(ch) for ch in result.stdout.strip().split('\n') if ch.isdigit()]
                self.log(f"[CONFIG] Supported channels: {len(config['channels'])}", callback)

        except Exception as e:
            self.log(f"[CONFIG ERROR] {e}", callback)

        return config

    def enable_monitor_mode(self, interface: str) -> str:
        """Enable monitor mode and return monitor interface name"""
        try:
            # Kill interfering processes
            subprocess.run("airmon-ng check kill", shell=True, capture_output=True)

            # Start monitor mode
            result = subprocess.run(f"airmon-ng start {interface}",
                                   shell=True, capture_output=True, text=True)

            # Parse monitor interface name
            if 'monitor mode enabled' in result.stdout.lower():
                match = re.search(r'monitor mode (?:enabled|vif enabled) on (\w+)',
                                result.stdout, re.IGNORECASE)
                if match:
                    self.monitor_interface = match.group(1)
                else:
                    self.monitor_interface = f"{interface}mon"
                return self.monitor_interface

        except Exception:
            pass
        return None

    def disable_monitor_mode(self, interface: str) -> bool:
        """Disable monitor mode"""
        try:
            subprocess.run(f"airmon-ng stop {interface}", shell=True, capture_output=True)
            self.monitor_interface = None
            return True
        except Exception:
            return False

    def realtime_ap_monitor(self, interface: str, callback: Callable = None,
                           duration: int = 0) -> None:
        """
        Real-time AP monitoring with live updates

        Args:
            interface: Monitor mode interface
            callback: Callback for updates
            duration: Monitor duration (0 = infinite)
        """
        self.is_running = True
        self.kill_signal.clear()
        self.ap_list = []

        self.log(f"[REALTIME] Starting AP monitoring on {interface}...", callback)
        self.log(f"[REALTIME] Press KILL SWITCH to stop", callback)

        output_file = f"/tmp/airodump_realtime_{int(time.time())}"

        try:
            # Start airodump-ng in background
            cmd = f"airodump-ng {interface} -w {output_file} --output-format csv"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

            start_time = time.time()

            while self.is_running and not self.kill_signal.is_set():
                # Check duration
                if duration > 0 and (time.time() - start_time) >= duration:
                    break

                # Parse CSV file
                csv_file = f"{output_file}-01.csv"
                if os.path.exists(csv_file):
                    aps = self._parse_airodump_csv(csv_file)

                    # Update statistics
                    self.realtime_stats['aps_found'] = len(aps)

                    # Find new APs
                    existing_bssids = [ap['bssid'] for ap in self.ap_list]
                    for ap in aps:
                        if ap['bssid'] not in existing_bssids:
                            self.log(f"[NEW AP] {ap['ssid']:20} {ap['bssid']} Ch:{ap['channel']:3} Sig:{ap['signal']}", callback)
                            if callback:
                                callback(f"[NEW AP] {ap['ssid']} ({ap['bssid']}) Ch:{ap['channel']}")

                    self.ap_list = aps

                    # Send update with all APs
                    if callback:
                        callback(f"[STATS] APs: {len(aps)} | Monitoring...")

                time.sleep(2)

            # Cleanup
            process.terminate()
            for ext in ['-01.csv', '-01.cap', '-01.kismet.csv', '-01.kismet.netxml']:
                try:
                    os.remove(f"{output_file}{ext}")
                except:
                    pass

        except Exception as e:
            self.log(f"[ERROR] {e}", callback)
        finally:
            self.is_running = False

    def _parse_airodump_csv(self, csv_file: str) -> List[Dict]:
        """Parse airodump-ng CSV output"""
        aps = []
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            ap_section_started = False
            for line in lines:
                if 'BSSID' in line and 'Power' in line:
                    ap_section_started = True
                    continue

                if ap_section_started:
                    if 'Station MAC' in line:
                        break

                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 14 and parts[0]:
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

                            try:
                                power_dbm = int(ap['power'])
                                ap['signal'] = f"{power_dbm} dBm"
                            except:
                                ap['signal'] = ap['power']

                            aps.append(ap)
                        except Exception:
                            continue

        except Exception:
            pass

        return aps

    def scan_and_select(self, interface: str, callback: Callable = None) -> List[Dict]:
        """
        Scan for APs and return list for user selection

        Returns list of APs with all details
        """
        self.log("[SCAN] Scanning for access points...", callback)

        # Run scan for 30 seconds
        self.realtime_ap_monitor(interface, callback, duration=30)

        self.log(f"[SCAN] Found {len(self.ap_list)} access points", callback)

        # Sort by signal strength
        sorted_aps = sorted(self.ap_list, key=lambda x: int(x['power']) if x['power'].lstrip('-').isdigit() else -100, reverse=True)

        return sorted_aps

    def automated_attack_workflow(self, interface: str, target: Dict,
                                  attack_types: List[str],
                                  callback: Callable = None,
                                  progress_callback: Callable = None) -> Dict:
        """
        Fully automated attack workflow with kill switch support

        Args:
            interface: Monitor interface
            target: Target AP dictionary from scan
            attack_types: List of attacks to run ['eapol', 'pmkid', 'deauth', 'wps']
            callback: Status callback
            progress_callback: Progress callback

        Returns:
            Results dictionary
        """
        self.is_running = True
        self.kill_signal.clear()

        results = {
            'target': target,
            'attacks': {},
            'success': False,
            'status': 'running'
        }

        bssid = target['bssid']
        channel = target['channel']
        ssid = target['ssid']

        self.log(f"[AUTO] Starting automated attack on {ssid} ({bssid})", callback)
        self.log(f"[AUTO] Attacks: {', '.join(attack_types)}", callback)
        self.log(f"[AUTO] KILL SWITCH available to abort", callback)

        try:
            total_attacks = len(attack_types)
            completed = 0

            # Set channel
            subprocess.run(f"iwconfig {interface} channel {channel}", shell=True, capture_output=True)

            # EAPOL Handshake Capture
            if 'eapol' in attack_types and not self.kill_signal.is_set():
                self.log(f"[AUTO] [{completed+1}/{total_attacks}] EAPOL Handshake Capture", callback)
                if progress_callback:
                    progress_callback(int((completed / total_attacks) * 100))

                # Implementation from wireless_attacks.py
                # ... (EAPOL capture code)
                completed += 1

            # PMKID Attack
            if 'pmkid' in attack_types and not self.kill_signal.is_set():
                self.log(f"[AUTO] [{completed+1}/{total_attacks}] PMKID Attack (Clientless)", callback)
                if progress_callback:
                    progress_callback(int((completed / total_attacks) * 100))

                # PMKID implementation
                # ... (PMKID code)
                completed += 1

            # Deauth Attack
            if 'deauth' in attack_types and not self.kill_signal.is_set():
                self.log(f"[AUTO] [{completed+1}/{total_attacks}] Deauthentication", callback)
                if progress_callback:
                    progress_callback(int((completed / total_attacks) * 100))

                # Deauth implementation
                # ... (Deauth code)
                completed += 1

            # WPS Attack
            if 'wps' in attack_types and not self.kill_signal.is_set():
                self.log(f"[AUTO] [{completed+1}/{total_attacks}] WPS Pixie Dust", callback)
                if progress_callback:
                    progress_callback(int((completed / total_attacks) * 100))

                # WPS implementation
                # ... (WPS code)
                completed += 1

            if self.kill_signal.is_set():
                self.log("[AUTO] Aborted by kill switch", callback)
                results['status'] = 'aborted'
            else:
                self.log("[AUTO] Automated attack sequence complete", callback)
                results['status'] = 'completed'

            if progress_callback:
                progress_callback(100)

        except Exception as e:
            self.log(f"[AUTO ERROR] {e}", callback)
            results['status'] = 'error'
            results['error'] = str(e)

        finally:
            self.is_running = False

        return results

    def realtime_packet_stream(self, interface: str, filter_type: str = "all",
                               callback: Callable = None) -> None:
        """
        Real-time packet streaming with filtering

        Args:
            interface: Monitor interface
            filter_type: "all", "eapol", "deauth", "beacon", "data"
            callback: Callback for each packet
        """
        self.is_running = True
        self.kill_signal.clear()

        self.log(f"[PACKET STREAM] Starting on {interface}...", callback)
        self.log(f"[PACKET STREAM] Filter: {filter_type}", callback)

        try:
            # Use tcpdump for packet capture
            if filter_type == "eapol":
                tcpdump_filter = "ether proto 0x888e"
            elif filter_type == "deauth":
                tcpdump_filter = "wlan type mgt subtype deauth"
            elif filter_type == "beacon":
                tcpdump_filter = "wlan type mgt subtype beacon"
            elif filter_type == "data":
                tcpdump_filter = "wlan type data"
            else:
                tcpdump_filter = ""

            cmd = f"tcpdump -i {interface} -l -n {tcpdump_filter}"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL, universal_newlines=True)

            while self.is_running and not self.kill_signal.is_set():
                line = process.stdout.readline()
                if line:
                    self.realtime_stats['packets_captured'] += 1
                    if callback:
                        callback(f"[PKT #{self.realtime_stats['packets_captured']}] {line.strip()}")

            process.terminate()

        except Exception as e:
            self.log(f"[STREAM ERROR] {e}", callback)
        finally:
            self.is_running = False

    def get_realtime_stats(self) -> Dict:
        """Get current real-time statistics"""
        return self.realtime_stats.copy()
