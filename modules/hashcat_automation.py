#!/usr/bin/env python3
"""
Hashcat Automation Module
Automated hash cracking with optimized wordlists and rules
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

class HashcatAutomation:
    def __init__(self, work_dir, log_callback=None):
        self.work_dir = Path(work_dir)
        self.log = log_callback or print
        self.hashes_dir = self.work_dir / "hashes"
        self.cracked_dir = self.work_dir / "cracked"
        self.wordlists_dir = Path("/usr/share/wordlists")

        self.hashes_dir.mkdir(exist_ok=True)
        self.cracked_dir.mkdir(exist_ok=True)

        # Hash type mappings
        self.hash_types = {
            'md5': 0,
            'sha1': 100,
            'sha256': 1400,
            'sha512': 1700,
            'ntlm': 1000,
            'netntlmv2': 5600,
            'wpa': 2500,
            'wpa2': 2500,
            'bcrypt': 3200,
            'md5crypt': 500,
            'sha512crypt': 1800,
            'mysql': 300,
            'mssql': 131,
            'oracle': 112,
            'postgres': 12,
            'zip': 13600,
            'rar': 13000,
            '7z': 11600,
            'pdf': 10500,
            'office2007': 9400,
            'office2010': 9500,
            'office2013': 9600,
            'keepass': 13400,
            'lastpass': 6800,
            '1password': 6600,
            'bitcoin': 11300,
            'ethereum': 15700,
            'linux_shadow': 1800,
            'kerberos': 13100,
            'krb5tgs': 13100
        }

    def download_premium_wordlists(self):
        """Download and configure premium wordlists"""
        self.log("Downloading premium wordlists...", "INFO")

        wordlists = {
            'rockyou': 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt',
            'crackstation': 'https://crackstation.net/files/crackstation.txt.gz',
            'weakpass_2a': 'https://download.weakpass.com/wordlists/90/weakpass_2a.txt.gz',
        }

        os.system("mkdir -p /usr/share/wordlists/premium")

        for name, url in wordlists.items():
            self.log(f"Downloading {name}...", "INFO")
            output = f"/usr/share/wordlists/premium/{name}.txt"

            if url.endswith('.gz'):
                os.system(f"wget {url} -O {output}.gz && gunzip {output}.gz")
            else:
                os.system(f"wget {url} -O {output}")

        # Download rule sets
        self.log("Downloading hashcat rules...", "INFO")
        os.system("cd /usr/share/hashcat/rules && wget https://raw.githubusercontent.com/NotSoSecure/password_cracking_rules/master/OneRuleToRuleThemAll.rule")

        self.log("Wordlist setup complete", "SUCCESS")

    def identify_hash_type(self, hash_string):
        """Identify hash type from string"""
        hash_len = len(hash_string)

        identifications = {
            32: 'MD5 or NTLM',
            40: 'SHA1',
            64: 'SHA256',
            128: 'SHA512',
            13: 'MySQL',
            16: 'MySQL5 or MSSQL'
        }

        if hash_len in identifications:
            self.log(f"Possible hash type: {identifications[hash_len]}", "INFO")
            return identifications[hash_len]
        else:
            self.log(f"Unknown hash type (length: {hash_len})", "WARNING")
            return None

    def auto_crack(self, hash_file, hash_type='auto'):
        """Automated hash cracking with multiple strategies"""
        self.log(f"Starting automated cracking: {hash_file}", "INFO")

        output_file = self.cracked_dir / f"cracked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # Detect hash type if auto
        if hash_type == 'auto':
            with open(hash_file, 'r') as f:
                sample_hash = f.readline().strip()
                self.identify_hash_type(sample_hash)

            hash_type_input = input("Enter hash type (e.g., ntlm, sha256, wpa): ")
            hash_mode = self.hash_types.get(hash_type_input.lower(), 1000)
        else:
            hash_mode = self.hash_types.get(hash_type.lower(), 1000)

        self.log(f"Using hash mode: {hash_mode}", "INFO")

        # Strategy 1: Quick dictionary attack
        self.log("Strategy 1: Quick dictionary attack", "INFO")
        wordlist = self.wordlists_dir / "rockyou.txt"

        if wordlist.exists():
            cmd = f"hashcat -m {hash_mode} {hash_file} {wordlist} -o {output_file} --force"
            os.system(cmd)

        # Strategy 2: Dictionary + rules
        self.log("Strategy 2: Dictionary with rules", "INFO")
        rules = "/usr/share/hashcat/rules/best64.rule"
        cmd = f"hashcat -m {hash_mode} {hash_file} {wordlist} -r {rules} -o {output_file} --force"
        os.system(cmd)

        # Strategy 3: Combinator attack
        self.log("Strategy 3: Combinator attack", "INFO")
        cmd = f"hashcat -m {hash_mode} {hash_file} -a 1 {wordlist} {wordlist} -o {output_file} --force"
        os.system(cmd)

        # Strategy 4: Mask attack (brute force)
        self.log("Strategy 4: Mask attack (8 char lowercase+digits)", "INFO")
        cmd = f"hashcat -m {hash_mode} {hash_file} -a 3 ?l?l?l?l?d?d?d?d -o {output_file} --force"
        os.system(cmd)

        # Display results
        self.log(f"Results saved to: {output_file}", "SUCCESS")
        if output_file.exists():
            os.system(f"cat {output_file}")

        return output_file

    def wpa_handshake_crack(self, cap_file, ssid=None):
        """Crack WPA/WPA2 handshake"""
        self.log("WPA/WPA2 handshake cracking", "INFO")

        # Convert to hashcat format if needed
        hccapx_file = self.hashes_dir / f"wpa_{int(datetime.now().timestamp())}.hccapx"

        self.log("Converting capture to hashcat format...", "INFO")
        os.system(f"cap2hccapx {cap_file} {hccapx_file}")

        output_file = self.cracked_dir / f"wpa_cracked_{int(datetime.now().timestamp())}.txt"

        # Crack with rockyou
        wordlist = self.wordlists_dir / "rockyou.txt"

        self.log("Starting WPA crack (this may take a while)...", "INFO")
        cmd = f"hashcat -m 2500 {hccapx_file} {wordlist} -o {output_file} --force"
        os.system(cmd)

        # Try with rules
        self.log("Trying with rules...", "INFO")
        cmd = f"hashcat -m 2500 {hccapx_file} {wordlist} -r /usr/share/hashcat/rules/best64.rule -o {output_file} --force"
        os.system(cmd)

        if output_file.exists():
            self.log("Password found!", "SUCCESS")
            os.system(f"cat {output_file}")
        else:
            self.log("Password not found in wordlist", "WARNING")

        return output_file

    def ntlm_crack_optimized(self, ntlm_hash_file):
        """Optimized NTLM hash cracking"""
        self.log("NTLM hash cracking (optimized)", "INFO")

        output_file = self.cracked_dir / f"ntlm_cracked_{int(datetime.now().timestamp())}.txt"

        strategies = [
            # Quick wins
            {
                'name': 'Common passwords',
                'wordlist': '/usr/share/wordlists/metasploit/password.lst',
                'rules': None
            },
            # Medium
            {
                'name': 'Rockyou basic',
                'wordlist': '/usr/share/wordlists/rockyou.txt',
                'rules': None
            },
            # Advanced
            {
                'name': 'Rockyou with best64 rules',
                'wordlist': '/usr/share/wordlists/rockyou.txt',
                'rules': '/usr/share/hashcat/rules/best64.rule'
            },
            # Intensive
            {
                'name': 'Rockyou with OneRule',
                'wordlist': '/usr/share/wordlists/rockyou.txt',
                'rules': '/usr/share/hashcat/rules/OneRuleToRuleThemAll.rule'
            }
        ]

        for strategy in strategies:
            self.log(f"Trying: {strategy['name']}", "INFO")

            cmd = f"hashcat -m 1000 {ntlm_hash_file} {strategy['wordlist']}"

            if strategy['rules']:
                cmd += f" -r {strategy['rules']}"

            cmd += f" -o {output_file} --force"

            result = os.system(cmd)

            # Check if cracked
            if output_file.exists():
                with open(output_file, 'r') as f:
                    if f.read().strip():
                        self.log(f"Cracked using: {strategy['name']}", "SUCCESS")
                        os.system(f"cat {output_file}")
                        return output_file

        return output_file

    def mask_attack_smart(self, hash_file, hash_type, pattern=None):
        """Smart mask attack based on pattern analysis"""
        self.log("Smart mask attack", "INFO")

        hash_mode = self.hash_types.get(hash_type.lower(), 1000)
        output_file = self.cracked_dir / f"mask_cracked_{int(datetime.now().timestamp())}.txt"

        # Common password patterns
        patterns = pattern or [
            '?u?l?l?l?l?d?d?d?d',     # Uppercase + lowercase + digits
            '?l?l?l?l?l?l?d?d',       # 6 letters + 2 digits
            '?l?l?l?l?d?d?d?d',       # 4 letters + 4 digits
            '?d?d?d?d?d?d?d?d',       # 8 digits
            '?u?l?l?l?l?l?d?d!',      # Word + digits + !
            '?u?l?l?l?l?l?l?l?d?d',   # Capital + 7 letters + 2 digits
        ]

        for mask in patterns:
            self.log(f"Trying mask: {mask}", "INFO")

            cmd = f"hashcat -m {hash_mode} {hash_file} -a 3 {mask} -o {output_file} --force"
            os.system(cmd)

            if output_file.exists():
                with open(output_file, 'r') as f:
                    if f.read().strip():
                        self.log(f"Cracked with mask: {mask}", "SUCCESS")
                        return output_file

        return output_file

    def hybrid_attack(self, hash_file, hash_type):
        """Hybrid dictionary + mask attack"""
        self.log("Hybrid attack (dictionary + mask)", "INFO")

        hash_mode = self.hash_types.get(hash_type.lower(), 1000)
        output_file = self.cracked_dir / f"hybrid_cracked_{int(datetime.now().timestamp())}.txt"
        wordlist = self.wordlists_dir / "rockyou.txt"

        # Dictionary + appended digits
        self.log("Dictionary + appended mask", "INFO")
        cmd = f"hashcat -m {hash_mode} {hash_file} -a 6 {wordlist} ?d?d?d?d -o {output_file} --force"
        os.system(cmd)

        # Prepended mask + dictionary
        self.log("Prepended mask + dictionary", "INFO")
        cmd = f"hashcat -m {hash_mode} {hash_file} -a 7 ?d?d?d?d {wordlist} -o {output_file} --force"
        os.system(cmd)

        return output_file

    def prince_attack(self, hash_file, hash_type):
        """PRINCE attack (probability infinite chained elements)"""
        self.log("PRINCE attack", "INFO")

        hash_mode = self.hash_types.get(hash_type.lower(), 1000)
        output_file = self.cracked_dir / f"prince_cracked_{int(datetime.now().timestamp())}.txt"
        wordlist = self.wordlists_dir / "rockyou.txt"

        cmd = f"hashcat -m {hash_mode} {hash_file} --attack-mode 1 {wordlist} {wordlist} -o {output_file} --force"
        os.system(cmd)

        return output_file

    def distributed_crack(self, hash_file, hash_type, nodes):
        """Distributed hash cracking across multiple machines"""
        self.log("Setting up distributed cracking...", "INFO")

        # This would distribute the keyspace across nodes
        # For now, just split the wordlist

        hash_mode = self.hash_types.get(hash_type.lower(), 1000)
        wordlist = self.wordlists_dir / "rockyou.txt"

        # Split wordlist
        lines_per_node = subprocess.run(['wc', '-l', str(wordlist)],
                                      capture_output=True,
                                      text=True).stdout.split()[0]
        lines_per_node = int(int(lines_per_node) / len(nodes))

        for idx, node in enumerate(nodes):
            start = idx * lines_per_node
            end = (idx + 1) * lines_per_node

            self.log(f"Node {node}: lines {start} to {end}", "INFO")

            # Would SSH to node and run hashcat with skip/limit

    def benchmark(self):
        """Run hashcat benchmark"""
        self.log("Running hashcat benchmark...", "INFO")
        os.system("hashcat -b")

    def show_cracked(self, hash_file):
        """Show previously cracked hashes"""
        self.log("Displaying cracked hashes...", "INFO")
        os.system(f"hashcat --show {hash_file}")

    def export_potfile(self):
        """Export hashcat potfile"""
        potfile = Path.home() / ".hashcat/hashcat.potfile"

        if potfile.exists():
            export_file = self.cracked_dir / f"exported_potfile_{int(datetime.now().timestamp())}.txt"
            os.system(f"cp {potfile} {export_file}")
            self.log(f"Potfile exported to: {export_file}", "SUCCESS")
            return export_file
        else:
            self.log("No potfile found", "WARNING")
            return None

    def stats_report(self, hash_file):
        """Generate cracking statistics"""
        self.log("Generating statistics...", "INFO")
        os.system(f"hashcat --status {hash_file}")

    def auto_crack_multiple_types(self, hash_file):
        """Try cracking with multiple hash types"""
        self.log("Attempting auto-detection and multi-type cracking", "INFO")

        common_types = ['ntlm', 'md5', 'sha1', 'sha256']
        output_file = self.cracked_dir / f"multi_type_{int(datetime.now().timestamp())}.txt"
        wordlist = self.wordlists_dir / "rockyou.txt"

        for hash_type in common_types:
            self.log(f"Trying as {hash_type}...", "INFO")

            hash_mode = self.hash_types[hash_type]
            cmd = f"hashcat -m {hash_mode} {hash_file} {wordlist} -o {output_file} --force"

            os.system(cmd)

            if output_file.exists():
                with open(output_file, 'r') as f:
                    if f.read().strip():
                        self.log(f"Successfully cracked as {hash_type}!", "SUCCESS")
                        return output_file

        return None
