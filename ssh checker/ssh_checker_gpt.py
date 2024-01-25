#!/usr/bin/env python3
import systemd.journal
import subprocess

# Set the maximum number of allowed failed login attempts
MAX_FAILED_ATTEMPTS = 3

def main():
    print("[+] Starting SSH Brute Force Detector.")

    failed_attempts = {}

    with systemd.journal.Reader() as journal:
        # seek to the end of the journal to get new entries
        journal.seek_tail()
        journal.get_previous()

        while True:
            try:
                # read and print log entries
                for entry in journal:
                    if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
                        # Check for failed SSH login attempts
                        if 'Failed password' in entry.get('MESSAGE', ''):
                            username = entry.get('USER', 'unknown')
                            ip_address = entry.get('REMOTE_ADDR', 'unknown')

                            # Update the count of failed attempts for each user
                            failed_attempts[username] = failed_attempts.get(username, 0) + 1

                            print(f"Failed SSH login attempt for user {username} from {ip_address}")

                            # Check if the user has exceeded the maximum allowed failed attempts
                            if failed_attempts[username] >= MAX_FAILED_ATTEMPTS:
                                print(f"ALARM: Too many failed login attempts for user {username}. Setting alarm.")
                                set_alarm(username)
                                # Reset the counter for this user
                                failed_attempts[username] = 0

            except KeyboardInterrupt:
                print("[+] Stopping SSH Brute Force Detector.")
                break

def set_alarm(username):
    # You can customize the alarm action here.
    # For example, you can send an email, log to a file, or execute a command.
    # In this example, we'll print a message.
    print(f"ALARM: Sending alert for user {username}!")

if __name__ == "__main__":
    main()
