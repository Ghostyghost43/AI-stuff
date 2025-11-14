#!/usr/bin/env python3
"""
WiFi Attack Intelligence Module
================================
Auto-target selection, success probability scoring, vendor fingerprinting

AUTHORIZED USE ONLY
"""

import re
import subprocess
from pathlib import Path
import json


class Colors:
    GHOST = '\033[38;5;147m'
    TOXIC = '\033[38;5;46m'
    NEON = '\033[38;5;51m'
    GOLD = '\033[38;5;220m'
    ENDC = '\033[0m'


class WiFiIntelligence:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.oui_database = self.load_oui_database()
        self.vulnerability_scores = {
            'WPS_UNLOCKED': 95,
            'WEP': 90,
            'DEFAULT_SSID': 75,
            'WEAK_ENCRYPTION': 70,
            'MANY_CLIENTS': 65,
            'WPA_OLD': 60,
            'STRONG_SIGNAL': 55,
            'WPA2_PSK': 45,
            'WPA3': 20
        }

    def load_oui_database(self):
        """Load MAC address OUI database for vendor fingerprinting"""
        # Simplified OUI database - in production, load from IEEE database
        return {
            '00:1A:11': 'Google',
            '00:1B:63': 'Apple',
            '00:22:6B': 'Cisco',
            '00:24:A5': 'Netgear',
            '00:25:9C': 'Cisco Linksys',
            '00:26:B8': 'D-Link',
            '00:0F:66': 'Netgear',
            '00:18:E7': 'Netgear',
            '00:1D:7E': 'Cisco Linksys',
            '00:1E:C7': 'D-Link',
            '00:1F:33': 'Netgear',
            '00:21:29': 'D-Link',
            '00:24:01': 'D-Link',
            '00:09:5B': 'Netgear',
            '00:0C:41': 'Linksys',
            '00:12:17': 'Linksys',
            '00:13:10': 'Linksys',
            '00:14:BF': 'Linksys',
            '00:16:B6': 'Linksys',
            '00:18:39': 'Linksys',
            '00:18:F8': 'Linksys',
            '00:1A:70': 'Linksys',
            '00:1C:10': 'Linksys',
            '00:1D:7E': 'Linksys',
            '00:1E:E5': 'Linksys',
            '00:21:29': 'Linksys',
            '00:22:6B': 'Linksys',
            '00:23:69': 'Linksys',
            '00:25:00': 'Linksys',
            '68:7F:74': 'TP-Link',
            '50:C7:BF': 'TP-Link',
            '00:27:19': 'TP-Link',
            'A0:F3:C1': 'TP-Link',
            '14:CF:92': 'TP-Link',
            'EC:08:6B': 'TP-Link',
            'F4:F2:6D': 'TP-Link',
            '90:F6:52': 'TP-Link',
            '00:50:56': 'VMware',
            '00:0C:29': 'VMware',
            '00:05:69': 'VMware',
        }

    def vendor_fingerprint(self, bssid):
        """Fingerprint router vendor from MAC address"""
        if not bssid:
            return "Unknown"

        # Extract OUI (first 3 octets)
        oui = ':'.join(bssid.upper().split(':')[:3])

        vendor = self.oui_database.get(oui, "Unknown")

        if self.verbose and vendor != "Unknown":
            print(f"{Colors.NEON}[FINGERPRINT] {bssid} → {vendor}{Colors.ENDC}")

        return vendor

    def identify_router_model(self, essid, bssid, encryption):
        """Try to identify specific router model from patterns"""
        models = []

        # SSID patterns
        if essid.startswith('NETGEAR'):
            models.append('Netgear Router')
        elif essid.startswith('Linksys'):
            models.append('Linksys Router')
        elif essid.startswith('TP-LINK'):
            models.append('TP-Link Router')
        elif essid.startswith('ASUS'):
            models.append('ASUS Router')
        elif essid.startswith('Belkin'):
            models.append('Belkin Router')
        elif essid.startswith('CenturyLink'):
            models.append('CenturyLink Modem')
        elif essid.startswith('xfinitywifi'):
            models.append('Comcast Xfinity Hotspot')
        elif essid.startswith('ATT'):
            models.append('AT&T Gateway')
        elif essid.startswith('Google Fiber'):
            models.append('Google Fiber Box')
        elif re.match(r'^[A-Z]{5}\d{3}$', essid):
            models.append('Verizon FiOS Router')
        elif re.match(r'^\w{2,3}\d{4,6}$', essid):
            models.append('ISP Default Router')

        # Vendor from MAC
        vendor = self.vendor_fingerprint(bssid)
        if vendor != "Unknown":
            models.append(vendor)

        # Encryption patterns
        if 'WEP' in encryption:
            models.append('Legacy Device (Pre-2008)')
        elif 'WPA3' in encryption:
            models.append('Modern Router (2019+)')
        elif 'WPA2' in encryption and 'AES' in encryption:
            models.append('Standard Router (2008+)')

        return ', '.join(models) if models else "Unknown"

    def calculate_success_probability(self, network, clients):
        """Calculate probability of successful attack"""
        score = 0
        factors = []

        # WPS vulnerabilities
        if network.get('wps') and not network.get('wps_locked'):
            score += self.vulnerability_scores['WPS_UNLOCKED']
            factors.append(f"WPS Unlocked (+{self.vulnerability_scores['WPS_UNLOCKED']}%)")

        # Encryption weaknesses
        encryption = network.get('encryption', '')
        if 'WEP' in encryption:
            score += self.vulnerability_scores['WEP']
            factors.append(f"WEP Encryption (+{self.vulnerability_scores['WEP']}%)")
        elif 'WPA3' in encryption:
            score -= 30
            factors.append("WPA3 (-30%)")
        elif 'WPA2' in encryption:
            score += self.vulnerability_scores['WPA2_PSK']
            factors.append(f"WPA2 (+{self.vulnerability_scores['WPA2_PSK']}%)")

        # Default SSID patterns
        essid = network.get('essid', '')
        default_patterns = [
            r'^NETGEAR\d+$',
            r'^Linksys$',
            r'^TP-LINK_\w+$',
            r'^DIRECT-\w+',
            r'^WiFi$',
            r'^Wireless$',
            r'^\w{2,3}\d{4,6}$'
        ]

        for pattern in default_patterns:
            if re.match(pattern, essid):
                score += self.vulnerability_scores['DEFAULT_SSID']
                factors.append(f"Default SSID Pattern (+{self.vulnerability_scores['DEFAULT_SSID']}%)")
                break

        # Signal strength (closer = easier)
        try:
            power = int(network.get('power', '-100'))
            if power > -50:
                score += self.vulnerability_scores['STRONG_SIGNAL']
                factors.append(f"Strong Signal (+{self.vulnerability_scores['STRONG_SIGNAL']}%)")
            elif power > -70:
                score += 30
                factors.append("Good Signal (+30%)")
        except:
            pass

        # Client count (more clients = more handshake opportunities)
        num_clients = len(clients)
        if num_clients >= 3:
            score += self.vulnerability_scores['MANY_CLIENTS']
            factors.append(f"{num_clients} Clients (+{self.vulnerability_scores['MANY_CLIENTS']}%)")
        elif num_clients >= 1:
            score += 40
            factors.append(f"{num_clients} Client(s) (+40%)")
        else:
            score -= 20
            factors.append("No Clients (-20%)")

        # Vendor vulnerabilities
        vendor = self.vendor_fingerprint(network.get('bssid', ''))
        if vendor in ['Netgear', 'Linksys', 'D-Link']:
            score += 25
            factors.append(f"Vulnerable Vendor: {vendor} (+25%)")

        # Normalize score to 0-100
        score = max(0, min(100, score))

        return {
            'score': score,
            'factors': factors,
            'verdict': self.get_verdict(score)
        }

    def get_verdict(self, score):
        """Get human-readable verdict"""
        if score >= 85:
            return f"{Colors.TOXIC}VERY HIGH - Highly Vulnerable{Colors.ENDC}"
        elif score >= 70:
            return f"{Colors.GOLD}HIGH - Good Target{Colors.ENDC}"
        elif score >= 50:
            return f"{Colors.NEON}MEDIUM - Moderate Difficulty{Colors.ENDC}"
        elif score >= 30:
            return "LOW - Challenging"
        else:
            return "VERY LOW - Hardened Target"

    def rank_targets(self, networks, clients_dict):
        """Rank all networks by attack success probability"""
        ranked = []

        for network in networks:
            bssid = network.get('bssid')
            clients = clients_dict.get(bssid, [])

            # Calculate score
            analysis = self.calculate_success_probability(network, clients)

            # Add metadata
            vendor = self.vendor_fingerprint(bssid)
            model = self.identify_router_model(
                network.get('essid', ''),
                bssid,
                network.get('encryption', '')
            )

            ranked.append({
                'network': network,
                'clients': clients,
                'score': analysis['score'],
                'factors': analysis['factors'],
                'verdict': analysis['verdict'],
                'vendor': vendor,
                'model': model
            })

        # Sort by score (highest first)
        ranked.sort(key=lambda x: x['score'], reverse=True)

        return ranked

    def auto_select_target(self, networks, clients_dict, min_score=60):
        """Automatically select best target"""
        ranked = self.rank_targets(networks, clients_dict)

        # Filter by minimum score
        viable = [r for r in ranked if r['score'] >= min_score]

        if not viable:
            return None

        best = viable[0]

        print(f"\n{Colors.TOXIC}{'='*80}")
        print(f"🎯 AUTO-SELECTED TARGET")
        print(f"{'='*80}{Colors.ENDC}\n")

        print(f"  Network: {best['network']['essid']}")
        print(f"  Score: {best['score']}/100")
        print(f"  Verdict: {best['verdict']}")
        print(f"  Vendor: {best['vendor']}")
        print(f"  Model: {best['model']}")
        print(f"\n  Success Factors:")
        for factor in best['factors']:
            print(f"    • {factor}")
        print()

        return best['network']

    def display_ranked_targets(self, networks, clients_dict):
        """Display all targets ranked by success probability"""
        ranked = self.rank_targets(networks, clients_dict)

        print(f"\n{Colors.NEON}{'='*120}")
        print(f"📊 TARGETS RANKED BY SUCCESS PROBABILITY")
        print(f"{'='*120}{Colors.ENDC}\n")

        print(f"{'#':<4} {'ESSID':<25} {'Score':<8} {'Verdict':<30} {'Vendor':<20} {'Clients':<8}")
        print("-" * 120)

        for i, target in enumerate(ranked, 1):
            essid = target['network']['essid']
            score = f"{target['score']}/100"
            verdict_display = target['verdict']
            vendor = target['vendor']
            num_clients = len(target['clients'])

            # Color code by score
            if target['score'] >= 85:
                color = Colors.TOXIC
            elif target['score'] >= 70:
                color = Colors.GOLD
            elif target['score'] >= 50:
                color = Colors.NEON
            else:
                color = Colors.GHOST

            print(f"{color}{i:<4} {essid:<25} {score:<8}{Colors.ENDC} {verdict_display:<40} {vendor:<20} {num_clients:<8}")

        print()

        return ranked


def main():
    print(f"{Colors.TOXIC}WiFi Intelligence Module Loaded{Colors.ENDC}")


if __name__ == '__main__':
    main()
