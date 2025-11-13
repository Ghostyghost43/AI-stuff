#!/usr/bin/env python3
"""
Framework Updater Module
Auto-update Franken-Pentest Framework from GitHub
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

class FrameworkUpdater:
    def __init__(self, work_dir, log_callback=None):
        self.work_dir = Path(work_dir)
        self.log = log_callback or print
        self.framework_dir = Path(__file__).parent.parent
        self.version_file = self.framework_dir / "VERSION"
        self.current_version = self.get_current_version()

    def get_current_version(self):
        """Get current framework version"""
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        return "1.0.0"

    def check_for_updates(self):
        """Check if updates are available"""
        self.log("Checking for updates...", "INFO")

        # Change to framework directory
        os.chdir(self.framework_dir)

        # Fetch latest changes
        result = subprocess.run(['git', 'fetch', 'origin'],
                              capture_output=True, text=True)

        # Check if behind
        result = subprocess.run(['git', 'rev-list', 'HEAD...origin/main', '--count'],
                              capture_output=True, text=True)

        commits_behind = int(result.stdout.strip() or 0)

        if commits_behind > 0:
            self.log(f"Updates available ({commits_behind} commits)", "INFO")
            return True
        else:
            self.log("Framework is up to date", "SUCCESS")
            return False

    def update_framework(self):
        """Update framework from GitHub"""
        self.log("Updating Franken-Pentest Framework...", "INFO")

        os.chdir(self.framework_dir)

        # Stash local changes
        self.log("Stashing local changes...", "INFO")
        os.system("git stash")

        # Pull latest changes
        self.log("Pulling latest changes...", "INFO")
        result = os.system("git pull origin main")

        if result == 0:
            self.log("Framework updated successfully!", "SUCCESS")

            # Reinstall if needed
            reinstall = input("Reinstall dependencies? (y/n): ")
            if reinstall.lower() == 'y':
                os.system("sudo bash franken-install.sh")

            self.log("Update complete! Please restart the framework.", "SUCCESS")
            return True
        else:
            self.log("Update failed", "ERROR")
            return False

    def rollback(self):
        """Rollback to previous version"""
        self.log("Rolling back to previous version...", "WARNING")

        os.chdir(self.framework_dir)

        # Get previous commit
        result = subprocess.run(['git', 'log', '--oneline', '-2'],
                              capture_output=True, text=True)

        commits = result.stdout.strip().split('\n')
        if len(commits) >= 2:
            previous_commit = commits[1].split()[0]

            self.log(f"Rolling back to commit: {previous_commit}", "INFO")
            os.system(f"git reset --hard {previous_commit}")

            self.log("Rollback complete", "SUCCESS")
            return True
        else:
            self.log("Cannot rollback - no previous version", "ERROR")
            return False

    def update_tools(self):
        """Update all pentesting tools"""
        self.log("Updating pentesting tools...", "INFO")

        tools_update = [
            "apt-get update",
            "apt-get upgrade -y metasploit-framework",
            "apt-get upgrade -y bettercap",
            "apt-get upgrade -y aircrack-ng",
            "apt-get upgrade -y wireshark",
            "msfupdate",
        ]

        for cmd in tools_update:
            self.log(f"Running: {cmd}", "INFO")
            os.system(cmd)

        self.log("Tools updated", "SUCCESS")

    def update_wordlists(self):
        """Update wordlists"""
        self.log("Updating wordlists...", "INFO")

        os.chdir("/usr/share/wordlists")

        if Path("SecLists").exists():
            os.chdir("SecLists")
            os.system("git pull")
        else:
            os.system("git clone https://github.com/danielmiessler/SecLists.git")

        self.log("Wordlists updated", "SUCCESS")

    def update_exploitdb(self):
        """Update Exploit Database"""
        self.log("Updating Exploit-DB...", "INFO")
        os.system("searchsploit -u")
        self.log("Exploit-DB updated", "SUCCESS")

    def full_update(self):
        """Complete system update"""
        self.log("Running full system update...", "INFO")

        # Framework
        if self.check_for_updates():
            self.update_framework()

        # Tools
        self.update_tools()

        # Wordlists
        self.update_wordlists()

        # Exploit DB
        self.update_exploitdb()

        self.log("Full update complete!", "SUCCESS")

    def show_changelog(self):
        """Show recent changes"""
        self.log("Recent changes:", "INFO")

        os.chdir(self.framework_dir)
        os.system("git log --oneline -10")

    def check_dependencies(self):
        """Check if all dependencies are installed"""
        self.log("Checking dependencies...", "INFO")

        required_tools = [
            'msfconsole',
            'setoolkit',
            'bettercap',
            'aircrack-ng',
            'mdk4',
            'wireshark',
            'nmap',
            'hashcat',
            'john'
        ]

        missing = []

        for tool in required_tools:
            result = subprocess.run(['which', tool],
                                  capture_output=True)
            if result.returncode != 0:
                missing.append(tool)
                self.log(f"  Missing: {tool}", "WARNING")
            else:
                self.log(f"  Found: {tool}", "SUCCESS")

        if missing:
            self.log(f"\nMissing tools: {', '.join(missing)}", "WARNING")
            install = input("Install missing tools? (y/n): ")
            if install.lower() == 'y':
                os.system("sudo bash franken-install.sh")
        else:
            self.log("All dependencies installed!", "SUCCESS")

        return len(missing) == 0
