# NetSage AI — Applied AI + Network Troubleshooting Assistant

NetSage AI is an AI-assisted network troubleshooting system developed for the Cisco-AICTE Virtual Internship Program 2026 (AI Track). It helps diagnose common Cisco-style network problems using symptoms, topology information, and `show` command evidence.

## Problem Statement

Junior network engineers often know individual troubleshooting commands but struggle to connect network symptoms with their actual root causes. NetSage AI helps identify likely faults, affected OSI layers, supporting evidence, next diagnostic commands, and recommended fixes.

## How It Works

```text
Network Symptoms + Show Command Evidence
                  ↓
          Structured AI Diagnosis
                  ↓
       Deterministic Rule Checker
                  ↓
             Human Review
                  ↓
       Approved / Corrected Diagnosis
                  ↓
             Fix & Verification



             Key Features
AI-based network fault diagnosis
Structured JSON diagnosis output
Deterministic Python rule checker
Duplicate IP detection
Subnet mask mismatch detection
Gateway and interface subnet validation
Interface status checking
Missing VLAN detection
Missing route detection
Human-in-the-loop review
Responsible AI logging
Results dashboard
Dataset

The project contains 30 Cisco-style network troubleshooting cases covering VLAN, gateway, DHCP, DNS, routing, ACL, NAT, wireless, spanning-tree, and port-security scenarios.

AI Diagnosis Output

Each diagnosis contains:

Root cause
OSI layer
Confidence
Supporting evidence
Next diagnostic command
Recommended fix steps
Responsible AI

AI recommendations are never treated as final automatically. Every diagnosis is reviewed by a human and classified as:

Accepted — correct diagnosis
Edited — partially correct and modified
Rejected — incorrect or unsafe

A deterministic Python rule checker independently validates common configuration errors, providing an additional safety layer.

Results

Out of 30 cases:

Result	Cases	Percentage
Accepted	24	80%
Edited	    5	17%
Rejected	1	3%
Total	   30	100%

The results demonstrate that AI can accelerate network troubleshooting while still requiring human judgment for reliable and safe decision-making.

Technologies Used
Python 3
Large Language Model (Claude)
CSV
JSON
Markdown
Matplotlib
Cisco networking concepts
Packet Tracer-style troubleshooting scenarios
Project Files
cases.csv — 30 troubleshooting cases
diagnose_prompt.md — structured AI diagnosis prompt
ai_diagnoses.json — AI diagnosis results
rule_checker.py — deterministic rule checker
checker_results.csv — rule checker results
human_review_log.csv — human review decisions
responsible_ai_log.md — Responsible AI analysis
dashboard.png — project results dashboard
Demo_Video_Script.md — project demonstration script
How to Run

Run the deterministic rule checker using:

python3 "project file/rule_checker.py" < datasets/cases.csv > datasets/checker_results.csv
Limitations

The current system uses Cisco-style lab scenarios and simulated network evidence. The rule checker covers selected common configuration errors and is not a replacement for complete network troubleshooting. The system does not automatically apply network configuration changes.

Future Scope
Support for additional Cisco commands
Larger troubleshooting datasets
More advanced rule-based validation
Packet Tracer integration
Retrieval-Augmented Generation using Cisco documentation
Automated pre-fix and post-fix verification
Stronger audit trails and approval workflows


Project

NetSage AI — Applied AI + Network Troubleshooting Assistant

Cisco-AICTE Virtual Internship Program 2026 — AI Track