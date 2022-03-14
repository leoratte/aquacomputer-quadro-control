from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QCheckBox

from abc import ABC, abstractmethod

from structure import RGB, FlowSensor, FanSetup, Fan,FanCtrlMode


class AquaForm(ABC):
    @abstractmethod
    def _createForm(self):
        pass

    @abstractmethod
    def _createInputFields(self):
        pass

    @abstractmethod
    def configToForm(self):
        pass

    @abstractmethod
    def formToConfig(self):
        pass


class FlowSensorForm(AquaForm):
    def __init__(self, flow_sensor: FlowSensor) -> None:
        self.flow_sensor = flow_sensor
        self._createInputFields()
        self._createForm()

    def _createForm(self):
        form = QFormLayout()   
        form.addRow(QLabel('Flow Sensor'))     
        form.addRow('ticks_per_liter', self.flowticks)
        form.addRow('correction_factor', self.flowcorrection)
        self.layout = form

    def _createInputFields(self):
        self.flowticks = QLineEdit()
        self.flowcorrection = QLineEdit()

    def configToForm(self):
        self.flowticks.setText(str(self.flow_sensor.ticks_per_liter))
        self.flowcorrection.setText(str(self.flow_sensor.correction_factor))

    def formToConfig(self):
        self.flow_sensor.ticks_per_liter = int(self.flowticks.text())
        self.flow_sensor.correction_factor = float(self.flowcorrection.text())


class TempSensorForm(AquaForm):
    def __init__(self, temp_sensors: list[float]) -> None:
        self.temp_sensors = temp_sensors
        self._createInputFields()
        self._createForm()

    def _createForm(self):
        form = QFormLayout()
        for i in range(4):
            form.addRow('temp_sensor' + str(i)+ ' offset', self.tempsensoroffset[i])
        self.layout = form

    def _createInputFields(self):
        self.tempsensoroffset = []
        for i in range(len(self.temp_sensors)):
            self.tempsensoroffset.append(QLineEdit())

    def configToForm(self):
        for i in range(len(self.temp_sensors)):
            self.tempsensoroffset[i].setText(str(self.temp_sensors[i]))

    def formToConfig(self):
        for i in range(len(self.temp_sensors)):
            self.temp_sensors[i] = float(self.tempsensoroffset[i].text())
        

