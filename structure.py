from dataclasses import dataclass
from enum import Enum


@dataclass
class FlowSensor:
    ticks_per_liter: int
    correction_factor: float

@dataclass
class FanSetup:
    hold_min_power: bool
    start_boost: bool
    min_percent: int
    max_percent: int
    fallback: int
    graph_rpm: int

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
    temp_target: float
    P: int
    I: int
    D1: int
    D2: float
    hysteresis: float

@dataclass
class Curve_mode:
    start_temp: int
    temp: list[float]
    percent: list[float]

@dataclass
class Fan:
    mode: FanCtrlMode
    pwm: int
    temp_sensor: int
    temp_target_vars: TempTargetMode
    curve_mode_vars: Curve_mode

@dataclass
class RGB:
    brightness: int
    off: bool

@dataclass
class QuadroConfig:
    aquabus: int
    flow_sensor: FlowSensor
    temp_sensors: list[float]
    fan_setups: list[FanSetup]
    fans: list[Fan]
    rgb: RGB
    profile: int

