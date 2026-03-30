########## Using OptMMP!####################
https://docs.google.com/spreadsheets/d/1pteNGGcYGjEugrDHnax--SiNVR0sKQ_OqQUhZdeJIjY/edit?usp=sharing
The General MMP settings on the RIOs is just a list of addresses, and their indexes, (no description)
So I made this list, and cross referenced it with the documentation. 
Thats the fist 255 entries. 
index 46,47 upper and lower clamps, that looks interesting. 

The other reason I wanted to make this list is 
the listed firmware updates modify the MMP settings per firmware version, 
and those changes are hard to track on the opto22 website.   
Here we have firmware version grv-r7-mm1001-10-4.1.0-b.74.s we care about, 

#thought: maybe the entire opto provisioning proces can be performed via MMP script  
Scripts folder: read registers script, (TODO):: write registers  
  
myBytes = [  0, 0, 4, 80,  0, 0, 255, 255,  240, 48, 1, 12,  0, 4, 0, 0]

  0, 0, -> destination ID
  4,    -> read length 
  80,   -> tcode (command type: r,w,x) 80-read block, 16=write block
  0, 0, -> high sourcc ip broadcast
  255, 255, -> low source ip broadcast 255.255.0.0.  
  240, 48, 1, 12, -> ofset(where in memory we're operating)
  0, 4, -> Length, number of bytes to read
  0, 0 -> termination

# so then you want to know wtf the register is all your docs in hex:
FFFFF030010C,Milliseconds since powerup,73882846
Opto MMP is on by default, can not be shut off, and controls everything the Opto devices do.
it also requires no passwords, or checksums! 
