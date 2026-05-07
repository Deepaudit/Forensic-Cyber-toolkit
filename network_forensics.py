#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         PABLO CYBER - NETWORK FORENSICS ANALYZER            ║
║         Capture, Analyze, Investigate Network Traffic        ║
╚══════════════════════════════════════════════════════════════╝
Author: PABLO CYBER
Purpose: Network forensics for ethical hacking & incident response
"""

import socket
import struct
import json
import datetime
import ipaddress
import urllib.request
import urllib.error
import argparse
import logging
import os
import sys
from collections import defaultdict

log = logging.getLogger("PABLO_NET_FORENSICS")
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


# ─── PUBLIC API INTEGRATIONS ──────────────────────────────────

class PublicAPIInvestigator:
    """Threat intelligence via free public APIs - PABLO CYBER"""

    ABUSEIPDB_BASE   = "https://api.abuseipdb.com/api/v2"
    VIRUSTOTAL_BASE  = "https://www.virustotal.com/api/v3"
    SHODAN_BASE      = "https://api.shodan.io"
    IPINFO_BASE      = "https://ipinfo.io"
    URLHAUS_BASE     = "https://urlhaus-api.abuse.ch/v1"
    THREATFOX_BASE   = "https://threatfox-api.abuse.ch/api/v1"

    def __init__(self, abuseipdb_key=None, virustotal_key=None, shodan_key=None):
        self.keys = {
            "abuseipdb": abuseipdb_key or os.environ.get("ABUSEIPDB_KEY"),
            "virustotal": virustotal_key or os.environ.get("VT_KEY"),
            "shodan": shodan_key or os.environ.get("SHODAN_KEY"),
        }

    def _request(self, url: str, headers: dict = None) -> dict:
        """Generic HTTP request handler."""
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            log.error(f"HTTP {e.code} for {url}")
            return {"error": str(e)}
        except Exception as e:
            log.error(f"Request failed: {e}")
            return {"error": str(e)}

    # ── IP Geolocation (FREE - no key needed) ─────────────────
    def geolocate_ip(self, ip: str) -> dict:
        """Geolocate IP using ipinfo.io (free tier)."""
        url = f"{self.IPINFO_BASE}/{ip}/json"
        result = self._request(url)
        result["queried_ip"] = ip
        result["source"] = "ipinfo.io"
        log.info(f"[GEO] {ip} → {result.get('country','?')}/{result.get('city','?')}")
        return result

    # ── URLHaus Malware URL Check (FREE) ──────────────────────
    def check_url_malware(self, url_to_check: str) -> dict:
        """Check URL against URLHaus malware database (no key required)."""
        import urllib.parse
        data = urllib.parse.urlencode({"url": url_to_check}).encode()
        try:
            req = urllib.request.Request(
                f"{self.URLHAUS_BASE}/url/",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                result["source"] = "URLHaus (abuse.ch)"
                log.info(f"[URLHAUS] {url_to_check} → {result.get('query_status','?')}")
                return result
        except Exception as e:
            return {"error": str(e)}

    # ── ThreatFox IOC Lookup (FREE) ───────────────────────────
    def threatfox_ioc_search(self, ioc: str) -> dict:
        """Search ThreatFox for IOC (IP, domain, hash) - free API."""
        payload = json.dumps({"query": "search_ioc", "search_term": ioc}).encode()
        try:
            req = urllib.request.Request(
                self.THREATFOX_BASE,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                result["source"] = "ThreatFox (abuse.ch)"
                log.info(f"[THREATFOX] IOC: {ioc} → {result.get('query_status','?')}")
                return result
        except Exception as e:
            return {"error": str(e)}

    # ── AbuseIPDB Check (requires free API key) ────────────────
    def check_abuseipdb(self, ip: str, max_age_days: int = 90) -> dict:
        """Check IP reputation on AbuseIPDB."""
        if not self.keys["abuseipdb"]:
            return {"error": "ABUSEIPDB_KEY not set. Get free key at abuseipdb.com"}

        url = f"{self.ABUSEIPDB_BASE}/check?ipAddress={ip}&maxAgeInDays={max_age_days}"
        headers = {
            "Key": self.keys["abuseipdb"],
            "Accept": "application/json"
        }
        result = self._request(url, headers)
        log.info(f"[ABUSEIPDB] {ip} → score: {result.get('data',{}).get('abuseConfidenceScore','?')}")
        return result

    # ── VirusTotal Hash/IP/Domain Check ───────────────────────
    def virustotal_check_ip(self, ip: str) -> dict:
        """Check IP on VirusTotal (requires API key)."""
        if not self.keys["virustotal"]:
            return {"error": "VT_KEY not set. Get free key at virustotal.com"}

        url = f"{self.VIRUSTOTAL_BASE}/ip_addresses/{ip}"
        headers = {"x-apikey": self.keys["virustotal"]}
        result = self._request(url, headers)
        log.info(f"[VIRUSTOTAL] IP: {ip} checked")
        return result

    def virustotal_check_hash(self, file_hash: str) -> dict:
        """Check file hash on VirusTotal."""
        if not self.keys["virustotal"]:
            return {"error": "VT_KEY not set. Get free key at virustotal.com"}

        url = f"{self.VIRUSTOTAL_BASE}/files/{file_hash}"
        headers = {"x-apikey": self.keys["virustotal"]}
        result = self._request(url, headers)
        log.info(f"[VIRUSTOTAL] Hash: {file_hash[:16]}... checked")
        return result

    # ── Shodan Host Info ──────────────────────────────────────
    def shodan_host_info(self, ip: str) -> dict:
        """Get Shodan host info (requires API key)."""
        if not self.keys["shodan"]:
            return {"error": "SHODAN_KEY not set. Get free key at shodan.io"}

        url = f"{self.SHODAN_BASE}/shodan/host/{ip}?key={self.keys['shodan']}"
        result = self._request(url)
        log.info(f"[SHODAN] {ip} → ports: {result.get('ports', [])}")
        return result

    # ── DNS Lookup ────────────────────────────────────────────
    def dns_lookup(self, domain: str) -> dict:
        """Resolve domain to IP addresses."""
        try:
            ips = socket.getaddrinfo(domain, None)
            unique_ips = list(set([x[4][0] for x in ips]))
            result = {
                "domain": domain,
                "resolved_ips": unique_ips,
                "timestamp": datetime.datetime.now().isoformat()
            }
            log.info(f"[DNS] {domain} → {unique_ips}")
            return result
        except Exception as e:
            return {"domain": domain, "error": str(e)}

    # ── Reverse DNS ───────────────────────────────────────────
    def reverse_dns(self, ip: str) -> dict:
        """Reverse DNS lookup for an IP."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {"ip": ip, "hostname": hostname}
        except Exception as e:
            return {"ip": ip, "error": str(e)}

    # ── Comprehensive IP Investigation ────────────────────────
    def full_ip_investigation(self, ip: str) -> dict:
        """Run all available checks on an IP address."""
        log.info(f"[INVESTIGATION] Starting full analysis of: {ip}")
        report = {
            "target_ip": ip,
            "investigation_time": datetime.datetime.now().isoformat(),
            "investigator": "PABLO CYBER - Network Forensics",
            "results": {}
        }

        report["results"]["geolocation"] = self.geolocate_ip(ip)
        report["results"]["reverse_dns"]  = self.reverse_dns(ip)
        report["results"]["abuseipdb"]    = self.check_abuseipdb(ip)
        report["results"]["virustotal"]   = self.virustotal_check_ip(ip)
        report["results"]["shodan"]       = self.shodan_host_info(ip)
        report["results"]["threatfox"]    = self.threatfox_ioc_search(ip)

        return report


