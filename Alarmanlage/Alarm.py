"""
Micropython Multitasking Framework (MMF)
Alarmanlage

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 07.04.2023
MIT License gemäss Angaben auf Github
"""

from MMF_Explorer import *

app = Application()

# Buzzer vorbereiten
app.buzzer = Buzzer(3)
app.buzzer_freq = 300
app.buzzer_freq_schritt = 20

# MMF - Komponenten
rot = DigitalOut(0)
gruen = DigitalOut(2)
pir = DigitalIn(4, pullup=False)

taster_a = ButtonA()
taster_b = ButtonB()

app.add_components(rot, gruen, taster_a, taster_b, pir)

# Wiederholte Funktionen
def buzzer_alarm():
    app.buzzer.set_tone(app.buzzer_freq)
    app.buzzer_freq += app.buzzer_freq_schritt
    if app.buzzer_freq > 1000 or app.buzzer_freq < 300:
        app.buzzer_freq_schritt *= -1
        
# Gewöhnliche Funktionen
def buzzer_aus():
    app.buzzer_alarm.active = False
    app.buzzer.set_tone(-1)
    
def buzzer_ein():
    app.buzzer_alarm.active = True
    
def alarm_ein():
    gruen.high = False
    rot.blink = 2
    buzzer_ein()

def alarm_aus():
    rot.high = gruen.high = False
    buzzer_aus()
    app.after(5000, gruen.set_high, True)

def programmende():
    alarm_aus()
    app.stop()

# Nachrichtenempfänger
def on_message(sender, topic, data):
    if sender == taster_a and topic == 'released':
        if data > 1000:
            alarm_aus()
        else:
            buzzer_aus()
    elif sender == taster_b and topic == 'released':
        if data < 1000:
            alarm_ein()
        else:
            programmende()
    elif sender == pir:
        if gruen.high:
            alarm_ein()

# Hauptprogramm
app.buzzer_alarm = app.add_function(50, buzzer_alarm)
alarm_aus()
app.run(message=on_message)


