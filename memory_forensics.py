#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         PABLO CYBER - MEMORY FORENSICS ANALYZER             ║
║         Live Memory Acquisition & Analysis                   ║
╚══════════════════════════════════════════════════════════════╝
Author: PABLO CYBER
Purpose: RAM forensics, process analysis, memory dump inspection
"""

import os
import sys
import re
import json
import struct
import ctypes
import datetime
import platform
import subprocess
import argparse
import logging
from pathlib import Path
from collections import defaultdict

log = logging.getLogger("PABLO_MEM_FORENSICS")
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


class MemoryForensics:
    """Live memory forensics - PABLO CYBER"""

    def __init__(self, output_dir="./mem_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ─── PROCESS LISTING ──────────────────────────────────────
    def list_processes(self) -> list:
        """List all running processes with forensic details."""
        processes = []

        if platform.system() == "Linux":
            proc_dir = Path("/proc")
            for entry in proc_dir.iterdir():
                if entry.name.isdigit():
                    pid = int(entry.name)
                    try:
                        cmdline_file = entry / "cmdline"
                        status_file  = entry / "status"
                        maps_file    = entry / "maps"

                        cmdline = cmdline_file.read_bytes().replace(b'\x00', b' ').decode(errors='replace').strip()
                        status  = {}

                        for line in status_file.read_text().splitlines():
                            if ':' in line:
                                k, v = line.split(':', 1)
                                status[k.strip()] = v.strip()

                        proc_info = {
                            "pid": pid,
                            "name": status.get("Name", "?"),
                            "state": status.get("State", "?"),
                            "ppid": status.get("PPid", "?"),
                            "uid": status.get("Uid", "?").split()[0] if status.get("Uid") else "?",
                            "threads": status.get("Threads", "?"),
                            "vm_rss": status.get("VmRSS", "?"),
                            "cmdline": cmdline[:256],
                        }

                        # Check for suspicious patterns
                        proc_info["suspicious"] = self._is_suspicious(proc_info)
                        processes.append(proc_info)

                    except (PermissionError, FileNotFoundError, ProcessLookupError):
                        continue

        elif platform.system() in ["Darwin", "Windows"]:
            # Fallback: use ps / tasklist
            try:
                if platform.system() == "Darwin":
                    out = subprocess.check_output(["ps", "aux"], text=True)
                else:
                    out = subprocess.check_output(["tasklist", "/FO", "CSV"], text=True)
                for line in out.splitlines()[1:]:
                    processes.append({"raw": line})
            except Exception as e:
                log.error(f"Process list failed: {e}")

        log.info(f"[PROCESSES] Found {len(processes)} processes")
        return processes

    def _is_suspicious(self, proc: dict) -> list:
        """Heuristic check for suspicious process characteristics."""
        flags = []
        name    = proc.get("name", "").lower()
        cmdline = proc.get("cmdline", "").lower()

        # Known suspicious process names
        suspicious_names = ["nc", "ncat", "netcat", "msfconsole", "meterpreter",
                            "mimikatz", "lazagne", "hydra", "nmap", "masscan"]
        if name in suspicious_names:
            flags.append(f"SUSPICIOUS_NAME:{name}")

        # No command line (hidden process)
        if not cmdline and proc.get("pid", 0) > 1:
            flags.append("EMPTY_CMDLINE")

        # Running from temp
        if any(x in cmdline for x in ["/tmp/", "/var/tmp/", "\\temp\\", "\\appdata\\local\\temp\\"]):
            flags.append("RUNNING_FROM_TEMP")

        return flags

    # ─── PROCESS MEMORY STRINGS ───────────────────────────────
    def dump_process_strings(self, pid: int, min_len: int = 6) -> list:
        """Extract strings from a process's memory maps (Linux only)."""
        strings = []

        if platform.system() != "Linux":
            log.error("Process memory string extraction only supported on Linux")
            return strings

        maps_file = Path(f"/proc/{pid}/maps")
        mem_file  = Path(f"/proc/{pid}/mem")

        if not maps_file.exists():
            log.error(f"PID {pid} not found")
            return strings

        try:
            with open(maps_file) as mf:
                maps = mf.readlines()

            with open(mem_file, "rb") as mem:
                for line in maps:
                    if "r" not in line.split()[1]:
                        continue  # skip non-readable regions
                    parts  = line.split()
                    addrs  = parts[0].split('-')
                    start  = int(addrs[0], 16)
                    end    = int(addrs[1], 16)
                    size   = end - start

                    if size > 100 * 1024 * 1024:  # skip regions > 100MB
                        continue

                    try:
                        mem.seek(start)
                        data = mem.read(size)
                        current = ""
                        for byte in data:
                            char = chr(byte)
                            if char.isprintable() and char != '\n':
                                current += char
                            else:
                                if len(current) >= min_len:
                                    strings.append(current)
                                current = ""
                    except (OSError, OverflowError):
                        continue

        except PermissionError:
            log.error(f"Permission denied for PID {pid}. Run as root.")

        log.info(f"[MEM-STRINGS] PID {pid}: extracted {len(strings)} strings")
        return strings

    # ─── NETWORK CONNECTIONS ──────────────────────────────────
    def get_network_connections(self) -> list:
        """Get all network connections with associated PIDs."""
        connections = []

        if platform.system() == "Linux":
            try:
                out = subprocess.check_output(
                    ["ss", "-tulnp"], text=True, stderr=subprocess.DEVNULL
                )
                for line in out.splitlines()[1:]:
                    connections.append({"raw": line.strip()})
                log.info(f"[NETCONN] Found {len(connections)} connections")
            except Exception as e:
                log.error(f"ss failed: {e}")

        elif platform.system() == "Darwin":
            try:
                out = subprocess.check_output(["lsof", "-i", "-n", "-P"], text=True)
                for line in out.splitlines()[1:]:
                    connections.append({"raw": line.strip()})
            except Exception as e:
                log.error(f"lsof failed: {e}")

        return connections

    # ─── LOADED MODULES / LIBRARIES ───────────────────────────
    def get_loaded_modules(self, pid: int) -> list:
        """List all shared libraries loaded by a process."""
        modules = []

        if platform.system() == "Linux":
            maps_file = Path(f"/proc/{pid}/maps")
            if not maps_file.exists():
                log.error(f"PID {pid} not found")
                return modules
            try:
                seen = set()
                for line in maps_file.read_text().splitlines():
                    parts = line.split()
                    if len(parts) >= 6 and parts[5].startswith('/'):
                        lib = parts[5]
                        if lib not in seen:
                            seen.add(lib)
                            modules.append({
                                "path": lib,
                                "perms": parts[1],
                                "is_exec": 'x' in parts[1]
                            })
            except PermissionError:
                log.error(f"Permission denied reading maps for PID {pid}")

        elif platform.system() == "Darwin":
            try:
                out = subprocess.check_output(["vmmap", str(pid)], text=True, stderr=subprocess.DEVNULL)
                for line in out.splitlines():
                    if ".dylib" in line or ".framework" in line:
                        modules.append({"raw": line.strip()})
            except Exception:
                pass

        log.info(f"[MODULES] PID {pid}: {len(modules)} loaded modules")
        return modules

    # ─── MEMORY REPORT ────────────────────────────────────────
    def generate_memory_report(self) -> str:
        """Generate full memory forensics report."""
        report = {
            "title": "Memory Forensics Report",
            "author": "PABLO CYBER",
            "timestamp": datetime.datetime.now().isoformat(),
            "system": platform.node(),
            "os": platform.system(),
            "processes": self.list_processes(),
            "network_connections": self.get_network_connections(),
        }

        # Flag suspicious processes
        suspicious = [p for p in report["processes"] if p.get("suspicious")]
        report["suspicious_processes"] = suspicious
        report["suspicious_count"] = len(suspicious)

        outfile = self.output_dir / f"memory_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(outfile, "w") as f:
            json.dump(report, f, indent=2)

        log.info(f"[REPORT] Memory report saved: {outfile}")
        log.warning(f"[ALERT] Suspicious processes detected: {len(suspicious)}")
        return str(outfile)


