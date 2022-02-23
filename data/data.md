## captured data
- data0.txt to data6.txt contain captured usb packets with addresses
- addresses 0000 to 003f contain the usb header
- actual data starts at address 0040
- the last two bytes are the checksum
- d0 to d6 contain only packet data and checksum
- d5 and d6 only differ in profile number and checksum

