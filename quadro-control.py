#!/bin/python3
from fileinput import filename
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
import quadro
import structure

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
        self.menu.addAction('&Connect', self.q.connect)
        self.menu.addAction('&Read Config', self._read)
        self.menu.addAction('&Write Config', self._write)
        self.menu.addAction('&Import JSON', self._import)
        self.menu.addAction('&Export JSON', self._export)

    def _createCentralWidget(self):
        window = QWidget()
        mainLayout = QVBoxLayout()

        first = QHBoxLayout()

        form = QFormLayout()
        form.addRow('aquabus', self.aquabus)
        form.addRow('ticks_per_liter', self.flowticks)
        form.addRow('correction_factor', self.flowcorrection)
        first.addLayout(form)

        form = QFormLayout()
        for i in range(4):
            form.addRow('temp_sensor offset ' + str(i), self.tempsensors[i])
        first.addLayout(form)
        mainLayout.addLayout(first)

        second = QHBoxLayout()
        for i in range(4):
            # fan.addLayout(QLabel('Fan ' + str(i)))
            form = QFormLayout()
            form.addRow(QLabel('Fan ' + str(i)))
            form.addRow('control mode', self.fanmode[i])
            form.addRow('pwm', self.fanpwm[i])
            form.addRow('temp source', self.fantempsrc[i])

            second.addLayout(form)

        mainLayout.addLayout(second)

        window.setLayout(mainLayout)
        self.setCentralWidget(window)


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

    def formToConfig(self):
        self.q.config.aquabus = int(self.aquabus.text())
        self.q.config.flow_sensor.ticks_per_liter = int(self.flowticks.text())
        self.q.config.flow_sensor.correction_factor = float(self.flowcorrection.text())
        for i in range(4):
            self.q.config.temp_sensors[i] = float(self.tempsensors[i].text())

            self.q.config.fans[i].mode = int(self.fanmode[i].currentIndex())
            self.q.config.fans[i].pwm = float(self.fanpwm[i].text())
            self.q.config.fans[i].temp_sensor = int(self.fantempsrc[i].text())

        

    def configToForm(self):
        self.aquabus.setText(str(self.q.config.aquabus))
        self.flowticks.setText(str(self.q.config.flow_sensor.ticks_per_liter))
        self.flowcorrection.setText(str(self.q.config.flow_sensor.correction_factor))
        for i in range(4):
            self.tempsensors[i].setText(str(self.q.config.temp_sensors[i]))

            self.fanmode[i].setCurrentIndex(int(self.q.config.fans[i].mode.value))
            self.fanpwm[i].setText((str(self.q.config.fans[i].pwm)))
            self.fantempsrc[i].setText(str(self.q.config.fans[i].temp_sensor))
        
    
    def generateInputFields(self):
        self.aquabus = QLineEdit()
        self.flowticks = QLineEdit()
        self.flowcorrection = QLineEdit()
        self.tempsensors = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fanmode = []
        self.fanpwm = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fantempsrc = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        for i in range(4):
            cb = QComboBox()
            cb.addItems(['PWM', 'TEMP_TARGET', 'CURVE', 'FAN1', 'FAN2', 'FAN3', 'FAN4'])
            self.fanmode.append(cb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())