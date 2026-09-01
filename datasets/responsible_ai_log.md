# Responsible AI Log — NetSage AI

This log documents every case where the AI assistant's diagnosis was incorrect,
incomplete, or potentially risky, and how the human reviewer corrected it.
Per the project's safety rule, **no AI diagnosis was applied as a fix without human review.**

## C04 — DHCP
- **Symptom:** All hosts on VLAN 40 get 169.254.x.x addresses intermittently, and duplicate IP warnings appear.
- **AI diagnosis:** DHCP scope for VLAN 40 is nearly exhausted, causing some clients to fall back to APIPA. (confidence: medium)
- **Correct root cause:** Static IP on PC5 conflicts with an address inside the DHCP scope
- **What went wrong:** AI blamed pool exhaustion; actual cause was a static IP conflicting with an in-scope DHCP address.
- **Review outcome:** Edited — root cause and fix steps corrected before logging

## C09 — Static Routing
- **Symptom:** Static route to remote branch was configured but traffic still fails; 'show ip route' shows the route missing.
- **AI diagnosis:** Static route to 10.2.2.0 is missing from the routing table entirely. (confidence: medium)
- **Correct root cause:** Incorrect subnet mask typed in static route (255.255.0.0 instead of 255.255.255.0), causing route rejection/overlap
- **What went wrong:** AI said the route was 'missing' but evidence showed it WAS entered, just with a typo'd subnet mask (255.255.0.0 vs 255.255.255.0) — a more specific and actionable root cause.
- **Review outcome:** Edited — root cause and fix steps corrected before logging

## C13 — ACL
- **Symptom:** Employees cannot access the finance server (10.5.5.10) from the sales VLAN, but ping to gateway works.
- **AI diagnosis:** ACL 101 is correctly blocking unauthorized access to the finance server as designed. (confidence: high)
- **Correct root cause:** Overly broad ACL entry blocks legitimate traffic from an unintended source subnet
- **What went wrong:** AI concluded the ACL was 'working as intended' and needed no action. It missed that the rule was overly broad and silently blocking a legitimate subnet too.
- **Review outcome:** Edited — root cause and fix steps corrected before logging

## C17 — Duplicate IP
- **Symptom:** Two PCs on the same VLAN keep dropping connection intermittently; switch logs show MAC flapping.
- **AI diagnosis:** A switching loop is causing MAC address instability between Fa0/3 and Fa0/9. (confidence: medium)
- **Correct root cause:** Duplicate IP address (10.20.20.15) assigned to two different hosts causing MAC/ARP instability
- **What went wrong:** AI guessed a switching loop from MAC flapping. Actual cause was a duplicate static IP on two hosts, confirmed by the ARP/ping conflict pattern.
- **Review outcome:** Edited — root cause and fix steps corrected before logging

## C19 — STP
- **Symptom:** After adding a new switch, spanning-tree keeps blocking a port users need, causing slow convergence complaints.
- **AI diagnosis:** A network loop has formed after adding SW7, causing an outage on VLAN 10. (confidence: medium)
- **Correct root cause:** Root bridge election chose a suboptimal (low-end) switch, causing inefficient traffic paths; priority not set on core switch
- **What went wrong:** AI escalated a low-severity STP suboptimal-root-bridge situation into 'a loop causing an outage' and recommended shutting a link immediately, which was unnecessary and risky.
- **Review outcome:** Rejected — AI recommendation not applied

## C22 — NAT
- **Symptom:** PC13 in VLAN 10 can reach the internet but internal server 10.1.1.20 times out.
- **AI diagnosis:** Internal server 10.1.1.20 is down or not responding to requests. (confidence: low)
- **Correct root cause:** NAT ACL too broad, translating internal-to-internal traffic that should bypass NAT
- **What went wrong:** AI suspected the server was down. NAT translation evidence actually showed internal-to-internal traffic being incorrectly NAT'd — a config issue, not a server outage.
- **Review outcome:** Edited — root cause and fix steps corrected before logging

## Summary
- Total cases reviewed: 30
- Accepted without changes: 24
- Edited by human reviewer: 5
- Rejected outright: 1
- AI/human agreement rate: 80.0%

## Why this matters
The AI assistant is useful for quickly narrowing down likely fault categories and
proposing next diagnostic commands, but it can misread evidence (e.g. confusing a
duplicate-IP symptom for a switching loop) or under/over-state severity. The rule
checker catches some but not all of these misses. This is exactly why the project
requires a human reviewer to approve or correct every diagnosis before any fix is
applied to a real or simulated device.