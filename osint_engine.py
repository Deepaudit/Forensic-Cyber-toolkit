#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         PABLO CYBER - OSINT FORENSICS ENGINE                ║
║         Open Source Intelligence via Public APIs            ║
╚══════════════════════════════════════════════════════════════╝
Author: PABLO CYBER
APIs: GitHub, HaveIBeenPwned, Gravatar, Crt.sh, HackerTarget
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import datetime
import argparse
import logging
import re
import os
import sys

log = logging.getLogger("PABLO_OSINT")
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


class OSINTForensics:
    """OSINT investigation using public APIs - PABLO CYBER"""

    GITHUB_API      = "https://api.github.com"
    CRTSH_API       = "https://crt.sh"
    HACKERTARGET    = "https://api.hackertarget.com"
    HAVEIBEENPWNED  = "https://haveibeenpwned.com/api/v3"
    GRAVATAR_API    = "https://www.gravatar.com"

    def __init__(self, github_token=None, hibp_key=None):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.hibp_key     = hibp_key     or os.environ.get("HIBP_KEY")

    def _get(self, url: str, headers: dict = None) -> dict | list | str:
        try:
            req = urllib.request.Request(url, headers=headers or {"User-Agent": "PABLO-CYBER-OSINT/2.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = resp.read().decode()
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
        except urllib.error.HTTPError as e:
            log.error(f"HTTP {e.code}: {url}")
            return {"error": f"HTTP {e.code}"}
        except Exception as e:
            log.error(f"Request failed: {e}")
            return {"error": str(e)}

    # ─── GITHUB OSINT ─────────────────────────────────────────
    def github_user_profile(self, username: str) -> dict:
        """Get complete GitHub user profile."""
        url     = f"{self.GITHUB_API}/users/{username}"
        headers = {"User-Agent": "PABLO-CYBER-OSINT"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        data = self._get(url, headers)
        log.info(f"[GITHUB] User: {username} → {data.get('name','?')} | repos: {data.get('public_repos','?')}")
        return data

    def github_user_repos(self, username: str, per_page: int = 50) -> list:
        """List all public repos for a GitHub user."""
        url     = f"{self.GITHUB_API}/users/{username}/repos?per_page={per_page}&sort=updated"
        headers = {"User-Agent": "PABLO-CYBER-OSINT"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        data = self._get(url, headers)
        if isinstance(data, list):
            repos = [{
                "name":        r.get("name"),
                "description": r.get("description"),
                "language":    r.get("language"),
                "stars":       r.get("stargazers_count"),
                "forks":       r.get("forks_count"),
                "updated":     r.get("updated_at"),
                "url":         r.get("html_url"),
                "topics":      r.get("topics", []),
            } for r in data]
            log.info(f"[GITHUB] {username}: {len(repos)} repos found")
            return repos
        return []

    def github_user_events(self, username: str) -> list:
        """Get recent public activity for a GitHub user."""
        url     = f"{self.GITHUB_API}/users/{username}/events/public?per_page=30"
        headers = {"User-Agent": "PABLO-CYBER-OSINT"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        data = self._get(url, headers)
        events = []
        if isinstance(data, list):
            for ev in data:
                events.append({
                    "type":       ev.get("type"),
                    "repo":       ev.get("repo", {}).get("name"),
                    "created_at": ev.get("created_at"),
                })
        log.info(f"[GITHUB] {username}: {len(events)} recent events")
        return events

    def github_search_code(self, query: str, per_page: int = 10) -> list:
        """Search GitHub code (useful for exposed secrets, credentials)."""
        url     = f"{self.GITHUB_API}/search/code?q={urllib.parse.quote(query)}&per_page={per_page}"
        headers = {"User-Agent": "PABLO-CYBER-OSINT", "Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        data = self._get(url, headers)
        results = []
        if isinstance(data, dict) and "items" in data:
            for item in data["items"]:
                results.append({
                    "name":       item.get("name"),
                    "path":       item.get("path"),
                    "repo":       item.get("repository", {}).get("full_name"),
                    "url":        item.get("html_url"),
                })
        log.info(f"[GITHUB] Code search '{query}': {len(results)} results")
        return results

    def github_org_members(self, org: str) -> list:
        """List public members of a GitHub organization."""
        url     = f"{self.GITHUB_API}/orgs/{org}/members?per_page=100"
        headers = {"User-Agent": "PABLO-CYBER-OSINT"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        data = self._get(url, headers)
        if isinstance(data, list):
            members = [{"login": m.get("login"), "url": m.get("html_url")} for m in data]
            log.info(f"[GITHUB] Org {org}: {len(members)} public members")
            return members
        return []

    # ─── CERTIFICATE TRANSPARENCY (crt.sh) ───────────────────
    def crtsh_domain_search(self, domain: str) -> list:
        """Search certificate transparency logs for domain subdomains."""
        url  = f"{self.CRTSH_API}/?q=%.{domain}&output=json"
        data = self._get(url)
        subdomains = set()

        if isinstance(data, list):
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.splitlines():
                    sub = sub.strip().lstrip("*.")
                    if domain in sub:
                        subdomains.add(sub)

        result = sorted(list(subdomains))
        log.info(f"[CRT.SH] {domain}: {len(result)} subdomains found")
        return result

    # ─── HACKERTARGET FREE APIs ───────────────────────────────
    def hackertarget_hostsearch(self, domain: str) -> list:
        """Find hosts for a domain using HackerTarget (free)."""
        url  = f"{self.HACKERTARGET}/hostsearch/?q={domain}"
        data = self._get(url)
        hosts = []
        if isinstance(data, str):
            for line in data.splitlines():
                if "," in line:
                    host, ip = line.split(",", 1)
                    hosts.append({"host": host.strip(), "ip": ip.strip()})
        log.info(f"[HACKERTARGET] {domain}: {len(hosts)} hosts")
        return hosts

    def hackertarget_reverse_ip(self, ip: str) -> list:
        """Find all domains hosted on an IP."""
        url  = f"{self.HACKERTARGET}/reverseiplookup/?q={ip}"
        data = self._get(url)
        domains = []
        if isinstance(data, str):
            domains = [d.strip() for d in data.splitlines() if d.strip()]
        log.info(f"[HACKERTARGET] {ip}: {len(domains)} domains")
        return domains

    def hackertarget_dns_lookup(self, domain: str) -> list:
        """Full DNS record lookup via HackerTarget."""
        url  = f"{self.HACKERTARGET}/dnslookup/?q={domain}"
        data = self._get(url)
        records = []
        if isinstance(data, str):
            for line in data.splitlines():
                if line.strip():
                    records.append(line.strip())
        log.info(f"[HACKERTARGET] DNS {domain}: {len(records)} records")
        return records

    def hackertarget_whois(self, domain: str) -> str:
        """WHOIS lookup via HackerTarget."""
        url  = f"{self.HACKERTARGET}/whois/?q={domain}"
        data = self._get(url)
        log.info(f"[WHOIS] {domain} queried")
        return data if isinstance(data, str) else json.dumps(data)

    def hackertarget_asn_lookup(self, ip: str) -> str:
        """ASN lookup for an IP."""
        url  = f"{self.HACKERTARGET}/aslookup/?q={ip}"
        data = self._get(url)
        log.info(f"[ASN] {ip}: {data}")
        return data if isinstance(data, str) else json.dumps(data)

    def hackertarget_traceroute(self, target: str) -> list:
        """Traceroute via HackerTarget API."""
        url  = f"{self.HACKERTARGET}/traceroute/?q={target}"
        data = self._get(url)
        hops = []
        if isinstance(data, str):
            hops = [h.strip() for h in data.splitlines() if h.strip()]
        return hops

    # ─── EMAIL INVESTIGATION ──────────────────────────────────
    def email_gravatar(self, email: str) -> dict:
        """Check Gravatar for profile info associated with an email."""
        import hashlib
        email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
        url  = f"{self.GRAVATAR_API}/{email_hash}.json"
        data = self._get(url)
        log.info(f"[GRAVATAR] {email}: {'found' if isinstance(data, dict) else 'not found'}")
        return data if isinstance(data, dict) else {"error": "No Gravatar profile found"}

    def haveibeenpwned(self, email: str) -> list:
        """Check if email was in known data breaches (requires HIBP API key)."""
        if not self.hibp_key:
            return [{"error": "HIBP API key required. Get one at haveibeenpwned.com/API/Key"}]

        url = f"{self.HAVEIBEENPWNED}/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false"
        headers = {
            "hibp-api-key": self.hibp_key,
            "User-Agent": "PABLO-CYBER-OSINT"
        }
        data = self._get(url, headers)
        if isinstance(data, list):
            log.info(f"[HIBP] {email}: {len(data)} breaches found!")
        return data

    # ─── FULL TARGET INVESTIGATION ────────────────────────────
    def investigate_domain(self, domain: str) -> dict:
        """Full domain OSINT investigation."""
        log.info(f"\n[OSINT] Starting full domain investigation: {domain}")
        report = {
            "target": domain,
            "type": "domain",
            "investigator": "PABLO CYBER - OSINT Engine",
            "timestamp": datetime.datetime.now().isoformat(),
            "results": {}
        }

        report["results"]["subdomains_crtsh"]  = self.crtsh_domain_search(domain)
        report["results"]["hosts_hackertarget"] = self.hackertarget_hostsearch(domain)
        report["results"]["dns_records"]        = self.hackertarget_dns_lookup(domain)
        report["results"]["whois"]              = self.hackertarget_whois(domain)

        return report

    def investigate_github_user(self, username: str) -> dict:
        """Full GitHub user OSINT."""
        log.info(f"\n[OSINT] Starting GitHub investigation: {username}")
        report = {
            "target": username,
            "type": "github_user",
            "investigator": "PABLO CYBER - OSINT Engine",
            "timestamp": datetime.datetime.now().isoformat(),
            "results": {}
        }

        report["results"]["profile"] = self.github_user_profile(username)
        report["results"]["repos"]   = self.github_user_repos(username)
        report["results"]["events"]  = self.github_user_events(username)

        return report


# ─── CLI ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PABLO CYBER - OSINT Forensics Engine")
    parser.add_argument("--github-user",    metavar="USER",   help="Investigate GitHub user")
    parser.add_argument("--github-org",     metavar="ORG",    help="List GitHub org members")
    parser.add_argument("--github-search",  metavar="QUERY",  help="Search GitHub code for exposed secrets")
    parser.add_argument("--domain",         metavar="DOMAIN", help="Full domain OSINT investigation")
    parser.add_argument("--subdomains",     metavar="DOMAIN", help="Find subdomains via crt.sh")
    parser.add_argument("--whois",          metavar="DOMAIN", help="WHOIS lookup")
    parser.add_argument("--dns",            metavar="DOMAIN", help="Full DNS records")
    parser.add_argument("--reverse-ip",     metavar="IP",     help="Find domains on same IP")
    parser.add_argument("--asn",            metavar="IP",     help="ASN lookup for IP")
    parser.add_argument("--email",          metavar="EMAIL",  help="Email OSINT (Gravatar + HIBP)")
    parser.add_argument("--traceroute",     metavar="TARGET", help="Traceroute via HackerTarget")
    parser.add_argument("--github-token",   help="GitHub personal access token")
    parser.add_argument("--hibp-key",       help="HaveIBeenPwned API key")
    args = parser.parse_args()

    osint = OSINTForensics(github_token=args.github_token, hibp_key=args.hibp_key)

    if args.github_user:
        r = osint.investigate_github_user(args.github_user)
        print(json.dumps(r, indent=2))

    elif args.github_org:
        r = osint.github_org_members(args.github_org)
        print(json.dumps(r, indent=2))

    elif args.github_search:
        r = osint.github_search_code(args.github_search)
        print(json.dumps(r, indent=2))

    elif args.domain:
        r = osint.investigate_domain(args.domain)
        print(json.dumps(r, indent=2))

    elif args.subdomains:
        r = osint.crtsh_domain_search(args.subdomains)
        print(json.dumps(r, indent=2))

    elif args.whois:
        print(osint.hackertarget_whois(args.whois))

    elif args.dns:
        r = osint.hackertarget_dns_lookup(args.dns)
        print("\n".join(r))

    elif args.reverse_ip:
        r = osint.hackertarget_reverse_ip(args.reverse_ip)
        print(json.dumps(r, indent=2))

    elif args.asn:
        print(osint.hackertarget_asn_lookup(args.asn))

    elif args.email:
        r = {
            "gravatar": osint.email_gravatar(args.email),
            "hibp":     osint.haveibeenpwned(args.email),
        }
        print(json.dumps(r, indent=2))

    elif args.traceroute:
        r = osint.hackertarget_traceroute(args.traceroute)
        for hop in r:
            print(hop)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
