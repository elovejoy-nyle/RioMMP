#!/user/bin/env python3
import socket, struct

ip = '192.168.1.7'
port = 2001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# write 0 to FFFF F038 0020
pkt = bytes([
    0,0,4,16,        # write block request
    0,0,255,255,     # high address = FFFF
    240,56,0,32,     # low address  = F0380020
    0,16,0,0,        # length = 16 data bytes
    0,0,0,0,         # first 4 data bytes = 0
    0,0,0,0,0,0,0,0,0,0,0,0  # pad to 16 data bytes
])

s.send(pkt)
resp = s.recv(12)
print(struct.unpack('>i', resp[4:8])[0])  # 0 = success
s.close()
