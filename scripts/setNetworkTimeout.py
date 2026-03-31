#!/usr/bin/env python3
import socket

ip = '192.168.1.7'
port = 2001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

DISCOVERY_PAYLOAD = bytes.fromhex(
    "00 00 04 50"
    "00 00 FF FF"
    "F0 30 00 20"
    "01 30 00 00"
)

s.sendall(DISCOVERY_PAYLOAD)
resp = s.recv(320)
print(resp.hex(" "))
s.close()
