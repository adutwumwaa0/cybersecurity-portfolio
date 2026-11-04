# Linux File Permissions & Access Control Audit

## Project Overview
As an entry-level security analyst at a healthcare organization, I performed an audit of the file system permissions on a Linux server. The goal of this project was to inspect the access rights on sensitive files and directories in the `/home/researcher2/projects` folder, identify security risks where files were overly permissive, and apply the Principle of Least Privilege using Linux CLI commands so that unauthorized users cannot read or tamper with critical data.

---

## Scenario
The organization's server contains a project directory used by internal researchers and analysts. An internal audit revealed three primary security concerns:
1. The `project_k.txt` file contained sensitive research data, but the "other" category had write access.
2. An archive file named `.project_x.txt` was a hidden file that should not have been accessible to the group or others.
3. The entire `/home/researcher2/projects/drafts` directory was overly permissive, allowing non-team members to modify draft reports.

---

## Investigation & Remediation Steps

### Step 1: Check Current Working Directory
Before making any changes, I checked my current location in the terminal to ensure I was in the proper working path.

```bash
pwd
Command line breakdown:
pwd: Print Working Directory.
Why I ran it: Confirmed I was located in /home/researcher2 before attempting to navigate or modify files.

Step 2: Inspect Directory Contents and Permissions
Next, I navigated to the target directory and inspected all files, including hidden files, along with their 10-character permission strings.
cd projects
ls -la
Command line breakdown:
cd projects: Changes the working directory to projects.
ls -la: Lists all directory contents. The -l flag displays the long listing format (permissions, owner, group, size, date), and -a shows all files, including hidden files that start with a dot (.).
My Observation:
The file project_k.txt had the permission string -rw-rw-rw-. This meant the user, the group, and other (everyone on the system) had write permissions.
The hidden file .project_x.txt had permissions -rw-r--r--, which meant unauthorized users could still view confidential draft data.

Step 3: Remove Unauthorized Write Permissions on a Critical File
To follow the principle of least privilege, "other" should never have write access to critical project files. I used the chmod command with symbolic permissions to remove write access from "other".
chmod o-w project_k.txt
Command line breakdown:
chmod: Change mode command used to alter file permissions.
o-w: Represents "other" (o), minus (-), write (w).
project_k.txt: The specific file target.
Verification: ls -l project_k.txt 
Result: The permission string changed from -rw-rw-rw- to -rw-rw-r--. Now, regular users outside the group can read the file if needed, but they cannot delete or alter its contents.

Step 4: Secure a Hidden Archive File
The file .project_x.txt is an internal archive that only the file owner should be able to read and write. Both the "group" and "other" categories should have no access.
chmod go-r .project_x.txt
Command line breakdown:
go-r: Targets both group (g) and other (o), and removes (-) read (r) access.
.project_x.txt: The hidden file target.
Verification: ls -la .project_x.txt
Result: The permission string changed to -rw-------. The owner retains full read and write access, while group members and all other users are completely locked out.
Step 5: Restrict Access to the Drafts Directory
Finally, I audited the drafts subdirectory. Directories require execute (x) permissions to enter them, but users outside the team should not be able to enter or modify drafts.
chmod g-w,o-rwx drafts
Command line breakdown:
g-w: Removes write access from the group so team members cannot accidentally delete the directory.
,: Separates multiple permission changes in a single command.
o-rwx: Strips read, write, and execute permissions entirely from "other".
drafts: The target directory.
ls -ld drafts 
Result: The -d flag displays the directory properties instead of its contents. The permissions now reflect drwxr-x---, ensuring no outside user can enter (x), list (r), or create files inside (w) this folder.

Key Takeaways
Principle of Least Privilege: Users should only be given the minimum permission level required to perform their daily duties.
Symbolic Mode: chmod with u (user), g (group), and o (other) combined with + or - makes it easy to add or remove granular rights without changing the entire permission string.
Hidden Files (.): Hidden files are not inherently secure; their file permissions must be audited and hardened just like visible files.
