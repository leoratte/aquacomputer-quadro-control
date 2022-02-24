# aquacomputer-quadro-control

Attempt to control aquacomputer quadro in python.

Currently not able to change the configuration on the device, as the checksum computation algorithm is unknown. I suspect it is some kind of CRC-16.  
Feel free to find a solution to this problem.

## capture config packets from aquasuite in linux
1. load usbmon module
2. run aquasuite in windows vm and pass quadro to vm
3. capture packets in wireshark from usbmon interface

[data](data/) contains usb packets sent by aquasuite

## 
constants.py contains the addresses of some config values

## CRC resources
- http://www.ross.net/crc/crcpaper.html
- https://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html
- https://reveng.sourceforge.io/