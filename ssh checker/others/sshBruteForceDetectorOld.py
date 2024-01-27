import re
from collections import defaultdict

# Your existing code to iterate through journal entries
with systemd.journal.Reader() as journal:
    journal.seek_tail()
    journal.get_previous()

    # Dictionary to store user-wise failed login attempts count
    failed_attempts_count = defaultdict(int)

    while True:
        try:
            for entry in journal:
                if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
                    if "Failed password for" in entry["MESSAGE"]:
                        # Extracting user, IP address, and timestamp using regular expressions
                        match = re.search(r'Failed password for (\S+) from (\S+) port \d+ ssh2', entry["MESSAGE"])
                        if match:
                            user = match.group(1)
                            ip_address = match.group(2)
                            timestamp = entry["SYSLOG_TIMESTAMP"]

                            # Update failed attempts count for the specific user
                            failed_attempts_count[user] += 1

                            # Print or use the extracted data as needed
                            print(f"User: {user}, IP Address: {ip_address}, Timestamp: {timestamp}, Failed Attempts Count: {failed_attempts_count[user]}")

        except KeyboardInterrupt:
            print("[+] Stopping SSH Brute Force Detector.")
            break
