#!/usr/bin/env python3
import systemd.journal

def main():
  print("[+] Starting SSH Brute Force Detector.")
  
  with systemd.journal.Reader() as journal:
    # seek to the end of the journal to get new entries
    journal.seek_tail()
    journal.get_previous()

    while True:
      try:
      # read and print log entries
        for entry in journal:
          if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
            # write your code here
            pass
            
      except KeyboardInterrupt:
        print("[+] Stopping SSH Brute Force Detector.")
        break

if __name__ == "__main__":
    main()
