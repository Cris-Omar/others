#!/usr/bin/env python3
from cysystemd.reader import JournalReader, JournalOpenMode
from datetime import datetime, timedelta

# Constants for brute force detection
THRESHOLD = 3  # Number of failed attempts
TIME_WINDOW = timedelta(minutes=1)  # Time window for counting attempts

def main():
    print("[+] Starting SSH Brute Force Detector.")
  
    journal_reader = JournalReader()
    journal_reader.open(JournalOpenMode.SYSTEM)
    journal_reader.seek_tail()
    journal_reader.previous(skip=0)

    # Dictionary to store failed login attempts per source IP
    failed_attempts = {}

    while True:
        try:
            # read and print log entries
            for entry in journal_reader:
                if 'sshd' in entry.data.get('SYSLOG_IDENTIFIER', ''):
                    if "Failed password for" in entry.data["MESSAGE"]:
                        source_ip = entry.data.get('MESSAGE', '').split()[-3]
                        timestamp_str = entry.data['SYSLOG_TIMESTAMP'].strip()  # Remove extra whitespace
                        timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')

                        # Check if source IP is in dictionary, if not, add it
                        if source_ip not in failed_attempts:
                            failed_attempts[source_ip] = {'count': 0, 'timestamp': timestamp}

                        # Check if the attempt is within the time window
                        if timestamp - failed_attempts[source_ip]['timestamp'] < TIME_WINDOW:
                            failed_attempts[source_ip]['count'] += 1
                        else:
                            failed_attempts[source_ip] = {'count': 1, 'timestamp': timestamp}

                        # Check if the number of failed attempts exceeds the threshold
                        if failed_attempts[source_ip]['count'] >= THRESHOLD:
                            print(f"[!] Brute force attack detected from {source_ip}")
                            # You can add further actions here, such as blocking the IP

        except KeyboardInterrupt:
            print("[+] Stopping SSH Brute Force Detector.")
            break

if __name__ == "__main__":
    main()