# ─── CLI ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PABLO CYBER - Memory Forensics")
    parser.add_argument("--processes", action="store_true", help="List all processes")
    parser.add_argument("--strings",   metavar="PID", type=int, help="Dump strings from process memory")
    parser.add_argument("--modules",   metavar="PID", type=int, help="List loaded modules for PID")
    parser.add_argument("--netconn",   action="store_true", help="Show network connections")
    parser.add_argument("--report",    action="store_true", help="Generate full memory report")
    parser.add_argument("--output",    default="./mem_output", help="Output directory")
    args = parser.parse_args()

    mf = MemoryForensics(output_dir=args.output)

    if args.processes:
        procs = mf.list_processes()
        print(json.dumps(procs, indent=2))

    elif args.strings:
        strs = mf.dump_process_strings(args.strings)
        print(f"\n[+] Strings from PID {args.strings}: {len(strs)}")
        for s in strs[:100]:
            print(f"  {s}")

    elif args.modules:
        mods = mf.get_loaded_modules(args.modules)
        print(json.dumps(mods, indent=2))

    elif args.netconn:
        conns = mf.get_network_connections()
        for c in conns:
            print(c.get("raw", json.dumps(c)))

    elif args.report:
        path = mf.generate_memory_report()
        print(f"\n[+] Report: {path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
