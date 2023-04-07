"""
Micropython Multitasking Framework (MMF)
Demo: Das Nachrichtensystem

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

# Importe
from MMF_Explorer import *

# Applikation erzeugen
app = Application()

# MMF - Komponenten erzeugen, hinzufügen und konfigurieren
rot = DigitalOut(0)
gruen = DigitalOut(2)
button_a = Button(12)

app.add_components(rot, gruen, button_a)

rot.blink = 1
gruen.blink = 2

# Nachrichtenempfänger
def on_message(sender, topic, data):
    if sender == button_a:
        if topic == 'pressed':
            gruen.high = False
        elif topic == 'released':
            gruen.blink = 2

# App starten
app.run(message=on_message)

