"""
Micropython Multitasking Framework (MMF)
PWMOut

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()

rot = PWMOut(0)
input_a = AnalogIn(0)

app.add_components(rot, input_a)
rot.blink = 1

def set_brightness():
    rot.percent = input_a.percent

app.add_function(100, set_brightness)
app.after(10000, rot.set_high, False)
app.after(12000, rot.set_high, True)
app.after(14000, app.stop)

def on_message(sender, topic, data):
    print(sender, topic, data)

app.run(message=on_message)

