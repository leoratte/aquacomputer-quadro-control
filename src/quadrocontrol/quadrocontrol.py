#!/bin/python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMessageBox


from quadrocontrol import quadro

from quadrocontrol import inputForms


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Quadro Control')

        self.q = quadro.Quadro()
        self.forms = []
        self.generateInputFields()
        self._createMenu()
        self._createCentralWidget()

        self.configToForm()
        try:
            self.q.connect()
            self._read()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Could not detect device")
            # msg.setIcon(QMessageBox.Error)
            # msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore)
            # msg.setDefaultButton(QMessageBox.Retry)
            # msg.setInformativeText("informative text, ya!")
            # msg.setDetailedText("details")
            msg.exec_()

    
    def closeEvent(self, event):
        self.q.disconnect()

    def _createMenu(self):
        self.menu = self.menuBar()
        # self.menu.addAction('&Exit', self.close)
        # self.menu.addAction('&Connect to Device', self.q.connect)
        # self.menu.addAction('&Disconnect Device', self.q.disconnect)
        # self.menu.addAction('&Read Config from Device', self._read)
        self.menu.addAction('&Write Config to Device', self._write)
        self.menu.addAction('&Import JSON', self._import)
        self.menu.addAction('&Export JSON', self._export)

    def _read(self):
        self.q.readConfig()
        self.configToForm()

    def _write(self):
        self.formToConfig()
        self.q.writeConfig()

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

        flowsensor = inputForms.FlowSensorForm(self.q.config.flow_sensor)
        self.forms.append(flowsensor)
        first.addLayout(flowsensor.layout)

        # temp sensor settings
        tempsensors = inputForms.TempSensorForm(self.q.config.temp_sensors)
        self.forms.append(tempsensors)
        first.addLayout(tempsensors.layout)

        mainLayout.addLayout(first)

        # fans
        fans = inputForms.FanForm(self.q.config.fan_setups, self.q.config.fans)
        self.forms.append(fans)
        mainLayout.addLayout(fans.layout)

        # rgb
        rgb = inputForms.RGBForm(self.q.config.rgb)
        self.forms.append(rgb)
        mainLayout.addLayout(rgb.layout)

        window.setLayout(mainLayout)
        self.setCentralWidget(window)

    def formToConfig(self):
        self.q.config.aquabus = int(self.aquabus.text())
        for e in self.forms:
            e.formToConfig()

    def configToForm(self):
        self.aquabus.setText(str(self.q.config.aquabus))
        for e in self.forms:
            e.configToForm()
    
    def generateInputFields(self):
        self.aquabus = QLineEdit()


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