# ─── PACKET ANALYZER (raw sockets) ───────────────────────────

class PacketAnalyzer:
    """Raw packet capture & analysis - requires root/admin."""

    def __init__(self):
        self.packets = []
        self.stats = defaultdict(int)

    def parse_ethernet(self, raw_data: bytes) -> dict:
        """Parse Ethernet frame header."""
        dest_mac = ':'.join(f'{b:02x}' for b in raw_data[:6])
        src_mac  = ':'.join(f'{b:02x}' for b in raw_data[6:12])
        proto    = struct.unpack('!H', raw_data[12:14])[0]
        return {"dest_mac": dest_mac, "src_mac": src_mac, "protocol": proto, "data": raw_data[14:]}

    def parse_ipv4(self, data: bytes) -> dict:
        """Parse IPv4 header."""
        version_ihl = data[0]
        ihl         = (version_ihl & 0xF) * 4
        ttl, proto  = data[8], data[9]
        src_ip      = socket.inet_ntoa(data[12:16])
        dest_ip     = socket.inet_ntoa(data[16:20])
        return {
            "src_ip": src_ip, "dest_ip": dest_ip,
            "ttl": ttl, "protocol": proto,
            "header_length": ihl, "data": data[ihl:]
        }

    def parse_tcp(self, data: bytes) -> dict:
        """Parse TCP segment."""
        src_port, dest_port, seq, ack = struct.unpack('!HHLL', data[:12])
        offset_flags = struct.unpack('!H', data[12:14])[0]
        flags = {
            "SYN": bool(offset_flags & 0x002),
            "ACK": bool(offset_flags & 0x010),
            "FIN": bool(offset_flags & 0x001),
            "RST": bool(offset_flags & 0x004),
            "PSH": bool(offset_flags & 0x008),
        }
        return {"src_port": src_port, "dest_port": dest_port, "seq": seq, "ack": ack, "flags": flags}

    def sniff(self, packet_count: int = 100, protocol_filter: str = None):
        """Capture raw packets (requires root privileges)."""
        if os.geteuid() != 0:
            log.error("Packet capture requires root privileges. Run with sudo.")
            return []

        log.info(f"[SNIFF] Starting capture: {packet_count} packets...")
        try:
            conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            for _ in range(packet_count):
                raw_data, _ = conn.recvfrom(65535)
                eth = self.parse_ethernet(raw_data)
                packet = {"ethernet": eth, "timestamp": datetime.datetime.now().isoformat()}

                if eth["protocol"] == 8:  # IPv4
                    ip = self.parse_ipv4(eth["data"])
                    packet["ipv4"] = ip
                    self.stats[f"{ip['src_ip']} → {ip['dest_ip']}"] += 1

                    if ip["protocol"] == 6:  # TCP
                        tcp = self.parse_tcp(ip["data"])
                        packet["tcp"] = tcp
                        self.stats["TCP"] += 1
                    elif ip["protocol"] == 17:
                        self.stats["UDP"] += 1

                self.packets.append(packet)
                log.info(f"Captured packet {len(self.packets)}/{packet_count}")

        except KeyboardInterrupt:
            log.info("Capture interrupted by user.")

        return self.packets


