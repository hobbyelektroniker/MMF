"""
Micropython Multitasking Framework (MMF)
DigitalIn, Button

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()

input_a = DigitalIn(12)
button_b = Button(13)

app.add_components(input_a, button_b)


def on_message(sender, topic, data):
    print(sender, topic, data)


print('input_a beim Start', input_a.value)
print('button_b beim Start', button_b.value)

app.run(message=on_message)

