from crc import CrcCalculator, Configuration

from structure import *

class QuadroConverter(object):
    def __init__(self):
        self.offset = 0
        width = 16
        poly=0x8005
        reverse_input=True
        reverse_output=True
        init_value=0x0000
        final_xor_value=0x426A
        configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
        use_table = True
        self.crc_calculator = CrcCalculator(configuration, use_table)
        

    def convert(self, length=1, factor=1, signed=False):
        ret = 0
        for i in range(length):
            ret = ret * 0x100 + self.arr[self.offset]
            self.offset += 1
        if signed and (ret & 0x8000):
            print("test")
            ret = ((ret -1) ^ 0xFFFF ) * -1
        return ret/factor

    def pad(self, num):
        self.offset += num

    def arrayToDataclass(self, array):
        self.arr = array
        self.offset = 0x3
    
        aquabus = self.convert()
        self.pad(2)

        ticks_per_liter = self.convert(2,1)
        correction_factor = self.convert(2,100,True)
        flow_sensor = FlowSensor(ticks_per_liter,correction_factor)

        temp_sensors = []
        for i in range(4):
            temp_sensors.append(self.convert(2,100,True))

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
            self.pad(1)
            temp_sensor = self.convert()
            
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
        off = bool(int(self.convert()) & 2)
        rgb = RGB(brightness, off)

        self.offset = 0x3ad
        profile = self.convert()

        return QuadroConfig(aquabus, flow_sensor, temp_sensors, fan_setups, fans, rgb, profile)

    def dataclassToArray(self, dataclass):
        #TODO
        return []
