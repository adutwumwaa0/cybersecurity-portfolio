# Python Automation: IP Allowlist Maintenance

## Lab Overview
In access management, maintaining IP allowlists by hand is prone to human error. In this lab, I developed a Python script that automates the process of removing unauthorized IP addresses from a firewall or system allowlist.

## Key Python Functions Used
* `open(..., "r")` & `open(..., "w")`: Context managers used to read and overwrite configurations.
* `.read()`: Extracts the entire text file into memory as a string.
* `.split()`: Parses the string into a list of separate IP strings.
* `.remove()`: Deletes the target elements matching the removal list.
* `.join()`: Reconstructs the cleaned list into a standardized file string.
