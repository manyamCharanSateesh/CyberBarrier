import platform
import os
import subprocess
from urllib.parse import urlparse

class BlockerManager:
    def __init__(self):
        self.system = platform.system()
        if self.system == "Windows":
            self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            self.hosts_path = "/etc/hosts"
        self.redirect_ip = "127.0.0.1"
        self.redirect_ipv6 = "::1"
        self.website_list = []
        
        # Mapping of common sites to their alternative/related domains for better blocking
        self.common_alt_domains = {
            "youtube.com": ["youtu.be", "m.youtube.com", "music.youtube.com"],
            "facebook.com": ["fb.com", "m.facebook.com"],
            "twitter.com": ["t.co", "x.com"],
            "instagram.com": ["instagr.am"],
            "reddit.com": ["redd.it", "old.reddit.com"],
            "linkedin.com": ["lnkd.in"]
        }

    def get_blocked_sites(self):
        """Reads the hosts file and returns a list of blocked websites."""
        blocked_sites = []
        if not os.path.exists(self.hosts_path):
            return blocked_sites

        try:
            with open(self.hosts_path, 'r') as file:
                content = file.read()
                for line in content.splitlines():
                    if (self.redirect_ip in line or self.redirect_ipv6 in line) and not line.strip().startswith("#"):
                        parts = line.split()
                        if len(parts) >= 2:
                            site = parts[1]
                            if site != "localhost" and site not in blocked_sites:
                                blocked_sites.append(site)
        except PermissionError:
            print("Permission denied: Run as Administrator to read hosts file.")
        return blocked_sites

    def _extract_hostname(self, url):
        """Extracts the hostname from a URL."""
        if not url:
            return None
        url = url.strip()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc
            # Remove www. prefix if present for cleaner storage/logic, 
            # though we will block both anyway.
            if hostname.startswith("www."):
                hostname = hostname[4:]
            return hostname
        except Exception:
            return None

    def block_site(self, website):
        """Blocks a website by adding it to the hosts file."""
        hostname = self._extract_hostname(website)
        if not hostname:
            return False
        
        # Block both bare domain and www subdomain
        sites_to_block = [hostname, f"www.{hostname}"]
        
        # Check for related domains
        if hostname in self.common_alt_domains:
            for alt in self.common_alt_domains[hostname]:
                sites_to_block.append(alt)
                if not alt.startswith("www.") and alt.count(".") == 1: # naive check for adding www to alts
                     sites_to_block.append(f"www.{alt}")
        
        current_blocked = self.get_blocked_sites()
        
        try:
            with open(self.hosts_path, 'a') as file:
                for site in sites_to_block:
                    # Check if already present to avoid duplicates
                    # (Simple check against what we read)
                    if site not in current_blocked:
                        file.write(f"{self.redirect_ip} {site}\n")
                        file.write(f"{self.redirect_ipv6} {site}\n")
            self._flush_dns()
            return True
        except PermissionError:
            print("Permission denied: Run as Administrator to write to hosts file.")
            return False

    def unblock_site(self, website):
        """Unblocks a website by removing it from the hosts file."""
        # Clean the input in case they passed a full URL
        hostname = self._extract_hostname(website)
        # If extraction failed (maybe because it was already just 'instagram.com'), try using raw
        if not hostname: 
             hostname = website.strip()

        sites_to_unblock = [hostname, f"www.{hostname}"]
        
        # Also unblock related domains if they exist
        if hostname in self.common_alt_domains:
             for alt in self.common_alt_domains[hostname]:
                sites_to_unblock.append(alt)
                if not alt.startswith("www.") and alt.count(".") == 1:
                     sites_to_unblock.append(f"www.{alt}")
        
        try:
            with open(self.hosts_path, 'r') as file:
                lines = file.readlines()
            
            with open(self.hosts_path, 'w') as file:
                for line in lines:
                    should_remove = False
                    for site in sites_to_unblock:
                        # Check for IP + hostname match
                        if (self.redirect_ip in line or self.redirect_ipv6 in line) and site in line:
                            # Verify it's match. We handle the case where the existing file has a trailing slash.
                            parts = line.split()
                            if len(parts) >= 2:
                                existing_site = parts[1]
                                # Clean up existing site (remove trailing slash if present) for comparison
                                if existing_site.rstrip('/') == site:
                                    should_remove = True
                                    break
                    
                    if not should_remove:
                        file.write(line)
            self._flush_dns()
            return True
        except PermissionError:
            print("Permission denied: Run as Administrator to write to hosts file.")
            return False

    def _flush_dns(self):
        """Flushes the DNS cache."""
        try:
            if self.system == "Windows":
                subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Linux/Mac commands vary, omitted for this specific Windows request but good to keep in mind
        except Exception as e:
            print(f"Failed to flush DNS: {e}")
