#!/usr/bin/env python3
import socket, struct
'''
KB=Knoweldge base:
https://www.opto22.com/support/resources-tools/knowledgebase/kb91081
https://www.opto22.com/support/resources-tools/knowledgebase/kb89636 # may be out of spec on firmware version.
https://www.opto22.com/support/resources-tools/knowledgebase/kb89670
https://www.opto22.com/support/resources-tools/knowledgebase/kb89676

KB89676 Addresses the fact that the ModbusTCP server may return error
KB89670 Addresses the stale ModbusTCP state, activation & bandwidth
KB89636 Addresses the TCP packet length of the ModbusTCP connections
KB91081 OptoMMP (TCP) or Modbus/TCP connection refused, possibly due to timeout.
#Address | KB  | SOLUTIONs 
0xF0380020 = kb91081 | set > 60K
'''


ip = '192.168.1.211'
port = 2001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Read 4 bytes from address F0380020
pkt = bytes([
    0, 0, 4, 80,      # header (read block request)
    0, 0, 255, 255,   # flags
    0xF0, 0x38, 0x00, 0x20,  # address
    0, 4, 0, 0        # length = 4 bytes
])

s.send(pkt)
resp = s.recv(24)

value = struct.unpack('>i', resp[16:20])[0]
print(value)

s.close()
