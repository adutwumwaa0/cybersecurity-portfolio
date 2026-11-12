# Threat Hunting with Google Chronicle (SIEM)

# Project Overview
As an entry-level Security Operations Center (SOC) analyst, I conducted a threat-hunting investigation using **Google Chronicle** (a cloud-native Security Information and Event Management platform). The goal of this lab was to query normalized security telemetry using Chronicle's Unified Data Model (UDM) to detect outbound connections to suspicious external domains, trace the internal host responsible for the traffic, and identify the active user account during the incident.

## Scenario
Threat intelligence flagged an external domain (`malicious-c2-domain.com`) known to be associated with command-and-control (C2) malware callbacks. 

My task was to query the normalized event logs using Chronicle UDM search syntax to:
1. Search DNS network logs to verify whether any internal machines queried the suspicious domain.
2. Identify the internal IP address (`principal.ip`) of the workstation making the connection.
3. Inspect HTTP web traffic from that internal IP to confirm whether payload communication occurred.
4. Review authentication events (`USER_LOGIN`) on that specific IP address to identify the affected employee account.
5. Check endpoint process launch logs (`PROCESS_LAUNCH`) to verify whether an unauthorized executable ran on the host.
---
## Investigation Steps & UDM Query Breakdown

## Step 1: Search for DNS Queries to the Malicious Domain
Before investigating individual workstations, I queried DNS resolution logs to confirm if any internal host attempted to contact the flagged domain.
```text
metadata.event_type = "NETWORK_DNS" AND target.hostname = "malicious-c2-domain.com"
```
# Query Breakdown:
`metadata.event_type = "NETWORK_DNS"`: Filters Chronicle's Unified Data Model specifically for Domain Name System (DNS) resolution events, ignoring unrelated system logs.
`AND`: Logical operator requiring both conditions to be true for an event to appear in the results.
`target.hostname = "malicious-c2-domain.com"`: Checks the destination hostname field against the known malicious Indicator of Compromise (IoC).
# What I Observed:
Chronicle returned three matching DNS lookup events originating from an internal workstation with the source IP address 10.0.4.15.
# Why I ran this code:
Malware relies on DNS lookups to translate domain names into IP addresses before communicating with an attacker's command-and-control server. Running this query confirmed internal contact with the threat indicator and isolated the affected endpoint IP.

## Step 2: Trace Outbound HTTP Traffic from the Infected Workstation
After identifying the internal workstation IP (10.0.4.15), I searched for web traffic originating from that machine to verify whether it established an active connection after resolving the domain.
```text
principal.ip = "10.0.4.15" AND metadata.event_type = "NETWORK_HTTP
```
# Query Breakdown:
`principal.ip = "10.0.4.15"`: In Chronicle's UDM schema, `principal` represents the entity originating the activity. This filters for all traffic coming from the flagged internal workstation.
`metadata.event_type = "NETWORK_HTTP"`: Narrows the investigation to web traffic to check for follow-up communication or file downloads.
# What I Observed:
The workstation initiated an outbound HTTP GET request to malicious-c2-domain.com/update.bin seconds after the initial DNS query occurred.
# Why I ran this code:
Seeing a DNS lookup shows intent, while inspecting subsequent HTTP connections confirms whether the workstation successfully communicated with the external server and attempted to download a payload.

## Step 3: Identify the Logged-In User on the Compromised Host
Because IP addresses identify machines rather than people, I queried authentication logs on 10.0.4.15 to determine which employee was logged in during the suspicious activity.
`principal.ip = "10.0.4.15" AND metadata.event_type = "USER_LOGIN"`
# Query Breakdown:
` principal.ip = "10.0.4.15"`: Keeps the search anchored to the compromised workstation.
`metadata.event_type = "USER_LOGIN"`: Filters for user authentication events recorded on that host around the time of the malicious network traffic.
# What I Observed:
An active login session was recorded for employee account m.garcia on workstation FINANCE-WKS09 prior to the outbound DNS and HTTP requests.
# Why I ran this code:
Mapping the workstation IP to a specific employee username allows the SOC team to contact the user, verify whether they clicked a suspicious link, and reset potentially compromised credentials.

## Step 4: Check for Suspicious Process Execution on the Host
Finally, I inspected endpoint execution telemetry on FINANCE-WKS09 to verify whether a malicious program or unauthorized script ran right before the outbound network connections.
`principal.hostname = "FINANCE-WKS09"` AND `metadata.event_type = "PROCESS_LAUNCH"`
# Query Breakdown:
`principal.hostname = "FINANCE-WKS09"`: Filters endpoint telemetry using the machine's asset hostname discovered during the login review.
`metadata.event_type = "PROCESS_LAUNCH"`: Displays programs and scripts executed on the endpoint.
# What I Observed:
A suspicious executable (invoice_viewer.exe) launched from the user's Downloads folder two seconds before the DNS query to malicious-c2-domain.com was recorded.
# Why I ran this code:
Reviewing process creation events confirms the root cause of the network alert, linking the external C2 callback directly to a malicious binary executed on the workstation so the incident can be escalated for containment and malware removal.

