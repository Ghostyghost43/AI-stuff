#!/usr/bin/env python3
"""
Advanced Wordlist Generator with OSINT Capabilities
====================================================
Generate targeted wordlists based on:
- Target profiling (Q&A)
- Social media scraping (Facebook, Instagram, Twitter, LinkedIn)
- Built-in modern password patterns
- Mutations and variations

AUTHORIZED USE ONLY - For penetration testing and security research.
"""

import os
import sys
import re
import itertools
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import json


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class WordlistGenerator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.profile = {}
        self.words = set()
        self.output_dir = Path.home() / "wifi_captures" / "wordlists"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message, level="INFO"):
        """Print formatted log messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": Colors.OKBLUE,
            "SUCCESS": Colors.OKGREEN,
            "WARNING": Colors.WARNING,
            "ERROR": Colors.FAIL,
        }
        color = colors.get(level, Colors.ENDC)
        print(f"{color}[{timestamp}] [{level}] {message}{Colors.ENDC}")

    def get_built_in_wordlists(self):
        """Generate built-in modern password patterns"""
        self.log("Generating built-in modern password patterns...", "INFO")

        patterns = []

        # Common password patterns (2024)
        common_passwords = [
            "password", "Password", "PASSWORD",
            "password123", "Password123", "PASSWORD123",
            "admin", "Admin", "ADMIN",
            "admin123", "Admin123",
            "welcome", "Welcome", "WELCOME",
            "welcome123", "Welcome123",
            "qwerty", "Qwerty", "QWERTY",
            "qwerty123", "Qwerty123",
            "letmein", "LetMeIn", "LETMEIN",
            "monkey", "Monkey",
            "dragon", "Dragon",
            "master", "Master",
            "sunshine", "Sunshine",
            "princess", "Princess",
            "football", "Football",
            "shadow", "Shadow",
            "michael", "Michael",
            "jennifer", "Jennifer",
            "computer", "Computer",
            "trustno1", "Trustno1",
        ]

        # Years (common in passwords)
        current_year = datetime.now().year
        years = [str(y) for y in range(1990, current_year + 1)]

        # Seasons and months
        seasons = ["spring", "summer", "autumn", "fall", "winter",
                   "Spring", "Summer", "Autumn", "Fall", "Winter"]
        months = ["january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november", "december",
                  "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December",
                  "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Tech/WiFi related
        wifi_related = [
            "wifi", "WiFi", "WIFI", "wireless", "Wireless", "WIRELESS",
            "router", "Router", "ROUTER", "internet", "Internet", "INTERNET",
            "network", "Network", "NETWORK", "password", "Password", "PASSWORD",
            "admin", "Admin", "ADMIN", "user", "User", "USER",
            "guest", "Guest", "GUEST", "private", "Private", "PRIVATE",
        ]

        # Common symbols and patterns
        symbols = ["!", "@", "#", "$", "*", ".", "_", "-"]
        numbers = ["1", "12", "123", "1234", "12345", "123456"]

        patterns.extend(common_passwords)
        patterns.extend([w + y for w in ["password", "admin", "wifi", "Welcome"] for y in years[-5:]])
        patterns.extend([w + n for w in wifi_related for n in numbers[:4]])
        patterns.extend([s + y for s in seasons for y in years[-3:]])
        patterns.extend([m + y for m in months[:12] for y in years[-3:]])

        # Add symbols
        for word in common_passwords[:10]:
            for sym in symbols[:4]:
                patterns.append(word + sym)
                patterns.append(word + "123" + sym)

        self.words.update(patterns)
        self.log(f"Generated {len(patterns)} built-in patterns", "SUCCESS")

    def profile_target(self):
        """Interactive target profiling through Q&A"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print("Target Profiling - Answer questions to generate custom wordlist")
        print(f"{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.WARNING}Press Enter to skip any question{Colors.ENDC}\n")

        questions = [
            ("first_name", "Target's first name"),
            ("last_name", "Target's last name"),
            ("nickname", "Target's nickname"),
            ("spouse_name", "Spouse/partner name"),
            ("child_name", "Children's names (comma separated)"),
            ("pet_name", "Pet names (comma separated)"),
            ("birth_year", "Birth year"),
            ("birth_month", "Birth month (e.g., January or 01)"),
            ("birth_day", "Birth day"),
            ("company", "Company/workplace name"),
            ("job_title", "Job title"),
            ("address", "Street name/address"),
            ("city", "City"),
            ("state", "State/Province"),
            ("zip", "ZIP/Postal code"),
            ("phone", "Phone number (last 4 digits)"),
            ("favorite_team", "Favorite sports team"),
            ("favorite_color", "Favorite color"),
            ("favorite_food", "Favorite food"),
            ("hobbies", "Hobbies/interests (comma separated)"),
            ("school", "School/university name"),
            ("grad_year", "Graduation year"),
            ("car_model", "Car make/model"),
            ("keywords", "Other keywords (comma separated)"),
        ]

        for key, question in questions:
            answer = input(f"{Colors.OKBLUE}{question}: {Colors.ENDC}").strip()
            if answer:
                if ',' in answer:
                    self.profile[key] = [a.strip() for a in answer.split(',')]
                else:
                    self.profile[key] = answer

        self.log(f"Collected {len(self.profile)} profile fields", "SUCCESS")

    def scrape_social_media(self, url):
        """Scrape public social media profiles for keywords"""
        self.log(f"Attempting to scrape: {url}", "INFO")

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract text content
                text = soup.get_text()

                # Extract common keywords (names, dates, places)
                # Look for capitalized words (potential names)
                words = re.findall(r'\b[A-Z][a-z]+\b', text)

                # Look for years
                years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)

                # Look for hashtags
                hashtags = re.findall(r'#(\w+)', text)

                # Add to profile
                if 'scraped_words' not in self.profile:
                    self.profile['scraped_words'] = []

                self.profile['scraped_words'].extend(words[:50])  # Limit to 50
                self.profile['scraped_years'] = years
                self.profile['scraped_hashtags'] = hashtags

                self.log(f"Extracted {len(words)} keywords, {len(years)} years, {len(hashtags)} hashtags", "SUCCESS")
                return True

            else:
                self.log(f"Failed to fetch URL (status: {response.status_code})", "WARNING")
                return False

        except Exception as e:
            self.log(f"Scraping error: {e}", "ERROR")
            return False

    def social_media_osint(self):
        """Gather OSINT from social media"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print("Social Media OSINT")
        print(f"{'='*70}{Colors.ENDC}\n")

        print("Enter URLs to scrape (Facebook, Instagram, Twitter, LinkedIn, etc.)")
        print(f"{Colors.WARNING}Note: Many sites require authentication. Public profiles work best.{Colors.ENDC}")
        print("Press Enter without URL when done.\n")

        while True:
            url = input(f"{Colors.OKBLUE}URL: {Colors.ENDC}").strip()

            if not url:
                break

            if url.startswith('http'):
                self.scrape_social_media(url)
            else:
                print(f"{Colors.FAIL}Invalid URL{Colors.ENDC}")

    def generate_mutations(self, word):
        """Generate common password mutations for a word"""
        mutations = set()

        # Original
        mutations.add(word)
        mutations.add(word.lower())
        mutations.add(word.upper())
        mutations.add(word.capitalize())

        # Leet speak
        leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'l': ['1'],
            'g': ['9'],
        }

        leet_word = word.lower()
        for char, replacements in leet_map.items():
            for repl in replacements:
                leet_word = leet_word.replace(char, repl)
        mutations.add(leet_word)

        # Common suffixes
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 5, current_year + 1)]
        numbers = ["1", "12", "123", "1234", "!", "!!", "@", "#", "$"]

        for suffix in years + numbers:
            mutations.add(word + suffix)
            mutations.add(word.capitalize() + suffix)
            mutations.add(word.lower() + suffix)

        # Common prefixes
        for prefix in ["!", "@", "#", "1", "12"]:
            mutations.add(prefix + word)
            mutations.add(prefix + word.capitalize())

        # Reverse
        mutations.add(word[::-1])

        # Double
        mutations.add(word + word)
        mutations.add(word + word.capitalize())

        return mutations

    def generate_combinations(self):
        """Generate combinations from profile data"""
        self.log("Generating combinations from profile data...", "INFO")

        # Extract all words from profile
        all_words = []

        for key, value in self.profile.items():
            if isinstance(value, list):
                all_words.extend(value)
            else:
                all_words.append(value)

        # Clean and filter
        all_words = [w.strip() for w in all_words if w and isinstance(w, str)]

        # Generate mutations for each word
        for word in all_words:
            if len(word) >= 3:
                mutations = self.generate_mutations(word)
                self.words.update(mutations)

        # Generate combinations
        # Two word combinations
        if len(all_words) >= 2:
            for i, word1 in enumerate(all_words[:10]):  # Limit to prevent explosion
                for word2 in all_words[:10]:
                    if word1 != word2:
                        combo = word1 + word2
                        self.words.update(self.generate_mutations(combo))

                        # With numbers
                        for num in ["1", "12", "123", "1234"]:
                            self.words.add(word1 + word2 + num)
                            self.words.add(word1 + num + word2)

        # Name + year combinations
        names = []
        for key in ['first_name', 'last_name', 'nickname']:
            if key in self.profile:
                names.append(self.profile[key])

        years = []
        if 'birth_year' in self.profile:
            years.append(self.profile['birth_year'])
            years.append(self.profile['birth_year'][-2:])  # Last 2 digits
        if 'grad_year' in self.profile:
            years.append(self.profile['grad_year'])

        for name in names:
            for year in years:
                self.words.add(name + year)
                self.words.add(name.capitalize() + year)
                self.words.add(name + "@" + year)
                self.words.add(name + year + "!")

        self.log(f"Generated {len(self.words)} total password candidates", "SUCCESS")

    def add_common_patterns(self):
        """Add common WiFi password patterns"""
        patterns = [
            # Router defaults
            "admin", "Admin", "ADMIN",
            "password", "Password", "PASSWORD",
            "1234567890", "0987654321",
            "admin123", "Admin123",
            "root", "Root",
            "toor",

            # WiFi specific
            "wifi", "WiFi", "WIFI",
            "wireless", "Wireless",
            "router", "Router",
            "internet", "Internet",
            "network", "Network",

            # Phone number patterns
            *[str(i) * 8 for i in range(10)],  # 11111111, 22222222, etc.
        ]

        # Add location-based if available
        if 'address' in self.profile:
            addr = self.profile['address']
            self.words.update(self.generate_mutations(addr))

        if 'zip' in self.profile:
            zip_code = self.profile['zip']
            self.words.add(zip_code)
            self.words.add(zip_code * 2)

        if 'phone' in self.profile:
            phone = self.profile['phone']
            self.words.add(phone)
            self.words.add(phone * 2)

        self.words.update(patterns)

    def save_wordlist(self, filename=None):
        """Save generated wordlist to file"""
        if not self.words:
            self.log("No words to save!", "WARNING")
            return None

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.output_dir / f"custom_wordlist_{timestamp}.txt"
        else:
            filename = self.output_dir / filename

        # Sort by length and complexity (longer, more complex first)
        sorted_words = sorted(self.words, key=lambda x: (len(x), sum(c.isdigit() for c in x)), reverse=True)

        with open(filename, 'w') as f:
            for word in sorted_words:
                f.write(word + '\n')

        self.log(f"Wordlist saved: {filename}", "SUCCESS")
        self.log(f"Total passwords: {len(sorted_words)}", "INFO")

        return str(filename)

    def interactive_menu(self):
        """Main interactive menu"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("=" * 70)
        print("Advanced Wordlist Generator with OSINT".center(70))
        print("=" * 70)
        print(f"{Colors.ENDC}\n")

        while True:
            print(f"\n{Colors.HEADER}Options:{Colors.ENDC}")
            print("  [1] Target profiling (Q&A)")
            print("  [2] Social media OSINT")
            print("  [3] Add built-in modern patterns")
            print("  [4] Generate wordlist")
            print("  [5] Save wordlist")
            print("  [6] Exit")

            choice = input(f"\n{Colors.OKBLUE}Select option [1-6]: {Colors.ENDC}").strip()

            if choice == '1':
                self.profile_target()
            elif choice == '2':
                self.social_media_osint()
            elif choice == '3':
                self.get_built_in_wordlists()
            elif choice == '4':
                if self.profile:
                    self.generate_combinations()
                    self.add_common_patterns()
                else:
                    self.log("No profile data! Complete profiling first.", "WARNING")
            elif choice == '5':
                filename = self.save_wordlist()
                if filename:
                    use_it = input(f"\n{Colors.OKBLUE}Return this wordlist path? (y/n): {Colors.ENDC}")
                    if use_it.lower() == 'y':
                        return filename
            elif choice == '6':
                break
            else:
                print(f"{Colors.FAIL}Invalid option{Colors.ENDC}")

        return None

    def quick_generate(self, target_info=None):
        """Quick wordlist generation with minimal input"""
        self.log("Quick wordlist generation...", "INFO")

        if target_info:
            self.profile.update(target_info)

        # Always include built-in patterns
        self.get_built_in_wordlists()

        # Generate from profile if available
        if self.profile:
            self.generate_combinations()
            self.add_common_patterns()

        return self.save_wordlist()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Advanced Wordlist Generator with OSINT',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive mode')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='Quick mode (built-in patterns only)')
    parser.add_argument('-n', '--name', type=str,
                        help='Target name')
    parser.add_argument('-y', '--year', type=str,
                        help='Birth year')

    args = parser.parse_args()

    gen = WordlistGenerator()

    if args.interactive:
        gen.interactive_menu()
    elif args.quick:
        target_info = {}
        if args.name:
            target_info['first_name'] = args.name
        if args.year:
            target_info['birth_year'] = args.year

        filename = gen.quick_generate(target_info)
        print(f"\nWordlist generated: {filename}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
