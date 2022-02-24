## captured data
- data0.txt to data7.txt contain captured usb packets with addresses
- addresses 0000 to 003f contain the usb header
- actual data starts at address 0040
- the last two bytes are the checksum
- d0 to d7 contain only packet data and checksum
- d5, d6 and d7 only differ in profile number (1,2,3) and checksum

