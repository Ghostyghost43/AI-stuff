#!/usr/bin/env python3
"""
Real-time Monitoring and Screenshot Module
===========================================
Live graphs, statistics, and automatic screenshot capture

AUTHORIZED USE ONLY
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from collections import deque
import json


class Colors:
    GHOST = '\033[38;5;147m'
    PHANTOM = '\033[38;5;213m'
    TOXIC = '\033[38;5;46m'
    NEON = '\033[38;5;51m'
    GOLD = '\033[38;5;220m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class WiFiMonitor:
    def __init__(self, interface, capture_dir):
        self.interface = interface
        self.capture_dir = Path(capture_dir)
        self.screenshot_dir = self.capture_dir / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Statistics
        self.stats = {
            'networks_found': 0,
            'clients_found': 0,
            'handshakes_captured': 0,
            'passwords_cracked': 0,
            'attacks_launched': 0,
            'start_time': time.time()
        }

        # Real-time data
        self.signal_history = deque(maxlen=100)
        self.client_activity = deque(maxlen=100)
        self.attack_log = []

    def take_screenshot(self, description=""):
        """Take screenshot of current terminal"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = self.screenshot_dir / f"screenshot_{timestamp}.png"

        # Try different screenshot tools
        screenshot_cmds = [
            ['scrot', str(screenshot_file)],
            ['import', '-window', 'root', str(screenshot_file)],
            ['gnome-screenshot', '-f', str(screenshot_file)],
        ]

        for cmd in screenshot_cmds:
            result = subprocess.run(cmd, capture_output=True, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                print(f"{Colors.NEON}📸 Screenshot saved: {screenshot_file}{Colors.ENDC}")

                # Add description file
                if description:
                    desc_file = screenshot_file.with_suffix('.txt')
                    with open(desc_file, 'w') as f:
                        f.write(f"Time: {timestamp}\n")
                        f.write(f"Description: {description}\n")

                return str(screenshot_file)

        # If all fail, try termshot (terminal-only)
        try:
            result = subprocess.run(['which', 'termshot'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['termshot', str(screenshot_file)], stderr=subprocess.DEVNULL)
                return str(screenshot_file)
        except:
            pass

        return None

    def update_stats(self, stat_name, value=None):
        """Update statistics"""
        if value is not None:
            self.stats[stat_name] = value
        else:
            self.stats[stat_name] += 1

    def log_attack(self, attack_type, target, result):
        """Log attack attempt"""
        self.attack_log.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': attack_type,
            'target': target,
            'result': result
        })

        # Auto-screenshot on success
        if result == 'success':
            self.take_screenshot(f"{attack_type} successful on {target}")

    def display_live_stats(self):
        """Display live statistics dashboard"""
        uptime = int(time.time() - self.stats['start_time'])
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60

        print(f"\n{Colors.PHANTOM}{'='*80}")
        print(f"👻 GHOST AUTOPWN - LIVE STATISTICS")
        print(f"{'='*80}{Colors.ENDC}\n")

        print(f"{Colors.TOXIC}📊 Session Stats:{Colors.ENDC}")
        print(f"  Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"  Networks Found: {Colors.NEON}{self.stats['networks_found']}{Colors.ENDC}")
        print(f"  Clients Detected: {Colors.NEON}{self.stats['clients_found']}{Colors.ENDC}")
        print(f"  Handshakes Captured: {Colors.GOLD}{self.stats['handshakes_captured']}{Colors.ENDC}")
        print(f"  Passwords Cracked: {Colors.TOXIC}{self.stats['passwords_cracked']}{Colors.ENDC}")
        print(f"  Attacks Launched: {Colors.PHANTOM}{self.stats['attacks_launched']}{Colors.ENDC}")
        print()

        # Success rate
        if self.stats['attacks_launched'] > 0:
            success_rate = (self.stats['passwords_cracked'] / self.stats['attacks_launched']) * 100
            print(f"{Colors.GOLD}✨ Success Rate: {success_rate:.1f}%{Colors.ENDC}\n")

    def draw_signal_graph(self, networks):
        """Draw ASCII graph of signal strengths"""
        if not networks:
            return

        print(f"{Colors.NEON}📡 Signal Strength Graph:{Colors.ENDC}\n")

        max_width = 60
        max_signal = -30  # dBm
        min_signal = -90

        for net in networks[:10]:  # Top 10
            try:
                power = int(net.get('power', '-100'))
                essid = net.get('essid', 'Unknown')[:20]

                # Normalize to graph width
                signal_range = max_signal - min_signal
                bar_length = int(((power - min_signal) / signal_range) * max_width)
                bar_length = max(0, min(max_width, bar_length))

                # Color by strength
                if power > -50:
                    color = Colors.TOXIC
                elif power > -70:
                    color = Colors.GOLD
                else:
                    color = Colors.GHOST

                bar = '█' * bar_length
                print(f"  {essid:<20} {color}{bar}{Colors.ENDC} {power} dBm")

            except:
                pass

        print()

    def draw_client_activity(self, clients_dict):
        """Draw graph of client activity"""
        if not clients_dict:
            return

        print(f"{Colors.PHANTOM}👥 Client Activity:{Colors.ENDC}\n")

        total_clients = sum(len(clients) for clients in clients_dict.values())
        max_width = 60

        # Get top APs by client count
        ap_clients = [(bssid, len(clients)) for bssid, clients in clients_dict.items()]
        ap_clients.sort(key=lambda x: x[1], reverse=True)

        for bssid, count in ap_clients[:10]:
            # Find network name
            essid = bssid[:17]  # Default to BSSID

            # Normalize to graph width
            if total_clients > 0:
                bar_length = int((count / max(max(c for _, c in ap_clients), 1)) * max_width)
            else:
                bar_length = 0

            bar = '▓' * bar_length
            print(f"  {essid:<20} {Colors.NEON}{bar}{Colors.ENDC} {count} client(s)")

        print()

    def save_session_report(self):
        """Save session report to JSON"""
        report_file = self.capture_dir / f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report = {
            'stats': self.stats,
            'attack_log': self.attack_log,
            'session_end': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"{Colors.GOLD}📄 Session report saved: {report_file}{Colors.ENDC}")

        return str(report_file)

    def generate_html_report(self):
        """Generate HTML report with graphs"""
        report_file = self.capture_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Ghost AutoPwn - Session Report</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            font-size: 32px;
            margin-bottom: 30px;
            text-shadow: 0 0 10px #00ff00;
        }}
        .stat-box {{
            background: #1a1a1a;
            border: 2px solid #00ff00;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
        }}
        .stat-value {{
            font-size: 48px;
            color: #00ffff;
            text-shadow: 0 0 20px #00ffff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #00ff00;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #1a1a1a;
        }}
    </style>
