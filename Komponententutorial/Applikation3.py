"""
Micropython Multitasking Framework (MMF)
Die Applikation: Nachrichtensystem

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 03.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_RP2040 import *

app = Application()
app.zaehlerstand = [0, 0]

def zaehle(index, faktor):
    app.zaehlerstand[index] += 1
    stand = app.zaehlerstand[index]
    text = f'Zähler {index}: {stand} nach {stand*faktor} Sekunden'
    app.notify(app.zaehler[index], 'count', text)
    
app.zaehler = [
    app.add_function(500, zaehle, 0, 0.5),
    app.add_function(1000, zaehle, 1, 1)]

app.after(6000, app.stop)
app.after(3000, app.zaehler[0].stop)

def on_message(sender, topic, data):
    if sender == app.zaehler[1]:
        print('   ', sender, topic, data)
    else:
        print(sender, topic, data)

app.run(message=on_message)



    

    


