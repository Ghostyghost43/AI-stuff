#!/usr/bin/env python3
"""
Anonymous Scanning Module
Scan through Tor, Proxychains, VPN with rotating IPs
"""

import os
import subprocess
import time
import requests
from pathlib import Path

class AnonymousScanner:
    def __init__(self, work_dir, log_callback=None):
        self.work_dir = Path(work_dir)
        self.log = log_callback or print
        self.tor_running = False
        self.current_ip = None

    def check_tor(self):
        """Check if Tor is installed and running"""
        if not subprocess.run(['which', 'tor'], capture_output=True).returncode == 0:
            self.log("Tor is not installed", "WARNING")
            return False

        # Check if Tor service is running
        result = subprocess.run(['systemctl', 'is-active', 'tor'],
                              capture_output=True, text=True)
        return result.stdout.strip() == 'active'

    def start_tor(self):
        """Start Tor service"""
        self.log("Starting Tor service...", "INFO")
        os.system("systemctl start tor")
        time.sleep(5)

        if self.check_tor():
            self.log("Tor started successfully", "SUCCESS")
            self.tor_running = True
            self.get_current_ip()
            return True
        else:
            self.log("Failed to start Tor", "ERROR")
            return False

    def stop_tor(self):
        """Stop Tor service"""
        self.log("Stopping Tor service...", "INFO")
        os.system("systemctl stop tor")
        self.tor_running = False

    def get_current_ip(self):
        """Check current external IP"""
        try:
            # Check through Tor
            if self.tor_running:
                proxies = {
                    'http': 'socks5h://127.0.0.1:9050',
                    'https': 'socks5h://127.0.0.1:9050'
                }
                response = requests.get('https://api.ipify.org', proxies=proxies, timeout=10)
            else:
                response = requests.get('https://api.ipify.org', timeout=10)

            self.current_ip = response.text
            self.log(f"Current IP: {self.current_ip}", "INFO")
            return self.current_ip
        except Exception as e:
            self.log(f"Failed to get IP: {e}", "ERROR")
            return None

    def renew_tor_identity(self):
        """Request new Tor identity (new IP)"""
        self.log("Requesting new Tor identity...", "INFO")

        try:
            # Send NEWNYM signal to Tor control port
            os.system("systemctl reload tor")
            time.sleep(10)

            new_ip = self.get_current_ip()
            if new_ip != self.current_ip:
                self.log(f"New IP obtained: {new_ip}", "SUCCESS")
                return True
            else:
                self.log("IP did not change", "WARNING")
                return False
        except Exception as e:
            self.log(f"Failed to renew identity: {e}", "ERROR")
            return False

    def setup_proxychains(self):
        """Configure proxychains for Tor"""
        config_file = "/etc/proxychains4.conf"

        config = """# Proxychains Configuration
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 9050
"""

        try:
            with open(config_file, 'w') as f:
                f.write(config)
            self.log("Proxychains configured for Tor", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Failed to configure proxychains: {e}", "ERROR")
            return False

    def tor_nmap(self, target, ports=None, scan_type='sV'):
        """Run nmap through Tor using proxychains"""
        if not self.check_tor():
            self.start_tor()

        self.setup_proxychains()

        output_file = self.work_dir / f"tor_scan_{target.replace('/', '_')}_{int(time.time())}.xml"

        # Build nmap command
        if ports:
            port_arg = f"-p {ports}"
        else:
            port_arg = "-p 80,443,22,21,3389"

        cmd = f"proxychains4 -q nmap -{scan_type} {port_arg} -Pn -T2 -oX {output_file} {target}"

        self.log(f"Scanning {target} through Tor...", "INFO")
        self.log("This will be slower due to Tor routing", "WARNING")

        os.system(cmd)

        self.log(f"Scan complete: {output_file}", "SUCCESS")
        return output_file

    def tor_curl(self, url):
        """Fetch URL through Tor"""
        if not self.check_tor():
            self.start_tor()

        cmd = f"curl --socks5-hostname 127.0.0.1:9050 {url}"
        return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    def tor_wget(self, url, output_file=None):
        """Download file through Tor"""
        if not self.check_tor():
            self.start_tor()

        output = output_file or self.work_dir / f"download_{int(time.time())}"

        cmd = f"proxychains4 -q wget -e use_proxy=yes -e http_proxy=127.0.0.1:9050 {url} -O {output}"
        os.system(cmd)

        return output

    def tor_nikto(self, target):
        """Run Nikto through Tor"""
        if not self.check_tor():
            self.start_tor()

        output_file = self.work_dir / f"tor_nikto_{target.replace('/', '_')}_{int(time.time())}.txt"

        cmd = f"proxychains4 -q nikto -h {target} -useproxy http://127.0.0.1:9050 -o {output_file}"
        os.system(cmd)

        return output_file

    def tor_sqlmap(self, url):
        """Run SQLMap through Tor"""
        if not self.check_tor():
            self.start_tor()

        cmd = f"proxychains4 -q sqlmap -u '{url}' --tor --tor-type=SOCKS5 --check-tor --batch"
        os.system(cmd)

    def rotating_ip_scan(self, target, num_rotations=5):
        """Scan target with rotating IPs through Tor"""
        if not self.check_tor():
            self.start_tor()

        results = []

        for i in range(num_rotations):
            self.log(f"Rotation {i+1}/{num_rotations}", "INFO")

            # Get current IP
            current_ip = self.get_current_ip()

            # Run scan
            output = self.tor_nmap(target)
            results.append({
                'ip': current_ip,
                'scan_file': output,
                'rotation': i+1
            })

            # Renew identity if not last rotation
            if i < num_rotations - 1:
                self.renew_tor_identity()
                time.sleep(10)

        self.log(f"Completed {num_rotations} rotations", "SUCCESS")
        return results

    def multi_proxy_scan(self, target, proxy_list_file):
        """Scan through multiple proxies from list"""
        if not os.path.exists(proxy_list_file):
            self.log(f"Proxy list not found: {proxy_list_file}", "ERROR")
            return None

        with open(proxy_list_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]

        results = []

        for idx, proxy in enumerate(proxies, 1):
            self.log(f"Scanning through proxy {idx}/{len(proxies)}: {proxy}", "INFO")

            # Create temporary proxychains config
            temp_config = self.work_dir / f"proxychains_temp_{idx}.conf"

            with open(temp_config, 'w') as f:
                f.write("strict_chain\n")
                f.write("proxy_dns\n")
                f.write("tcp_read_time_out 15000\n")
                f.write("tcp_connect_time_out 8000\n\n")
                f.write("[ProxyList]\n")
                f.write(f"{proxy}\n")

            # Run scan
            output = self.work_dir / f"proxy_scan_{idx}_{int(time.time())}.xml"
            cmd = f"proxychains4 -f {temp_config} nmap -sV -Pn -T2 -oX {output} {target}"

            os.system(cmd)
            results.append(output)

            # Cleanup
            os.remove(temp_config)

        return results

    def vpn_scan(self, target, vpn_config):
        """Scan through VPN connection"""
        self.log(f"Connecting to VPN: {vpn_config}", "INFO")

        # Connect to VPN
        vpn_process = subprocess.Popen(['openvpn', '--config', vpn_config],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        # Wait for connection
        time.sleep(15)

        # Get new IP
        self.get_current_ip()

        # Run scan
        output_file = self.work_dir / f"vpn_scan_{target.replace('/', '_')}_{int(time.time())}.xml"
        os.system(f"nmap -sV -oX {output_file} {target}")

        # Disconnect VPN
        vpn_process.terminate()
        vpn_process.wait()

        self.log("VPN disconnected", "INFO")
        return output_file

    def install_anonymity_tools(self):
        """Install Tor and related tools"""
        self.log("Installing anonymity tools...", "INFO")

        commands = [
            "apt-get update",
            "apt-get install -y tor",
            "apt-get install -y proxychains4",
            "apt-get install -y openvpn",
            "apt-get install -y torsocks",
            "systemctl enable tor",
            "systemctl start tor"
        ]

        for cmd in commands:
            self.log(f"Running: {cmd}", "INFO")
            os.system(cmd)

        self.log("Anonymity tools installed", "SUCCESS")

    def test_anonymity(self):
        """Test if anonymous browsing is working"""
        self.log("Testing anonymity...", "INFO")

        # Get real IP
        try:
            real_ip = requests.get('https://api.ipify.org', timeout=10).text
            self.log(f"Real IP: {real_ip}", "INFO")
        except:
            self.log("Could not get real IP", "ERROR")
            return False

        # Get Tor IP
        if not self.check_tor():
            self.start_tor()

        try:
            proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            tor_ip = requests.get('https://api.ipify.org', proxies=proxies, timeout=30).text
            self.log(f"Tor IP: {tor_ip}", "INFO")

            if real_ip != tor_ip:
                self.log("Anonymity is working!", "SUCCESS")
                return True
            else:
                self.log("Anonymity failed - same IP!", "ERROR")
                return False
        except Exception as e:
            self.log(f"Tor test failed: {e}", "ERROR")
            return False

    def stealth_scan(self, target):
        """Ultra-stealth scan through Tor with delays"""
        if not self.check_tor():
            self.start_tor()

        self.setup_proxychains()

        output_file = self.work_dir / f"stealth_scan_{target.replace('/', '_')}_{int(time.time())}.xml"

        # Very slow and stealthy
        cmd = f"proxychains4 -q nmap -sS -T1 -f --randomize-hosts --data-length 32 -Pn -oX {output_file} {target}"

        self.log("Running stealth scan (this will be VERY slow)...", "WARNING")
        os.system(cmd)

        return output_file

    def tor_metasploit(self, target, module):
        """Run Metasploit module through Tor"""
        if not self.check_tor():
            self.start_tor()

        rc_file = self.work_dir / f"tor_msf_{int(time.time())}.rc"

        with open(rc_file, 'w') as f:
            f.write("# Metasploit through Tor\n")
            f.write("setg Proxies socks5:127.0.0.1:9050\n")
            f.write(f"use {module}\n")
            f.write(f"set RHOSTS {target}\n")
            f.write("check\n")
            f.write("exploit\n")

        os.system(f"msfconsole -r {rc_file}")

    def configure_tor_bridges(self, bridge_list):
        """Configure Tor to use bridges (for censored networks)"""
        tor_config = "/etc/tor/torrc"

        config_append = "\n# Bridges\nUseBridges 1\n"
        for bridge in bridge_list:
            config_append += f"Bridge {bridge}\n"

        try:
            with open(tor_config, 'a') as f:
                f.write(config_append)

            os.system("systemctl restart tor")
            self.log("Tor bridges configured", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Failed to configure bridges: {e}", "ERROR")
            return False

    def onion_scan(self, onion_address):
        """Scan .onion hidden service"""
        if not self.check_tor():
            self.start_tor()

        self.log(f"Scanning onion service: {onion_address}", "INFO")

        # Use torsocks for onion services
        output_file = self.work_dir / f"onion_scan_{onion_address.replace('.onion', '')}_{int(time.time())}.xml"

        cmd = f"torsocks nmap -sV -Pn -p- -T2 -oX {output_file} {onion_address}"
        os.system(cmd)

        return output_file
