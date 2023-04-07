"""
Micropython Multitasking Framework (MMF)
Die Applikation: millis()

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *
import time

app = Application()

print(app.millis())
time.sleep(0.01)
print(app.millis())

# app.run()



