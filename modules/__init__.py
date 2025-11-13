"""
Franken-Pentest Framework - Advanced Modules
Version 2.0.0-ULTIMATE

All modules for the ultimate penetration testing framework
"""

__version__ = "2.0.0-ULTIMATE"
__author__ = "Franken-Pentest Team"

# Import all modules for easy access
from .exploit_automation import ExploitAutomation
from .anonymous_scanning import AnonymousScanner
from .post_exploitation import PostExploitation
from .better_bettercap import BettercapAdvanced
from .physical_attacks import PhysicalAttacks
from .hashcat_automation import HashcatAutomation
from .msf_database import MSFDatabase
from .framework_updater import FrameworkUpdater

__all__ = [
    'ExploitAutomation',
    'AnonymousScanner',
    'PostExploitation',
    'BettercapAdvanced',
    'PhysicalAttacks',
    'HashcatAutomation',
    'MSFDatabase',
    'FrameworkUpdater'
]
