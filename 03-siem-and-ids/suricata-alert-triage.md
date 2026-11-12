# Intrusion Detection Analysis with Suricata (IDS)

# Project Overview
As an entry-level Security Operations Center (SOC) analyst, I conducted network intrusion detection and alert triage using **Suricata** (an open-source Intrusion Detection System). The goal of this lab was to inspect custom Suricata signature rules, run Suricata against a captured packet file (`sample.pcap`), analyze triggered alerts in `fast.log` and `eve.json`, and build a custom rule to detect unauthorized HTTP traffic.

## Scenario
The security monitoring team suspected unauthorized web communications and potential port scanning on an internal subnet. A packet capture file (`sample.pcap`) and a custom signature file (`custom.rules`) were placed on a Linux analysis machine.

My task was to use the Linux command line and Suricata to:
1. Inspect the syntax and structure of an existing Suricata detection rule inside `custom.rules`.
2. Run Suricata in offline replay mode against `sample.pcap` using our custom ruleset.
3. Examine `fast.log` to triage triggered alerts, identifying source/destination IP addresses, ports, and signature IDs.
4. Query `eve.json` to inspect deep application-layer telemetry for forensic verification.
5. Construct a custom Suricata rule to detect unencrypted plaintext password transmissions over HTTP.
---
## Investigation Steps & Command Breakdown

## Step 1: Inspect the Custom Suricata Rule File
Before running the intrusion detection engine, I examined the contents of `custom.rules` to verify the active signature syntax.
```bash
cat custom.rules
```
# Command Breakdown:
`cat`: Linux utility that reads a file and prints its contents directly to the terminal screen.
`custom.rules`: The signature file containing our network detection rules.
# What I Observed:
The file contained the following signature definition:`alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"GET on wire"; flow:established,to_server; content:"GET"; http_method; sid:1000001; rev:1;)`
`alert`: The action Suricata takes when network traffic matches the rule (generates an alert log entry).
`http`: Specifies the application protocol being inspected.
`$HOME_NET any -> $EXTERNAL_NET any`: The rule header defining traffic direction—from any port on the internal network ($HOME_NET) to any port on an external network ($EXTERNAL_NET).
`msg:"GET on wire"`: The human-readable alert description logged when the rule triggers.
`sid:1000001`: Signature ID—a unique numeric identifier assigned to this specific rule.
`rev:1`: Revision number tracking updates to the signature.
# Why I ran this code:
Reviewing the rule header and options before running Suricata ensures I understand exactly what network behavior triggers an alert and helps distinguish legitimate activity from suspicious traffic.

## Step 2: Run Suricata Against the Packet Capture File
Next, I executed Suricata in offline mode to scan sample.pcap using only the signatures defined in custom.rules.
`sudo suricata -r sample.pcap -S custom.rules -k none`
# Command Breakdown:
`sudo`: Executes Suricata with root privileges so it can write alert logs to protected system directories (/var/log/suricata/).
`suricata`: Invokes the Suricata IDS engine.
`-r sample.pcap`: Runs Suricata in offline PCAP replay mode, reading packets from sample.pcap instead of listening on a live network adapter.
`-S custom.rules`: Directs Suricata to load only the rules inside custom.rules rather than all default system rulesets.
`-k none`: Disables packet checksum verification.
# What I Observed:
Suricata processed all packets in sample.pcap and printed a summary confirming that packets were decoded, inspected against 1 loaded rule, and logged without checksum errors.
# Why I ran this code:
Running Suricata offline against a .pcap allows an analyst to test detection rules safely without affecting live network traffic. Using -k none is necessary in virtual lab environments because virtual network interfaces often alter packet checksums, which would otherwise cause Suricata to ignore valid packets.

## Step 3: Triage Triggered Alerts in fast.log
After Suricata finished inspecting the packet capture, I reviewed fast.log to see which alerts were generated.
`cat /var/log/suricata/fast.log`
# Command Breakdown:
cat: Prints the contents of the alert log file.
`/var/log/suricata/fast.log`: Suricata's concise alert log, recording each triggered rule on a single readable line.
# What I Observed:
The log displayed concise single-line alert entries, including a reconnaissance alert and our custom HTTP trigger:05/12-14:22:10.123456 [**] [1:1000002:1] ET SCAN Potential Nmap Port Scan Detected [**] [Priority: 2] {TCP} 192.168.1.50:49201 -> 192.168.1.1:8005/12-14:22:15.881204 [**] [1:1000001:1] GET on wire [**] [Priority: 3] {TCP} 192.168.1.50:51422 -> 93.184.216.34:80
# Why I ran this code:
fast.log gives a Tier 1 SOC analyst an immediate triage summary—showing the exact timestamp, Signature ID (1000002 and 1000001), alert message, protocol ({TCP}), internal source IP (192.168.1.50), and destination IP/port.

## Step 4: Inspect Detailed Event Telemetry in eve.json
To investigate the exact HTTP payloads and metadata behind the alerts, I queried Suricata's structured JSON log file.
`jq 'select(.event_type=="alert")' /var/log/suricata/eve.json`
# Command Breakdown:
`jq`: A command-line JSON processor used to parse and format structured JSON logs cleanly.
`'select(.event_type=="alert")'`: Filters the JSON records so only alert events are displayed, ignoring background flow and statistics logs.
`/var/log/suricata/eve.json`: Suricata's Extensible Event Format log containing rich application-layer metadata.
# What I Observed:
The JSON output revealed deep forensic context for the HTTP alert, including the exact requested URI path (/admin/login.php), HTTP status code, and client User-Agent string.
# Why I ran this code:
While `fast.log` confirms that an alert fired, `eve.json` provides the full application-layer details needed to verify whether the activity is a true positive incident or benign administrative traffic.

## Step 5: Write a Custom Rule to Detect Plaintext HTTP Passwords
Finally, I authored a custom signature to alert the SOC whenever unencrypted credentials are transmitted over HTTP port 80.
`alert http $HOME_NET any ->$EXTERNAL_NET 80 (msg:"SECURITY ALERT: Plaintext Password Detected in Outbound HTTP"; flow:to_server,established; content:"password="; nocase; sid:1000003; rev:1;)`

# Rule Breakdown:
`alert http $HOME_NET any -> $EXTERNAL_NET 80`:
Monitors outbound HTTP traffic from any internal host to any external server on port 80.
`flow:to_server,established`: Inspects only active, established TCP connections traveling toward the destination server.
`content:"password="; nocase;`: Searches the packet payload for the string password=, ignoring uppercase or lowercase variations.
`sid:1000003; rev:1;`: Assigns a unique custom Signature ID (1000003) and sets the initial revision to 1.
# What I Observed:
Testing this rule confirmed that Suricata immediately flags outbound web requests containing cleartext password parameters.
# Why I ran this code:
Transmitting passwords over unencrypted HTTP exposes user credentials to network eavesdropping. Creating a dedicated signature ensures automated detection whenever legacy or misconfigured applications send cleartext credentials across the network.
