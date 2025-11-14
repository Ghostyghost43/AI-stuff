#!/usr/bin/env python3
"""
Smart Launcher for Pentest Platform
Checks dependencies and provides helpful error messages
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   You have: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def check_root():
    """Check if running as root"""
    if os.geteuid() != 0:
        print("⚠️  WARNING: Not running as root")
        print("   Many features require root privileges")
        print("   Run with: sudo python3 launch.py")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)

def check_dependencies():
    """Check and report on dependencies"""
    deps = {
        'PyQt5': 'GUI framework (REQUIRED)',
        'scapy': 'Packet manipulation for MITM attacks',
        'matplotlib': 'Graph visualization',
        'networkx': 'Network topology graphs',
        'netifaces': 'Network interface detection',
        'numpy': 'Numerical operations',
        'psutil': 'System monitoring'
    }

    missing_required = []
    missing_optional = []

    print("\n📦 Checking dependencies...")
    print("=" * 50)

    for module, description in deps.items():
        try:
            __import__(module)
            print(f"✓ {module:15} {description}")
        except ImportError:
            if module == 'PyQt5':
                missing_required.append(module)
                print(f"❌ {module:15} {description}")
            else:
                missing_optional.append(module)
                print(f"⚠️  {module:15} {description}")

    print("=" * 50)

    if missing_required:
        print(f"\n❌ CANNOT LAUNCH - Missing required: {', '.join(missing_required)}")
        print("\n🔧 FIX:")
        print("   Run the installation script:")
        print("   sudo ./install-pentest-platform.sh")
        print("\n   Or install manually:")
        print("   pip3 install PyQt5")
        sys.exit(1)

    if missing_optional:
        print(f"\n⚠️  Optional dependencies missing: {', '.join(missing_optional)}")
        print("   Some features will be limited")
        print("   Install with:")
        print(f"   pip3 install {' '.join(missing_optional)}")
        print("\n   Or run: sudo ./install-pentest-platform.sh")
        response = input("\nContinue with limited features? (Y/n): ")
        if response.lower() == 'n':
            sys.exit(0)

    print("\n✅ All checks passed!")

def check_tools():
    """Check if pentesting tools are installed"""
    tools = {
        'nmap': 'Network scanner',
        'aircrack-ng': 'Wireless attacks',
        'hashcat': 'GPU password cracker',
        'john': 'CPU password cracker',
    }

    print("\n🔧 Checking pentesting tools...")
    print("=" * 50)

    missing_tools = []
    for tool, description in tools.items():
        if os.system(f"which {tool} > /dev/null 2>&1") == 0:
            print(f"✓ {tool:15} {description}")
        else:
            missing_tools.append(tool)
            print(f"⚠️  {tool:15} {description}")

    print("=" * 50)

    if missing_tools:
        print(f"\n⚠️  Tools not found: {', '.join(missing_tools)}")
        print("   Install with: sudo ./install-pentest-platform.sh")
        print("   Or manually: sudo apt-get install " + ' '.join(missing_tools))

def main():
    """Main launcher"""
    print("╔═══════════════════════════════════════════════════╗")
    print("║   🔒 Advanced Pentest Automation Platform         ║")
    print("║   Smart Dependency Checker & Launcher             ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()

    # Run checks
    check_python_version()
    check_root()
    check_dependencies()
    check_tools()

    print("\n🚀 Launching GUI...")
    print("=" * 50)

    # Import and launch
    try:
        import pentest_platform
        pentest_platform.main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 TIP: Check the error above and install missing dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()
