"""
Micropython Multitasking Framework (MMF)
AnalogIn

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()

input_a = AnalogIn(0)

app.add_components(input_a)

def messung():
    value = input_a.value
    volt = input_a.volt
    percent = input_a.percent
    print(f'{value} entspricht {volt} Volt ({percent}% der Betriebsspannung.')

app.add_function(500, messung)

def on_message(sender, topic, data):
    print(sender, topic, data)

app.run(message=on_message)

