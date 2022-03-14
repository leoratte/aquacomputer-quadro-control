from dataclasses import dataclass, field
from enum import Enum


@dataclass
class FlowSensor:
    ticks_per_liter: int = 169
    correction_factor: float = 0.0

@dataclass
class FanSetup:
    hold_min_power: bool = False
    start_boost: bool = True
    min_percent: int = 5
    max_percent: int = 100
    fallback: int = 100
    graph_rpm: int = 2000

class FanCtrlMode(Enum):
    PWM = 0
    TEMP_TARGET = 1
    CURVE = 2
    FAN1 = 3
    FAN2 = 4
    FAN3 = 5
    FAN4 = 6

@dataclass
class TempTargetMode:
    temp_target: float = 35.0
    P: int = 0
    I: int = 0
    D1: int = 0
    D2: float = 0.0
    hysteresis: float = 0.0

@dataclass
class Curve_mode:
    start_temp: int = 28
    temp: list[float] = field(default_factory=lambda: [27.0, 28.1, 28.9, 29.8, 30.6, 31.5, 32.29, 33.2, 34.0, 34.9, 35.7, 36.6, 37.4, 38.29, 39.1, 40.0])
    percent: list[float] = field(default_factory=lambda: [0.0, 1.4, 2.8, 5.0, 8.0, 12.0, 16.8, 22.6, 29.2, 36.6, 45.0, 54.2, 64.4, 75.4, 87.2, 100.0])

@dataclass
class Fan:
    mode: FanCtrlMode = FanCtrlMode.PWM
    pwm: int = 100
    temp_sensor: int = -1
    temp_target_vars: TempTargetMode = TempTargetMode()
    curve_mode_vars: Curve_mode = Curve_mode()

@dataclass
class RGB:
    brightness: int = 255
    on: bool = True

@dataclass
class QuadroConfig:
    aquabus: int = 28
    flow_sensor: FlowSensor = FlowSensor()
    temp_sensors: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])
    fan_setups: list[FanSetup] = field(default_factory=lambda: [FanSetup(), FanSetup(), FanSetup(), FanSetup()])
    fans: list[Fan] = field(default_factory=lambda: [Fan(), Fan(), Fan(), Fan()])
    rgb: RGB = RGB()
    profile: int = 1

