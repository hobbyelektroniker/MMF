"""
Micropython Multitasking Framework MMF
Hardwareunabhängige Basiskomponenten

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 04.04.2023
MIT License gemäss Angaben auf Github
"""

from MMFClasses import *
from machine import Pin


class DigitalIn(Task):
    def __init__(self, num, pullup=True, interval=100, **kwargs):
        super().__init__(interval=interval, **kwargs)
        if num:
            if pullup:
                self.port = Pin(num, Pin.IN, Pin.PULL_UP)
            else:
                self.port = Pin(num, Pin.IN)
        self._num = num
        self._state = 0

    def step(self):
        value = self.value
        if value != self._state:
            self._state = value
            self.app.notify(self, "changed", value)

    @property
    def value(self):
        return self.port.value()


class Button(DigitalIn):
    def __init__(self, num, pullup=True, reverse=None, interval=100, **kwargs):
        super().__init__(num, pullup, interval, **kwargs)
        self._press_time = 0
        if reverse is None:
            reverse = pullup
        self._reverse = reverse

    def step(self):
        value = self.value
        if value != self._state:
            self._state = value
            self.app.notify(self, "changed", value)
            if value:
                self.app.notify(self, "pressed", value)
                self._press_time = self.app.millis()
            else:
                self.app.notify(self, "released", self.app.millis() - self._press_time)

    @property
    def value(self):
        return not bool(self.port.value()) if self._reverse else bool(self.port.value())


class DigitalOut(Task):
    def __init__(self, num, high=False, interval=100, **kwargs):
        super().__init__(interval=interval, **kwargs)
        if num is not None:
            self.port = Pin(num, Pin.OUT)
        self._num = num
        self._state = 0
        self._default_interval = self.interval
        self.set_high(high)
        
    def set_high(self, value):
        self._blink = 0
        self._pulse = None
        self.set_state(value)

    def set_blink(self, blink):
        self._pulse = None
        self._blink = blink
        self.interval = 500 // blink if blink else self._default_interval

    def set_pulse(self, value):
        if value == (0, 0):
            value = None
        self._pulse = value
        if not value:
            self._blink = 0
            self._interval = self._default_interval
        else:
            self._interval = value[0] + value[1]
            self._blink = 0
            self.set_state(0)

    def set_state(self, value):
        state = 1 if value else 0
        self.port.value(state)
        if self._state != state:
            self._state = state
            if self.app:
                self.app.notify(self, 'changed', state)

    def toggle(self):
        self.set_blink(0)
        self.set_state(not self._state)
        
    def step(self):
        def pulse_off():
            if self._pulse:
                self.set_state(0)

        if self._pulse and not self.high:
            self.set_state(1)
            self.app.after(self._pulse[0], pulse_off)            
        elif self.blink:
            self.set_state(not self._state)

    @property
    def high(self):
        return self._state == 1

    @high.setter
    def high(self, value):
        self.set_high(value)

    @property
    def blink(self):
        return self._blink

    @blink.setter
    def blink(self, value):
        self.set_blink(value)

    @property
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, value):
        self.set_pulse(value)
