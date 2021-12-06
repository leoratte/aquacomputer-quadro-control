import usb
import usb.core
import usb.util
from time import sleep

from constants import *


class Quadro(object):
    # usb identification of aquacomputer quadro
    VID = 0x0c70
    PID = 0xf00d

    def __init__(self):
        self._had_driver = False
        self._dev = usb.core.find(idVendor=Quadro.VID, idProduct=Quadro.PID)

        if self._dev is None:
            raise ValueError("Device not found")

        if self._dev.is_kernel_driver_active(1):
            self._dev.detach_kernel_driver(1)
            self._had_driver = True

        self._dev.set_configuration()
        self.data = []

    # call before
    def __del__(self):
        """Closes connection with the device and reattatches driver"""
        usb.util.release_interface(self._dev, 1)
        if self._had_driver:
            self._dev.attach_kernel_driver(1)
    
    # read current config data from quadro
    def readConfig(self):
        """read current config data from quadro and store in self.data"""
        bmRequestType=0xa1
        bRequest=0x01
        wValue=0x0303
        wIndex=0x01
        wLength=1013
        self.data = self._dev.ctrl_transfer(bmRequestType, bRequest, wValue=wValue, wIndex=wIndex, data_or_wLength=wLength)   

    def writeConfig(self):
        """write config data to quadro
        not working, computation of checksum needed"""
        # TODO calculate checksum in last two bytes of self.data
        bmRequestType=0x21
        bRequest=0x09
        wValue=0x0303
        wIndex=0x01
        self._dev.ctrl_transfer(bmRequestType, bRequest, wValue=wValue, wIndex=wIndex, data_or_wLength=self.data)

    def readParameter(self, parameter):
        """Returns value from self.data"""
        (positon, length) = parameter
        ret = 0
        for i in range(length):
            ret = ret * 0x100 + self.data[positon + i]
        return ret

    def writeParameter(self, value, parameter):

        (positon, length) = parameter
        for i in range(length-1,-1,-1):
            self.data[positon + i] = value % 0x100
            value //= 0x100

    def importConfigHexDump(self, filename):
        file = open(filename,'rt')
        data = []
        for line in file:
            line = line[4:].strip().split(' ')
            for element in line:
                data.append(int(element,base=16))
        self.data = data[0x40:]
        file.close()

    def importConfigJson(self, filename):
        file = open(filename,'rt')
        # TODO
        file.close()

    def exportConfigJson(self, filename):
        file = open(filename,'rt')
        # TODO
        file.close()
