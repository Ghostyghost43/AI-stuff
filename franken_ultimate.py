#!/usr/bin/env python3
"""
Franken-Pentest Framework v2.0 ULTIMATE
Enhanced with advanced automation modules

For authorized security testing only.
"""

import os
import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

# Import the original framework
from franken_pentest import FrankenPentest, Colors, BANNER

# Import new advanced modules
try:
    from modules.exploit_automation import ExploitAutomation
    from modules.anonymous_scanning import AnonymousScanner
    from modules.post_exploitation import PostExploitation
    from modules.better_bettercap import BettercapAdvanced
    from modules.physical_attacks import PhysicalAttacks
    from modules.hashcat_automation import HashcatAutomation
    from modules.msf_database import MSFDatabase
    from modules.framework_updater import FrameworkUpdater
    MODULES_LOADED = True
except ImportError as e:
    print(f"{Colors.YELLOW}[WARNING] Advanced modules not fully loaded: {e}{Colors.RESET}")
    MODULES_LOADED = False


class FrankenUltimate(FrankenPentest):
    """Enhanced Franken-Pentest with advanced modules"""

    def __init__(self):
        super().__init__()

        # Initialize advanced modules if available
        if MODULES_LOADED:
            self.exploit_auto = ExploitAutomation(self.work_dir, self.log)
            self.anon_scanner = AnonymousScanner(self.work_dir, self.log)
            self.post_exploit = PostExploitation(self.work_dir, self.log)
            self.bettercap_adv = BettercapAdvanced(self.work_dir, self.log)
            self.physical = PhysicalAttacks(self.work_dir, self.log)
            self.hashcat = HashcatAutomation(self.work_dir, self.log)
            self.msf_db = MSFDatabase(self.log)
            self.updater = FrameworkUpdater(self.work_dir, self.log)

    def show_menu(self):
        """Enhanced main menu with advanced options"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}═══ FRANKEN-PENTEST v2.0 ULTIMATE ═══{Colors.RESET}\n")

        modules = {
            "1": "Metasploit Integration",
            "2": "Social Engineering Toolkit (SET)",
            "3": "Bettercap Network Attacks",
            "4": "Wireless Attacks (mdk4 + Aircrack-ng)",
            "5": "Network Sniffing (Wireshark/tshark)",
            "6": "Automated Attack Chains",
            "7": "🔥 Advanced Exploit Automation (NEW)",
            "8": "🕵️  Anonymous Scanning (Tor/Proxychains) (NEW)",
            "9": "💀 Post-Exploitation Suite (NEW)",
            "10": "⚡ Enhanced Bettercap Attacks (NEW)",
            "11": "📡 Physical Attack Module (NEW)",
            "12": "🔓 Hashcat Automation (NEW)",
            "13": "💾 MSF Database Manager (NEW)",
            "14": "🔄 Framework Updater (NEW)",
            "15": "Session Management",
            "16": "Generate Report",
            "17": "Tool Status Check",
            "0": "Exit"
        }

        for key, value in modules.items():
            if "NEW" in value:
                print(f"{Colors.GREEN}{Colors.BOLD}[{key}]{Colors.RESET} {value}")
            else:
                print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")
        return choice

    def advanced_exploit_menu(self):
        """Advanced exploit automation menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ ADVANCED EXPLOIT AUTOMATION ═══{Colors.RESET}\n")

        options = {
            "1": "Smart Auto-Exploit (from nmap scan)",
            "2": "Multi-Stage Exploitation",
            "3": "Exploit Suggester",
            "4": "Brute Force Services",
            "5": "Auxiliary Scanner Suite",
            "6": "Pivot Attack Setup",
            "7": "Generate Custom Payload",
            "8": "Create Payload Dropper",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            target = input("Enter target IP/network: ")
            nmap_xml = input("Enter nmap XML file (or leave blank to scan now): ")
            self.exploit_auto.smart_exploit(target, nmap_xml if nmap_xml else None)

        elif choice == "2":
            target = input("Enter target: ")
            module = input("Enter initial exploit module: ")
            self.exploit_auto.multi_stage_exploit(target, module)

        elif choice == "3":
            target = input("Enter target: ")
            self.exploit_auto.exploit_suggester(target)

        elif choice == "4":
            target = input("Enter target: ")
            services = input("Enter services (comma-separated, e.g., ssh,ftp,smb): ").split(',')
            self.exploit_auto.brute_force_services(target, services)

        elif choice == "5":
            target = input("Enter target: ")
            self.exploit_auto.auxiliary_scan_suite(target)

        elif choice == "6":
            session_id = input("Enter session ID: ")
            pivot_target = input("Enter pivot target network: ")
            self.exploit_auto.pivot_attack(session_id, pivot_target)

        elif choice == "7":
            payload_type = input("Enter payload type (e.g., windows/meterpreter/reverse_tcp): ")
            lhost = input("Enter LHOST: ")
            lport = input("Enter LPORT: ")
            self.exploit_auto.generate_custom_payload(payload_type, lhost, lport)

        elif choice == "8":
            payload_file = input("Enter payload file path: ")
            self.exploit_auto.payload_dropper(Path(payload_file))

        return choice != "0"

    def anonymous_scanning_menu(self):
        """Anonymous scanning menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ ANONYMOUS SCANNING ═══{Colors.RESET}\n")

        options = {
            "1": "Start Tor Service",
            "2": "Check Current IP",
            "3": "Renew Tor Identity (New IP)",
            "4": "Scan Through Tor",
            "5": "Rotating IP Scan",
            "6": "Tor Nikto Scan",
            "7": "Tor SQLMap",
            "8": "Stealth Scan",
            "9": "Test Anonymity",
            "10": "Install Anonymity Tools",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            self.anon_scanner.start_tor()

        elif choice == "2":
            self.anon_scanner.get_current_ip()

        elif choice == "3":
            self.anon_scanner.renew_tor_identity()

        elif choice == "4":
            target = input("Enter target: ")
            self.anon_scanner.tor_nmap(target)

        elif choice == "5":
            target = input("Enter target: ")
            rotations = int(input("Number of rotations (default 5): ") or "5")
            self.anon_scanner.rotating_ip_scan(target, rotations)

        elif choice == "6":
            target = input("Enter target URL: ")
            self.anon_scanner.tor_nikto(target)

        elif choice == "7":
            url = input("Enter target URL: ")
            self.anon_scanner.tor_sqlmap(url)

        elif choice == "8":
            target = input("Enter target: ")
            self.anon_scanner.stealth_scan(target)

        elif choice == "9":
            self.anon_scanner.test_anonymity()

        elif choice == "10":
            self.anon_scanner.install_anonymity_tools()

        return choice != "0"

    def post_exploit_menu(self):
        """Post-exploitation menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ POST-EXPLOITATION SUITE ═══{Colors.RESET}\n")

        options = {
            "1": "Full Post-Exploitation (Auto)",
            "2": "Privilege Escalation",
            "3": "Establish Persistence",
            "4": "Data Exfiltration",
            "5": "Lateral Movement",
            "6": "Mimikatz Automation",
            "7": "Domain Enumeration",
            "8": "Kerberoasting",
            "9": "BloodHound Collection",
            "10": "Cleanup Tracks",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        session_id = input("Enter Meterpreter session ID: ") if choice != "0" else None

        if choice == "1":
            target_os = input("Target OS (windows/linux): ")
            self.post_exploit.full_post_exploit(session_id, target_os)

        elif choice == "2":
            target_os = input("Target OS (windows/linux): ")
            self.post_exploit.privilege_escalation(session_id, target_os)

        elif choice == "3":
            target_os = input("Target OS (windows/linux): ")
            self.post_exploit.persistence(session_id, target_os)

        elif choice == "4":
            self.post_exploit.data_exfiltration(session_id)

        elif choice == "5":
            subnet = input("Enter target subnet: ")
            self.post_exploit.lateral_movement(session_id, subnet)

        elif choice == "6":
            self.post_exploit.mimikatz_automation(session_id)

        elif choice == "7":
            self.post_exploit.domain_enumeration(session_id)

        elif choice == "8":
            self.post_exploit.kerberoasting(session_id)

        elif choice == "9":
            self.post_exploit.bloodhound_collection(session_id)

        elif choice == "10":
            target_os = input("Target OS (windows/linux): ")
            self.post_exploit.cleanup_tracks(session_id, target_os)

        return choice != "0"

    def physical_attacks_menu(self):
        """Physical attacks menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ PHYSICAL ATTACK MODULE ═══{Colors.RESET}\n")

        options = {
            "1": "WiFi Beacon Spam",
            "2": "WiFi Deauth Storm",
            "3": "Network Crash Attack",
            "4": "Evil Twin KARMA",
            "5": "USB Rubber Ducky Payload",
            "6": "Rogue DHCP Server",
            "7": "Bluetooth Attack Suite",
            "8": "Slowloris DoS",
            "9": "WiFi Jamming",
            "10": "Fake AP Honeypot",
            "11": "Full Physical Assessment",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            interface = input("Enter monitor interface: ")
            num_ssids = int(input("Number of SSIDs (default 100): ") or "100")
            self.physical.wifi_beacon_spam(interface, num_ssids)

        elif choice == "2":
            interface = input("Enter monitor interface: ")
            mode = input("Mode (all/targeted): ")
            self.physical.wifi_deauth_storm(interface, mode)

        elif choice == "3":
            interface = input("Enter interface: ")
            target = input("Enter target IP (or leave blank): ")
            self.physical.network_crash_attack(interface, target if target else None)

        elif choice == "4":
            interface = input("Enter monitor interface: ")
            self.physical.evil_twin_karma(interface)

        elif choice == "5":
            payload_type = input("Payload type (reverse_shell/exfiltrate/backdoor/wifi_passwords/disable_defender): ")
            self.physical.usb_rubber_ducky_payload(payload_type)

        elif choice == "6":
            interface = input("Enter interface: ")
            self.physical.rogue_dhcp_server(interface)

        elif choice == "7":
            self.physical.bluetooth_attack_suite()

        elif choice == "8":
            target = input("Enter target: ")
            port = int(input("Enter port (default 80): ") or "80")
            self.physical.slowloris_attack(target, port)

        elif choice == "9":
            interface = input("Enter monitor interface: ")
            self.physical.wifi_jamming_attack(interface)

        elif choice == "10":
            interface = input("Enter monitor interface: ")
            ssid = input("Enter SSID: ")
            self.physical.fake_ap_honeypot(interface, ssid)

        elif choice == "11":
            interface = input("Enter interface: ")
            self.physical.full_physical_assessment(interface)

        return choice != "0"

    def hashcat_menu(self):
        """Hashcat automation menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ HASHCAT AUTOMATION ═══{Colors.RESET}\n")

        options = {
            "1": "Auto-Crack Hashes",
            "2": "WPA/WPA2 Handshake Crack",
            "3": "NTLM Crack (Optimized)",
            "4": "Smart Mask Attack",
            "5": "Hybrid Attack",
            "6": "Download Premium Wordlists",
            "7": "Show Cracked Hashes",
            "8": "Benchmark",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            hash_file = input("Enter hash file path: ")
            hash_type = input("Hash type (or 'auto'): ")
            self.hashcat.auto_crack(hash_file, hash_type)

        elif choice == "2":
            cap_file = input("Enter .cap file path: ")
            self.hashcat.wpa_handshake_crack(cap_file)

        elif choice == "3":
            hash_file = input("Enter NTLM hash file: ")
            self.hashcat.ntlm_crack_optimized(hash_file)

        elif choice == "4":
            hash_file = input("Enter hash file: ")
            hash_type = input("Hash type: ")
            self.hashcat.mask_attack_smart(hash_file, hash_type)

        elif choice == "5":
            hash_file = input("Enter hash file: ")
            hash_type = input("Hash type: ")
            self.hashcat.hybrid_attack(hash_file, hash_type)

        elif choice == "6":
            self.hashcat.download_premium_wordlists()

        elif choice == "7":
            hash_file = input("Enter hash file: ")
            self.hashcat.show_cracked(hash_file)

        elif choice == "8":
            self.hashcat.benchmark()

        return choice != "0"

    def msf_db_menu(self):
        """MSF Database menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ MSF DATABASE MANAGER ═══{Colors.RESET}\n")

        options = {
            "1": "Auto-Setup Database",
            "2": "Check Database Status",
            "3": "Import Nmap Scan",
            "4": "Query Hosts",
            "5": "Query Services",
            "6": "Query Vulnerabilities",
            "7": "Query Credentials",
            "8": "Export Database",
            "9": "Backup Database",
            "10": "Workspace Management",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            self.msf_db.auto_setup()

        elif choice == "2":
            self.msf_db.check_db_status()

        elif choice == "3":
            xml_file = input("Enter nmap XML file: ")
            self.msf_db.import_nmap_scan(xml_file)

        elif choice == "4":
            self.msf_db.query_hosts()

        elif choice == "5":
            port = input("Enter port (or leave blank for all): ")
            self.msf_db.query_services(int(port) if port else None)

        elif choice == "6":
            self.msf_db.query_vulns()

        elif choice == "7":
            self.msf_db.query_creds()

        elif choice == "8":
            format_type = input("Format (xml/json): ")
            self.msf_db.export_data(format_type)

        elif choice == "9":
            self.msf_db.backup_database()

        elif choice == "10":
            self.msf_db.workspace_list()

        return choice != "0"

    def updater_menu(self):
        """Framework updater menu"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ FRAMEWORK UPDATER ═══{Colors.RESET}\n")

        options = {
            "1": "Check for Updates",
            "2": "Update Framework",
            "3": "Update All Tools",
            "4": "Update Wordlists",
            "5": "Update Exploit-DB",
            "6": "Full System Update",
            "7": "Show Changelog",
            "8": "Check Dependencies",
            "9": "Rollback Version",
            "0": "Back"
        }

        for key, value in options.items():
            print(f"{Colors.GREEN}[{key}]{Colors.RESET} {value}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")

        if choice == "1":
            self.updater.check_for_updates()

        elif choice == "2":
            self.updater.update_framework()

        elif choice == "3":
            self.updater.update_tools()

        elif choice == "4":
            self.updater.update_wordlists()

        elif choice == "5":
            self.updater.update_exploitdb()

        elif choice == "6":
            self.updater.full_update()

        elif choice == "7":
            self.updater.show_changelog()

        elif choice == "8":
            self.updater.check_dependencies()

        elif choice == "9":
            self.updater.rollback()

        return choice != "0"

    def run(self):
        """Enhanced main program loop"""
        print(BANNER)
        print(f"{Colors.CYAN}Version: 2.0.0-ULTIMATE{Colors.RESET}")
        print(f"{Colors.CYAN}Session ID: {self.session_id}{Colors.RESET}")
        print(f"{Colors.CYAN}Log file: {self.session_log}{Colors.RESET}\n")

        if not MODULES_LOADED:
            print(f"{Colors.YELLOW}[WARNING] Running in basic mode - advanced modules not loaded{Colors.RESET}\n")

        self.log("Franken-Pentest Framework v2.0 ULTIMATE started", "INFO")
        self.check_root()

        while True:
            try:
                choice = self.show_menu()

                # Original modules (1-6)
                if choice == "1":
                    while self.metasploit_menu():
                        pass

                elif choice == "2":
                    while self.set_menu():
                        pass

                elif choice == "3":
                    while self.bettercap_menu():
                        pass

                elif choice == "4":
                    while self.wireless_menu():
                        pass

                elif choice == "5":
                    while self.wireshark_menu():
                        pass

                elif choice == "6":
                    while self.attack_chains_menu():
                        pass

                # New advanced modules (7-14)
                elif choice == "7" and MODULES_LOADED:
                    while self.advanced_exploit_menu():
                        pass

                elif choice == "8" and MODULES_LOADED:
                    while self.anonymous_scanning_menu():
                        pass

                elif choice == "9" and MODULES_LOADED:
                    while self.post_exploit_menu():
                        pass

                elif choice == "10" and MODULES_LOADED:
                    self.log("Enhanced Bettercap - use option 3 for basic or integrate advanced features", "INFO")

                elif choice == "11" and MODULES_LOADED:
                    while self.physical_attacks_menu():
                        pass

                elif choice == "12" and MODULES_LOADED:
                    while self.hashcat_menu():
                        pass

                elif choice == "13" and MODULES_LOADED:
                    while self.msf_db_menu():
                        pass

                elif choice == "14" and MODULES_LOADED:
                    while self.updater_menu():
                        pass

                # Original modules continued (15-17)
                elif choice == "15":
                    self.session_management()

                elif choice == "16":
                    self.generate_report()

                elif choice == "17":
                    self.tool_status_check()

                elif choice == "0":
                    self.log("Exiting Franken-Pentest Framework", "INFO")
                    print(f"\n{Colors.GREEN}Thank you for using Franken-Pentest v2.0 ULTIMATE!{Colors.RESET}")
                    print(f"{Colors.YELLOW}Session log: {self.session_log}{Colors.RESET}\n")
                    sys.exit(0)

                else:
                    self.log("Invalid option", "WARNING")

            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}[*] Interrupted{Colors.RESET}")
                confirm = input("Exit? (y/n): ")
                if confirm.lower() == 'y':
                    sys.exit(0)

            except Exception as e:
                self.log(f"Error: {str(e)}", "ERROR")
                import traceback
                traceback.print_exc()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Franken-Pentest Framework v2.0 ULTIMATE - All-in-One Penetration Testing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 franken_ultimate.py

For authorized security testing only!
        """
    )

    parser.add_argument('-v', '--version', action='version', version='Franken-Pentest v2.0.0-ULTIMATE')

    args = parser.parse_args()

    framework = FrankenUltimate()
    framework.run()


if __name__ == "__main__":
    main()
