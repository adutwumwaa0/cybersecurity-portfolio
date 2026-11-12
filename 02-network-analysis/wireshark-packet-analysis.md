# Network Packet Inspection with Wireshark

## Project Overview
As an entry-level security analyst, I investigated a captured network packet file (`.pcap`) using **Wireshark**. The objective of this lab was to analyze raw network traffic from an internal corporate network, examine the three-way handshake of a TCP session, identify unencrypted web communications that exposed user credentials, and trace DNS queries to identify external servers contacted by compromised internal machines.

---

## Scenario
A network monitoring tool flagged an alert indicating suspicious activity involving an internal workstation. An analyst on the team collected a packet capture file named `sample.pcap` during the alert window. 

My task was to open the capture file in Wireshark and use display filters to:
1. Isolate all network communications involving the suspect workstation IP address.
2. Analyze TCP connection states and inspect the TCP three-way handshake (`SYN`, `SYN-ACK`, `ACK`).
3. Investigate application-layer HTTP traffic to locate cleartext usernames and passwords.
4. Follow TCP communication streams to reconstruct complete web conversations.
5. Filter DNS queries to identify domain name resolution requests initiated from the internal network.

---

## Investigation Steps & Display Filter Breakdown
### Step 1: Open the Capture File and Filter by Suspect IP Address
After launching Wireshark and opening `sample.pcap`, the packet pane displayed thousands of background packets. To narrow the view specifically to the device under investigation (`192.168.1.105`), I entered an IP display filter into the filter toolbar.
```text
ip.addr == 192.168.1.105
Filter Breakdown:
ip.addr: Examines the Internet Protocol (IPv4) header for both source and destination addresses.
==: The comparison operator meaning "is equal to".
192.168.1.105: The specific internal IP address assigned to the investigated workstation.
Why I ran this code:
Raw packet captures contain broad background network noise (such as ARP broadcasts and internal discovery services). Applying ip.addr == 192.168.1.105 filtered out all unrelated traffic and isolated every incoming and outgoing conversation involving this machine.

Step 2: Analyze the TCP Three-Way Handshake
To confirm that legitimate network sessions were established between the client workstation and external web servers, I filtered for connection initiation requests.
tcp.flags.syn == 1
Filter Breakdown:
tcp.flags: Instructs Wireshark to inspect the control bits inside the Transmission Control Protocol (TCP) header.
.syn == 1: Targets packets where the SYN (Synchronize) flag bit is set to 1 (active).
What I Observed:I located the three sequential packets forming the complete TCP three-way handshake:Client $\rightarrow$ Server: A packet with [SYN] set, initiating the request to connect.Server $\rightarrow$ Client: A packet with [SYN, ACK] set, acknowledging the client's request and synchronizing sequence numbers.Client $\rightarrow$ Server: A packet with [ACK] set, confirming acknowledgment and completing the established connection.
Why I ran this code:
Verifying the full handshake confirmed that active, established communication occurred between the internal host and the external server. It also helped distinguish legitimate traffic from SYN scan floods, where an attacker sends multiple SYN packets without completing the handshake.

Step 3: Identify Unencrypted HTTP Requests and Plaintext Credentials
Because standard HTTP operates on port 80 without encryption, data submitted via web forms is transmitted in readable text. I applied a filter to check for HTTP form submissions.
http.request.method == "POST"
Filter Breakdown:
http: Directs Wireshark to inspect application-layer Hypertext Transfer Protocol traffic.
request.method: Focuses on the specific action requested by the client browser.
"POST": Limits results to packets where data is being sent or submitted to a web server (such as login pages).
What I Observed:
Wireshark highlighted an HTTP POST packet destined for /login.php.
Selecting the packet and expanding the HTML Form URL Encoded section in the packet details pane revealed the entered credentials in cleartext:
username: admin
password: Password123
Why I ran this code:
Attackers on the same subnet can use packet sniffers to steal user credentials if traffic is not encrypted. Isolating POST requests allowed me to verify whether sensitive user data was exposed without TLS/HTTPS encryption.
Step 4: Follow the Complete TCP Stream
Viewing an isolated packet only provides a single snapshot of data. To view the entire conversation between the client workstation and the web server in human-readable order, I reconstructed the stream.
Action Taken:
Right-clicked the HTTP POST packet in the packet list pane and selected Follow TCP Stream.
What I Observed:
Wireshark opened a conversation window with color-coded text:
Red text: Data sent from the client workstation (HTTP headers, user-agent, form variables, and credentials).
Blue text: Server responses (HTTP status codes, session cookies, and HTML markup).
Why I ran this code:
Following the stream allows an analyst to read the entire dialogue as a continuous transcript, verifying what the user submitted and how the web application responded (e.g., whether the authentication succeeded or redirected).
Step 5: Filter for Outbound DNS Resolution Queries
When malicious software or users communicate with external domains, the machine must first resolve domain names to IP addresses using DNS. I filtered for outgoing DNS lookup requests.
dns.flags.response == 0
Filter Breakdown:
dns: Filters for Domain Name System traffic (Port 53 UDP/TCP).
flags.response == 0: Identifies DNS requests (queries) sent by the client. A value of 1 indicates a response returned by a DNS server.
What I Observed:
The filtered view listed the exact hostnames queried by the internal machine, including queries to legitimate internal servers and an anomalous lookup request to an external unknown domain.
Why I ran this code:
Monitoring outbound DNS queries (response == 0) reveals external domains contacted by internal endpoints, helping analysts detect command-and-control (C2) domains, malicious downloads, or unauthorized external browsing.

