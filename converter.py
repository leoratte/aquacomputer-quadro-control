from crc import CrcCalculator, Configuration
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
        width=16
        poly=0x8005
        reverse_input=True
        reverse_output=True
        init_value=0x0000
        final_xor_value=0x426A
        configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
        use_table = True
        self.crc_calculator = CrcCalculator(configuration, use_table)

    def convert(self, length=1, factor=1):
        ret = int.from_bytes(self.arr[self.offset: self.offset + length], 'big', signed=2==length)
        self.offset += length
        if factor > 1:
            return ret/factor
        else:
            return ret

    def pad(self, num):
        self.offset += num

    def arrayToDataclass(self, array: list):
        assert len(array) == 961 
        checksum = self.crc_calculator.calculate_checksum(array[:0x3bf])
        assert int.from_bytes(array[0x3bf: ], 'big', signed=False) == checksum
        self.arr = array
        self.offset = 0x3
    
        aquabus = self.convert()
        self.pad(2)

        ticks_per_liter = self.convert(2,1)
        correction_factor = self.convert(2,100)
        flow_sensor = FlowSensor(ticks_per_liter,correction_factor)

        temp_sensors = []
        for i in range(4):
            temp_sensors.append(self.convert(2,100))

        fan_setups = []
        for i in range(4):
            flags = int(self.convert())
            hold_min_power = bool(flags & 1)
            start_boost = bool(flags & 2)
            min_percent = self.convert(2,100)
            max_percent = self.convert(2,100)
            fallback = self.convert(2,100)
            graph_rpm = self.convert(2,1)
            fan_setups.append(FanSetup(hold_min_power, start_boost, min_percent, max_percent, fallback, graph_rpm))

        fans = []
        for x in range(4):
            mode = FanCtrlMode(self.convert())
            pwm = self.convert(2,100)
            temp_sensor = self.convert(2,1)
            
            temp_target = self.convert(2,100)
            p = self.convert(2,1)
            i = self.convert(2,1)
            d1 = self.convert(2,1)
            d2 = self.convert(2,100)
            hysteresis = self.convert(2,100)
            temp_target_vars = TempTargetMode(temp_target, p, i, d1, d2, hysteresis)
            self.pad(2)
            
            start_temp = self.convert(2,100)
            temp = []
            for i in range(16):
                temp.append(self.convert(2,100))
            percent = []
            for i in range(16):
                percent.append(self.convert(2,100))
            curve_mode_vars = Curve_mode(start_temp, temp, percent)

            fans.append(Fan(mode, pwm, temp_sensor, temp_target_vars, curve_mode_vars))

        self.offset = 0x18a
        brightness = self.convert()
        self.pad(1)
        on = not bool(int(self.convert()) & 2)
        rgb = RGB(brightness, on)

        self.offset = 0x3bd
        profile = self.convert()

        return QuadroConfig(aquabus, flow_sensor, temp_sensors, fan_setups, fans, rgb, profile)
    
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
            self.revert(dataclass.fans[i].temp_target_vars.D1,2,1)
            self.revert(dataclass.fans[i].temp_target_vars.D2,2,100)
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
        checksum = self.crc_calculator.calculate_checksum(self.arr)
        self.arr.extend(int(checksum).to_bytes(2,'big',signed=False))
        return self.arr
