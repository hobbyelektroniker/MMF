"""
Micropython Multitasking Framework (MMF)
Demo: Hello World!

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

app.add_components(rot, gruen)

rot.blink = 1
gruen.blink = 2

# App starten
app.run()

