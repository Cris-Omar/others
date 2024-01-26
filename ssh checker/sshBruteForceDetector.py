#!/usr/bin/env python3
import systemd.journal
import time

def main():
  print("[+] Starting SSH Brute Force Detector.")
  
  failedAttempts = {}
  
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
          #search for "sshd" in the "entry" dictionary b searching ba the "SYSLOG_IDENTIFIER" result.
          if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
              #if there is an entry that includes "Failed password for" in the "MESSAGE" entry, then..
              if "Failed password for" in entry["MESSAGE"]:
                
                #splitting output into multiple words
                parts = entry['MESSAGE'].split()
                #getting the 6th word of the "MESSAGE" entry data
                ipAddress = parts[5]
                userName = parts[3]
                #"MONOTONIC_TIMESTAMP" Monotonic time starts at an arbitrary point. It cannot move backwards. Finally, and most importantly, it is completely independent of the system clock
                timeStamp = entry['__MONOTONIC_TIMESTAMP']

                #############################CHECK THIS:
                if userName in failedAttempts:
                  # Update the timestamp and increment the count
                  last_timestamp, count = failedAttempts[userName]
                  if timeStamp - last_timestamp >= 60:
                      count += 1
                      failedAttempts[userName] = (timeStamp, count)

                      # Check if the count exceeds 2 (3 failed attempts)
                      if count == 3:
                          print(f"The user {userName} with the IP Address {ipAddress} entered 3 wrong passwords in less than 1 minute.")
                          # Add your alerting mechanism here
                      else:
                          # Reset count if the timestamp difference is more than 1 minute
                          failedAttempts[userName] = (timeStamp, 1)
                  else:
                      # Add the user to the dictionary with initial values
                      failedAttempts[userName] = (timeStamp, 1)
                ##################################
                      
      #exit programm when user clicks "CTRL+C"
      except KeyboardInterrupt:
        print("[+] Stopping SSH Brute Force Detector.")
        break

if __name__ == "__main__":
    main()