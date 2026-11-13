# Cybersecurity Technical Portfolio

Welcome to my Cybersecurity Portfolio. I am an entry-level **Cybersecurity Analyst** with a background in **English Language Education (B.A.)** and **Administrative & Operations Management**. Having completed the **Google Cybersecurity Professional Certificate**, I combine hands-on technical analysis—spanning SIEM log investigations, network packet inspection, Linux/SQL auditing, and Python automation—with structured documentation and clear risk communication.

This repository contains my documented lab workflows, command-line breakdowns, security queries, and automation scripts across five core domains of defensive security.

---

## Core Technical Competencies

* **Security Operations & SIEM:** Splunk (SPL), Google Chronicle (UDM), Event Correlation, Brute-Force & C2 Triage
* **Network Security & IDS:** Wireshark, `tcpdump`, Suricata IDS Signature Analysis (`fast.log`, `eve.json`), TCP/IP, DNS, HTTP
* **Systems & Database Security:** Linux CLI (Bash), File Permissions (`chmod`), MariaDB/MySQL Incident Filtering
* **Security Automation:** Python 3 (File I/O, List/String Manipulation, Regular Expressions `re`, Log Parsing)
* **Governance, Risk & Compliance (GRC):** NIST Cybersecurity Framework (CSF), CIA Triad, Vulnerability Remediation, Principle of Least Privilege

---

## Repository Structure & Project Directory

```text
cybersecurity-portfolio/
├── README.md
├── 01-linux-sql/
│   ├── linux-permissions-audit.md
│   ├── sql-security-queries.md
│   └── sql-security-queries.sql
├── 02-network-analysis/
│   ├── tcpdump-traffic-investigation.md
│   └── wireshark-packet-analysis.md
├── 03-siem-and-ids/
│   ├── splunk-investigation-report.md
│   ├── chronicle-log-analysis.md
│   └── suricata-alert-triage.md
├── 04-python-automation/
│   ├── README.md
│   └── update_allow_list.py
└── 05-security-audits-and-grc/
    └── vulnerability-assessment-report.md
```

## Hands-On Projects & Lab Write-Ups

### 1. [Linux File Permissions & SQL Incident Investigation](./01-linux-sql/)
* **[Linux File Permissions & Access Control Audit](./01-linux-sql/linux-permissions-audit.md):** Audited sensitive research directories (`/home/researcher2/projects`) using `ls -la` and enforced the Principle of Least Privilege using `chmod` symbolic permissions to lock down hidden archives and group folders.
* **[SQL Security Queries & Log Filtering](./01-linux-sql/sql-security-queries.md) | [Raw SQL Script](./01-linux-sql/sql-security-queries.sql):** Queried `log_in_attempts` and `employees` tables in MariaDB using `WHERE`, `AND`, `OR`, `NOT`, and `LIKE` wildcards (`%`) to isolate after-hours failed logins, track suspicious IP subnets (`198.51.100.%`), and filter departmental machines for security patching.

### 2. [Network Traffic & Packet Analysis](./02-network-analysis/)
* **[CLI Packet Sniffing with `tcpdump`](./02-network-analysis/tcpdump-traffic-investigation.md):** Captured and filtered network traffic on Linux interfaces (`-i eth0`), suppressed DNS/port translation (`-nn`) for forensic integrity, isolated HTTP and DNS flows, and inspected ASCII packet payloads (`-A`) alongside offline `.pcap` files (`-r`).
* **[Wireshark Packet Inspection](./02-network-analysis/wireshark-packet-analysis.md):** Analyzed offline packet captures (`sample.pcap`) using display filters to trace TCP 3-way handshakes (`tcp.flags.syn == 1`), uncover plaintext credentials in unencrypted `HTTP POST` requests, reconstruct full TCP streams, and audit outbound DNS queries (`dns.flags.response == 0`).

### 3. [SIEM Threat Hunting & IDS Alert Triage](./03-siem-and-ids/)
* **[Incident Investigation in Splunk (SIEM)](./03-siem-and-ids/splunk-investigation-report.md):** Used Splunk Search Processing Language (SPL) to aggregate Windows failed logon events (`EventCode=4625`) with `stats count` and `sort`, identifying a high-velocity brute-force attack and correlating it with a subsequent successful logon (`EventCode=4624`).
* **[Threat Hunting with Google Chronicle](./03-siem-and-ids/chronicle-log-analysis.md):** Queried normalized telemetry using Chronicle's Unified Data Model (UDM) to trace outbound DNS lookups (`NETWORK_DNS`) to a command-and-control domain, pivot to the compromised internal host (`principal.ip`), identify the active user (`USER_LOGIN`), and pinpoint malicious binary execution (`PROCESS_LAUNCH`).
* **[Intrusion Detection & Alert Triage with Suricata](./03-siem-and-ids/suricata-alert-triage.md):** Executed Suricata in offline PCAP replay mode (`-r sample.pcap -S custom.rules -k none`), triaged triggered signatures in `fast.log`, parsed deep JSON metadata in `eve.json` using `jq`, and authored custom rules to detect cleartext HTTP password transmissions.

### 4. [Cybersecurity Task Automation with Python](./04-python-automation/)
* **[Python Automation Lab Reference & IP Allowlist Algorithm](./04-python-automation/README.md) | [Python Script](./04-python-automation/update_allow_list.py):** Developed a reusable Python algorithm using context managers (`with open()`), string splitting (`.split()`), iterative list filtering (`for`, `if`, `.remove()`), and string reconstruction (`"\n".join()`) to automatically revoke unauthorized IP addresses from `allow_list.txt`. Includes custom functions for account lockout checks (`login_check()`), anomaly ratios (`analyze_logins()`), string slicing, and Regular Expressions (`re.findall()`).

### 5. [Vulnerability Assessment & GRC Security Audits](./05-security-audits-and-grc/)
* **[Server Vulnerability Assessment & Remediation Report](./05-security-audits-and-grc/vulnerability-assessment-report.md):** Conducted an open-port and service audit (`nmap -sV`) on an internal Linux server and documented Defense-in-Depth remediation controls—disabling root SSH access (`PermitRootLogin no`), enforcing TLS 1.2/1.3 in Apache, and hardening MariaDB (`mysql_secure_installation` & `127.0.0.1` loopback binding)—mapped to CVSS severity scores, the CIA Triad, and the NIST CSF.

# Certifications & Education
* Google Cybersecurity Professional Certificate — Coursera (2026)
* Bachelor of Arts in English Language — University of Education, Winneba

# Contact & Connect

* LinkedIn: Adutwumwaa Frimpong
* GitHub: https://github.com/adutwumwaa0/cybersecurity-portfolio
* Email: adutwumwaafrimpong79@gmail.com
