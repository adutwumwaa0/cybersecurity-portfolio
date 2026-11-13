# Algorithm for File Updates in Python

# Project Overview
As an entry-level security analyst, I developed a Python script to automate the maintenance of an IP address allowlist (`allow_list.txt`). In a healthcare organization, access to restricted patient records is controlled by an allowlist of employee IP addresses. Rather than manually searching and editing text files—which introduces human error—I built an algorithm that reads the existing allowlist, cross-references it against a `remove_list` of revoked IP addresses, deletes any matching entries, and overwrites the file with the updated list.

## Scenario
The security team regularly updates the `"allow_list.txt"` file to revoke access for employees who change departments or leave the organization. A separate list named `remove_list` contains the IP addresses that should no longer have access to the restricted subnetwork.

My task was to build a Python algorithm to:
1. Open the `"allow_list.txt"` file and read its contents into a string variable.
2. Convert the string of IP addresses into a Python list using `.split()` so individual elements can be manipulated.
3. Iterate through the `remove_list` using a `for` loop and check if each IP exists in the allowlist.
4. Remove unauthorized IP addresses using the `.remove()` method.
5. Convert the cleaned list back into a single string using `.join()` and overwrite `"allow_list.txt"` with the revised data.
---
## Algorithm Development & Code Breakdown

## Step 1: Open the File That Contains the Allow List
First, I assigned the file name `"allow_list.txt"` to the `import_file` variable and used a `with` statement alongside `open()` in read mode (`"r"`) to access the file.
```python
import_file = "allow_list.txt"
with open(import_file, "r") as file:
# Code Breakdown:
`import_file = "allow_list.txt"`: Stores the file path as a string variable so it can be reused cleanly across the script.
`with`: A context manager that automatically handles closing the file once the indented block finishes executing, preventing memory leaks or file corruption.
`open(import_file, "r")`: Opens the target file in read-only mode ("r").as file: Assigns the opened file object to the temporary variable file.
# What I Observed:
The script successfully established a read connection to "allow_list.txt" without altering the underlying data.
# Why I ran this code:
Before any IP addresses can be evaluated or removed, Python must open the file resource safely so its contents can be loaded into memory.

## Step 2: Read the File Contents
Inside the with block, I applied the .read() method to extract the text from the file and store it in a string variable named ip_addresses.
```
with open(import_file, "r") as file:
    ip_addresses = file.read()
    ```
    Code Breakdown:
`ip_addresses`: The variable created to hold the text contents of the file.
`file.read()`: Reads the entire file content and returns it as a single continuous string.
# What I Observed:
The ip_addresses variable now held all IP addresses from "allow_list.txt" as a single block of text separated by whitespace and newline characters.
# Why I ran this code:
Python cannot directly use list methods on an external .txt file; .read() brings the raw data into a string variable inside the program.

# Step 3: Convert the String into a List
To remove individual IP addresses, I needed to convert ip_addresses from a single text string into a Python list using the .split() method.
```
ip_addresses = ip_addresses.split()
```
# Code Breakdown:
`ip_addresses.split()`: Splits a string into a list of individual items. When called with empty parentheses, .split() automatically divides the string at every space or newline character (\n).
# What I Observed:
The single string transformed into a structured Python list (e.g., ['192.168.100.1', '192.168.100.5', '10.0.0.10']), where each IP address is an indexed element.
# Why I ran this code:
Removing a specific IP address from a long text string is error-prone because partial string matches could corrupt neighboring IPs. Converting the string into a list ensures each IP address is treated as a complete, distinct element.

  # Step 4: Iterate Through the Remove List and Delete Matches
Next, I created a for loop to iterate through each IP in remove_list, used an if conditional to check if that IP was present in ip_addresses, and removed it using .remove().
```
for element in remove_list:
    if element in ip_addresses:
        ip_addresses.remove(element)
      ```
Code Breakdown:
`for element in remove_list:`: Loops through the remove_list one item at a time, assigning the current IP to the loop variable element.
`if element in ip_addresses:`: Evaluates whether the current element exists inside the ip_addresses list before attempting deletion.
`ip_addresses.remove(element)`: Deletes the matching IP address from the ip_addresses list.
# What I Observed:
Every IP address found in both remove_list and ip_addresses was stripped out of the ip_addresses list without throwing a ValueError.
# Why I ran this code:
Using if element in ip_addresses prevents the script from crashing if an IP in remove_list was already removed earlier, while .remove() enforces the Principle of Least Privilege by revoking unauthorized access.

# Step 5: Update the File with the Revised List of IP Addresses
Finally, I converted the cleaned ip_addresses list back into a newline-separated string using .join(), and opened "allow_list.txt" in write mode ("w") to overwrite the old contents.
```
ip_addresses = "\n".join(ip_addresses)

with open(import_file, "w") as file:
    file.write(ip_addresses)
```
Code Breakdown:
`"\n".join(ip_addresses)`: Combines all elements of the ip_addresses list back into a single string, placing a newline character (\n) between each IP address so every IP sits on its own line.
`with open(import_file, "w") as file:`: Reopens "allow_list.txt" in write mode ("w"), which clears the existing file contents and prepares it for new data.
`file.write(ip_addresses)`: Writes the updated string of authorized IP addresses into the file.
# What I Observed:
Opening `"allow_list.txt"` after running the script confirmed that all unauthorized IP addresses in remove_list were gone, while all valid employee IP addresses remained intact on separate lines.
# Why I ran this code:
Python's .write() method requires a string argument rather than a list. Using "\n".join() restores the original file formatting before "w" mode commits the updated access control list to disk.

    
