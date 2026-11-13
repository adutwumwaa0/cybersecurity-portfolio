# Network Traffic Analysis with tcpdump

## Project Overview
As an entry-level security analyst, I investigated a suspicious network event using the command-line packet sniffing tool `tcpdump`. The objective of this lab was to inspect live and captured network traffic on a Linux virtual machine, identify anomalous communication patterns, filter traffic by IP address and port, and inspect raw packet payloads to identify potential security incidents.

---

## Scenario
A network monitoring alert indicated suspicious incoming and outgoing traffic on an internal organization server. The investigation required:
1. Inspecting available network interfaces to confirm the active capture point.
2. Capturing and filtering network traffic using specific packet count thresholds.
3. Filtering packets by protocol, port, and IP address to isolate suspicious flows.
4. Reading and analyzing pre-captured `.pcap` files without resolving numeric IP addresses or port names.

---

## Investigation & Remediation Steps

Step 1: Identify Available Network Interfaces
Before capturing live network packets, I identified the active network interface available on the system.
```
bash
sudo tcpdump -D
```
# Command line breakdown:
`sudo`: Executes the command with root administrative privileges, required to open raw network sockets.
`tcpdump`: The packet sniffer utility.
`-D`: Lists all available network interfaces that tcpdump can capture on.
# Why I ran it: 
To determine the correct interface identifier (such as eth0) so that I did not attempt to capture on inactive or loopback interfaces.

## Step 2: Capture a Baseline Packet Sample
To confirm that network traffic was actively flowing through the target interface, I ran a basic live capture limited to a small sample size.
```
sudo tcpdump -i eth0 -v -c 5
```
# Command line breakdown:
`-i eth0`: Specifies the capture interface (eth0).
`-v`: Enables verbose output, displaying IP header details such as Time to Live (TTL), packet length, and protocol options.
`-c 5`: Sets a packet count threshold to halt execution automatically after capturing 5 packets.
# Why I ran it: 
Without the -c flag, tcpdump runs continuously until interrupted. Setting a limit prevents terminal buffer overflow during an active investigation.

## Step 3: Disable DNS and Port Resolution for Forensic Accuracy
By default, tcpdump attempts to resolve IP addresses into hostnames and port numbers into service names. To preserve the raw numeric values and reduce lookup latency, I added numeric flags.
```
sudo tcpdump -i eth0 -nn -c 5
```
# Command line breakdown:
`-nn`: Disables both hostname resolution (first n) and port service translation (second n).
# Why I ran it: 
Prevents tcpdump from converting port 80 to http or port 53 to domain, ensuring I saw exact IP addresses and port numbers. It also eliminates unnecessary reverse-DNS queries over the network during an incident.

## Step 4: Filter by Port and Protocol
The monitoring alert flagged potential unencrypted web communications and anomalous DNS traffic. I applied protocol-specific filters to isolate these streams.
# Filtering for Web Traffic (Port 80)
```
sudo tcpdump -i eth0 -nn -c 5 port 80
```
# Command line breakdown:
`port 80`: A primitive filter that directs tcpdump to capture packets where either the source or destination port matches HTTP port 80.
# Filtering for DNS Queries (Port 53 UDP)
```
sudo tcpdump -i eth0 -nn -c 5 udp port 53
```
# Command line breakdown:
`udp port 53`: Combines the transport protocol (udp) with the service port (53), isolating domain name resolution requests and responses.

## Step 5: Filter by Source and Destination Host
To investigate an external host suspected of reconnaissance or data exfiltration, I filtered traffic linked to a specific IP address (192.168.1.100).
```
sudo tcpdump -i eth0 -nn -c 5 host 192.168.1.100
```
# Command line breakdown:
`host 192.168.1.100`: Captures any packet where 192.168.1.100 appears as either the source or destination address.
# Refining Directionality:
To view only incoming packets: `sudo tcpdump -i eth0 -nn -c 5 src host 192.168.1.100`
To view only outgoing packets: `sudo tcpdump -i eth0 -nn -c 5 dst host 192.168.1.100`

## Step 6: Inspect Packet Payloads in ASCII Format
To determine whether an HTTP session carried unencrypted sensitive text, I captured packets and displayed their data payloads in ASCII characters.
```
sudo tcpdump -i eth0 -nn -A -c 5 port 80
```
# Command line breakdown:
`-A`: Prints packet payload contents in ASCII text format alongside header data.
# My Observation:
Inspecting the ASCII output revealed plaintext HTTP request headers (such as GET /index.html HTTP/1.1 and Host: example.com), confirming that the communication was completely unencrypted.

## Step 7: Read and Analyze a Forensic PCAP File
In incident response workflows, analysts often examine offline capture files rather than live feeds. I analyzed an archived capture file named capture.pcap.
```
sudo tcpdump -nn -r capture.pcap -c 10
```
# Command line breakdown:
`-r capture.pcap`: Reads network packets from a saved file instead of listening on a live interface.
`-c 10`: Limits display to the first 10 packets stored in the file.
# Why I ran it: 
Allows offline forensic reproduction of security events without altering or replaying the actual network traffic.
