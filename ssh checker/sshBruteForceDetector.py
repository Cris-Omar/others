#!/usr/bin/env python3
import systemd.journal
from pprint import pprint

time_window = 60
threshold = 3

def compute_failure_event(session, event):
  print("[!] invalid login detected")

  event_message = event['MESSAGE']
  src_ip = event_message.split()[5]
  user = event_message.split()[3]


  if src_ip not in session:
     
     #create new session entry
     session[src_ip] = {
        'hits' : 1,
        'timestamp' : event['_SOURCE_REALTIME_TIMESTAMP'],
        'user' : user
     }

  else:
     delta = event['_SOURCE_REALTIME_TIMESTAMP'] - session[src_ip]['timestamp']

     if delta.seconds > time_window:
        # reset hit counter
        session[src_ip]['hits'] = 1
     else:
        #within time window:
        session[src_ip]['hits'] += 1

        #evaluate hit counter
        if session[src_ip]['hits'] > threshold: 
           print ('[!] Brute-Force attempt detected. Within the last ' + str(time_window) + 'seconds, an attacker tried at least' + str(threshold) + 'times to log in with an invalid pw!')

        #update timestamp
        session[src_ip]['timestamp'] = event['_SOURCE_REALTIME_TIMESTAMP']


def main():
  print("[+] Starting SSH Brute Force Detector.")
  
  #open a connection to systemd jornal
  with systemd.journal.Reader() as journal:
    # seek to the end of the journal to get new entries
    journal.seek_tail()
    journal.get_previous()

    #creating session variable
    session = {}

    #loop throuth journal entries:
    while True:
      try:
        # read and print log entries
        for entry in journal:
          #search for "sshd" in the "entry" dictionary b searching ba the "SYSLOG_IDENTIFIER" result.
          if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
              #if there is an entry that includes "Failed password for" in the "MESSAGE" entry, then..
              if "Failed password for" in entry["MESSAGE"]:
                 compute_failure_event(session, entry)
                
      #exit programm when user clicks "CTRL+C"
      except KeyboardInterrupt:
        print("[+] Stopping SSH Brute Force Detector.")
        break

if __name__ == "__main__":
    main()