###    getUptime.py >>python getUptime.py OR >>python getUptime.py 127.0.0.1

import sys
import socket
import struct
if len(sys.argv) < 2:   # if an arguement isn't included
    host = 'localhost'  # default to localhost
else:
    host = sys.argv[1]  # otherwise use the first argument

port = 2001 # default OptoMMP port number
# create socket with IPv4 family, and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use that socket connect to host:port tuple
s.connect((host, port))
# build uptime block request:                 F0  30  01  0C    <- uptime location in hex
myBytes = [0, 0, 4, 80,  0,  0,  255, 255,   240, 48,  1, 12,     0, 4, 0,0]

# send request and save the response
nSent = s.send(bytearray(myBytes)) # want nSent to be exactly 16 bytes
data = s.recv(24) # read response block is 24 bytes
data_block = data[16:20] # data_block is in bytes 16-19 for Read Response, stop at 20.

# decode bytearray in big-endian order (>) for integer value (i)
output = str(struct.unpack_from('>i', bytearray(data_block)))
# clip out first `(` and last two characters `,)` before printing
print 'uptime: ' + output[1:-2] + 'ms'
# close the socket:
s.close()
