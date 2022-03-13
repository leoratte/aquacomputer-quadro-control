#!/bin/python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QCheckBox


import quadro
from structure import FanCtrlMode

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Quadro Control')

        self.q = quadro.Quadro()
        self.generateInputFields()
        self._createMenu()
        self._createCentralWidget()

    def _createMenu(self):
        self.menu = self.menuBar()
        # self.menu.addAction('&Exit', self.close)
        self.menu.addAction('&Connect to Device', self.q.connect)
        self.menu.addAction('&Read Config from Device', self._read)
        self.menu.addAction('&Write Config to Device', self._write)
        self.menu.addAction('&Import JSON', self._import)
        self.menu.addAction('&Export JSON', self._export)

    def _read(self):
        self.q.readConfig()
        self.configToForm()

    def _write(self):
        self.formToConfig()
        # self.q.writeConfig()
        print(self.q.config)

    def _import(self):
        filename = QFileDialog.getOpenFileName(filter="JSON Files (*.json)")[0]
        if filename != "":
            self.q.importConfigJson(filename)
            self.configToForm()

    def _export(self):
        self.formToConfig()
        filename = QFileDialog.getSaveFileName(filter="JSON Files (*.json)")[0]
        if filename != "":
            self.q.exportConfigJson(filename)

    def _createCentralWidget(self):
        window = QWidget()
        mainLayout = QVBoxLayout()

        first = QHBoxLayout()

        # aquabus and flwo sensor settings
        form = QFormLayout()
        form.addRow('aquabus', self.aquabus)
        first.addLayout(form)

        form = QFormLayout()        
        form.addRow('ticks_per_liter', self.flowticks)
        form.addRow('correction_factor', self.flowcorrection)
        first.addLayout(form)

        # temp sensor settings
        form = QFormLayout()
        for i in range(4):
            form.addRow('temp_sensor' + str(i)+ ' offset', self.tempsensors[i])
        first.addLayout(form)
        mainLayout.addLayout(first)

        # fan settings
        second = QHBoxLayout()
        for i in range(4):
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

            second.addLayout(form)
        mainLayout.addLayout(second)

        third = QHBoxLayout()
        form = QFormLayout()
        form.addRow(QLabel('RGB'))
        form.addRow('brightness', self.brightness)
        form.addRow('rgb on', self.rgbon)
        third.addLayout(form)
        mainLayout.addLayout(third)

        window.setLayout(mainLayout)
        self.setCentralWidget(window)

    def formToConfig(self):
        self.q.config.aquabus = int(self.aquabus.text())
        self.q.config.flow_sensor.ticks_per_liter = int(self.flowticks.text())
        self.q.config.flow_sensor.correction_factor = float(self.flowcorrection.text())
        for i in range(4):
            self.q.config.temp_sensors[i] = float(self.tempsensors[i].text())

            # fans
            self.q.config.fan_setups[i].hold_min_power = self.holdminpwm[i].isChecked()
            self.q.config.fan_setups[i].start_boost = self.startboost[i].isChecked()
            self.q.config.fan_setups[i].min_percent = float(self.fanmin[i].text())
            self.q.config.fan_setups[i].max_percent = float(self.fanmax[i].text())
            self.q.config.fan_setups[i].fallback = float(self.fallback[i].text())
       
            self.q.config.fans[i].mode = FanCtrlMode(int(self.fanmode[i].currentIndex()))
            self.q.config.fans[i].pwm = float(self.fanpwm[i].text())
            self.q.config.fans[i].temp_sensor = int(self.fantempsrc[i].text())

            # temp target
            self.q.config.fans[i].temp_target_vars.temp_target = float(self.temptarget[i].text())
            self.q.config.fans[i].temp_target_vars.P = int(self.p[i].text())
            self.q.config.fans[i].temp_target_vars.I = int(self.i[i].text())
            self.q.config.fans[i].temp_target_vars.D1 = int(self.d1[i].text())
            self.q.config.fans[i].temp_target_vars.D2 = float(self.d2[i].text())
            self.q.config.fans[i].temp_target_vars.hysteresis = float(self.hysteresis[i].text())

            # curve mode
            self.q.config.fans[i].curve_mode_vars.start_temp = float(self.fanstarttemp[i].text())
            starttemp = float(self.starttemp[i].text())
            endtemp = float(self.endtemp[i].text())
            startpwm = float(self.startpwm[i].text())
            endpwm = float(self.endpwm[i].text())
            for x in range(16):
                temp = round(starttemp + (endtemp - starttemp) * x / 15, 2)
                pwm = round(startpwm + (endpwm - startpwm) * x / 15, 2)
                self.q.config.fans[i].curve_mode_vars.temp[x] = temp
                self.q.config.fans[i].curve_mode_vars.percent[x] = pwm

        # rgb
        self.q.config.rgb.brightness = int(self.brightness.text())
        self.q.config.rgb.on = self.rgbon.isChecked()

    def configToForm(self):
        self.aquabus.setText(str(self.q.config.aquabus))
        self.flowticks.setText(str(self.q.config.flow_sensor.ticks_per_liter))
        self.flowcorrection.setText(str(self.q.config.flow_sensor.correction_factor))
        for i in range(4):
            self.tempsensors[i].setText(str(self.q.config.temp_sensors[i]))

            # fans
            self.holdminpwm[i].setChecked(self.q.config.fan_setups[i].hold_min_power)
            self.startboost[i].setChecked(self.q.config.fan_setups[i].start_boost)
            self.fanmin[i].setText(str(self.q.config.fan_setups[i].min_percent))
            self.fanmax[i].setText(str(self.q.config.fan_setups[i].max_percent))
            self.fallback[i].setText(str(self.q.config.fan_setups[i].fallback))

            self.fanmode[i].setCurrentIndex(int(self.q.config.fans[i].mode.value))
            self.fanpwm[i].setText((str(self.q.config.fans[i].pwm)))
            self.fantempsrc[i].setText(str(self.q.config.fans[i].temp_sensor))

            # temp target
            self.temptarget[i].setText(str(self.q.config.fans[i].temp_target_vars.temp_target))
            self.p[i].setText(str(self.q.config.fans[i].temp_target_vars.P))
            self.i[i].setText(str(self.q.config.fans[i].temp_target_vars.I))
            self.d1[i].setText(str(self.q.config.fans[i].temp_target_vars.D1))
            self.d2[i].setText(str(self.q.config.fans[i].temp_target_vars.D2))
            self.hysteresis[i].setText(str(self.q.config.fans[i].temp_target_vars.hysteresis))

            # curve mode
            self.fanstarttemp[i].setText(str(self.q.config.fans[i].curve_mode_vars.start_temp))
            self.starttemp[i].setText(str(self.q.config.fans[i].curve_mode_vars.temp[0]))
            self.startpwm[i].setText(str(self.q.config.fans[i].curve_mode_vars.percent[0]))
            self.endtemp[i].setText(str(self.q.config.fans[i].curve_mode_vars.temp[15]))
            self.endpwm[i].setText(str(self.q.config.fans[i].curve_mode_vars.percent[15]))

        # rgb
        self.brightness.setText(str(self.q.config.rgb.brightness))
        self.rgbon.setChecked(self.q.config.rgb.on)
    
    def generateInputFields(self):
        self.aquabus = QLineEdit()
        self.flowticks = QLineEdit()
        self.flowcorrection = QLineEdit()
        self.tempsensors = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]

        # fans
        self.holdminpwm = [QCheckBox(), QCheckBox(), QCheckBox(), QCheckBox()]
        self.startboost = [QCheckBox(), QCheckBox(), QCheckBox(), QCheckBox()]

        self.fanmin = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fanmax = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fallback = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fanmode = []
        for i in range(4):
            cb = QComboBox()
            cb.addItems(['PWM', 'TEMP_TARGET', 'CURVE', 'FAN1', 'FAN2', 'FAN3', 'FAN4'])
            self.fanmode.append(cb)
        self.fanpwm = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fantempsrc = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]

        #target temp mode
        self.temptarget = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.p = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.i = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.d1 = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.d2 = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.hysteresis = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]

        #curve mode
        self.fanstarttemp = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.starttemp = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.startpwm = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.endtemp = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.endpwm = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]

        # rgb
        self.brightness = QLineEdit()
        self.rgbon = QCheckBox()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
