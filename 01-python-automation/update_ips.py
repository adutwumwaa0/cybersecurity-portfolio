"""
Algorithm for File Updates in Python
Removes revoked or compromised IP addresses from a network allowlist.
"""

def remove_ips(import_file, remove_list):
    # Read the current approved list
    with open(import_file, "r") as file:
        ip_addresses = file.read()

    # Convert string of IPs into an iterable list
    ip_addresses = ip_addresses.split()

    # Iterate through remove list and take out matching entries
    for element in remove_list:
        if element in ip_addresses:
            ip_addresses.remove(element)

    # Convert list back to string and write to file
    ip_addresses_str = " ".join(ip_addresses)
    with open(import_file, "w") as file:
        file.write(ip_addresses_str)

if __name__ == "__main__":
    target_file = "allow_list.txt"
    revoked_ips = ["192.168.1.2", "192.168.1.4"]
    remove_ips(target_file, revoked_ips)
    print("Allowlist updated successfully.")
