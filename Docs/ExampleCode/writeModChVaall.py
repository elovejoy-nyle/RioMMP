###    writeModChVal.py >>python writeModChVal.py <module #> <channel #> <1|0>
import sys
import socket
import struct

host = '127.0.0.1' # groov EPIC IP

if(len(sys.argv) != 4): # If the module, channel, and/or value are not provided.
        print 'Please provide module #, channel #, and value [1|0].'
        print 'Exiting script . . .'
        exit() # Inform the user and exit the script.

port = 2001 # default OptoMMP port number
tcode = 1   # write block request
modN = int(sys.argv[1]) # first argument
chN = int(sys.argv[2])  # second argument
val = int(sys.argv[3])  # third argument

# create socket with IPv4 family, and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use that socket connect to host:port tuple
s.connect((host, port))
# Calculate the destination offset:
# EPIC digital write start address = 0xF0220000
dest = 0xF0220000 + (modN * 0x1000) + (chN * 0x40)
# build the write block request: 
myBytes = [0, 0, (1 << 2), (tcode << 4), 0, 0, 255, 255, int(str(hex(dest))[2:4],16), int(str(hex(dest))[4:6],16), int(str(hex(dest))[6:8],16), int(str(hex(dest))[8:10],16), 0,16,  0,0,  0,0,0,val] + [0]*12;
# + [0]*12 to fill the write block and make it the correct size.

# send the write block request and save the response:
nSent = s.send(bytearray(myBytes)) # want nSent to be exactly 32 bytes
data = s.recv(12) # write block response is 12 bytes
data_block = data[4:8] # data_block is in bytes 4-7 for Write Response, stop at 8.

# decode bytearray in big-endian order(>) for integer value (i)
output = str(struct.unpack_from('>i', bytearray(data_block)))
# clip out first `(` and last two characters `,)` to get the status code number
status = int(output[1:-2])
if (status == 0):
    print 'Write success ' + str(status)
else:
    print 'Write failure ' + str(status)
#close the socket:
s.close()
