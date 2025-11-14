#!/usr/bin/env python3
"""
Ghost-Themed UI Components
===========================
Colorful ghost-themed interface elements
"""


class Colors:
    GHOST = '\033[38;5;147m'
    PHANTOM = '\033[38;5;213m'
    SPOOKY = '\033[38;5;93m'
    NEON = '\033[38;5;51m'
    TOXIC = '\033[38;5;46m'
    BLOOD = '\033[38;5;196m'
    GOLD = '\033[38;5;220m'
    CYBER = '\033[38;5;81m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def ghost_banner():
    """Display awesome ghost-themed banner"""
    banner = f"""{Colors.PHANTOM}
    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
   ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
   ██║  ███╗███████║██║   ██║███████╗   ██║
   ██║   ██║██╔══██║██║   ██║╚════██║   ██║
   ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
{Colors.ENDC}
{Colors.TOXIC}    ╔══════════════════════════════════════════╗
    ║  👻 AUTOPWN - WiFi Security Suite 👻  ║
    ║    Advanced Penetration Testing Tool    ║
    ╚══════════════════════════════════════════╝{Colors.ENDC}

{Colors.BLOOD}{Colors.BOLD}    ⚠️  AUTHORIZED USE ONLY ⚠️{Colors.ENDC}
{Colors.GHOST}    For Penetration Testing & Security Research{Colors.ENDC}

{Colors.NEON}    Features:{Colors.ENDC}
{Colors.PHANTOM}    • 🎯 Evil Twin & Karma Attacks
    • 🔥 Multi-Vector WiFi Attacks
    • 🧠 AI Target Selection
    • 📊 Real-Time Monitoring
    • 🕵️  Stealth & IDS Evasion{Colors.ENDC}

{Colors.GOLD}{'='*55}{Colors.ENDC}
"""
    print(banner)


def show_attack_menu():
    """Display attack selection menu"""
    print(f"\n{Colors.PHANTOM}{'='*70}")
    print(f"👻 SELECT ATTACK VECTOR")
    print(f"{'='*70}{Colors.ENDC}\n")

    print(f"{Colors.TOXIC}━━━ Classic Attacks ━━━{Colors.ENDC}")
    print(f"  [1] 🎯 {Colors.NEON}PMKID Attack{Colors.ENDC} (No clients needed - Fast)")
    print(f"  [2] 🤝 {Colors.NEON}WPA Handshake{Colors.ENDC} (Traditional method)")
    print(f"  [3] 🔓 {Colors.NEON}WPS Pixie Dust{Colors.ENDC} (If WPS enabled)")
    print(f"  [4] 🔨 {Colors.NEON}WPS PIN Bruteforce{Colors.ENDC} (Slow but thorough)\n")

    print(f"{Colors.PHANTOM}━━━ Advanced Attacks ━━━{Colors.ENDC}")
    print(f"  [5] 👤 {Colors.TOXIC}Evil Twin Attack{Colors.ENDC} (Fake AP + Captive Portal)")
    print(f"  [6] 🌀 {Colors.TOXIC}Karma Attack{Colors.ENDC} (Respond to all probes)")
    print(f"  [7] 📡 {Colors.TOXIC}Channel Hopping Scan{Colors.ENDC} (Deep recon)\n")

    print(f"{Colors.GOLD}━━━ Automated ━━━{Colors.ENDC}")
    print(f"  [8] 🤖 {Colors.CYBER}Auto-Attack{Colors.ENDC} (Try all methods)")
    print(f"  [9] 🧠 {Colors.CYBER}AI-Select Target{Colors.ENDC} (Let AI choose best target)\n")

    print(f"{Colors.GHOST}━━━ Options ━━━{Colors.ENDC}")
    print(f"  [S] 🕵️  {Colors.PHANTOM}Stealth Mode{Colors.ENDC} (IDS/IPS Evasion)")
    print(f"  [M] 📊 {Colors.NEON}Show Statistics{Colors.ENDC}")
    print(f"  [Q] 🚪 {Colors.BLOOD}Quit{Colors.ENDC}\n")


def show_stealth_menu():
    """Display stealth configuration menu"""
    print(f"\n{Colors.PHANTOM}{'='*70}")
    print(f"🕵️  STEALTH & EVASION CONFIGURATION")
    print(f"{'='*70}{Colors.ENDC}\n")

    print(f"  [{Colors.TOXIC}1{Colors.ENDC}] 👻 {Colors.GHOST}Ghost Mode{Colors.ENDC} - Maximum stealth (very slow)")
    print(f"  [{Colors.NEON}2{Colors.ENDC}] ⚖️  {Colors.NEON}Balanced Mode{Colors.ENDC} - Moderate stealth/speed")
    print(f"  [{Colors.GOLD}3{Colors.ENDC}] 🔥 {Colors.PHANTOM}Aggressive Mode{Colors.ENDC} - Fast, minimal stealth")
    print(f"  [{Colors.CYBER}4{Colors.ENDC}] ⚙️  {Colors.CYBER}Custom Settings{Colors.ENDC} - Manual configuration")
    print(f"  [{Colors.BLOOD}5{Colors.ENDC}] 🛡️  {Colors.BLOOD}IDS Detection{Colors.ENDC} - Scan for security systems\n")


def success_message(title, details):
    """Display success message"""
    print(f"\n{Colors.TOXIC}{Colors.BOLD}{'='*70}")
    print(f"✨ {title} ✨")
    print(f"{'='*70}{Colors.ENDC}\n")

    for key, value in details.items():
        print(f"{Colors.NEON}{key}:{Colors.ENDC} {value}")

    print()


def error_message(title, details):
    """Display error message"""
    print(f"\n{Colors.BLOOD}{Colors.BOLD}{'='*70}")
    print(f"💀 {title} 💀")
    print(f"{'='*70}{Colors.ENDC}\n")

    print(f"{Colors.PHANTOM}{details}{Colors.ENDC}\n")


def progress_bar(current, total, prefix='', suffix=''):
    """Display progress bar"""
    bar_length = 50
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    percent = f"{100 * current / total:.1f}%"

    print(f'\r{Colors.NEON}{prefix} |{Colors.TOXIC}{bar}{Colors.NEON}| {percent} {suffix}{Colors.ENDC}', end='', flush=True)

    if current >= total:
        print()


def show_capture_success(essid, password=None, file=None):
    """Show successful capture message"""
    print(f"\n{Colors.TOXIC}{'='*70}")
    print(f"{'🎯 CAPTURE SUCCESSFUL 🎯':^70}")
    print(f"{'='*70}{Colors.ENDC}\n")

    print(f"{Colors.NEON}Network:{Colors.ENDC} {essid}")

    if password:
        print(f"{Colors.TOXIC}Password:{Colors.ENDC} {Colors.BOLD}{password}{Colors.ENDC}")

    if file:
        print(f"{Colors.GHOST}Saved to:{Colors.ENDC} {file}")

    print()


def main():
    ghost_banner()
    show_attack_menu()


if __name__ == '__main__':
    main()
