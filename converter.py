from crccheck.crc import Crc16Usb

from abc import ABC, abstractstaticmethod

from structure import *

class AquaConverter(ABC):
    def convert(offset: int, arr: list, length=1, factor=1):
        ret = int.from_bytes(arr[offset: offset + length], 'big', signed=2==length)
        offset += length
        if factor > 1:
            ret = ret/factor
        return offset, ret

    def revert(offset: int, arr: list, value, length=1,factor=1):
        value = int(value*factor)
        vals = value.to_bytes(length,'big',signed=2==length)
        for i in range(length):
            arr[offset] = vals[i]
            offset += 1
        return offset

    @abstractstaticmethod
    def arrayToDataClass(array):
        pass

    @abstractstaticmethod
    def dataclassToArray(array, dataclass):
        pass

class FlowConverter(AquaConverter):
    pass


class QuadroConverter(object):
    def __init__(self):
        self.offset = 0

    def convert(self, length=1, factor=1):
        ret = int.from_bytes(self.arr[self.offset: self.offset + length], 'big', signed=2==length)
        self.offset += length
        if factor > 1:
            return ret/factor
        else:
            return ret

    def pad(self, num):
        self.offset += num

    def arrayToConfig(self, array: list, config: QuadroConfig):
        assert len(array) == 961 
        checksum = Crc16Usb.calc(array[1:0x3bf])
        assert int.from_bytes(array[0x3bf: ], 'big', signed=False) == checksum
        self.arr = array
        self.offset = 0x3
    
        config.aquabus = self.convert()
        self.pad(2)

        config.flow_sensor.ticks_per_liter = self.convert(2,1)
        config.flow_sensor.correction_factor = self.convert(2,100)

        for i in range(4):
            config.temp_sensors[i] = self.convert(2,100)

        for i in range(4):
            flags = int(self.convert())
            config.fan_setups[i].hold_min_power = bool(flags & 1)
            config.fan_setups[i].start_boost = bool(flags & 2)
            config.fan_setups[i].min_percent = self.convert(2,100)
            config.fan_setups[i].max_percent = self.convert(2,100)
            config.fan_setups[i].fallback = self.convert(2,100)
            config.fan_setups[i].graph_rpm = self.convert(2,1)

        for i in range(4):
            config.fans[i].mode = FanCtrlMode(self.convert())
            config.fans[i].pwm = self.convert(2,100)
            config.fans[i].temp_sensor = self.convert(2,1)
            
            config.fans[i].temp_target_vars.temp_target = self.convert(2,100)
            config.fans[i].temp_target_vars.P = self.convert(2,1)
            config.fans[i].temp_target_vars.I = self.convert(2,1)
            config.fans[i].temp_target_vars.D = self.convert(2,1)
            config.fans[i].temp_target_vars.reset_time = self.convert(2,100)
            config.fans[i].temp_target_vars.hysteresis = self.convert(2,100)
            self.pad(2)
            
            config.fans[i].curve_mode_vars.start_temp = self.convert(2,100)
            for x in range(16):
                config.fans[i].curve_mode_vars.temp[x] = self.convert(2,100)
            for x in range(16):
                config.fans[i].curve_mode_vars.percent[x] = self.convert(2,100)

        self.offset = 0x18a
        config.rgb.brightness = self.convert()
        self.pad(1)
        config.rgb.on = not bool(int(self.convert()) & 2)

        self.offset = 0x3bd
        config.profile = self.convert()
    
    def revert(self,value, length=1,factor=1):
        value = int(value*factor)
        vals = value.to_bytes(length,'big',signed=2==length)
        for i in range(length):
            self.arr[self.offset] = vals[i]
            self.offset += 1

    def dataclassToArray(self, dataclass: QuadroConfig):
        self.offset = 0x3
        self.revert(dataclass.aquabus)
        self.pad(2)
        self.revert(dataclass.flow_sensor.ticks_per_liter,2,1)
        self.revert(dataclass.flow_sensor.correction_factor,2,100)
        for i in range(4):
            self.revert(dataclass.temp_sensors[i],2,100)
        for i in range(4):
            flags = dataclass.fan_setups[i].hold_min_power ^ dataclass.fan_setups[i].start_boost << 1
            self.revert(flags)
            self.revert(dataclass.fan_setups[i].min_percent,2,100)
            self.revert(dataclass.fan_setups[i].max_percent,2,100)
            self.revert(dataclass.fan_setups[i].fallback,2,100)
            self.revert(dataclass.fan_setups[i].graph_rpm,2,1)
        for i in range(4):
            self.revert(dataclass.fans[i].mode.value)
            self.revert(dataclass.fans[i].pwm,2,100)
            self.revert(dataclass.fans[i].temp_sensor,2,1)
            self.revert(dataclass.fans[i].temp_target_vars.temp_target,2,100)
            self.revert(dataclass.fans[i].temp_target_vars.P,2,1)
            self.revert(dataclass.fans[i].temp_target_vars.I,2,1)
            self.revert(dataclass.fans[i].temp_target_vars.D,2,1)
            self.revert(dataclass.fans[i].temp_target_vars.reset_time,2,100)
            self.revert(dataclass.fans[i].temp_target_vars.hysteresis,2,100)
            self.pad(2)
            self.revert(dataclass.fans[i].curve_mode_vars.start_temp,2,100)
            for x in range(16):
                self.revert(dataclass.fans[i].curve_mode_vars.temp[x],2,100)
            for x in range(16):
                self.revert(dataclass.fans[i].curve_mode_vars.percent[x],2,100)
        self.offset = 0x18a
        self.revert(dataclass.rgb.brightness)
        self.pad(1)
        self.revert((not dataclass.rgb.on) << 1)
        self.offset = 0x3bd
        self.revert(dataclass.profile)
        self.arr = self.arr[:0x3bf]
        checksum = Crc16Usb.calc(self.arr[1:])
        self.arr.extend(int(checksum).to_bytes(2,'big',signed=False))
        return self.arr