# ─── PORT SCANNER ─────────────────────────────────────────────

class PortScanner:
    """Forensic port scanner - PABLO CYBER."""

    COMMON_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
        6667: "IRC", 4444: "Metasploit", 1337: "H4X0R"
    }

    def scan(self, target: str, ports: list = None, timeout: float = 1.0) -> dict:
        """Scan target for open ports."""
        ports = ports or list(self.COMMON_PORTS.keys())
        results = {"target": target, "open_ports": [], "closed_ports": [], "timestamp": datetime.datetime.now().isoformat()}

        log.info(f"[SCAN] Scanning {target} | {len(ports)} ports")
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                code = sock.connect_ex((target, port))
                sock.close()
                service = self.COMMON_PORTS.get(port, "Unknown")
                if code == 0:
                    results["open_ports"].append({"port": port, "service": service, "state": "OPEN"})
                    log.info(f"  [OPEN]   {port:5d}/tcp  {service}")
                else:
                    results["closed_ports"].append(port)
            except Exception as e:
                log.warning(f"  Error on port {port}: {e}")

        log.info(f"[SCAN] Complete: {len(results['open_ports'])} open / {len(results['closed_ports'])} closed")
        return results


# ─── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PABLO CYBER - Network Forensics Analyzer")
    parser.add_argument("--investigate", metavar="IP", help="Full IP investigation (all APIs)")
    parser.add_argument("--geo",         metavar="IP", help="Geolocate an IP address")
    parser.add_argument("--urlcheck",    metavar="URL", help="Check URL for malware (URLHaus)")
    parser.add_argument("--ioc",         metavar="IOC", help="Search ThreatFox for IOC")
    parser.add_argument("--scan",        metavar="TARGET", help="Port scan a target")
    parser.add_argument("--dns",         metavar="DOMAIN", help="DNS lookup")
    parser.add_argument("--rdns",        metavar="IP", help="Reverse DNS lookup")
    parser.add_argument("--abuseipdb-key", help="AbuseIPDB API key")
    parser.add_argument("--vt-key",      help="VirusTotal API key")
    parser.add_argument("--shodan-key",  help="Shodan API key")
    args = parser.parse_args()

    api = PublicAPIInvestigator(
        abuseipdb_key=args.abuseipdb_key,
        virustotal_key=args.vt_key,
        shodan_key=args.shodan_key
    )

    if args.investigate:
        result = api.full_ip_investigation(args.investigate)
        print(json.dumps(result, indent=2))

    elif args.geo:
        print(json.dumps(api.geolocate_ip(args.geo), indent=2))

    elif args.urlcheck:
        print(json.dumps(api.check_url_malware(args.urlcheck), indent=2))

    elif args.ioc:
        print(json.dumps(api.threatfox_ioc_search(args.ioc), indent=2))

    elif args.scan:
        scanner = PortScanner()
        result = scanner.scan(args.scan)
        print(json.dumps(result, indent=2))

    elif args.dns:
        print(json.dumps(api.dns_lookup(args.dns), indent=2))

    elif args.rdns:
        print(json.dumps(api.reverse_dns(args.rdns), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
