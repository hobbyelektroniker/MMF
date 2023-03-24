"""
Micropython Multitasking Framework MMF
Demo: Blinkende Leds

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 24.03.2023
MIT License gemäss Angaben auf Github
"""

# Importe
from MMF_Explorer import *

# App erzeugen
app = Application()

# MMF - Komponenten erzeugen
rot = DigitalOut(0)
gruen = DigitalOut(2)

# MMF - Komponenten der App hinzufügen
app.add_components(rot, gruen)

# MMF - Komponenten vorbereiten
rot.blink = 1
gruen.blink = 2

# App starten
app.run()

