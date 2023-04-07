"""
Micropython Multitasking Framework (MMF)
Demo: Verzögerte Funktionen

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
display = Display()

# MMF - Komponenten erzeugen, hinzufügen und konfigurieren
rot = DigitalOut(0)
gruen = DigitalOut(2)
button_a = ButtonA()
button_b = ButtonB()

app.add_components(rot, gruen, button_a, button_b)

rot.blink = 1
gruen.blink = 2

# Funktionen
def print_text(txt, x, y, scale):
    display.clear_all()
    display.print(txt, x, y, scale)
    display.update()

def aus():
    rot.high = False
    gruen.high = False
    display.clear_all()
    display.update()
    app.stop()    

def byebye():
    print_text("Bye", 40, 80, scale=10)
    app.after(5000, aus) 

# Nachrichtenempfänger
def on_message(sender, topic, data):
    if sender == button_a:
        if topic == 'pressed':
            gruen.high = False
        elif topic == 'released':
            gruen.blink = 2
    if sender == button_b:
        if topic == 'pressed':
            byebye()

# App starten
app.run(message=on_message)

