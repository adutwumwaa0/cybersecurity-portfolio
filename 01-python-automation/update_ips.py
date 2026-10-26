# Program: Update IP Allowlist
# Course: Google Cybersecurity Professional Certificate - Course 7
# Description: This script removes unauthorized IP addresses from an allowlist file.

# Define the file containing the allowlist
import_file = "allow_list.txt"

# List of IP addresses that need to be removed from the allowlist
remove_list = ["192.168.1.2", "192.168.1.4", "10.0.0.99"]


def update_file(import_file, remove_list):
    # Step 1: Open the file and read its contents
    with open(import_file, "r") as file:
        ip_addresses = file.read()

    # Step 2: Convert the string into a list using .split()
    ip_addresses = ip_addresses.split()

    # Step 3: Iterate through the remove_list to find and remove target IPs
    for element in remove_list:
        if element in ip_addresses:
            ip_addresses.remove(element)
            print(f"Removed IP: {element}")
        else:
            print(f"IP not found: {element}")

    # Step 4: Convert the list back into a string separated by spaces
    ip_addresses = " ".join(ip_addresses)

    # Step 5: Open the file in write mode to overwrite it with the updated list
    with open(import_file, "w") as file:
        file.write(ip_addresses)

    print("\nAllowlist update complete!")


# Run the function
update_file(import_file, remove_list)
