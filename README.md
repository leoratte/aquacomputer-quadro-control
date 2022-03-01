# aquacomputer-quadro-control
Control aquacomputer quadro in python from linux.

## capabilities
- read current configuration from device
- import previously captured configuration (see capture config packets)
- easily change value of:
    - fan speed, control mode, control variables, ...
    - sensor correction
    - rgb brightness, rgb on/off

## not implemented
- full rgb controll
- config value validation (use at own risk)

## installation
- requirements:
    - python3
    - pip
    - git

```
git clone https://github.com/leoratte/aquacomputer-quadro-control.git
cd aquacomputer-quadro-control
sudo pip install -r requirements.txt
```

- udev rule 
    - substitute `<group>` with own group
    - allows usage without root
    - may require reboot
```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0c70", ATTRS{idProduct}=="f00d", GROUP="<group>", MODE="0660"' | sudo tee /lib/udev/rules.d/99-usb-quadro.rules
```

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

