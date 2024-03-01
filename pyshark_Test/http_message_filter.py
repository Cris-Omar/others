#!/usr/bin/env python3
import pyshark

# Open trace file
cap = pyshark.FileCapture('http-header-streams/data-exfiltration2.pcap')
print(cap)
