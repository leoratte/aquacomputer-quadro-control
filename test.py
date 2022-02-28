#!/bin/python3
from quadro import Quadro
from structure import FanCtrlMode


q = Quadro()
q.connect()
q.readConfig()
q.config.rgb.off=True
q.config.fans[1].pwm=55
q.config.fans[2].mode = FanCtrlMode.FAN1
q.writeConfig()