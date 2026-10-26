# Program: Parse Failed SSH Logins
# Course: Google Cybersecurity Professional Certificate - Course 7
# Description: Parses an auth.log file to find failed login attempts and count them per IP.

# The log file we want to analyze
log_file_path = "auth.log"

# Dictionary to hold IP addresses and their failed attempt counts
failed_attempts = {}

# Alert threshold for suspicious brute-force activity
ALERT_LIMIT = 5

print("Starting log investigation...")

# Open and read the log file line by line
with open(log_file_path, "r") as file:
    for line in file:
        # Check if the line represents a failed SSH login attempt
        if "sshd" in line and "Failed password" in line:
            # Split the line into individual words
            words = line.split()

            # Find the position of the word 'from' to grab the IP address right after it
            if "from" in words:
                from_index = words.index("from")
                ip_address = words[from_index + 1]

                # If IP is already in our dictionary, add 1; otherwise, start count at 1
                if ip_address in failed_attempts:
                    failed_attempts[ip_address] = failed_attempts[ip_address] + 1
                else:
                    failed_attempts[ip_address] = 1

# Display the findings
print("\n--- Failed Login Summary ---")
for ip, count in failed_attempts.items():
    if count >= ALERT_LIMIT:
        print(f"IP: {ip} | Failed Attempts: {count} ---> [ALERT: Potential Brute-Force]")
    else:
        print(f"IP: {ip} | Failed Attempts: {count}")

print("-----------------------------")
