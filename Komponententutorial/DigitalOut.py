"""
Micropython Multitasking Framework (MMF)
DigitalOut

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()

rot = DigitalOut(0)
gruen = DigitalOut(2, high=True)

app.add_components(rot, gruen)

rot.pulse = 100, 900
gruen.blink = 1
app.after(5000, rot.set_high, True)
app.after(5000, gruen.set_high, False)
app.after(7000, rot.toggle)

def on_message(sender, topic, data):
    print(sender, topic, data)

app.run(message=on_message)

