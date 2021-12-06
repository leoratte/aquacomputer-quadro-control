from quadro import Quadro
from constants import *
from quadro import Quadro
from time import sleep

checksum = [0,0]
value = 10000
seaching = True

q = Quadro()
q.readConfig()
print(q.readParameter(FAN1_FALLBACK_RPM))
q.close()