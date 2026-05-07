#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         PABLO CYBER - DIGITAL FORENSICS ENGINE v2.0         ║
║              Ethical Hacking & Forensics Toolkit             ║
║                    Author: PABLO CYBER                       ║
╚══════════════════════════════════════════════════════════════╝

DISCLAIMER: This tool is intended for ETHICAL use only.
Use only on systems you own or have explicit permission to analyze.
"""

import os
import sys
import json
import hashlib
import datetime
import platform
import subprocess
import argparse
import logging
from pathlib import Path

# ─── BANNER ───────────────────────────────────────────────────
BANNER = """
\033[1;32m
██████╗  █████╗ ██████╗ ██╗      ██████╗      ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║     ██╔═══██╗    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██████╔╝███████║██████╔╝██║     ██║   ██║    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔══██╗██║     ██║   ██║    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
██║     ██║  ██║██████╔╝███████╗╚██████╔╝    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝      ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
\033[0m
\033[1;36m           [ DIGITAL FORENSICS ENGINE ] - Author: PABLO CYBER \033[0m
\033[0;33m           [ Ethical Hacking & Forensics Research Platform   ] \033[0m
"""

# ─── LOGGING SETUP ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger("PABLO_FORENSICS")


class ForensicsEngine:
    """Core Digital Forensics Engine by PABLO CYBER"""

    def __init__(self, output_dir="./forensics_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.evidence = []
        log.info(f"ForensicsEngine initialized | Session: {self.session_id}")

    # ─── HASH GENERATION ──────────────────────────────────────
    def hash_file(self, filepath: str) -> dict:
        """Generate MD5, SHA1, SHA256 hashes for file integrity."""
        filepath = Path(filepath)
        if not filepath.exists():
            log.error(f"File not found: {filepath}")
            return {}

        hashes = {}
        algorithms = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256(),
            "sha512": hashlib.sha512(),
        }

        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                for algo in algorithms.values():
                    algo.update(chunk)

        for name, algo in algorithms.items():
            hashes[name] = algo.hexdigest()

        hashes["file"] = str(filepath)
        hashes["size_bytes"] = filepath.stat().st_size
        hashes["timestamp"] = datetime.datetime.now().isoformat()

        log.info(f"[HASH] {filepath.name} | SHA256: {hashes['sha256'][:16]}...")
        return hashes

    # ─── SYSTEM INFO COLLECTION ───────────────────────────────
    def collect_system_info(self) -> dict:
        """Collect detailed system information for forensic baseline."""
        info = {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "collection_time": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
        }

        # Uptime (Linux/Mac)
        if platform.system() in ["Linux", "Darwin"]:
            try:
                uptime = subprocess.check_output(["uptime", "-p"], text=True).strip()
                info["uptime"] = uptime
            except Exception:
                pass

        log.info(f"[SYSINFO] Collected system baseline for: {info['hostname']}")
        self.evidence.append({"type": "system_info", "data": info})
        return info

    # ─── FILE TIMELINE ────────────────────────────────────────
    def build_file_timeline(self, directory: str, extensions: list = None) -> list:
        """Build forensic timeline of file access/modification times."""
        timeline = []
        directory = Path(directory)

        if not directory.exists():
            log.error(f"Directory not found: {directory}")
            return []

        for filepath in directory.rglob("*"):
            if filepath.is_file():
                if extensions and filepath.suffix.lower() not in extensions:
                    continue
                try:
                    stat = filepath.stat()
                    entry = {
                        "file": str(filepath),
                        "size": stat.st_size,
                        "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "accessed": datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
                        "extension": filepath.suffix,
                    }
                    timeline.append(entry)
                except (PermissionError, OSError) as e:
                    log.warning(f"Cannot access {filepath}: {e}")

        # Sort by modification time
        timeline.sort(key=lambda x: x["modified"], reverse=True)
        log.info(f"[TIMELINE] Built timeline: {len(timeline)} files in {directory}")
        self.evidence.append({"type": "file_timeline", "directory": str(directory), "data": timeline})
        return timeline

    # ─── STRING EXTRACTION ────────────────────────────────────
    def extract_strings(self, filepath: str, min_length: int = 4) -> list:
        """Extract printable strings from binary files (like Unix 'strings')."""
        filepath = Path(filepath)
        strings_found = []

        if not filepath.exists():
            log.error(f"File not found: {filepath}")
            return []

        try:
            with open(filepath, "rb") as f:
                data = f.read()

            current = ""
            for byte in data:
                char = chr(byte)
                if char.isprintable() and char != '\n':
                    current += char
                else:
                    if len(current) >= min_length:
                        strings_found.append(current)
                    current = ""

            if len(current) >= min_length:
                strings_found.append(current)

        except (PermissionError, OSError) as e:
            log.error(f"Cannot read {filepath}: {e}")

        log.info(f"[STRINGS] Extracted {len(strings_found)} strings from {filepath.name}")
        return strings_found

    # ─── REPORT GENERATION ────────────────────────────────────
    def generate_report(self, title: str = "Forensic Report") -> str:
        """Generate a JSON forensic report of all collected evidence."""
        report = {
            "title": title,
            "author": "PABLO CYBER",
            "tool": "Pablo Cyber Digital Forensics Engine v2.0",
            "session_id": self.session_id,
            "generated_at": datetime.datetime.now().isoformat(),
            "evidence_count": len(self.evidence),
            "evidence": self.evidence,
        }

        report_file = self.output_dir / f"forensic_report_{self.session_id}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        log.info(f"[REPORT] Saved to: {report_file}")
        return str(report_file)


# ─── CLI ENTRYPOINT ───────────────────────────────────────────
def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="PABLO CYBER - Digital Forensics Engine",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--hash", metavar="FILE", help="Hash a file (MD5/SHA1/SHA256/SHA512)")
    parser.add_argument("--sysinfo", action="store_true", help="Collect system information")
    parser.add_argument("--timeline", metavar="DIR", help="Build file timeline for a directory")
    parser.add_argument("--strings", metavar="FILE", help="Extract strings from binary file")
    parser.add_argument("--report", action="store_true", help="Generate forensic report")
    parser.add_argument("--output", default="./forensics_output", help="Output directory")

    args = parser.parse_args()
    engine = ForensicsEngine(output_dir=args.output)

    if args.hash:
        result = engine.hash_file(args.hash)
        print(json.dumps(result, indent=2))

    if args.sysinfo:
        result = engine.collect_system_info()
        print(json.dumps(result, indent=2))

    if args.timeline:
        result = engine.build_file_timeline(args.timeline)
        print(f"\n[+] Timeline entries: {len(result)}")
        for entry in result[:20]:
            print(f"  {entry['modified']} | {entry['file']}")

    if args.strings:
        result = engine.extract_strings(args.strings)
        print(f"\n[+] Strings found: {len(result)}")
        for s in result[:50]:
            print(f"  {s}")

    if args.report:
        path = engine.generate_report()
        print(f"\n[+] Report saved: {path}")

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
