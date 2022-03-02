#!/bin/python3
from quadro import Quadro

q = Quadro()
q.connect()             # connect to usb device
q.readConfig()          # read current config from quadro
q.config.rgb.off=True   # change values in conig
q.config.fans[1].pwm=55
q.writeConfig()         # write new config back to quadro
