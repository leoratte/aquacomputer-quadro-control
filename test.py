from quadro import Quadro
from constants import *

q = Quadro()
q.readConfig()
print(q.readParameter(FAN1_PWM))
q.close()