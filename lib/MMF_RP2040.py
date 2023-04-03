"""
Micropython Multitasking Framework MMF
RP2040 Unterstützung

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 24.03.2023
MIT License gemäss Angaben auf Github
"""

from MMFClasses import _Application
from MMFComponents import *
from machine import PWM, ADC
import utime


class Application(_Application):
    @classmethod
    def millis(cls):
        return utime.ticks_ms()

    @classmethod
    def func_name(cls, func):
        return func.__name__


class PWMOut(DigitalOut):
    """
    Zugriff auf native Port: .port
    freq: 7 Hz - 125 MHz
    """
    def __init__(self, num, high=False, interval=100, percent=50, freq=500, **kwargs):
        self.port = PWM(Pin(num))
        super().__init__(0, high=high, interval=interval, **kwargs)
        self._num = num
        self.freq = freq
        self.percent = percent

    def set_state(self, value):
        state = 1 if value else 0
        if state:
            self.port.duty_u16(self._duty)
        else:
            self.port.duty_u16(0)
        if self._state != state:
            self._state = state
            if self.app:
                self.app.notify(self, 'changed', self._state)

    def deinit(self):
        self.port.deinit()

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        self._percent = value
        self._duty = int(65535 / 100 * value) - 1
        if self.high:
            self.port.duty_u16(self._duty)

    @property
    def freq(self):
        return self.port.freq()

    @freq.setter
    def freq(self, value):
        self.port.freq(value)

class AnalogIn(Task):
    def __init__(self, num, interval=100, **kwargs):
        super().__init__(interval=interval, **kwargs)
        self._num = num
        self.port = ADC(Pin(26 + num))

    def step(self):
        pass

    @property
    def value(self):
        return self.port.read_u16()

    @property
    def volt(self):
        return round(3.3 * self.value / 65535, 2)
