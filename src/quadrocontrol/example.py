#!/bin/python3
from quadrocontrol import quadro.Quadro as Quadro

q = Quadro()
q.connect()             # connect to usb device
q.readConfig()          # read current config from quadro
q.config.rgb.on=False   # change values in config
q.config.fans[1].pwm=55
q.writeConfig()         # write new config back to quadro
q.disconnect()
