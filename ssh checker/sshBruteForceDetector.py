#!/usr/bin/env python3
import systemd.journal

def main():
  print("[+] Starting SSH Brute Force Detector.")
  
  #open a connection to systemd jornal
  with systemd.journal.Reader() as journal:
    # seek to the end of the journal to get new entries
    journal.seek_tail()
    journal.get_previous()

    #loop throuth journal entries:
    while True:
      try:
        # read and print log entries
        for entry in journal:
          #search for sshd entries
          if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
            if "Failed password for" in entry["MESSAGE"]:
              
              #splitting output
              parts = entry["MESSAGE"].split()
              print(entry)
              print(parts)

      #exit programm when user clicks "CTRL+C"
      except KeyboardInterrupt:
        print("[+] Stopping SSH Brute Force Detector.")
        break

if __name__ == "__main__":
    main()