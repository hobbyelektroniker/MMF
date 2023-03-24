"""
Micropython Multitasking Framework MMF
Unterstützung für Pico Explorer Base (https://shop.pimoroni.com/products/pico-explorer-base)

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 24.03.2023
MIT License gemäss Angaben auf Github
"""

from MMFClasses import *
from MMFComponents import *
from MMF_RP2040 import *
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

class Display(PicoGraphics):
    def __init__(self):
        super().__init__(DISPLAY_PICO_EXPLORER)
        self.fg = self.create_pen(255, 255, 255)
        self.bg = self.create_pen(0, 0, 0)
        self.set_font("bitmap8")
        self.set_pen(self.fg)

    def clear_all(self):
        self.set_pen(self.bg)
        self.clear()
        self.set_pen(self.fg)

    def print(self, text, x, y, scale):
        self.text(text, x, y, scale=scale)

def ButtonA(pullup=True, time=100):
    return Button(12, pullup=pullup, time=time)


def ButtonB(pullup=True, time=100):
    return Button(13, pullup=pullup, time=time)


def ButtonX(pullup=True, time=100):
    return Button(14, pullup=pullup, time=time)


def ButtonY(pullup=True, time=100):
    return Button(15, pullup=pullup, time=time)
