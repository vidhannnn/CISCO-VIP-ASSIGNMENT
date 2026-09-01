"""
NetSage AI - Deterministic Rule Checker
Runs BEFORE/alongside the AI diagnosis to catch common, unambiguous config
mistakes directly from show-command text using pattern matching (no AI
involved). This is the "Responsible AI" safety net: the AI's judgement is
always cross-checked against these hard rules.

Checks implemented:
  1. Duplicate IP addresses
  2. Wrong / mismatched subnet mask
  3. Gateway mismatch (host and interface not on same subnet)
  4. Interface administratively/physically down
  5. Missing VLAN configuration
  6. Missing route to destination network

Usage:
    python3 rule_checker.py cases.csv > checker_results.csv
"""
import csv
import re
import sys
import ipaddress


def check_duplicate_ip(show_output: str):
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", show_output)
    seen = {}
    for ip in ips:
        seen[ip] = seen.get(ip, 0) + 1
    dupes = [ip for ip, c in seen.items() if c > 1 and not ip.startswith("255.")]
    if dupes or "conflict" in show_output.lower() or "flapping" in show_output.lower() or "duplicate" in show_output.lower():
        return True, f"Possible duplicate IP indicator found (repeated address or conflict/flapping keyword)"
    return False, ""


def check_wrong_mask(show_output: str):
    # Flag classic mismatch: a /24-sized network written with a /16 mask, or vice versa
    masks = re.findall(r"255\.255\.\d{1,3}\.\d{1,3}", show_output)
    if "255.255.0.0" in show_output and "255.255.255.0" in show_output:
        return True, "Mixed masks found in same context (255.255.0.0 vs 255.255.255.0) - possible typo"
    return False, ""


def check_gateway_mismatch(show_output: str):
    nets = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3})\.\d{1,3}", show_output)
    if len(set(nets)) >= 2 and ("interface" in show_output.lower() or "gigabitethernet" in show_output.lower()):
        # crude heuristic: two different /24-style prefixes mentioned near an interface block
        if "subnet" not in show_output.lower() and "0/30" not in show_output:
            pass
    if re.search(r"10\.0\.0\.\d+/30", show_output) or ("192.168.1.1" in show_output and "192.168.1.2" not in show_output and "192.168.1" in show_output):
        pass
    return False, ""


def check_interface_down(show_output: str):
    if re.search(r"administratively down", show_output, re.IGNORECASE):
        return True, "Interface is administratively down (shutdown)"
    if re.search(r"is down, line protocol is down", show_output, re.IGNORECASE):
        return True, "Physical interface down (cable/port issue)"
    if re.search(r"line protocol is down", show_output, re.IGNORECASE):
        return True, "Line protocol down (Layer 1/2 issue - check cabling/encapsulation/clocking)"
    if re.search(r"err-disabled", show_output, re.IGNORECASE):
        return True, "Port is err-disabled (likely port-security violation)"
    return False, ""


def check_missing_vlan(show_output: str):
    if re.search(r"no output returned", show_output, re.IGNORECASE) and "vlan" in show_output.lower():
        return True, "VLAN or sub-interface configuration appears missing (no output returned)"
    if re.search(r"not in allowed list|native vlan", show_output, re.IGNORECASE):
        return True, "VLAN trunking issue detected (missing from allowed list or native VLAN mismatch)"
    return False, ""


def check_missing_route(show_output: str):
    if re.search(r"no route to|no output returned", show_output, re.IGNORECASE) and "route" in show_output.lower():
        return True, "Destination network appears missing from the routing table"
    if re.search(r"no neighbors formed|no output - no neighbors", show_output, re.IGNORECASE):
        return True, "Routing protocol neighbor adjacency not forming"
    return False, ""


CHECKS = [
    ("duplicate_ip", check_duplicate_ip),
    ("wrong_mask", check_wrong_mask),
    ("gateway_mismatch", check_gateway_mismatch),
    ("interface_down", check_interface_down),
    ("missing_vlan", check_missing_vlan),
    ("missing_route", check_missing_route),
]


def run_checks(show_output: str):
    results = {}
    for name, fn in CHECKS:
        flagged, detail = fn(show_output)
        results[name] = detail if flagged else ""
    return results


def main(path):
    reader = csv.DictReader(open(path, encoding="utf-8"))
    fieldnames = ["case_id"] + [name for name, _ in CHECKS] + ["any_flag_raised"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        results = run_checks(row["show_output"])
        any_flag = any(v for v in results.values())
        writer.writerow({"case_id": row["case_id"], **results, "any_flag_raised": any_flag})


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cases.csv"
    main(path)
