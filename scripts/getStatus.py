#!/usr/bin/env python3
import socket
import struct

ip = "192.168.1.211"
port = 2001

def u32be(b):
    return struct.unpack(">I", b)[0]

def cstr(b):
    return b.split(b"\x00", 1)[0].decode("ascii", errors="replace")

def fmt_ip(b):
    return ".".join(str(x) for x in b)

def fmt_mac(b):
    return ":".join(f"{x:02x}" for x in b)

MODEL_NAMES = {
    0x00000103: "GRV-R7-MM1001-10",
    0x00000108: "GRV-R7-MM2001-10",
}

DISCOVERY_PAYLOAD = bytes.fromhex(
    "00 00 04 50"
    "00 00 FF FF"
    "F0 30 00 20"
    "01 30 00 00"
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.sendall(DISCOVERY_PAYLOAD)
resp = s.recv(320)
s.close()

print(f"response length : {len(resp)} bytes")
#print(f"status          : {u32be(resp[4:8])}")
print()

# Verified fields from your captured response layout
model_code = u32be(resp[16:20])

hw_month = resp[20]
hw_day   = resp[21]
hw_year  = struct.unpack(">H", resp[22:24])[0]

# The earlier parser was off by 2 bytes here.
mac_addr = resp[30:36]
ip_addr  = resp[36:40]
subnet   = resp[40:44]
gateway  = resp[44:48]

part_string = cstr(resp[112:144])
fw_date     = cstr(resp[144:160])
fw_time     = cstr(resp[160:176])

#print("decoded:")
print(f"model code      : 0x{model_code:08X}")
print(f"model name      : {MODEL_NAMES.get(model_code, 'unknown')}")
print(f"hw revision     : {hw_month:02d}/{hw_day:02d}/{hw_year:04d}")
print(f"mac             : {fmt_mac(mac_addr)}")
print(f"ip              : {fmt_ip(ip_addr)}")
print(f"subnet          : {fmt_ip(subnet)}")
print(f"gateway         : {fmt_ip(gateway)}")
print(f"part string     : {part_string}")
print(f"firmware date   : {fw_date}")
print(f"firmware time   : {fw_time}")
print()
#print("raw:") 
#print(resp.hex(" "))
'''
response length : 320 bytes
status          : 0

decoded:
model code      : 0x00000103
model name      : GRV-R7-MM1001-10
hw revision     : 04/13/2020
mac             : 00:a0:3d:05:62:67
ip              : 192.168.1.211
subnet          : 255.255.255.0
gateway         : 192.168.1.1
part string     : GRV-R7-MM1001-10
firmware date   : 02/25/2026
firmware time   : 04:18:44

'''
