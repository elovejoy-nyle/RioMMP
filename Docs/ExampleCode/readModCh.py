###    readModCh.py >>python readModCh.py <module #> <channel #>
import sys
import socket
import struct

host = '127.0.0.1' # groov EPIC IP

if(len(sys.argv) != 3): # If the module and/or channel are not provided.
    print 'Please provide module # and channel #.'
    print 'Exiting script . . .'
    exit() # Inform the user and exit the script.

port = 2001 # default OptoMMP port number
tcode = 5   # read block request
modN = int(sys.argv[1]) # first argument
chN = int(sys.argv[2])  # second argument

# create socket with IPv4 family, and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use that socket connect to host:port tuple
s.connect((host, port))
# Calculate the destination offset:
# EPIC digital read start address = 0xF01E0000
dest = 0xF01E0000 + (modN * 0x1000) + (chN * 0x40)
# build the read block request:
myBytes = [0, 0, (1 << 2), (tcode << 4), 0, 0, 255, 255, int(str(hex(dest))[2:4],16), int(str(hex(dest))[4:6],16), int(str(hex(dest))[6:8],16), int(str(hex(dest))[8:10],16), 0, 16, 0, 0];

# send the read block request and save the response:
nSent = s.send(bytearray(myBytes)) # want nSent to be exactly 16 bytes
data = s.recv(24) # read block response is 24 bytes
data_block = data[16:20] # data_block is in bytes 16-19 for Read Response, stop at 20.

# decode bytearray in big-endian order (>) for integer value (i)
output = str(struct.unpack_from('>i', bytearray(data_block)))
# clip out first `(` and last two characters `,)` before printing
print 'module ' + str(modN) + ', point ' + str(chN) + ' = ' + output[1:-2]
#close the socket:
s.close()
