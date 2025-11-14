"""
Network Scanner Module
Handles network reconnaissance, port scanning, and service detection
"""

import subprocess
import re
import json
from typing import Dict, List, Callable


class NetworkScanner:
    """Network scanning functionality using nmap and custom tools"""

    def __init__(self):
        self.scan_history = []

    def scan(self, target: str, scan_type: str, callback: Callable = None,
             progress_callback: Callable = None) -> Dict:
        """
        Perform network scan

        Args:
            target: Target IP/CIDR
            scan_type: Type of scan to perform
            callback: Callback for status updates
            progress_callback: Callback for progress updates

        Returns:
            Dictionary containing scan results
        """
        results = {
            'target': target,
            'scan_type': scan_type,
            'hosts': [],
            'status': 'running'
        }

        if callback:
            callback(f"[SCAN] Starting {scan_type} on {target}")

        # Map scan types to nmap commands
        scan_commands = {
            "Quick Scan (-T4 -F)": f"nmap -T4 -F {target}",
            "Full Port Scan (-p-)": f"nmap -p- {target}",
            "Service Version Detection (-sV)": f"nmap -sV {target}",
            "OS Detection (-O)": f"nmap -O {target}",
            "Aggressive Scan (-A)": f"nmap -A {target}",
            "Stealth Scan (-sS)": f"nmap -sS {target}",
            "UDP Scan (-sU)": f"nmap -sU --top-ports 100 {target}"
        }

        # Add output format for parsing
        nmap_cmd = scan_commands.get(scan_type, f"nmap {target}") + " -oX -"

        try:
            if callback:
                callback(f"[CMD] {nmap_cmd}")

            # Execute nmap
            process = subprocess.Popen(
                nmap_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Read output
            stdout, stderr = process.communicate()

            if progress_callback:
                progress_callback(50)

            if process.returncode == 0:
                # Parse XML output
                results['hosts'] = self._parse_nmap_xml(stdout)
                results['status'] = 'completed'
                results['raw_output'] = stdout

                if callback:
                    callback(f"[SCAN] Found {len(results['hosts'])} hosts")
                    for host in results['hosts'][:5]:  # Show first 5
                        callback(f"  - {host['ip']}: {len(host.get('ports', []))} open ports")

                if progress_callback:
                    progress_callback(100)
            else:
                results['status'] = 'failed'
                results['error'] = stderr
                if callback:
                    callback(f"[ERROR] Scan failed: {stderr}")

        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            if callback:
                callback(f"[ERROR] {str(e)}")

        self.scan_history.append(results)
        return results

    def _parse_nmap_xml(self, xml_output: str) -> List[Dict]:
        """Parse nmap XML output"""
        hosts = []

        # Simple XML parsing (in production, use xml.etree.ElementTree)
        # This is a simplified version
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_output)

            for host_elem in root.findall('host'):
                host_data = {}

                # Get IP address
                address_elem = host_elem.find('address')
                if address_elem is not None:
                    host_data['ip'] = address_elem.get('addr')
                    host_data['mac'] = None

                    # Get MAC if available
                    for addr in host_elem.findall('address'):
                        if addr.get('addrtype') == 'mac':
                            host_data['mac'] = addr.get('addr')
                            host_data['vendor'] = addr.get('vendor', 'Unknown')

                # Get hostname
                hostnames_elem = host_elem.find('hostnames')
                if hostnames_elem is not None:
                    hostname_elem = hostnames_elem.find('hostname')
                    if hostname_elem is not None:
                        host_data['hostname'] = hostname_elem.get('name')

                # Get open ports
                ports_elem = host_elem.find('ports')
                if ports_elem is not None:
                    host_data['ports'] = []
                    for port_elem in ports_elem.findall('port'):
                        state_elem = port_elem.find('state')
                        if state_elem is not None and state_elem.get('state') == 'open':
                            port_data = {
                                'port': port_elem.get('portid'),
                                'protocol': port_elem.get('protocol'),
                                'state': 'open'
                            }

                            # Get service info
                            service_elem = port_elem.find('service')
                            if service_elem is not None:
                                port_data['service'] = service_elem.get('name')
                                port_data['version'] = service_elem.get('version', '')
                                port_data['product'] = service_elem.get('product', '')

                            host_data['ports'].append(port_data)

                # Get OS detection
                os_elem = host_elem.find('os')
                if os_elem is not None:
                    osmatch_elem = os_elem.find('osmatch')
                    if osmatch_elem is not None:
                        host_data['os'] = osmatch_elem.get('name')
                        host_data['os_accuracy'] = osmatch_elem.get('accuracy')

                hosts.append(host_data)

        except Exception as e:
            print(f"XML parsing error: {e}")
            # Fallback to regex parsing
            hosts = self._parse_nmap_text(xml_output)

        return hosts

    def _parse_nmap_text(self, text_output: str) -> List[Dict]:
        """Fallback text parsing"""
        hosts = []
        # Simple regex-based parsing
        ip_pattern = re.compile(r'Nmap scan report for ([0-9.]+)')
        matches = ip_pattern.findall(text_output)

        for ip in matches:
            hosts.append({'ip': ip, 'ports': []})

        return hosts

    def quick_ping_sweep(self, network: str, callback: Callable = None) -> Dict:
        """Quick ping sweep to find live hosts"""
        if callback:
            callback(f"[PING] Sweeping {network} for live hosts")

        cmd = f"nmap -sn {network} -oX -"

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            hosts = self._parse_nmap_xml(result.stdout)
            if callback:
                callback(f"[PING] Found {len(hosts)} live hosts")

            return {
                'network': network,
                'live_hosts': hosts,
                'count': len(hosts)
            }

        except Exception as e:
            if callback:
                callback(f"[ERROR] Ping sweep failed: {e}")
            return {'network': network, 'live_hosts': [], 'error': str(e)}

    def vulnerability_scan(self, target: str, callback: Callable = None) -> Dict:
        """Run vulnerability scanning scripts"""
        if callback:
            callback(f"[VULN] Running vulnerability scan on {target}")

        cmd = f"nmap --script vuln {target} -oX -"

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600
            )

            if callback:
                callback(f"[VULN] Scan complete")

            return {
                'target': target,
                'vulnerabilities': result.stdout,
                'status': 'completed'
            }

        except Exception as e:
            if callback:
                callback(f"[ERROR] Vulnerability scan failed: {e}")
            return {'target': target, 'error': str(e)}
