# Incident Investigation in Splunk (SIEM)

# Project Overview
As an entry-level Security Operations Center (SOC) analyst, I conducted an incident investigation using **Splunk** (a Security Information and Event Management tool). The goal of this lab was to ingest and query raw security event logs using Splunk's Search Processing Language (SPL) to detect anomalous behavior, trace failed authentication spikes, identify potential brute-force attacks, and pinpoint compromised user accounts.

## Scenario
The organization's SIEM system collected security event logs from internal web servers and Windows workstations over a 24-hour monitoring period. An automated alert flagged an unusual spike in authentication errors. 

My task was to query the indexed log data (`index="main"`) using SPL commands to:
1. Explore the log structure and verify available event fields.
2. Filter for Windows failed logon events (`EventCode=4625`) to detect unauthorized access attempts.
3. Group and count failed login events by source IP address and target username using `stats count`.
4. Sort results to highlight the highest-volume threat actors.
5. Correlate failed login attempts with subsequent successful logins (`EventCode=4624`) to determine whether a breach occurred.
---
## Investigation Steps & SPL Query Breakdown

## Step 1: Baseline Log Exploration
Before writing specific detection filters, I ran a broad search against the primary index to inspect the available fields, timestamps, and log formats.
```spl
 index="main"
```
**Query Breakdown**:
`index="main"`: Instructs Splunk to search inside the default main data repository where the ingested security event logs are stored.
**What I Observed**:
In the left-hand Interesting Fields sidebar, I identified key parsed fields including EventCode, src_ip (source IP address), TargetUserName, ComputerName, and sourcetype.
**Why I ran this code**:
Reviewing baseline logs confirms that data ingestion is working properly and identifies the exact field names (case-sensitive) required for filtering.
## Step 2: Filter for Failed Authentication Events
To investigate potential password-guessing or brute-force attacks, I narrowed the search to isolate Windows failed login events.
```spl
index="main" EventCode=4625
```
**Query Breakdown**:
`index="main"`: Targets the primary log repository.
`EventCode=4625`: Filters specifically for Windows Security Event ID 4625, which logs every failed account logon attempt.
**What I Observed**:
The event count dropped from thousands of general system logs down to a concentrated set of failed authentication records occurring within a narrow timeframe.
**Why I ran this code**:
Filtering by EventCode=4625 removes routine operational noise (such as scheduled tasks and successful logins) so I could focus solely on rejected access attempts.
## Step 3: Aggregate and Count Failed Attempts by IP and User
Viewing individual failed events one by one makes it difficult to spot patterns. I used the pipe character (|) to pass the search results into a statistical counting command.
```spl
index="main" EventCode=4625
| stats count by src_ip, TargetUserName
| sort - count
```
**Query Breakdown**:
`|`: The pipe operator takes the output from the search on the left and feeds it as input into the command on the right.
`stats count by src_ip, TargetUserName`: Groups all matching failed login events together and calculates the total count for each unique combination of source IP address and targeted account name.
`sort - count`: Sorts the aggregated table in descending order (-), placing the highest number of failed attempts at the very top.
**What I Observed**:
One external IP address (198.51.100.42) generated over 150 failed login attempts against the admin_jdoe account within a 10-minute window, whereas normal employee typos averaged only 1 to 2 failures.
**Why I ran this code**:
Aggregating logs with stats count turns raw event streams into actionable intelligence, immediately revealing which IP addresses are conducting high-velocity brute-force attacks and which accounts are being targeted.
## Step 4: Check for Account Compromise (Failed Logins Followed by Success)
After identifying the targeted account (admin_jdoe) and suspect IP (198.51.100.42), I needed to verify whether the attacker eventually guessed the correct password and gained access.
```spl
index="main" src_ip="198.51.100.42" (EventCode=4625 OR EventCode=4624)
| table _time, EventCode, src_ip, TargetUserName, ComputerName
| sort _time
```
**Query Breakdown**:
src_ip="198.51.100.42": Isolates all network activity originating from the identified suspect IP address.
`(EventCode=4625 OR EventCode=4624)`: Searches for both failed logins (4625) and successful logins (4624). Parentheses ensure both event codes are evaluated for that specific IP.
`table _time, EventCode, src_ip, TargetUserName, ComputerName`: Formats the output into a clean, readable report showing only the essential investigation columns.
`sort _time`: Orders the events chronologically from oldest to newest so I could trace the exact sequence of events.
**What I Observed**:
Following 154 consecutive 4625 (Failed) events, a single 4624 (Successful Logon) event was recorded from 198.51.100.42 for admin_jdoe on workstation FINANCE-PC04.
**Why I ran this code**:
Determining whether a brute-force attack succeeded changes the incident priority from a blocked scan to an active account compromise requiring immediate containment (password reset and IP block).

