"""
Micropython Multitasking Framework (MMF)
Die Applikation: Funktionen

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()
app.zaehlerstand = 0
    
def schreibe_text(text):
    print(text)
    
def programmende(text):
    print(text)
    app.stop()

def stoppe_zaehler(text):
    print(text)
    app.zaehler.stop()

def zaehle():
    app.zaehlerstand += 1
    print(f'Stand {app.zaehlerstand} nach {app.zaehlerstand*0.5} Sekunden')
    
app.zaehler = app.add_function(500, zaehle)
app.after(6000, programmende, 'Bei Sekunde 6 wird das Programm beendet.')
app.after(4000, stoppe_zaehler, 'Nach 4 Sekunden wird der Zähler gestoppt.')
app.after(3000, schreibe_text, 'Sekunde 3')
app.after(2000, schreibe_text, 'Sekunde 2')

print('Das Programm wird gestartet')
app.run()
print('Das Programm ist beendet')



    

    


