#!/usr/bin/env python3
"""
Metasploit Database Connection Module
Automated MSF database setup, management, and querying
"""

import os
import subprocess
import json
from pathlib import Path

class MSFDatabase:
    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.db_config = Path.home() / ".msf4/database.yml"

    def check_postgres(self):
        """Check if PostgreSQL is running"""
        result = subprocess.run(['systemctl', 'is-active', 'postgresql'],
                              capture_output=True, text=True)
        return result.stdout.strip() == 'active'

    def start_postgres(self):
        """Start PostgreSQL service"""
        self.log("Starting PostgreSQL...", "INFO")
        os.system("systemctl start postgresql")
        os.system("systemctl enable postgresql")

        if self.check_postgres():
            self.log("PostgreSQL started successfully", "SUCCESS")
            return True
        else:
            self.log("Failed to start PostgreSQL", "ERROR")
            return False

    def init_msf_db(self):
        """Initialize Metasploit database"""
        self.log("Initializing Metasploit database...", "INFO")

        # Start PostgreSQL
        if not self.check_postgres():
            self.start_postgres()

        # Initialize database
        result = subprocess.run(['msfdb', 'init'], capture_output=True, text=True)

        if result.returncode == 0:
            self.log("Metasploit database initialized", "SUCCESS")
            return True
        else:
            self.log(f"Database initialization failed: {result.stderr}", "ERROR")
            return False

    def reinit_msf_db(self):
        """Reinitialize (delete and recreate) MSF database"""
        self.log("WARNING: This will delete all MSF data!", "WARNING")
        confirm = input("Are you sure? (yes/no): ")

        if confirm.lower() == 'yes':
            self.log("Deleting and reinitializing database...", "INFO")
            os.system("msfdb delete")
            os.system("msfdb init")
            self.log("Database reinitialized", "SUCCESS")
        else:
            self.log("Operation cancelled", "INFO")

    def check_db_status(self):
        """Check MSF database status"""
        self.log("Checking database status...", "INFO")
        os.system("msfdb status")

    def connect_to_db(self):
        """Test database connection"""
        self.log("Testing database connection...", "INFO")

        test_script = """
db_status
exit
"""
        result = subprocess.run(['msfconsole', '-q', '-x', test_script],
                              capture_output=True, text=True)

        if 'Connected to' in result.stdout:
            self.log("Database connection successful!", "SUCCESS")
            return True
        else:
            self.log("Database connection failed", "ERROR")
            return False

    def import_nmap_scan(self, xml_file):
        """Import nmap scan into MSF database"""
        if not Path(xml_file).exists():
            self.log(f"File not found: {xml_file}", "ERROR")
            return False

        self.log(f"Importing {xml_file} into MSF database...", "INFO")

        rc_script = f"""
db_import {xml_file}
hosts
services
exit
"""
        os.system(f"msfconsole -q -x '{rc_script}'")

    def query_hosts(self):
        """Query all hosts in database"""
        self.log("Querying hosts from database...", "INFO")

        rc_script = """
hosts -c address,name,os_name,os_flavor
exit
"""
        os.system(f"msfconsole -q -x '{rc_script}'")

    def query_services(self, port=None):
        """Query services in database"""
        self.log("Querying services from database...", "INFO")

        if port:
            rc_script = f"services -p {port}\nexit\n"
        else:
            rc_script = "services -c port,proto,name,info\nexit\n"

        os.system(f"msfconsole -q -x '{rc_script}'")

    def query_vulns(self):
        """Query vulnerabilities in database"""
        self.log("Querying vulnerabilities...", "INFO")
        os.system("msfconsole -q -x 'vulns; exit'")

    def query_creds(self):
        """Query captured credentials"""
        self.log("Querying credentials...", "INFO")
        os.system("msfconsole -q -x 'creds; exit'")

    def query_loot(self):
        """Query collected loot"""
        self.log("Querying loot...", "INFO")
        os.system("msfconsole -q -x 'loot; exit'")

    def export_data(self, format='xml'):
        """Export database data"""
        output_file = f"/tmp/msf_export_{int(__import__('time').time())}.{format}"

        self.log(f"Exporting database to {output_file}...", "INFO")

        if format == 'xml':
            os.system(f"msfconsole -q -x 'db_export -f xml {output_file}; exit'")
        elif format == 'json':
            os.system(f"msfconsole -q -x 'db_export -f json {output_file}; exit'")

        self.log(f"Export complete: {output_file}", "SUCCESS")
        return output_file

    def workspace_create(self, name):
        """Create new workspace"""
        self.log(f"Creating workspace: {name}", "INFO")
        os.system(f"msfconsole -q -x 'workspace -a {name}; exit'")

    def workspace_list(self):
        """List all workspaces"""
        self.log("Listing workspaces...", "INFO")
        os.system("msfconsole -q -x 'workspace; exit'")

    def workspace_switch(self, name):
        """Switch to workspace"""
        self.log(f"Switching to workspace: {name}", "INFO")
        os.system(f"msfconsole -q -x 'workspace {name}; exit'")

    def auto_setup(self):
        """Automated complete database setup"""
        self.log("Running automated MSF database setup...", "INFO")

        # 1. Check/start PostgreSQL
        if not self.check_postgres():
            self.start_postgres()

        # 2. Initialize MSF database
        self.init_msf_db()

        # 3. Test connection
        if self.connect_to_db():
            self.log("MSF database setup complete!", "SUCCESS")
            return True
        else:
            self.log("Setup failed, trying reinit...", "WARNING")
            self.reinit_msf_db()
            return self.connect_to_db()

    def backup_database(self):
        """Backup MSF database"""
        backup_file = f"/tmp/msf_backup_{int(__import__('time').time())}.sql"

        self.log(f"Backing up database to {backup_file}...", "INFO")
        os.system(f"sudo -u postgres pg_dump msf > {backup_file}")

        self.log(f"Backup complete: {backup_file}", "SUCCESS")
        return backup_file

    def restore_database(self, backup_file):
        """Restore MSF database from backup"""
        if not Path(backup_file).exists():
            self.log(f"Backup file not found: {backup_file}", "ERROR")
            return False

        self.log(f"Restoring database from {backup_file}...", "INFO")
        os.system(f"sudo -u postgres psql msf < {backup_file}")

        self.log("Restore complete", "SUCCESS")
        return True
