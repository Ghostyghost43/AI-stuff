"""
Hash Cracking Module
Supports hashcat, John the Ripper, and various hash types
"""

import subprocess
import os
import re
import time
from typing import Dict, Callable


class HashCracker:
    """Hash cracking functionality"""

    def __init__(self):
        self.is_running = False
        self.cracked_hashes = []

    # Hash type mapping for hashcat
    HASH_TYPES = {
        "WPA/WPA2 (22000)": "22000",
        "NTLM (1000)": "1000",
        "MD5 (0)": "0",
        "SHA1 (100)": "100",
        "SHA256 (1400)": "1400",
        "bcrypt (3200)": "3200",
        "NetNTLMv2 (5600)": "5600",
        "Kerberos TGS-REP (13100)": "13100"
    }

    def crack(self, hash_data: str, hash_type: str, wordlist: str,
             attack_mode: str, tool: str = "Hashcat (GPU)",
             callback: Callable = None, progress_callback: Callable = None) -> Dict:
        """
        Crack hashes

        Args:
            hash_data: Hash string or file path
            hash_type: Type of hash
            wordlist: Wordlist file path
            attack_mode: Attack mode (dictionary, brute force, etc.)
            tool: Tool to use (hashcat or john)
            callback: Status callback
            progress_callback: Progress callback

        Returns:
            Cracking results
        """
        self.is_running = True
        results = {
            'success': False,
            'hash_type': hash_type,
            'attack_mode': attack_mode,
            'tool': tool,
            'password': None
        }

        if callback:
            callback(f"[CRACK] Starting {tool} attack")
            callback(f"[CRACK] Hash type: {hash_type}")
            callback(f"[CRACK] Attack mode: {attack_mode}")

        try:
            # Write hash to temp file if it's not a file already
            if os.path.exists(hash_data):
                hash_file = hash_data
            else:
                hash_file = f"/tmp/hash_{int(time.time())}.txt"
                with open(hash_file, 'w') as f:
                    f.write(hash_data)

            if progress_callback:
                progress_callback(10)

            if "Hashcat" in tool:
                results = self._crack_with_hashcat(hash_file, hash_type,
                                                   wordlist, attack_mode,
                                                   callback, progress_callback)
            else:
                results = self._crack_with_john(hash_file, hash_type,
                                               wordlist, attack_mode,
                                               callback, progress_callback)

            if results.get('success'):
                self.cracked_hashes.append(results)

        except Exception as e:
            results['error'] = str(e)
            if callback:
                callback(f"[ERROR] {str(e)}")

        self.is_running = False
        return results

    def _crack_with_hashcat(self, hash_file: str, hash_type: str,
                           wordlist: str, attack_mode: str,
                           callback: Callable = None,
                           progress_callback: Callable = None) -> Dict:
        """Crack with hashcat"""
        results = {'success': False, 'tool': 'hashcat'}

        # Get hash mode number
        hash_mode = self.HASH_TYPES.get(hash_type, "0")

        if callback:
            callback(f"[HASHCAT] Hash mode: {hash_mode}")

        # Build command based on attack mode
        if attack_mode == "Dictionary Attack":
            cmd = f"hashcat -m {hash_mode} -a 0 {hash_file} {wordlist} --force"

        elif attack_mode == "Brute Force":
            # Brute force with mask attack
            cmd = f"hashcat -m {hash_mode} -a 3 {hash_file} ?a?a?a?a?a?a?a?a --force"

        elif attack_mode == "Combinator":
            cmd = f"hashcat -m {hash_mode} -a 1 {hash_file} {wordlist} {wordlist} --force"

        elif attack_mode == "Hybrid (Dict + Mask)":
            cmd = f"hashcat -m {hash_mode} -a 6 {hash_file} {wordlist} ?d?d?d?d --force"

        elif attack_mode == "Rule-based":
            # Use best64 rules
            rules_file = "/usr/share/hashcat/rules/best64.rule"
            if not os.path.exists(rules_file):
                rules_file = "/usr/share/doc/hashcat/rules/best64.rule"
            cmd = f"hashcat -m {hash_mode} -a 0 {hash_file} {wordlist} -r {rules_file} --force"

        else:
            cmd = f"hashcat -m {hash_mode} -a 0 {hash_file} {wordlist} --force"

        # Add show option to display cracked passwords
        cmd += " --show"

        if callback:
            callback(f"[HASHCAT] {cmd}")

        if progress_callback:
            progress_callback(30)

        try:
            # Run hashcat
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            if progress_callback:
                progress_callback(80)

            # Parse output for cracked password
            output = result.stdout + result.stderr

            if callback:
                # Show some progress
                lines = output.split('\n')
                for line in lines[-10:]:  # Last 10 lines
                    if line.strip():
                        callback(f"[HASHCAT] {line[:100]}")

            # Look for cracked password
            # Format varies by hash type
            password = None

            # WPA/WPA2 format: hash:ssid:password
            if hash_mode == "22000":
                match = re.search(r':([^:]+)$', output)
                if match:
                    password = match.group(1)

            # Most formats: hash:password
            else:
                if ':' in output:
                    lines = output.split('\n')
                    for line in lines:
                        if ':' in line and not line.startswith('#'):
                            parts = line.split(':')
                            if len(parts) >= 2:
                                password = parts[-1].strip()
                                break

            if password:
                results['success'] = True
                results['password'] = password
                if callback:
                    callback(f"[SUCCESS] Password cracked: {password}")
            else:
                if callback:
                    callback("[FAILED] Password not found")

            if progress_callback:
                progress_callback(100)

        except subprocess.TimeoutExpired:
            if callback:
                callback("[TIMEOUT] Hashcat timed out")
            results['error'] = 'Timeout'

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            results['error'] = str(e)

        return results

    def _crack_with_john(self, hash_file: str, hash_type: str,
                        wordlist: str, attack_mode: str,
                        callback: Callable = None,
                        progress_callback: Callable = None) -> Dict:
        """Crack with John the Ripper"""
        results = {'success': False, 'tool': 'john'}

        # Determine john format
        john_formats = {
            "NTLM (1000)": "nt",
            "MD5 (0)": "raw-md5",
            "SHA1 (100)": "raw-sha1",
            "SHA256 (1400)": "raw-sha256",
            "bcrypt (3200)": "bcrypt",
            "NetNTLMv2 (5600)": "netntlmv2",
        }

        john_format = john_formats.get(hash_type, "")

        if callback:
            callback(f"[JOHN] Format: {john_format}")

        # Build command
        if john_format:
            cmd = f"john --format={john_format} --wordlist={wordlist} {hash_file}"
        else:
            cmd = f"john --wordlist={wordlist} {hash_file}"

        if progress_callback:
            progress_callback(30)

        try:
            # Run John
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600
            )

            if progress_callback:
                progress_callback(70)

            # Show cracked passwords
            show_cmd = f"john --show {hash_file}"
            show_result = subprocess.run(
                show_cmd,
                shell=True,
                capture_output=True,
                text=True
            )

            if callback:
                callback(f"[JOHN] {show_result.stdout}")

            # Parse output
            if ':' in show_result.stdout:
                lines = show_result.stdout.split('\n')
                for line in lines:
                    if ':' in line and 'password hash' not in line.lower():
                        parts = line.split(':')
                        if len(parts) >= 2:
                            password = parts[1].strip()
                            results['success'] = True
                            results['password'] = password
                            if callback:
                                callback(f"[SUCCESS] Password cracked: {password}")
                            break

            if not results['success'] and callback:
                callback("[FAILED] Password not found")

            if progress_callback:
                progress_callback(100)

        except subprocess.TimeoutExpired:
            if callback:
                callback("[TIMEOUT] John timed out")
            results['error'] = 'Timeout'

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            results['error'] = str(e)

        return results

    def benchmark(self, callback: Callable = None) -> Dict:
        """Run hashcat benchmark"""
        if callback:
            callback("[BENCHMARK] Running hashcat benchmark...")

        try:
            cmd = "hashcat -b --force"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )

            if callback:
                lines = result.stdout.split('\n')
                for line in lines[:20]:  # First 20 lines
                    if line.strip():
                        callback(f"[BENCHMARK] {line}")

            return {'success': True, 'output': result.stdout}

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}

    def stop(self):
        """Stop cracking"""
        self.is_running = False
        # Kill hashcat/john processes
        subprocess.run("killall hashcat john", shell=True, capture_output=True)

    def get_wordlist_info(self, wordlist: str) -> Dict:
        """Get information about wordlist"""
        try:
            # Count lines
            result = subprocess.run(
                f"wc -l {wordlist}",
                shell=True,
                capture_output=True,
                text=True
            )

            count = int(result.stdout.split()[0])

            # Get file size
            size = os.path.getsize(wordlist)
            size_mb = size / (1024 * 1024)

            return {
                'path': wordlist,
                'count': count,
                'size_mb': round(size_mb, 2)
            }

        except Exception:
            return {'path': wordlist, 'error': 'Could not read wordlist'}

    def generate_wordlist(self, output_file: str, min_len: int = 8,
                         max_len: int = 12, charset: str = "alnum",
                         callback: Callable = None) -> Dict:
        """Generate wordlist using crunch"""
        if callback:
            callback(f"[CRUNCH] Generating wordlist {min_len}-{max_len} chars")

        try:
            cmd = f"crunch {min_len} {max_len} -o {output_file}"

            if charset == "alnum":
                cmd += " -t @@@@@@@@"
            elif charset == "alpha":
                cmd += " abcdefghijklmnopqrstuvwxyz"
            elif charset == "numeric":
                cmd += " 0123456789"

            subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                timeout=300
            )

            if os.path.exists(output_file):
                if callback:
                    callback(f"[CRUNCH] Wordlist created: {output_file}")
                return {'success': True, 'file': output_file}
            else:
                return {'success': False}

        except Exception as e:
            if callback:
                callback(f"[ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}
