#!/usr/bin/env python3
import numpy

###### Configuration ######
log_access_path = './access.log'
log_auth_path = './auth.log'
###########################


###### Functions #############

def load_logfile(filename):
	with open(filename) as f:
		content = f.readlines()
		content = [line.strip() for line in content]    # Removes Newline-Character
	return content


def main():
	print("[+] Starting Log Analyzer")

	print("[+] Loading Logs")
	log_auth_events = load_logfile(log_auth_path)

	print("[+] Looking for Attacker IP")
	failed_attempts_per_ip = {}
	for log_entry in log_auth_events:
		if "Failed password for" in log_entry:
			ip_address = log_entry.split()[-4]
			failed_attempts_per_ip[ip_address] = failed_attempts_per_ip.get(ip_address, 0) + 1

	print("[!] Following Attacker IPs have been found:")
	for ip, attempts in failed_attempts_per_ip.items():
		print(f"{ip}	>>	{attempts} failed attempts")


if __name__ == "__main__":
	main()