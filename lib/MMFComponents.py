"""
Micropython Multitasking Framework MMF
Hardwareunabhängige Basiskomponenten

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 24.03.2023
MIT License gemäss Angaben auf Github
"""

from MMFClasses import *
from machine import Pin


class DigitalIn(Task):
    def __init__(self, num, pullup=True, reverse=True, interval=100, **kwargs):
        super().__init__(interval=interval, **kwargs)
        if num:
            if pullup:
                self.port = Pin(num, Pin.IN, Pin.PULL_UP)
            else:
                self.port = Pin(num, Pin.IN)
        self._num = num
        self._state = 0
        self._reverse = reverse

    def step(self):
        value = self.value
        if value != self._state:
            self._state = value
            self.app.notify(self, "changed", value)

    @property
    def value(self):
        if self._reverse:
            return not self.port.value()
        else:
            return self.port.value()


class Button(DigitalIn):
    def __init__(self, num, pullup=True, reverse=True, interval=100, **kwargs):
        super().__init__(num, pullup, reverse, interval, **kwargs)
        self._press_time = 0

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


class DigitalOut(Task):
    def __init__(self, num, high=False, interval=100, **kwargs):
        super().__init__(interval=interval, **kwargs)
        if num is not None:
            self.port = Pin(num, Pin.OUT)
        self._num = num
        self._state = high
        self._blink = 0
        self._pulse = (0, 0)
        self.active = False
        self.set_state(high)

    def set_blink(self, blink):
        self._blink = blink
        if blink:
            self.interval = 500 // blink
        self.active = blink != 0

    def set_pulse(self, pulse):
        if not pulse: pulse = (0, 0)
        self._pulse = pulse
        periode = pulse[0] + pulse[1]
        if periode:
            self.set_blink(1000 / periode)
        else:
            self.set_blink(0)

    def set_state(self, value):
        state = 1 if value else 0
        self.port.value(state)
        if self._state != state:
            self._state = state
            if self.app:
                self.app.notify(self, 'changed', self._state)

    def toggle(self, blink=0):
        self.set_blink(blink)
        self.set_state(not self._state)

    def step(self):
        if self._pulse and self._pulse != (0, 0):
            self.set_state(1)
            self.app.after(self._pulse[0], self.set_state, 0)
        else:
            self.set_state(not self._state)

    @property
    def high(self):
        return self._state == 1

    @high.setter
    def high(self, value):
        self.set_pulse((0, 0))
        self.set_state(value)

    @property
    def blink(self):
        return self._blink

    @blink.setter
    def blink(self, value):
        self.set_pulse((0, 0))
        self.set_blink(value)

    @property
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, value):
        self.set_pulse(value)
