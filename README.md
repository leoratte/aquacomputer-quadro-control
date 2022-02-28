# aquacomputer-quadro-control
Attempt to control aquacomputer quadro in python.

## capture config packets from aquasuite in linux
1. load usbmon module
2. run aquasuite in windows vm and pass quadro to vm
3. capture packets in wireshark from usbmon interface

[data](data/) contains usb packets sent by aquasuite

## CRC resources
- http://www.ross.net/crc/crcpaper.html
- https://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html
- https://reveng.sourceforge.io/
- https://media.ccc.de/v/eh16-27-how_to_reverese_crcs

## CRC properties
```
width = 16
poly = 0x8005
reverse_input = True
reverse_output = True
init_value = 0x0000
final_xor_value = 0x426A
```