</head>
<body>
    <div class="header">👻 GHOST AUTOPWN - SESSION REPORT</div>

    <div class="stat-box">
        <h2>Session Statistics</h2>
        <div class="stat-value">{self.stats['networks_found']}</div>
        <div>Networks Found</div>
    </div>

    <div class="stat-box">
        <div class="stat-value">{self.stats['passwords_cracked']}</div>
        <div>Passwords Cracked</div>
    </div>

    <div class="stat-box">
        <h2>Attack Log</h2>
        <table>
            <tr>
                <th>Time</th>
                <th>Attack Type</th>
                <th>Target</th>
                <th>Result</th>
            </tr>
"""

        for attack in self.attack_log:
            html += f"""
            <tr>
                <td>{attack['timestamp']}</td>
                <td>{attack['type']}</td>
                <td>{attack['target']}</td>
                <td>{attack['result']}</td>
            </tr>
"""

        html += """
        </table>
    </div>
</body>
</html>
"""

        with open(report_file, 'w') as f:
            f.write(html)

        print(f"{Colors.TOXIC}📊 HTML report generated: {report_file}{Colors.ENDC}")

        return str(report_file)


def main():
    print(f"{Colors.TOXIC}Monitoring Module Loaded{Colors.ENDC}")


if __name__ == '__main__':
    main()
