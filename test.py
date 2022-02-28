#!/bin/python3
import pprint

from quadro import Quadro


q = Quadro()
q.connect()
q.readConfig()
pprint.pprint(q.config.config)