class FanForm(AquaForm):
    def __init__(self, fan_setups:list[FanSetup], fans:list[Fan]) -> None:
        self.fan_setups = fan_setups
        self.fans = fans
        self._createInputFields()
        self._createForm()
        
    def _createForm(self):
        self.layout = QHBoxLayout()
        for i in range(len(self.fans)):
            form = QFormLayout()
            form.addRow(QLabel('Fan ' + str(i)))

            form.addRow('hold min pwm',self.holdminpwm[i])
            form.addRow('start boost',self.startboost[i])

            form.addRow('min pwm', self.fanmin[i])
            form.addRow('max pwm', self.fanmax[i])
            form.addRow('fallback pwm', self.fallback[i])

            form.addRow('control mode', self.fanmode[i])
            form.addRow('pwm', self.fanpwm[i])
            form.addRow('temp source', self.fantempsrc[i])

            # target temp
            form.addRow('target temp', self.temptarget[i])
            form.addRow('P', self.p[i])
            form.addRow('I', self.i[i])
            form.addRow('D1', self.d1[i])
            form.addRow('D2', self.d2[i])
            form.addRow('hysteresis', self.hysteresis[i])

            # curve mode
            form.addRow('fan start temp', self.fanstarttemp[i])
            form.addRow('start temp', self.starttemp[i])
            form.addRow('start pwm', self.startpwm[i])
            form.addRow('end temp', self.endtemp[i])
            form.addRow('end pwm', self.endpwm[i])

            self.layout.addLayout(form)


    def formToConfig(self):
        # fans
        for i in range(len(self.fans)):
            self.fan_setups[i].hold_min_power = self.holdminpwm[i].isChecked()
            self.fan_setups[i].start_boost = self.startboost[i].isChecked()
            self.fan_setups[i].min_percent = float(self.fanmin[i].text())
            self.fan_setups[i].max_percent = float(self.fanmax[i].text())
            self.fan_setups[i].fallback = float(self.fallback[i].text())
       
            self.fans[i].mode = FanCtrlMode(int(self.fanmode[i].currentIndex()))
            self.fans[i].pwm = float(self.fanpwm[i].text())
            self.fans[i].temp_sensor = int(self.fantempsrc[i].text())

            # temp target
            self.fans[i].temp_target_vars.temp_target = float(self.temptarget[i].text())
            self.fans[i].temp_target_vars.P = int(self.p[i].text())
            self.fans[i].temp_target_vars.I = int(self.i[i].text())
            self.fans[i].temp_target_vars.D1 = int(self.d1[i].text())
            self.fans[i].temp_target_vars.D2 = float(self.d2[i].text())
            self.fans[i].temp_target_vars.hysteresis = float(self.hysteresis[i].text())

            # curve mode
            self.fans[i].curve_mode_vars.start_temp = float(self.fanstarttemp[i].text())
            starttemp = float(self.starttemp[i].text())
            endtemp = float(self.endtemp[i].text())
            startpwm = float(self.startpwm[i].text())
            endpwm = float(self.endpwm[i].text())
            for x in range(16):
                temp = round(starttemp + (endtemp - starttemp) * x / 15, 2)
                pwm = round(startpwm + (endpwm - startpwm) * x / 15, 2)
                self.fans[i].curve_mode_vars.temp[x] = temp
                self.fans[i].curve_mode_vars.percent[x] = pwm


    def configToForm(self):
        # fans
        for i in range(len(self.fans)):
            self.holdminpwm[i].setChecked(self.fan_setups[i].hold_min_power)
            self.startboost[i].setChecked(self.fan_setups[i].start_boost)
            self.fanmin[i].setText(str(self.fan_setups[i].min_percent))
            self.fanmax[i].setText(str(self.fan_setups[i].max_percent))
            self.fallback[i].setText(str(self.fan_setups[i].fallback))

            self.fanmode[i].setCurrentIndex(int(self.fans[i].mode.value))
            self.fanpwm[i].setText((str(self.fans[i].pwm)))
            self.fantempsrc[i].setText(str(self.fans[i].temp_sensor))

            # temp target
            self.temptarget[i].setText(str(self.fans[i].temp_target_vars.temp_target))
            self.p[i].setText(str(self.fans[i].temp_target_vars.P))
            self.i[i].setText(str(self.fans[i].temp_target_vars.I))
            self.d1[i].setText(str(self.fans[i].temp_target_vars.D1))
            self.d2[i].setText(str(self.fans[i].temp_target_vars.D2))
            self.hysteresis[i].setText(str(self.fans[i].temp_target_vars.hysteresis))

            # curve mode
            self.fanstarttemp[i].setText(str(self.fans[i].curve_mode_vars.start_temp))
            self.starttemp[i].setText(str(self.fans[i].curve_mode_vars.temp[0]))
            self.startpwm[i].setText(str(self.fans[i].curve_mode_vars.percent[0]))
            self.endtemp[i].setText(str(self.fans[i].curve_mode_vars.temp[15]))
            self.endpwm[i].setText(str(self.fans[i].curve_mode_vars.percent[15]))


    def _createInputFields(self):
        # fans
        self.holdminpwm = []
        self.startboost = []
        self.fanmin = []
        self.fanmax = []
        self.fallback = []
        self.fanmode = []
        self.fanpwm = []
        self.fantempsrc = []

        #target temp mode
        self.temptarget = []
        self.p = []
        self.i = []
        self.d1 = []
        self.d2 = []
        self.hysteresis = []

        #curve mode
        self.fanstarttemp = []
        self.starttemp = []
        self.startpwm = []
        self.endtemp = []
        self.endpwm = []
        for i in range(len(self.fans)):
            self.holdminpwm.append(QCheckBox())
            self.startboost.append(QCheckBox())
            self.fanmin.append(QLineEdit())
            self.fanmax.append(QLineEdit())
            self.fallback.append(QLineEdit())

            cb = QComboBox()
            cb.addItems(['PWM', 'TEMP_TARGET', 'CURVE', 'FAN1', 'FAN2', 'FAN3', 'FAN4'])
            self.fanmode.append(cb)
            self.fanpwm.append(QLineEdit())
            self.fantempsrc.append(QLineEdit())

            self.temptarget.append(QLineEdit())
            self.p.append(QLineEdit())
            self.i.append(QLineEdit())
            self.d1.append(QLineEdit())
            self.d2.append(QLineEdit())
            self.hysteresis.append(QLineEdit())

            self.fanstarttemp.append(QLineEdit())
            self.starttemp.append(QLineEdit())
            self.startpwm.append(QLineEdit())
            self.endtemp.append(QLineEdit())
            self.endpwm.append(QLineEdit())


class RGBForm(AquaForm):
    def __init__(self, rgb: RGB) -> None:
        self.rgb = rgb
        self._createInputFields()
        self._createForm()

    def _createForm(self):
        form = QFormLayout()
        form.addRow(QLabel('RGB'))
        form.addRow('brightness', self.brightness)
        form.addRow('rgb on', self.rgbon) 
        self.layout = form

    def _createInputFields(self):
        self.brightness = QLineEdit()
        self.rgbon = QCheckBox()

    def formToConfig(self):
        self.rgb.brightness = int(self.brightness.text())
        self.rgb.on = self.rgbon.isChecked()

    def configToForm(self):
        self.brightness.setText(str(self.rgb.brightness))
        self.rgbon.setChecked(self.rgb.on)