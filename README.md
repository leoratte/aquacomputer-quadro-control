# aquacomputer-quadro-control
Control aquacomputer quadro in python from linux.

## capabilities
- read current configuration from device
- import previously captured configuration (see capture config packets)
- easily change value off:
    - fan speed, control mode, control variables, ...
    - sensor correction
    - rgb brightness, rgb on/off

## not implemented
- full rgb controll

## usage
```
from quadro import Quadro

q = Quadro()
q.connect()             # connect to usb device
q.readConfig()          # read current config from quadro
q.config.rgb.off=True   # change values in conig
q.config.fans[1].pwm=55
q.writeConfig()         # write new config back to quadro
```




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

