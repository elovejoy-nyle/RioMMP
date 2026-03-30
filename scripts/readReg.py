#!/usr/bin/env python3
import socket
import struct
import csv
import sys
'''
registers from: 1465_OptoMMP_Protocol_Guide.pdf 
pg:123-126
there are more registers. corners were cut

'''
host = sys.argv[1] if len(sys.argv) > 1 else '10.1.0.156'
#host = '10.1.0.156'
port = 2001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

with open('a.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        reg = row[0].replace(" ", "")   # e.g. F030010C
        #print(f"###{reg}###")
        desc = row[1]

        addr = int(reg, 16)

        # build read block (same pattern as your example)
        myBytes = [
            0,0,4,80, 0,0,255,255,
            (addr>>24)&0xFF,
            (addr>>16)&0xFF,
            (addr>>8)&0xFF,
            addr&0xFF,
            0,4,0,0 # we're assuming every reg is 4bytes (its not)
        ]

        s.send(bytearray(myBytes))
        data = s.recv(24)
        val = struct.unpack('>I', data[16:20])[0]
        #out = open('reg.csv','w')
        #out.write(f"{reg},{desc},{val}\n")
        print(f"{reg},{desc},{val}")

s.close()

'''
address,desc,value
FFFFF0300000,Memory Map revision number,1
FFFFF0300004,Powerup Clear flag,0
FFFFF0300008,Busy flag,0
FFFFF030000C,I Last error code,57349
FFFFF0300010,Transaction label for previous transaction,1006632960
FFFFF0300012,Source address of the unit that sent the request,61488
FFFFF0300014,Error address for last error,4029678696
FFFFF0300018,Loader revision,0
FFFFF030001C,IP Firmware (kernel) revision,50659840
FFFFF0300020,Unit type of the device,259
FFFFF0300024,Hardware revision (Month),67962852
FFFFF0300025,Hardware revision (Day),218621056
FFFFF0300026,Hardware revision (Year),132415488
FFFFF0300028,Number of bytes of installed RAM,2147483648
FFFFF030002C,Pad for alignment,160
FFFFF030002E,ENET1 MAC address,10501381
FFFFF0300034,IP ENET1 TCP/IP address,167837852
FFFFF0300038,IP ENET1 TCP/IP subnet mask,4294967040
FFFFF030003C,IP ENET1 TCP/IP default gateway,167837697
FFFFF0300040,IP ENET1 DNS server address,134744072
FFFFF0300044,Reserved,0
FFFFF0300048,Device sends BootP or DHCP request when turned on,0
FFFFF030004C,Degrees are in F or C,1
FFFFF0300050,Reserved,0
FFFFF0300054,Watchdog time in milliseconds,0
FFFFF0300058,TCP/IP minimum Response Timeout (RTO),0
FFFFF030005C,Digital scan counter,0
FFFFF0300060,Analog and digital scan counter,7254457
FFFFF0300064,Initial RTO,0
FFFFF0300068,TCP number of retries,0
FFFFF030006C,TCP idle session timeout,0
FFFFF0300070,Ethernet errors: late collisions,0
FFFFF0300074,Ethernet errors: excessive collisions,0
FFFFF0300078,Ethernet errors: other,0
FFFFF030007C,Smart modules present,1
FFFFF0300080,Device’s part number,1196578349
FFFFF03000A0,Firmware version date,808988465
FFFFF03000B0,Firmware version time,808598066
FFFFF0300100,ARCNET reconfigs detected,0
FFFFF0300104,ARCNET reconfigs initiated by I/O unit,0
FFFFF0300108,Number of times the device closed the session because it was idle,0
FFFFF030010C,Milliseconds since powerup,73882846
FFFFF0300110,Ethernet MAC resets since powerup,0
FFFFF0300114,Digital output channel resets since powerup,0
FFFFF0300118,Digital interrupt failures since powerup,0
FFFFF030011C,Total number of PID loops available,4
FFFFF0300120,ARCNET transmit attempts since powerup,0
FFFFF0300124,ARCNET other,0
FFFFF0300128,ARCNET ACKs,7254498
FFFFF030012C,ARCNET delay between transmit attempt and ACK,0
FFFFF0300130,ARCNET timeout value,0
FFFFF0300134,ARCNET timeouts,0
FFFFF0300138,ARCNET receive interrupts,0
FFFFF030013C,Reserved,0
FFFFF0300140,Milliseconds per analog/HDD scan,1093646143
FFFFF0300144,Milliseconds per digital scan,0
FFFFF0300148,Number of digital modules supported,0
FFFFF030014C,Unique serial number,953189
FFFFF0300150,Multidrop address,0
FFFFF0300154,Baud rate,0
FFFFF0300158,Number of framing errors during serial transmission,0
FFFFF030015C,Number of FIFO overrun errors,0
FFFFF0300160,Elapsed time since powerup (seconds),73883
FFFFF0300164,Reserved,1
FFFFF0300228,Milliseconds since powerup (64-bit),0
FFFFF0300230,Current boot device,0
FFFFF0300234,Reserved,1
FFFFF0300248,Result of Status Area Write commands,0
FFFFF030024C,Firmware revision,0
FFFFF0300250,Number of writes to permanent storage,1
'''
