"""
Micropython Multitasking Framework MMF
Demo: Zeitgesteuerte Funktionen

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
app.zaehlerstand = 0

# MMF - Komponenten erzeugen
rot = DigitalOut(0)
gruen = DigitalOut(2)
button_a = ButtonA()
button_b = ButtonB()

# MMF - Komponenten der App hinzufügen
app.add_components(rot, gruen, button_a, button_b)

# Fremdkomponenten erstellen
display = Display()

# Funktionen
def print_text(txt, x, y, scale):
    display.clear_all()
    display.print(txt, x, y, scale)
    display.update()

def aus():
    display.clear_all()
    display.update()
    rot.high = False
    gruen.high = False
    app.stop()
    
def byby():
    app.zaehler.stop()
    print_text("Bye", 40, 80, 10)
    app.after(2000, print_text, "Bis bald", 10, 80, 6)
    app.after(5000, aus)
    
def zaehlen():
    app.zaehlerstand += 1
    print_text(str(app.zaehlerstand), 80, 80, 10)
    
def on_message(sender, topic, data):
    if sender == button_a:
        if topic == 'pressed':
            gruen.high = False
        elif topic == 'released':
            gruen.blink = 2
    if sender == button_b:
        if topic == 'pressed':
            byby()

# Funktionen hinzufügen
app.zaehler = app.add_function(1000, zaehlen)

# MMF - Komponenten vorbereiten
rot.blink = 1
gruen.blink = 2

# App starten
app.run(message=on_message)

